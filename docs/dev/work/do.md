---
"actualCommitMessage": "Refactor: `dtask`, `bltodo`, `mdgbdata` prevent story/task\
  \ status & ID fabrication for improved data fidelity"
"description": "A list of small, focused tasks guiding the current commit with detailed\
  \ microsected activities."
"intendedCommitMessage": ""
"priorCommit": "d7328886e1775a2944f8daa71b70ee536874564e"
"title": "do.md"
"workBranch": "dtask-settle-fixes"
---


# Current work

# Completed work

x - copying work into the '# Completed work' section should not write the story ID 'file-input'
---
id: e004bd60-0408-7f01-845d-2e17bfa6710d-0cbe5172
storyID: 02cc0bee-ece0-71b1-963f-10caf5a60c9d-94e4fad9
storyName: 'Story: Bug fixes for dtask settle'
---
Writing work into the '# Completed work' section should not write the story ID 'file-input' as shown here:
```markdown
    ---
    id: file-input
    ---
```
Writing the bare tasks do not need to be encapsulated in a file scope story because each task has its own story ID attribute.
Add an update to the relevant software module specs and fix the behavior.

x - dtask pop (backlog.py?) should not attempt to write derived status into stories when serializing.
---
id: 4beb3878-9dc8-7ad3-9fe0-603ac972482a-983f1fd4
storyID: 02cc0bee-ece0-71b1-963f-10caf5a60c9d-94e4fad9
storyName: 'Story: Bug fixes for dtask settle'
---
`Story.status` must never be set to a fabricated/default value anywhere in the parse/serialize
pipeline. `StoryStatus.DO` (or any other status) should only ever be recorded on a `Story` when it
was explicitly present in the parsed source (an explicit status marker in the heading) or explicitly
set by a caller/UI. Backlog logic (`gbops.resolve_story_status` et al.) already determines whether a
story is complete by examining its tasks' statuses at runtime, so a stored `Story.status` is never
needed just to answer "is this story done" questions.

Concretely, for example the 'd - ' below was fabricated and written into do.md, but it wasn't present
in TODO.md's source:
```markdown
    ## d - Story: Bug fixes for dtask settle
    ---
    id: 02cc0bee-ece0-71b1-963f-10caf5a60c9d-94e4fad9
    ---
```

Update these spec sources (remove the "default to `StoryStatus.DO`" rule; parsing a markerless/
non-pattern story heading, even one with tasks, must leave `Story.status` as `None`):
- docs/dev/spec/mdgbdata-spec.md: the "Story Name and Story Status" section's "If no status pattern
  matched, set the `Story.status` to `StoryStatus.DO`." line and the "Summary of Round trip handling
  of the story marker" bullet about a default being set when a marker was found; the "Task Name,
  Status, and Detail" section's "(default `StoryStatus.DO` for non-pattern headings)" note; and the
  implementation-notes bullet "non-pattern stories with tasks default `Story.status` to
  `StoryStatus.DO`".
- docs/dev/spec/usecases/story-task-parsing-md.md: the "a default story status of 'do' must be
  applied" sentence.
- docs/dev/spec/adr/ddf/script-ai-friendly-texts-development-description-format.md: the "it defaults
  to a 'do' status" sentence.

Then fix `bin/mdgbdata.py`'s `parse_stories_from_markdown` to stop defaulting the story status to
`StoryStatus.DO` when no status pattern matched (it must stay `None`), and confirm
`_render_markdown_story` still renders a `None`-status story with the plain (non-prefixed) header,
exactly like the existing "text story" rendering path, so a `# Story: X` heading with tasks but no
explicit marker round-trips without gaining a fabricated `d - ` prefix.

Audit `bin/bltodo.py`'s `_strip_default_story_status` workaround (added specifically to undo this
fabricated default before writing to the backlog/done.md) — once the parser itself never fabricates
the default, confirm whether this workaround is still needed anywhere before simplifying or removing
it.

Update all mdgbdata-spec.md-backed tests (tests/test_mdgbdata.py and any dependents in
tests/test_bltodo*.py, tests/test_domd.py, tests/features/**) that currently assert a markerless/
non-pattern story heading with tasks parses to `StoryStatus.DO` — they must instead assert
`status is None`, with serialization of such a story keeping the plain header form.

# Work Summary

## 2026-10-13 15:54

---
workHeadline: "Refactor: `dtask`, `bltodo`, `mdgbdata` prevent story/task status & ID fabrication for improved data fidelity"
specChanges: "The git diff refines story status parsing/serialization by preventing automatic 'do' defaulting, requiring explicit matching or external provision for `Story.status`, and omits the `id` attribute from front-matter for synthetic \"file-input\" stories across several spec files."
workChanges: "Two `dtask settle` bug fixes were moved from `TODO.md` to `do.md`, a `dtask pop` serialization bug requiring spec and `mdgbdata.py` modifications is detailed, and new `wsum` test failure tasks were added to `TODO.md`."
---

**Work Planning**: This diff reflects updates to development task tracking. Two tasks related to `dtask settle` bug fixes have been marked as completed in `TODO.md` and moved to a newly created `do.md` file, which now serves to hold completed work. The task concerning `dtask pop` incorrectly writing derived status during serialization includes a detailed explanation of the issue and outlines a plan to modify several specification documents, `bin/mdgbdata.py`, and various test files to prevent the fabrication of story statuses. Additionally, new tasks addressing `wsum` test failures have been added to `TODO.md`.

**Specification**: The git diff introduces a significant refinement to how story statuses are parsed and serialized across `script-ai-friendly-texts-development-description-format.md`, `dtask-final-modules-spec.md`, `mdgbdata-spec.md`, and `story-task-parsing-md.md`. The core change stipulates that `Story.status` is never to be fabricated by the parser; it must only be set when explicitly matched from a header pattern or provided externally. This update prevents automatic defaulting of a story's status to 'do', ensuring more precise data representation. Additionally, a new serialization rule for synthetic "file-input" stories (used for bare task lists) was added, instructing the `id` attribute to be omitted from their front-matter, which refines how such tasks are round-tripped and presented.

**Implementation**: The changes in `bltodo.py` and `mdgbdata.py` remove the automatic assignment of a "do" status to stories and tasks that do not explicitly specify one, ensuring that the generated markdown accurately reflects the input without fabricating status information. Consequently, the "Story:" marker, if present in a heading, is now preserved in the story's name rather than being implicitly tied to a "do" status. Furthermore, an internal "file-input" story ID, used for unassociated tasks, is no longer written to disk, preventing the persistence of synthetic identifiers. These modifications improve data fidelity and consistency when parsing and rendering markdown.
