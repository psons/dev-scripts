"""Pytest-BDD scenario tests for dtask init --workbranch

This file explicitly defines BDD scenarios using the @scenario decorator.
Each scenario maps to a Gherkin scenario in the .feature file.

IMPORTANT: For pytest-bdd to find step definitions, they must be registered in a module
that pytest imports before matching steps to scenarios. This is done by:
1. Importing the step module (which runs the @given/@when/@then decorators)
2. Making the step functions available in this module's namespace

The step functions are named with the step text as their docstrings, so pytest-bdd
can match them to the Gherkin steps in the .feature file.
"""

import pytest
from pytest_bdd import scenario

# CRITICAL: Import step module to register steps with pytest-bdd
# This MUST be done before @scenario decorators are evaluated
from tests.steps.test_dtask_init_workbranch import (  # noqa: F401
    # Fixture
    git_repo,
    # Given steps
    given_clean_git_repo,
    given_clean_working_tree,
    given_multiple_commits,
    # When steps
    when_run_dtask_init_workbranch,
    # Then steps
    then_branch_created,
    then_branch_checked_out,
    then_do_file_created,
    then_do_file_contains_frontmatter,
    then_do_file_not_staged,
    then_do_file_contains_table,
    then_branch_at_same_commit,
    then_working_tree_clean,
)


@scenario(
    "dtask/init_workbranch.feature",
    "Initialize feature branch with workbranch flag"
)
def test_init_workbranch_scenario(git_repo):
    """Test scenario: Initialize feature branch with workbranch flag"""
    pass


@scenario(
    "dtask/init_workbranch.feature",
    "Workbranch frontmatter is properly set"
)
def test_workbranch_frontmatter_scenario(git_repo):
    """Test scenario: Workbranch frontmatter is properly set"""
    pass


@scenario(
    "dtask/init_workbranch.feature",
    "Workbranch creates branch from current HEAD"
)
def test_workbranch_from_head_scenario(git_repo):
    """Test scenario: Workbranch creates branch from current HEAD"""
    pass
