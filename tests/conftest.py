"""
Pytest configuration and hooks for dtask testing.

OVERVIEW
--------
This module configures pytest and pytest-bdd for the dtask test suite. It uses pytest
"hooks" - special functions that pytest recognizes and calls at specific points during
test discovery and execution. This is the central place where pytest test behavior is
configured.

PYTEST LIFECYCLE & WHERE THIS FILE FITS
---------------------------------------
When you run `pytest`, the following happens:

1. pytest starts and looks for conftest.py in the test directory
2. pytest imports and executes conftest.py to register hooks
3. pytest discovers test files and features matching patterns (*.py, *.feature)
4. pytest_configure hook runs (our function)
5. pytest discovers test items (individual test functions and BDD scenarios)
6. pytest_collection_modifyitems hook runs (our function)
7. Tests are collected and reported
8. Tests are executed

THIS FILE'S ROLE
---------------
conftest.py is pytest's configuration file. It:
- Registers custom pytest "hooks" that pytest calls at specific times
- Defines shared fixtures that multiple test files can use
- Applies custom logic to all tests in the directory and subdirectories
- Defines custom markers (tags) for filtering tests

For pytest-bdd specifically, this file ensures that:
- BDD scenarios from .feature files are recognized as tests
- Custom markers are registered so you can filter tests

PYTEST HOOKS EXPLAINED
---------------------
Hooks are special functions with reserved names that pytest recognizes. Pytest calls
these functions at specific points in its lifecycle. The naming convention is
"pytest_<event>". Some key hooks:

- pytest_configure: Called after command line options are parsed, before collection
- pytest_collection_modifyitems: Called after test items are collected, before execution
- pytest_runtest_setup: Called before each test runs
- pytest_runtest_teardown: Called after each test runs

See: https://docs.pytest.org/en/stable/reference.html#hooks

IMPORTS & MODULES
----------------
- pytest: Core pytest framework
- pytest_bdd: Extension that adds BDD (Gherkin) support to pytest
  - given, when, then: Decorators for step definitions (from steps/*.py)
- pytest_plugins: Special list that tells pytest which modules to import

STEP DEFINITION DISCOVERY
-------------------------
For pytest-bdd to work, step definitions (Python functions decorated with @given, @when, @then)
must be imported BEFORE feature files are parsed. This module uses pytest_plugins to ensure
that happens. See the pytest_plugins line below.

When pytest discovers steps/test_dtask_init_workbranch.py, it will:
1. Import the module
2. Execute the @given, @when, @then decorators
3. Register those functions as step implementations
4. Then when .feature files are parsed, the steps are available
"""

import pytest
from pytest_bdd import given, when, then

# Import step definitions early to ensure they're registered before feature discovery
from tests.steps import test_dtask_init_workbranch  # noqa: F401


def pytest_configure(config):
    """
    HOOK: Called by pytest after command-line options are parsed.
    
    PURPOSE
    -------
    This hook registers custom pytest markers that can be used to tag and filter tests.
    
    CALLED BY
    ---------
    pytest (core framework) - automatically called during pytest startup before test collection
    
    EXECUTION TIMING
    ----------------
    This runs once per pytest session, before any test files are discovered.
    Runs before: pytest_collection_modifyitems, before any tests are collected
    
    PARAMETERS
    ----------
    config : pytest.Config
        The pytest configuration object that controls how pytest behaves.
        It has methods like addinivalue_line() to register markers.
    
    WHAT IT DOES
    -----------
    Registers the "bdd" marker so you can later use it to tag and filter tests:
    
    @pytest.mark.bdd          # Tag a test with this marker
    def test_something():
        pass
    
    Then run: pytest -m bdd   # Run only tests marked with @pytest.mark.bdd
    
    HOW MARKERS WORK
    ----------------
    Markers are essentially tags for tests. They allow you to:
    - Filter test runs: pytest -m bdd, pytest -m "not bdd"
    - Group related tests together
    - Apply custom behavior to specific test categories
    
    In our case, we use "bdd" to mark all BDD scenario tests (from .feature files)
    so they can be run separately from pure unit tests if needed.
    
    PYTEST-BDD CONNECTION
    --------------------
    When pytest-bdd discovers BDD scenarios (from .feature files), those scenarios
    become pytest test items. In the next hook (pytest_collection_modifyitems), we
    detect these BDD scenarios and apply the "bdd" marker to them automatically.
    """
    config.addinivalue_line(
        "markers",
        "bdd: mark test as a BDD scenario (deselect with '-m \"not bdd\"')"
    )


def pytest_collection_modifyitems(config, items):
    """
    HOOK: Called by pytest after test items are collected but before execution.
    
    PURPOSE
    -------
    This hook processes all discovered test items and applies custom markers to BDD
    scenarios. It allows us to dynamically tag BDD tests so they can be filtered.
    
    CALLED BY
    ---------
    pytest (core framework) - automatically called after test collection, before execution
    
    EXECUTION TIMING
    ----------------
    This runs after:
      - pytest_configure (markers are registered)
      - Test discovery (pytest found all test files and .feature files)
    Before:
      - Any tests actually execute
    
    PARAMETERS
    ----------
    config : pytest.Config
        The pytest configuration object (same as in pytest_configure)
    
    items : list of pytest.Item
        All discovered test items (test functions, BDD scenarios, etc.)
        Each item represents one executable test that pytest will run.
    
    WHAT IT DOES
    -----------
    Iterates through all test items and:
    1. Checks if the item is a BDD scenario (by checking for "scenario" in keywords)
    2. If it is a scenario, applies the "bdd" marker to it
    
    This means all tests generated from .feature files automatically get tagged
    with @pytest.mark.bdd without requiring manual annotation.
    
    HOW TO USE THIS LATER
    --------------------
    After this runs, you can filter tests:
    
    Run ONLY BDD tests:
      pytest -m bdd
    
    Run ONLY non-BDD tests:
      pytest -m "not bdd"
    
    Run ONLY BDD scenarios from a specific file:
      pytest tests/features/dtask/init_workbranch.feature -m bdd
    
    PYTEST-BDD CONNECTION
    --------------------
    When pytest-bdd processes .feature files, it converts each Scenario into a pytest
    test item with "scenario" in its keywords. This function detects those BDD-generated
    items and tags them so they can be managed separately from traditional pytest tests.
    
    EXAMPLE FLOW
    -----------
    1. pytest_configure runs → "bdd" marker is registered
    2. pytest discovers tests:
       - Finds test_dtask_init_workbranch.py with test functions
       - Finds init_workbranch.feature with BDD scenarios
       - pytest-bdd converts scenarios to test items
    3. pytest_collection_modifyitems runs:
       - Iterates through all items
       - Finds scenario items (from .feature files)
       - Applies @pytest.mark.bdd to them
    4. Tests can now be filtered and run
    """
    for item in items:
        if "scenario" in item.keywords:
            item.add_marker(pytest.mark.bdd)
