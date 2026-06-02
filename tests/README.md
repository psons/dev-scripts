# dtask Test Suite

## Overview

This directory contains the test suite for the `dtask` CLI utility. Tests follow Behavior-Driven Development (BDD) principles using Gherkin feature files and pytest-bdd.

## Structure

```
tests/
├── conftest.py              # Pytest configuration and fixtures
├── features/                # Gherkin feature files (.feature)
│   └── dtask/
│       ├── init_workbranch.feature
│       ├── init_dirty_newdo.feature
│       └── commit_no_wsum.feature
├── features/
│   └── wsum/
│       └── wsum.feature
├── steps/                   # Step definition implementations
│   ├── __init__.py
│   ├── test_dtask_init_workbranch.py
│   ├── test_dtask_init_dirty_newdo.py
│   └── test_dtask_commit_no_wsum.py
│   └── test_wsum_steps.py
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

Other feature modules:

```bash
pytest tests/features/dtask/test_init_dirty_newdo.py
pytest tests/features/dtask/test_commit_no_wsum.py
pytest tests/features/wsum/test_wsum.py
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

1. **Sandboxed Environments**:  All tests run in isolated temporary directories to prevent side effects on the actual repository
                                The actual directory will be: ${TMPDIR}/pytest-of-${USER}

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

### init_dirty_newdo.feature

Tests `dtask init` behavior for dirty working trees and do.md replacement safeguards:

- **Scenario 1**: `--dirty --newdo` commits dirty do.md before replacing
  - Verifies an intermediate `do.md when ...` commit is made
  - Verifies new do.md `priorCommit` points to the save commit
- **Scenario 2**: `--dirty --newdo` when do.md is already committed
  - Verifies no extra save commit is made
  - Verifies new do.md `priorCommit` points to pre-command HEAD
- **Scenario 3**: `--dirty` without `--newdo` when do.md is dirty
  - Verifies non-zero exit and guidance mentioning `--newdo`
  - Verifies existing do.md content remains unchanged after failure
- **Scenario 4**: `--dirty` with only non-do.md dirty files
  - Verifies init succeeds and creates do.md
  - Verifies pre-existing non-do.md modifications remain present

### commit_no_wsum.feature

Tests `dtask commit` behavior without `--wsum` integration:

- **Scenario 1**: Default commit uses `workHeadline`
  - Verifies commit message comes from `workHeadline`
  - Verifies `actualCommitMessage` is updated to match
  - Verifies untracked files are excluded
- **Scenario 2**: `--actual <message>` uses explicit message
  - Verifies explicit message is written to do.md and used for commit
- **Scenario 3**: `--actual` without message copies `intendedCommitMessage`
  - Verifies copied value is committed and persisted to do.md
- **Scenario 4**: `--update` includes tracked unstaged changes only
  - Verifies tracked changes are included and untracked are excluded
- **Scenario 5**: `--final` with dirty do.md
  - Verifies first commit includes do.md changes and task files
  - Verifies second commit removes do.md with finalized removal message
- **Scenario 6**: `--final` with clean working tree
  - Verifies removal-only finalization commit still occurs
- **Scenario 7**: `--all` and `--update` are mutually exclusive
  - Verifies command fails with argparse conflict error

### wsum.feature

Tests `wsum.py` as a standalone CLI utility (explicitly excluding dtask integration):

- **Scenario 1**: default invocation is staged-only
  - Verifies staged changes are summarized
  - Verifies tracked unstaged and untracked files are excluded
- **Scenario 2**: `--all` includes staged, tracked unstaged, and untracked changes
  - Verifies inclusion scope matches all-change semantics
- **Scenario 3**: `--update` includes tracked unstaged but excludes untracked
  - Verifies update scope alignment with tracked-only semantics
- **Scenario 4**: `--base` compares against a non-default ref
  - Verifies base-ref override is applied
- **Scenario 5**: stdin diff input takes precedence
  - Verifies provided stdin diff is summarized instead of internal git diff
- **Scenario 6**: empty diff handling
  - Verifies command exits with error when there is nothing to summarize
- **Scenario 7**: extra diff arg validation
  - Verifies unsupported extra git diff args are rejected with an error
- **Scenario 8**: markdown formatting compatibility
  - Verifies timestamp heading and `workHeadline` frontmatter structure

## Step Definitions

Step definitions are implemented across:

- `steps/test_dtask_init_workbranch.py`
- `steps/test_dtask_init_dirty_newdo.py`
- `steps/test_dtask_commit_no_wsum.py`
- `steps/test_wsum_steps.py`

Together they include:

- **Given**: Repository initialization and state setup
- **When**: dtask command execution
- **Then**: Assertions on repository state, file content, and git status

## Extending Tests

To add new test scenarios:

1. Add feature definitions to `.feature` files
2. Implement corresponding step definitions in `steps/test_*.py`
3. Use the `GitRepoTestFixture` class to manage sandboxed repositories
4. Run tests to verify: `pytest`

## Explaining and Expanding the Suite with the New Skill

Use the `pytest-bdd-from-command` skill to generate and explain pytest-bdd coverage from a command reference plus an expected outcome.

What to provide to the skill:

1. Command usage details (syntax, flags, examples, expected errors)
2. A short description of desired behavior (success and failure expectations)
3. Any constraints (file naming, fixture reuse, target folders)

What the skill will produce in this repository:

1. Gherkin feature files in `tests/features/<command_slug>/<command_slug>.feature`
2. Step definition files in `tests/steps/test_<command_slug>_steps.py`
3. Runnable pytest commands and scenario coverage notes

Required compliance from `docs/dev/spec/testing-tools/test-tools-spec.md`:

1. Shared helper code is required for command execution logic
2. Runtime objects must remain isolated per scenario (no mutable object reuse across scenarios)
3. Scenario state must flow through fixtures and pytest-bdd `target_fixture` mappings
4. No global state leakage and no side effects outside test sandboxes

Suggested prompt pattern:

"Using the pytest-bdd-from-command skill, generate feature and step files for <command>, include success and failure scenarios, and keep runtime state isolated per scenario."

Leaner prompt pattern:

"Use pytest-bdd-from-command for <command> with this outcome: <expected outcome>."

The "<expected outcome>" should be a reference to a section in a file under docs/dev/spec/usecases such as the subsections under 
'# usage situations' in docs/dev/work/backlog-link/branch-strategy-story.md. 

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
