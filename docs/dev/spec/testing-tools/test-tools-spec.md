# Test Tools Specification: Behavior-Driven Development Framework

## 1. Objective & Scope
This specification defines the testing framework, test directory layout, and architectural boundaries for the Python-based CLI utilities located in `./bin`. 

The primary focus is testing `dtask`, a utility that orchestrates localized file operations (managing `docs/dev/work/do.md`) and side-effect-heavy Git operations (branching, checking out, and multi-stage commits).

---

## 2. Testing Framework Architecture
To ensure test speed, complete environmental isolation, and robust verification of real Git behavior, the project utilizes **Pytest** paired with **Pytest-BDD**.

### Key Rules
* **Zero Global State / No State Leakage:** Tests must use standard Pytest fixtures and Pytest-BDD `target_fixture` mappings to pass data down the Given-When-Then pipeline.
* **Strict Sandboxing:** No test execution may alter the repository hosting this project. Every test interaction with a Git repository or local markdown file must happen inside a sandboxed ecosystem.
* **Step Phrase Isolation Across Commands:** When multiple command families are tested in the same repository (for example `dtask` and `wsum`), step phrases must be command-scoped to avoid cross-feature step resolution collisions.
  - Prefer command-specific phrases such as `I run wsum command "..."`, `the wsum command succeeds`, and `the wsum error output mentions "..."`.
  - Avoid generic shared phrases like `I run "..."`, `the command succeeds`, and `the error output mentions "..."` across unrelated command families.
* **Correct YAML parsing** A YAML parser should be used for reading and writing YAML with correct adherence to quoting and escaping rules.

---

## 3. Test Repositories
Repositories to test Git should be simple and minimal with just a few files 
 - To track the the state of 
    - docs/dev/work/do.md
  - To represent tracked clean files, tracked dirty files, and untracked files. 
 - file-one.txt
 - file-two.txt
 - file-tree.txt


## 4. Directory Layout Integration
The project layout is organized as follows:

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

---

## 5. Documentation Maintenance Requirements

### Tests README Must Be Current
The file `tests/README.md` is a required part of the test system contract and must be kept up to date whenever test behavior, file layout, naming conventions, or workflow guidance changes.

At minimum, updates to tests/features, tests/steps, fixture strategy, or test-generation workflows must be reflected in `tests/README.md` in the same change set.

### Skill Compliance With This Specification
Any project skill that generates or modifies pytest-bdd artifacts (including `pytest-bdd-from-command`) must explicitly consult this specification file `docs/dev/spec/testing-tools/test-tools-spec.md` before producing outputs.

If a skill definition does not already include that requirement, it must be updated to include it.

Skills must also enforce command-scoped step phrasing to prevent step-definition conflicts between different command families.