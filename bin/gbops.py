#!/usr/bin/env python3
"""gbops - pure operations on gbdata domain types.

This module is the isolation layer for behavior that github.com/psons/gb-data does not
provide. bin/gbdata.py is regenerated from docs/dev/spec/gbdata-spec-2.md and must stay a
plain data-model module, so any upsert/merge/tagging logic lives here instead.

No I/O, no markdown parsing, and no git operations belong in this module.

Public API:
- STORY_ID_ATTR / STORY_NAME_ATTR: attribute keys used to tag bare tasks with their story.
- INCOMPLETE_TASK_STATUSES / DONE_TASK_STATUSES: status classification sets.
- with_attributes / tag_task_with_story / tag_tasks_with_story / story_ref / regroup_tasks_by_story
- upsert_tasks / upsert_story / lift_story_to_top / find_story
- is_incomplete / incomplete_tasks / finished_tasks / stories_with_incomplete_tasks
"""

from __future__ import annotations

from dataclasses import replace

from gbdata import Story, Task, TaskStatus

STORY_ID_ATTR = "storyID"
STORY_NAME_ATTR = "storyName"

INCOMPLETE_TASK_STATUSES = frozenset(
    {
        TaskStatus.DO,
        TaskStatus.IN_PROGRESS,
        TaskStatus.SCHEDULED,
    }
)
# Statuses recorded (harvested) into do.md's '# Completed work' bare task list: a task is done,
# abandoned, or unfinished (given up on for now, but not still actively incomplete work).
HARVEST_TASK_STATUSES = frozenset(
    {
        TaskStatus.COMPLETED,
        TaskStatus.ABANDONED,
        TaskStatus.UNFINISHED,
    }
)

ANONYMOUS_STORY_ID = "anonymous-story"
ANONYMOUS_STORY_NAME = "Completed Tasks"


def with_attributes(obj: Task | Story, **kv: object) -> Task | Story:
    """Return a copy of obj with the given key/value pairs merged into attributes."""
    merged = dict(obj.attributes) if obj.attributes else {}
    merged.update(kv)
    return replace(obj, attributes=merged)


def strip_story_ref(task: Task) -> Task:
    """Return a task without storyID/storyName metadata while preserving all other attributes."""
    if not task.attributes:
        return task
    remaining = {key: value for key, value in task.attributes.items() if key not in {STORY_ID_ATTR, STORY_NAME_ATTR}}
    if not remaining:
        return replace(task, attributes=None)
    return replace(task, attributes=remaining)


def tag_task_with_story(task: Task, story: Story) -> Task:
    """Return a copy of task with storyID/storyName set from story, without overwriting existing values."""
    existing = task.attributes or {}
    updates: dict[str, object] = {}
    if not existing.get(STORY_ID_ATTR):
        updates[STORY_ID_ATTR] = story.id
    if not existing.get(STORY_NAME_ATTR):
        updates[STORY_NAME_ATTR] = story.name
    if not updates:
        return task
    return with_attributes(task, **updates)


def tag_tasks_with_story(story: Story) -> list[Task]:
    """Return story's tasks tagged with storyID/storyName attributes."""
    return [tag_task_with_story(task, story) for task in (story.tasks or [])]


def story_ref(task: Task) -> tuple[str | None, str | None]:
    """Return the (storyID, storyName) attribute values recorded on a task, if any."""
    attributes = task.attributes or {}
    story_id = attributes.get(STORY_ID_ATTR)
    story_name = attributes.get(STORY_NAME_ATTR)
    return (
        str(story_id) if story_id is not None else None,
        str(story_name) if story_name is not None else None,
    )


def regroup_tasks_by_story(tasks: list[Task]) -> list[Story]:
    """Group a bare task list back into Story objects keyed by storyID.

    Tasks without a recorded storyID are collected into a single anonymous story.
    """
    order: list[str] = []
    grouped: dict[str, list[Task]] = {}
    names: dict[str, str | None] = {}

    for task in tasks:
        story_id, story_name = story_ref(task)
        key = story_id if story_id is not None else ANONYMOUS_STORY_ID
        if key not in grouped:
            order.append(key)
            grouped[key] = []
            names[key] = story_name
        grouped[key].append(task)

    stories: list[Story] = []
    for key in order:
        stories.append(
            Story(
                id=key,
                name=names[key] or ANONYMOUS_STORY_NAME,
                status=None,
                description=None,
                maxTasks=None,
                tasks=grouped[key],
                attributes=None,
            )
        )
    return stories


def upsert_tasks(existing: list[Task] | None, incoming: list[Task] | None) -> list[Task]:
    """Merge incoming tasks into existing by id. No task is ever deleted.

    Tasks present in incoming replace the matching existing task in place (preserving
    existing order); tasks only present in incoming are appended in incoming order.
    """
    existing = list(existing or [])
    incoming = list(incoming or [])

    incoming_by_id = {task.id: task for task in incoming}
    merged: list[Task] = []
    seen_ids: set[str] = set()

    for task in existing:
        replacement = incoming_by_id.get(task.id)
        merged.append(replacement if replacement is not None else task)
        seen_ids.add(task.id)

    for task in incoming:
        if task.id not in seen_ids:
            merged.append(task)
            seen_ids.add(task.id)

    return merged


def upsert_story(existing: Story, incoming: Story) -> Story:
    """Field-wise replace of scalar story fields from incoming when set, plus task-wise upsert."""
    updates: dict[str, object] = {}
    if incoming.name:
        updates["name"] = incoming.name
    if incoming.status is not None:
        updates["status"] = incoming.status
    if incoming.description is not None:
        updates["description"] = incoming.description
    if incoming.maxTasks is not None:
        updates["maxTasks"] = incoming.maxTasks
    if incoming.attributes:
        merged_attributes = dict(existing.attributes) if existing.attributes else {}
        merged_attributes.update(incoming.attributes)
        updates["attributes"] = merged_attributes
    updates["tasks"] = upsert_tasks(existing.tasks, incoming.tasks)

    return replace(existing, **updates)


def find_story(stories: list[Story], story: Story) -> Story | None:
    """Find a story in stories matching story by id, falling back to a case-insensitive name match."""
    if story.id:
        for candidate in stories:
            if candidate.id == story.id:
                return candidate

    story_name = (story.name or "").strip().lower()
    if not story_name:
        return None
    for candidate in stories:
        if (candidate.name or "").strip().lower() == story_name:
            return candidate
    return None


def lift_story_to_top(stories: list[Story], story: Story) -> list[Story]:
    """Return stories with story placed at the top, preserving relative order of the rest."""
    return [story] + list(stories)


def is_incomplete(task: Task) -> bool:
    """Return True if task's status is one of the incomplete statuses."""
    return task.status in INCOMPLETE_TASK_STATUSES


def incomplete_tasks(story: Story) -> list[Task]:
    """Return story's tasks that are incomplete."""
    return [task for task in (story.tasks or []) if is_incomplete(task)]


def finished_tasks(story: Story) -> list[Task]:
    """Return story's tasks that are harvestable (completed, abandoned, or unfinished)."""
    return [task for task in (story.tasks or []) if task.status in HARVEST_TASK_STATUSES]


def stories_with_incomplete_tasks(stories: list[Story]) -> list[Story]:
    """Return the stories from stories that contain at least one incomplete task."""
    return [story for story in stories if incomplete_tasks(story)]


__all__ = [
    "STORY_ID_ATTR",
    "STORY_NAME_ATTR",
    "INCOMPLETE_TASK_STATUSES",
    "HARVEST_TASK_STATUSES",
    "ANONYMOUS_STORY_ID",
    "ANONYMOUS_STORY_NAME",
    "with_attributes",
    "strip_story_ref",
    "tag_task_with_story",
    "tag_tasks_with_story",
    "story_ref",
    "regroup_tasks_by_story",
    "upsert_tasks",
    "upsert_story",
    "find_story",
    "lift_story_to_top",
    "is_incomplete",
    "incomplete_tasks",
    "finished_tasks",
    "stories_with_incomplete_tasks",
]
