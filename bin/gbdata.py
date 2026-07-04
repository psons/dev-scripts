#!/usr/bin/env python3
"""Goal Blotter shared domain model types."""

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


class StoryStatus(str, Enum):
    """Allowed story status values."""

    ABANDONED = "abandoned"
    COMPLETED = "completed"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    UNFINISHED = "unfinished"
    DO = "do"


@dataclass(frozen=True, slots=True)
class Task:
    """A single task entry in a story."""

    id: str
    status: TaskStatus
    name: str
    detail: str | None = None
    attribs: dict[str, object] | None = None


@dataclass(frozen=True, slots=True)
class Story:
    """A story that groups tasks."""

    id: str
    status: StoryStatus
    name: str
    description: str | None = None
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


__all__ = [
    "TaskStatus",
    "StoryStatus",
    "Task",
    "Story",
    "Goal",
    "TimePriorityBlock",
    "WorkHierarchy",
]
