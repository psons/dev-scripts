"""pytest configuration for dtask feature tests

This conftest ensures step definitions are registered before scenarios are executed.
"""

# Import step definitions early to register them with pytest-bdd
# This MUST be done before feature scenarios are parsed
from tests.steps.test_dtask_init_workbranch import *  # noqa: F401, F403
