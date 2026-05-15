---
description: Prioritized development tasks and improvements pending implementation for the TaskForm application.
---
# possible bug from previous work o
d - fix dtask commit --final bug:
    - this may have been dealt with based on previous tasks.
 the commit after removing do.md failed with errors:
    fatal: pathspec 'dev-scripts/docs/dev/work/do.md' did not match any files
    Error: git add (removal of do.md) failed.


# dtask commit enhancements story.

d - improve the headings in do.md: 
 - eliminate the '## Microsected task activities' heading.
 - eliminate the heading: '# do.md - A list of a few small tasks that guide the current commit.'
 - add a front-matter attribute line: 'title: do.md'


# dtask commit summary enhancements story.
d - implement [docs/dev/spec/wsum-module-spec.md](../spec/worksum-module-spec.md) 

d - implement dtask enhancements to work with wsum module

d - dtask should always save and commit do.md
    use case:  
    The do.md file now grows with the work summary for intermediate commits on a feature.  If te new summary is part of a later commit, the summary from the change to do.md pollutes what actually changed in the subsequent commit.  It is better to includes the do.md work summary updates in te same commit they describe.


# branch strategy enhancements story.
d - make branch a required option for dtask init
    - the branch may already exist
    - the branch will always be checked out.
    - verify functionality: I haven't used this much.

d - build out tool specs to support ../spec/usecases/dtask-branch-enhancements-1-spec.md 
 - [proposed-branching-strategy.md](../spec/usecases/proposed-branching-strategy.md)
 - based on docs/dev/spec/usecases/branch-strategy-request.md
 
# Archive worksum story
d - remove the summary-message command and the worksum command, and their specs.
 - use dtask and a do.md file to explicitly mention them in a commit message for the last commit to include them.