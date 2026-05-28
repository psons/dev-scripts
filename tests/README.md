# dtask Test Suite

## Overview

This directory contains the test suite for the `dtask` CLI utility. Tests follow Behavior-Driven Development (BDD) principles using Gherkin feature files and pytest-bdd.

## Structure

```
tests/
├── conftest.py              # Pytest configuration and fixtures
├── features/                # Gherkin feature files (.feature)
│   └── dtask/
│       └── init_workbranch.feature
├── steps/                   # Step definition implementations
│   ├── __init__.py
│   └── test_dtask_init_workbranch.py
└── README.md               # This file
```

## Running Tests

### Prerequisites

Install test dependencies:
```bash
pip install pytest pytest-bdd
```

### Run All Tests

```bash
pytest
```

### Run Only BDD Tests

```bash
pytest -m bdd
```

### Run Specific Feature

```bash
pytest tests/features/dtask/test_init_workbranch.py
```

### Run with Verbose Output

```bash
pytest -v --tb=short
```

### Run with Gherkin Terminal Reporter

```bash
pytest -v --gherkin-terminal-reporter
```

## Test Design Principles

1. **Sandboxed Environments**: All tests run in isolated temporary directories to prevent side effects on the actual repository

2. **Zero Global State**: Tests use pytest fixtures to manage state, with no shared state between test runs

3. **Realistic Git Operations**: Tests use real Git commands to verify authentic behavior

4. **Clean Repositories**: Each test starts with a minimal test repository containing:
   - Initial commit with README.md
   - Standard test files (file-one.txt, file-two.txt)
   - docs/dev/work/do.md for tracking task state

## Feature Files

### init_workbranch.feature

Tests the `dtask init --workbranch` command:

- **Scenario 1**: Initialize feature branch with workbranch flag
  - Verifies branch creation and checkout
  - Verifies do.md creation with proper frontmatter
  - Verifies do.md is not staged

- **Scenario 2**: Workbranch frontmatter is properly set
  - Verifies all expected frontmatter fields

- **Scenario 3**: Workbranch creates branch from current HEAD
  - Verifies branch points to correct commit
  - Verifies working tree remains clean

## Step Definitions

Step definitions are implemented in `steps/test_dtask_init_workbranch.py` and include:

- **Given**: Repository initialization and state setup
- **When**: dtask command execution
- **Then**: Assertions on repository state, file content, and git status

## Extending Tests

To add new test scenarios:

1. Add feature definitions to `.feature` files
2. Implement corresponding step definitions in `steps/test_*.py`
3. Use the `GitRepoTestFixture` class to manage sandboxed repositories
4. Run tests to verify: `pytest`

## Common Issues

### pytest-bdd not found

Install with: `pip install pytest-bdd`

### Tests fail with "dtask not found"

Ensure dtask is installed or available in PATH:
```bash
pip install -e .  # Install current package in development mode
```

### Permission errors on temporary directories

Tests create temporary directories in the system temp folder. Ensure write permissions:
```bash
ls -la /tmp  # Verify permissions
```
