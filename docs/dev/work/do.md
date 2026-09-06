---
"actualCommitMessage": "Advance DDF plugin specs and nullable section handling for\
  \ MDGBDF-backed do.md parsing"
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
d - do design to work out how dtask can manipulate the do.md model loaded into memory as DDF.
    d - update the spec to explain how a document template looks to cause mdgbdf to be used to parse a section.
        docs/dev/spec/ddf-plugin-spec.md
    the spec should have the heading patterns call the mdgbdf parser, updated to account for the fact that they might not always be H1s.
        How does dtask have a role in defining the format of do.md, and the mdgbdf module knows about stories?

            d - spec that dtask passes the template pattern for do.md, to tell ddf which section should be parsed with mdgbdfdata.py
                    - The ' # Current Work' and'# Completed Work' sections?
                    
            d - dtask uses the template to figure out how to find the stories and tasks in the DDF doc model of do.md

=== Implementation Phases (from docs/dev/spec/ddf-spec.md)

x - **Phase 1** (this spec): Basic DDF parsing and serialization
- Parse markdown documents to `DDFDoc` object model
- Support document and section front-matter (YAML)
- Support arbitrary heading nesting (H1-H6)
- Serialize to markdown and JSON with lossless round-trip

/ - **Phase 2** (future - see [ddf-plugin-spec.md](./ddf-plugin-spec.md)): Plugin architecture
- Register plugins for specialized formats (e.g., MDGBDF for stories/tasks)
- Plugin-based section parsing via `ddfType` attribute
- Preserve specialized object models within DDF structure
    / - write the spec
    / add do.md example to spec.
    / carefully review: docs/dev/spec/usecases/ddf/do-dot-md-example.json 
    d - merge the plugin spec into the code ready spec.
    d - implement the code


d - Promote Bare Task lists in DDF to a backlog story
    get back to this issue:
    dev-scripts/docs/dev/spec/adr/ddf/ddf-issues.md:## issue: Bare task lists in DDF documents.  Promote it to a backlog item.

d - file this analysis for organizing tasks and work summaries together
    - do some forward looking thinking as to whether a template can be re-structured without any code changes to make a story list where work summaries are together with tasks.  No, I think perhaps a work summary can have a task ID that was completed when wsum becomes task aware a lit of tasks that are now changed to in progress of completed can be paired with te work summary.  If dtask commit is run frequently and task statuses are updated, then the work summary will naturally be summarizing the work to complete the tasks.  At some point, perhaps an LLM can be trained to figure out work based on historical completed tasks.    

# Story: Establish local LLM for wsum
A free local LLM and local AI tool can be a key piece of running dev-scripts without costly tool support. 
wsum is not that demanding, so a simple local LLM should be available to generate the summaries.  Olama is likely the tool, and the vid below explains what is needed. I probably want an installer, and some product, maybe the one pitched in the vid to select a model
d - add a backlog item to allow wsum.py to work without google gemini.
 - Here is a youtube vid with a basis for how to proceed.
    - https://www.google.com/search?q=local+ai&oq=local+&gs_lcrp=EgZjaHJvbWUqDQgBEAAYkQIYgAQYigUyBggAEEUYOTINCAEQABiRAhiABBiKBTINCAIQABiRAhiABBiKBTINCAMQABiRAhiABBiKBTINCAQQABiRAhiABBiKBTIKCAUQABixAxiABDINCAYQLhivARjHARiABDIHCAcQABiABDITCAgQLhiDARivARjHARixAxiABDIHCAkQABiPAtIBCTg1NDBqMGoxNagCCLACAfEFuRx0qh0tjj7xBbkcdKodLY4-&sourceid=chrome&source=chrome.rb&ie=UTF-8#fpstate=ive&vld=cid:b0e850a7-31f1-4749-8c5c-7330f34084de_443cf449,vid:edIHPoWgIKU,st:85 
 - maybe a free, ideally local LLM.
 - Maybe just add some configurability, to include copilot, since copilot seems to provide a role as an interface to other moidel providers (even a reseller of those models)
 d - build an installer 

# Completed work


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
