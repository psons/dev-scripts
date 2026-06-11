---
"actualCommitMessage": "feat: Expand backlog spec, update do.md, enhance gb-data attribs,\
  \ and refine module patterns for backlog command"
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

d - update the gbdata module to separate the gb-data types from the parsing capabilities so that backlog.py and plugins it uses such as bltodo.py can import the same gb-data classes. 

    d - split mdgbdata-spec.md out of docs/dev/spec/gbdata-spec.md
    - parsing is existing spec, but the code ready spec will be impacted too.
    - it should describe serializing and deserializing the GB model as markdown
    - it should import gbdata.

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
