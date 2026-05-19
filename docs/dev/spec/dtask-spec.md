# Overview
create a python script to support the work flow / use cases in docs/dev/spec/usecases/do-file-tasks.md

The dtask command manages the current git branch and commit messages for the current task using yaml front mater in a docs/dev/work/do.md file. 

# do.md template


A basic do.md file has text similar to:

```markdown
---
title: do.md
description: A list of small, focused tasks guiding the current commit with detailed microsected activities.
workBranch: <name_of_a_branch_to_commit_work_on>
priorCommit: <latest_git_commit_hash_>
intendedCommitMessage: <description_of_planned_work>
actualCommitMessage: <description_of_completed_work>
---
<task_text>
```

The 'description:' is constant to for do.md to help understand what is in the do.md file, and may be linked from other project mark down files to help agents discover it.

The 'intendedCommitMessage:' is a message that the engineer believes when starting work, will be a sensible message when committing the work.   

The 'actualCommitMessage:' is the commit message to be used when the work is finally committed.  Since definition and understanding of a task often changes during work, the actualCommitMessages is likely to be different than the intendedCommitMessage.   The difference between the two can represent learning worth mention in the sprint retrospective.

The dtask command supports the following subcommands:

help - prints a list of the sub commands and a description of each.

init - if the git working tree is clean, and there is no do.md file, the init subcommand initializes a new do.md from a base template and sets the priorCommit, and any other optionally provided information according to the following options:

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

## clarification 2026-05-18
Ensure that if do.md is updated in any way by dtask, ensure that it is saved and added to the working set before making the commit. In particular, the --actual flag updates the actualCommitMessage and requires that do.md be written and added to the working set before the commit.

### Change to implement --newdo
implement --newdo as specified and the script as specified so that the init command will only replace the do.md file if the --newdo flag is provided. 

# not in scope.
at this time, do not implement the features in docs/dev/spec/dtask-un-spec.md

# dtask commit enhancements story.
In this story, the leader `d - ` represents a task to do.
Example
```markdown
d - change `dtask commit` behavior to by default only commit staged files and only include unstaged files if a --all switch is provided.
```

# dtask commit flag --update
Add a `--update` option to `dtask commit` to support committing tracked work while intentionally leaving untracked files out of scope.

## purpose
When refining a task, engineers often create new notes/spec files that should remain untracked until a later commit. `dtask commit --update` should support this workflow by staging only tracked file updates.

## behavior
- `dtask commit --update` must run the equivalent of `git add --update` before commit.
- The resulting commit scope includes:
    - already staged files
    - tracked files with unstaged modifications
    - tracked files deleted from the working tree
- The resulting commit scope excludes:
    - untracked files
- Commit message behavior remains unchanged: use `actualCommitMessage` from `docs/dev/work/do.md`, with existing `--actual` behavior preserved.

## option interactions
- `--update` and `--all` are mutually exclusive.
- `dtask commit` with neither `--all` nor `--update` keeps current default behavior (commit staged files only).
- `dtask commit --final --update` should behave like `--final` but with first-commit staging scope equal to `--update` semantics, except for the existing rule that dirty `do.md` must be included in the first commit.

## alignment requirement
- `dtask commit --update` file-inclusion scope must align with `wsum --update` summarization scope.

## help text update
Commit command usage/help should include `--update, -u` and describe it as: stage tracked updates only (same scope as `git add --update`, excluding untracked files).

## do.md dirty with --final but without --all
if do.md has been modified since the last commit, and the --final option has been specified, then the do.md must be added to the staged files to be part of the commit.
As previously specified, the do.md file must be removed if the --final option is given, and an additional commit made with the message ''removed do.md for finalized tasks''

# commit --final remove do.md with working tree clean and no staged changes
dtask commit --final should remove the do.md file and then commit even if the working tree is clean and there are no staged changes.

# improve the --final help text and commit message.
Some update is needed.
helptext for the --final option should be as follows:
 
```
--final                 Signal task complete. Performs two commits:
                                                1) commit do.md with staged changes (or all/tracked changes with
                                                    --all/--update respectively) with actualCommitMessage;
                                                2) remove do.md and commit with message
                                                    'removed do.md for finalized tasks'.
```
The commit message with the removal of the do.md commit should match the help text for the second commit

# init requires a branch
## Use Case
A mission oriented purpose of dtask is to help the user with good branch management.  If a user has not specified a branch, the command should fail with a message that init requires a branch.

## behavior
if a branch is not specified with --workbranch (or -b) the command should fail with a message that init requires a branch.

## not required
there is no requirement that the specified branch is different than the current branch.  dtask will have no knowledge of branching strategy, but a future utility that will help with branching strategy may use dtask and have that requirement.


# dtask using the wsum.py module
Add integration between `dtask commit` and `bin/wsum.py` so work summaries and commit headlines can be generated into `docs/dev/work/do.md`.

## new option
- Add the `--wsum` option to `dtask commit`.
- When `--wsum` is provided, `dtask` must call the wsum python module function summarize_work and add the the WorkSummaryResult.markdown to `docs/dev/work/do.md`.
- The added markdown will include frontmatter key `workHeadline:` and the generated work summary content in the body.

## do.md summary insertion rules
- If this is the first generated summary being added to `docs/dev/work/do.md`, `dtask` must add a markdown header `# Work Summary` before adding the summary text.
- If `# Work Summary` already exists, prepend summary content immediately after the existing `# Work Summary` header, before any older subsections.

### Clarification 2026-05-18 17:21
dtask should not provide any headings under the # Work Summary header.  The required headings will be part of the WorkSummaryResult.markdown.
Verified assumption: in the current `bin/wsum.py` implementation, every successful `summarize_work` return includes `WorkSummaryResult.markdown` containing frontmatter with `workHeadline:`.
The new subsections under '# Work Summary' should be inserted into do.md at the top of the '# Work Summary' immediately after the '# Work Summary' heading, before any older subsections.

### Clarification 2026-05-19 08:58
When wsum.summarize_work is invoked by dtask, the scope of the commit from --update or --all should be reflected in the request by setting the correct values for include_unstaged and include_untracked.

## commit message behavior
- For `dtask commit` runs without `--final`, default commit message behavior changes to use the first, or newest `workHeadline` from `docs/dev/work/do.md`.
- `--final` keeps the existing commit message behavior that uses `actualCommitMessage`.
- Existing `--actual` / `-a` behavior remains unchanged and applies as already implemented for `actualCommitMessage`.

### Clarification 2026-05-19 11:14
dtask commits without --final or --actual should assure that the frontmatter workHeadline is used to update the actualCommitMessage into the do.md file and used as the commit message. 

## Clarification 2026-05-19 12:14
work summaries should be inserted into do.md immediately after the heading '# Work Summary', before any existing summary subsection content.

## wsum execution and timeout
- `dtask --wsum` must allow `wsum.summarize_work` at most 45 seconds to complete.
- If `wsum` does not complete within 45 seconds, `dtask` must terminate the `wsum.summarize_work` call, treat this as an error, and stop the `--wsum` update flow.
 
## wsum error handling
- If `wsum` returns an error (including timeout termination), `dtask` should surface the `wsum` error details as clearly as possible.
- Error guidance should recommend manual fallback by asking the user to provide a manual work summary and set `actualCommitMessage:` in `docs/dev/work/do.md`.

## clarification 2026-05-18 13:55
Update comments to enforces that if dtask commit has been invoked with the default commit of staged changes only, then wsum should only attempt to summarize staged changes.


# scenario based test plan for --final edge cases
Scenario based tests are deferred at this time so as to avoid creating a scheme to avoid polluting the git index.

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


