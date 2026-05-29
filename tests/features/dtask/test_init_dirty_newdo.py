"""Pytest-BDD scenario tests for dtask init --dirty and --newdo

Each function maps one Gherkin scenario to a test via the @scenario decorator.
Step definitions are loaded from tests.steps.test_dtask_init_dirty_newdo,
registered as a pytest plugin in tests/conftest.py.
"""

from pytest_bdd import scenario


@scenario(
    "dtask/init_dirty_newdo.feature",
    "newdo commits a dirty do.md before replacing it",
)
def test_newdo_commits_dirty_do_md(git_repo):
    pass


@scenario(
    "dtask/init_dirty_newdo.feature",
    "newdo has no effect when do.md is already committed",
)
def test_newdo_no_effect_when_committed(git_repo):
    pass


@scenario(
    "dtask/init_dirty_newdo.feature",
    "dirty without newdo exits with error when do.md is dirty",
)
def test_dirty_without_newdo_errors(git_repo):
    pass


@scenario(
    "dtask/init_dirty_newdo.feature",
    "dirty allows init when only non-do.md files are dirty",
)
def test_dirty_non_do_md_files(git_repo):
    pass
