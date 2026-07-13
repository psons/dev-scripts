"""Unit tests for gbdata domain model behavior."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

# Add bin directory to sys.path so we can import gbdata.py
_bin_dir = Path(__file__).resolve().parents[1] / "bin"
if str(_bin_dir) not in sys.path:
    sys.path.insert(0, str(_bin_dir))

_spec = importlib.util.spec_from_file_location("gbdata", _bin_dir / "gbdata.py")
if _spec is None or _spec.loader is None:
    raise RuntimeError("Unable to load gbdata module for tests")
gbdata = importlib.util.module_from_spec(_spec)
sys.modules["gbdata"] = gbdata
_spec.loader.exec_module(gbdata)

TaskStatus = gbdata.TaskStatus
StoryStatus = gbdata.StoryStatus
Task = gbdata.Task
Story = gbdata.Story


def test_task_attributes_defaults_to_none():
    task = Task(id="t1", status=TaskStatus.DO, name="demo")

    assert task.attributes is None


def test_task_attributes_accepts_object_map():
    task = Task(id="t1", status=TaskStatus.DO, name="demo", attributes={"prompt": "build parser"})

    assert task.attributes == {"prompt": "build parser"}


def test_story_status_defaults_to_none():
    story = Story(id="s1", name="demo")

    assert story.status is None


def test_story_status_accepts_enum_or_none():
    with_status = Story(id="s1", name="demo", status=StoryStatus.DO)
    without_status = Story(id="s2", name="demo", status=None)

    assert with_status.status == StoryStatus.DO
    assert without_status.status is None


def test_task_status_values_match_spec():
    assert [status.value for status in TaskStatus] == [
        "abandoned",
        "completed",
        "scheduled",
        "in_progress",
        "unfinished",
        "do",
    ]


def test_story_status_values_match_spec():
    assert [status.value for status in StoryStatus] == [
        "abandoned",
        "completed",
        "scheduled",
        "in_progress",
        "unfinished",
        "do",
    ]
