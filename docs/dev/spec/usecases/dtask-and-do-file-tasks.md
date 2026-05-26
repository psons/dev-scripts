# General flow for dtask
## General use
support task analysis and documentation work flow using a do.md file describing how to complete the current task, and support good branch and commit practices:
 - make a branch for the task (or feature).
 - make 1 or more commits for a task.
 - microsect the task if necessary and do commits for each microsected task.
 - optionally squash the commits down to a single commit

microsecting a task means to break it down into small sub-steps for implementation that are more detailed and granular than what an engineer would be inclined to collaborate on with a team. The microsected pieces of a task should be written into the do.md and should not have dependencies outside of the code repo unless those dependencies are already part of the task (and other externally communicated work accounts for the integration).

## flow
### init, commit, ..., commit --final
The user starts with a dtask init and adds detail to perform the task into do.md.  It may be enough for an AI agent to complete the task, or may requires a spec or other manual work.

The user and AI do work, and stage changes with `git add` commands and use 'dtask commit' to get the commit message and commit work.  Normally the user should update the actualCommitMessage in the do.md file before dtask commit.  If the do.md file has not changed since the last commit, but there are staged changes, then dtask should warn the user that a dtask squash, but the commit will proceed.

When the task is complete the user may choose to do a `dtask commit --final` which will do two commits.  First, add all unstaged files will be staged and committed. Second, the do.md file will be removed and an additional commit made.  This state sets up a new cycle for a new task starting with dtask init. 

### dtask squash, git rebase.
dtask squash will search from the latest commit backward until it either finds a sequence of commits with the same commit message or reached the priorCommit from the do.md file.  The first sequence of commits with identical commit messages will be squashed into a single commit.

# use situations

## `dtask init --workbranch` with a clean repo
given a initialized 

## dtask init with --dirty and --newdo 
The user asserts that a new do.md file should be created clean.  If there is an existing uncommitted do.md, then it will be added to a commit, and overwritten. That commit will be the priorCommit in the new do.md file because the old one is assumed to relate to a previous task. 

If the do.md file is already committed, then --newdo has no affect. There is no new commit, and the priorCommit in the new do.md file is the commit from before dtask was run.

## dtask init with --dirty but not --newdo and do.md is dirty
The user has not used --newdo to indicate that the existing do.md file is to be overwritten, so dtask should exit with an error, refusing to overwrite do.md.   In this case, if the do.md is to be preserved, then a dtask commit makes more sense
### Test
---
given: 
---

## dtask commit flag --update
Frequently in refining a current story or task for implementation, a new spec or story is created.   
That new spec or story should remain un tracked while the current work is being implemented.  The --update option to `git add` will avoid pulling tracked files into the staged changes, and will match the wsum file scope with the --update flag. 

## dtask init without --branch (or -b) is an error.
A mission oriented purpose of dtask is to help the user with good branch management.  If a user has not specified a branch, the command should fail with a message that init requires a branch.


