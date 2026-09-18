#!/usr/bin/env python3
"""domd - the do.md domain layer used by dtask.

do.md is a DDF document whose '# Current work' and '# Completed work' sections are parsed
as MDGBDF (see ddfmdgbdf.py) via a template, per docs/dev/spec/ddf-plugin-spec.md and
docs/dev/spec/dtask-final-modules-spec.md.

Public API:
- DoDoc: wraps a parsed do.md DDFDoc, exposing current-work/completed-work story/task access.
- load / save: read and write a do.md file as a DoDoc.
- harvest_completed: move completed/abandoned/unfinished tasks out of current work stories
  into the completed work section as a bare, storyID/storyName-tagged task list.
- stories_to_push_back: current-work stories that still have incomplete tasks.
- settle: harvest completed work, push incomplete stories back, drop current work, and save.
- finalize: the full dtask `commit --final` sequence's do.md/backlog operation.
- parse_args / main: CLI entry points (command module pattern).
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass, replace
from pathlib import Path
import sys

import backlog
import ddf
import ddfmdgbdf  # noqa: F401  (import registers the MDGBDF plugin with ddf.py)
import gbops
from gbdata import Story, Task

CURRENT_WORK = "Current work"
COMPLETED_WORK = "Completed work"

DO_MD_TEMPLATE = {
    "rules": [
        {"pattern": r"^#+\s+Current work\s*$", "ddfType": "MDGBDF"},
        {"pattern": r"^#+\s+Completed work\s*$", "ddfType": "MDGBDF"},
    ]
}


@dataclass(frozen=True, slots=True)
class DoMdCommandResult:
    """Structured result for a domd command invocation."""

    command: str
    do_md_path: str
    pushed_stories: list[Story]
    completed_tasks: list[Task]
    output_text: str


class DoMdSectionNotFoundError(ValueError):
    """Raised when do.md is missing a required '# Current work' or '# Completed work' section."""


class DoDoc:
    """Thin wrapper over a DDFDoc parsed from do.md using the MDGBDF plugin template."""

    def __init__(self, doc: ddf.DDFDoc) -> None:
        self.doc = doc

    def _find_section(self, name: str) -> ddfmdgbdf.MDGBDFSection | None:
        for section in self.doc.sections:
            heading = section.heading.lstrip("#").strip().lower()
            if heading == name.lower():
                if not isinstance(section, ddfmdgbdf.MDGBDFSection):
                    raise DoMdSectionNotFoundError(
                        f"do.md section '{name}' was not parsed as MDGBDF; check the DO_MD_TEMPLATE"
                    )
                return section
        return None

    def current_work_stories(self) -> list[Story]:
        """Return the Story objects in the '# Current work' section, or [] if absent."""
        section = self._find_section(CURRENT_WORK)
        return section.stories if section is not None else []

    def set_current_work_stories(self, stories: list[Story]) -> None:
        """Replace the Story list in the '# Current work' section."""
        section = self._find_section(CURRENT_WORK)
        if section is None:
            raise DoMdSectionNotFoundError(f"do.md is missing a '# {CURRENT_WORK}' section")
        section.stories = stories

    def completed_work_tasks(self) -> list[Task]:
        """Return the bare task list recorded in the '# Completed work' section, or [] if absent."""
        section = self._find_section(COMPLETED_WORK)
        if section is None:
            return []
        tasks: list[Task] = []
        for story in section.stories:
            tasks.extend(story.tasks or [])
        return tasks

    def append_completed_tasks(self, tasks: list[Task]) -> None:
        """Append tasks to the '# Completed work' section as a bare (ungrouped) task list."""
        if not tasks:
            return
        section = self._find_section(COMPLETED_WORK)
        if section is None:
            raise DoMdSectionNotFoundError(
                f"do.md is missing a '# {COMPLETED_WORK}' section to record harvested tasks in"
            )
        existing_tasks = self.completed_work_tasks()
        section.stories = gbops.regroup_tasks_by_story(existing_tasks + tasks)

    def drop_stories(self, story_ids) -> None:
        """Remove stories with the given ids from '# Current work'. No-op if the section is absent."""
        section = self._find_section(CURRENT_WORK)
        if section is None:
            return
        ids = set(story_ids)
        section.stories = [story for story in section.stories if story.id not in ids]


def load(path: str | Path) -> DoDoc:
    """Parse a do.md file into a DoDoc."""
    text = Path(path).read_text(encoding="utf-8")
    return DoDoc(ddf.parse_from_markdown(text, template=DO_MD_TEMPLATE))


def save(doc: DoDoc, path: str | Path) -> None:
    """Serialize a DoDoc back to a do.md file."""
    Path(path).write_text(ddf.serialize_to_markdown(doc.doc), encoding="utf-8")


def harvest_completed(doc: DoDoc) -> list[Task]:
    """Move harvestable tasks (completed/abandoned/unfinished) out of current work stories
    and into the completed work section as a storyID/storyName-tagged bare task list.

    Returns the harvested tasks.
    """
    current_stories = doc.current_work_stories()
    if not current_stories:
        return []

    harvested: list[Task] = []
    remaining_stories: list[Story] = []

    for story in current_stories:
        tagged_tasks = gbops.tag_tasks_with_story(story)
        finished_ids = {task.id for task in gbops.finished_tasks(story)}
        remaining_tasks = [task for task in tagged_tasks if task.id not in finished_ids]
        harvested.extend(task for task in tagged_tasks if task.id in finished_ids)

        if remaining_tasks or not finished_ids:
            remaining_stories.append(replace(story, tasks=remaining_tasks or None))
        # A story with no remaining tasks (all harvested) is dropped from current work.

    doc.set_current_work_stories(remaining_stories)
    doc.append_completed_tasks(harvested)
    return harvested


def stories_to_push_back(doc: DoDoc) -> list[Story]:
    """Return current-work stories that still have incomplete tasks."""
    return gbops.stories_with_incomplete_tasks(doc.current_work_stories())


def settle(path: str | Path, *, provider: str | None = None) -> DoMdCommandResult:
    """Settle do.md and the backlog without committing or removing do.md.

    Push failures are fatal: if any push_story call fails, do.md is not modified on disk.
    """
    do_md_path = Path(path)
    doc = load(do_md_path)

    completed_tasks = harvest_completed(doc)

    to_push = stories_to_push_back(doc)
    pushed: list[Story] = []
    for story in to_push:
        pushed.append(backlog.push_story(story, provider=provider))

    doc.drop_stories([story.id for story in to_push])
    save(doc, do_md_path)

    lines = [f"do.md settled: {do_md_path}"]
    lines.append(f"Harvested {len(completed_tasks)} completed task(s).")
    lines.append(f"Pushed {len(pushed)} story(ies) back to the backlog.")
    return DoMdCommandResult(
        command="settle",
        do_md_path=str(do_md_path),
        pushed_stories=pushed,
        completed_tasks=completed_tasks,
        output_text="\n".join(lines) + "\n",
    )


def finalize(path: str | Path, *, provider: str | None = None) -> DoMdCommandResult:
    """Run the do.md/backlog portion of the dtask `commit --final` sequence."""
    result = settle(path, provider=provider)
    return replace(
        result,
        command="finalize",
        output_text=result.output_text.replace("do.md settled:", "do.md finalized:", 1),
    )


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="domd",
        description="do.md domain layer: harvest completed work and push incomplete stories back",
    )
    subparsers = parser.add_subparsers(dest="command")
    finalize_parser = subparsers.add_parser("finalize", help="Harvest completed work and push incomplete stories back")
    finalize_parser.add_argument("path", help="Path to do.md")
    finalize_parser.add_argument("--provider", default=None, help="Backlog provider module name")
    subparsers.add_parser("help", help="Show command usage summary")
    return parser


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments for domd."""
    return _build_parser().parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the domd command-line interface."""
    args = parse_args(argv)

    if args.command in (None, "help"):
        _build_parser().print_help()
        return 0

    try:
        result = finalize(args.path, provider=args.provider)
    except (ValueError, FileNotFoundError, UnicodeDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(result.output_text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "CURRENT_WORK",
    "COMPLETED_WORK",
    "DO_MD_TEMPLATE",
    "DoMdCommandResult",
    "DoMdSectionNotFoundError",
    "DoDoc",
    "load",
    "save",
    "harvest_completed",
    "stories_to_push_back",
    "settle",
    "finalize",
    "parse_args",
    "main",
]
