---
"actualCommitMessage": "feat(dtask): Relocate story for `pop` subcommand from TODO.md\
  \ to do.md, formalize spec"
"description": "A list of small, focused tasks guiding the current commit with detailed\
  \ microsected activities."
"intendedCommitMessage": "implement dtask pop subcommand"
"priorCommit": "32341444081849db3d0e713686fcf82468281ce8"
"title": "do.md"
"workBranch": "dtask-pop"
---



# Current work

# / - story: dtask integration with backlog.py
/ - early version of dtask pop which does not remove content from the backlog
    d - update dtask with a pop subcommand that reads 1 story by default from backlog.py and inserts it at the top of do.md, below the front-matter.
    - refer to the plugin api in docs/dev/spec/backlog-spec.md 
        / - update the spec docs/dev/spec/dtask-spec.md
         - [dtask spec](../spec//dtask-spec.md#pop-subcommand)
        / - update the program.


d - add a '--number (-n) n' option to take more than 1 Story or task object.  
 - possibly don't do this

d - add a --task option to `dtask pop` to just 1 task instead of a whole story.
 - possibly don't do this
 ### analysis
 popping a single task creates focus, whereas seeing the whole story lends context and helps avoid overlap in the way things are written.
 ### judgement 
 favor popping the whole story.  Allow the focus to come via the act of marking a single task as in progress '/', and likely adding prompts or elaboration

## limitations and assumptions 
Data in the TODO.md that is not part of a Task or Story will may be lost subject to the progress on support for DDF, todo.md, linking back to backlogs, and placeholders in the backlog.
 - this assumption avoids the need to build document preserving functionality in what I am calling for the future Dev Description Format (DDF). docs/dev/spec/adr/dev-description-format.md
 - This simplifying assumption avoids the situation where users would see the same object in two files with possibly different state.
 - Take together with the previous assumption, it means state for the TODO list can be manipulated as objects in memory and written back to the TODO.md file in new state.   


# / - story: mdgbdata.py or bltodo.py should only return work stories 
 - presently, stories tagged with the string "story:" are not considered work stories if they do not have a status or tasks. 
    - need to reverse this decision, but make sure text stories do not get flagged as 'story:'
        - do it by adding a status if the story marker is present.
x - update the spec withe respect to the rules for round trip handling of the story marker.
x - update the program
prompt: update mdgbdata.py per the updated spec docs/dev/spec/mdgbdata-spec.md, particularly to treat headings with the story marker as work stories.
x - implement an flag so bltodo can ask for only work stories
    - the logic for identifying work stories should stay encapsulated in mdgbdata.py
    - bltodo.py will use the flag to filter stories, for popstory
    - later when bltodo.py will update a story, it should be done by ID so that the distinction of being a work story does not matter.
    x - update the spec docs/dev/spec/mdgbdata-spec.md
    x - update the program mdgbdata.py per the updated spec docs/dev/spec/mdgbdata-spec.md
    x - update the program mdgbdata.py per the updated spec docs/dev/spec/mdgbdata-spec.md for the new 'Command line Requirements' to support the new --work subcommand
    x - update the docs/dev/spec/mdgbdata-spec.md to require that the help subcommand shows all subcommand and subcommand options.
    x - per the updated spec docs/dev/spec/mdgbdata-spec.md for the new 'Command line Requirements' update the help subcommand behavior
d - update use case documentation per comment in the google doc version of the spec.
d - update help text in bltodo.py
 - bltodo.py has knowledge of work queue management and is closer to the user, whereas mdgbdata.py is just a parser / serializer.
    - Text in the TODO file will be ignored doe heading sections that do not represnt work stories. 
 - users would interact with mdgbdata.py rarely if ever.  

# Completed work

x - update the gbdata Story object to allow status to be None.
 - A Section is simply a story with no status or tasks. 
 - update gbdata.py to allow status to be None in Story.

x - update the DDF specs to eliminate Section objects mentions in favor of informational stories.
 - docs/dev/spec/adr/script-ai-friendly-texts-development-description-format.md
 - docs/dev/spec/usecases/development-description-format-uses.md

x - update docs/dev/spec/mdgbdata-spec.md to support DDF according to updates and new source specifications mentioned under '### Sources'

x - ask AI for an audit to:
prompt: update the docs/dev/spec/mdgbdata-spec.md to assure that it is sufficient as a free standing document to update mdgbdata.py and tests without having to read source documents. 

x - update mdgbdata.py to support full DDF per updated docs/dev/spec/mdgbdata-spec.md  

x - update the gbdata model property name "attribs" to "attributes"

x - review the AI output from generating mdgbdata.py
 - is 'id' part of the front-matter, or a separate thing when writing md?
 - remove support for legacy  attribs.  The requirement has been removed from the spec. 

x - regenerate mdgbdata.py per the spec docs/dev/spec/mdgbdata-spec.md, and update tests.
prompt2: re-read the docs/dev/spec/mdgbdata-spec.md to set the file-scope story name according to the example and get rid of the extra quoting level when keys are quoted YAML and stored story attributes.

x - update spec and code so that front-matter is not stripped out of sections that are not stories.

x - do some manual testing of mdgbdata.py

x - mdgbdata.py - fix excessive quoting of front-matter is that is keeping quotes in the key names and values  read from markdown . Use the same YAML library as the dtask script. Update spec program and tests.
 - though marked as complet, there are still some issies with multiline frontmatter being separated.   For now, TODO.md does not support multi line front-matter
 
x - mdgbdata.py Use "file-{the input file name}" instead of "(file)" when naming a file scope story.  Update spec program and tests.

x - mdgbdata.py add blank lines between tasks in serialized output for cleaner viewing.
 x - update the spec.
 x - update the program.
 prompt: update mdgbdata.py to conform to the new additions to the spec docs/dev/spec/mdgbdata-spec2.md at lines 520 to 524.

## x - story: support story attributes in tasks
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

# - avoid 'anonymous-story' as an id
 - assure that Story objects always have IDS that exist for their life time.
 x - update the spec
 x - prompt: update mdgbdata.py and tests to conform with the update in the '### ID Generation' section of docs/dev/spec/mdgbdata-spec.md.


# Work Summary

## 2026-07-29 15:53

---
workHeadline: "feat(dtask): Relocate story for `pop` subcommand from TODO.md to do.md, formalize spec"
---

This change adds documentation for the `dtask pop` subcommand. The story for `dtask pop`, previously outlined in `TODO.md`, has been moved to `do.md`as "/ - story: dtask integration with backlog.py." The `dtask-spec.md` file was updated to formally define the `pop` subcommand's behavior, including how it integrates with `backlog.py` and handles the `do.md` file. This move prepares the `dtask pop` feature for implementation by placing its work details in `do.md` and codifying its specification.

## 2026-07-29 15:10

---
workHeadline: "feat(mdgbdata, bltodo): Add --work option to filter active stories; improve CLI help & update tests/docs"
---

This change introduces a `--work` option to the `mdgbdata` tool, allowing users to filter story lists to include only "work stories"—those with an assigned status or associated tasks. This filtering capability has been integrated into `mdgbdata.py`'s parsing and conversion functions, as well as the `bltodo.py` script's `pop_story` function to ensure only active work items are prioritized. Additionally, the CLI's help output has been significantly enhanced to provide a more comprehensive overview of all subcommands and their options, improving discoverability for this new feature. Corresponding tests were added in `test_bltodo.py` and `test_mdgbdata.py` to validate the new filtering logic and the updated help command, and the `mdgbdata-spec.md` documentation was updated to reflect these changes.


## 2026-07-29 13:13

---
workHeadline: "Feat(mdgbdata): Enhance markdown parsing for 'Story:' markers, improve output format, consolidate docs, and add tests"
---

The `mdgbdata.py` script was updated to enhance its markdown parsing by recognizing explicit "Story:" markers in headings, automatically assigning a 'do' status, and ensuring these are correctly serialized. The script's markdown output now includes blank lines between tasks and two blank lines between stories for improved readability. Accompanying these code changes, older, fragmented specification documents for `mdgbdata.py` were replaced with a single, consolidated `mdgbdata-spec.md`, which details the new parsing and serialization rules. Documentation in `backlog-spec.md`, `TODO.md`, and `do.md` was updated to clarify pending work related to `dtask` and `bltodo.py` integration. New unit tests were added to confirm the correct implementation of the story marker logic and the new serialization formatting.

## 2026-07-28 17:09

---
workHeadline: "feat(mdgbdata): Enhance stdin/stdout/file processing; refine markdown serialization, parsing & round-trip conversion"
---

This update significantly refines `bin/mdgbdata.py` to enable command-line `tojson` and `tomd` operations via standard input and output, alongside file-based processing. The changes introduce a more nuanced markdown serialization of story headers, distinguishing between work and informational stories, and allow the suppression of story headers for "file-input" stories to accommodate document-level frontmatter. Parsing logic now correctly processes file-scope frontmatter and promotes headings to stories when associated tasks are present, ensuring a more robust round-trip conversion of Markdown GB Data Form documents. Comprehensive updates to the `mdgbdata-spec2.md` documentation and relevant tests validate these new behaviors.
## 2026-07-28 14:16

---
workHeadline: "Refine mdgbdata specs: restructure, update mdgbdata-spec2 with parsing rules, and enhance docs/dev/work/README.md and TODO.md"
---

This update significantly refactors the `mdgbdata` specification by deleting the old `mdgbdata-spec.md` and moving its content, along with a previous version of `mdgbdata-spec2.md`, to an `obsolete` directory. The primary specification, `mdgbdata-spec2.md`, has been updated with detailed terminology and explicit rules for parsing and serializing object properties and attributes, particularly focusing on YAML front-matter and informal key-value notation. Additionally, the `docs/dev/work/README.md` file now includes descriptions for `TODO.md` and `do.md`, while the `TODO.md` file itself had its front-matter removed, reflecting adjustments to document structure.
## 2026-07-28 14:11

---
workHeadline: "Refactor mdgbdata for robust story/task parsing, generic type-safe status map, story maxTasks, update backlog/bltodo and tests"
---

The `mdgbdata.py` module underwent a significant refactoring to enhance the parsing and serialization of story and task data from Markdown. The `load_status_map` function was updated to be more generic, accepting specific status enum types (`StoryStatus` or `TaskStatus`), thereby improving type safety. This change involved new helper functions for coercing and distinguishing formal properties like `id`, `status`, `name`, `description`, `detail`, and a newly added `maxTasks` for stories, from general attributes in both YAML frontmatter and informal attribute lines. Corresponding adjustments were made in `backlog.py` and `bltodo.py` to align with the new function signature, and comprehensive unit tests were added and modified in `test_mdgbdata.py` to validate these robust parsing and serialization behaviors.

## 2026-07-16 20:35

---
workHeadline: "Feat(mdgbdata): Preserve leading prose & malformed YAML in markdown parsing; update spec & tests"
---

This update to the `mdgbdata.py` script and its documentation significantly enhances its robustness in handling markdown input. Previously, the parser would warn and ignore leading prose or malformed YAML frontmatter blocks; now, these elements are gracefully preserved as part of the story or task description. This change ensures no content is lost during markdown-to-JSON conversion. Corresponding updates were made to `mdgbdata-spec.md` to reflect this new preservation behavior and clarify task header detection, while tests were modified to assert the content preservation and remove checks for the deprecated warning message.
## 2026-07-15 17:55

---
workHeadline: "feat(mdgbdata): Adopt PyYAML for robust Markdown frontmatter, formalize `id` & attributes, update spec & tests"
---

This update significantly overhauls `bin/mdgbdata.py` to adopt `PyYAML` for parsing and serializing story and task frontmatter, enabling more robust handling of `id` properties and ad-hoc attributes directly within Markdown. The previous custom `id:` line parsing logic has been replaced, and attributes are now treated as formal YAML properties, which allows for advanced features like quoted keys and type preservation. Accompanying changes in `docs/dev/spec/mdgbdata-spec.md` formalize these new YAML-based rules, clarify file-scope story naming conventions, and refine story heading detection. Extensive updates and additions to the test suite ensure the correct parsing and serialization of the new frontmatter structure, confirming data integrity and round-trip functionality.
## 2026-07-13 11:45

---
workHeadline: "refactor: Allow Story.status to be None to allow for usage of the Story object to hold markdown DDF H1 sections"
---

Update spec, gbdata.py and tests per headline.


## 2026-07-12 11:50

---
workHeadline: "refactor: Rename Task.attribs to Task.attributes across codebase, updating parsing, serialization, docs, and tests for consistency"
---

The primary change in this diff is the renaming of the `attribs` field to `attributes` within the `Task` dataclass in `bin/gbdata.py` and `bin/mdgbdata.py`, affecting how ad-hoc task properties are stored and processed. This modification is propagated throughout the codebase, including updates to the parsing logic in `_parse_front-matter_block` and `parse_stories_from_markdown`, and serialization functions like `_task_to_dict` and `_render_markdown_story` in `bin/mdgbdata.py`. Supporting documentation in `docs/dev/spec/gbdata-spec-2.md`, `docs/dev/spec/mdgbdata-spec.md`, and `docs/dev/spec/usecases/story-task-parsing-md.md` has been updated to reflect this new field name and its implications for user-defined attributes. Corresponding unit tests in `tests/test_gbdata.py` and `tests/test_mdgbdata.py` were also adjusted to validate the `attributes` field's default behavior, parsing, and serialization, ensuring consistency across the application. Additionally, minor updates were made to `docs/dev/spec/usecases/README.md`, `docs/dev/work/TODO.md`, and `docs/dev/work/do.md` to refine descriptions and reflect progress on related work items.

## 2026-07-11 10:52

---
workHeadline: "feat: Implement ad-hoc task attributes in `mdgbdata.py` with Markdown front-matter support, parsing, serialization, and tests"
---

The `mdgbdata.py` script has been significantly enhanced to support ad-hoc attributes for tasks, allowing users to define custom `key: value` pairs directly within Markdown. This update introduces parsing logic for both single-line attributes and multi-line front-matter blocks delimited by `---`, integrating these new properties into the `Task.attribs` field. Furthermore, the script now serializes these attributes back into Markdown as YAML front-matter and includes them in the JSON representation of stories and tasks. The `mdgbdata-spec.md` document was updated to formally describe these new parsing and serialization rules, while `test_mdgbdata.py` now includes comprehensive tests to ensure correct behavior and data round-tripping for the ad-hoc task attributes.
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
workHeadline: "feat: Introduce DDF spec, enhance `mdgbdata` with task list support and formal attribute parsing rules"
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
