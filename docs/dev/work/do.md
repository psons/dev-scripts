---
"actualCommitMessage": "feat(mdgbdata): Add MDGBDF-JSON conversion CLI with `tojson`,\
  \ `tomd` subcommands, extensive tests, and updated docs"
"description": "A list of small, focused tasks guiding the current commit with detailed\
  \ microsected activities."
"intendedCommitMessage": "build out backlog.py and bltodo plugin"
"priorCommit": "bd788f6fc546768f50e3c981c1ffeec5d21a67fb"
"title": "do.md"
"workBranch": "backlog-command"
---




x - improve the gb-data model to include an attribs dictionary that can hold unvalidated key-value data such as 'prompt: ' frontmatter like attributes for Goals, tasks, and stories.
 source: project: dev-scripts
 file: docs/dev/work/TODO.md
 - the attribs will be useful for holding data to be passed back from apps using backlog interfaces to the underlying implementation of the backlog when updating, such as a source file, or a story name if the underlying interface does not support stories as a first class object.  (This may be true of taskwarrior)

x - update the gbdata module to separate the gb-data types from the parsing capabilities so that backlog.py and plugins such as bltodo.py can import the same gb-data classes. 

    x - realign the specs to streamline maintenance.
    prompt: audit the information in docs/dev/spec/gbdata-spec-ready.md to determine if there is any background information in source documets docs/dev/spec/backlog-spec.md and docs/dev/spec/usecases/story-task-parsing-md.md that is pertinant to gbdata.py but not in gbdata-spec-ready.md include any missing information in a document  docs/dev/spec/md-gb-data-background.md 


        x - prompt: Please update the background doc to include any information that from docs/dev/spec/gbdata-spec.md that is not included in docs/dev/spec/gbdata-spec-ready.md.

        x - prompt: update the tone and perspective of docs/dev/spec/md-gb-data-background.md  to read as an authoritative source of reasoning for the specification in docs/dev/spec/gbdata-spec-ready.md.  The specs are to be streamlined so that docs/dev/spec/gbdata-spec.md can be treated as obsolete and moved to docs/dev/spec/obsolete, and later deleted.  It should be possible to regenerate gbdata.py from md-gb-data-background.md and gbdata-spec-ready.md without gbdata-spec.md. story-task-parsing-md.md will be retained for future user documentation, and may be referenced from md-gb-data-background.md, but should not be required for future revisions to gbdata.py.  The background file will be the foundation for a future refactor to separate markdown parsing from the gb types.

        x - prompt: move gbdata-spec-ready.md to docs/dev/spec and update any markdown links to its location.

        x - prompt: rename docs/dev/spec/gbdata-spec-ready.md to docs/dev/spec/gbdata-spec-2.md and updat all markdown references to it.

    x - split mdgbdata-spec.md out of docs/dev/spec/gbdata-spec-2.md.  Update 
    - parsing is existing spec, but the code ready spec will be impacted too.
    - it should describe serializing and deserializing the GB model as markdown
    - it should import gbdata.
       / - prompt: create a spec mdgbdata-spec.md from the markdown parsing related capabilities described in docs/dev/spec/gbdata-spec-2.md so that the classes in the resulting gbdata module could be imported into other modules to provide a unified data domain model for plugins to backlog.py.  Remove the markdown parsing specs from gbdata-spec-2.md.  Update the md-gb-data-background.md document to explain the separation.   

        x - update docs/dev/spec/mdgbdata-spec.md at 'Revision needed: ' marker to indicate how ids are to be generated (as they are for goal blotter or the task POC.)

        x - prompt:
            Refactor gbdata.py to separate the markdown parsing capabilities As described in docs/dev/spec/md-gb-data-background.md and the updated specs mentioned in that document.  A new module called mdgbdata.py will be created.  Also separate and update the unit tests so that tests for parsing functionality provide coverage for mdgbdata.py.
            The spec for mdgbdata.py is in docs/dev/spec/mdgbdata-spec.md
            The updated spec for gbdata.py is in docs/dev/spec/gbdata-spec-2.md



    x - fully describe MGBDF serialization docs/dev/spec/mdgbdata-spec.md

/ - review and test the functionality of mdgbdata.py
    x - add command line subcommand support to mdgbdata to do conversion between markdown and json. 
        prompt: 
            Implement the '### Command line Requirements' that have been added to mdgbdata-spec.md.
            Also generate BDD tests for the command line support.  
    x - update mdgbdata.py to include the story description attribute in the json schema and MDGBDF parsing per the updated docs/dev/spec/mdgbdata-spec.md.


# / story: Pilot a filesystem integration with TODO.md as a task store to start backlog.py and exercise interaction needed with do.md.
x - Update gb-data to include a status in the story type.
/ - write a version of backlog that parses stories and tasks out of a file and loads them into the GB domain model in memory
    x - write a spec to support a building python apps as the command module pattern based on wsum.py.
        - [python-command-module-skill.md](../spec/python-command-module-pattern.md)

/ - define the interface needed for plugins that backlog.py
 - docs/dev/spec/backlog-spec.md 
 - [backlog-spec.md](../spec/backlog-spec.md)

/ - finish bltodo.py spec which was started in the backlog spec.
    x - decide if the plugin should have command like capabilities, such as might support more specific behaviors than backlog.py.
        - No. see docs/dev/spec/adr/relationship between CLI and plugin modules.md   
        - refer to the section '# bltodo.py - The default plugin.' in the docs/dev/spec/backlog-spec.md

d - update dtask with a pop subcommand that pops a story by default from backlog.py and inserts it at the top of do.md, below the frontmatter.
    d - add a --task option to pop just 1 task instead of a whole story.
    



# Work Summary

## 2026-07-04 12:14

---
workHeadline: "feat(mdgbdata): Add MDGBDF-JSON conversion CLI with `tojson`, `tomd` subcommands, extensive tests, and updated docs"
---

This update significantly enhances `bin/mdgbdata.py` by introducing command-line functionality to convert between Markdown GB Data Form (MDGBDF) and JSON representations of stories and tasks. The module now supports `tojson`, `tomd`, and `help` subcommands, providing robust serialization and deserialization that includes story descriptions and task details. This new functionality is thoroughly documented in `docs/dev/spec/mdgbdata-spec.md`, outlining module and command-line requirements, including expected warning and error conditions for malformed inputs. Comprehensive BDD tests in `tests/features/mdgbdata/mdgbdata.feature` and `tests/steps/test_mdgbdata_steps.py` validate the command-line behavior, ensuring the tool correctly processes various input scenarios and provides appropriate feedback.
## 2026-07-04 09:55

---
workHeadline: "Refactor: Split `gbdata` into domain model and `mdgbdata` for parsing; update status enums and tests for clarity"
---

The `gbdata.py` module was refactored to serve exclusively as a shared domain model, with all markdown parsing and status metadata utilities extracted into a new `mdgbdata.py` module. This change introduces a distinct`StoryStatus` enum in `gbdata.py` and updates the `Task` and `Story` dataclasses to use non-optional status fields and more flexible attribute types. Correspondingly, unit tests were reorganized, with `test_gbdata.py`focusing on the domain model and a new `test_mdgbdata.py` covering the markdown parsing logic, including deterministic UUID generation for parsed stories and tasks. The `do.md` file was also updated to reflect this refactoring and clarify the new module responsibilities.


## 2026-06-11 09:34

---
workHeadline: "Refactor gbdata spec: new gbdata-spec-2.md, obsolete old spec, update background doc for gbdata.py generation"
---

The `gbdata-spec-ready.md` specification was replaced by `gbdata-spec-2.md`, now located directly in the `docs/dev/spec` directory, centralizing the implementation source of truth for `bin/gbdata.py`. The original `gbdata-spec.md` was moved to `docs/dev/spec/obsolete` and renamed `gbdata-spec-old.md`, formally marking it as obsolete. Supporting documentation, `md-gb-data-background.md`, was updated to reference the new `gbdata-spec-2.md` as the authoritative specification, reinforcing the streamlined documentation hierarchy. This change aims to simplify maintenance and ensure that `gbdata.py` can be generated solely from the current `gbdata-spec-2.md` and `md-gb-data-background.md`.
## 2026-06-11 09:21

---
workHeadline: "Realign gbdata docs: consolidate spec files, obsolete old, revise background rationale, and update tests and do.md"
---

The `docs/dev/spec/code-ready` directory has been removed, with its contents, `gbdata-spec-2.md` and associated JSON metadata files, moved directly into the `docs/dev/spec` directory. The `gbdata-spec.md` file has been marked obsolete and relocated to `docs/dev/spec/obsolete`, while the `md-gb-data-background.md` document has been substantially revised to serve as the authoritative rationale and governance context for the `gbdata.py` implementation. Consequently, test file paths in `tests/test_gbdata.py` have been updated to reflect these new document locations, and the `do.md` task list has been updated to reflect the progress on this specification realignment.
## 2026-06-11 08:54

---
workHeadline: "Docs: Add dryrun for bltodo load, plan gbdata refactor to mdgbdata module, and consolidate gbdata background info"
---

The `backlog-spec.md` file was updated to include a new `--dryrun` option for the `bltodo.py` load subcommand. The `do.md` file now outlines a detailed plan to refactor `gbdata.py` by extracting its markdown parsing capabilities into a new `mdgbdata.py` module, along with corresponding updates to documentation, specifications, and unit tests. A new file, `md-gb-data-background.md`, has been created to consolidate essential background and contextual information for `gbdata.py` from various source documents, aiming to establish an authoritative reference for future development and streamline the specification process by deprecating older, dispersed information.
## 2026-06-10 23:02

---
workHeadline: "feat: Expand backlog spec, update do.md, enhance gb-data attribs, and refine module patterns for backlog command"
---

The primary changes involve a significant expansion of the `backlog.py` specification, detailing its plugin architecture, default `bltodo.py` implementation, and data handling using a new "Markdown GB Data Form." Concurrently, the active work items in `do.md` were updated to reflect these developments, including enhancements to the `gb-data` model to incorporate an `attribs` dictionary. Minor clarifications were also made to the `python-command-module-pattern.md` for improved guidance and terminology consistency in `wsum-module-spec.md`. These updates collectively outline a clear path for implementing the new `backlog` command and its related data management capabilities.
## 2026-06-10 18:34

---
workHeadline: "feat(gbdata): Add `attribs` field to `Task` dataclass for flexible metadata; update specs and TODO"
---

This change introduces a new `attribs` dictionary field to the `Task` dataclass in `bin/gbdata.py`, enabling the storage of unvalidated key-value metadata. The `gbdata-spec-2.md` documentation was updated to reflect this addition, specifying that parsed markdown tasks should default `attribs` to `None` and outlining new tests for this functionality. The `TODO.md` file was also revised to clarify the purpose of the `attribs` field, emphasizing its role in facilitating data exchange between backlog interfaces and underlying implementations, and another task was marked as completed. This enhancement provides a flexible mechanism for applications to associate arbitrary data with tasks and stories within the `gbdata` model.
## 2026-06-10 16:48

---
workHeadline: "feat: Implement backlog.py command module & define CLI pattern; enhance dtask/gbdata for markdown task parsing"
---

This update introduces new specifications and tasks related to enhancing the `dtask` and `gbdata` tools, specifically focusing on a new `backlog.py` command module. Key changes include clarifying `dtask` branching strategy requirements, detailing `gbdata.py`'s parsing capabilities for markdown-based stories and tasks, and outlining a plugin architecture for `backlog.py` to manage various task sources like `TODO.md`. A new `python-command-module-pattern.md` defines a consistent structure for CLI tools, emphasizing `argparse` integration, testability, and a clear functional interface. The `TODO.md` file now reflects these new development streams, while a `do.md` file has been added to guide the current commit towards building out `backlog.py` and its initial `bltodo` plugin.
