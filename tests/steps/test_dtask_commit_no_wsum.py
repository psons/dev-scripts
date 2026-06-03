"""
Pytest-BDD step definitions for dtask commit scenarios without --wsum.

This module covers:
- default commit behavior using workHeadline from do.md
- --actual with explicit values or copied from intendedCommitMessage
- --update staging tracked changes only
- --final commit and removal flow
- --all/--update mutual exclusion
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import frontmatter
from pytest_bdd import given, when, then, parsers

DO_MD_RELATIVE = "docs/dev/work/do.md"
DO_MD_DESCRIPTION = (
    "A list of small, focused tasks guiding the current commit with detailed "
    "microsected activities."
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


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


def _render_do_md(metadata: dict, body: str = "Task notes.\n") -> str:
    post = frontmatter.Post(body.rstrip() + "\n", **metadata)
    return frontmatter.dumps(post)


def _read_frontmatter(git_repo) -> dict:
    content = _do_md_path(git_repo).read_text()
    return frontmatter.loads(content).metadata


def _write_committed_do_md(git_repo, metadata: dict, body: str = "Task notes.\n"):
    do_md = _do_md_path(git_repo)
    do_md.parent.mkdir(parents=True, exist_ok=True)
    do_md.write_text(_render_do_md(metadata, body))
    git_repo.run_git_command(["add", DO_MD_RELATIVE])
    git_repo.run_git_command(["commit", "-m", "Add committed do.md"])


def _run_commit_command(git_repo, args: list[str]):
    git_repo.last_command_result = git_repo.run_dtask_command(["commit", *args])
    return git_repo.last_command_result


def _commit_message_at_ref(git_repo, ref: str) -> str:
    result = subprocess.run(
        ["git", "log", "-1", "--format=%s", ref],
        cwd=git_repo.repo_dir,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def _show_name_status(git_repo, ref: str) -> str:
    result = subprocess.run(
        ["git", "show", "--format=", "--name-status", ref],
        cwd=git_repo.repo_dir,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


def _status_for_path(git_repo, path: str) -> str:
    result = subprocess.run(
        ["git", "status", "--porcelain", "--", path],
        cwd=git_repo.repo_dir,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


# ---------------------------------------------------------------------------
# Background step
# ---------------------------------------------------------------------------


@given("a git repository with initial commit and tracked files")
def given_repo_with_tracked_files(git_repo):
    for fname in ["file-one.txt", "file-two.txt"]:
        (git_repo.repo_dir / fname).write_text(f"# {fname}\n")
    git_repo.run_git_command(["add", "file-one.txt", "file-two.txt"])
    git_repo.run_git_command(["commit", "-m", "Add tracked test files"])


@given("a committed do.md file for the current branch with frontmatter:")
def given_committed_do_md(git_repo, datatable):
    frontmatter = {
        "title": "do.md",
        "description": DO_MD_DESCRIPTION,
        "workBranch": git_repo.get_current_branch(),
        "priorCommit": _current_head(git_repo),
    }
    for row in datatable[1:]:
        key = row[0]
        value = row[1]
        if value == "current branch":
            value = git_repo.get_current_branch()
        elif value == "current HEAD":
            value = _current_head(git_repo)
        frontmatter[key] = value

    _write_committed_do_md(git_repo, frontmatter)


# ---------------------------------------------------------------------------
# Given steps
# ---------------------------------------------------------------------------


@given("the committed do.md file has frontmatter:")
def given_committed_do_md_frontmatter(git_repo, datatable):
    frontmatter = _read_frontmatter(git_repo)
    for row in datatable[1:]:
        key = row[0]
        value = row[1]
        frontmatter[key] = value
    do_md = _do_md_path(git_repo)
    do_md.write_text(_render_do_md(frontmatter))
    git_repo.run_git_command(["add", DO_MD_RELATIVE])
    git_repo.run_git_command(["commit", "-m", "Update do.md frontmatter for commit scenario"])


@given(parsers.parse('the tracked file "{filename}" has staged changes with content "{content}"'))
def given_staged_tracked_file(git_repo, filename, content):
    file_path = git_repo.repo_dir / filename
    file_path.write_text(f"{content}\n")
    git_repo.run_git_command(["add", filename])


@given(parsers.parse('the tracked file "{filename}" has unstaged changes with content "{content}"'))
def given_unstaged_tracked_file(git_repo, filename, content):
    file_path = git_repo.repo_dir / filename
    file_path.write_text(f"{content}\n")


@given(parsers.parse('the untracked file "{filename}" exists with content "{content}"'))
def given_untracked_file(git_repo, filename, content):
    file_path = git_repo.repo_dir / filename
    file_path.write_text(f"{content}\n")


@given(parsers.parse('the do.md file has dirty text "{content}"'))
def given_dirty_do_md(git_repo, content):
    do_md = _do_md_path(git_repo)
    do_md.write_text(do_md.read_text().rstrip() + f"\n\n{content}\n")


# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------


@when('I run "dtask commit"')
def when_run_dtask_commit(git_repo):
    _run_commit_command(git_repo, [])


@when(parsers.parse('I run "dtask commit --actual {actual_message}"'))
def when_run_dtask_commit_actual_with_message(git_repo, actual_message):
    _run_commit_command(git_repo, ["--actual", actual_message])


@when('I run "dtask commit --actual"')
def when_run_dtask_commit_actual_copy_intended(git_repo):
    _run_commit_command(git_repo, ["--actual"])


@when('I run "dtask commit --update"')
def when_run_dtask_commit_update(git_repo):
    _run_commit_command(git_repo, ["--update"])


@when('I run "dtask commit --final"')
def when_run_dtask_commit_final(git_repo):
    git_repo.head_before_dtask = _current_head(git_repo)
    _run_commit_command(git_repo, ["--final"])


@when('I run "dtask commit --all --update"')
def when_run_dtask_commit_all_and_update(git_repo):
    _run_commit_command(git_repo, ["--all", "--update"])


# ---------------------------------------------------------------------------
# Then steps
# ---------------------------------------------------------------------------


@then("the command succeeds")
def then_command_succeeds(git_repo):
    result = git_repo.last_command_result
    assert result.returncode == 0, (
        f"Expected exit code 0, got {result.returncode}\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )


@then("the command fails with a non-zero exit code")
def then_command_fails(git_repo):
    result = git_repo.last_command_result
    assert result.returncode != 0, (
        f"Expected non-zero exit code, got {result.returncode}\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )


@then(parsers.parse('the error output mentions "{text}"'))
def then_error_mentions(git_repo, text):
    result = git_repo.last_command_result
    combined = f"{result.stdout}\n{result.stderr}"
    assert text in combined, (
        f"Expected '{text}' in command output.\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )


@then(parsers.parse('the latest commit message is "{message}"'))
def then_latest_commit_message(git_repo, message):
    assert _commit_message_at_ref(git_repo, "HEAD") == message


@then(parsers.parse('do.md frontmatter value "{key}" is "{value}"'))
def then_do_md_frontmatter_value(git_repo, key, value):
    frontmatter = _read_frontmatter(git_repo)
    assert str(frontmatter.get(key, "")) == value, (
        f"Expected do.md frontmatter '{key}' to be '{value}', got '{frontmatter.get(key, '')}'."
    )


@then(parsers.parse('the commit includes "{path}"'))
def then_latest_commit_includes_path(git_repo, path):
    output = _show_name_status(git_repo, "HEAD")
    assert path in output, (
        f"Expected latest commit to include '{path}'.\n"
        f"Commit output:\n{output}"
    )


@then(parsers.parse('the commit does not include "{path}"'))
def then_latest_commit_does_not_include_path(git_repo, path):
    output = _show_name_status(git_repo, "HEAD")
    assert path not in output, (
        f"Did not expect latest commit to include '{path}'.\n"
        f"Commit output:\n{output}"
    )


@then("the do.md file no longer exists")
def then_do_md_removed(git_repo):
    assert not _do_md_path(git_repo).exists(), "Expected do.md to be removed"


@then("the last 2 commit messages are:")
def then_last_two_commit_messages(git_repo, datatable):
    expected = [row[0] for row in datatable[1:]]
    result = subprocess.run(
        ["git", "log", "--format=%s", "-n", str(len(expected))],
        cwd=git_repo.repo_dir,
        capture_output=True,
        text=True,
        check=True,
    )
    messages = result.stdout.splitlines()
    assert messages == expected, (
        f"Expected last commit messages {expected}, got {messages}.\n"
        f"git log output:\n{result.stdout}"
    )


@then(parsers.parse('the previous commit includes "{path}"'))
def then_previous_commit_includes_path(git_repo, path):
    output = _show_name_status(git_repo, "HEAD~1")
    assert path in output, (
        f"Expected previous commit to include '{path}'.\n"
        f"Commit output:\n{output}"
    )


@then(parsers.parse('the file "{filename}" is still untracked'))
def then_file_is_still_untracked(git_repo, filename):
    status = _status_for_path(git_repo, filename)
    assert status.startswith("??"), (
        f"Expected '{filename}' to remain untracked, got status '{status}'."
    )
