---
"actualCommitMessage": "feat: Introduce DDF spec, enhance `mdgbdata` with tasklist\
  \ support and formal attribute parsing rules"
"description": "A list of small, focused tasks guiding the current commit with detailed\
  \ microsected activities."
"intendedCommitMessage": "implement dtask pop subcommand"
"priorCommit": "32341444081849db3d0e713686fcf82468281ce8"
"title": "do.md"
"workBranch": "dtask-pop"
---


x - avoid anonymous-story as an id
 - assure that Story objects always have IDS that exist for their life time.
 x - update the spec
 x - prompt: update mdgbdata.py and tests to conform with the update in the '### ID Generation' section of docs/dev/spec/mdgbdata-spec.md.


# d - Story: backlog and mdgbdata support tasks lists
backlog.py and mdgbdata.py should support lists of tasks that are not wrapped in Stories.   This will simplify the vision for the backlog prioritized and backlog top command.   Pop will be deprecated because it implies that the thing that is popped would be removed from the list.  Top is just a listing command.  removing (by pop) causes the backlog to not show tasks that are in progress

The need for this rethinking comes from the situation where 

## stages of work to implement:
d - spec support reading informal mark down attributes
    d - generate it 
    d - check it out with test it with tojson

d - support writing attributes in formal markdown as YAML
    - per '#### MDGBDF Front-matter for Section, Story, or Task'
    in docs/dev/spec/mdgbdata-spec.md

d - verify / support reading the form frontmatter

d - rework mdgbdata.py to put the story title and story ID as attributes under the task
    - which is pretty useful if I pop just a task task into do.md. 
    - which might be needed to integrate with taskwarrior.

 prompt: update mdgbdata.py to support new features of the spec , especially in sections
  - to populate attribs in the domain model:'### Ad hoc attributes'
  - to add the story attribute when serializing for task listing: '### Module Requirements' and '#### Task Lists'     


# Work Summary

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

The diff primarily focuses on enhancing ID generation and preservation for stories and tasks within `mdgbdata.py`. New helper functions, `_make_story_id` and `_make_task_id`, were introduced to ensure that explicit IDs are retained during markdown parsing and to generatestable, deterministic IDs when none are provided. The `mdgbdata-spec.md` was updated to document these new ID generation rules, emphasizing the UUIDv7 and hash8 format and the handling of unnamed items. Corresponding tests in `test_mdgbdata.py` were extended to validate the format of these newly generated story IDs. A minor clarification was also made in the `backlog.py` help message.
