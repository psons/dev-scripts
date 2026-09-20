---
actualCommitMessage: dtask commit --final now performs dtask settle before removing
  do.md
description: A list of small, focused tasks guiding the current commit with detailed
  microsected activities.
intendedCommitMessage: 'Complete specs and generate ddf.py enhancement to parse and
  serialize ddf documents with gbdata Tasks and Stories embedded in them '
priorCommit: 52763a3a8c405c92465d29758e0e081768e1457f
title: do.md
workBranch: plugin-ddf
---

# Acceptance criteria
Complete specs and generate ddf.py enhancement to parse and serialize ddf documents with gbdata Tasks and Stories embedded in them
use cases:
    User does `dtask commit --final` and before deleting do.md, dtask finds incomplete work in the do.md '#current work' section, it must push it back into the backlog, and remove it from do.md.
        the dtask must read the tasks out of do.md the do.md '#current work' section as a ddf object with embedded gbdata.Story objects, and determine if there are incomplete tasks.
            If there are incomplete tasks, any whole story with incomplete tasks should be 'pushed' back to the backlog using backlog.py.  At present the only implementation use by backlog.py is bltodo.py which uses TODO.md.
                the backlog.py plugin should support the PushStory protocol
                The bltodo.py implement the PushStory protocol per docs/dev/spec/backlog-spec.md (lift story to top of queue and Upsert tasks if te story exists)
                    - The bltodo.py plugin should save a recovery copy of TODO.md before saving this update

    User does dtask commit notes completed tasks in the 'do.md# Completed work' section [do](./do.md#completed-work)
        tasks that are completed, abandoned, or unfinished are listed in the ./do.md#completed-work section
        Tasks are written as a list of tasks, without being enclosed in their stories.
        Tasks have a storyID attribute set to indicate the ID of the story they are part of.
        Tasks have a storyName attribute set to indicate the name of the story they are part of.

## External integration wih Goal Blotter
Goal Blotter is not planned to support documents like DDF documents in its data domain, but will rather have some scheme to support links in description fields to documents and resources needed to complete Tasks and Stories.

# Current work

## x - Story: dtask final design with DDF
---
id: 378696af-f825-7014-a5c8-b44613991e88-7fbdbe43
---


## x - Story: DDF parsing with MDGBDF sections supported.
---
id: 6ef8e760-6efb-76f5-b56f-c6bb09e1f751-d8018269
epic: dtask can update do.md and TODO.md
---

# story: implement dtask settle.
x - build out use case example.
prompt:

With selected context in docs/dev/spec/usecases/docs/dev/spec/usecases/dtask/dtask-and-do-file-tasks.md,

    create a file that shows the state of do.md after running dtask settle where do.md had been in the
    state of docs/dev/spec/usecases/docs/dev/spec/usecases/dtask/basic-do-file-after-pop-with-progress.md.
    the new file should be docs/dev/spec/usecases/docs/dev/spec/usecases/dtask/basic-do-file-after-settle.md.

    The dtask settle command, when implemented will do all the operations desired on the do.md file and the backlog for dtask commit --final, except that it will not do a git commit and not remove do.md.

x - add support for dtask settle
prompt:

Implement the dtask settle subcommand to do all the operations desired on the do.md file and the backlog for dtask commit --final, except that it will not do a git commit and not remove do.md.

BDD tests should be generated in accordance with docs/dev/spec/usecases/docs/dev/spec/usecases/dtask/dtask-and-do-file-tasks.md # usage situations.## dtask settle

Help text should be added

x - **Phase 2** (future - see [ddf-plugin-spec.md](./ddf-plugin-spec.md)): Plugin architecture
from === Implementation Phases (from docs/dev/spec/ddf-spec.md)
- Register plugins for specialized formats (e.g., MDGBDF for stories/tasks)
- Plugin-based section parsing via `ddfType` attribute
- Preserve specialized object models within DDF structure
    x - write the spec
    x - add do.md example to spec.
    x carefully review: docs/dev/spec/usecases/ddf/do-dot-md-example.json
    a - merge the plugin spec into the code ready spec.
        for now, docs/dev/spec/dtask-final-modules-spec.md can remain a freestanding code ready spec for the integrated DDF plugin solution.
        - implement the code as part of dtask --final AI step.

x - Implement the code ready spec docs/dev/spec/dtask-final-modules-spec.md

x - compare the backlog.py protocol to the acceptance write up and reconcile what it means to 'push' a story.

# Completed work

---
id: 08de6878-8f5e-7ff3-9b8f-c472544ec177-6a7e38b4
---

x - design specs for the dtask --final updates
---
id: d9da7fef-16a4-7910-8758-34917c830427-20c5c8cf
prompt: given the Acceptance criteria which describes how the dtask command needs
  to read and write do.md files and TODO.md files.   Propose a module structure to
  implement the operations to upsert tasks and implement the pushStory protocol, and
  add the attributes.storyID and attributes.storyName.  Note that some of these operations
  would be hidden from dtask behind the backlog.py and bltodo.py modules.  Others
  would be called by dtask working with a DDF object representing do.md.  Take into
  consideration ease of update when the gbdata.py module must be updated to incorporate
  infrequent changes from the externally managed github.com/gb-data repository
---

x - review the generated spec:
---
id: 373e8088-5da0-7b5c-ae17-a6fd1a615594-fca4725c
---
docs/dev/spec/dtask-final-modules-spec.md

x - ask AI to verify that the spec still matches [ADR](../spec/adr/ddf/ddf-issues.md) decisions
---
id: 8e8b32a5-d194-7407-a039-3870345d9316-6b396aaa
---

x - resolve issues with # dtask commit --final module structure spec.## 3. bin/mdgbdata.py — heading-level offset support.### 3.1 Parsing
---
id: ba292e3f-294d-799a-a85e-376e8598b3c2-684bb11a
---
around line 160 ...

```markdown
- The existing implicit file-scope story (content before the first story heading) is unchanged and
  is still produced when text precedes the first heading at `story_heading_level`.
```
When mdgbdata is called to parse a section called in a ddf document, a DDFSection is needed by the caller, so the content before the first story needs to be saved.  DDF would save this as preamble text, however in a section parsed by mdgbdata, it will be saves as a text only story at the beginning of the Story list.  The Story list will be saves as the sections attribute in the DDFSection returned by the mdgbdata  should be set as the preamble text in that DDFSection.
    affects:
        docs/dev/spec/dtask-final-modules-spec.md:
            # dtask commit --final module structure spec.## 5. bin/ddfmdgbdf.py — NEW: the MDGBDF plugin
When mdgbdata is used to parse a document, which may be a file, the ddf module is not involved, the object model only uses gbdata.py types (not DDFSection), and the return is a list of Story objects, so a file scoped text story is needed at the beginning of the list to store that content.

x - **Phase 1** (this spec): Basic DDF parsing and serialization
---
id: bb26ced0-6ae0-7a3a-b616-ae79cdd3ae54-f0c7b54b
---
from === Implementation Phases (from docs/dev/spec/ddf-spec.md)
- Parse markdown documents to `DDFDoc` object model
- Support document and section front-matter (YAML)
- Support arbitrary heading nesting (H1-H6)
- Serialize to markdown and JSON with lossless round-trip

x - do design to work out how dtask can manipulate the do.md model loaded into memory as DDF.
---
id: 8ba0fe62-4d47-7608-8bb7-57ce04f2c17d-73cad705
---
    d - update the spec to explain how a document template looks to cause mdgbdf to be used to parse a section.
        docs/dev/spec/ddf-plugin-spec.md
    the spec should have the heading patterns call the mdgbdf parser, updated to account for the fact that they might not always be H1s.
        How does dtask have a role in defining the format of do.md, and the mdgbdf module knows about stories?

            x - spec that dtask passes the template pattern for do.md, to tell ddf which section should be parsed with mdgbdata.py
                    - The ' # Current Work' and'# Completed Work' sections?

            x - dtask uses the template to figure out how to find the stories and tasks in the DDF doc model of do.md

x - Promote Bare Task lists in DDF to a backlog story
---
id: 7a97968e-4d10-7120-9f0d-7606db9ce6e4-04a86d3d
---
    get back to this issue:
    [Bare Task lists in DDF Issue](../spec/adr/ddf/ddf-issues.md#issue-bare-task-lists-in-ddf-documents)
    [Bare Task lists in DDF Issue github link](https://github.com/psons/dev-scripts/blob/main/docs/dev/spec/adr/ddf/ddf-issues.md#issue-bare-task-lists-in-ddf-documents)

    dev-scripts/docs/dev/spec/adr/ddf/ddf-issues.md:## issue: Bare task lists in DDF documents.  Promote it to a backlog item.

x - backlog item for stories/d-local-llm-for-wsum.md
---
id: 89b72eee-f9a1-7ccd-ba89-aa1c0016998a-12880d48
---

# Work Summary


## 2026-09-20 17:06

---
workHeadline: 'feat: Improve dtask story/task management; ensure completed tasks persist
  on settle and refine do.md formatting'
specChanges: The `dtask-and-do-file-tasks.md` spec is updated to clarify `dtask` and
  `do.md` behavior, specifying that `do.md` should contain bare tasks within story
  sections, `dtask settle` must include completed tasks when stories are returned
  to the backlog, whole stories must be moved during push/pop, and tasks written to
  `do.md` are upserted copies.
---

**Specification**: The provided git diff updates the `dtask-and-do-file-tasks.md` specification document, introducing a new section for "Needed corrections." This section clarifies several critical behaviors for the `dtask` utility, particularly concerning how tasks and stories are handled within the `do.md` file and during the `dtask settle` operation. It specifies that `do.md` should only contain bare tasks, without redundant story metadata when within a story section, and that `dtask settle` must include completed tasks when stories are returned to the backlog. Additionally, the document now emphasizes that the system should always move whole stories during push and pop operations, and that tasks written to `do.md` are copies from their source stories, managed via upsert.

**Implementation**: The `domd.py` script and related `dtask` command have been updated to improve how tasks are managed between the `do.md` file and the backlog. The primary change ensures that when `do.md` is settled or finalized, all tasks associated with a story—including those marked as completed—are preserved and pushed back to the backlog, preventing data loss. Additionally, stories popped into `do.md` are now correctly formatted with H2 headings under the "Current work" section, and a new `gbops.strip_story_ref` utility removes story metadata from tasks harvested into the "Completed work" section, keeping them as bare entries. Corresponding tests have been updated and added to validate these new behaviors.

## 2026-09-06 12:24

---
workHeadline: Advance DDF plugin specs and nullable section handling for MDGBDF-backed
  do.md parsing
---


The changes advance DDF plugin support by updating the plugin specification to describe parsing and serialization through ddfType, template-driven section matching, plugin registry behavior, runtime ddfType preservation, and a concrete do.md template for routing # Current work and # Completed Work through MDGBDF.

The DDF object model and implementation now allow DDFSection.sections to be None, with JSON schema, JSON deserialization, Markdown serialization, and tests updated so sections without children can be represented either as an empty list or null.

New DDF design notes capture open issues around bare task lists, preamble plugin handling, and whether plugin calls should consume nested subsections or be applied section by section.

The work documents were reorganized to reflect the current DDF/MDGBDF design effort, including refined tasks for dtask integration, bare task list handling, and future local LLM support for wsum.

## 2026-08-29 11:17

---
workHeadline: 'feat(dtask): Work on spec and tasks to enable DDF parsing of do.md
  with MDGBDF sections for improved story and task management'
workChanges: A new story in `docs/dev/work/do.md` details enabling DDF parsing with
  MDGBDF sections for `dtask` to manage stories and tasks, outlining a multi-phase
  plan starting with basic parsing.
---

**Work Planning**: A new story has been added to `docs/dev/work/do.md`, outlining the work to enable DDF parsing with MDGBDF sections for improved story and task management. This update details how the `dtask` script will utilize the `ddf` module to interpret `do.md` content, specifically focusing on identifying stories and tasks within the document. The change also clarifies the multi-phase implementation plan for DDF parsing, with basic parsing as the immediate goal and a plugin architecture for specialized formats like MDGBDF slated for a future phase.

## 2026-08-29 11:12

---
workHeadline: 'feat: Refactor DDF plugin docs, update TODO with DDF phases, and introduce
  do.md for structured task tracking'
specChanges: Refactored DDF plugin documentation by moving and updating spec files,
  introducing a new document for DDF issues, updating related DDF spec references,
  and clarifying task/story history to formalize and strengthen the DDF framework.
workChanges: '`TODO.md` was updated to include detailed DDF "Implementation Phases"
  within existing stories, and a new `do.md` file was created with YAML front matter
  for commit-related metadata and sections for tracking work.'
---

**Work Planning**: The `TODO.md` file was updated to include detailed "Implementation Phases" for the DDF (Development Description Format) within existing stories, outlining steps for basic parsing, plugin architecture, and full MDGBDF compatibility. Concurrently, a new `do.md` file was created, featuring YAML front matter to store commit-related metadata and sections for tracking current, completed, and summarized work, likely as part of a structured approach to managing development tasks.

**Specification**: This commit refactors the documentation for the Development Description Format (DDF) plugin specifications. The `script-ai-friendly-texts-development-description-format.md` and `plugin-ddf-spec.md` files have been moved and substantially updated to `docs/dev/spec/adr/ddf/script-ai-friendly-texts-development-description-format.md` and `docs/dev/spec/ddf-plugin-spec.md` respectively, aimed at clarifying the DDF's plugin architecture. A new document, `docs/dev/spec/adr/ddf/ddf-issues.md`, was introduced to address specific challenges related to heading level preservation and the distinct treatment of DDF and MDGBDF sections during serialization. Corresponding updates were made in `ddf-basic-spec.md` and `ddf-spec.md` to reference the new plugin specification. A minor clarification regarding task and story history was also included in `script-module-relationships.md`, all contributing to a more formalized and robust DDF framework.
