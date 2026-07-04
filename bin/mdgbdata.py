#!/usr/bin/env python3
"""Markdown parsing and status metadata utilities for gb-data."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from hashlib import sha1
import json
from pathlib import Path
import re
import sys
from typing import TypeAlias
from uuid import UUID

from gbdata import Story, StoryStatus, Task, TaskStatus


@dataclass(frozen=True, slots=True)
class StatusEntry:
    """Status metadata entry from status-map style definitions."""

    val: str
    pat_str: str


StatusMap: TypeAlias = dict[TaskStatus, StatusEntry]


@dataclass(frozen=True, slots=True)
class MdgbdataCommandResult:
    """Structured result returned by mdgbdata command helpers."""

    command: str
    input_path: str
    output_text: str

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
_WS_RE = re.compile(r"\s+")


def load_status_map(path: str | Path) -> StatusMap:
    """Load status metadata from a JSON file."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError("Status metadata root must be a JSON object")

    status_map: StatusMap = {}
    for key, value in raw.items():
        try:
            status = TaskStatus(key)
        except ValueError as exc:
            raise ValueError(f"Invalid status key: {key}") from exc

        if not isinstance(value, dict):
            raise ValueError(f"Invalid metadata entry for '{key}': expected object")
        if "val" not in value:
            raise ValueError(f"Invalid metadata entry for '{key}': missing field 'val'")
        if "pat_str" not in value:
            raise ValueError(f"Invalid metadata entry for '{key}': missing field 'pat_str'")

        val = value["val"]
        pat_str = value["pat_str"]
        if not isinstance(val, str) or not val.strip():
            raise ValueError(f"Invalid metadata entry for '{key}': field 'val' must be non-empty string")
        if not isinstance(pat_str, str) or not pat_str.strip():
            raise ValueError(f"Invalid metadata entry for '{key}': field 'pat_str' must be non-empty string")

        status_map[status] = StatusEntry(val=val, pat_str=pat_str)

    return status_map


def compile_status_patterns(status_map: StatusMap) -> dict[TaskStatus, re.Pattern[str]]:
    """Compile status-map regex patterns."""
    compiled: dict[TaskStatus, re.Pattern[str]] = {}
    for status, entry in status_map.items():
        try:
            compiled[status] = re.compile(entry.pat_str)
        except re.error as exc:
            raise ValueError(f"Invalid regex for status '{status.value}': {exc}") from exc
    return compiled


def detect_status(
    line: str,
    compiled_patterns: dict[TaskStatus, re.Pattern[str]],
) -> TaskStatus | None:
    """Detect a status from a line using deterministic enum order."""
    for status in TaskStatus:
        pattern = compiled_patterns.get(status)
        if pattern is not None and pattern.match(line):
            return status
    return None


def strip_status_prefix(
    line: str,
    status: TaskStatus,
    compiled_patterns: dict[TaskStatus, re.Pattern[str]],
) -> str:
    """Strip only the matched status marker prefix from a line."""
    pattern = compiled_patterns.get(status)
    if pattern is None:
        return line.strip()

    match = pattern.match(line)
    if match is None:
        return line.strip()
    return line[match.end() :].strip()


def _normalize_for_hash(text: str) -> str:
    return _WS_RE.sub(" ", text.strip())


def _hash8(text: str) -> str:
    normalized = _normalize_for_hash(text)
    return sha1(normalized.encode("utf-8")).hexdigest()[:8]


def _normalize_name(text: str, fallback: str) -> str:
    name = text.strip()
    return name if name else fallback


def _trim_outer_blank_lines(lines: list[str]) -> list[str]:
    start = 0
    end = len(lines)
    while start < end and not lines[start].strip():
        start += 1
    while end > start and not lines[end - 1].strip():
        end -= 1
    return lines[start:end]


def _parse_explicit_id_line(line: str) -> str | None:
    if line.startswith((" ", "\t")) or not line.startswith("id:"):
        return None

    value = line[3:].lstrip()
    if not value:
        return None

    return value.split(None, 1)[0]


def _is_story_prefixed_heading(text: str) -> bool:
    tokens = text.strip().split()
    if not tokens:
        return False
    first = tokens[0].lower()
    if first.startswith("story:"):
        return True
    return len(tokens) > 1 and tokens[1].lower().startswith("story:")


def _strip_story_prefix(text: str) -> str:
    match = re.match(r"^\s*(?:[^\s-]+\s*-\s*)?(?i:story:)\s*(.*)$", text)
    if match is None:
        return text.strip()
    return match.group(1).strip()


def _task_header_status(
    line: str,
    compiled_patterns: dict[TaskStatus, re.Pattern[str]],
) -> TaskStatus | None:
    if line.startswith((" ", "\t")):
        return None
    return detect_status(line, compiled_patterns)


def _to_story_status(status: TaskStatus) -> StoryStatus:
    return StoryStatus(status.value)


def _deterministic_uuid7(seed_text: str) -> str:
    # Build a stable UUID with version=7 and RFC 4122 variant bits set.
    data = bytearray(sha1(seed_text.encode("utf-8")).digest()[:16])
    data[6] = (data[6] & 0x0F) | 0x70
    data[8] = (data[8] & 0x3F) | 0x80
    return str(UUID(bytes=bytes(data)))


def _make_id(kind: str, name: str, order: int, parent_order: int | None = None) -> str:
    if parent_order is None:
        seed = f"{kind}:{order}:{_normalize_for_hash(name)}"
    else:
        seed = f"{kind}:{parent_order}:{order}:{_normalize_for_hash(name)}"
    return f"{_deterministic_uuid7(seed)}-{_hash8(name)}"


def parse_stories_from_markdown(
    text: str,
    story_status_map: StatusMap,
    task_status_map: StatusMap,
) -> list[Story]:
    """Parse stories and tasks from markdown text in a single pass."""
    if not text:
        return []

    story_patterns = compile_status_patterns(story_status_map)
    task_patterns = compile_status_patterns(task_status_map)

    stories: list[Story] = []

    story_counter = 0
    current_story_index: int | None = None
    current_story_name: str | None = None
    current_story_status: StoryStatus | None = None
    current_story_level: int | None = None
    current_story_id: str | None = None
    current_story_description_lines: list[str] = []
    current_story_tasks: list[Task] = []
    current_story_expects_id_line = False

    current_task_index = 0
    current_task_name: str | None = None
    current_task_status: TaskStatus | None = None
    current_task_id: str | None = None
    current_task_detail_lines: list[str] = []
    current_task_expects_id_line = False

    pending_heading_level: int | None = None
    pending_heading_text: str | None = None
    pending_heading_description_lines: list[str] = []

    def start_story(
        name: str,
        status: TaskStatus,
        level: int,
        initial_description_lines: list[str] | None = None,
    ) -> None:
        nonlocal story_counter, current_story_index, current_story_name
        nonlocal current_story_status, current_story_level, current_story_description_lines
        nonlocal current_story_id, current_story_tasks, current_story_expects_id_line
        nonlocal current_task_index

        story_counter += 1
        current_story_index = story_counter
        current_story_name = _normalize_name(name, "(unnamed story)")
        current_story_status = _to_story_status(status)
        current_story_level = level
        current_story_id = None
        current_story_description_lines = [] if initial_description_lines is None else list(initial_description_lines)
        current_story_tasks = []
        current_story_expects_id_line = not current_story_description_lines
        current_task_index = 0

    def finalize_task() -> None:
        nonlocal current_task_name, current_task_status, current_task_id, current_task_detail_lines
        nonlocal current_task_index, current_task_expects_id_line

        if current_task_name is None or current_task_status is None:
            return

        if current_story_index is None:
            raise ValueError("Internal parser error: task without active story index")

        current_task_index += 1
        task_name = _normalize_name(current_task_name, "(unnamed task)")
        detail_lines = _trim_outer_blank_lines(current_task_detail_lines)
        detail = "\n".join(detail_lines) if detail_lines else None
        task_id = current_task_id or _make_id("task", task_name, current_task_index, parent_order=current_story_index)
        current_story_tasks.append(
            Task(
                id=task_id,
                name=task_name,
                status=current_task_status,
                detail=detail,
                attribs=None,
            )
        )

        current_task_name = None
        current_task_status = None
        current_task_id = None
        current_task_detail_lines = []
        current_task_expects_id_line = False

    def finalize_story() -> None:
        nonlocal current_story_index, current_story_name, current_story_status
        nonlocal current_story_level, current_story_id, current_story_tasks
        nonlocal current_story_description_lines
        nonlocal current_story_expects_id_line

        if current_story_name is None or current_story_status is None:
            return

        finalize_task()

        if current_story_index is None:
            raise ValueError("Internal parser error: story without index")

        story_name = _normalize_name(current_story_name, "(unnamed story)")
        description_lines = _trim_outer_blank_lines(current_story_description_lines)
        story_description = "\n".join(description_lines) if description_lines else None
        story_id = current_story_id or _make_id("story", story_name, current_story_index)
        stories.append(
            Story(
                id=story_id,
                name=story_name,
                status=current_story_status,
                description=story_description,
                tasks=current_story_tasks or None,
            )
        )

        current_story_index = None
        current_story_name = None
        current_story_status = None
        current_story_level = None
        current_story_id = None
        current_story_description_lines = []
        current_story_tasks = []
        current_story_expects_id_line = False

    for line in text.splitlines():
        heading_match = _HEADING_RE.match(line)
        if heading_match is not None:
            heading_level = len(heading_match.group(1))
            heading_text = heading_match.group(2).strip()

            if current_story_level is not None and heading_level > current_story_level:
                if current_task_name is not None:
                    current_task_detail_lines.append(line)
                else:
                    current_story_description_lines.append(line)
                continue

            if current_story_name is not None:
                finalize_story()

            pending_heading_level = None
            pending_heading_text = None
            pending_heading_description_lines = []

            story_status = detect_status(heading_text, story_patterns)
            if story_status is not None:
                stripped_heading = strip_status_prefix(heading_text, story_status, story_patterns)
                story_name = _strip_story_prefix(stripped_heading)
                start_story(story_name, story_status, heading_level)
                continue

            if _is_story_prefixed_heading(heading_text):
                story_name = _strip_story_prefix(heading_text)
                start_story(story_name, TaskStatus.DO, heading_level)
                continue

            pending_heading_level = heading_level
            pending_heading_text = heading_text
            pending_heading_description_lines = []
            continue

        if current_task_expects_id_line:
            explicit_task_id = _parse_explicit_id_line(line)
            current_task_expects_id_line = False
            if explicit_task_id is not None:
                current_task_id = explicit_task_id
                continue

        if current_story_expects_id_line:
            explicit_story_id = _parse_explicit_id_line(line)
            current_story_expects_id_line = False
            if explicit_story_id is not None:
                current_story_id = explicit_story_id
                continue

        task_status = _task_header_status(line, task_patterns)
        if task_status is not None:
            if current_story_name is None:
                if pending_heading_text is not None and pending_heading_level is not None:
                    start_story(
                        pending_heading_text,
                        TaskStatus.DO,
                        pending_heading_level,
                        initial_description_lines=pending_heading_description_lines,
                    )
                    pending_heading_level = None
                    pending_heading_text = None
                    pending_heading_description_lines = []
                else:
                    start_story("Unscoped", TaskStatus.DO, 7)

            if current_task_name is not None:
                finalize_task()

            task_name = strip_status_prefix(line, task_status, task_patterns)
            current_task_name = _normalize_name(task_name, "(unnamed task)")
            current_task_status = task_status
            current_task_id = None
            current_task_detail_lines = []
            current_task_expects_id_line = True
            continue

        if current_task_name is not None:
            current_task_detail_lines.append(line)
            continue

        if current_story_name is not None:
            current_story_description_lines.append(line)
            continue

        if pending_heading_text is not None:
            pending_heading_description_lines.append(line)

    if current_story_name is not None:
        finalize_story()

    return stories


def parse_stories_from_markdown_file(
    path: str | Path,
    story_status_map: StatusMap,
    task_status_map: StatusMap,
    encoding: str = "utf-8",
) -> list[Story]:
    """Read a markdown file and parse story/task structures from it."""
    text = Path(path).read_text(encoding=encoding)
    return parse_stories_from_markdown(text, story_status_map, task_status_map)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _story_status_entry(status: StoryStatus | TaskStatus, story_status_map: StatusMap) -> StatusEntry:
    return story_status_map[TaskStatus(status.value)]


def _task_status_entry(status: TaskStatus, task_status_map: StatusMap) -> StatusEntry:
    return task_status_map[status]


def _story_to_dict(story: Story) -> dict[str, object]:
    data: dict[str, object] = {
        "id": story.id,
        "status": story.status.value,
        "name": story.name,
    }
    if story.description is not None:
        data["description"] = story.description
    if story.maxTasks is not None:
        data["maxTasks"] = story.maxTasks
    if story.tasks is not None:
        data["tasks"] = [_task_to_dict(task) for task in story.tasks]
    return data


def _task_to_dict(task: Task) -> dict[str, object]:
    data: dict[str, object] = {
        "id": task.id,
        "status": task.status.value,
        "name": task.name,
    }
    if task.detail is not None:
        data["detail"] = task.detail
    if task.attribs is not None:
        data["attribs"] = task.attribs
    return data


def _stories_to_json_text(stories: list[Story]) -> str:
    return json.dumps([_story_to_dict(story) for story in stories], indent=2) + "\n"


def _task_from_mapping(value: object) -> Task:
    if not isinstance(value, dict):
        raise ValueError("Task entry must be a JSON object")

    try:
        task_status = TaskStatus(value["status"])
        task_name = str(value["name"])
        task_id = str(value["id"])
    except KeyError as exc:
        raise ValueError(f"Task entry missing field '{exc.args[0]}'") from exc
    except ValueError as exc:
        raise ValueError(f"Task entry has invalid status: {exc}") from exc

    detail = value.get("detail")
    attribs = value.get("attribs")
    if detail is not None and not isinstance(detail, str):
        raise ValueError("Task detail must be a string when present")
    if attribs is not None and not isinstance(attribs, dict):
        raise ValueError("Task attribs must be an object when present")

    return Task(
        id=task_id,
        status=task_status,
        name=task_name,
        detail=detail,
        attribs=attribs,
    )


def _story_from_mapping(value: object) -> Story:
    if not isinstance(value, dict):
        raise ValueError("Story entry must be a JSON object")

    try:
        story_status = StoryStatus(value["status"])
        story_name = str(value["name"])
        story_id = str(value["id"])
    except KeyError as exc:
        raise ValueError(f"Story entry missing field '{exc.args[0]}'") from exc
    except ValueError as exc:
        raise ValueError(f"Story entry has invalid status: {exc}") from exc

    description = value.get("description")
    max_tasks = value.get("maxTasks")
    tasks_raw = value.get("tasks")
    if description is not None and not isinstance(description, str):
        raise ValueError("Story description must be a string when present")
    if max_tasks is not None and not isinstance(max_tasks, int):
        raise ValueError("Story maxTasks must be an integer when present")
    if tasks_raw is not None and not isinstance(tasks_raw, list):
        raise ValueError("Story tasks must be a list when present")

    tasks = None if tasks_raw is None else [_task_from_mapping(item) for item in tasks_raw]
    return Story(
        id=story_id,
        status=story_status,
        name=story_name,
        description=description,
        maxTasks=max_tasks,
        tasks=tasks,
    )


def _stories_from_json_text(text: str) -> list[Story]:
    try:
        raw = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Input file is not valid JSON: {exc}") from exc

    if not isinstance(raw, list):
        raise ValueError("JSON input must be a list of stories")

    return [_story_from_mapping(item) for item in raw]


def _contains_non_story_text(
    text: str,
    story_patterns: dict[TaskStatus, re.Pattern[str]],
    task_patterns: dict[TaskStatus, re.Pattern[str]],
) -> bool:
    current_story_level: int | None = None
    current_task_active = False
    pending_heading_level: int | None = None
    pending_heading_needs_story = False

    for line in text.splitlines():
        heading_match = _HEADING_RE.match(line)
        if heading_match is not None:
            heading_level = len(heading_match.group(1))
            heading_text = heading_match.group(2).strip()

            if current_story_level is not None and heading_level > current_story_level:
                continue

            current_story_level = None
            current_task_active = False

            if pending_heading_level is not None and pending_heading_needs_story:
                return True
            pending_heading_level = None
            pending_heading_needs_story = False

            story_status = detect_status(heading_text, story_patterns)
            if story_status is not None or _is_story_prefixed_heading(heading_text):
                current_story_level = heading_level
                continue

            pending_heading_level = heading_level
            pending_heading_needs_story = True
            continue

        task_status = _task_header_status(line, task_patterns)
        if task_status is not None:
            current_task_active = True
            if pending_heading_level is not None:
                current_story_level = pending_heading_level
                pending_heading_level = None
                pending_heading_needs_story = False
            elif current_story_level is None:
                current_story_level = 7
            continue

        if not line.strip():
            continue

        if current_task_active or current_story_level is not None:
            continue

        if pending_heading_level is not None:
            pending_heading_needs_story = True
            continue

        return True

    if pending_heading_level is not None and pending_heading_needs_story:
        return True

    return False


def _contains_markdown_structure(text: str, task_patterns: dict[TaskStatus, re.Pattern[str]]) -> bool:
    for line in text.splitlines():
        if _HEADING_RE.match(line) is not None:
            return True
        if _task_header_status(line, task_patterns) is not None:
            return True
    return False


def _render_markdown_story(story: Story, story_status_map: StatusMap, task_status_map: StatusMap) -> list[str]:
    if story.status == StoryStatus.DO:
        lines = [f"# Story: {story.name}"]
    else:
        story_entry = _story_status_entry(story.status, story_status_map)
        lines = [f"# {story_entry.val} - Story: {story.name}"]
    lines.append(f"id: {story.id}")
    if story.description:
        lines.extend(story.description.splitlines())
    if story.tasks:
        for task in story.tasks:
            task_entry = _task_status_entry(task.status, task_status_map)
            lines.append(f"{task_entry.val} - {task.name}")
            lines.append(f"id: {task.id}")
            if task.detail:
                lines.extend(task.detail.splitlines())
    return lines


def stories_to_markdown_text(
    stories: list[Story],
    story_status_map: StatusMap,
    task_status_map: StatusMap,
) -> str:
    lines: list[str] = []
    for index, story in enumerate(stories):
        if index > 0:
            lines.append("")
        lines.extend(_render_markdown_story(story, story_status_map, task_status_map))
    return "\n".join(lines).rstrip() + ("\n" if lines else "")


def convert_markdown_file_to_json_text(
    path: str | Path,
    story_status_map: StatusMap,
    task_status_map: StatusMap,
    encoding: str = "utf-8",
) -> str:
    markdown_text = Path(path).read_text(encoding=encoding)
    story_patterns = compile_status_patterns(story_status_map)
    task_patterns = compile_status_patterns(task_status_map)
    if not _contains_markdown_structure(markdown_text, task_patterns):
        raise ValueError("Input file does not contain any markdown headers or tasks")
    if _contains_non_story_text(markdown_text, story_patterns, task_patterns):
        print("WARNING: some non story text will be ignored", file=sys.stderr)
    stories = parse_stories_from_markdown(markdown_text, story_status_map, task_status_map)
    return _stories_to_json_text(stories)


def convert_json_file_to_markdown_text(
    path: str | Path,
    story_status_map: StatusMap,
    task_status_map: StatusMap,
    encoding: str = "utf-8",
) -> str:
    stories = _stories_from_json_text(Path(path).read_text(encoding=encoding))
    return stories_to_markdown_text(stories, story_status_map, task_status_map)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="mdgbdata",
        description="Convert Markdown GB Data Form to and from JSON",
    )
    subparsers = parser.add_subparsers(dest="command")

    tojson_parser = subparsers.add_parser("tojson", help="Convert Markdown GB Data Form to JSON")
    tojson_parser.add_argument("path", help="Path to a Markdown GB Data Form file")

    tomd_parser = subparsers.add_parser("tomd", help="Convert JSON to Markdown GB Data Form")
    tomd_parser.add_argument("path", help="Path to a JSON file")

    subparsers.add_parser("help", help="Show command usage summary")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = _repo_root()
    story_status_map = load_status_map(repo_root / "docs/dev/spec/story_status_metadata.json")
    task_status_map = load_status_map(repo_root / "docs/dev/spec/task_status_metadata.json")

    if args.command in (None, "help"):
        parser = argparse.ArgumentParser(
            prog="mdgbdata",
            description="Convert Markdown GB Data Form to and from JSON",
        )
        subparsers = parser.add_subparsers(dest="command")
        subparsers.add_parser("tojson", help="Convert Markdown GB Data Form to JSON")
        subparsers.add_parser("tomd", help="Convert JSON to Markdown GB Data Form")
        subparsers.add_parser("help", help="Show command usage summary")
        parser.print_help()
        return 0

    try:
        if args.command == "tojson":
            output_text = convert_markdown_file_to_json_text(args.path, story_status_map, task_status_map)
        elif args.command == "tomd":
            output_text = convert_json_file_to_markdown_text(args.path, story_status_map, task_status_map)
        else:
            raise ValueError(f"Unknown command: {args.command}")
    except (FileNotFoundError, ValueError, UnicodeDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(output_text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "StatusEntry",
    "StatusMap",
    "load_status_map",
    "compile_status_patterns",
    "detect_status",
    "strip_status_prefix",
    "parse_stories_from_markdown",
    "parse_stories_from_markdown_file",
]
