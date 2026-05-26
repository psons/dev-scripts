# Test Tools Specification: Behavior-Driven Development Framework

## 1. Objective & Scope
This specification defines the testing framework, test directory layout, and architectural boundaries for the Python-based CLI utilities located in `./bin`. 

The primary focus is testing `dtask`, a utility that orchestrates localized file operations (managing `docs/dev/work/do.md`) and side-effect-heavy Git operations (branching, checking out, and multi-stage commits).

---

## 2. Testing Framework Architecture
To ensure test speed, complete environmental isolation, and robust verification of real Git behavior, the project utilizes **Pytest** paired with **Pytest-BDD**.

### Key Rules
* **No `src/` Directory Structure:** Tests run directly against executable scripts in `./bin`.
* **Zero Global State / No State Leakage:** Tests must use standard Pytest fixtures and Pytest-BDD `target_fixture` mappings to pass data down the Given-When-Then pipeline.
* **Strict Sandboxing:** No test execution may alter the repository hosting this project. Every test interaction with a Git repository or local markdown file must happen inside a sandboxed ecosystem.

---

## 3. Directory Layout Integration
Test locations mirror the specification structure. The project layout is organized as follows:

```text
.
├── bin/                          # Executable production Python scripts (e.g., dtask)
├── docs/
│   ├── user/
│   └── dev/
│       ├── work/                 # Target execution directory for dtask (contains do.md)
│       └── spec/
│           ├── usecases/         # Input requirements used to build feature files
│           └── testing-tools/    # This specification (test-tools-spec.md)
└── tests/                        # Dedicated root for testing execution
    ├── features/                 # Human-readable Gherkin .feature specifications
    │   └── dtask/                # Feature groups separated by subcommand boundaries
    └── steps/                    # Executable step definitions bound to the features
        └── test_dtask.py         # Main step definition mapping