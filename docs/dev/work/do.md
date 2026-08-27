---
"actualCommitMessage": "Formalize DDF: enhance TODO/do.md with DDF support, specify\
  \ parsing, object model, plugin architecture & examples"
"description": "A list of small, focused tasks guiding the current commit with detailed\
  \ microsected activities."
"intendedCommitMessage": ""
"priorCommit": "5b4fe98504037f0a3c621f629f5d8fce5248ffba"
"title": "do.md"
"workBranch": "basic-ddf"
---

# Current work

# d - Story: introduce basic DDF parsing
---
id: 47811019-b0e1-741c-800e-24e779d3bb99-171c1d27
epic: dtask can update do.md and TODO.md
---
x - import the proposed spec, and anything that may be in the backlog

/ - review spec and generate the DDF command.
 - docs/dev/spec/ddf-basic-spec.md 
 x - transform docs/dev/spec/ddf-spec-started-from-_mdgbdata-spec_.md 
 - review and update : docs/dev/spec/usecases/development-description-format-uses.md which was foundational for mdgbdf
 - incorporate - [Basic Spec](../spec/ddf-basic-spec.md) into [ddf-spec.md](../spec/ddf-spec.md)
 - review and update: docs/dev/spec/adr/script-ai-friendly-texts-development-description-format.md

d - make sure the ddf example file is mentioned. docs/dev/spec/usecases/ddf/normal-ddf.md
d - AI build out [ddf-spec.md](../spec/ddf-spec.md) to be full authoritative spec for the phase 1 version of ddf.py

d - generate phase 1 ddf module and tests.

 d - manual path doc built from mdgbdf spec: docs/dev/spec/ddf-spec-started-from-_mdgbdata-spec_.md
  prompt1: Write the H! section '## Markdown Parsing Requirements: definition of DDF' bty incorporating docs/dev/spec/ddf-basic-spec.md

   prompt2: Update the DDF spec to define the type DDFDoc as the top level type represented in goalBlotter.schema.json



# Completed work


# Work Summary


## 2026-08-27 15:26

---
workHeadline: "Formalize DDF: enhance TODO/do.md with DDF support, specify parsing, object model, plugin architecture & examples"
specChanges: "New documentation for DDF defines parsing and serialization of markdown to an in-memory object and back to JSON/markdown, including an extensible plugin architecture and concrete examples for acceptance testing."
workChanges: "The Development Description Format (DDF) has been formalized across `TODO.md` and `do.md` to enable programmatic work item manipulation, with `TODO.md` updated for unique story IDs, a core story renamed to \"DDF parsing with MDGBDF sections supported,\" and `dtask` mandated to treat a new `do.md` (featuring YAML front matter and DDF module tasks) as a DDF document."
---

**Work Planning**: This update formalizes the Development Description Format (DDF) within the project's work tracking. The `TODO.md` file was revised to include unique identifiers for stories, with a core story renamed to "DDF parsing with MDGBDF sections supported" to reflect enhanced parsing capabilities. A new story explicitly mandates that the `dtask` tool treat `do.md` as a DDF document. Concurrently, a new `do.md` file was created, featuring a structured YAML front matter and outlining specific tasks for implementing, specifying, and testing the DDF module. These changes collectively aim to enable programmatic manipulation of work items and standardize work descriptions across both `TODO.md` and `do.md`.

**Specification**: These changes introduce new documentation for the Development Description Format (DDF), outlining a comprehensive approach to parsing and serializing markdown content. The `ddf-basic-spec.md` and `ddf-spec.md` files define the core DDF object model, specifying how markdown, including front-matter and various heading levels, should be interpreted and converted to an in-memory object and back to JSON or markdown without data loss. A `plugin-ddf-spec.md` further details an extensible architecture for specialized section parsing. Finally, `normal-ddf.md` and `normal-ddf.json` provide a concrete example of a markdown document and its expected DDF JSON representation, serving as an acceptance test for the parser's behavior.
