"""Unit tests for bltodo.push_story (PushStory protocol implementation)."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


_bin_dir = Path(__file__).resolve().parents[1] / "bin"
if str(_bin_dir) not in sys.path:
    sys.path.insert(0, str(_bin_dir))


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


gbdata = _load_module("gbdata", _bin_dir / "gbdata.py")
gbops = _load_module("gbops", _bin_dir / "gbops.py")
_load_module("mdgbdata", _bin_dir / "mdgbdata.py")
bltodo = _load_module("bltodo", _bin_dir / "bltodo.py")

Story = gbdata.Story
Task = gbdata.Task
StoryStatus = gbdata.StoryStatus
TaskStatus = gbdata.TaskStatus


def _write_todo(path: Path) -> None:
    path.write_text(
        "# d - Story: Alpha\n"
        "---\n"
        "id: story-a\n"
        "---\n"
        "d - first task\n"
        "---\n"
        "id: task-1\n"
        "---\n"
        "x - second task\n"
        "---\n"
        "id: task-2\n"
        "---\n"
        "# d - Story: Beta\n"
        "---\n"
        "id: story-b\n"
        "---\n"
        "d - third task\n"
        "---\n"
        "id: task-3\n"
        "---\n",
        encoding="utf-8",
    )


def _recovery_files(todo_file: Path) -> list[Path]:
    recovery_dir = bltodo._recovery_dir_for_todo(todo_file)
    if not recovery_dir.exists():
        return []
    return sorted(recovery_dir.iterdir())


def test_push_story_new_story_lands_at_top(monkeypatch, tmp_path: Path):
    todo_file = tmp_path / "sample.md"
    _write_todo(todo_file)
    monkeypatch.setenv("BL_TODO_FILE", str(todo_file))

    new_story = Story(
        id="story-c",
        name="Gamma",
        status=StoryStatus.DO,
        tasks=[Task(id="task-9", status=TaskStatus.DO, name="new task")],
    )

    result = bltodo.push_story(new_story)

    assert result.id == "story-c"
    stories = bltodo.load_todo_stories()
    assert [s.id for s in stories][0] == "story-c"
    assert [s.id for s in stories] == ["story-c", "story-a", "story-b"]


def test_push_story_existing_story_upserts_tasks_and_lifts_to_top(monkeypatch, tmp_path: Path):
    todo_file = tmp_path / "sample.md"
    _write_todo(todo_file)
    monkeypatch.setenv("BL_TODO_FILE", str(todo_file))

    pushed = Story(
        id="story-b",
        name="Beta Updated",
        status=StoryStatus.DO,
        tasks=[
            Task(id="task-3", status=TaskStatus.COMPLETED, name="third task"),
            Task(id="task-4", status=TaskStatus.DO, name="fourth task"),
        ],
    )

    result = bltodo.push_story(pushed)

    assert result.name == "Beta Updated"
    assert [t.id for t in result.tasks] == ["task-3", "task-4"]
    assert result.tasks[0].status == TaskStatus.COMPLETED

    stories = bltodo.load_todo_stories()
    assert [s.id for s in stories][0] == "story-b"
    assert len(stories) == 2  # story-a remains, story-b lifted (not duplicated)


def test_push_story_no_task_is_ever_deleted(monkeypatch, tmp_path: Path):
    todo_file = tmp_path / "sample.md"
    _write_todo(todo_file)
    monkeypatch.setenv("BL_TODO_FILE", str(todo_file))

    pushed = Story(id="story-a", name="Alpha", status=StoryStatus.DO, tasks=[])

    result = bltodo.push_story(pushed)

    assert [t.id for t in result.tasks] == ["task-1", "task-2"]


def test_push_story_saves_recovery_copy_before_writing(monkeypatch, tmp_path: Path):
    todo_file = tmp_path / "sample.md"
    _write_todo(todo_file)
    monkeypatch.setenv("BL_TODO_FILE", str(todo_file))

    assert _recovery_files(todo_file) == []

    bltodo.push_story(Story(id="story-c", name="Gamma", status=StoryStatus.DO, tasks=[]))

    assert len(_recovery_files(todo_file)) >= 1
