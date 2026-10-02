---
actualCommitMessage: Refactor dtask settle and story management in TODO.md/do.md;
  update .gitignore and add project terms to VS Code cSpell dictionary
description: A list of small, focused tasks guiding the current commit with detailed
  microsected activities.
intendedCommitMessage: Correct story moving behavior by dtask settle.
priorCommit: 0c768e9ec75a873f3d04e4bf33e4b36167cb7259
title: do.md
workBranch: settle-story-move-fixes
---

# Current work

# Completed work

---
id: file-input
---

x - finish drafting the plan in docs/dev/spec/usecases/dtask/dtask-and-do-file-tasks.md
---
id: 288f4b77-53c5-7f84-8287-e3876f677f53-81d7676c
storyID: 3eef52a5-c922-7b93-be8f-c651526c1495-968152ff
storyName: init a feature to correct story moving behavior by dtask settle.
---

x - clean stuff out of the planning draft to proper places
---
id: 6ec073d3-8f22-7b8a-9dc1-84ba76da98e9-7d63f005
storyID: 3eef52a5-c922-7b93-be8f-c651526c1495-968152ff
storyName: init a feature to correct story moving behavior by dtask settle.
---
Some content from docs/dev/spec/usecases/dtask/dtask-and-do-file-tasks.md
should move to use cases, ADRs.

x - implement the needed backlog PushStory protocol
---
id: 67dfbbff-68c9-7d92-bf0a-f76365d26252-900478d8
storyID: 3eef52a5-c922-7b93-be8f-c651526c1495-968152ff
storyName: init a feature to correct story moving behavior by dtask settle.
---
    / - update docs/dev/spec/backlog-spec.md
    ---
    prompt:
    update the docs/dev/spec/backlog-spec.md to include implementation of PushStory and a subcommand pushstory.  PushStory has the behaviors specified for dtask settle in dtask-and-do-file-tasks.md
    ---
    This task might be complete.

x - specify user override behavior for Story.status
---
id: bd88a0fc-1fdd-728f-89c6-b0f7ddf7e9b2-75b0d2cf
storyID: 3eef52a5-c922-7b93-be8f-c651526c1495-968152ff
storyName: init a feature to correct story moving behavior by dtask settle.
---
clarify in prompts and specs that it is the backlog that is a control interface for story status, and setting may be exposed to a caller (moved to use case doc).
    x - update do and TODO examples in docs/dev/spec/usecases/dtask so that they do not have the 'd' status on stories.  This will now be considered superfluous behavior.

x - Develop
---
id: c3ae1b23-eb0b-7f1f-925e-ff3cf176a495-9e4bd027
storyID: 3eef52a5-c922-7b93-be8f-c651526c1495-968152ff
storyName: init a feature to correct story moving behavior by dtask settle.
---
    update tests that have been based on files in docs/dev/spec/usecases/dtask so that they do not have status in the heading per the revised examples.

    x - have ai: create an example of a story in do.md that will error because it has incomplete tasks, but has been flagged as completed or abandoned.
     prompt: read docs/dev/spec/backlog-spec.md, and create a file docs/dev/spec/usecases/dtask/do-file-with-error-story-status.md as an example of do.md file content with a story that will cause an error in bltodo.py because it has incomplete tasks, but has been flagged as completed or abandoned. Add a link reference to the example file from backlog-spec.md

    x - have ai: create an example of a story with no tasks and flagged as 'completed' that will be treated by backlog.py as completed and moved into the done file per the implementation behavior of bltodo.py.
     prompt: read docs/dev/spec/backlog-spec.md, and create a file docs/dev/spec/usecases/dtask/do-file-with-completed-no-tasks-story-status.md as an example of do.md file content with a story with no tasks and flagged as 'completed' that will be treated by backlog.py as completed and moved into the done file per the implementation behavior of bltodo.py. Add a link reference to the example file from backlog-spec.md

     prompt: Also create a matching done file example.

    x - have ai: create an example of a story where all tasks are completed or abandoned that will be treated by backlog.py as completed and moved into the done file per the implementation behavior of bltodo.py.
    prompt:
    read docs/dev/spec/backlog-spec.md, and create a use case file  as an example of do.md file content with a story where all tasks are completed or abandoned that will be treated by backlog.py as completed and moved into the done file per the implementation behavior of bltodo.py.  Add a link reference to the example file from backlog-spec.md.  Also create the done file example.

x - Do the specified corrections to complete the story
---
id: 14df4224-cadb-7407-8498-b2957f062a85-65e18538
storyID: 3eef52a5-c922-7b93-be8f-c651526c1495-968152ff
storyName: init a feature to correct story moving behavior by dtask settle.
---
    Read:
        - Use case information in docs/dev/spec/usecases/dtask/dtask-and-do-file-tasks.md # usage situations.## dtask settle.### More needed corrections
        - Enhancements to the backlog PushStory implementation and behaviors of the bltodo.py plugin specified in docs/dev/spec/backlog-spec.md
        - and ADRs for dtask in docs/dev/spec/adr/dtask/dtask-issues.md
    Then Update the story moving behavior of dtask settle per updated specifications to correct the problem: dtask settle is ignoring stories that do not have tasks, which is not correct.

x - The mdgbdata behaviors should be documented to never explicitly write a status into a serialized story or set the property if it has not been found in content being parsed.
---
id: 4b4aa998-7af0-7925-8ad6-1bf0c2f281f8-d38bceaf
storyID: 3eef52a5-c922-7b93-be8f-c651526c1495-968152ff
storyName: init a feature to correct story moving behavior by dtask settle.
---


## d - Story: Delivery step
---
id: 4b1b4f62-1e7a-7827-8249-e20e592c6c53-c92cce46
---

a - update the dtask final spec from the dtask-and-do-file-tasks.md
---
id: 2dfdc26a-a412-7453-b3f3-5e4a7c559e2e-4e33ea5d
storyID: 3eef52a5-c922-7b93-be8f-c651526c1495-968152ff
storyName: init a feature to correct story moving behavior by dtask settle.
---
 - any other specs, plus:
    - # usage situations.## dtask settle.### Needed corrections
    - # usage situations.## dtask settle.### More needed corrections

# Work Summary


## 2026-10-07 10:06

---
workHeadline: 'refactor: Streamline `TODO.md`/`do.md` for `dtask settle` story management
  and clarify `--final` help message in `dtask`'
workChanges: The git diff refactors `TODO.md` and `do.md` to address `dtask settle`
  and story management, adding bug fixes and DDF compliance tasks to `TODO.md`, and
  formalizing `do.md`'s 'Completed work' with metadata and standardized references.
---

**Work Planning**: The git diff outlines a refactoring and bug-fixing initiative across `TODO.md` and `do.md`, primarily addressing `dtask settle` behaviors and story management. `TODO.md` gains new entries for bug fixes related to story ID handling and task upsertion in the 'Completed work' section, and an enhancement to normalize story heading levels. It also introduces tasks to evolve `TODO.md` into a DDF-compliant document. In `do.md`, a significant number of previously 'Current work' items have been moved into a formalized 'Completed work' section, now including explicit metadata such as `id` and `storyName`. Minor textual corrections were made, standardizing references to `bltodo.py` and updating YAML frontmatter for consistency.

**Implementation**: In `bin/dtask`, the help message for the `--final` flag was updated. Previously, it stated "Signal task complete," but has been revised to "Signal branch feature complete." This change clarifies that the `--final` flag is specifically used to mark a feature branch as complete, providing more precise guidance to users of the `dtask` command-line tool.

## 2026-10-02 14:00

---
workHeadline: Refactor dtask settle and story management in TODO.md/do.md; update
  .gitignore and add project terms to VS Code cSpell dictionary
workChanges: Refactoring across `TODO.md` and `do.md` addresses `dtask settle` and
  story management, introducing bug fixes and DDF evolution tasks in `TODO.md`, and
  formalizing 'Completed work' with metadata in `do.md` alongside minor textual corrections.
---

**Work Planning**: The git diff outlines a refactoring and bug-fixing initiative across `TODO.md` and `do.md`, primarily addressing `dtask settle` behaviors and story management. `TODO.md` gains new entries for bug fixes related to story ID handling and task upsertion in the 'Completed work' section, and an enhancement to normalize story heading levels. It also introduces tasks to evolve `TODO.md` into a DDF-compliant document. In `do.md`, a significant number of previously 'Current work' items have been moved into a formalized 'Completed work' section, now including explicit metadata such as `id` and `storyName`. Minor textual corrections were made, standardizing references to `bltodo.py` and updating YAML frontmatter for consistency.

**Implementation**: This commit updates the project's `.gitignore` file to exclude the `docs/dev/work/done` directory from version control, preventing temporary or generated "done" work files from being committed. Additionally, the `.vscode/settings.json` file was updated to include several new terms, such as "capsys," "psons," "showdone," and "upserting," in the cSpell dictionary. This enhancement improves the spell checker's accuracy within the VS Code environment for project-specific terminology.

## 2026-10-02 11:25

---
workHeadline: 'feat: Revamp story lifecycle with done.md archiving, standardize "d
  -" prefix removal, and formalize do.md ''Completed work'''
workChanges: The update standardizes story titles by removing "d -" prefixes in `TODO.md`
  and `do.md`, removes an obsolete `dtask unpop` story from `TODO.md`, and formalizes
  completed work in `do.md` with `id`, `storyID`, and `storyName` metadata.
---

**Work Planning**: The update standardizes story titles by removing "d -" prefixes across both `TODO.md` and `do.md`, enhancing clarity and consistency in the project backlog. In `TODO.md`, an obsolete story regarding a `dtask unpop` subcommand was entirely removed, streamlining future development plans. For `do.md`, the changes introduce a new "Completed work" section, where finished tasks from the "Current work" section are moved, now formalized with explicit metadata including `id`, `storyID`, and `storyName`. This refactoring significantly improves project visibility and organization for both in-progress and completed feature development.

**Implementation**: This set of changes introduces a `done.md` archiving mechanism for completed stories across `bltodo.py`, `domd.py`, `dtask`, and `gbops.py`. In `bltodo.py`, new functions and a `showdone` command are added to manage and display stories moved from `todo.md` to `done.md`, with `push_story` now automatically triggering this archiving. The `domd.py` and `dtask` scripts are updated to push all current work stories back to the backlog, deferring the decision to archive completed stories to `bltodo.py`. Finally, `gbops.py` gains a `resolve_story_status` function, which determines a story's completion based on its task states, forming the core logic for this new archiving workflow.

## 2026-09-22 14:25

---
workHeadline: 'feat: Implement `do.md` for in-progress tasks, formalize `dtask` content
  preservation via ADR and `done.md`'
specChanges: Refactored `dtask` documentation, updating `dtask-and-do-file-tasks.md`
  to refer to a new ADR, `dtask-issues.md`, which formalizes the decision for the
  `bltodo` plugin to save completed stories to `docs/dev/work/done/done.md` to prevent
  content loss during `dtask settle`.
workChanges: Migrated "init a feature to correct story moving behavior by dtask settle"
  story and tasks from `TODO.md` to a new `do.md` file for structured current work,
  while updating `TODO.md` with unique identifiers for remaining stories.
---

**Work Planning**: This change migrates an active development story, "init a feature to correct story moving behavior by dtask settle," along with its associated planning and implementation tasks, from `TODO.md` to a newly created `do.md` file. The `do.md` file is introduced as a dedicated space for current work, featuring structured metadata and sections for in-progress and completed tasks. Concurrently, `TODO.md` is updated to incorporate unique identifiers for its remaining stories, indicating a move towards more granular tracking of development items across both files.

**Specification**: The changes refactor documentation related to how `dtask` handles completed work and content preservation, introducing a new Architectural Decision Record (ADR). The file `docs/dev/spec/usecases/dtask/dtask-and-do-file-tasks.md` has been updated to remove detailed proposals for managing completed stories and preventing content loss, instead stating runtime behaviors for story and task statuses and referring to the new ADR. A new file, `docs/dev/spec/adr/dtask/dtask-issues.md`, was created to document the problem of content loss during `dtask settle`, explore various solutions, and formalize the accepted decision to have the `bltodo` plugin save completed stories to `docs/dev/work/done/done.md`. This shift clarifies the design decisions for `dtask`'s content management and recovery mechanisms.
