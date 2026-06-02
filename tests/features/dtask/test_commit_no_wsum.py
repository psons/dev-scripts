"""Pytest-BDD scenario tests for dtask commit without --wsum.

Each function maps one Gherkin scenario to a test via the @scenario decorator.
Step definitions are loaded from tests.steps.test_dtask_commit_no_wsum,
registered as a pytest plugin in tests/conftest.py.
"""

from pytest_bdd import scenario


@scenario(
    "dtask/commit_no_wsum.feature",
    "default commit uses workHeadline and keeps untracked files out of scope",
)
def test_default_commit_uses_workheadline(git_repo):
    pass


@scenario(
    "dtask/commit_no_wsum.feature",
    "--actual with an explicit message updates do.md before committing",
)
def test_commit_actual_explicit_message(git_repo):
    pass


@scenario(
    "dtask/commit_no_wsum.feature",
    "--actual without an argument copies intendedCommitMessage",
)
def test_commit_actual_copies_intended(git_repo):
    pass


@scenario(
    "dtask/commit_no_wsum.feature",
    "--update includes tracked unstaged changes but excludes untracked files",
)
def test_commit_update_includes_tracked_only(git_repo):
    pass


@scenario(
    "dtask/commit_no_wsum.feature",
    "--final removes do.md after committing dirty task changes",
)
def test_commit_final_dirty_do_md(git_repo):
    pass


@scenario(
    "dtask/commit_no_wsum.feature",
    "--final removes do.md even when the working tree is clean",
)
def test_commit_final_clean_tree(git_repo):
    pass


@scenario(
    "dtask/commit_no_wsum.feature",
    "--all and --update cannot be combined",
)
def test_commit_all_and_update_are_mutually_exclusive(git_repo):
    pass
