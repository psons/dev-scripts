---
"actualCommitMessage": "Refactor TODO.md to do.md for completed tasks, refine mdgbdata\
  \ to omit \"file-input\" story IDs from frontmatter, and update specs"
"description": "A list of small, focused tasks guiding the current commit with detailed\
  \ microsected activities."
"intendedCommitMessage": "upsert task text if already in do.md #Completed work"
"priorCommit": "5e6e93493bd6d7a1b4c6793fe62cff5b9502935a"
"title": "do.md"
"workBranch": "completed-work-duplication"
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

x - The do.md # Completed work section should not have a story ID printed.
---
id: 494de960-7a7f-72c2-a7ad-050a78e27bd3-04761a93
'"file-input")': story_frontmatter["id"] = story.id`). That only covers the first
  save after
Code: '`mdgbdata._render_markdown_story` must drop the `story.id == "file-input"`
  literal check and'
storyID: 09dc64b3-fee1-70de-a008-0f54c098571e-1c1f6eb5
storyName: 'Story: The do.md # Completed work section should not have a story ID printed.'
---
### prompt1
DDF type MDGBDF sections to be printed as bare task lists should not have a printed ID for an enclosing story.
What spec updates are needed to so so that do.md # Completed work section does not have a story ID printed?
Add the detail underneath this task.

Root cause: `mdgbdata._render_markdown_story`'s suppressed-header rule only omits `id` when it
equals the literal sentinel string `"file-input"` (`if not (suppress_header and story.id ==
`domd.append_completed_tasks` constructs the in-memory wrapper `Story(id="file-input", ...)`. On
the next parse (e.g. a later `dtask pop`/settle re-reading the saved do.md), the bare task list
under `# Completed work` has no heading, so `mdgbdata.ensure_file_scope_story()` creates a fresh
implicit "file-input" story and assigns it a real derived id (`{uuid7}-{hash8}`, e.g.
`08de6878-8f5e-7ff3-9b8f-c472544ec177-6a7e38b4` as seen above) instead of the literal sentinel. The
literal-string check no longer matches, so the `id` gets printed again on the next save — this is
exactly the `08de6878-...` id currently sitting under `# Completed work` in this file.

Spec updates needed:
- `docs/dev/spec/mdgbdata-spec.md` "Markdown Serialization" section: generalize the file-input
  suppressed-header rule so `id` is unconditionally omitted from the front-matter block whenever
  the header is suppressed (first story named exactly `file-input`), regardless of the id's value
  — not only when `id == "file-input"` literally. Note that this id is always deterministically
  re-derivable at parse time from (kind, story order, name) when not explicit in the source, so
  omitting it from markdown never loses information for this synthetic grouping story; only
  `stories_to_json_text` (JSON) still includes the id, since JSON output is not subject to this
  markdown-only suppression rule.
- `docs/dev/spec/dtask-final-modules-spec.md` §3.3 "Bare task list rendering": update to state the
  `id` omission applies unconditionally to the suppressed-header story, since the file-input
  wrapper id backing the `# Completed work` bare task list is always internal/synthetic, not just
  when it happens to equal the literal string `"file-input"`.
- No change needed in `docs/dev/spec/usecases/story-task-parsing-md.md` or the ddf ADR script spec;
  this rule is specific to mdgbdata.py's Markdown Serialization section.

unconditionally omit `id` whenever `suppress_header` is true.

Tests to update: `tests/test_mdgbdata.py`'s
`test_stories_to_markdown_suppresses_first_story_header_for_file_input_story_name` and
`test_cli_tomd_suppresses_first_story_header_for_file_input_name` currently assert the id IS
written for a suppressed-header story with a non-sentinel id — they must be changed to assert the
`id` line is absent. `test_stories_to_markdown_omits_id_for_synthetic_file_input_story_with_literal_id`
already covers the literal-sentinel case and should keep passing unchanged. Add a round-trip test
in `tests/test_domd.py` that harvests completed tasks, saves, reloads, harvests/saves again, and
asserts no `id:` line precedes the `# Completed work` bare task list after the *second* save too
(the first save already passes today; only the second save currently regresses).

### prompt2
Now update the specs ad implement the code and tests for this task.

# Work Summary

## 2026-10-15 15:05

---
workHeadline: "Refactor TODO.md to do.md for completed tasks, refine mdgbdata to omit \"file-input\" story IDs from frontmatter, and update specs"
specChanges: "Documentation for `dtask-final-modules-spec.md` and `mdgbdata-spec.md` was updated to ensure the `id` property of the synthetic \"file-input\" story for `# Completed work` tasks is unconditionally omitted from markdown front-matter, preventing re-derivable IDs from being explicitly written while retaining them in JSON serialization."
workChanges: "Refactored `TODO.md` by moving completed `dtask settle` and `Story.status` items to a new `do.md` log under a '# Completed work' section, and updated `TODO.md` with a new story for upserting tasks into the completed section."
---

**Work Planning**: The `TODO.md` file was refactored, removing several completed stories and tasks related to `dtask settle` bug fixes and `Story.status` serialization. These items have been moved to a newly created `do.md` file, which now serves as a log for completed work, specifically under a '# Completed work' section. The `TODO.md` file now contains a single, new story focused on ensuring tasks written into the '# Completed work' section are upserted. This change aims to better organize ongoing and completed tasks within the project documentation.

**Specification**: The documentation for `dtask-final-modules-spec.md` and `mdgbdata-spec.md` has been updated to clarify the serialization behavior of the synthetic "file-input" story, specifically when handling tasks in the `# Completed work` section. The change specifies that the `id` property of this grouping story should be unconditionally omitted from markdown front-matter, regardless of whether it's a literal sentinel or a re-parsed generated ID. This ensures that only the bare task list is written, aligning with the design decision to prevent synthetic or re-derivable IDs from being explicitly written into markdown, while still retaining the `id` during JSON serialization. This refinement improves consistency and clarity in how `dtask` and `mdgbdata` handle completed tasks.

**Implementation**: The `mdgbdata.py` script was refined to consistently omit the `id` field from the frontmatter of "file-input" stories when rendering markdown. This prevents an internal sentinel ID from being written to the output, ensuring cleaner markdown for file-level content. Supporting tests in `test_domd.py` and `test_mdgbdata.py` were updated or introduced to verify that this "file-input" story ID is correctly absent from the generated markdown, specifically confirming that the "completed work" section does not erroneously begin with frontmatter after repeated save operations.
