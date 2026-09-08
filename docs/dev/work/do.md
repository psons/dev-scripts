---
"actualCommitMessage": "reviewing docs/dev/spec/dtask-final-modules-spec.md and related\
  \ sources"
"description": "A list of small, focused tasks guiding the current commit with detailed\
  \ microsected activities."
"intendedCommitMessage": "Complete specs and generate ddf.py enhancement to parse\
  \ and serialize ddf documents with gbdata Tasks and Stories embedded in them "
"priorCommit": "52763a3a8c405c92465d29758e0e081768e1457f"
"title": "do.md"
"workBranch": "plugin-ddf"
---

# Acceptance criteria
Complete specs and generate ddf.py enhancement to parse and serialize ddf documents with gbdata Tasks and Stories embedded in them
use cases:
    User does `dtask commit --final` and before deleting do.md, dtask finds incomplete work in the do.md '#current work' section, it must push it back into the backlog, and remove it from do.md.
        the dtask must read the tasks out of do.md the do.md '#current work' section as a ddf object with embedded gbdata.Story objects, and determine if there are incomplete tasks.
            If there are incomplete tasks, any whole story with incomplete tasks should be 'pushed' back to the backlog using backlog.py.  At present the only implementation use by backlog.py is bltdo.py which uses TODO.md.
                the backlog.py plugin should support the PushStory protocol
                The bltodo.py implement the PushStory protocol per docs/dev/spec/backlog-spec.md (lift story to top of queue and Upsert tasks if te story exists) 
                    - The bltodo.py plugin should save a recovery copy of TODO.md before saving this update

    User does dtask commit notes completed tasks in the 'do.md# Completed work' section [do](./do.md#completed-work)
        tasks that are completed, abandoned, or unfinished are listed in the ./do.md#completed-work section
        Tasks are written as a list of tasks, without being enclosed in their stories.
        Tasks have a storyID attribute set to indicate the ID of the story they are part of.
        Tasks have a storyName attribute set to indicate the name of the story they are part of. 

# Current work


## dtask final design with DDF
/ - design specs for the dtask --final updates 
prompt: given the Acceptance criteria which describes how the dtask command needs to read and write do.md files and TODO.md files.   Propose a module structure to implement the operations to upsert tasks and implement the pushStory protocol, and add the attributes.storyID and attributes.storyName.  Note that some of thes operations would be hidden from dtask behind the backlog.py and bltodo.py modules.  Others would be called by dtask working with a DDF object representing do.md.  Take into consideration ease of update when the gbdata.py module must be updated to incorporate infrequent changes from the externally managed github.com/psons/gb-data repository 

## d - Story: DDF parsing with MDGBDF sections supported.
---
id: 6ef8e760-6efb-76f5-b56f-c6bb09e1f751-d8018269

epic: dtask can update do.md and TODO.md

---

d - compare the backlog.py protocol to the acceptance write up and reconcile what it means to 'push' a story.

/ - **Phase 2** (future - see [ddf-plugin-spec.md](./ddf-plugin-spec.md)): Plugin architecture
from === Implementation Phases (from docs/dev/spec/ddf-spec.md)
- Register plugins for specialized formats (e.g., MDGBDF for stories/tasks)
- Plugin-based section parsing via `ddfType` attribute
- Preserve specialized object models within DDF structure
    / - write the spec
    / add do.md example to spec.
    / carefully review: docs/dev/spec/usecases/ddf/do-dot-md-example.json 
    d - merge the plugin spec into the code ready spec.
    d - implement the code




## Story: record unfinished work and correlated summaries in do.md for dtask final.

d - When tasks are in progress in do.md and dtask --final is run, do.md should show the unfinished tasks
might be the # Completed Work section or a new $ unfinished section.
The intent is that work summaries and modified files can be understood with the tasks that were worked on, even if not finished.

d - file this analysis for organizing tasks and work summaries together
    - do some forward looking thinking as to whether a template can be re-structured without any code changes to make a story list where work summaries are together with tasks.  No, I think perhaps a work summary can have a task ID that was completed when wsum becomes task aware a lit of tasks that are now changed to in progress of completed can be paired with te work summary.  If dtask commit is run frequently and task statuses are updated, then the work summary will naturally be summarizing the work to complete the tasks.  At some point, perhaps an LLM can be trained to figure out work based on historical completed tasks.    



# Completed work

x - **Phase 1** (this spec): Basic DDF parsing and serialization
from === Implementation Phases (from docs/dev/spec/ddf-spec.md)
- Parse markdown documents to `DDFDoc` object model
- Support document and section front-matter (YAML)
- Support arbitrary heading nesting (H1-H6)
- Serialize to markdown and JSON with lossless round-trip

x - do design to work out how dtask can manipulate the do.md model loaded into memory as DDF.
    d - update the spec to explain how a document template looks to cause mdgbdf to be used to parse a section.
        docs/dev/spec/ddf-plugin-spec.md
    the spec should have the heading patterns call the mdgbdf parser, updated to account for the fact that they might not always be H1s.
        How does dtask have a role in defining the format of do.md, and the mdgbdf module knows about stories?

            x - spec that dtask passes the template pattern for do.md, to tell ddf which section should be parsed with mdgbdfdata.py
                    - The ' # Current Work' and'# Completed Work' sections?
                    
            x - dtask uses the template to figure out how to find the stories and tasks in the DDF doc model of do.md

x - Promote Bare Task lists in DDF to a backlog story
    get back to this issue:
    [Bare Task lists in DDF Issue](../spec/adr/ddf/ddf-issues.md#issue-bare-task-lists-in-ddf-documents)
    [Bare Task lists in DDF Issue github link](https://github.com/psons/dev-scripts/blob/main/docs/dev/spec/adr/ddf/ddf-issues.md#issue-bare-task-lists-in-ddf-documents)
    
    dev-scripts/docs/dev/spec/adr/ddf/ddf-issues.md:## issue: Bare task lists in DDF documents.  Promote it to a backlog item.

x - backlog item for stories/d-local-llm-for-wsum.md

# Work Summary

## 2026-09-06 12:24

---
workHeadline: "Advance DDF plugin specs and nullable section handling for MDGBDF-backed do.md parsing"
---


The changes advance DDF plugin support by updating the plugin specification to describe parsing and serialization through ddfType, template-driven section matching, plugin registry behavior, runtime ddfType preservation, and a concrete do.md template for routing # Current work and # Completed Work through MDGBDF. 

The DDF object model and implementation now allow DDFSection.sections to be None, with JSON schema, JSON deserialization, Markdown serialization, and tests updated so sections without children can be represented either as an empty list or null. 

New DDF design notes capture open issues around bare task lists, preamble plugin handling, and whether plugin calls should consume nested subsections or be applied section by section. 

The work documents were reorganized to reflect the current DDF/MDGBDF design effort, including refined tasks for dtask integration, bare task list handling, and future local LLM support for wsum.

## 2026-08-29 11:17

---
workHeadline: "feat(dtask): Work on spec and tasks to enable DDF parsing of do.md with MDGBDF sections for improved story and task management"
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
