---
actualCommitMessage: dtask adds do.md to the commit it changes.
description: A list of small, focused tasks guiding the current commit with detailed
  microsected activities.
intendedCommitMessage: dtask use wsum for AI generated work summary and commit message
priorCommit: 18416e5fc35b12fb91d3f84b76032340c7f3ff69
workBranch: dtask-wsum
---

# do.md - A list of a few small tasks that guide the current commit.

# init requires a branch
x - make branch a required option for dtask init
    - the branch may already exist
    - the branch will always be checked out.
    - verify functionality: I haven't used this much.

# possible bug from previous work 
a - fix dtask commit --final bug:
    - abandoned. does not seem to be a problem
    - this may have been dealt with based on previous tasks.
 the commit after removing do.md failed with errors:
    fatal: pathspec 'dev-scripts/docs/dev/work/do.md' did not match any files
    Error: git add (removal of do.md) failed.


# dtask commit enhancements story.

x - improve the headings in do.md: 
 - eliminate the '## Microsected task activities' heading.
 - eliminate the heading: '# do.md - A list of a few small tasks that guide the current commit.'
 - add a front-matter attribute line: 'title: do.md'


# dtask commit summary enhancements story.
x - implement [docs/dev/spec/wsum-module-spec.md](../spec/worksum-module-spec.md) 
 - done as prerequisite

# Story  implement dtask enhancements to integrate with the work with wsum module.
x - generate an updated specification section to docs/dev/spec/dtask-spec.md called 'dtask using the wsum.py module'
    - add a --wsum option to invoke the wsum command to update the work summary in do.md, including the workHeadline: frontmatter
    - change default behavior for commits without the --final option to use the workHeadline as the commit message. 
    - add documentation that to say that '--final will use the actual commit message behavior (as already implemented), including the existing implementations of --actual (and -a) 
    - if wsum errors, try to communicate the wsum error, and suggest the user provide a manual summary and 'actualCommitMessage:' in do.md
    - add a header '# Work Summary' to do.md before adding the work summary if this is the first work summary being added to do.md.
## 2026-05-19 09:07

---
workHeadline: dtask commit: Dynamically scope wsum for --update/--all, prepend summaries to do.md, update spec and cleanup do.md
---

This diff significantly refines the integration of `dtask commit` with `wsum` for work summary generation. The `bin/dtask` script now dynamically adjusts the `wsum` summary scope (staged-only, staged plus unstaged, or all files) to align with the `dtask` command's `--update` or `--all` flags. The logic for inserting these summaries into `docs/dev/work/do.md` has been revamped to prepend new summaries at the beginning of the `# Work Summary` section, ensuring recent work is always at the forefront and avoiding redundant headings. Supporting documentation in `docs/dev/spec/dtask-spec.md` was updated to reflect these new insertion rules and `wsum` invocation behaviors, and `docs/dev/work/do.md` was cleaned up to reflect current development progress.
    - the wsum command should only be allowed to take 45 seconds to run. 
        - if not successful in 45 seconds, it should be killed and considered in error.
x - implement the updated specification section to docs/dev/spec/dtask-spec.md called 'dtask using the wsum.py module'

x - dtask should always save and commit do.md
    use case:  
    The do.md file now grows with the work summary for intermediate commits on a feature.  If te new summary is part of a later commit, the summary from the change to do.md pollutes what actually changed in the subsequent commit.  It is better to includes the do.md work summary updates in te same commit they describe.

d - update dtask to use wsum --update if the user has passed --update to wsum 
 - verify that the python api supports the equivalent to the --update flag. 

d - update dtask to use wsum --all if the user has passed --all to wsum 
 - verify that the python api supports the equivalent to the --all flag flag. 



# Work Summary

## 2026-05-18 13:58

---
workHeadline: dtask: Add --wsum for auto work summary in do.md, refine commit message logic, and auto-stage do.md changes
---

This update to the `dtask` script introduces a new `--wsum` option for the `commit` subcommand, enabling automatic generation and insertion of work summaries into `do.md` using the `wsum` module, complete with a 45-second timeout. The commit message logic has been refined to prioritize `workHeadline` for standard commits and `actualCommitMessage` for `--final` commits. Critically, `dtask` now ensures that any modifications it makes to `do.md`, such as adding work summaries or updating commit messages, are automatically staged for inclusion in the current commit, resolving potential issues with unstaged `do.md` changes.



## 2026-05-18 13:10

---
workHeadline: dtask adds do.md to the commit if it changes.
---

Behavior fix where dtask adds do.md to the commit if it changes in the dtask run.



## 2026-05-18 12:23

---
workHeadline: feat(dtask): update dtask spec for wsum --wsum for work summaries, update docs and TODOs
---

updates the `dtask-spec.md` to mandate a branch for `dtask init` and introduces a new `--wsum` option for `dtask commit`. This new option integrates `dtask` with `wsum.py` to generate work summaries and commit headlines, specifying how these are inserted into `do.md` and handled in commit messages, along with timeout and error handling. Concurrently, the `TODO.md` file has been streamlined by removing completed or superseded tasks related to prior `dtask` enhancements and adding a new task for a `dtask pop` subcommand. Lastly, `do.md` reflects an updated commit message and detailed task breakdowns for the new `wsum` integration.


## 2026-05-16 13:31

---
workHeadline: Enforce dtask work branch in init, mandate do.md commits for history, update tasks for wsum integration, and fix front-matter
---

The `dtask` utility now enforces the requirement of a work branch during the `init` command, with updates to both the script and its documentation to ensure better branch management. In `docs/dev/work/do.md`, the task list was significantly updated to include planned enhancements for `do.md` headings and its integration with the `wsum` module for automated work summaries. The update also adds a requirement for `dtask` to consistently commit the `do.md` file to preserve the history of work summaries across intermediate commits. Finally, minor corrections were made to the `do.md` front-matter to fix typos and reset the current commit state.


## 2026-05-18 17:10

---
workHeadline: `dtask`: Enhance commit with `--wsum` for auto do.md summary generation, refine commit msg, and auto-stage do.md
---

The `docs/dev/work/do.md` file has been updated to reflect the completion of a task concerning `dtask`'s `do.md` commit behavior. A new work summary for May 18, 2026, has been added, detailing enhancements to the `dtask` script. These improvements introduce a `--wsum` option for the `commit` subcommand, automating work summary generation in `do.md` via the `wsum` module with a 45-second timeout. The script's commit message logic has also been refined, and `dtask` now automatically stages `do.md` modifications to ensure they are consistently included in the current commit.


