#!/usr/bin/env python3
"""Markdown parsing and status metadata utilities for gb-data."""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha1
import json
from pathlib import Path
import re
from typing import TypeAlias
from uuid import UUID

from gbdata import Story, StoryStatus, Task, TaskStatus


@dataclass(frozen=True, slots=True)
class StatusEntry:
    """Status metadata entry from status-map style definitions."""

    val: str
    pat_str: str


StatusMap: TypeAlias = dict[TaskStatus, StatusEntry]

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


def _is_story_prefixed_heading(text: str) -> bool:
    tokens = text.strip().split()
    if not tokens:
        return False
    first = tokens[0].lower()
    if first.startswith("story:"):
        return True
    return len(tokens) > 1 and tokens[1].lower().startswith("story:")


def _strip_story_prefix(text: str) -> str:
    match = re.match(r"^\s*(?:\S+\s+)?(?i:story:)\s*(.*)$", text)
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
    current_story_tasks: list[Task] = []

    current_task_index = 0
    current_task_name: str | None = None
    current_task_status: TaskStatus | None = None
    current_task_detail_lines: list[str] = []

    pending_heading_level: int | None = None
    pending_heading_text: str | None = None

    def start_story(name: str, status: TaskStatus, level: int) -> None:
        nonlocal story_counter, current_story_index, current_story_name
        nonlocal current_story_status, current_story_level, current_story_tasks
        nonlocal current_task_index

        story_counter += 1
        current_story_index = story_counter
        current_story_name = _normalize_name(name, "(unnamed story)")
        current_story_status = _to_story_status(status)
        current_story_level = level
        current_story_tasks = []
        current_task_index = 0

    def finalize_task() -> None:
        nonlocal current_task_name, current_task_status, current_task_detail_lines
        nonlocal current_task_index

        if current_task_name is None or current_task_status is None:
            return

        if current_story_index is None:
            raise ValueError("Internal parser error: task without active story index")

        current_task_index += 1
        task_name = _normalize_name(current_task_name, "(unnamed task)")
        detail_lines = _trim_outer_blank_lines(current_task_detail_lines)
        detail = "\n".join(detail_lines) if detail_lines else None
        task_id = _make_id("task", task_name, current_task_index, parent_order=current_story_index)
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
        current_task_detail_lines = []

    def finalize_story() -> None:
        nonlocal current_story_index, current_story_name, current_story_status
        nonlocal current_story_level, current_story_tasks

        if current_story_name is None or current_story_status is None:
            return

        finalize_task()

        if current_story_index is None:
            raise ValueError("Internal parser error: story without index")

        story_name = _normalize_name(current_story_name, "(unnamed story)")
        story_id = _make_id("story", story_name, current_story_index)
        stories.append(
            Story(
                id=story_id,
                name=story_name,
                status=current_story_status,
                tasks=current_story_tasks or None,
            )
        )

        current_story_index = None
        current_story_name = None
        current_story_status = None
        current_story_level = None
        current_story_tasks = []

    for line in text.splitlines():
        heading_match = _HEADING_RE.match(line)
        if heading_match is not None:
            heading_level = len(heading_match.group(1))
            heading_text = heading_match.group(2).strip()

            if current_story_level is not None and heading_level > current_story_level:
                if current_task_name is not None:
                    current_task_detail_lines.append(line)
                continue

            if current_story_name is not None:
                finalize_story()

            pending_heading_level = None
            pending_heading_text = None

            story_status = detect_status(heading_text, story_patterns)
            if story_status is not None:
                story_name = strip_status_prefix(heading_text, story_status, story_patterns)
                start_story(story_name, story_status, heading_level)
                continue

            if _is_story_prefixed_heading(heading_text):
                story_name = _strip_story_prefix(heading_text)
                start_story(story_name, TaskStatus.DO, heading_level)
                continue

            pending_heading_level = heading_level
            pending_heading_text = heading_text
            continue

        task_status = _task_header_status(line, task_patterns)
        if task_status is not None:
            if current_story_name is None:
                if pending_heading_text is not None and pending_heading_level is not None:
                    start_story(pending_heading_text, TaskStatus.DO, pending_heading_level)
                    pending_heading_level = None
                    pending_heading_text = None
                else:
                    start_story("Unscoped", TaskStatus.DO, 7)

            if current_task_name is not None:
                finalize_task()

            task_name = strip_status_prefix(line, task_status, task_patterns)
            current_task_name = _normalize_name(task_name, "(unnamed task)")
            current_task_status = task_status
            current_task_detail_lines = []
            continue

        if current_task_name is not None:
            current_task_detail_lines.append(line)

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
