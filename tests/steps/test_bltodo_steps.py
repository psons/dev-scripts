"""Pytest-BDD step definitions for bltodo CLI behavior."""

from __future__ import annotations

from dataclasses import dataclass
import os
import shlex
import subprocess
import sys
from pathlib import Path

import pytest
from pytest_bdd import given, parsers, then, when


BLTODO_SCRIPT = Path(__file__).resolve().parents[2] / "bin" / "bltodo.py"


@dataclass
class BltodoCliState:
    repo_root: Path
    tmp_path: Path
    env: dict[str, str]
    result: subprocess.CompletedProcess[str] | None = None
    todo_path: Path | None = None


@pytest.fixture
def bltodo_cli(tmp_path: Path) -> BltodoCliState:
    return BltodoCliState(
        repo_root=Path(__file__).resolve().parents[2],
        tmp_path=tmp_path,
        env=os.environ.copy(),
    )


def _run_bltodo(state: BltodoCliState, command: str) -> None:
    args = shlex.split(command)
    if not args:
        raise AssertionError("Expected a non-empty bltodo command string")
    if args[0] != "bltodo":
        args = ["bltodo", *args]

    state.result = subprocess.run(
        [sys.executable, str(BLTODO_SCRIPT), *args[1:]],
        cwd=state.repo_root,
        capture_output=True,
        text=True,
        env=state.env,
    )


@given(parsers.parse('a bltodo TODO file named "{filename}" with content:'), target_fixture="bltodo_cli")
def given_bltodo_todo_file(bltodo_cli: BltodoCliState, filename: str, docstring: str) -> BltodoCliState:
    path = bltodo_cli.tmp_path / filename
    path.write_text(docstring.lstrip("\n"), encoding="utf-8")
    bltodo_cli.todo_path = path
    return bltodo_cli


@given("BL_TODO_FILE points to that bltodo TODO file", target_fixture="bltodo_cli")
def given_bltodo_file_env(bltodo_cli: BltodoCliState) -> BltodoCliState:
    assert bltodo_cli.todo_path is not None
    bltodo_cli.env["BL_TODO_FILE"] = str(bltodo_cli.todo_path)
    return bltodo_cli


@given("BL_TODO_FILE points to a missing bltodo file", target_fixture="bltodo_cli")
def given_missing_bltodo_file_env(bltodo_cli: BltodoCliState) -> BltodoCliState:
    bltodo_cli.env["BL_TODO_FILE"] = str(bltodo_cli.tmp_path / "does-not-exist.md")
    return bltodo_cli


@when(parsers.parse('I run bltodo command "{command}"'))
def when_run_bltodo(bltodo_cli: BltodoCliState, command: str) -> None:
    _run_bltodo(bltodo_cli, command)


@then("the bltodo command succeeds")
def then_bltodo_command_succeeds(bltodo_cli: BltodoCliState) -> None:
    result = bltodo_cli.result
    assert result is not None
    assert result.returncode == 0, (
        f"Expected success, got exit code {result.returncode}\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )


@then("the bltodo command fails with a non-zero exit code")
def then_bltodo_command_fails(bltodo_cli: BltodoCliState) -> None:
    result = bltodo_cli.result
    assert result is not None
    assert result.returncode != 0, (
        f"Expected failure, got exit code {result.returncode}\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )


@then(parsers.parse('the bltodo stdout contains "{text}"'))
def then_bltodo_stdout_contains(bltodo_cli: BltodoCliState, text: str) -> None:
    result = bltodo_cli.result
    assert result is not None
    assert text in result.stdout, f"Expected '{text}' in stdout:\n{result.stdout}"
