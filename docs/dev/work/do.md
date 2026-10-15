---
"actualCommitMessage": "feat(domd): Implement upsert for completed tasks in do.md,\
  \ preventing duplication; updated specs and tests"
"description": "A transient file for the feature branch containing current work Stories\
  \ popped from the top of a backlog, enhanced for implementation, then moved to the\
  \ Completed work section."
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

x - test task
---
id: d0b7fd52-eceb-7762-9a55-2cb1ddacf3c1-165a4d59
storyID: acca8cc8-af09-7ca8-9ae6-04ec74356158-a14f8b0a
storyName: 'Story: tasks written into ''# Completed work'' should be upserted.'
---

x - test task
---
id: d0b7fd52-eceb-7762-9a55-2cb1ddacf3c1-165a4d59
storyID: acca8cc8-af09-7ca8-9ae6-04ec74356158-a14f8b0a
storyName: 'Story: tasks written into ''# Completed work'' should be upserted.'
---

x - tasks written into '# Completed work' should be upserted.
---
id: 92eaed74-ec6a-7504-9c96-cfd07ef83ee9-65673e28
storyID: acca8cc8-af09-7ca8-9ae6-04ec74356158-a14f8b0a
storyName: 'Story: tasks written into ''# Completed work'' should be upserted.'
---
tasks written into '# Completed work' should be upserted.
They are currently being duplicated.
The task in this file 'x - test task' was marked as completed, and after a settle, pop, settle sequence as shown below, the task appears twice in the '#Completed work' section.
```markdown
    dtask settle
    dtask pop
    dtask settle
```
If a completed task is present when the story is settled back into the backlog multiple times before the whole story is completed.
### prompt 1
Do I currently have a description of the behavior to upsert a task?
### prompt 2
update this task with instructions for the specification enhancements to fix the bug.  Include a description of what it means to upsert a task.

What it means to upsert a task (into a bare task list, e.g. do.md's `# Completed work` section):
- Tasks are matched by `id`. An incoming task whose `id` already exists in the target list
  **replaces that task in place** (same position), using the incoming task's `status`, `name`,
  `detail`, and `attributes` (including `storyID`/`storyName`) wholesale.
- An incoming task whose `id` is not already present is **appended** to the end, in incoming order.
- No existing task is ever deleted/dropped just because it is absent from the incoming batch.
- This is exactly `gbops.upsert_tasks(existing, incoming) -> list[Task]`, which already implements
  this id-keyed merge (used today by `gbops.upsert_story` for backlog pushes) — it is not yet used
  by do.md's completed-work writer.

Root cause of the duplication bug: `domd.DoDoc.append_completed_tasks` (bin/domd.py) builds the
`# Completed work` task list via plain concatenation — `tasks=existing_tasks + tasks` — instead of
an id-keyed upsert. Across a `settle, pop, settle` sequence, the same already-completed task gets
harvested and appended again on the second settle, producing a duplicate entry instead of updating
the existing one in place.

Spec updates needed:
- `docs/dev/spec/usecases/dtask/dtask-and-do-file-tasks.md`: expand the terse "Needed corrections"
  sentence "When If a tasks are written into do.md # Completed work, they are upserted." into the
  full upsert definition above (id-keyed merge; matching existing tasks are replaced in place,
  preserving position; new tasks are appended; nothing is ever deleted).
- `docs/dev/spec/dtask-final-modules-spec.md`: document that `domd.DoDoc.append_completed_tasks`
  (and therefore `domd.harvest_completed`/`domd.settle`) must perform this upsert via
  `gbops.upsert_tasks`, not concatenation, alongside the existing `upsert_tasks`/`upsert_story`
  documentation already there for the backlog path.

Code fix: `bin/domd.py`'s `append_completed_tasks` must replace `tasks=existing_tasks + tasks` with
`tasks=gbops.upsert_tasks(existing_tasks, tasks)`.

Tests to add: `tests/test_domd.py` needs a regression test that harvests the same completed task
twice (simulating `settle, pop, settle`) and asserts it appears exactly once in `# Completed work`
afterward, with its position preserved and its `storyID`/`storyName`/`status` reflecting the most
recent harvest.

### prompt 3
Now update the specs and implement the code and tests for this task.

x - update tests to match the new DO_MD_DESCRIPTION in dtask.
---
id: 287f1fa7-92d4-7805-ae8d-4c935b4e685f-713cd890
storyID: acca8cc8-af09-7ca8-9ae6-04ec74356158-a14f8b0a
storyName: 'Story: tasks written into ''# Completed work'' should be upserted.'
---
The update in dtask is correct and the tests need to be updated.

# Work Summary


## 2026-10-15 16:22

---
workHeadline: "feat(domd): Implement upsert for completed tasks in do.md, preventing duplication; updated specs and tests"
specChanges: "The `dtask` spec is refined to use `domd.DoDoc.append_completed_tasks` with `gbops.upsert_tasks` to merge completed tasks into `do.md`'s \"Completed work\" section, updating existing tasks by ID and appending new ones, without ever removing completed tasks."
workChanges: "`TODO.md` now defines upserting tasks into `do.md`'s `# Completed work` to prevent duplication, addressing a `bin/domd.py` bug; this requires spec updates, a code fix, new tests, and `do.md`'s frontmatter has been refactored to direct YAML."
---

**Work Planning**: The `TODO.md` file has been significantly updated, providing a detailed definition of what it means to "upsert" tasks into the `do.md` file's `# Completed work` section, emphasizing id-keyed replacement and appending to prevent duplication. This update identifies the root cause of a duplication bug in `bin/domd.py`, where tasks were concatenated instead of upserted, and outlines the required specification enhancements in `dtask-final-modules-spec.md` and `usecases/dtask/dtask-and-do-file-tasks.md`, along with a proposed code fix and new regression tests. Additionally, the frontmatter in `do.md` has been refactored for clarity, transitioning from quoted string values to direct YAML key-value pairs.

**Specification**: The provided git diff refines the specifications for how `dtask` manages completed tasks within the `do.md` file's "Completed work" section. The changes detail that `domd.DoDoc.append_completed_tasks` must use `gbops.upsert_tasks` to merge incoming tasks. This upsert mechanism ensures that if a task's ID already exists in the "Completed work" list, its details are updated in place, preventing duplicates, especially when `dtask settle` re-harvests already-completed tasks. New tasks with unique IDs are appended, and no existing completed task is ever removed.

**Implementation**: The `domd.py` script was updated to prevent duplication of completed tasks when re-harvested into the `do.md` file's "Completed work" section. Specifically, the `append_completed_tasks` method now upserts tasks by ID, updating existing entries and adding new ones, a change reflected in its docstring and the `dtask` script's description of the `do.md` file. A new unit test in `test_domd.py` validates this upsert functionality, ensuring that re-harvested tasks are updated in place rather than duplicated.
## 2026-10-15 15:05

---
workHeadline: Refactor TODO.md to do.md for completed tasks, refine mdgbdata to omit
  "file-input" story IDs from frontmatter, and update specs
specChanges: Documentation for `dtask-final-modules-spec.md` and `mdgbdata-spec.md`
  was updated to ensure the `id` property of the synthetic "file-input" story for
  `# Completed work` tasks is unconditionally omitted from markdown front-matter,
  preventing re-derivable IDs from being explicitly written while retaining them in
  JSON serialization.
workChanges: Refactored `TODO.md` by moving completed `dtask settle` and `Story.status`
  items to a new `do.md` log under a '# Completed work' section, and updated `TODO.md`
  with a new story for upserting tasks into the completed section.
---

**Work Planning**: The `TODO.md` popped out several completed stories and tasks related to `dtask settle` bug fixes and `Story.status` serialization. These items have been moved to a newly created `do.md` file, which now serves as a log for completed work, specifically under a '# Completed work' section. The `TODO.md` file now contains a single, new story focused on ensuring tasks written into the '# Completed work' section are upserted. This change aims to better organize ongoing and completed tasks within the project documentation.

**Specification**: The documentation for `dtask-final-modules-spec.md` and `mdgbdata-spec.md` has been updated to clarify the serialization behavior of the synthetic "file-input" story, specifically when handling tasks in the `# Completed work` section. The change specifies that the `id` property of this grouping story should be unconditionally omitted from markdown front-matter, regardless of whether it's a literal sentinel or a re-parsed generated ID. This ensures that only the bare task list is written, aligning with the design decision to prevent synthetic or re-derivable IDs from being explicitly written into markdown, while still retaining the `id` during JSON serialization. This refinement improves consistency and clarity in how `dtask` and `mdgbdata` handle completed tasks.

**Implementation**: The `mdgbdata.py` script was refined to consistently omit the `id` field from the frontmatter of "file-input" stories when rendering markdown. This prevents an internal sentinel ID from being written to the output, ensuring cleaner markdown for file-level content. Supporting tests in `test_domd.py` and `test_mdgbdata.py` were updated or introduced to verify that this "file-input" story ID is correctly absent from the generated markdown, specifically confirming that the "completed work" section does not erroneously begin with frontmatter after repeated save operations.
