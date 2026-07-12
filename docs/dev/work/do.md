---
"actualCommitMessage": "refactor: Rename Task.attribs to Task.attributes across codebase, updating parsing, serialization, docs, and tests for consistency"
"description": "A list of small, focused tasks guiding the current commit with detailed\
  \ microsected activities."
"intendedCommitMessage": "implement dtask pop subcommand"
"priorCommit": "32341444081849db3d0e713686fcf82468281ce8"
"title": "do.md"
"workBranch": "dtask-pop"
---

# Completed work

x - update the gbdata model property name "attribs" to "attributes"

## story: support story attributes in tasks
Proceed with work to support attributes in tasks, such as the story id and title.
This is in a state of partial specification, and specs need to be cleaned up with respect 
to abandoned work to support task level popping from backlog.py -> bltodo.py

### stages of work to implement:
#### 1 - spec support reading informal mark down attributes
x - generate / update spec from user documentation
prompt: update the docs/dev/spec/mdgbdata-spec.md per the '# Ad hoc attributes' section of docs/dev/spec/usecases/story-task-parsing-md.md. Assure that other updates to describe that mdgbdata-spec.md accounts for scope and implementation of its responsibilities for serialization of MDGBDF and JSON are retained. 

x - generate / update code from software spec
prompt: update mdgbdata.py from the updated docs/dev/spec/mdgbdata-spec.md and also update tests.

x - check it out with test it with tojson

x - support writing attributes in formal markdown as YAML
    - per '#### MDGBDF Front-matter for Section, Story, or Task'
    in docs/dev/spec/mdgbdata-spec.md

x - verify / support reading the form front-matter


# - avoid anonymous-story as an id
 - assure that Story objects always have IDS that exist for their life time.
 x - update the spec
 x - prompt: update mdgbdata.py and tests to conform with the update in the '### ID Generation' section of docs/dev/spec/mdgbdata-spec.md.



# Work Summary

## 2026-07-12 11:50

---
workHeadline: "refactor: Rename Task.attribs to Task.attributes across codebase, updating parsing, serialization, docs, and tests for consistency"
---

The primary change in this diff is the renaming of the `attribs` field to `attributes` within the `Task` dataclass in `bin/gbdata.py` and `bin/mdgbdata.py`, affecting how ad-hoc task properties are stored and processed. This modification is propagated throughout the codebase, including updates to the parsing logic in `_parse_frontmatter_block` and `parse_stories_from_markdown`, and serialization functions like `_task_to_dict` and `_render_markdown_story` in `bin/mdgbdata.py`. Supporting documentation in `docs/dev/spec/gbdata-spec-2.md`, `docs/dev/spec/mdgbdata-spec.md`, and `docs/dev/spec/usecases/story-task-parsing-md.md` has been updated to reflect this new field name and its implications for user-defined attributes. Corresponding unit tests in `tests/test_gbdata.py` and `tests/test_mdgbdata.py` were also adjusted to validate the `attributes` field's default behavior, parsing, and serialization, ensuring consistency across the application. Additionally, minor updates were made to `docs/dev/spec/usecases/README.md`, `docs/dev/work/TODO.md`, and `docs/dev/work/do.md` to refine descriptions and reflect progress on related work items.

## 2026-07-11 10:52

---
workHeadline: "feat: Implement ad-hoc task attributes in `mdgbdata.py` with Markdown frontmatter support, parsing, serialization, and tests"
---

The `mdgbdata.py` script has been significantly enhanced to support ad-hoc attributes for tasks, allowing users to define custom `key: value` pairs directly within Markdown. This update introduces parsing logic for both single-line attributes and multi-line frontmatter blocks delimited by `---`, integrating these new properties into the `Task.attribs` field. Furthermore, the script now serializes these attributes back into Markdown as YAML frontmatter and includes them in the JSON representation of stories and tasks. The `mdgbdata-spec.md` document was updated to formally describe these new parsing and serialization rules, while `test_mdgbdata.py` now includes comprehensive tests to ensure correct behavior and data round-tripping for the ad-hoc task attributes.
## 2026-07-11 09:52

---
workHeadline: "Refactor `mdgbdata` docs; move ad-hoc attribute rules; clarify JSON parsing; split story/task docs; update TODOs"
---

This diff primarily refactors documentation related to markdown parsing and attribute handling for `mdgbdata.py`. Key changes include migrating detailed 'Ad hoc attribute' rules from `mdgbdata-spec.md` to `story-task-parsing-md.md` for better organization, while also clarifying the `mdgbdata.py`'s parsing scope and adding a requirement for JSON parsing. The `story-task-parsing.md` file was split, with task status parsing rules moved to a new, dedicated `story-task-status-parsing.md` file. Furthermore, the `TODO.md` and `do.md` files were updated to reflect future work, including a planned refactoring of the 'attribs' property to 'attributes' in the `gbdata` model and explicit steps for updating the `mdgbdata-spec.md` to incorporate the new attribute handling definitions.
## 2026-07-08 17:46
"
---
workHeadline: "Add gshove.sh: automate backing up uncommitted changes to a new branch, push, and restore original state"
---

A new shell script, `gshove.sh`, has been added to the `bin` directory. This script automates the process of taking all uncommitted changes from the current branch, moving them to a newly created `shove-<original_branch_name>` branch, committing them with a user-provided message, and pushing that branch to the remote. This functionality is crucial for preventing data loss by ensuring un-pushed work is safely backed up. After pushing, the script meticulously restores the original branch to its exact previous state, including staged, unstaged, and untracked files, while also providing instructions for branch cleanup.
## 2026-07-08 17:41

---
workHeadline: "Docs: Improve `dtask` README for AI-driven workflow, prune obsolete docs, add `TODO.md` caveats & simplify task lists"
---

The `dtask` README has been updated to clarify its role in automating the workflow between work tasks and git commits, emphasizing its use with `do.md` for AI prompts and improved commit message generation. Concurrently, obsolete architectural proposals related to "script-ai-friendly-texts" have been removed from the documentation. The `TODO.md` file now includes crucial limitations and assumptions regarding data handling and the `pop` subcommand, while `do.md` reflects ongoing deliberations about simplifying task list support within `backlog.py` and `mdgbdata.py` to streamline the overall task management workflow.
## 2026-07-07 13:19

---
workHeadline: "feat: Introduce DDF spec, enhance `mdgbdata` with tasklist support and formal attribute parsing rules"
---

The project introduces a new "Development Description Format" (DDF) specification, centralizing attribute handling for stories and tasks in Markdown. This expands `mdgbdata.py`'s capabilities to include serialization and a new `--tasklist` option, allowing tasks to be output individually with their parent story's ID and name. The `mdgbdata-spec.md` now details both informal (single-line) and formal (YAML front-matter) rules for attribute parsing and writing, replacing prior ad-hoc definitions. The `do.md` work log reflects progress on formalizing story IDs and outlines a new story to enable `backlog` and `mdgbdata` to support task lists, improving overall task management workflows.

## 2026-07-07 12:58

---
workHeadline: "docs(mdgbdf): Enhance MDGBDF with ad hoc attributes for AI-friendly task management; refactor dtask pop to top; improve docs"
---

This update primarily refines the Markdown-driven Great Big Data Format (MDGBDF) specification, notably in `docs/dev/spec/mdgbdata-spec.md`, by introducing support for "ad hoc attributes" in story and task headers. This enhancement, detailed further in the new `script-ai-friendly-texts.md` proposal, aims to make text conventions more AI-friendly and streamline task management. Corresponding `TODO.md` and `do.md` entries reflect these changes, including a rework of `dtask`'s `pop` subcommand to `top` with new options for integrating stories and tasks. Additionally, new documentation directories (`docs/dev/spec/adr/proposals` and `docs/dev/spec/obsolete`) are introduced for better organization of architectural decision records and obsolete specifications.

## 2026-07-06 07:39

---
workHeadline: "Improve story/task ID generation and preservation in mdgbdata, update spec and tests"
---

The diff primarily focuses on enhancing ID generation and preservation for stories and tasks within `mdgbdata.py`. New helper functions, `_make_story_id` and `_make_task_id`, were introduced to ensure that explicit IDs are retained during markdown parsing and to generate stable, deterministic IDs when none are provided. The `mdgbdata-spec.md` was updated to document these new ID generation rules, emphasizing the UUIDv7 and hash8 format and the handling of unnamed items. Corresponding tests in `test_mdgbdata.py` were extended to validate the format of these newly generated story IDs. A minor clarification was also made in the `backlog.py` help message.
