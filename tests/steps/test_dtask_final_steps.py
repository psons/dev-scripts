"""Step definitions for dtask finalization BDD scenarios."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess

import frontmatter
from pytest_bdd import given, then, when, parsers

DO_MD_RELATIVE = "docs/dev/work/do.md"


def _do_md_path(git_repo) -> Path:
    return git_repo.repo_dir / DO_MD_RELATIVE


def _current_head(git_repo) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=git_repo.repo_dir,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def _write_committed_file(git_repo, relative_path: str, content: str, message: str) -> None:
    path = git_repo.repo_dir / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    git_repo.run_git_command(["add", relative_path])
    git_repo.run_git_command(["commit", "-m", message])


def _run_finalization(git_repo, args: list[str]) -> None:
    git_repo.head_before_dtask = _current_head(git_repo)
    git_repo.finalization_do_md_before = _do_md_path(git_repo).read_text(encoding="utf-8")
    git_repo.last_finalization_result = git_repo.run_dtask_command(args)


@given("do.md contains current work with active and completed tasks")
def given_do_md_contains_finalization_work(git_repo, monkeypatch):
    do_md = _do_md_path(git_repo)
    do_md.parent.mkdir(parents=True, exist_ok=True)
    metadata = {
        "title": "do.md",
        "description": "Finalization test work.",
        "workBranch": git_repo.get_current_branch(),
        "priorCommit": _current_head(git_repo),
        "actualCommitMessage": "finalize current work",
        "intendedCommitMessage": "finalize current work",
    }
    body = (
        "# Current work\n\n"
        "## d - Story: Active Story\n"
        "---\n"
        "id: story-active\n"
        "---\n"
        "d - active task\n"
        "---\n"
        "id: task-active\n"
        "---\n"
        "x - completed task\n"
        "---\n"
        "id: task-completed\n"
        "---\n"
        "u - unfinished task\n"
        "---\n"
        "id: task-unfinished\n"
        "---\n\n"
        "# Completed work\n\n"
    )
    do_md.write_text(frontmatter.dumps(frontmatter.Post(body, **metadata)), encoding="utf-8")
    git_repo.run_git_command(["add", DO_MD_RELATIVE])
    git_repo.run_git_command(["commit", "-m", "Add finalization do.md"])

    todo_file = git_repo.repo_dir / "TODO.md"
    todo_file.write_text("", encoding="utf-8")
    monkeypatch.setenv("BL_TODO_FILE", str(todo_file))


@given("TODO.md contains an existing story for the current work")
def given_existing_backlog_story(git_repo):
    _write_committed_file(
        git_repo,
        "TODO.md",
        "# d - Story: Active Story\n"
        "---\n"
        "id: story-active\n"
        "---\n"
        "d - existing task\n"
        "---\n"
        "id: task-existing\n"
        "---\n",
        "Add existing backlog story",
    )


@given("a tracked work file has staged changes")
def given_staged_work_file(git_repo):
    path = git_repo.repo_dir / "work.txt"
    path.write_text("work requiring finalization\n", encoding="utf-8")
    git_repo.run_git_command(["add", "work.txt"])


@given("the backlog provider is unavailable")
def given_unavailable_backlog_provider(monkeypatch):
    monkeypatch.setenv("BACKLOG_PROVIDER", "provider_that_does_not_exist")


@when('I run "dtask commit --final --all" for finalization')
def when_run_finalization_all(git_repo):
    _run_finalization(git_repo, ["commit", "--final", "--all"])


@when('I run "dtask commit --final" for finalization')
def when_run_finalization(git_repo):
    _run_finalization(git_repo, ["commit", "--final"])


@then("the finalization command succeeds")
def then_finalization_succeeds(git_repo):
    result = git_repo.last_finalization_result
    assert result.returncode == 0, f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"


@then("the finalization command fails")
def then_finalization_fails(git_repo):
    result = git_repo.last_finalization_result
    assert result.returncode != 0, f"Expected failure, got stdout:\n{result.stdout}\nstderr:\n{result.stderr}"


def _backlog_stories(git_repo):
    import sys

    bin_dir = Path(__file__).resolve().parents[2] / "bin"
    if str(bin_dir) not in sys.path:
        sys.path.insert(0, str(bin_dir))
    import bltodo

    return bltodo.load_todo_stories(git_repo.repo_dir / "TODO.md")


@then("the backlog has the finalized story at the top")
def then_backlog_story_at_top(git_repo):
    stories = _backlog_stories(git_repo)
    assert stories, "Expected at least one story in TODO.md"
    assert stories[0].id == "story-active"
    assert stories[0].name == "Active Story"


@then("TODO.md contains the unfinished current-work story at the top")
def then_todo_contains_unfinished_story_at_top(git_repo):
    stories = _backlog_stories(git_repo)
    assert stories, "Expected TODO.md to contain the pushed story"
    assert stories[0].id == "story-active"
    assert stories[0].name == "Active Story"


@then(parsers.parse('TODO.md contains active task "{task_name}" in story "{story_name}"'))
def then_todo_contains_active_task(git_repo, task_name, story_name):
    stories = _backlog_stories(git_repo)
    story = next((story for story in stories if story.name == story_name), None)
    assert story is not None, f"Expected story {story_name!r} in TODO.md"
    assert task_name in [task.name for task in story.tasks or []]


@then("the backlog story contains the active task and its existing task")
def then_backlog_story_contains_tasks(git_repo):
    stories = _backlog_stories(git_repo)
    task_ids = [task.id for task in stories[0].tasks or []]
    assert task_ids == ["task-existing", "task-active"]


@then(parsers.parse('the first finalization commit contains completed task "{task_name}" with story ID "{story_id}" and story name "{story_name}"'))
def then_first_commit_contains_completed_task(git_repo, task_name, story_id, story_name):
    result = subprocess.run(
        ["git", "show", "HEAD~1:docs/dev/work/do.md"],
        cwd=git_repo.repo_dir,
        capture_output=True,
        text=True,
        check=True,
    )
    content = result.stdout
    assert "# Completed work" in content
    assert task_name in content
    assert f"storyID: {story_id}" in content
    assert f"storyName: {story_name}" in content


@then("the finalization do.md file no longer exists")
def then_do_md_no_longer_exists(git_repo):
    assert not _do_md_path(git_repo).exists()


@then("the do.md file remains unchanged")
def then_do_md_remains_unchanged(git_repo):
    assert _do_md_path(git_repo).exists()
    assert _do_md_path(git_repo).read_text(encoding="utf-8") == git_repo.finalization_do_md_before


@then("no final removal commit was created")
def then_no_final_removal_commit(git_repo):
    result = subprocess.run(
        ["git", "log", "--format=%s", "-n", "1"],
        cwd=git_repo.repo_dir,
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.strip() != "removed do.md for finalized tasks"
