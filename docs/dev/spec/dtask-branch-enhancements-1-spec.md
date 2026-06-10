
See also: [proposed-branching-strategy.md](usecases/proposed-branching-strategy.md)

For branching strategy, dtask init should not be done to workBranch:main or whatever the detailed commits are kept on.
 - dtask requires a work branch, but currently allows it to be main.
 - a tool to manage branching strategy should do whatever branch merging is called for by the strategy.

d - dtask should require a workBranch be specified other than main, but allow support for an override.

should support default branch names, but allow environment vars to set different names for te branch roles:
    release
    main
    integrate
    archive
    <<feature>>

a squash feature should be supported to squash all the commits on the feature branch

a merge command should be added to merge the feature branch if a commit --final was done.
 - should add a tag with the branch name pointing to the merged commit.