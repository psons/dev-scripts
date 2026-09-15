#!/usr/bin/env python3
"""backlog - command module for querying prioritized backlog data via plugins.

Public API:
- Prioritized / PopTask / PopStory / PushStory: runtime-checkable plugin protocols.
- resolve_provider_name: choose provider from CLI arg, env, or default.
- load_provider_module: import a provider plugin module.
- run_backlog_command: run a backlog subcommand and return structured output.
- push_story: programmatic entry point to push a Story object to the configured provider.
- parse_args / main: CLI entry points.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import importlib
import os
from pathlib import Path
import sys
from typing import Literal, Protocol, runtime_checkable

import mdgbdata
from gbdata import Story, StoryStatus, Task, TaskStatus


OutputFormat = Literal["mdgbdf", "json"]


@runtime_checkable
class Prioritized(Protocol):
    """Protocol for providers that can return prioritized tasks."""

    def prioritized(self) -> list[Task]:
        """Return tasks in priority order."""


@runtime_checkable
class PopTask(Protocol):
    """Protocol for providers that can return the top-priority task."""

    def pop_task(self) -> Task | None:
        """Return the highest-priority task, if any."""


@runtime_checkable
class PopStory(Protocol):
    """Protocol for providers that can return the top-priority story."""

    def pop_story(self) -> Story | None:
        """Return the highest-priority story, if any."""


@runtime_checkable
class PushStory(Protocol):
    """Protocol for providers that can push a story to the top of the backlog."""

    def push_story(self, story: Story) -> Story:
        """Lift story to the top of the backlog, upserting it if it already exists."""


@dataclass(frozen=True, slots=True)
class BacklogCommandResult:
    """Structured result for a backlog command invocation."""

    command: str
    provider: str
    output_format: OutputFormat
    output_text: str


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _load_status_maps() -> tuple[mdgbdata.StatusMap, mdgbdata.StatusMap]:
    repo_root = _repo_root()
    story_map = mdgbdata.load_status_map(repo_root / "docs/dev/spec/story_status_metadata.json", StoryStatus)
    task_map = mdgbdata.load_status_map(repo_root / "docs/dev/spec/task_status_metadata.json", TaskStatus)
    return story_map, task_map


def _wrap_tasks_as_story(tasks: list[Task], *, name: str) -> Story:
    return Story(
        id="anonymous-story",
        status=StoryStatus.DO,
        name=name,
        description=None,
        maxTasks=None,
        tasks=tasks or None,
    )


def _stories_from_command_result(command: str, plugin: object) -> list[Story]:
    if command == "prioritized":
        if not isinstance(plugin, Prioritized):
            raise ValueError("Configured provider does not implement Prioritized protocol")
        return [_wrap_tasks_as_story(plugin.prioritized(), name="Prioritized Tasks")]

    if command == "poptask":
        if not isinstance(plugin, PopTask):
            raise ValueError("Configured provider does not implement PopTask protocol")
        top_task = plugin.pop_task()
        return [_wrap_tasks_as_story([top_task] if top_task is not None else [], name="Top Task")]

    if command == "popstory":
        if not isinstance(plugin, PopStory):
            raise ValueError("Configured provider does not implement PopStory protocol")
        top_story = plugin.pop_story()
        return [] if top_story is None else [top_story]

    raise ValueError(f"Unknown command: {command}")


def resolve_provider_name(provider: str | None = None) -> str:
    """Resolve provider from argument, env var, or default.

    Precedence:
    1. Explicit provider argument.
    2. BACKLOG_PROVIDER environment variable.
    3. "bltodo" default.
    """
    if provider:
        return provider
    return os.environ.get("BACKLOG_PROVIDER", "bltodo")


def load_provider_module(provider: str):
    """Load a provider plugin module by name."""
    try:
        return importlib.import_module(provider)
    except ModuleNotFoundError as exc:
        raise ValueError(f"Unknown backlog provider '{provider}'") from exc


def _story_from_text(
    text: str,
    input_format: OutputFormat,
    story_map: mdgbdata.StatusMap,
    task_map: mdgbdata.StatusMap,
) -> Story:
    """Parse a single Story (with its tasks) out of MDGBDF or JSON input text."""
    if input_format == "json":
        stories = mdgbdata._stories_from_json_text(text)
    else:
        stories = mdgbdata.parse_stories_from_markdown(text, story_map, task_map)
    if not stories:
        raise ValueError("No story found in pushstory input")
    return stories[0]


def push_story(story: Story, *, provider: str | None = None) -> Story:
    """Push story to the configured provider's backlog via the PushStory protocol."""
    provider_name = resolve_provider_name(provider)
    plugin = load_provider_module(provider_name)
    if not isinstance(plugin, PushStory):
        raise ValueError("Configured provider does not implement PushStory protocol")
    return plugin.push_story(story)


def run_backlog_command(
    *,
    command: str,
    provider: str | None = None,
    output_format: OutputFormat = "mdgbdf",
    input_text: str | None = None,
    input_format: OutputFormat = "mdgbdf",
) -> BacklogCommandResult:
    """Execute a backlog subcommand and render output text.

    The provider module is selected using `provider`, then `BACKLOG_PROVIDER`, then
    defaulting to `bltodo`. For `command="pushstory"`, `input_text` (MDGBDF or JSON, per
    `input_format`) is required and is parsed into the Story to push.
    """
    provider_name = resolve_provider_name(provider)
    plugin = load_provider_module(provider_name)
    story_map, task_map = _load_status_maps()

    if command == "pushstory":
        if input_text is None:
            raise ValueError("pushstory requires input_text (MDGBDF or JSON story content)")
        if not isinstance(plugin, PushStory):
            raise ValueError("Configured provider does not implement PushStory protocol")
        story = _story_from_text(input_text, input_format, story_map, task_map)
        stories = [plugin.push_story(story)]
    else:
        stories = _stories_from_command_result(command, plugin)

    if output_format == "json":
        output_text = mdgbdata.stories_to_json_text(stories)
    else:
        output_text = mdgbdata.stories_to_markdown_text(stories, story_map, task_map)

    return BacklogCommandResult(
        command=command,
        provider=provider_name,
        output_format=output_format,
        output_text=output_text,
    )


def _build_parser() -> argparse.ArgumentParser:
    """Build and return the backlog CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="backlog",
        description="Query prioritized backlog data via a provider plugin",
        epilog=(
            "Environment variables:\n"
            "  BACKLOG_PROVIDER  Provider module name to use when --provider is not set.\n"
            "                    If unset, the backlog provider defaults to: bltodo"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--provider",
        default=None,
        help="Backlog provider module name (default: BACKLOG_PROVIDER or bltodo)",
    )
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument("--mdgbdf", action="store_true", help="Output Markdown GB Data Form")
    output_group.add_argument("--json", action="store_true", help="Output JSON")

    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("prioritized", help="Show prioritized tasks")
    subparsers.add_parser("poptask", help="Show the highest-priority task")
    subparsers.add_parser("popstory", help="Show the highest-priority story")
    pushstory_parser = subparsers.add_parser(
        "pushstory", help="Push a story (from file or stdin) to the top of the backlog"
    )
    pushstory_parser.add_argument(
        "path", nargs="?", help="Optional path to MDGBDF or JSON story content; reads stdin when omitted"
    )
    subparsers.add_parser("help", help="Show command usage summary")

    return parser


def _normalize_output_flag_position(argv: list[str] | None) -> list[str] | None:
    if argv is None:
        return None

    normalized = list(argv)
    for flag in ("--json", "--mdgbdf"):
        if flag not in normalized:
            continue

        flag_index = normalized.index(flag)
        command_index = next(
            (i for i, token in enumerate(normalized) if token in {"prioritized", "poptask", "popstory", "pushstory", "help"}),
            None,
        )
        if command_index is None or flag_index < command_index:
            continue

        normalized.pop(flag_index)
        normalized.insert(command_index, flag)

    return normalized


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments for backlog."""
    parser = _build_parser()
    input_argv = list(sys.argv[1:]) if argv is None else argv
    normalized_argv = _normalize_output_flag_position(input_argv)
    return parser.parse_args(normalized_argv)


def main(argv: list[str] | None = None) -> int:
    """Run the backlog command-line interface."""
    args = parse_args(argv)

    if args.command in (None, "help"):
        _build_parser().print_help()
        return 0

    output_format: OutputFormat = "json" if args.json else "mdgbdf"
    try:
        if args.command == "pushstory":
            input_text = Path(args.path).read_text(encoding="utf-8") if args.path else sys.stdin.read()
            result = run_backlog_command(
                command=args.command,
                provider=args.provider,
                output_format=output_format,
                input_text=input_text,
                input_format=output_format,
            )
        else:
            result = run_backlog_command(
                command=args.command,
                provider=args.provider,
                output_format=output_format,
            )
    except (ValueError, FileNotFoundError, UnicodeDecodeError) as exc:
        print(f"Error: {exc}")
        return 1

    print(result.output_text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "Prioritized",
    "PopTask",
    "PopStory",
    "PushStory",
    "BacklogCommandResult",
    "resolve_provider_name",
    "load_provider_module",
    "run_backlog_command",
    "push_story",
    "parse_args",
    "main",
]
