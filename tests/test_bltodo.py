"""Unit tests for bltodo provider behavior."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


_bin_dir = Path(__file__).resolve().parents[1] / "bin"
if str(_bin_dir) not in sys.path:
    sys.path.insert(0, str(_bin_dir))


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module {name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


gbdata = _load_module("gbdata", _bin_dir / "gbdata.py")
_load_module("mdgbdata", _bin_dir / "mdgbdata.py")
bltodo = _load_module("bltodo", _bin_dir / "bltodo.py")


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


def test_resolve_todo_file_uses_env_var(monkeypatch, tmp_path: Path):
    todo_file = tmp_path / "sample.md"
    _write_todo(todo_file)
    monkeypatch.setenv("BL_TODO_FILE", str(todo_file))

    resolved = bltodo.resolve_todo_file()

    assert resolved == todo_file.resolve()


def test_prioritized_returns_tasks_in_file_order(monkeypatch, tmp_path: Path):
    todo_file = tmp_path / "sample.md"
    _write_todo(todo_file)
    monkeypatch.setenv("BL_TODO_FILE", str(todo_file))

    tasks = bltodo.prioritized()

    assert [task.id for task in tasks] == ["task-1", "task-2", "task-3"]


def test_pop_task_returns_top_priority_task(monkeypatch, tmp_path: Path):
    todo_file = tmp_path / "sample.md"
    _write_todo(todo_file)
    monkeypatch.setenv("BL_TODO_FILE", str(todo_file))

    task = bltodo.pop_task()

    assert task is not None
    assert task.id == "task-1"


def test_pop_story_returns_top_priority_story(monkeypatch, tmp_path: Path):
    todo_file = tmp_path / "sample.md"
    _write_todo(todo_file)
    monkeypatch.setenv("BL_TODO_FILE", str(todo_file))

    story = bltodo.pop_story()

    assert story is not None
    assert story.id == "story-a"


def test_main_prints_todo_path_and_mdgbdf(monkeypatch, tmp_path: Path, capsys):
    todo_file = tmp_path / "sample.md"
    _write_todo(todo_file)
    monkeypatch.setenv("BL_TODO_FILE", str(todo_file))

    exit_code = bltodo.main([])
    out = capsys.readouterr().out

    assert exit_code == 0
    assert f"TODO file: {todo_file.resolve()}" in out
    assert "# Story: Alpha" in out
