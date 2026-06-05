#!/usr/bin/env python3
"""Goal Blotter data model types.

This module defines Python types for the Goal Blotter hierarchy described by
`goalBlotter.schema.json` in the gb-data project.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TypeAlias


class TaskStatus(str, Enum):
    """Allowed task status values."""

    ABANDONED = "abandoned"
    COMPLETED = "completed"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    UNFINISHED = "unfinished"
    DO = "do"


@dataclass(frozen=True, slots=True)
class StatusEntry:
    """Status metadata entry from status-map style definitions."""

    val: str
    pat_str: str


StatusMap: TypeAlias = dict[TaskStatus, StatusEntry]


@dataclass(frozen=True, slots=True)
class Task:
    """A single task entry in a story."""

    id: str
    name: str
    status: TaskStatus | None = None
    detail: str | None = None


@dataclass(frozen=True, slots=True)
class Story:
    """A story that groups tasks."""

    id: str
    name: str
    maxTasks: int | None = None
    tasks: list[Task] | None = None


@dataclass(frozen=True, slots=True)
class Goal:
    """A goal that groups stories."""

    id: str
    name: str
    description: str | None = None
    maxStories: int | None = None
    stories: list[Story] | None = None


@dataclass(frozen=True, slots=True)
class TimePriorityBlock:
    """Top-level planning block that groups goals."""

    id: str
    name: str
    sprintMax: int
    goals: list[Goal] | None = None


WorkHierarchy: TypeAlias = TimePriorityBlock
