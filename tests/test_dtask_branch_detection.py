"""Regression tests for dtask branch detection in commit mode."""

from __future__ import annotations

import subprocess
from pathlib import Path


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


def _write_do_md(repo_dir: Path, work_branch: str):
    do_md = repo_dir / "docs" / "dev" / "work" / "do.md"
    do_md.parent.mkdir(parents=True, exist_ok=True)
    do_md.write_text(
        """---
title: do.md
description: test
workBranch: """ + work_branch + """
priorCommit: ""
intendedCommitMessage: ""
actualCommitMessage: ""
---
Task notes.
"""
    )


def test_commit_works_on_unborn_branch_with_symbolic_ref(tmp_path: Path):
    """dtask commit should resolve branch name even before first commit exists."""
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()

    _run_git(repo_dir, ["init"])
    _run_git(repo_dir, ["config", "user.email", "test@example.com"])
    _run_git(repo_dir, ["config", "user.name", "Test User"])

    branch = _run_git(repo_dir, ["symbolic-ref", "--short", "HEAD"]).stdout.strip()
    _write_do_md(repo_dir, branch)

    (repo_dir / "file-one.txt").write_text("first commit content\n")

    result = subprocess.run(
        ["dtask", "commit", "--all", "--actual", "first commit message"],
        cwd=repo_dir,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, (
        f"Expected dtask commit to succeed on unborn branch.\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )

    message = _run_git(repo_dir, ["log", "-1", "--format=%s"]).stdout.strip()
    assert message == "first commit message"


def test_commit_reports_symbolic_ref_error_when_head_is_detached(tmp_path: Path):
    """dtask commit should surface git's symbolic-ref failure in detached HEAD state."""
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()

    _run_git(repo_dir, ["init"])
    _run_git(repo_dir, ["config", "user.email", "test@example.com"])
    _run_git(repo_dir, ["config", "user.name", "Test User"])

    (repo_dir / "README.md").write_text("seed\n")
    _run_git(repo_dir, ["add", "README.md"])
    _run_git(repo_dir, ["commit", "-m", "seed commit"])

    branch = _run_git(repo_dir, ["symbolic-ref", "--short", "HEAD"]).stdout.strip()
    _write_do_md(repo_dir, branch)

    _run_git(repo_dir, ["checkout", "--detach", "HEAD"])
    (repo_dir / "file-two.txt").write_text("detached update\n")

    result = subprocess.run(
        ["dtask", "commit", "--all", "--actual", "detached message"],
        cwd=repo_dir,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "fatal: ref HEAD is not a symbolic ref" in result.stderr
