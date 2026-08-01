
# relationship between CLI and plugin modules
Should backlog plugins have command like capabilities, such as might support more specific behaviors than backlog.py?

No, because:
    - the plugins should be tested with unit tests that exercise the API that backlog.py should use, an those unit tests may also test implementation specific functions too.
    - This raises
        question: How should implementation specific capabilities should be exposed, such as managing history of task and story state.
        answer: there is no such thing as implementation specific capabilities, though there may be capabilities that are not implemented for all plugins.
            - the universal API of Goal and task related considerations should be though of as One overarching thing, even if the backlog.py or Goal Blotter of dtask does
            not deal with the whole set of functionality of the API.
            - task and story history could be its own top level feature, and may have it's own implementation, independent of the backlog implementation.
            - physical backup is a sysadmin consideration not to be addressed here.

plugin protocol functions return types from gbdata.py.

# dtask and backlog.py integration with bltodo.py 

bltodo.py has recovery commands, seemingly contradicting the 
assertion of '**relationship between CLI and plugin modules**'

since dtask owns do.md, the backlog protocol can not make sure the do.md write succeeds before deleting the story from the file

dtask owns do.md
bltodo.py owns TODO.md

sooo... 
    bltodo.py should **carefully** update the TODO.md file with id for everything before it processes the pop.
        the bltodo.py will save recovery, then read and rewrite the backlog file in mdgbdf with the with IDs

    **carefully** means save it to history first, then load it update it, and write it back with ids for everything before returning the popped task 
        This is truly a pop, since the content is removed. We do *not* transitionally involve the caller(s) (dtask and backlog.py) expecting them to to persist the data and call bltodo.py finally delete it from the queue.
        if bltodo is really careful, it can pop without needing a call back.   the idea of undoing last operation, or restoring the backlog maybe comes into play, so the recovery showrecovery commands have been built.

dtask calls backlog.pop_story which determines that the configured plugin is bltodo.py
    q: is the recovery operation part of the backlog protocol, or an implementation behavior of bltodo.py?
    a: it is an implementation detail of bltodo.py.  
        - bltodo.py will have a command show recovery files, which will print the name of the recovery directory and show a listing of recovery files in that directory. 
