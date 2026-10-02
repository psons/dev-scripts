
# backlog.py
Implement backlog.py as a command module according to the pattern docs/dev/spec/python-command-module-pattern.md.

backlog.py should invoke plugin modules to implement the 'Backlog Plugin Protocols' below.

## Plugin modules
backlog.py should support a plugin architecture that uses typing.Protocol to define the capabilities needed by backlog.

### Integration with plugins

#### Support of Protocols by plugins
plugins should use the @runtime_checkable decorator so that backlog.py can use isinstance() to determine if required protocols are implemented by a plugin, and raise an error as appropriate to the user. 

#### Plugin selection
backlog.py should support a --provider flag to indicate which plugin to use.

If the --provider flag is not present, use a string value from the environment setting BACKLOG_PROVIDER to determine which plugin to use.

If BACKLOG_PROVIDER is not set, default to bltodo.

#### Planning Roadmap:
The default plugin is Todo as bltodo.py
##### Future Plugins
Other possible future plugins are to implement the backlog protocols against:
 - Taskwarrior as bltw.py
 - Jira as bljira.py
 - Goal Blotter as blgb.py


## Backlog Plugin Protocols

The functions implementing the 'Backlog Plugin Protocols' should return types defined in bin/gbdata.py

* Prioritized implements prioritized which returns a listing of tasks, which are assumed to be in priority order
* PopTask implements pop_task which returns the highest priority task
* PopStory implements pop_story which returns the highest priority story, including all of its tasks. If there are no Stories, but there are tasks, an anonymous story that contains the task list is returned, and other attributes of the story are not set.

## Future Backlog Plugin Protocols
These plugin protocols are not to be implemented yet, but are enumerated here for design planning.

* UpdateTask implements update_task which finds the task with the same id as the task argument and replaces it in the backlog attribute by attribute.  The previous state will be save in some TBD way.

* UpdateStory implements update_story which finds the Story with same id as the required Story argument and replaces it in the backlog attribute by attribute including the full list of tasks.  The previous state will be saved in some implementation dependant way.

* PushStory implements push_story which places the pushed story at the top of the backlog and if the story already existed in the backlog, does a task wise upsert of the pushed story. Task wise upsert means that new tasks are added, and existing tasks are updated, but no tasks are deleted. The previous state will be saved in some way, which may be specific to the plugin implementation.


d - update this spec to say what the load function does. Does it find the story or task by id?  Ir is it to load a local file system cache such as TODO.md
-/t

* Load implements load, which takes a required URL argument of which defaults to the protocol and syntax forms supported by the plugin.  Load defaults to the file:: protocol and the bltodo.py plugin.    If no protocol of the URL exist, defaults and environment settings will exist to perform the load function  

## subcommands of backlog.py 
The subcommands output the data from the corresponding protocol methods according to the following options:
    --mdgbdf: outputs data as MDGBDF using a public API method of mdgbdf.py.
    --json: outputs data as JSON  using a public API method of mdgbdf.py.

The sub command prioritized invokes the 'prioritized' method of the Prioritized protocol of the configured backlog plugin. 
The sub command poptask invokes the 'pop_task' method of the PopTask protocol of the configured backlog plugin.
The sub command popstory invokes the 'pop_story' method of the PopStory protocol of the configured backlog plugin.

The help subcommand outputs a usage summary of subcommands and options.

# plugins do not implement user command line parsing and options for the backlog protocol
See docs/dev/spec/adr/relationship between CLI and plugin modules.md

# bltodo.py - The default plugin.

bltodo.py should be created to implement the first plugin.

bltodo.py will be a plugin that  
 - implements the 'Backlog Plugin Protocols'
 - uses mdgbdata.py to read and write tasks and stories from and to a markdown TODO.md file.

The path to the todo file can be set using and environment variable BL_TODO_FILE

If BL_TODO_FILE is not set, default to the path docs/dev/work/TODO.md relative to the git repo root that contains current working directory.

unit tests should be provided that do not read or write the docs/dev/work/TODO.md file in the source repository.

plugin api: bltodo.py provides an API function for each  of the 'Backlog Plugin Protocols' supported by backlog.py

### Recovery support methods
bltodo.py should also provide two recovery-oriented API methods:

- save_recovery:
    - creates or reuses a recovery directory in a temporary filesystem location, using a mechanism aligned with pytest-style temporary artifact storage (ephemeral temp-root based storage, not repository-local source paths).
    - saves a copy of the current backlog file into that recovery directory.
    - should preserve the source backlog file unchanged and only write the copied recovery artifact.
    - takes an optional argument to specify the number of recovery files to keep, with a default of 4.

- show_recovery:
    - prints the full path of the backlog file currently in use.
    - prints the full path of the recovery directory.
    - prints a listing of the recovery directory contents.

- normalize_backlog:
    - calls into mdgbdata.py to read the current backlog file and normalize content to the formal MDGBDF specification.
    - ensures Story and Task id properties are present according to mdgbdata.py rules during normalization.
    - must successfully invoke save_recovery before writing any normalized content back to the backlog file.
    - after successful recovery save, writes the normalized content back to the configured backlog file path.

### pop_story behavior in bltodo.py
Before returning the popped Story, pop_story must perform the following sequence:

1. call normalize_backlog so that all stories are stored with id attributes.
2. re-read the backlog file after normalization so the in-memory Story list includes normalized id attributes.
3. fetch the Story to pop from that Story list.
4. save a recovery file of the backlog using save_recovery.
5. remove the popped Story from the Story list.
6. save the revised Story list back to the backlog file, excluding the popped Story.

### PushStory protocol in backlog.py

```python
@runtime_checkable
class PushStory(Protocol):
    def push_story(self, story: Story) -> Story: ...
```

- New subcommand `pushstory`, which reads MDGBDF or JSON from a file argument or stdin.
- A programmatic entry point `push_story(story: Story, provider: str | None = None) -> Story` so
  callers such as `dtask` pass a `Story` object directly instead of round-tripping through text.
- `run_backlog_command` gains the `pushstory` dispatch and returns the merged story in the existing
  `BacklogCommandResult` shape.
- `backlog.py` contains **no** merge logic. It performs provider resolution, the `isinstance`
  protocol check (raising a user-facing error when the provider does not implement `PushStory`),
  and dispatch.

### push_story behavior in bltodo.py

```python
def push_story(story: Story, todo_file: str | Path | None = None) -> Story:
    path = resolve_todo_file_path(todo_file)
    normalize_backlog(path)                     # guarantees ids on existing stories
    stories = _read_stories_from_backlog(path)  # re-read to pick up normalized ids
    save_recovery(path)                         # required before any write
    match = gbops.find_story(stories, story)
    merged = gbops.upsert_story(match, story) if match else story
    remaining = [s for s in stories if s is not match]
    _write_stories_to_backlog(path, gbops.lift_story_to_top(remaining, merged))
    return merged
```

- The recovery copy is mandatory and must succeed before the write, matching the `normalize_backlog`
  and `pop_story` contracts above.
- Plugin-specific concerns (path resolution, recovery, MDGBDF write-back, ordering) stay in
  `bltodo.py`. The *meaning* of "upsert" stays in `gbops.py` so future `bljira.py` / `blgb.py`
  plugins reuse it.
- `TODO.md` is written at `story_heading_level=1` (the default), unchanged. `bltodo.py` calls
  `mdgbdata.py` directly and does not route through `ddf.py`, so a future move to a DDF-wrapped
  `# Backlog` section in `TODO.md` is isolated to `bltodo.py` and does not change `gbops.py` or
  `backlog.py`.

### Completed story archiving in bltodo.py

bltodo.py must check the status of each Story in the backlog and archive any Story whose run time
status derived from task state matches `StoryStatus.COMPLETED` to a stack-ordered done file, rather
than leaving completed stories in the backlog.

- The status used for this check is never read directly from `Story.status`. It must be obtained by
  calling a dedicated status-resolution function (e.g. `gbops.resolve_story_status`) that derives
  the runtime status from `Story.tasks` per the rules originally written in 
  [do.md](../work/do.md) and
  [dtask-and-do-file-tasks.md](./usecases/dtask/dtask-and-do-file-tasks.md) that are now authoratative here.:
  - if `tasks` is absent, unset, or an empty list, the story status is `do`.
  - if `tasks` contains any task that is not `completed` or `abandoned`, the story status is `do`
    (and may be `in_progress`).
  - if every task in `tasks` is `completed` or `abandoned`, the story status is `completed`. See
    [do-file-with-all-tasks-completed-story-status.md](./usecases/dtask/do-file-with-all-tasks-completed-story-status.md)
    for an example do.md story archived under this rule, and
    [done-file-with-all-tasks-completed-story.md](./usecases/dtask/done-file-with-all-tasks-completed-story.md)
    for the matching done.md content after archiving.
  - an explicitly set `Story.status` of `completed` or `abandoned` on a story with no tasks is
    honored as-is. See
    [do-file-with-completed-no-tasks-story-status.md](./usecases/dtask/do-file-with-completed-no-tasks-story-status.md)
    for an example do.md story that is archived to done.md under this rule, and
    [done-file-with-completed-no-tasks-story.md](./usecases/dtask/done-file-with-completed-no-tasks-story.md)
    for the matching done.md content after archiving.
  - an explicitly set `Story.status` of `completed` or `abandoned` on a story that has any task
    which is not `completed` or `abandoned` is an error: the status-resolution function must raise
    rather than silently resolve or archive the story. See
    [do-file-with-error-story-status.md](./usecases/dtask/do-file-with-error-story-status.md)
    for an example do.md story that triggers this error.
- The done file path is `docs/dev/work/done/done.md`, resolved relative to the git repo root that
  contains the current working directory (the same repo-root resolution used for the TODO file).
  This path is not configurable via an environment variable.
- `done.md` is a DDF document (see `ddf.py` / [ddf-spec.md](./ddf-spec.md)) with the stack stored in a template
  section `# Completed Stories`, parsed and serialized as MDGBDF (`ddfType: MDGBDF`), mirroring the
  `DO_MD_TEMPLATE` pattern used by `domd.py` for `do.md`.
- `archive_completed_stories` is a dedicated API function, invoked automatically by
  `push_story`. It performs the following sequence:

  1. read the current backlog Story list.
  2. resolve each Story's runtime status via the status-resolution function above, and partition
     stories into completed (resolved status is `StoryStatus.COMPLETED`) and remaining stories.
  3. if there are no completed stories, do nothing and return an empty list.
  4. save a recovery file of the backlog using `save_recovery` before making any change.
  5. write the remaining (non-completed) Story list back to the backlog file.
  6. load `done.md`, creating an empty `# Completed Stories` section if the file does not yet exist.
  7. push each completed Story onto the top of the `# Completed Stories` stack, so the
     most-recently-archived story is stored first, ahead of previously archived stories.
  8. save `done.md`.
  9. return the list of archived Story objects.

### bltodo command line  

bltodo.py when executed as a command with no argument runs the show subcommand by default

#### subcommands
show
 - reports the full absolute path for the TODO file it is using on stdout.
 - outputs the backlog contents in 'Markdown GB Data Form' (MDGBDF)

showdone [n]
 - reports the full absolute path for the done file (docs/dev/work/done/done.md) on stdout.
 - outputs the completed stories from the `# Completed Stories` section in 'Markdown GB Data Form' (MDGBDF).
 - takes an optional numeric argument n to limit output to the top n completed stories on the stack.
 - if n is not provided, outputs all completed stories.

showrecovery
 - invokes the show_recovery function.
 - prints the backlog file path, recovery directory path, and recovery directory listing.

recovery [n]
 - invokes the save_recovery function.
 - takes an optional numeric argument n to specify how many recovery files to keep.
 - if n is not provided, defaults to keeping 4 recovery files.

help
 - shows help text in the style of dtask.

# Output Format -'Markdown GB Data Form' (MDGBDF)
MDGBDF is implemented in mdgbdata.py and is described in docs/dev/spec/mdgbdata-spec.md.


 
