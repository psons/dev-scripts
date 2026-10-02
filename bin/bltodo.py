#!/usr/bin/env python3
"""bltodo - default backlog.py provider backed by a markdown TODO file.

Public API:
- resolve_todo_file_path: return the TODO path from argument/env/default.
- load_todo_stories: parse TODO markdown into Story objects.
- prioritized / pop_task / pop_story / push_story: backlog provider protocol methods.
- resolve_done_file_path / load_done_stories / archive_completed_stories: done.md archiving.
- build_command_result / parse_args / main: CLI entry points.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
from datetime import datetime, timezone
import getpass
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

import ddf
import ddfmdgbdf  # noqa: F401  (import registers the MDGBDF plugin with ddf.py)
import gbops
import mdgbdata
from gbdata import Story, StoryStatus, Task, TaskStatus

COMPLETED_STORIES = "Completed Stories"

DONE_MD_TEMPLATE = {"rules": [{"pattern": r"^#+\s+Completed Stories\s*$", "ddfType": "MDGBDF"}]}


@dataclass(frozen=True, slots=True)
class BltodoCommandResult:
    """Structured result for bltodo command execution."""

    todo_file: str
    output_text: str


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _git_repo_root(cwd: str | Path | None = None) -> Path | None:
    """Return git repo root for cwd, or None when cwd is not in a git repo."""
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=str(cwd) if cwd is not None else None,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    root = result.stdout.strip()
    return Path(root).resolve() if root else None


def _load_status_maps() -> tuple[mdgbdata.StatusMap, mdgbdata.StatusMap]:
    repo_root = _repo_root()
    story_map = mdgbdata.load_status_map(repo_root / "docs/dev/spec/story_status_metadata.json", StoryStatus)
    task_map = mdgbdata.load_status_map(repo_root / "docs/dev/spec/task_status_metadata.json", TaskStatus)
    return story_map, task_map


def resolve_todo_file_path(todo_file: str | Path | None = None) -> Path:
    """Resolve TODO markdown path from arg, env var, or repo default."""
    if todo_file is not None:
        return Path(todo_file).expanduser().resolve()

    env_path = os.environ.get("BL_TODO_FILE")
    if env_path:
        return Path(env_path).expanduser().resolve()

    git_root = _git_repo_root()
    if git_root is not None:
        return (git_root / "docs/dev/work/TODO.md").resolve()

    return (_repo_root() / "docs/dev/work/TODO.md").resolve()


def resolve_todo_file(todo_file: str | Path | None = None) -> Path:
    """Backward-compatible alias for resolve_todo_file_path."""
    return resolve_todo_file_path(todo_file)


def resolve_done_file_path() -> Path:
    """Resolve the done.md path: git-repo-root relative, not configurable via env var."""
    git_root = _git_repo_root()
    base = git_root if git_root is not None else _repo_root()
    return (base / "docs/dev/work/done/done.md").resolve()


def _recovery_dir_for_todo(todo_file: str | Path | None = None) -> Path:
    todo_path = resolve_todo_file_path(todo_file)
    temp_root = Path(tempfile.gettempdir()) / f"TODO-of-{getpass.getuser()}" / "bltodo-recovery"
    # Namespacing by TODO path avoids collisions across similarly named files.
    namespace = str(todo_path).replace(os.sep, "_").replace(":", "_")
    return temp_root / namespace


def save_recovery(todo_file: str | Path | None = None, keep: int = 4) -> Path:
    """Save a copy of the backlog file into temp recovery storage and prune old copies."""
    if keep < 1:
        raise ValueError("keep must be >= 1")

    source_path = resolve_todo_file_path(todo_file)
    recovery_dir = _recovery_dir_for_todo(source_path)
    recovery_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    suffix = source_path.suffix if source_path.suffix else ".md"
    dest_path = recovery_dir / f"{source_path.stem}.{timestamp}{suffix}"
    shutil.copy2(source_path, dest_path)

    recovery_files = sorted((p for p in recovery_dir.iterdir() if p.is_file()), key=lambda p: p.name, reverse=True)
    for stale in recovery_files[keep:]:
        stale.unlink()

    return dest_path


def show_recovery(todo_file: str | Path | None = None) -> str:
    """Return a printable recovery summary with TODO path, recovery path, and contents."""
    source_path = resolve_todo_file_path(todo_file)
    recovery_dir = _recovery_dir_for_todo(source_path)

    lines = [f"TODO file: {source_path}", f"Recovery dir: {recovery_dir}", "Recovery files:"]
    if recovery_dir.exists():
        entries = sorted(recovery_dir.iterdir(), key=lambda p: p.name)
        if entries:
            lines.extend(f"- {entry.name}" for entry in entries)
        else:
            lines.append("(empty)")
    else:
        lines.append("(missing)")

    return "\n".join(lines)


def _read_stories_from_backlog(
    backlog_path: Path,
    *,
    work_stories_only: bool = False,
) -> list[Story]:
    story_map, task_map = _load_status_maps()
    markdown_text = backlog_path.read_text(encoding="utf-8")
    return mdgbdata.parse_stories_from_markdown(
        markdown_text,
        story_map,
        task_map,
        work_stories_only=work_stories_only,
    )


_STORY_MARKER_RE = re.compile(r"(?i:^story:\W*)")


def _strip_default_story_status(story: Story) -> Story:
    """Drop Story.status back to None when it is the ambiguous default 'do' value.

    'do' is indistinguishable from "no status marker was present" (mdgbdata.py defaults an
    unmarked work story's status to 'do'), so writing it back out as an explicit "d -" prefix
    would fabricate a status marker the source text never actually had. The "Story:" word itself
    is preserved (folded into the name) since mdgbdata.py only emits it when status is set.
    """
    if story.status != StoryStatus.DO:
        return story
    name = story.name or ""
    if _STORY_MARKER_RE.match(name):
        return replace(story, status=None)
    return replace(story, status=None, name=f"Story: {name}" if name else "Story:")


def _write_stories_to_backlog(backlog_path: Path, stories: list[Story]) -> None:
    story_map, task_map = _load_status_maps()
    normalized_stories = [_strip_default_story_status(story) for story in stories]
    markdown_text = mdgbdata.stories_to_markdown_text(normalized_stories, story_map, task_map)
    backlog_path.write_text(markdown_text, encoding="utf-8")


def _find_completed_stories_section(doc: ddf.DDFDoc) -> ddfmdgbdf.MDGBDFSection | None:
    for section in doc.sections:
        heading = section.heading.lstrip("#").strip().lower()
        if heading == COMPLETED_STORIES.lower():
            if not isinstance(section, ddfmdgbdf.MDGBDFSection):
                raise ValueError(
                    f"done.md section '{COMPLETED_STORIES}' was not parsed as MDGBDF; check DONE_MD_TEMPLATE"
                )
            return section
    return None


def _load_done_doc(done_path: Path) -> ddf.DDFDoc:
    if done_path.exists():
        text = done_path.read_text(encoding="utf-8")
        return ddf.parse_from_markdown(text, template=DONE_MD_TEMPLATE)
    return ddf.DDFDoc(sections=[ddfmdgbdf.MDGBDFSection(heading=f"# {COMPLETED_STORIES}", stories=[], heading_level=1)])


def _save_done_doc(done_path: Path, doc: ddf.DDFDoc) -> None:
    done_path.parent.mkdir(parents=True, exist_ok=True)
    done_path.write_text(ddf.serialize_to_markdown(doc), encoding="utf-8")


def load_done_stories(done_file: str | Path | None = None) -> list[Story]:
    """Return the archived Story stack from done.md's '# Completed Stories' section."""
    done_path = Path(done_file).expanduser().resolve() if done_file is not None else resolve_done_file_path()
    section = _find_completed_stories_section(_load_done_doc(done_path))
    return section.stories if section is not None else []


def archive_completed_stories(todo_file: str | Path | None = None) -> list[Story]:
    """Sweep stories whose runtime status resolves to 'completed' out of the backlog and onto
    the done.md '# Completed Stories' stack (most-recently-archived stories first).

    This is a dedicated function, not wired into normalize_backlog or pop_story: only push_story
    invokes it automatically.
    """
    backlog_path = resolve_todo_file_path(todo_file)
    stories = _read_stories_from_backlog(backlog_path)

    remaining: list[Story] = []
    completed: list[Story] = []
    for story in stories:
        if gbops.resolve_story_status(story) == StoryStatus.COMPLETED:
            completed.append(story)
        else:
            remaining.append(story)

    if not completed:
        return []

    save_recovery(backlog_path)
    _write_stories_to_backlog(backlog_path, remaining)

    done_path = resolve_done_file_path()
    doc = _load_done_doc(done_path)
    section = _find_completed_stories_section(doc)
    if section is None:
        section = ddfmdgbdf.MDGBDFSection(heading=f"# {COMPLETED_STORIES}", stories=[], heading_level=1)
        doc.sections.append(section)
    section.stories = [_strip_default_story_status(story) for story in completed] + section.stories
    _save_done_doc(done_path, doc)

    return completed


def normalize_backlog(todo_file: str | Path | None = None) -> Path:
    """Normalize backlog markdown via mdgbdata, saving recovery before write-back."""
    backlog_path = resolve_todo_file_path(todo_file)
    stories = _read_stories_from_backlog(backlog_path)
    save_recovery(backlog_path)
    _write_stories_to_backlog(backlog_path, stories)
    return backlog_path


def load_todo_stories(todo_file: str | Path | None = None) -> list[Story]:
    """Load stories from the configured TODO markdown file."""
    return _read_stories_from_backlog(resolve_todo_file_path(todo_file))


def prioritized(todo_file: str | Path | None = None) -> list[Task]:
    """Return all tasks in priority order based on story/task file order."""
    tasks: list[Task] = []
    for story in load_todo_stories(todo_file):
        if story.tasks:
            tasks.extend(story.tasks)
    return tasks


def pop_task(todo_file: str | Path | None = None) -> Task | None:
    """Return the highest-priority task, if one exists."""
    tasks = prioritized(todo_file)
    return tasks[0] if tasks else None


def pop_story(todo_file: str | Path | None = None) -> Story | None:
    """Pop and return the highest-priority story after normalizing and persisting backlog changes."""
    backlog_path = resolve_todo_file_path(todo_file)

    normalize_backlog(backlog_path)
    stories = _read_stories_from_backlog(backlog_path)

    pop_index = next(
        (index for index, story in enumerate(stories) if story.status is not None or bool(story.tasks)),
        None,
    )
    if pop_index is None:
        return None

    popped_story = stories[pop_index]
    save_recovery(backlog_path)
    del stories[pop_index]
    _write_stories_to_backlog(backlog_path, stories)
    return popped_story


def push_story(story: Story, todo_file: str | Path | None = None) -> Story:
    """Lift story to the top of the backlog, upserting its tasks if it already exists.

    Guarantees ids on existing stories via normalize_backlog, saves a recovery copy of the
    backlog before writing, and never deletes a task (see gbops.upsert_tasks). Afterward,
    archives any story (including this one) whose runtime status now resolves to 'completed'
    onto the done.md stack (see archive_completed_stories).
    """
    backlog_path = resolve_todo_file_path(todo_file)

    normalize_backlog(backlog_path)
    stories = _read_stories_from_backlog(backlog_path)

    save_recovery(backlog_path)

    match = gbops.find_story(stories, story)
    merged = gbops.upsert_story(match, story) if match is not None else story
    remaining = [existing for existing in stories if existing is not match]
    _write_stories_to_backlog(backlog_path, gbops.lift_story_to_top(remaining, merged))

    archive_completed_stories(backlog_path)
    return merged


def build_command_result(todo_file: str | Path | None = None) -> BltodoCommandResult:
    """Build command output containing TODO path and MDGBDF backlog text."""
    path = resolve_todo_file_path(todo_file)
    stories = load_todo_stories(path)
    story_map, task_map = _load_status_maps()
    md_text = mdgbdata.stories_to_markdown_text(stories, story_map, task_map)
    output = f"TODO file: {path}\n{md_text}"
    return BltodoCommandResult(todo_file=str(path), output_text=output)


def _build_parser() -> argparse.ArgumentParser:
    git_root = _git_repo_root()
    if git_root is not None:
        default_todo = (git_root / "docs/dev/work/TODO.md").resolve()
    else:
        default_todo = (_repo_root() / "docs/dev/work/TODO.md").resolve()
    parser = argparse.ArgumentParser(
        prog="bltodo",
        description="Default backlog provider reading stories/tasks from a TODO.md file",
        epilog=(
            "Environment variables:\n"
            "  BL_TODO_FILE  Absolute or relative path to the TODO markdown file.\n"
            f"                If unset, bltodo uses git-root-relative path: {default_todo}"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("show", help="Print TODO path and MDGBDF backlog")
    showdone_parser = subparsers.add_parser("showdone", help="Print done file path and archived completed stories")
    showdone_parser.add_argument(
        "n", nargs="?", type=int, default=None, help="Limit output to the top n completed stories (default: all)"
    )
    subparsers.add_parser("showrecovery", help="Show backlog path, recovery dir, and directory listing")
    recovery_parser = subparsers.add_parser("recovery", help="Save a recovery copy of the TODO file")
    recovery_parser.add_argument("n", nargs="?", type=int, default=4, help="Number of recovery files to keep (default: 4)")
    subparsers.add_parser("help", help="Show command usage summary")
    return parser


def _help_text() -> str:
    return """bltodo - default backlog provider backed by a markdown TODO file

Subcommands:
    help            Print this help message.

    show            Print TODO file path and Markdown GB Data Form (MDGBDF) backlog.

    showdone [n]    Print done file path and completed stories archived in 'done.md', in
                    'Markdown GB Data Form' (MDGBDF). Optional n limits output to the top n
                    completed stories (default: all).

    showrecovery    Show the TODO file path, recovery directory path, and recovery directory listing.

    recovery [n]    Save a recovery copy of the TODO file.
                    Optional n sets number of recovery files to keep (default: 4).
"""


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI args for bltodo."""
    parser = _build_parser()
    return parser.parse_args(list(sys.argv[1:]) if argv is None else argv)


def main(argv: list[str] | None = None) -> int:
    """Run the bltodo command-line interface."""
    args = parse_args(argv)
    command = args.command or "show"

    if command == "help":
        print(_help_text(), end="")
        return 0

    try:
        if command == "show":
            result = build_command_result()
            print(result.output_text, end="")
            return 0

        if command == "showdone":
            done_path = resolve_done_file_path()
            stories = load_done_stories(done_path)
            if args.n is not None:
                stories = stories[: args.n]
            story_map, task_map = _load_status_maps()
            md_text = mdgbdata.stories_to_markdown_text(stories, story_map, task_map)
            print(f"Done file: {done_path}\n{md_text}", end="")
            return 0

        if command == "showrecovery":
            print(show_recovery())
            return 0

        if command == "recovery":
            keep = int(args.n)
            recovery_path = save_recovery(keep=keep)
            print(f"Saved recovery: {recovery_path}")
            return 0

        _build_parser().print_help()
        return 1
    except (FileNotFoundError, ValueError, UnicodeDecodeError, OSError) as exc:
        print(f"Error: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "BltodoCommandResult",
    "resolve_todo_file",
    "resolve_todo_file_path",
    "resolve_done_file_path",
    "load_done_stories",
    "archive_completed_stories",
    "save_recovery",
    "show_recovery",
    "normalize_backlog",
    "load_todo_stories",
    "prioritized",
    "pop_task",
    "pop_story",
    "push_story",
    "build_command_result",
    "parse_args",
    "main",
]
