---
"actualCommitMessage": "feat: Add pytest-bdd scenarios for `dtask init` dirty working tree, validating `--dirty` and `--newdo` with `do.md` files"
"description": "A list of small, focused tasks guiding the current commit with detailed\
  \ microsected activities."
"intendedCommitMessage": "python BDD scenarios for - dtask init with --dirty and --newdo"
"priorCommit": "0aaa26eac974263929d80288610a0a7c7ee890aa"
"title": "do.md"
"workBranch": "bdd-dtask-init-dirty"
"workHeadline": "feat: Add pytest-bdd scenarios for `dtask init` dirty working tree, validating `--dirty` and `--newdo` with `do.md` files"
---


## story: python BDD - dtask init with --dirty and --newdo
x - do a one time run through AI created "next BDD Feature" for dtask, using this feature: 
    - Prompt: 
        generate BDD feature and step files from the '#usage situation': '## dtask init with --dirty and --newdo ' in docs/dev/spec/usecases/dtask-and-do-file-tasks.md
        - using the file layout and other instructions for a generalized version of docs/dev/spec/testing-tools/test-tools-spec.md
        - for further detail on dtask init features and scenarios, read the spec for the app: docs/dev/spec/dtask-spec.md


# Work Summary

## 2026-05-29 13:59

---
"workHeadline": "feat: Add pytest-bdd scenarios for `dtask init` dirty working tree, validating `--dirty` and `--newdo` with `do.md` files"
---

This change introduces new `pytest-bdd` scenarios and associated step definitions to validate the `dtask init` command's behavior when the git working tree is dirty. Specifically, it adds tests for how the `--dirty` and `--newdo` flags handle uncommitted `do.md` files, ensuring that an existing dirty `do.md` is correctly committed before a new one is created, or that an error is raised if `--newdo` is not specified when `do.md` is dirty. The update also confirms that `dtask init --dirty` can proceed when only non-`do.md` files are modified, and correctly asserts the `priorCommit` metadata in the newly generated `do.md` file based on the git history.

## 2026-05-29 12:59

---
workHeadline: Docs: Clarify dtask init behavior, define section frontmatter, and note sandboxed test environment.
---

This update clarifies documentation and sets the stage for new development. The `dtask-spec.md` file now more precisely defines "section frontmatter," while `dtask-and-do-file-tasks.md` was enhanced with detailed behavior for `dtask init` when using `--dirty` and `--newdo` flags, including a new scenario for handling a dirty `do.md` without the `--newdo` flag. A task related to generating BDD features for these `dtask init` scenarios was removed from `TODO.md` and subsequently initiated in a new `do.md` file. Additionally, the `tests/README.md` now explicitly notes the sandboxed environment where tests execute.
