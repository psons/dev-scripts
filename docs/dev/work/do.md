---
"actualCommitMessage": "Realign gbdata docs: consolidate spec files, obsolete old,\
  \ revise background rationale, and update tests and do.md"
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

/ - update the gbdata module to separate the gb-data types from the parsing capabilities so that backlog.py and plugins such as bltodo.py can import the same gb-data classes. 

    x - realign the specs to streamline maintenance.
    prompt: audit the information in docs/dev/spec/gbdata-spec-ready.md to determine if there is any background information in source documets docs/dev/spec/backlog-spec.md and docs/dev/spec/usecases/story-task-parsing-md.md that is pertinant to gbdata.py but not in gbdata-spec-ready.md include any missing information in a document  docs/dev/spec/md-gb-data-background.md 


    prompt: Please update the background doc to include any information that from docs/dev/spec/gbdata-spec.md that is not included in docs/dev/spec/gbdata-spec-ready.md.

    prompt: update the tone and perspective of docs/dev/spec/md-gb-data-background.md  to read as an authoritative source of reasoning for the specification in docs/dev/spec/gbdata-spec-ready.md.  The specs are to be streamlined so that docs/dev/spec/gbdata-spec.md can be treated as obsolete and moved to docs/dev/spec/obsolete, and later deleted.  It should be possible to regenerate gbdata.py from md-gb-data-background.md and gbdata-spec-ready.md without gbdata-spec.md. story-task-parsing-md.md will be retained for future user documentation, and may be referenced from md-gb-data-background.md, but should not be required for future revisions to gbdata.py.  The background file will be the foundation for a future refactor to separate markdown parsing from the gb types.

    prompt: move gbdata-spec-ready.md to docs/dev/spec and update any markdown links to its location.

    d - split mdgbdata-spec.md out of docs/dev/spec/gbdata-spec.md
    - parsing is existing spec, but the code ready spec will be impacted too.
    - it should describe serializing and deserializing the GB model as markdown
    - it should import gbdata.
        prompt:
            There is a need to refactor gbdata.py to separate the markdown parsing capabilities into a new module called mdgbdata.py.  Unit tests wil also need to be updated.

            As a first step. separate 



            
            Also separate the unit tests for mdgbdata from gbdata.py.  It is expected that the types gbdata defines will be imported by mdgbdata.py.  The  

        d - This is prompt 1 of 2 to migrate gbdata.py markdown parsing capabilities to a new module.  This first prompt is to create the new module and the new capabilities. prompt 1 of 2 to duplicate gbdata.py markdown parsing capabilities in a new module called mdgbdata.py:
            generate docs/dev/spec/mdgbdata-spec.md as a spec for mdgbdata.py with the parsing capabilities of gbdata.py. mdgbdata.py will replace gbdata.py as a parser, so create unit tests for mdgbdata.py to match the tests for gbdata.py to match  
        d - prompt 2 of 2 to remove markdown parsing capabilities from gbdata.py:
            remove the markdown parsing capabilities from docs/dev/spec/gbdata-spec.md that have been migrated to mdgbdata-spec.md.
                - regenerate docs/dev/spec/gbdata-spec-ready.md and gbdata.py (Actually should enhance gbdata-spec.md to eliminate need for code-ready directory)
                - regenerate gbdata.py (determine if it still needs ay unit testing, ad adapt as appropriate)

    d - fully describe MGBDF serialization docs/dev/spec/mdgbdata-spec.md




# / story: Pilot a filesystem integration with TODO.md as a task store to start backlog.py and exercise interaction needed with do.md.
x - Update gb-data to include a status in the story type.
/ - write a version of backlog that parses stories and tasks out of a file and loads them into the GB domain model in memory
    x - write a spec to support a building python apps as the command module pattern based on wsum.py.
        - [python-command-module-skill.md](../spec/python-command-module-pattern.md)

/ - define the interface needed for plugins that backlog.py
 - docs/dev/spec/backlog-spec.md 
 - [backlog-spec.md](../spec/backlog-spec.md)

d - update dtask with a pop subcommand that pops a story by default from backlog.py and inserts it at the top of do.md, below the frontmatter.
    d - add a --task option to pop just 1 task instead of a whole story.
    



# Work Summary


## 2026-06-11 09:21

---
workHeadline: "Realign gbdata docs: consolidate spec files, obsolete old, revise background rationale, and update tests and do.md"
---

The `docs/dev/spec/code-ready` directory has been removed, with its contents, `gbdata-spec-ready.md` and associated JSON metadata files, moved directly into the `docs/dev/spec` directory. The `gbdata-spec.md` file has been marked obsolete and relocated to `docs/dev/spec/obsolete`, while the `md-gb-data-background.md` document has been substantially revised to serve as the authoritative rationale and governance context for the `gbdata.py` implementation. Consequently, test file paths in `tests/test_gbdata.py` have been updated to reflect these new document locations, and the `do.md` task list has been updated to reflect the progress on this specification realignment.
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

This change introduces a new `attribs` dictionary field to the `Task` dataclass in `bin/gbdata.py`, enabling the storage of unvalidated key-value metadata. The `gbdata-spec-ready.md` documentation was updated to reflect this addition, specifying that parsed markdown tasks should default `attribs` to `None` and outlining new tests for this functionality. The `TODO.md` file was also revised to clarify the purpose of the `attribs` field, emphasizing its role in facilitating data exchange between backlog interfaces and underlying implementations, and another task was marked as completed. This enhancement provides a flexible mechanism for applications to associate arbitrary data with tasks and stories within the `gbdata` model.
## 2026-06-10 16:48

---
workHeadline: "feat: Implement backlog.py command module & define CLI pattern; enhance dtask/gbdata for markdown task parsing"
---

This update introduces new specifications and tasks related to enhancing the `dtask` and `gbdata` tools, specifically focusing on a new `backlog.py` command module. Key changes include clarifying `dtask` branching strategy requirements, detailing `gbdata.py`'s parsing capabilities for markdown-based stories and tasks, and outlining a plugin architecture for `backlog.py` to manage various task sources like `TODO.md`. A new `python-command-module-pattern.md` defines a consistent structure for CLI tools, emphasizing `argparse` integration, testability, and a clear functional interface. The `TODO.md` file now reflects these new development streams, while a `do.md` file has been added to guide the current commit towards building out `backlog.py` and its initial `bltodo` plugin.
