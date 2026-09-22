---
"actualCommitMessage": "developing specs to have dtasks settle completed stories to\
  \ the backlog api: bltodo in docs/dev/work..."
"description": "A list of small, focused tasks guiding the current commit with detailed\
  \ microsected activities."
"intendedCommitMessage": "Correct story moving behavior by dtask settle."
"priorCommit": "0c768e9ec75a873f3d04e4bf33e4b36167cb7259"
"title": "do.md"
"workBranch": "settle-story-move-fixes"
---

# Current work



## d - Story: init a feature to correct story moving behavior by dtask settle.
---
id: 3eef52a5-c922-7b93-be8f-c651526c1495-968152ff
---
dtask settle is ignoring stories that do not have tasks, which is not correct.

/ - finish drafting the plan in docs/dev/spec/usecases/dtask/dtask-and-do-file-tasks.md
---
id: 288f4b77-53c5-7f84-8287-e3876f677f53-81d7676c
---


/ - clean stuff out of the planning draft to proper places
---
id: 6ec073d3-8f22-7b8a-9dc1-84ba76da98e9-7d63f005
---
Some content from docs/dev/spec/usecases/dtask/dtask-and-do-file-tasks.md
should move to use cases, adrs.

/ - implement the needed backlog updateStory protocol
    / - update docs/dev/spec/backlog-spec.md
    ---
    prompt: 
    update the docs/dev/spec/backlog-spec.md to include implementation of UpdateStory and a subcommand update_story.  UpdateStory performs an upsert of a story, like PushStory does, but instead of lifting it to the top of te queue.
    The bltodo plugin will perform a logical (run time state) check of the new status, and if the story is now "completed" it will be written to as defined by the runtime state examining tasks, 

    ---

d - update the dtask final spec from the dtask-and-do-file-tasks.md
---
id: 2dfdc26a-a412-7453-b3f3-5e4a7c559e2e-4e33ea5d
---
 - any other specs, plus:
    - # usage situations.## dtask settle.### Needed corrections
    - # usage situations.## dtask settle.### More needed corrections


# Completed work


# Work Summary


## 2026-09-22 14:25

---
workHeadline: "feat: Implement `do.md` for in-progress tasks, formalize `dtask` content preservation via ADR and `done.md`"
specChanges: "Refactored `dtask` documentation, updating `dtask-and-do-file-tasks.md` to refer to a new ADR, `dtask-issues.md`, which formalizes the decision for the `bltodo` plugin to save completed stories to `docs/dev/work/done/done.md` to prevent content loss during `dtask settle`."
workChanges: "Migrated \"init a feature to correct story moving behavior by dtask settle\" story and tasks from `TODO.md` to a new `do.md` file for structured current work, while updating `TODO.md` with unique identifiers for remaining stories."
---

**Work Planning**: This change migrates an active development story, "init a feature to correct story moving behavior by dtask settle," along with its associated planning and implementation tasks, from `TODO.md` to a newly created `do.md` file. The `do.md` file is introduced as a dedicated space for current work, featuring structured metadata and sections for in-progress and completed tasks. Concurrently, `TODO.md` is updated to incorporate unique identifiers for its remaining stories, indicating a move towards more granular tracking of development items across both files.

**Specification**: The changes refactor documentation related to how `dtask` handles completed work and content preservation, introducing a new Architectural Decision Record (ADR). The file `docs/dev/spec/usecases/dtask/dtask-and-do-file-tasks.md` has been updated to remove detailed proposals for managing completed stories and preventing content loss, instead stating runtime behaviors for story and task statuses and referring to the new ADR. A new file, `docs/dev/spec/adr/dtask/dtask-issues.md`, was created to document the problem of content loss during `dtask settle`, explore various solutions, and formalize the accepted decision to have the `bltodo` plugin save completed stories to `docs/dev/work/done/done.md`. This shift clarifies the design decisions for `dtask`'s content management and recovery mechanisms.
