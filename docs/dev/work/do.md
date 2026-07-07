---
"actualCommitMessage": "docs(mdgbdf): Enhance MDGBDF with ad hoc attributes for AI-friendly\
  \ task management; refactor dtask pop to top; improve docs"
"description": "A list of small, focused tasks guiding the current commit with detailed\
  \ microsected activities."
"intendedCommitMessage": "implement dtask pop subcommand"
"priorCommit": "32341444081849db3d0e713686fcf82468281ce8"
"title": "do.md"
"workBranch": "dtask-pop"
---


d - avoid anonymous-story as an id
 - assure that Story objects always have IDS that exist for their life time.
 x - update the spec
 x - prompt: update mdgbdata.py and tests to conform with the update in the '### ID Generation' section of docs/dev/spec/mdgbdata-spec.md.

d - rework `backlog prioritized` to put the story title and story ID as attributes under the task
    - which is pretty useful if I pop just a task task into do.md. 
    - which might be needed to integrate with taskwarrior.

 prompt: update mdgbdata.py to support new features of the spec , especially in sections
  - '### Ad hoc attributes'            

# Work Summary

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
