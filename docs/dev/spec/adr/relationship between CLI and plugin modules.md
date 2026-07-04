See also a task in do.md or the TODO.md backlog.
x - decide if the plugin should have command like capabilities, such as might support more specific behaviors than backlog.py. 
    - lets say no, because:
        - the plugins should be tested with unit tests that exercise the API that backlog.py should use, an those unit tests may also test implementation specific functions too.
        - This raises
            question: How should implementation specific capabilities should be exposed, such as managing history of task and story state.
            answer: there is no such thing as implementation specific capabilities, though there may be capabilities that are not implemented for all plugins.
                - the universal API of Goal and task related considerations should be thouught of as One overaching thing, even if the backlog.py or Goal Blotter of dtask does
                not deal with the whole set of functionality of the API.
                - task and story history could be its own top level feature, and may have it's own implementation, independent of the backlog implementation.
                - physical backup is a sysadmin consideration not to be addressed here.
