"""Unit tests for bltodo provider behavior."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
import sys

import pytest

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
gbops = _load_module("gbops", _bin_dir / "gbops.py")
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


def test_resolve_todo_file_defaults_to_caller_git_repo_root(monkeypatch, tmp_path: Path):
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    subprocess.run(["git", "init"], cwd=repo_dir, check=True, capture_output=True, text=True)
    monkeypatch.delenv("BL_TODO_FILE", raising=False)
    monkeypatch.chdir(repo_dir)

    resolved = bltodo.resolve_todo_file_path()

    assert resolved == (repo_dir / "docs/dev/work/TODO.md").resolve()


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
    rewritten = todo_file.read_text(encoding="utf-8")
    assert "Story: Alpha" not in rewritten
    assert "Story: Beta" in rewritten


def test_pop_story_skips_informational_story_and_returns_first_work_story(monkeypatch, tmp_path: Path):
    todo_file = tmp_path / "sample.md"
    todo_file.write_text(
        "# Notes\n"
        "Just informational text\n"
        "# d - Story: Alpha\n"
        "---\n"
        "id: story-a\n"
        "---\n"
        "d - first task\n"
        "---\n"
        "id: task-1\n"
        "---\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("BL_TODO_FILE", str(todo_file))

    story = bltodo.pop_story()

    assert story is not None
    assert story.id == "story-a"


def test_normalize_backlog_adds_ids_and_rewrites(monkeypatch, tmp_path: Path):
    todo_file = tmp_path / "sample.md"
    todo_file.write_text(
        "# d - Story: Alpha\n"
        "d - first task\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("BL_TODO_FILE", str(todo_file))

    bltodo.normalize_backlog()

    normalized = todo_file.read_text(encoding="utf-8")
    assert normalized.count("id:") >= 2


def test_normalize_backlog_does_not_fabricate_an_explicit_do_status_marker(monkeypatch, tmp_path: Path):
    todo_file = tmp_path / "sample.md"
    todo_file.write_text(
        "## Story: Beta\n"
        "d - some task\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("BL_TODO_FILE", str(todo_file))

    bltodo.normalize_backlog()

    normalized = todo_file.read_text(encoding="utf-8")
    assert "d - Story: Beta" not in normalized
    assert "Story: Beta" in normalized


def test_normalize_backlog_drops_an_explicit_do_marker_since_it_is_the_default(monkeypatch, tmp_path: Path):
    todo_file = tmp_path / "sample.md"
    todo_file.write_text(
        "# d - Story: Alpha\n"
        "d - first task\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("BL_TODO_FILE", str(todo_file))

    bltodo.normalize_backlog()

    normalized = todo_file.read_text(encoding="utf-8")
    assert "d - Story: Alpha" not in normalized
    assert "# Story: Alpha" in normalized


def test_pop_story_saves_recovery_before_removal(monkeypatch, tmp_path: Path):
    todo_file = tmp_path / "sample.md"
    _write_todo(todo_file)
    monkeypatch.setenv("BL_TODO_FILE", str(todo_file))

    bltodo.pop_story()
    recovery_text = bltodo.show_recovery()

    assert "Recovery files:" in recovery_text
    assert ".md" in recovery_text


def test_main_prints_todo_path_and_mdgbdf(monkeypatch, tmp_path: Path, capsys):
    todo_file = tmp_path / "sample.md"
    _write_todo(todo_file)
    monkeypatch.setenv("BL_TODO_FILE", str(todo_file))

    exit_code = bltodo.main([])
    out = capsys.readouterr().out

    assert exit_code == 0
    assert f"TODO file: {todo_file.resolve()}" in out
    assert "# d - Story: Alpha" in out


def test_save_recovery_creates_copy_and_prunes(monkeypatch, tmp_path: Path):
    todo_file = tmp_path / "sample.md"
    _write_todo(todo_file)
    monkeypatch.setenv("BL_TODO_FILE", str(todo_file))

    saved_paths = [bltodo.save_recovery(keep=2) for _ in range(3)]
    recovery_dir = saved_paths[-1].parent
    files = sorted(path for path in recovery_dir.iterdir() if path.is_file())

    assert len(files) == 2
    assert saved_paths[-1].name in {path.name for path in files}
    assert all(path.read_text(encoding="utf-8") == todo_file.read_text(encoding="utf-8") for path in files)


def test_show_recovery_lists_paths_and_files(monkeypatch, tmp_path: Path):
    todo_file = tmp_path / "sample.md"
    _write_todo(todo_file)
    monkeypatch.setenv("BL_TODO_FILE", str(todo_file))

    bltodo.save_recovery(keep=4)
    text = bltodo.show_recovery()

    assert f"TODO file: {todo_file.resolve()}" in text
    assert "Recovery dir:" in text


def test_archive_completed_stories_no_tasks_moves_story_to_done_file(monkeypatch, tmp_path: Path):
    todo_file = tmp_path / "sample.md"
    _write_todo(todo_file)
    monkeypatch.setenv("BL_TODO_FILE", str(todo_file))
    done_file = tmp_path / "done.md"
    monkeypatch.setattr(bltodo, "resolve_done_file_path", lambda: done_file)

    todo_file.write_text(
        todo_file.read_text(encoding="utf-8") + "# x - Story: Gamma\n---\nid: story-c\n---\n",
        encoding="utf-8",
    )

    archived = bltodo.archive_completed_stories()

    assert [s.id for s in archived] == ["story-c"]
    remaining = bltodo.load_todo_stories()
    assert "story-c" not in {s.id for s in remaining}
    done_stories = bltodo.load_done_stories(done_file)
    assert [s.id for s in done_stories] == ["story-c"]


def test_archive_completed_stories_all_tasks_completed_moves_whole_story(monkeypatch, tmp_path: Path):
    todo_file = tmp_path / "sample.md"
    monkeypatch.setenv("BL_TODO_FILE", str(todo_file))
    done_file = tmp_path / "done.md"
    monkeypatch.setattr(bltodo, "resolve_done_file_path", lambda: done_file)
    todo_file.write_text(
        "# d - Story: Alpha\n---\nid: story-a\n---\nd - first task\n---\nid: task-1\n---\n"
        "# d - Story: Beta\n---\nid: story-b\n---\nx - only task\n---\nid: task-2\n---\n",
        encoding="utf-8",
    )

    archived = bltodo.archive_completed_stories()

    assert [s.id for s in archived] == ["story-b"]
    remaining = bltodo.load_todo_stories()
    assert [s.id for s in remaining] == ["story-a"]
    done_stories = bltodo.load_done_stories(done_file)
    assert done_stories[0].tasks[0].name == "only task"


def test_archive_completed_stories_is_a_noop_when_nothing_is_completed(monkeypatch, tmp_path: Path):
    todo_file = tmp_path / "sample.md"
    _write_todo(todo_file)
    monkeypatch.setenv("BL_TODO_FILE", str(todo_file))

    def fail_if_called():
        raise AssertionError("resolve_done_file_path should not be called when nothing is completed")

    monkeypatch.setattr(bltodo, "resolve_done_file_path", fail_if_called)

    archived = bltodo.archive_completed_stories()

    assert archived == []


def test_archive_completed_stories_raises_on_flagged_story_with_incomplete_task(monkeypatch, tmp_path: Path):
    todo_file = tmp_path / "sample.md"
    monkeypatch.setenv("BL_TODO_FILE", str(todo_file))
    todo_file.write_text(
        "# x - Story: Gamma\n---\nid: story-c\n---\nd - unfinished analysis\n---\nid: task-1\n---\n",
        encoding="utf-8",
    )

    with pytest.raises(gbops.StoryStatusConflictError):
        bltodo.archive_completed_stories()


def test_push_story_archives_pushed_story_when_it_resolves_completed(monkeypatch, tmp_path: Path):
    todo_file = tmp_path / "sample.md"
    _write_todo(todo_file)
    monkeypatch.setenv("BL_TODO_FILE", str(todo_file))
    done_file = tmp_path / "done.md"
    monkeypatch.setattr(bltodo, "resolve_done_file_path", lambda: done_file)

    pushed = gbdata.Story(id="story-z", name="Zed", status=gbdata.StoryStatus.COMPLETED, tasks=[])

    result = bltodo.push_story(pushed)

    assert result.id == "story-z"
    remaining = bltodo.load_todo_stories()
    assert "story-z" not in {s.id for s in remaining}
    done_stories = bltodo.load_done_stories(done_file)
    assert [s.id for s in done_stories] == ["story-z"]


def test_showdone_prints_done_path_and_archived_stories(monkeypatch, tmp_path: Path, capsys):
    todo_file = tmp_path / "sample.md"
    monkeypatch.setenv("BL_TODO_FILE", str(todo_file))
    done_file = tmp_path / "done.md"
    monkeypatch.setattr(bltodo, "resolve_done_file_path", lambda: done_file)
    done_file.write_text(
        "# Completed Stories\n\n## x - Story: Archived One\n---\nid: story-done\n---\n",
        encoding="utf-8",
    )

    exit_code = bltodo.main(["showdone"])
    out = capsys.readouterr().out

    assert exit_code == 0
    assert f"Done file: {done_file}" in out
    assert "Archived One" in out


def test_showdone_limits_to_top_n(monkeypatch, tmp_path: Path, capsys):
    todo_file = tmp_path / "sample.md"
    monkeypatch.setenv("BL_TODO_FILE", str(todo_file))
    done_file = tmp_path / "done.md"
    monkeypatch.setattr(bltodo, "resolve_done_file_path", lambda: done_file)
    done_file.write_text(
        "# Completed Stories\n\n"
        "## x - Story: Newest\n---\nid: story-2\n---\n\n"
        "## x - Story: Oldest\n---\nid: story-1\n---\n",
        encoding="utf-8",
    )

    exit_code = bltodo.main(["showdone", "1"])
    out = capsys.readouterr().out

    assert exit_code == 0
    assert "Newest" in out
    assert "Oldest" not in out


def test_main_showrecovery_command(monkeypatch, tmp_path: Path, capsys):
    todo_file = tmp_path / "sample.md"
    _write_todo(todo_file)
    monkeypatch.setenv("BL_TODO_FILE", str(todo_file))

    bltodo.save_recovery()
    exit_code = bltodo.main(["showrecovery"])
    out = capsys.readouterr().out

    assert exit_code == 0
    assert "TODO file:" in out
    assert "Recovery dir:" in out
    assert "Recovery files:" in out


def test_main_recovery_command_accepts_keep_argument(monkeypatch, tmp_path: Path, capsys):
    todo_file = tmp_path / "sample.md"
    _write_todo(todo_file)
    monkeypatch.setenv("BL_TODO_FILE", str(todo_file))

    exit_code = bltodo.main(["recovery", "2"])
    out = capsys.readouterr().out

    assert exit_code == 0
    assert "Saved recovery:" in out
