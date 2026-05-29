"""
Pytest-BDD step definitions for dtask init --dirty and --newdo scenarios

Tests the behavior of dtask init when the working tree is not clean, covering:
- --dirty --newdo with an uncommitted do.md: old do.md is committed then replaced
- --dirty --newdo with an already-committed do.md: no extra commit, just replaced
- --dirty without --newdo when do.md is dirty: exits with error requiring --newdo
- --dirty with only non-do.md dirty files and no do.md: init proceeds normally

The git_repo fixture is shared from tests.steps.test_dtask_init_workbranch and
registered globally via pytest_plugins in tests/conftest.py.
"""

import subprocess
from pathlib import Path

import pytest
import yaml
from pytest_bdd import given, when, then, parsers


# ---------------------------------------------------------------------------
# Background step
# ---------------------------------------------------------------------------

@given("a git repository with initial commit and tracked files")
def given_repo_with_tracked_files(git_repo):
    """Extend base repo fixture with canonical tracked test files.

    Per test-tools-spec, test repos include:
      - file-one.txt, file-two.txt, file-three.txt  (tracked clean files)
      - docs/dev/work/do.md                          (tracked via scenarios)
    """
    for fname in ["file-one.txt", "file-two.txt", "file-three.txt"]:
        (git_repo.repo_dir / fname).write_text(f"# {fname}\n")
    git_repo.run_git_command(["add", "file-one.txt", "file-two.txt", "file-three.txt"])
    git_repo.run_git_command(["commit", "-m", "Add tracked test files"])


# ---------------------------------------------------------------------------
# Given steps
# ---------------------------------------------------------------------------

@given("the working tree has an uncommitted do.md file")
def given_uncommitted_do_md(git_repo):
    """Create docs/dev/work/do.md but leave it untracked (never committed)."""
    do_md = git_repo.repo_dir / "docs" / "dev" / "work" / "do.md"
    do_md.parent.mkdir(parents=True, exist_ok=True)
    do_md.write_text(
        "---\ntitle: do.md\nworkBranch: old-feature\n---\nOld task notes.\n"
    )


@given("the working tree has a committed do.md file")
def given_committed_do_md(git_repo):
    """Create docs/dev/work/do.md, stage it, and commit it."""
    do_md = git_repo.repo_dir / "docs" / "dev" / "work" / "do.md"
    do_md.parent.mkdir(parents=True, exist_ok=True)
    do_md.write_text(
        "---\ntitle: do.md\nworkBranch: old-feature\n---\nOld task notes.\n"
    )
    git_repo.run_git_command(["add", "docs/dev/work/do.md"])
    git_repo.run_git_command(["commit", "-m", "Add committed do.md"])


@given("the working tree is clean")
def given_working_tree_is_clean(git_repo):
    """Assert the working tree has no uncommitted changes at all."""
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=git_repo.repo_dir,
        capture_output=True,
        text=True,
    )
    assert result.stdout.strip() == "", (
        f"Expected a clean working tree, got:\n{result.stdout}"
    )


@given(parsers.parse('the working tree has a modified tracked file "{filename}"'))
def given_modified_tracked_file(git_repo, filename):
    """Modify a committed tracked file so the working tree is dirty."""
    file_path = git_repo.repo_dir / filename
    assert file_path.exists(), (
        f"'{filename}' must already exist as a tracked file. "
        "Ensure the Background step created it."
    )
    file_path.write_text(f"# {filename} - modified\n")


@given("there is no existing do.md file")
def given_no_do_md(git_repo):
    """Assert that docs/dev/work/do.md does not exist."""
    assert not (git_repo.repo_dir / "docs" / "dev" / "work" / "do.md").exists(), (
        "do.md should not exist at the start of this scenario"
    )


# ---------------------------------------------------------------------------
# When steps
# ---------------------------------------------------------------------------

@when(parsers.parse('I run "dtask init --workbranch {branch_name} --dirty --newdo"'))
def when_run_dtask_init_dirty_newdo(git_repo, branch_name):
    """Run dtask init with both --dirty and --newdo flags.

    Stores HEAD hash before running so Then steps can compare commit state.
    """
    result_head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=git_repo.repo_dir,
        capture_output=True,
        text=True,
    )
    git_repo.head_before_dtask = result_head.stdout.strip()
    git_repo.last_command_result = git_repo.run_dtask_command(
        ["init", "--workbranch", branch_name, "--dirty", "--newdo"]
    )
    git_repo.test_branch_name = branch_name


@when(parsers.parse('I run "dtask init --workbranch {branch_name} --dirty"'))
def when_run_dtask_init_dirty(git_repo, branch_name):
    """Run dtask init with --dirty but without --newdo."""
    git_repo.last_command_result = git_repo.run_dtask_command(
        ["init", "--workbranch", branch_name, "--dirty"]
    )
    git_repo.test_branch_name = branch_name


# ---------------------------------------------------------------------------
# Then steps
# ---------------------------------------------------------------------------

@then("the command succeeds")
def then_command_succeeds(git_repo):
    """Assert that the last dtask command exited with code 0."""
    result = git_repo.last_command_result
    assert result.returncode == 0, (
        f"Expected exit code 0, got {result.returncode}\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )


@then("the command fails with a non-zero exit code")
def then_command_fails(git_repo):
    """Assert that the last dtask command exited with a non-zero code."""
    result = git_repo.last_command_result
    assert result.returncode != 0, (
        f"Expected non-zero exit code, got {result.returncode}\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )


@then(parsers.parse('the error output mentions "{text}"'))
def then_error_mentions(git_repo, text):
    """Assert that stderr (or stdout) contains the given text."""
    result = git_repo.last_command_result
    combined = result.stderr + result.stdout
    assert text in combined, (
        f"Expected '{text}' in command output.\n"
        f"stdout: {result.stdout}\nstderr: {result.stderr}"
    )


@then(parsers.parse('a commit exists with a message containing "{msg}"'))
def then_commit_exists_with_message(git_repo, msg):
    """Assert at least one commit in the log has a message containing msg."""
    result = subprocess.run(
        ["git", "log", "--format=%s", "--all"],
        cwd=git_repo.repo_dir,
        capture_output=True,
        text=True,
    )
    messages = result.stdout.splitlines()
    assert any(msg in line for line in messages), (
        f"No commit found with message containing '{msg}'.\n"
        f"Commit messages:\n{result.stdout}"
    )


@then(parsers.parse('no commit was made with a message containing "{msg}"'))
def then_no_commit_with_message(git_repo, msg):
    """Assert no commit in the log has a message containing msg."""
    result = subprocess.run(
        ["git", "log", "--format=%s", "--all"],
        cwd=git_repo.repo_dir,
        capture_output=True,
        text=True,
    )
    messages = result.stdout.splitlines()
    assert not any(msg in line for line in messages), (
        f"Found an unexpected commit with message containing '{msg}'.\n"
        f"Commit messages:\n{result.stdout}"
    )


@then('a new "docs/dev/work/do.md" file is created')
def then_new_do_md_created(git_repo):
    """Assert docs/dev/work/do.md exists after dtask ran."""
    assert (git_repo.repo_dir / "docs" / "dev" / "work" / "do.md").exists(), (
        "docs/dev/work/do.md was not created"
    )


@then("the new do.md priorCommit matches the commit that saved the old do.md")
def then_prior_commit_is_old_do_md_commit(git_repo):
    """Assert that priorCommit in the new do.md is the hash of the commit
    that dtask made to save the old do.md (the 'do.md when ...' commit)."""
    log = subprocess.run(
        ["git", "log", "--format=%H %s"],
        cwd=git_repo.repo_dir,
        capture_output=True,
        text=True,
    )
    save_commit = next(
        (line.split()[0] for line in log.stdout.splitlines() if "do.md when" in line),
        None,
    )
    assert save_commit is not None, (
        "Could not find a 'do.md when' commit in git log.\n"
        f"Log:\n{log.stdout}"
    )

    content = (git_repo.repo_dir / "docs" / "dev" / "work" / "do.md").read_text()
    fm = _parse_frontmatter(content)
    prior = fm.get("priorCommit", "")
    assert prior == save_commit, (
        f"priorCommit '{prior}' does not match 'do.md when' commit '{save_commit}'"
    )


@then("the new do.md priorCommit matches the commit before dtask ran")
def then_prior_commit_is_head_before_dtask(git_repo):
    """Assert that priorCommit in the new do.md equals the HEAD that existed
    before dtask init was run (i.e. no extra commit was inserted)."""
    content = (git_repo.repo_dir / "docs" / "dev" / "work" / "do.md").read_text()
    fm = _parse_frontmatter(content)
    prior = fm.get("priorCommit", "")
    assert prior == git_repo.head_before_dtask, (
        f"priorCommit '{prior}' does not match HEAD before dtask '{git_repo.head_before_dtask}'"
    )


@then("the do.md file is not staged")
def then_do_md_not_staged(git_repo):
    """Assert docs/dev/work/do.md is not in the git staging area."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        cwd=git_repo.repo_dir,
        capture_output=True,
        text=True,
    )
    assert "docs/dev/work/do.md" not in result.stdout, (
        "docs/dev/work/do.md should not be staged after dtask init"
    )


@then(parsers.parse('the file "{filename}" is still modified in the working tree'))
def then_file_still_modified(git_repo, filename):
    """Assert the file is listed as modified (M) in git status."""
    result = subprocess.run(
        ["git", "status", "--porcelain", filename],
        cwd=git_repo.repo_dir,
        capture_output=True,
        text=True,
    )
    assert result.stdout.strip() != "", (
        f"Expected '{filename}' to still be modified, but git status reports it clean."
    )


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _parse_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter from a file whose content starts with ---."""
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    return yaml.safe_load(parts[1]) or {}
