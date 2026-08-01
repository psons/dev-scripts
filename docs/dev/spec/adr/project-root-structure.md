
problem -- how should a project root be found?  How should TODO.md be found?
        - dtask has find_repo_root() which assumes we are doing it based on a git repository.  That is good for dtask because a big part of its job is to mange git commits.
        The backlog command manages work that could in theory cut across get repos.  In fact it does for library integration.  How should the backlog command manage its scope?  Is it bound to creation of a collection of artifacts? The backlog should not be part of the git repo for larger integration projects.  the bltodo.py plugin is an exception because it is for small projects, and can use the same git based logic as dtask. so if not set in the environment, use the same path logic as dtask uses for do.md. Users may even wish to symlink that to a backlog elsewhere.

        for small personal scale projects however it is good to back up and version the TODO.md file on a detailed source branch.
