
See also: [proposed-branching-strategy.md](usecases/proposed-branching-strategy.md)

dtask init should not default to workBranch:main 

dtask should require a workBranch be specified other than main, but allow support for an override.

should support default branch names, but allow environment vars to set different names for te branch roles:
    release
    main
    integrate
    archive
    <<feature>>

a squash feature should be supported to squash all the commits on the feature branch

a merge command should be added to merge the feature branch if a commit --final was done.
 - should add a tag with the branch name pointing to the merged commit.