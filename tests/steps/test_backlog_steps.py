"""Pytest-BDD step definitions for backlog CLI behavior."""

from __future__ import annotations

import json
from dataclasses import dataclass
import os
import shlex
import subprocess
import sys
from pathlib import Path

import pytest
from pytest_bdd import given, parsers, then, when


BACKLOG_SCRIPT = Path(__file__).resolve().parents[2] / "bin" / "backlog.py"


@dataclass
class BacklogCliState:
    repo_root: Path
    tmp_path: Path
    env: dict[str, str]
    result: subprocess.CompletedProcess[str] | None = None
    todo_path: Path | None = None


@pytest.fixture
def backlog_cli(tmp_path: Path) -> BacklogCliState:
    return BacklogCliState(
        repo_root=Path(__file__).resolve().parents[2],
        tmp_path=tmp_path,
        env=os.environ.copy(),
    )


def _run_backlog(state: BacklogCliState, command: str) -> None:
    args = shlex.split(command)
    if not args:
        raise AssertionError("Expected a non-empty backlog command string")
    if args[0] != "backlog":
        args = ["backlog", *args]

    state.result = subprocess.run(
        [sys.executable, str(BACKLOG_SCRIPT), *args[1:]],
        cwd=state.repo_root,
        capture_output=True,
        text=True,
        env=state.env,
    )


@given(parsers.parse('a backlog TODO file named "{filename}" with content:'), target_fixture="backlog_cli")
def given_backlog_todo_file(backlog_cli: BacklogCliState, filename: str, docstring: str) -> BacklogCliState:
    path = backlog_cli.tmp_path / filename
    path.write_text(docstring.lstrip("\n"), encoding="utf-8")
    backlog_cli.todo_path = path
    return backlog_cli


@given("BL_TODO_FILE points to that backlog TODO file", target_fixture="backlog_cli")
def given_bltodo_file_env(backlog_cli: BacklogCliState) -> BacklogCliState:
    assert backlog_cli.todo_path is not None
    backlog_cli.env["BL_TODO_FILE"] = str(backlog_cli.todo_path)
    backlog_cli.env.pop("BACKLOG_PROVIDER", None)
    return backlog_cli


@when(parsers.parse('I run backlog command "{command}"'))
def when_run_backlog(backlog_cli: BacklogCliState, command: str) -> None:
    _run_backlog(backlog_cli, command)


@then("the backlog command succeeds")
def then_backlog_command_succeeds(backlog_cli: BacklogCliState) -> None:
    result = backlog_cli.result
    assert result is not None
    assert result.returncode == 0, (
        f"Expected success, got exit code {result.returncode}\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )


@then(parsers.parse('the backlog stdout contains "{text}"'))
def then_backlog_stdout_contains(backlog_cli: BacklogCliState, text: str) -> None:
    result = backlog_cli.result
    assert result is not None
    assert text in result.stdout, f"Expected '{text}' in stdout:\n{result.stdout}"


@then(parsers.parse('the backlog stdout JSON contains a task id "{task_id}"'))
def then_backlog_json_contains_task_id(backlog_cli: BacklogCliState, task_id: str) -> None:
    result = backlog_cli.result
    assert result is not None
    payload = json.loads(result.stdout)
    assert isinstance(payload, list)
    assert payload, "Expected at least one story in JSON output"
    tasks = payload[0].get("tasks") or []
    assert tasks, "Expected at least one task in JSON output"
    assert tasks[0].get("id") == task_id
