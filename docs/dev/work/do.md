---
"actualCommitMessage": "feat(bltodo): Add TODO.md recovery with save/show commands,\
  \ rename resolve_todo_file, update docs and tests"
"description": "A list of small, focused tasks guiding the current commit with detailed\
  \ microsected activities."
"intendedCommitMessage": "dtask(Feat) to remove popped stories from backlog, but put\
  \ unfinished work back when --final"
"priorCommit": "816de4af8e307023e15e220d8908b350fc420c3f"
"title": "do.md"
"workBranch": "pop-n-unpop"
---


# Current work

# Story: Create recovery needed by bltodo.py
/ - add save_recovery and show_recovery

	x - do spec  
	estimate: 2p  
prompt:
enhance the bltodo.py spec within docs/dev/spec/backlog-spec.md to include specifications for methods save_recovery and show_recovery
save_recovery should use a temp filesystem mechanism similar to how pytest saves test results, and save a copy of the backlog file.  
show_recovery should print the backlog file path, the recovery directory path, and the listing of the recovery directory. 


	/ - run prompt, review, play test  
	estimate: 1p  
prompt: add to the section '#### subcommands' for the bltodo.py spec within docs/dev/spec/backlog-spec.md for the recovery commands.
 - 'showrecovery' which invokes the show_recovery function
 - 'recovery' which takes an optional 'n' argument to specify the number of recovery files to keep, and invokes the save_recovery function.

d - prompt: update bltodo.py per spec within docs/dev/spec/backlog-spec.md

# d - Story: finish dtask pop to remove story from backlog file
---
id: 06a070cf-03b3-7f21-9177-8ecd7a1d4150-63b72315
estimate: 4p
---

d - pop has to delete the story some how.   
    since dtask owns do.md, the backlog protocol can make sure the do.md write succeeds before deleting the story from the file
    sooo. backlog, or specifically bltodo.py should carefully update the TODO.md file wit id for everything before it processes the pop
        - carefully means save it to history first, then load it update it, and write it back with ids for everything before returning the popped task 
            this isn't pop at all, and should be renamed if we expect the caller to persist the data and call backlog back to finally delete it.
            if bltodo is really careful, it can pop without needing a call back.   the idea of undoing last operation, or restoring the backlog maybe comes into play.

            drafting spec prompt:
            A calling python module wil ask to "pop" some content out of a file A.  There is a chance that the caller will fail some how before persisting the popped content.  When this happens, the caller must be able to request that file A bew restored to it s previous state, as it was before the pop.
            The module implementing the pop operation needs a helper module called 

            dtask calls backlog.pop_story which determines that the configured plugin is bltodo.py
                q: is the recovery operation part of the backlog protocol, or an implementation behavior of bltodo.py?
                a: it is an implementation detail of bltodo.py.  
                    - bltodo.py will have a command show recovery files, which will print the name of the recovery directory and show a listing of recovery files in that directory. 

d - remove the popped story from the backlog file
---
id: cc2de8ac-b996-702e-94df-00d06fe13017-2fb086c5
---
 - This feature avoids the situation where users would need to maintain the same Story in two files.
 - Take together with the previous assumption, it means state for the TODO list can be manipulated as objects in memory and written back to the TODO.md file in new state.
    a - add a feature to strip the id: attributes upon serialization by mdgbdata.py.   This avoids unnecessary noise in te TODO.md if there is no write back to the backlog.
        a - include a feature to eliminate the front-matter section if there are no attributes to write into it.

d - write spec for pop remove from backlog TODO.md
 - dtask writes the popped story to do.md
    - it should error if the write to do.md is unsuccessful
 - once it has been successfully written to do.md
 - extend the backlog protocol on backlog.py to support 'remove-story'
    - dtask should call the backlog module with the id of the popped story to remove it from the backlog. 
        - the call should error if unsuccessful.
        at present the only plugin that exists is bltodo.py which must interpret the 'remove-story' as a removal from thw backlog file  (TODO.md by default)
            - bltodo.py should
                - save the backlog file to history using histcache.py as a module 
                    - error if unable to save TODO.md to history
                - read the backlog file, remove the task with the matching id from the list, and rewrite the backlog file.

# Completed work

# Work Summary


## 2026-07-31 12:04

---
workHeadline: "feat(bltodo): Add TODO.md recovery with save/show commands, rename resolve_todo_file, update docs and tests"
---

The `bltodo.py` script has been significantly enhanced to include robust recovery capabilities for the `TODO.md` backlog file. This update introduces `save_recovery` to create timestamped backups in a temporary directory and prune older copies, and `show_recovery` to display paths to the active backlog and its recovery files. The command-line interface now features `recovery` and `showrecovery` subcommands, allowing users to manage these backups directly. Additionally, the internal `resolve_todo_file` function was renamed to `resolve_todo_file_path` for improved clarity, with a backward-compatible alias maintained. Corresponding updates have been made to the `backlog-spec.md` documentation and the `test_bltodo.py` test suite to reflect these new functionalities.
