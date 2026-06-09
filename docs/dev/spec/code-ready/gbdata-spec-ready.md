# gbdata.py Code-Ready Specification

## Purpose
This document is the implementation source of truth for `bin/gbdata.py` in this repository.

`bin/gbdata.py` must be generated from this document after review. It must not be generated directly from `docs/dev/spec/gbdata-spec.md`.

The module must:
- Provide Python data-model types matching the Goal Blotter hierarchy described in gb-data (`Task`, `Story`, `Goal`, `TimePriorityBlock`, and `WorkHierarchy`).
- Provide status metadata loading and status detection utilities using the metadata files in this repository.
- Provide markdown parsing that builds `Story` objects containing `Task` objects, following `docs/dev/spec/usecases/story-task-parsing-md.md`.

## Inputs and Dependencies

### Local Files Used at Runtime
- `docs/dev/spec/code-ready/story_status_metadata.json`
- `docs/dev/spec/code-ready/task_status_metadata.json`

### Python Version and Libraries
- Target Python: 3.11+
- Standard library only.
- Required stdlib modules include: `dataclasses`, `enum`, `typing`, `pathlib`, `json`, `re`, `hashlib`.

No third-party package dependencies are required for `bin/gbdata.py`.

## Domain Model Requirements

### Enum and Metadata Types
Implement:

1. `TaskStatus(str, Enum)` with exact members and values:
   - `ABANDONED = "abandoned"`
   - `COMPLETED = "completed"`
   - `SCHEDULED = "scheduled"`
   - `IN_PROGRESS = "in_progress"`
   - `UNFINISHED = "unfinished"`
   - `DO = "do"`

2. `StatusEntry` dataclass:
   - `val: str`
   - `pat_str: str`

3. `StatusMap` type alias:
   - `dict[TaskStatus, StatusEntry]`

### Work Hierarchy Types
Implement dataclasses with `frozen=True` and `slots=True`:

1. `Task`
   - `id: str`
   - `name: str`
   - `status: TaskStatus | None = None`
   - `detail: str | None = None`

2. `Story`
   - `id: str`
   - `name: str`
   - `status: TaskStatus | None = None`
   - `maxTasks: int | None = None`
   - `tasks: list[Task] | None = None`

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

## Status Metadata Behavior

### Metadata File Contract
Both status metadata JSON files are object maps keyed by status name matching `TaskStatus` values. Each value object contains:
- `val`: a single-character shorthand code
- `pat_str`: regex string used to match a status-prefixed line

Current expected values in both files:
- `abandoned`: `val="a"`, `pat_str="^[aA] *-"`
- `completed`: `val="x"`, `pat_str="^[xX] *-"`
- `scheduled`: `val="s"`, `pat_str="^[sS] *-"`
- `in_progress`: `val="/"`, `pat_str="^[\\/\\\\] *-"`
- `unfinished`: `val="u"`, `pat_str="^[uU] *-"`
- `do`: `val="d"`, `pat_str="^[dD] *-"`

### Required Functions
Implement utility functions:

1. `load_status_map(path: str | Path) -> StatusMap`
   - Reads JSON.
   - Validates all keys map to `TaskStatus`.
   - Validates each entry has non-empty `val` and `pat_str`.
   - Returns `StatusMap` keyed by enum members.
   - Raises `ValueError` for invalid schema/content; propagates `FileNotFoundError`.

2. `compile_status_patterns(status_map: StatusMap) -> dict[TaskStatus, re.Pattern[str]]`
   - Compiles each `pat_str`.
   - Raises `ValueError` with status key context for invalid regex.

3. `detect_status(line: str, compiled_patterns: dict[TaskStatus, re.Pattern[str]]) -> TaskStatus | None`
   - Returns first matching status in deterministic enum order.
   - Returns `None` if no pattern matches.

4. `strip_status_prefix(line: str, status: TaskStatus, compiled_patterns: dict[TaskStatus, re.Pattern[str]]) -> str`
   - Removes only the matched leading status marker and the `-` prefix token.
   - Trims leading/trailing whitespace of remaining headline.

## Markdown Parsing Requirements

### Scope
`gbdata.py` must include a parser focused on producing story/task structures from markdown content.

Required entry points:

1. `parse_stories_from_markdown(text: str, story_status_map: StatusMap, task_status_map: StatusMap) -> list[Story]`
2. `parse_stories_from_markdown_file(path: str | Path, story_status_map: StatusMap, task_status_map: StatusMap, encoding: str = "utf-8") -> list[Story]`

The file variant reads text then delegates to the text variant.

### Markdown Interpretation Rules
Follow these rules from `story-task-parsing-md.md`.

#### Story Header Detection
A line starts a new story when any of these are true:

1. It is a markdown heading at level 1 through 6 and matches a story status pattern after heading markers.
2. It is a markdown heading at level 1 through 6 and contains tasks below it (non-pattern matched stories are still stories).
3. It is a markdown heading at level 1 through 6 whose heading text starts with `Story:` (case-insensitive, with optional surrounding whitespace).

Interpretation details:
- Heading marker must be at left margin to be considered a heading (`^#{1,6}\\s+`).
- Stories cannot nest. A heading deeper than current story level is part of description context, not a new story.
- A heading at the same or shallower level than current story closes the current story scope and may start another story.

#### Story Name and Story Status
For status-pattern stories:
- Evaluate status patterns against heading text content (after removing `#` markers and leading spaces).
- If matched, set and persist `Story.status` on the output dataclass.
- Story `name` is heading content with status prefix removed.

For non-pattern stories:
- `name` is normalized heading text (trimmed; preserve internal spacing).
- If no status pattern is detected, default `status` to `TaskStatus.DO`.
- This includes the corner case where a heading is promoted to a story only because it contains task lines.

#### Task Header Detection
A line starts a new task when all are true:

1. Line is at left margin (no leading spaces or tabs).
2. Line matches one of the task status patterns.
3. Parser is currently within an active story scope.

Non-task-like indented lines must be treated as detail text, never as a task header.

#### Task Name, Status, and Detail
- `status` is detected via task status pattern match.
- `name` is the task line with status prefix removed.
- `detail` is all subsequent lines until one of:
  - a new task header,
  - a new story boundary,
  - a heading at same or higher level than current story.
- Preserve newlines in detail text; trim outer blank lines.

#### Story Description Handling
- Lines after a story header that are not task headers and not a closing heading boundary are story description context.
- Since `Story` has no `description` field, story description is not serialized into dataclass output.
- Story description still contributes to detecting boundaries and preventing false story/task starts.

### Bare Task Behavior
Per use-case text, bare tasks can exist without explicit story context, but parser output must be `list[Story]`.

Implement this rule:
- Prefer explicit unnamed markdown headings (`#`, `##`, `###`, `####`, `#####`, `######`) as normal story containers when present.
- If task headers appear before any active story, auto-create a synthetic story named `"Unscoped"` with deterministic id and attach those tasks.
- The synthetic `"Unscoped"` story must use default status `TaskStatus.DO`.
- Synthetic story must be first in output if encountered before first real story.

### Heading Boundary Rules
When inside a story with heading level `L`:
- Heading level `> L`: treated as inner content context; does not close story.
- Heading level `<= L`: closes current story and all active task/detail accumulation.

### ID Generation
IDs are required fields for `Task` and `Story`.

Use deterministic, stable IDs based on source order and text:
- Story id format: `story-{index}-{hash8}`
- Task id format: `task-{story_index}-{task_index}-{hash8}`

Where:
- `index` and `task_index` are 1-based order in parse result.
- `hash8` is first 8 hex chars of SHA-1 of normalized name text.

Normalization for hash input:
- Strip outer whitespace.
- Collapse internal whitespace runs to a single space.
- Keep case as-is.

## API Surface

`bin/gbdata.py` must export the following names via `__all__`:
- `TaskStatus`
- `StatusEntry`
- `StatusMap`
- `Task`
- `Story`
- `Goal`
- `TimePriorityBlock`
- `WorkHierarchy`
- `load_status_map`
- `compile_status_patterns`
- `detect_status`
- `strip_status_prefix`
- `parse_stories_from_markdown`
- `parse_stories_from_markdown_file`

## Error Handling
- Invalid metadata key not in `TaskStatus`: raise `ValueError` naming invalid key.
- Invalid metadata entry object shape: raise `ValueError` naming key and missing field.
- Invalid regex in `pat_str`: raise `ValueError` naming key and regex compile error.
- File decode errors in markdown file parser: propagate `UnicodeDecodeError`.

Parser robustness rules:
- Never raise for unmatched lines; treat as descriptive text.
- Never raise for empty markdown; return empty list.
- Never create empty-named tasks. If stripping prefix yields empty task name, use `"(unnamed task)"`.
- Never create empty-named stories. If heading text becomes empty, use `"(unnamed story)"`.

## Implementation Notes
- Keep parsing algorithm single-pass over input lines (`O(n)`).
- Avoid recursive parser design; use explicit state variables:
  - current story object-in-progress
  - current task object-in-progress
  - current story heading level
  - per-story task list buffer
  - task detail line buffer
- Compile regex once per parse call.

## Test Requirements for `tests/`
At minimum, include tests for:

1. Metadata loading
   - valid JSON loads expected enum keys
   - invalid key raises `ValueError`
   - invalid entry shape raises `ValueError`

2. Status detection
   - each known pattern maps to expected status
   - unknown line returns `None`

3. Story parsing
   - status-matched heading creates story with stripped name
   - status-matched heading persists `Story.status`
   - non-pattern heading with tasks still creates story
   - non-pattern stories default `Story.status` to `TaskStatus.DO`
   - `Story:` heading creates story without tasks
   - nested heading does not create nested story
   - heading levels 1 through 6 are supported for story boundaries

4. Task parsing
   - left-margin task recognized
   - indented task-like line not recognized
   - task detail accumulation until boundary
   - task names/defaults for empty headline

5. Boundary behavior
   - same-level heading closes current story
   - higher-level heading closes current story
   - deeper heading does not close current story

6. Bare tasks
   - tasks before first heading go to synthetic `Unscoped` story

7. Deterministic IDs
   - same input yields same ids across parses
   - id format matches spec

## Non-Goals
- Parsing full markdown AST.
- Parsing `Goal` and `TimePriorityBlock` from markdown in this phase.
- Auto-mutating metadata JSON files.

## Acceptance Criteria
This spec is accepted when:

1. A generated `bin/gbdata.py` exposes all required types and functions with required signatures.
2. Data-model fields and enum values match the requirements in this document.
3. Markdown parsing behavior follows the use-case boundary and detection rules in this document.
4. Tests covering all required areas pass under `pytest`.
5. No third-party dependency is required for module operation.