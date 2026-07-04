"""Pytest-BDD step definitions for mdgbdata CLI behavior."""

from __future__ import annotations

import json
from dataclasses import dataclass
import shlex
import subprocess
import sys
from pathlib import Path

import pytest
from pytest_bdd import given, parsers, then, when


MDGBDATA_SCRIPT = Path(__file__).resolve().parents[2] / "bin" / "mdgbdata.py"


@dataclass
class MdgbdataCliState:
    repo_root: Path
    tmp_path: Path
    result: subprocess.CompletedProcess[str] | None = None
    input_path: Path | None = None


@pytest.fixture
def mdgbdata_cli(tmp_path: Path) -> MdgbdataCliState:
    return MdgbdataCliState(
        repo_root=Path(__file__).resolve().parents[2],
        tmp_path=tmp_path,
    )


def _run_mdgbdata(state: MdgbdataCliState, command: str) -> None:
    args = shlex.split(command)
    if not args:
        raise AssertionError("Expected a non-empty mdgbdata command string")
    if args[0] != "mdgbdata":
        args = ["mdgbdata", *args]
    resolved_args = [args[0], args[1]]
    for arg in args[2:]:
        resolved_args.append(str(Path(arg) if Path(arg).is_absolute() else state.tmp_path / arg))
    state.result = subprocess.run(
        [sys.executable, str(MDGBDATA_SCRIPT), *resolved_args[1:]],
        cwd=state.repo_root,
        capture_output=True,
        text=True,
    )


@given(parsers.parse('a markdown file named "{filename}" with content:'), target_fixture="mdgbdata_cli")
def given_markdown_file(mdgbdata_cli: MdgbdataCliState, filename: str, docstring: str) -> MdgbdataCliState:
    path = mdgbdata_cli.tmp_path / filename
    path.write_text(docstring.lstrip("\n"), encoding="utf-8")
    mdgbdata_cli.input_path = path
    return mdgbdata_cli


@given(parsers.parse('a JSON file named "{filename}" with content:'), target_fixture="mdgbdata_cli")
def given_json_file(mdgbdata_cli: MdgbdataCliState, filename: str, docstring: str) -> MdgbdataCliState:
    path = mdgbdata_cli.tmp_path / filename
    path.write_text(docstring.lstrip("\n"), encoding="utf-8")
    mdgbdata_cli.input_path = path
    return mdgbdata_cli


@when(parsers.parse('I run mdgbdata command "{command}"'))
def when_run_mdgbdata(mdgbdata_cli: MdgbdataCliState, command: str) -> None:
    _run_mdgbdata(mdgbdata_cli, command)


@then("the mdgbdata command succeeds")
def then_mdgbdata_command_succeeds(mdgbdata_cli: MdgbdataCliState) -> None:
    result = mdgbdata_cli.result
    assert result is not None
    assert result.returncode == 0, (
        f"Expected success, got exit code {result.returncode}\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )


@then("the mdgbdata command fails with a non-zero exit code")
def then_mdgbdata_command_fails(mdgbdata_cli: MdgbdataCliState) -> None:
    result = mdgbdata_cli.result
    assert result is not None
    assert result.returncode != 0, (
        f"Expected failure, got exit code {result.returncode}\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )


@then(parsers.parse('the mdgbdata stderr contains "{text}"'))
def then_mdgbdata_stderr_contains(mdgbdata_cli: MdgbdataCliState, text: str) -> None:
    result = mdgbdata_cli.result
    assert result is not None
    assert text in result.stderr, f"Expected '{text}' in stderr:\n{result.stderr}"


@then(parsers.parse('the mdgbdata stdout contains "{text}"'))
def then_mdgbdata_stdout_contains(mdgbdata_cli: MdgbdataCliState, text: str) -> None:
    result = mdgbdata_cli.result
    assert result is not None
    assert text in result.stdout, f"Expected '{text}' in stdout:\n{result.stdout}"


@then(
    parsers.parse(
        'the mdgbdata stdout JSON contains a story named "{story_name}" with status "{story_status}" '
        'and a task named "{task_name}" with status "{task_status}"'
    )
)
def then_mdgbdata_stdout_json_contains_story_and_task(
    mdgbdata_cli: MdgbdataCliState,
    story_name: str,
    story_status: str,
    task_name: str,
    task_status: str,
) -> None:
    result = mdgbdata_cli.result
    assert result is not None
    data = json.loads(result.stdout)
    assert isinstance(data, list)
    assert data, "Expected at least one story in JSON output"
    story = data[0]
    assert story["name"] == story_name
    assert story["status"] == story_status
    assert story.get("tasks"), "Expected at least one task in story output"
    task = story["tasks"][0]
    assert task["name"] == task_name
    assert task["status"] == task_status


@then(parsers.parse('the mdgbdata stdout JSON story description is "{description}"'))
def then_mdgbdata_stdout_json_story_description(mdgbdata_cli: MdgbdataCliState, description: str) -> None:
    result = mdgbdata_cli.result
    assert result is not None
    data = json.loads(result.stdout)
    assert isinstance(data, list)
    assert data, "Expected at least one story in JSON output"
    assert data[0].get("description") == description