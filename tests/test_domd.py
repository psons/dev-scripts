"""Unit tests for bin/domd.py, the do.md domain layer."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

_bin_dir = Path(__file__).resolve().parents[1] / "bin"
if str(_bin_dir) not in sys.path:
    sys.path.insert(0, str(_bin_dir))


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, _bin_dir / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


gbdata = _load("gbdata")
gbops = _load("gbops")
mdgbdata = _load("mdgbdata")
ddf = _load("ddf")
ddfmdgbdf = _load("ddfmdgbdf")
bltodo = _load("bltodo")
backlog = _load("backlog")
domd = _load("domd")

TaskStatus = gbdata.TaskStatus
StoryStatus = gbdata.StoryStatus

DO_MD_TEXT = (
    "# Current work\n\n"
    "## d - Story: Alpha\n"
    "d - incomplete task\n\n"
    "x - a completed task\n\n"
    "## Story: Beta\n"
    "x - all done task\n\n"
    "# Completed work\n\n"
    "x - previously completed task\n"
    "---\n"
    "storyID: story-zzz\n"
    "storyName: Old Story\n"
    "---\n"
)


def _write_do_md(tmp_path: Path) -> Path:
    path = tmp_path / "do.md"
    path.write_text(DO_MD_TEXT, encoding="utf-8")
    return path


def test_load_reads_current_and_completed_work_stories(tmp_path: Path):
    path = _write_do_md(tmp_path)
    doc = domd.load(path)

    current_stories = doc.current_work_stories()
    assert [s.name for s in current_stories] == ["Alpha", "Beta"]

    completed_tasks = doc.completed_work_tasks()
    assert completed_tasks[0].name == "previously completed task"


def test_harvest_completed_moves_finished_tasks_and_drops_fully_finished_stories(tmp_path: Path):
    path = _write_do_md(tmp_path)
    doc = domd.load(path)

    harvested = domd.harvest_completed(doc)

    harvested_names = {task.name for task in harvested}
    assert "a completed task" in harvested_names
    assert "all done task" in harvested_names

    current_stories = doc.current_work_stories()
    assert [s.name for s in current_stories] == ["Alpha"]
    assert [t.name for t in current_stories[0].tasks] == ["incomplete task"]

    completed_tasks = doc.completed_work_tasks()
    completed_names = {t.name for t in completed_tasks}
    assert {"previously completed task", "a completed task", "all done task"} <= completed_names

    for task in harvested:
        story_id, story_name = gbops.story_ref(task)
        assert story_id is not None
        assert story_name is not None

    remaining_task = current_stories[0].tasks[0]
    assert remaining_task.attributes is None or ("storyID" not in remaining_task.attributes and "storyName" not in remaining_task.attributes)


def test_append_completed_tasks_uses_a_single_file_input_story_for_bare_tasks(tmp_path: Path):
    path = _write_do_md(tmp_path)
    doc = domd.load(path)
    story = doc.current_work_stories()[0]
    harvested = [gbops.tag_task_with_story(task, story) for task in (story.tasks or [])]

    doc.append_completed_tasks(harvested)

    section = doc._find_section(domd.COMPLETED_WORK)
    assert section is not None
    assert [s.id for s in section.stories] == ["file-input"]
    assert section.stories[0].name == "file-input"

    task_names = [task.name for task in section.stories[0].tasks or []]
    assert "previously completed task" in task_names
    assert "incomplete task" in task_names
    for task in section.stories[0].tasks or []:
        if task.attributes:
            assert "storyID" in task.attributes or "storyName" in task.attributes


def test_stories_to_push_back_returns_only_incomplete_stories(tmp_path: Path):
    path = _write_do_md(tmp_path)
    doc = domd.load(path)
    domd.harvest_completed(doc)

    to_push = domd.stories_to_push_back(doc)

    assert [s.name for s in to_push] == ["Alpha"]


def test_settle_pushes_full_story_back_to_backlog_including_completed_tasks(monkeypatch, tmp_path: Path):
    path = _write_do_md(tmp_path)
    todo_file = tmp_path / "TODO.md"
    todo_file.write_text("", encoding="utf-8")
    monkeypatch.setenv("BL_TODO_FILE", str(todo_file))
    monkeypatch.delenv("BACKLOG_PROVIDER", raising=False)

    captured: dict[str, list[str]] = {}

    def fake_push_story(story, *, provider=None):
        captured["task_names"] = [task.name for task in (story.tasks or [])]
        return story

    monkeypatch.setattr(backlog, "push_story", fake_push_story)

    domd.settle(path)

    assert captured["task_names"] == ["incomplete task", "a completed task"]


def test_finalize_runs_settle_flow_before_returning_finalized_result(monkeypatch, tmp_path: Path):
    path = _write_do_md(tmp_path)
    todo_file = tmp_path / "TODO.md"
    todo_file.write_text("", encoding="utf-8")
    monkeypatch.setenv("BL_TODO_FILE", str(todo_file))
    monkeypatch.delenv("BACKLOG_PROVIDER", raising=False)

    called = []
    real_settle = domd.settle

    def observing_settle(*args, **kwargs):
        called.append("settle")
        return real_settle(*args, **kwargs)

    monkeypatch.setattr(domd, "settle", observing_settle)

    result = domd.finalize(path)

    assert called == ["settle"]
    assert result.command == "finalize"
    assert result.output_text.startswith("do.md finalized:")


def test_save_round_trips_current_work(tmp_path: Path):
    path = _write_do_md(tmp_path)
    doc = domd.load(path)
    domd.harvest_completed(doc)
    domd.save(doc, path)

    reloaded = domd.load(path)
    assert [s.name for s in reloaded.current_work_stories()] == ["Alpha"]


def test_finalize_pushes_incomplete_stories_and_removes_from_do_md(monkeypatch, tmp_path: Path):
    do_md_path = _write_do_md(tmp_path)
    todo_file = tmp_path / "TODO.md"
    todo_file.write_text("", encoding="utf-8")
    monkeypatch.setenv("BL_TODO_FILE", str(todo_file))
    monkeypatch.delenv("BACKLOG_PROVIDER", raising=False)

    result = domd.finalize(do_md_path)

    assert len(result.pushed_stories) == 1
    assert result.pushed_stories[0].name == "Alpha"

    reloaded = domd.load(do_md_path)
    assert reloaded.current_work_stories() == []

    todo_stories = bltodo.load_todo_stories(todo_file)
    assert todo_stories[0].name == "Alpha"
    assert [t.name for t in todo_stories[0].tasks] == ["incomplete task", "a completed task"]


def test_finalize_tolerates_do_md_without_current_work_section(monkeypatch, tmp_path: Path):
    do_md_path = tmp_path / "do.md"
    do_md_path.write_text("---\ntitle: do.md\n---\n# Work Summary\n\nnothing to see here\n", encoding="utf-8")
    todo_file = tmp_path / "TODO.md"
    todo_file.write_text("", encoding="utf-8")
    monkeypatch.setenv("BL_TODO_FILE", str(todo_file))

    result = domd.finalize(do_md_path)

    assert result.pushed_stories == []
    assert result.completed_tasks == []
