---
"actualCommitMessage": "feat(gbdata): Introduce code-ready spec workflow for `gbdata.py`\
  \ with domain model, status, and markdown parsing"
"description": "A list of small, focused tasks guiding the current commit with detailed\
  \ microsected activities."
"intendedCommitMessage": "spec to generate model module for backlog.py"
"priorCommit": "ebf5d03cc27857091ac879530af2d1a478de8e69"
"title": "do.md"
"workBranch": "gbdata-module"
---


# / story: Pilot a filesystem integration with TODO.md as a task store to start backlog and exercice interaction needed with do.md.
x - Update gb-data to include a status in the story type.
/ - do docs/dev/spec/gbdata-spec.md to generate docs/dev/spec/code-ready/gbdata-spec-ready.md.

/ - include story parsing metadata in this project from enhance gb-data json schema
	x - do some egrep play to parse stories

/ - build a python domain model using json schema from GB
 - bin/gbdata.py
 - try it out with subsequent tasks
 / - enhance the model to include Story metadata similar to https://github.com/psons/gb-data/blob/main/task_status_metadata.json 
/ - write a spec for story file parsing.
 - docs/dev/spec/usecases/story-task-parsing-md.md
 - reference from docs/dev/spec/gbdata-spec.md 
 / - include improvements in docs/dev/spec/gbdata-spec.md to generate a docs/dev/spec/code-ready/gbdata-spec-ready.md per te REAME.md there 

 d - task: prompt: generate code-ready/gbdata-spec-ready.md according to docs/dev/spec/gbdata-spec.md 
 d - review the code-ready spec
    d - make required coprrections:
        d - push update the schema at githib to include status in Story.
        d - clarify spec so that it will support all 6 H levels for stories.



# Work Summary


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
