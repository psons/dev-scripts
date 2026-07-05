#!/usr/bin/env python3
"""bltodo - default backlog provider backed by a markdown TODO file.

Public API:
- resolve_todo_file: return the TODO path from argument/env/default.
- load_todo_stories: parse TODO markdown into Story objects.
- prioritized / pop_task / pop_story: backlog provider protocol methods.
- build_command_result / parse_args / main: CLI entry points.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import os
from pathlib import Path

import mdgbdata
from gbdata import Story, StoryStatus, Task


@dataclass(frozen=True, slots=True)
class BltodoCommandResult:
    """Structured result for bltodo command execution."""

    todo_file: str
    output_text: str


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _load_status_maps() -> tuple[mdgbdata.StatusMap, mdgbdata.StatusMap]:
    repo_root = _repo_root()
    story_map = mdgbdata.load_status_map(repo_root / "docs/dev/spec/story_status_metadata.json")
    task_map = mdgbdata.load_status_map(repo_root / "docs/dev/spec/task_status_metadata.json")
    return story_map, task_map


def resolve_todo_file(todo_file: str | Path | None = None) -> Path:
    """Resolve TODO markdown path from arg, env var, or repo default."""
    if todo_file is not None:
        return Path(todo_file).expanduser().resolve()

    env_path = os.environ.get("BL_TODO_FILE")
    if env_path:
        return Path(env_path).expanduser().resolve()

    return (_repo_root() / "docs/dev/work/TODO.md").resolve()


def load_todo_stories(todo_file: str | Path | None = None) -> list[Story]:
    """Load stories from the configured TODO markdown file."""
    story_map, task_map = _load_status_maps()
    return mdgbdata.parse_stories_from_markdown_file(resolve_todo_file(todo_file), story_map, task_map)


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
    """Return the highest-priority story, or a synthetic story for bare tasks."""
    stories = load_todo_stories(todo_file)
    if stories:
        return stories[0]

    tasks = prioritized(todo_file)
    if not tasks:
        return None

    return Story(
        id="anonymous-story",
        status=StoryStatus.DO,
        name="Anonymous",
        description=None,
        maxTasks=None,
        tasks=tasks,
    )


def build_command_result(todo_file: str | Path | None = None) -> BltodoCommandResult:
    """Build command output containing TODO path and MDGBDF backlog text."""
    path = resolve_todo_file(todo_file)
    stories = load_todo_stories(path)
    story_map, task_map = _load_status_maps()
    md_text = mdgbdata.stories_to_markdown_text(stories, story_map, task_map)
    output = f"TODO file: {path}\n{md_text}"
    return BltodoCommandResult(todo_file=str(path), output_text=output)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI args for bltodo."""
    default_todo = (_repo_root() / "docs/dev/work/TODO.md").resolve()
    parser = argparse.ArgumentParser(
        prog="bltodo",
        description="Default backlog provider reading stories/tasks from a TODO.md file",
        epilog=(
            "Environment variables:\n"
            "  BL_TODO_FILE  Absolute or relative path to the TODO markdown file.\n"
            f"                If unset, bltodo uses: {default_todo}"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the bltodo command-line interface."""
    parse_args(argv)
    try:
        result = build_command_result()
    except (FileNotFoundError, ValueError, UnicodeDecodeError) as exc:
        print(f"Error: {exc}")
        return 1

    print(result.output_text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "BltodoCommandResult",
    "resolve_todo_file",
    "load_todo_stories",
    "prioritized",
    "pop_task",
    "pop_story",
    "build_command_result",
    "parse_args",
    "main",
]
