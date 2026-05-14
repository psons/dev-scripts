# Overview
create a python script to support the work flow / use cases in docs/dev/spec/usecases/do-file-tasks.md

The dtask command manages the curent git branch and commit messages for the curent task using yaml front mater in a docs/dev/work/do.md file. 

# do.md template


A basic do.md file has text similar to:

```markdown
---
description: A list of small, focused tasks guiding the current commit with detailed microsected activities.
workBranch: <name_of_a_branch_to_commit_work_on>
priorCommit: <latest_git_commit_hash_>
intendedCommitMessage: <description_of_planned_work>
actualCommitMessage: <description_of_completed_work>
---


# do.md - A list of a few small tasks that guide the current commit.

## Microsected task activities
<task_text>
```

The 'description:' is constant to for do.md to help AO understand what is in the do.md file, and may be linked from other project mark down files to help agents discover it.

The 'intendedCommitMessage:' is a message that the engineer belives when starting work, will be a sensible message when committing the work.   

The 'actualCommitMessage:' is the commit message to be used when the work is finally committed.  Since definition and understanding of a task often changes during work, the actualCommitMessages is likely to be different than the intendedCommitMessage.   The difference between the two can represent learning worth mention in the sprint retrospective.

The dtask command supports the following subcommands:

help - prints a list of the sub commands and a description of each.

init - if the git working tree is clean, and there is no do.md file, the init subcommand initializes a new do.md from a base template and sets the priorCommit set, and any other optionally provided information according to the following options:

    --workbranch <name_of_a_branch_to_commit_work_on> a git checkout -b will be performed to create and check out the workBranch  

    -b same as --workbranch

    --intended <description_of_planned_work> the do.md intendedCommitMessage will be set to  <description_of_planned_work>

    -i same as --intended

    --dirty allows work on the init command to proceed even if the git working tree is not clean.  If the do.md file already exists and has been modified since the last commit, exit with an error indicating that the --newdo flag should be used to save and replace the do.md fileWithout the --dirty flag, 'dtask init' will exit with an error if the the working tree is dirty or the do.md file already exists, or both.

    --newdo used together with --dirty, asserts that a fresh do.md file should be created.  If an existing do.md has been modified since the last commit, it will be committed first (with message 'do.md when <cmd>') and that commit becomes the priorCommit in the new do.md, since the old do.md is assumed to relate to a previous task.  If the do.md file is already committed (not dirty), --newdo has no effect: no extra commit is made and the priorCommit in the new do.md is the commit that existed before dtask init was run.  Using --dirty without --newdo when do.md is dirty will exit with an error; in that case a dtask commit is more appropriate.

commit - add a commit on workBranch using the do.md actualCommitMessage.  If the --actual flag is provided, update the do.md actualCommitMessage before using the actualCommitMessage for the commit.

    --actual [<description_of_completed_work>] the do.md actualCommitMessage will be set to  <description_of_completed_work>.  The --actual flag with no arguments copies the do.md intendedCommitMessage to the actualCommit message before the commit. This means the task work proceeded as expected.
    
    -a same as --actual

    --final signals that the task is complete.  dtask commit --final performs two commits: first, all unstaged files are staged and committed using the actualCommitMessage; second, the do.md file is removed and an additional commit is made with a commit message of 'remove do.md'.  This leaves the working tree ready for a new task cycle starting with dtask init.

# Change to implement --newdo
implement --newdo as specified and the script as specified so that the init command will only replace the do.md file if the --newdo flag is provided. 

# not in scope.
at this time, do not implement the features in docs/dev/spec/dtask-un-spec.md

# dtask commit enhancements story.
In this story, the leader `d - ` represents a task to do.

d - change `dtask commit` behavior to by default only commit staged files and only include unstaged files if a --all switch is provided.

# do.md dirty with --final but without --all
if do.md has been modified since the last commit, and the --final option has been specified, then the do.md final must be added to the staged files to be part of the commit.
As previously specified, the do.md file must be removed if the --final option is given, and an additional commit made with the message ''removed do.md for finalized tasks''

# commit --final remove do.md with working tree clean and no staged changes
dtask commit --final should remove the do.md file and then commit even if the working tree is clean and there are no staged changes.

# improve the --final help text and commit message.
I rejected the proposed text in a prior change, but some update is needed.
helptext for the --final option should be as follows:
 
```
--final                 Signal task complete. Performs two commits:
                                                1) commit do.md with staged changes (or all changes if
                                                    --all is used) with actualCommitMessage;
                                                2) remove do.md and commit with message
                                                    'removed do.md for finalized tasks'.
```
The commit message with the removal of the do.md commit should match the help text for te second commit


# scenario based test plan for --final edge cases
Scenarip based tests are deferred at this time so as to avoid creating a scheme to avoid polluting the git index.

## scenario 1: do.md dirty, --final, no --all
goal: confirm dirty do.md is included in the first commit, then do.md is removed in the second commit.

setup:
- create or update docs/dev/work/do.md so the file is dirty.
- stage at least one non-do.md file (or keep only do.md dirty).
- ensure actualCommitMessage in do.md is non-empty.

command:
- run `dtask commit --final`

expected results:
- command exits successfully.
- two commits are created.
- commit 1 uses actualCommitMessage from do.md and includes do.md content updates.
- commit 2 message is `remove do.md` and deletes docs/dev/work/do.md.
- final working tree no longer has docs/dev/work/do.md.

verification checks:
- `git log --oneline -n 2`
- `git show --name-status HEAD`
- `git show --name-status HEAD~1`

## scenario 2: clean working tree, no staged changes, --final
goal: confirm dtask can finalize by removing do.md even when there is nothing else to commit.

setup:
- ensure docs/dev/work/do.md exists and is committed (not dirty).
- ensure there are no staged or unstaged changes.

command:
- run `dtask commit --final`

expected results:
- command exits successfully.
- exactly one new commit is created.
- commit message is `remove do.md`.
- commit deletes docs/dev/work/do.md.

verification checks:
- `git log --oneline -n 1`
- `git show --name-status HEAD`
- `git status --short`


