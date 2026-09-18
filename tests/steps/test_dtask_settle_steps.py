"""Step definitions for the dtask settle BDD scenarios."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
import shutil
import subprocess

import pytest
from pytest_bdd import given, then, when, parsers


REPO_ROOT = Path(__file__).resolve().parents[2]
USECASE_DIR = REPO_ROOT / "docs/dev/spec/usecases/docs/dev/spec/usecases/dtask"
DO_MD_RELATIVE = "docs/dev/work/do.md"


@dataclass
class SettleContext:
    repo_dir: Path
    before_do_md: str = ""
    before_commit_count: str = ""
    result: subprocess.CompletedProcess[str] | None = None


@pytest.fixture
def settle_repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Create a sandbox from the documented post-pop fixture states."""
    repo_dir = tmp_path / "settle-repo"
    repo_dir.mkdir()
    subprocess.run(["git", "init"], cwd=repo_dir, check=True, capture_output=True, text=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo_dir, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_dir, check=True)

    do_md = repo_dir / DO_MD_RELATIVE
    do_md.parent.mkdir(parents=True)
    shutil.copy2(USECASE_DIR / "basic-do-file-after-pop-with-progress.md", do_md)
    todo_file = repo_dir / "TODO.md"
    shutil.copy2(USECASE_DIR / "two-story-TODO-after-pop.md", todo_file)
    subprocess.run(["git", "add", "."], cwd=repo_dir, check=True)
    subprocess.run(["git", "commit", "-m", "Document post-pop task state"], cwd=repo_dir, check=True, capture_output=True, text=True)

    monkeypatch.setenv("PATH", f"{REPO_ROOT / 'bin'}{os.pathsep}{os.environ.get('PATH', '')}")
    monkeypatch.setenv("BL_TODO_FILE", str(todo_file))
    monkeypatch.delenv("BACKLOG_PROVIDER", raising=False)
    return SettleContext(repo_dir=repo_dir)


def _run_settle(repo_dir: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["dtask", "settle"],
        cwd=repo_dir,
        capture_output=True,
        text=True,
    )


def _do_md_path(repo_dir: Path) -> Path:
    return repo_dir / DO_MD_RELATIVE


@given("the documented dtask settle fixture state")
def given_documented_settle_fixture(settle_repo):
    return settle_repo


@given("the dtask settle backlog provider is unavailable")
def given_settle_provider_unavailable(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("BACKLOG_PROVIDER", "provider_that_does_not_exist")


@when("I run the dtask settle command")
def when_run_settle(settle_repo):
    settle_repo.before_do_md = _do_md_path(settle_repo.repo_dir).read_text(encoding="utf-8")
    settle_repo.before_commit_count = subprocess.run(
        ["git", "rev-list", "--count", "HEAD"],
        cwd=settle_repo.repo_dir,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    settle_repo.result = _run_settle(settle_repo.repo_dir)


@then("the dtask settle command succeeds")
def then_settle_succeeds(settle_repo):
    result = settle_repo.result
    assert result.returncode == 0, f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"


@then("the dtask settle command fails")
def then_settle_fails(settle_repo):
    assert settle_repo.result.returncode != 0


@then("the dtask settle do.md file remains")
def then_settle_do_md_remains(settle_repo):
    assert _do_md_path(settle_repo.repo_dir).exists()


@then(parsers.parse('the dtask settle do.md records completed task "{task_name}" with its story attribution'))
def then_settle_records_completed_task(settle_repo, task_name):
    content = _do_md_path(settle_repo.repo_dir).read_text(encoding="utf-8")
    completed_section = content.split("# Completed work", 1)[1]
    assert task_name in completed_section
    assert "storyID: " in completed_section
    assert "storyName: story 1" in completed_section
    assert task_name not in content.split("# Completed work", 1)[0]


@then(parsers.parse('the dtask settle backlog contains unfinished task "{task_name}" in story "{story_name}"'))
def then_settle_backlog_contains_task(settle_repo, task_name, story_name):
    bin_dir = str(REPO_ROOT / "bin")
    import sys
    if bin_dir not in sys.path:
        sys.path.insert(0, bin_dir)
    import bltodo

    stories = bltodo.load_todo_stories(settle_repo.repo_dir / "TODO.md")
    story = next(story for story in stories if story.name == story_name)
    assert task_name in [task.name for task in story.tasks or []]


@then("the dtask settle command creates no git commit")
def then_settle_no_commit(settle_repo):
    count = subprocess.run(
        ["git", "rev-list", "--count", "HEAD"],
        cwd=settle_repo.repo_dir,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    assert count == settle_repo.before_commit_count


@then("the dtask settle do.md is unchanged")
def then_settle_do_md_unchanged(settle_repo):
    assert _do_md_path(settle_repo.repo_dir).read_text(encoding="utf-8") == settle_repo.before_do_md