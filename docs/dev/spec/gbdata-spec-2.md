# gbdata.py Code-Ready Specification (Domain Model)

## Purpose
This document is the implementation source of truth for `bin/gbdata.py` in this repository.

`bin/gbdata.py` must be generated from this document after review.

The module must:
- Provide Python domain-model types matching the Goal Blotter hierarchy in the gb-data model (`Task`, `Story`, `Goal`, `TimePriorityBlock`, and `WorkHierarchy`).
- Provide status enum values for task and story objects.
- Avoid embedding markdown parsing behavior so model types can be imported by backlog providers and related modules as a unified contract.

## Model updates

Aligned with the gb-data schema at:
https://github.com/psons/gb-data/blob/main/goalBlotter.schema.json

Update applied:
- `Task.attribs` has been renamed to `Task.attributes`.
- `Story.status` is now optional (`None` allowed) to support informational stories.
- `Story.attributes` has been added for story-level integration metadata.


## Module Boundary
`gbdata.py` is the domain-model module.

Markdown parsing and status-pattern interpretation are specified separately in [docs/dev/spec/mdgbdata-spec.md](docs/dev/spec/mdgbdata-spec.md) and implemented in `bin/mdgbdata.py`.

## Inputs and Dependencies

### Python Version and Libraries
- Target Python: 3.11+
- Standard library only.
- Required stdlib modules include: `dataclasses`, `enum`, `typing`.

No third-party package dependencies are required for `bin/gbdata.py`.

## Domain Model Requirements

### Enum Types
Implement:

1. `TaskStatus(str, Enum)` with exact members and values:
   - `ABANDONED = "abandoned"`
   - `COMPLETED = "completed"`
   - `SCHEDULED = "scheduled"`
   - `IN_PROGRESS = "in_progress"`
   - `UNFINISHED = "unfinished"`
   - `DO = "do"`

2. `StoryStatus(str, Enum)` with exact members and values:
   - `ABANDONED = "abandoned"`
   - `COMPLETED = "completed"`
   - `SCHEDULED = "scheduled"`
   - `IN_PROGRESS = "in_progress"`
   - `UNFINISHED = "unfinished"`
   - `DO = "do"`

### Work Hierarchy Types
Implement dataclasses with `frozen=True` and `slots=True`:

1. `Task`
   - `id: str`
   - `status: TaskStatus`
   - `name: str`
   - `detail: str | None = None`
   - `attributes: dict[str, object] | None = None`

2. `Story`
   - `id: str`
   - `status: StoryStatus | None = None`
   - `name: str`
   - `description: str | None = None`
   - `maxTasks: int | None = None`
   - `tasks: list[Task] | None = None`
   - `attributes: dict[str, object] | None = None`

3. `Goal`
   - `id: str`
   - `name: str`
   - `description: str | None = None`
   - `maxStories: int | None = None`
   - `stories: list[Story] | None = None`

4. `TimePriorityBlock`
   - `id: str`
   - `name: str`
   - `sprintMax: int`
   - `goals: list[Goal] | None = None`

5. `WorkHierarchy` type alias:
   - `TimePriorityBlock`

## API Surface

`bin/gbdata.py` must export the following names via `__all__`:
- `TaskStatus`
- `StoryStatus`
- `Task`
- `Story`
- `Goal`
- `TimePriorityBlock`
- `WorkHierarchy`

## Error Handling
- Domain type definitions should not implement parser behavior or metadata file I/O.
- Errors related to markdown parsing or metadata pattern files are handled by `mdgbdata.py`.

## Implementation Notes
- Keep this module focused on shared model contracts.
- Keep this module import-light for broad reuse across provider modules.

## Test Requirements for `tests/`
At minimum, include tests for:

1. Enum and value stability
   - `TaskStatus` members and string values match this document exactly.
   - `StoryStatus` members and string values match this document exactly.

2. Dataclass structure and defaults
   - All fields exist with required defaults.
   - `Task.attributes` defaults to `None` and supports unknown-valued metadata.
   - `Story.attributes` defaults to `None` and supports unknown-valued metadata.

3. Serialization compatibility shape
   - Type instances can be constructed with schema-compatible field values.
   - `Task.status` is represented as non-optional in the model.
   - `Story.status` is optional and supports `None` for informational stories.

## Non-Goals
- Markdown parsing.
- Status metadata file loading.
- Regex pattern compilation or status detection from text lines.
- Markdown file read/write behavior.

## Acceptance Criteria
This spec is accepted when:

1. A generated `bin/gbdata.py` exposes all required model types with required signatures.
2. Enum values and dataclass fields match this document exactly.
3. The module has no markdown parsing logic.
4. Tests covering model definitions and defaults pass under `pytest`.
5. No third-party dependency is required for module operation.
