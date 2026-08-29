---
"actualCommitMessage": "feat(dtask): Enable DDF parsing of do.md with MDGBDF sections\
  \ for improved story and task management"
"description": "A list of small, focused tasks guiding the current commit with detailed\
  \ microsected activities."
"intendedCommitMessage": ""
"priorCommit": "52763a3a8c405c92465d29758e0e081768e1457f"
"title": "do.md"
"workBranch": "plugin-ddf"
---


# Current work
# d - Story: DDF parsing with MDGBDF sections supported.
---
id: 6ef8e760-6efb-76f5-b56f-c6bb09e1f751-d8018269
epic: dtask can update do.md and TODO.md
---

d - template used by dtask for do.md can find the MDGBDF section '# Current Work'
---
id: 1e585069-3e8d-77bb-bdd1-5fc6513846a0-33d44846
---
    d - do design to work out how dtask can manipulate the do.md model loaded into memory as DDF.
        d - update the spec to explain how a document template looks to cause mdgbdf to be used to parse a section.
        the spec should have the heading patterns that are stories, such as '^# Story:' or whatever is in the mdgbdf parser, updated to account for the fact that they might not always be H1s.
            How does dtask have a role in defining the format of do.md, and the mdgbdf module knows about stories?
                - I think dtask tells ddf to use the mdgbdf parser for the H1 sections that have stories...
                    dtask passes the template pattern for do.md, which should also tell dtask where to find the stories and tasks in the DDF object of do.md
                        - Is this the ' # Current Work' section?
                        - do some forward looking thinking as to whether a template can be re-structured without any code changes to make a story list where work summaries are together with tasks.  No, I think perhaps a work summary can have a task ID that was completed when wsum becomes task aware a lit of tasks that are now changed to in progress of completed can be paired with te work summary.  If dtask commit is run frequently and task statuses are updated, then the work summary will naturally be summarizing the work to complete the tasks.  At some point, perhaps an LLM can be trained to figure out work based on historical completed tasks.    

    ### Implementation Phases (from docs/dev/spec/ddf-spec.md)

    **Phase 1** (this spec): Basic DDF parsing and serialization
    - Parse markdown documents to `DDFDoc` object model
    - Support document and section front-matter (YAML)
    - Support arbitrary heading nesting (H1-H6)
    - Serialize to markdown and JSON with lossless round-trip

    **Phase 2** (future - see [ddf-plugin-spec.md](./ddf-plugin-spec.md)): Plugin architecture
    - Register plugins for specialized formats (e.g., MDGBDF for stories/tasks)
    - Plugin-based section parsing via `ddfType` attribute
    - Preserve specialized object models within DDF structure


# Completed work


# Work Summary


## 2026-08-29 11:17

---
workHeadline: "feat(dtask): Enable DDF parsing of do.md with MDGBDF sections for improved story and task management"
workChanges: "A new story in `docs/dev/work/do.md` details enabling DDF parsing with MDGBDF sections for `dtask` to manage stories and tasks, outlining a multi-phase plan starting with basic parsing."
---

**Work Planning**: A new story has been added to `docs/dev/work/do.md`, outlining the work to enable DDF parsing with MDGBDF sections for improved story and task management. This update details how the `dtask` script will utilize the `ddf` module to interpret `do.md` content, specifically focusing on identifying stories and tasks within the document. The change also clarifies the multi-phase implementation plan for DDF parsing, with basic parsing as the immediate goal and a plugin architecture for specialized formats like MDGBDF slated for a future phase.
## 2026-08-29 11:12

---
workHeadline: "feat: Refactor DDF plugin docs, update TODO with DDF phases, and introduce do.md for structured task tracking"
specChanges: "Refactored DDF plugin documentation by moving and updating spec files, introducing a new document for DDF issues, updating related DDF spec references, and clarifying task/story history to formalize and strengthen the DDF framework."
workChanges: "`TODO.md` was updated to include detailed DDF \"Implementation Phases\" within existing stories, and a new `do.md` file was created with YAML front matter for commit-related metadata and sections for tracking work."
---

**Work Planning**: The `TODO.md` file was updated to include detailed "Implementation Phases" for the DDF (Development Description Format) within existing stories, outlining steps for basic parsing, plugin architecture, and full MDGBDF compatibility. Concurrently, a new `do.md` file was created, featuring YAML front matter to store commit-related metadata and sections for tracking current, completed, and summarized work, likely as part of a structured approach to managing development tasks.

**Specification**: This commit refactors the documentation for the Development Description Format (DDF) plugin specifications. The `script-ai-friendly-texts-development-description-format.md` and `plugin-ddf-spec.md` files have been moved and substantially updated to `docs/dev/spec/adr/ddf/script-ai-friendly-texts-development-description-format.md` and `docs/dev/spec/ddf-plugin-spec.md` respectively, aimed at clarifying the DDF's plugin architecture. A new document, `docs/dev/spec/adr/ddf/ddf-issues.md`, was introduced to address specific challenges related to heading level preservation and the distinct treatment of DDF and MDGBDF sections during serialization. Corresponding updates were made in `ddf-basic-spec.md` and `ddf-spec.md` to reference the new plugin specification. A minor clarification regarding task and story history was also included in `script-module-relationships.md`, all contributing to a more formalized and robust DDF framework.
