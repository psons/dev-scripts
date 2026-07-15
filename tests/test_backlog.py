"""Unit tests for backlog command module behavior."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
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


_load_module("gbdata", _bin_dir / "gbdata.py")
_load_module("mdgbdata", _bin_dir / "mdgbdata.py")
_load_module("bltodo", _bin_dir / "bltodo.py")
backlog = _load_module("backlog", _bin_dir / "backlog.py")


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
        "# d - Story: Beta\n"
        "---\n"
        "id: story-b\n"
        "---\n"
        "d - second task\n"
        "---\n"
        "id: task-2\n"
        "---\n",
        encoding="utf-8",
    )


def test_resolve_provider_name_precedence(monkeypatch):
    monkeypatch.setenv("BACKLOG_PROVIDER", "bltodo")

    assert backlog.resolve_provider_name("custom") == "custom"
    assert backlog.resolve_provider_name() == "bltodo"


def test_run_backlog_prioritized_json(monkeypatch, tmp_path: Path):
    todo_file = tmp_path / "todo.md"
    _write_todo(todo_file)
    monkeypatch.setenv("BL_TODO_FILE", str(todo_file))
    monkeypatch.delenv("BACKLOG_PROVIDER", raising=False)

    result = backlog.run_backlog_command(command="prioritized", output_format="json")
    payload = json.loads(result.output_text)

    assert result.provider == "bltodo"
    assert payload[0]["tasks"][0]["id"] == "task-1"


def test_run_backlog_poptask_mdgbdf(monkeypatch, tmp_path: Path):
    todo_file = tmp_path / "todo.md"
    _write_todo(todo_file)
    monkeypatch.setenv("BL_TODO_FILE", str(todo_file))

    result = backlog.run_backlog_command(command="poptask", output_format="mdgbdf")

    assert "# Story: Top Task" in result.output_text
    assert "d - first task" in result.output_text


def test_main_help_returns_zero(capsys):
    exit_code = backlog.main(["help"])
    out = capsys.readouterr().out

    assert exit_code == 0
    assert "usage:" in out


def test_unknown_provider_raises_value_error():
    with pytest.raises(ValueError, match="Unknown backlog provider"):
        backlog.load_provider_module("does_not_exist_provider")
