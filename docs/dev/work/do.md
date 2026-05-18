---
actualCommitMessage: test message
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

d - implement dtask enhancements to integrate with the work with wsum module.
 x - generate an updated specification section to docs/dev/spec/dtask-spec.md called 'dtask using the wsum.py module'
    - add a --wsum option to invoke the wsum command to update the work summary in do.md, including the workHeadline: frontmatter
    - change default behavior for commits without the --final option to use the workHeadline as the commit message. 
    - add documentation that to say that '--final will use the actual commit message behavior (as already implemented), including the existing implementations of --actual (and -a) 
    - if wsum errors, try to communicate the wsum error, and suggest the user provide a manual summary and 'actualCommitMessage:' in do.md
    - add a header '# Work Summary' to do.md before adding the work summary if this is the first work summary being added to do.md.
    - the wsum command should only be allowed to take 45 seconds to run. 
        - if not successful in 45 seconds, it should be killed and considered in error.
 d - implement the updated specification section to docs/dev/spec/dtask-spec.md called 'dtask using the wsum.py module'

d - dtask should always save and commit do.md
    use case:  
    The do.md file now grows with the work summary for intermediate commits on a feature.  If te new summary is part of a later commit, the summary from the change to do.md pollutes what actually changed in the subsequent commit.  It is better to includes the do.md work summary updates in te same commit they describe.

# Work Summary

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

