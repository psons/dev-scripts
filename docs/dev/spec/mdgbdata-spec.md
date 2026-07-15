# mdgbdata.py Code-Ready Specification (Markdown Parsing)

## Purpose

### Sources 
This document uses the following sources and is to be maintained as the single source of truth for implementation of `bin/mdgbdata.py` in this repository.:
 - [docs/dev/spec/usecases/story-task-parsing-md.md](./usecases/story-task-parsing-md.md)
 - [docs/dev/spec/usecases/development-description-format-uses.md](./usecases/development-description-format-uses.md)
 - [docs/dev/spec/adr/script-ai-friendly-texts-development-description-format.md](./adr/script-ai-friendly-texts-development-description-format.md)
 - [docs/dev/spec/gbdata-spec-2.md](./gbdata-spec-2.md)

Source files above are background context only. This document is normative and intentionally self-contained for implementation and test work.


### Output
`bin/mdgbdata.py` must be generated from this document.

`bin/mdgbdata.py` owns the implementation of MDGBDF parsing and serialization, and JSON parsing and serialization for the shared gb-data model.


### Module Requirements
The module must:
- Provide status metadata loading and status detection utilities using repository metadata files.
- Provide DDF markdown parsing that builds ordered `Story` objects containing optional `Task` objects.
- Provide DDF serialization that outputs markdown text from ordered `Story` objects and preserves non-task informational story content.
- Provide JSON parsing and serialization for the gb-data schema representation of those objects.
- Import domain classes from `bin/gbdata.py` so parsing output uses the shared gb-data model.

The format described in this document that will be read and written by `bin/mdgbdata.py`
will be referred to in other specifications as 'Markdown GB Data Form' (MDGBDF) or Development Description Format (DDF).

### Command line Requirements
Commandline support should be provided by `bin/mdgbdata.py`for the following sub commands:

    tojson 
        will read a file whose path is given as a command line argument and is presumed to be 'Markdown GB Data Form' and output JSON text representing a list of stories possibly containing tasks conforming to the schema https://github.com/psons/gb-data/blob/main/goalBlotter.schema.json

        if the input file is markdown and contains text that is not part of a story or task, a WARNING should be printed on stderr indicating that "some non story text will be ignored"

        If the input file does not contain any markdown headers or tasks, raise an error 

    tomd 
        will read a file whose path is given as a command line argument and is presumed to be json conforming to the schema https://github.com/psons/gb-data/blob/main/goalBlotter.schema.json and output 'Development Description Format (DDF)'

        if the input file is not valid json, raise an error.  

    help
        will print a command usage summary for all subcommands 


## Module Boundary
`mdgbdata.py` owns markdown/text parsing and serialization behavior for MDGBDF/DDF.

`gbdata.py` owns domain types and the shared status enum.

`mdgbdata.py` must import `TaskStatus`, `Task`, and `Story` from `gbdata.py` instead of redefining those types.

## Inputs and Dependencies

### Local Files Used at Runtime
- `docs/dev/spec/story_status_metadata.json`
- `docs/dev/spec/task_status_metadata.json`

### Python Version and Libraries
- Target Python: 3.11+
- Required libraries include: `PyYAML` (same library used by `bin/dtask`).
- Required stdlib modules include: `typing`, `pathlib`, `json`, `re`, `hashlib`.

`bin/mdgbdata.py` requires `PyYAML` for front-matter parsing and serialization.

## Metadata Types
Implement:

1. `StatusEntry` dataclass:
   - `val: str`
   - `pat_str: str`

2. `StatusMap` type alias:
   - `dict[TaskStatus, StatusEntry]`

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

### Standalone Contract
This section is sufficient to implement and test `bin/mdgbdata.py` without reading other documents.
If any rule here differs from referenced source documents, this file takes precedence for this repository.

### Scope
`mdgbdata.py` must include a parser focused on producing full DDF story/task structures from markdown content.

Required entry points:

1. `parse_stories_from_markdown(text: str, story_status_map: StatusMap, task_status_map: StatusMap) -> list[Story]`
2. `parse_stories_from_markdown_file(path: str | Path, story_status_map: StatusMap, task_status_map: StatusMap, encoding: str = "utf-8") -> list[Story]`

The file variant reads text then delegates to the text variant.

DDF parser/serializer scope must preserve whole-document information as an ordered list of stories:
- If content exists before the first H1 heading, it is represented as a file-scope informational `Story`.
- If no H1 headings exist, the whole file is represented as a single file-scope informational `Story`.
- Every H1 heading starts a new non-file-scope `Story`.
- Informational stories may have `status=None` and no tasks.

File-scope story naming:
- When parsing from a file path, the file-scope story Story.name must be the concatenation of:
    The string "file-"
    the basename including extension (directory removed).
- File-scope tasks and description text are attached to that file-scope story.
- If a file has no H1 headings, the single informational story must still use `file-{input file name}`.
- When parsing from raw text without a file path, implementations may use a stable placeholder file-scope name.

`mdgbdata.py` must include a parser to load and validate json text to produce story/task structures.

### JSON Mapping Contract
JSON serialization and parsing must use the following field mapping:
- Story required fields: `id`, `name`
- Story optional fields: `status`, `description`, `maxTasks`, `tasks`, `attributes`
- Task required fields: `id`, `status`, `name`
- Task optional fields: `detail`, `attributes`

Validation rules:
- When present, `Story.status` and `Task.status` must be enum-compatible status strings.
- When present, `Story.attributes` and `Task.attributes` must be JSON objects.
- When present, `Story.tasks` must be an array of task objects.


### Markdown Interpretation Rules
All markdown behavior required for implementation is specified below.

#### Story Header Detection
A line starts a new story when any of these are true:

1. It is a markdown heading at level 1 and matches a story status pattern after heading markers.
2. It is a markdown heading at level 1 and contains tasks below it (non-pattern matched headings are still stories if they contain tasks).
3. It is a markdown heading at level 1 whose heading text starts with `Story:` (case-insensitive, with optional surrounding whitespace).

For full DDF document boundaries, every H1 heading (`^# `) must start a new `Story` even when no status pattern or tasks are present.

Interpretation details:
- Heading marker must be at left margin to be considered a heading (`^#{1,6}\\s+`).
- Stories cannot nest. A heading deeper than current story level is part of description context, not a new story.
- A heading at the same or shallower level than current story closes the current story scope and may start another story.

#### Story Name and Story Status
For status-pattern stories:
- Evaluate status patterns against heading text content (after removing `#` markers and leading spaces).
- If matched, set and persist `Story.status` on the model dataclass.
- Story `name` is heading content with status prefix and `Story:` string removed.

For non-pattern stories:
- `name` is normalized heading text (trimmed; preserve internal spacing).
- If no status pattern is detected and tasks are present in the story, default `status` to `TaskStatus.DO`.
- If no status pattern is detected and no tasks are present, `status` must remain `None`.
- This includes the corner case where a heading is promoted to a story only because it contains task lines.

Story-level ad hoc metadata must be supported:
- Any attribute key not mapped to an explicit `Story` field is stored in `Story.attributes`.
- Story attributes follow the same informal `key: value` and formal front-matter parsing rules used for task attributes, scoped to the current story.

When serializing stories to MDGBDF:
- Use heading level 1 for each serialized story.
- If `Story.status is None` or `Story.status == StoryStatus.DO`, write header as:
   `# Story: <name>`
- Otherwise write header as:
   `# <status_val> - Story: <name>`
   where `<status_val>` is the `val` shorthand from story status metadata.

#### Story Description
- `description` is all lines excluding section front-matter after the story header that are not part of a task, until one of:
  - a new story boundary,
- Preserve newlines in description text; trim outer blank lines.
- Parsed markdown stories default `attributes` to `None` if no Ad hoc attributes are found.

#### Task Header Detection
A line starts a new task when all are true:

1. Line is at left margin (no leading spaces or tabs).
2. Line matches one of the task status patterns.
3. Parser is currently within an active story scope, or within an H1-H6 heading scope that must be promoted to a story per Story Header Detection item 2.

If a task-status line is encountered under an H1-H6 heading that has not yet been materialized as a story, that heading must first be promoted to a `Story` (default `TaskStatus.DO` for non-pattern headings), and the line must then be treated as a task header within that story.

Non-task-like indented lines must be treated as detail text, never as a task header.

#### Task Name, Status, and Detail
- `status` is detected via task status pattern match.
- `name` is the task line with status prefix removed.
- `detail` is all subsequent lines excluding section front-matter, until one of:
  - a new task header,
  - a new story boundary,
  - a heading at same or higher level than current story.
- Preserve newlines in detail text; trim outer blank lines.
- Parsed markdown tasks default `attributes` to `None` if no Ad hoc attributes are found.

#### Formal `id` Model Property
- `id` is a formal schema property of both `Story` and `Task` in Python objects and must map to `Story.id` and `Task.id`, not to `attributes`.
- In markdown front-matter, `id` must be parsed and serialized using the same YAML property handling as other recognized properties.
- `id` handling must not depend on positional, non-YAML line parsing rules.
- When `id` is not provided through parsed data, deterministic id generation rules still apply.

#### Ad hoc Attributes
Users can add ad hoc attributes to tasks without changing the core schema.

- Any attribute key that is not an explicitly supported property of the `Task` object must be stored in `Task.attributes`.
- Informal Markdown input must support a single-line `key: value` form.
- An attribute line is recognized when non-whitespace text begins at the left margin and is followed by a colon.
- The attribute value is the text after the colon up to the end of the line.
- Attributes may appear anywhere after the relevant task header line within the task scope.

Users can add ad hoc attributes to stories without changing the core schema.

- Any attribute key that is not an explicitly supported property of the `Story` object must be stored in `Story.attributes`.
- Informal Markdown input must support a single-line `key: value` form for story scope.
- Attributes may appear anywhere after the relevant story header line within the story scope when not inside task scope.

##### Ad hoc Attributes Duplicating formal Property names with natural text representations
The following Formal properties of Tasks in the gbdata model that have a parsable text representation separate from the YAML and Informal Single line may also appear as attributes.
 *status*
 *name*
 *detail*

The following Formal properties of Stories in the gbdata model that have a parsable text representation separate from the YAML and Informal Single line may also appear as attributes.
 *status*
 *name*
 *description*
 *maxTasks*

###### Example:

For the following, a file named some-work.md with the markdown text shown below should load to the python gbdata model and should serialize as the JSON shown below.

```markdown
---
"actualCommitMessage": "Buggy first update of mdgbdata.py to support DDF"
"description": "A list of small, focused tasks guiding the current commit with detailed microsected activities."
"title": "some-work.md"
---

This text is part of the file-scoped story description

# Completed work

x - update the gbdata Story object to allow status to be None.
 - A Section is simply a story with no status or tasks. 
 - update gbdata.py to allow status to be None in Story.

```
```json
[
  {
    "id": "08de6878-8f5e-7ff3-9b8f-c472544ec177-6a7e38b4",
    "name": "file-some-work.md",
    "description": "This text is part of the file-scoped story description",
    "attributes": {
      "actualCommitMessage": "Buggy first update of mdgbdata.py to support DDF",
      "description": "A list of small, focused tasks guiding the current commit with detailed microsected activities."
    }
  },
  {
    "id": "35c21655-8361-75c1-ac45-6c6d7a266c54-97782496",
    "name": "Completed work",
    "status": "do",
    "tasks": [
      {
        "id": "e1111a67-255b-7018-b9d4-745108237e86-33345472",
        "status": "completed",
        "name": "update the gbdata Story object to allow status to be None.",
        "detail": " - A Section is simply a story with no status or tasks. \n - update gbdata.py to allow status to be None in Story."
      }
    ]
  }      
]
```


#### MDGBDF Front-matter for Story or Task (Including H1 Section Headings)
YAML key/value pairs embedded in a block of text inside a markdown section body, which may represent a story or task, delimited by a `---` line before and after the block. Expanding on conventional file front-matter, MDGBDF front-matter may also appear after any H1 Section, Task or Story heading.

In DDF documents, conventional front-matter is the special subcase of MDGBDF front-matter where there is a file-scope story that has no text before the first front-matter delimiter. 

Formal Markdown input rules use real YAML parsing through `yaml.safe_load` (PyYAML), matching the YAML library usage in `bin/dtask`.

Front-matter parsing behavior:
- Parse the block as YAML object mapping.
- Parse all keys and scalar values for properties and attributes using normal YAML semantics from `yaml.safe_load`.
- Property and attribute values stored in the gb-data model must be the parsed YAML values, not raw markdown token text.
- Recognized model properties (including `id`) map to formal `Story` or `Task` fields; unrecognized keys map to `attributes`.
- Non-mapping YAML front-matter is invalid input.
- YAML parse errors in front-matter raise `ValueError`.

Pattern:
```
# Section Heading

---
key: value
key2: value2
---

Section body text.
```

Example (a work summary entry inside `# Work Summary`):
```markdown
# 2026-05-19 12:26

---
"workHeadline": "refactor(dtask): simplify do.md work summary insertion"
---

This update streamlines the dtask script's handling of work summary insertions.
```

##### Front-matter future support
Front-matter is not supported for section headings lower than H1 at this time.
Future improvements are described in the backlog stories/ddf-refactor.md

#### Formal Markdown Output Rules
When properties or attributes are serialized as markdown, they must be written as YAML front-matter using the MDGBDF front-matter rules above.

Serialization behavior:
- Story properties and attributes are serialized inside a front-matter block immediately after the story header.
- Task properties and attributes are serialized inside a front-matter block immediately after the task header.
- For both stories and tasks, `id` must be represented as the YAML `id` property in that front-matter block.
- A front-matter block opens with `---` and closes with `---` on left margin.
- Front-matter is serialized with PyYAML (`yaml.safe_dump`) using block-style mapping and insertion-order key preservation.
- Property and attribute serialization must follow normal YAML scalar quoting behavior as emitted by `yaml.safe_dump`.

JSON serialization behavior for YAML-derived attributes:
- Values parsed from YAML front-matter must be serialized to JSON using their parsed property and attribute values from the gb-data model.
- JSON output must reflect YAML parsing semantics (for example, quote delimiters used only for YAML syntax are not part of the resulting string value).


#### Story Description Handling
- `description` consists of Lines after a story header that are not task headers. MDGBDF front-matter and not a crossing heading boundary are story description content.
- Story description contributes to detecting boundaries and preventing false story/task starts.
- In DDF, story description for informational stories is preserved as authored text and must round-trip through parse/serialize flows.

### Bare Task Behavior
Per use-case text, bare tasks can exist without explicit story context, but parser output must be `list[Story]`.

Implement this rule:
- Prefer explicit unnamed markdown headings (`#`, `##`, `###`, `####`, `#####`, `######`) as normal story containers when present.
- If task headers appear before any active story, auto-create a file-scoped story with deterministic id and attach those tasks.
- file-scoped story must be first in the model Story list.

For full DDF parsing, when file-scope story context already exists, bare tasks before the first H1 should be attached to that file-scope story.

### Heading Boundary Rules
When inside a story with heading level `L`:
- Heading level `> L`: treated as inner content context; does not close story.
- Heading level `<= L`: closes current story and all active task/detail accumulation.

### ID Generation
Unique IDs are required fields for `Task` and `Story`.

Generate IDs where possible based on source order and text:
- Story id format: `{UUIDV7}-{hash8}`
- Task id format: `{UUIDV7}-{hash8}`
- If a transient or synthetic story is promoted to a real story to hold tasks, generate a unique story id using these same rules.

Once an ID is created for a non transient or synthetic Story or Task objects, it should be retained through all parsing and serialization
operations, even if the content of the Object changes.

Where:
- `UUIDV7` is the fully approved standard implementation for UUID7 generated for each id.
- `hash8` is first 8 hex chars of SHA-1 of normalized name text.
    If a story or task has no name, temporarily generate a 20 character random string 
    to use in the  hash8 computation, and discard the temporary name.

Normalization for hash input:
- Strip outer whitespace.
- Collapse internal whitespace runs to a single space.
- Keep case as-is.



## API Surface

`bin/mdgbdata.py` must export the following names via `__all__`:
- `StatusEntry`
- `StatusMap`
- `load_status_map`
- `compile_status_patterns`
- `detect_status`
- `strip_status_prefix`
- `parse_stories_from_markdown`
- `parse_stories_from_markdown_file`
- `stories_to_json_text`
- `stories_to_markdown_text`
- `convert_markdown_file_to_json_text`
- `convert_json_file_to_markdown_text`
- `parse_args`
- `main`

## Error Handling
- Invalid metadata key not in `TaskStatus`: raise `ValueError` naming invalid key.
- Invalid metadata entry object shape: raise `ValueError` naming key and missing field.
- Invalid regex in `pat_str`: raise `ValueError` naming key and regex compile error.
- File decode errors in markdown file parser: propagate `UnicodeDecodeError`.
- Invalid YAML front-matter blocks: raise `ValueError`.

Parser robustness rules:
- Never raise for unmatched lines; treat as descriptive text.
- Never raise for empty markdown; return empty list.
- Never create empty-named tasks. If stripping prefix yields empty task name, use `"(unnamed task)"`.
- Never create empty-named stories. If heading text becomes empty, use `"(unnamed story)"`.

## Implementation Notes
- Keep parsing algorithm single-pass over input lines (`O(n)`).
- Avoid recursive parser design; use explicit state variables.
- Compile regex once per parse call.
- Import domain classes from `gbdata.py`; do not duplicate dataclass definitions.

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
   - non-pattern stories with tasks default `Story.status` to `TaskStatus.DO`
   - non-pattern H1 stories without tasks produce informational stories with `Story.status is None`
   - `Story:` heading creates story without tasks
   - story attributes parse to `Story.attributes`
   - nested heading does not create nested story
   - heading levels 1 through 6 are supported for story boundaries

4. Task parsing
   - left-margin task recognized
   - indented task-like line not recognized
   - task detail accumulation until boundary
   - task names/defaults for empty headline
   - task `attributes` default to `None`
   - task `id` parsed from YAML section front-matter as formal model property
   - quoted YAML keys/values in front-matter are parsed to unquoted keys/values in `attributes`

5. YAML property mapping
   - story `id` parsed from YAML front-matter as formal model property
   - task and story `id` serialized in YAML front-matter (not positional `id:` line parsing)

6. Boundary behavior
   - same-level heading closes current story
   - higher-level heading closes current story
   - deeper heading does not close current story

7. Bare tasks
   - tasks before first heading go to special file-scope story

8. Deterministic IDs
   - same input yields same ids across parses
   - id format matches spec

9. DDF whole-document preservation
   - content before first H1 is preserved in file-scope story
   - file with no H1 is represented as a single file-scope story
   - file-scope story name uses `file-{input file name}` in file-based parsing
   - parsing then serializing preserves informational story description text

## Non-Goals
- Parsing full markdown documents with non Story and Task content in this phase.
- Parsing `Goal` and `TimePriorityBlock` from markdown in this phase.
- Auto-mutating metadata JSON files.

## Acceptance Criteria
This spec is accepted when:

1. A generated `bin/mdgbdata.py` exposes all required functions/types with required signatures.
2. Parsing behavior follows this document.
3. `mdgbdata.py` uses model types imported from `gbdata.py`.
4. Tests covering parsing and metadata behavior pass under `pytest`.
5. No third-party dependency is required for module operation.
