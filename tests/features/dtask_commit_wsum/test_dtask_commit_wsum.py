"""
Pytest-BDD test scenario mapping for dtask commit --wsum feature

This module registers the BDD scenarios from dtask_commit_wsum.feature
and maps them to the step definitions in test_dtask_commit_wsum_steps.py.

The pytest-bdd framework automatically discovers and executes these scenarios
when pytest runs this module.
"""

from pathlib import Path
from pytest_bdd import scenarios

# Load all scenarios from the feature file
feature_file = Path(__file__).parent / "dtask_commit_wsum.feature"
scenarios(str(feature_file))
