"""Unit tests for dtask pop subcommand behavior."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BIN_DIR = REPO_ROOT / "bin"
DTASK_SCRIPT = BIN_DIR / "dtask"


def _run_git(repo_dir: Path, args: list[str], check: bool = True) -> subprocess.CompletedProcess:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_dir,
        capture_output=True,
        text=True,
    )
    if check and result.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} failed\nstdout: {result.stdout}\nstderr: {result.stderr}"
        )
    return result


def _write_do_md(repo_dir: Path, body: str) -> Path:
    do_md = repo_dir / "docs" / "dev" / "work" / "do.md"
    do_md.parent.mkdir(parents=True, exist_ok=True)
    do_md.write_text(
        """---
title: do.md
description: test
workBranch: test-branch
priorCommit: ""
intendedCommitMessage: ""
actualCommitMessage: ""
---
"""
        + body,
        encoding="utf-8",
    )
    return do_md


def _write_todo_md(repo_dir: Path, text: str) -> Path:
    todo_md = repo_dir / "docs" / "dev" / "work" / "TODO.md"
    todo_md.parent.mkdir(parents=True, exist_ok=True)
    todo_md.write_text(text, encoding="utf-8")
    return todo_md


def _run_dtask_pop(repo_dir: Path, todo_path: Path) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["BL_TODO_FILE"] = str(todo_path)
    env["BACKLOG_PROVIDER"] = "bltodo"
    env["PYTHONPATH"] = str(BIN_DIR) + os.pathsep + env.get("PYTHONPATH", "")
    return subprocess.run(
        [str(DTASK_SCRIPT), "pop"],
        cwd=repo_dir,
        env=env,
        capture_output=True,
        text=True,
    )


def test_pop_inserts_story_at_top_of_current_work(tmp_path: Path):
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()

    _run_git(repo_dir, ["init"])

    do_md = _write_do_md(
        repo_dir,
        "# Current work\n\nExisting line\n",
    )
    todo_md = _write_todo_md(
        repo_dir,
        "# d - Story: Alpha\n"
        "d - first task\n",
    )

    result = _run_dtask_pop(repo_dir, todo_md)

    assert result.returncode == 0, f"stdout: {result.stdout}\nstderr: {result.stderr}"
    content = do_md.read_text(encoding="utf-8")
    assert "# Current work" in content
    assert "# d - Story: Alpha" in content
    assert "d - first task" in content
    assert content.index("# d - Story: Alpha") < content.index("Existing line")


def test_pop_creates_current_work_section_after_frontmatter(tmp_path: Path):
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()

    _run_git(repo_dir, ["init"])

    do_md = _write_do_md(
        repo_dir,
        "# Some other section\n\nBody\n",
    )
    todo_md = _write_todo_md(
        repo_dir,
        "# d - Story: Alpha\n"
        "d - first task\n",
    )

    result = _run_dtask_pop(repo_dir, todo_md)

    assert result.returncode == 0, f"stdout: {result.stdout}\nstderr: {result.stderr}"
    content = do_md.read_text(encoding="utf-8")

    frontmatter_end = content.index("---\n", 4) + 4
    current_work_pos = content.index("# Current work")
    assert current_work_pos >= frontmatter_end
    assert "# d - Story: Alpha" in content


def test_pop_fails_when_do_md_missing(tmp_path: Path):
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()

    _run_git(repo_dir, ["init"])

    todo_md = _write_todo_md(
        repo_dir,
        "# d - Story: Alpha\n"
        "d - first task\n",
    )

    result = _run_dtask_pop(repo_dir, todo_md)

    assert result.returncode != 0
    assert "Run 'dtask init' first" in result.stderr


def test_help_lists_pop_subcommand(tmp_path: Path):
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    _run_git(repo_dir, ["init"])

    result = subprocess.run(
        [str(DTASK_SCRIPT), "help"],
        cwd=repo_dir,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "pop" in result.stdout
