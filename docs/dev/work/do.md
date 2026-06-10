---
"actualCommitMessage": "feat: Enhance gbdata.py per code-ready spec with markdown parsing for Stories/Tasks, add status support, comprehensive tests, and update docs"
"description": "A list of small, focused tasks guiding the current commit with detailed\
  \ microsected activities."
"intendedCommitMessage": "feat: Enhance gbdata.py with markdown parsing for Stories/Tasks, add status support, comprehensive tests, and update docs"
"priorCommit": "ebf5d03cc27857091ac879530af2d1a478de8e69"
"title": "do.md"
"workBranch": "gbdata-module"
---


# / story: Pilot a filesystem integration with TODO.md as a task store to start backlog and exercise interaction needed with do.md.
x - Update gb-data to include a status in the story type.
x - do docs/dev/spec/gbdata-spec.md to generate docs/dev/spec/code-ready/gbdata-spec-ready.md.

x - include story parsing metadata in this project from enhance gb-data json schema
	x - do some egrep play to parse stories

x - build a python domain model using json schema from GB
 - bin/gbdata.py
 - try it out with subsequent tasks
 x - enhance the model to include Story metadata similar to https://github.com/psons/gb-data/blob/main/task_status_metadata.json 
x - write a spec for story file parsing.
 - docs/dev/spec/usecases/story-task-parsing-md.md
 - reference from docs/dev/spec/gbdata-spec.md 
 x - include improvements in docs/dev/spec/gbdata-spec.md to generate a docs/dev/spec/code-ready/gbdata-spec-ready.md per the README.md there 

 x - task: prompt: generate code-ready/gbdata-spec-ready.md according to docs/dev/spec/gbdata-spec.md 
 x - review the code-ready spec
    x - make required corrections:
        x - push update the schema at github to include status in Story.
        x - clarify spec so that it will support all 6 H levels for stories.



# Work Summary

## 2026-06-10 16:20

---
workHeadline: "feat: Enhance gbdata.py with markdown parsing for Stories/Tasks, add status support, comprehensive tests, and update docs"
---

The `bin/gbdata.py` module was significantly enhanced to include robust markdown parsing capabilities for extracting `Story` and `Task` objects. This involved adding new functions to load and compile status metadata from JSON, detect and strip status prefixes, and a core `parse_stories_from_markdown` function to interpret markdown headings and task lists into structured data. The `Story` dataclass was updated with an optional status field to support this new parsing logic. A comprehensive new test suite, `tests/test_gbdata.py`, was added to validate all aspects of the new markdown parsing, ensuring correct identification of stories, tasks, statuses, and details across various markdown structures. The project's development documentation in `docs/dev/work/TODO.md` and `docs/dev/work/do.md` was updated to reflect the completion of these parsing enhancements and to outline the next steps for a backlog tool that will utilize this new functionality.

## 2026-06-09 16:52

---
workHeadline: "feat(gbdata): Introduce code-ready spec workflow for `gbdata.py` with domain model, status, and markdown parsing"
---

This update introduces a new structured specification workflow for the `bin/gbdata.py` module, shifting its implementation source to the newly created `docs/dev/spec/code-ready/gbdata-spec-ready.md`. This detailed, code-ready specification now defines the Python domain model for `gbdata`, including `Task` and `Story` objects, along with comprehensive requirements for loading status metadata from dedicated JSON files and parsing markdown content to extract stories and tasks. The original `docs/dev/spec/gbdata-spec.md` was updated to reflect this new documentation hierarchy and task execution flow, while `docs/dev/spec/usecases/story-task-parsing-md.md` provides the behavioral rules for the markdown parser.
## 2026-06-05 16:46

---
workHeadline: "feat: Add `bin/gbdata.py` with Goal Blotter data models for `Task`, `Story`, `Goal`, and `TimePriorityBlock`"
---

This change introduces the `bin/gbdata.py` module, which defines Python data model types for a Goal Blotter hierarchy, including `TaskStatus`, `Task`, `Story`, `Goal`, and `TimePriorityBlock`. These types are designed to model a structured work breakdown for goal management. The module's creation is documented and specified in `docs/dev/spec/gbdata-spec.md`, which explicitly references an external JSON schema for the data model. Additionally, a `do.md` entry reflects the task of generating this specification.
