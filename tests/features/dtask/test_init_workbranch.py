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
