---
"actualCommitMessage": "feat(bltodo.py) TODo specific pop behavior to save recovery to safely pop story content for insertion to do.md"
"description": "A list of small, focused tasks guiding the current commit with detailed\
  \ microsected activities."
"intendedCommitMessage": "dtask(Feat) to remove popped stories from backlog, but put\
  \ unfinished work back when --final"
"priorCommit": "816de4af8e307023e15e220d8908b350fc420c3f"
"title": "do.md"
"workBranch": "pop-n-unpop"
---

# Current work


# Completed work

# d - Story: finish dtask pop for the bltodo plugin to remove story from backlog file
---
id: 06a070cf-03b3-7f21-9177-8ecd7a1d4150-63b72315
estimate: 4p
---
in bltodo.py, pop has to delete the story some how.   

        drafting spec prompt:
        A calling python module wil ask to "pop" some content out of a file A.  There is a chance that the caller will fail some how before persisting the popped content.  When this happens, the caller must be able to request that file A bew restored to it s previous state, as it was before the pop.
        The module implementing the pop operation needs a helper module called 


x - implement add id capability in bltodo.py
    specPrompt:update the bltodo.py spec within docs/dev/spec/backlog-spec.md to require a method that will call into mdgbdata to read the contents of the backlog file and and normalize it to the formal mdgbdata specification, including id properties  for Stories and Tasks.  The method must successfully save a recovery file and then The method should then resave the normalized contents back to the backlog file.

x - update bltodo pop_story to carefully remove the popped story from the backlog.
    specPrompt: 
update the bltodo.py spec within docs/dev/spec/backlog-spec.md so that: before returning the popped story, pop_story will 
     - call normalize_backlog so that all stories are stored id attributes
     - re-read the backlog file with id attributes
     - fetch the story to pop from the list of stories
     - save a recovery file of the backlog 
     - remove the popped story from the list of stories.
     - save the revised list of stories to the backlog file (without the popped story)     


x - remove the popped story from the backlog file
---
id: cc2de8ac-b996-702e-94df-00d06fe13017-2fb086c5
---
 - This feature avoids the situation where users would need to maintain the same Story in two files.
 - Take together with the previous assumption, it means state for the TODO list can be manipulated as objects in memory and written back to the TODO.md file in new state.
    a - add a feature to strip the id: attributes upon serialization by mdgbdata.py.   This avoids unnecessary noise in te TODO.md if there is no write back to the backlog.
        a - include a feature to eliminate the front-matter section if there are no attributes to write into it.


# d - story: bug fix
x - update a line in the spec do TODO.md is based on git, not the script location.

update the bltodo.py spec within docs/dev/spec/backlog-spec.md 
edit this:

If BL_TODO_FILE is not set, default to the path relative to the running program file ../docs/dev/work/TODO.md.

# d - story: list bug from quick test an make tasks.

x - bltodo.py should locate backlog file per project
    bug: a different repo reached to the dev-scripts backlog to pop.
    x - spec written as one line modification in spec
    x - prompt: update bltodo.py per its spec within docs/dev/spec/backlog-spec.md, as updated since the last git commit. 

    x - will be fixed, I think when above is fixed - everything shares a collection of recovery files, because the 
        location is partly based on the path to the file being backed up.
 x - recovery path has pytest in the nam. get it out.


# Story: Create recovery needed by bltodo.py
x - add save_recovery and show_recovery

	x - do spec  
	estimate: 2p  
prompt:
enhance the bltodo.py spec within docs/dev/spec/backlog-spec.md to include specifications for methods save_recovery and show_recovery
save_recovery should use a temp filesystem mechanism similar to how pytest saves test results, and save a copy of the backlog file.  
show_recovery should print the backlog file path, the recovery directory path, and the listing of the recovery directory. 


	x - run prompt, review, play test  
	estimate: 1p  
prompt: add to the section '#### subcommands' for the bltodo.py spec within docs/dev/spec/backlog-spec.md for the recovery commands.
 - 'showrecovery' which invokes the show_recovery function
 - 'recovery' which takes an optional 'n' argument to specify the number of recovery files to keep, and invokes the save_recovery function.

x - prompt: update bltodo.py per spec within docs/dev/spec/backlog-spec.md


# Work Summary

## 2026-08-01 14:41

---
workHeadline: "feat: Streamline docs; remove obsolete files, consolidate architecture, add user doc structure, and clean up todos"
---

This update streamlines documentation by removing obsolete files like `story_test.json` and `todo-test-round-trip.md`, and consolidating architectural decisions regarding CLI and plugin module relationships into the new `script-module-relationships.md`. Additionally, a new specification for `user-documentation-structure.md` was introduced, outlining the expected layout and content for user-facing guides. The `TODO.md` and `do.md` files were also cleaned up, marking several `bltodo.py` and `dtask` related tasks as complete and refining explanations for `pop` behavior.
## 2026-08-01 11:33

---
workHeadline: "feat(bltodo): Prioritize TODO.md at git root; update spec, add test, document project root structure"
---

The provided git diff introduces changes to `bltodo.py` and its supporting documentation and tests, primarily focused on how the `TODO.md` backlog file is located. The `bltodo.py` script now prioritizes finding `TODO.md` relative to the git repository root of the current working directory, if the `BL_TODO_FILE` environment variable is not set, a behavior that is now reflected in `backlog-spec.md` and validated by a new unit test in `test_bltodo.py`. Additionally, a new architectural decision record, `project-root-structure.md`, has been added to explain the rationale behind this change, and minor modifications were made to `do.md` and `TODO.md` to update work items and fix formatting.
## 2026-07-31 17:05

---
workHeadline: "feat(bltodo): Implement backlog normalization, pre-pop recovery, and update docs/tests for enhanced data integrity"
---

The `bltodo.py` script has been updated to include a new `normalize_backlog` function, which reads, standardizes, and rewrites the backlog markdown, ensuring all stories have ID attributes. The `pop_story` method now incorporates this normalization, along with a critical step to save a recovery file of the backlog *before* removing a story and persisting the changes. These modifications enhance data integrity and provide a robust recovery mechanism. The changes are reflected in `docs/dev/spec/backlog-spec.md` and new tests have been added to `tests/test_bltodo.py` to cover the new functionality.
## 2026-07-31 12:04

---
workHeadline: "feat(bltodo): Add TODO.md recovery with save/show commands, rename resolve_todo_file, update docs and tests"
---

The `bltodo.py` script has been significantly enhanced to include robust recovery capabilities for the `TODO.md` backlog file. This update introduces `save_recovery` to create timestamped backups in a temporary directory and prune older copies, and `show_recovery` to display paths to the active backlog and its recovery files. The command-line interface now features `recovery` and `showrecovery` subcommands, allowing users to manage these backups directly. Additionally, the internal `resolve_todo_file` function was renamed to `resolve_todo_file_path` for improved clarity, with a backward-compatible alias maintained. Corresponding updates have been made to the `backlog-spec.md` documentation and the `test_bltodo.py` test suite to reflect these new functionalities.
