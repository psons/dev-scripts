---
"actualCommitMessage": "completed specs for correction: dtask settle is ignoring stories\
  \ that do not have tasks"
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

x - finish drafting the plan in docs/dev/spec/usecases/dtask/dtask-and-do-file-tasks.md
---
id: 288f4b77-53c5-7f84-8287-e3876f677f53-81d7676c
---


x - clean stuff out of the planning draft to proper places
---
id: 6ec073d3-8f22-7b8a-9dc1-84ba76da98e9-7d63f005
---
Some content from docs/dev/spec/usecases/dtask/dtask-and-do-file-tasks.md
should move to use cases, adrs.

/ - implement the needed backlog PushStory protocol
    / - update docs/dev/spec/backlog-spec.md
    ---
    prompt: 
    update the docs/dev/spec/backlog-spec.md to include implementation of PushStory and a subcommand pushstory.  PushStory has the behaviors specified for dtask settle in dtask-and-do-file-tasks.md    
    ---
    This task might be complete.


/ - specify user override behavior for Story.status
clarify in prompts and specs that it is the backlog that is a control interface for story status, and setting may be exposed to a caller (moved to use case doc). 
    x - update do and TODO examples in docs/dev/spec/usecases/dtask so that they do not have the 'd' status on stories.  This will now be considered superfluous behavior.

/ - Develop
    update tests that have been based on files in docs/dev/spec/usecases/dtask so that they do not have status in the heading per the revised examples.

    x - have ai: create an example of a story in do.md that will error because it has incomplete tasks, but has been flagged as completed or abandoned.
     prompt: read docs/dev/spec/backlog-spec.md, and create a file docs/dev/spec/usecases/dtask/do-file-with-error-story-status.md as an example of do.md file content with a story that will cause an error in bltodo.py because it has incomplete tasks, but has been flagged as completed or abandoned. Add a link reference to the example file from backlog-spec.md

    x - have ai: create an example of a story with no tasks and flagged as 'completed' that will be treated by backlog.py as completed and moved into the done file per the implementation behavior of bltodp.py.
     prompt: read docs/dev/spec/backlog-spec.md, and create a file docs/dev/spec/usecases/dtask/do-file-with-completed-no-tasks-story-status.md as an example of do.md file content with a story with no tasks and flagged as 'completed' that will be treated by backlog.py as completed and moved into the done file per the implementation behavior of bltodp.py. Add a link reference to the example file from backlog-spec.md

     prompt: Also create a matching done file example.

    x - have ai: create an example of a story where all tasks are completed or abandoned that will be treated by backlog.py as completed and moved into the done file per the implementation behavior of bltodp.py. 
    prompt:
    read docs/dev/spec/backlog-spec.md, and create a use case file  as an example of do.md file content with a story where all tasks are completed or abandoned that will be treated by backlog.py as completed and moved into the done file per the implementation behavior of bltodp.py.  Add a link reference to the example file from backlog-spec.md.  Also create the done file example.

d - Do the specified corrections to complete the story 
prompt: 
    Read:
        - Use case information in docs/dev/spec/usecases/dtask/dtask-and-do-file-tasks.md # usage situations.## dtask settle.### More needed corrections
        - Enhancements to the backlog PushStory implementation and behaviors of the bltodo.py plugin specified in docs/dev/spec/backlog-spec.md
        - and ADRs for dtask in docs/dev/spec/adr/dtask/dtask-issues.md 
    Then Update the story moving behavior of dtask settle per updated specifications to correct the problem: dtask settle is ignoring stories that do not have tasks, which is not correct.


x - The mdgbdata behaviors should be documented to never explicitly write a status into a serialized story or set the property if it has not been found in content being parsed.


### Delivery step


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
