# Development Project Setup

Navigation:
- [User Docs Home](../README.md)
- [Node JS Based Development](../node-js-development/README.md)
- [Firebase Project Development](../firebase-development/README.md)
- [Feature Based Work Story and Source Commit Workflows](../feature-workflow/README.md)
- [AI Knowledge Indexing and Skills](../ai-knowledge-skills/README.md)

## Activities Currently Facilitated

- Initialize and track task-focused do.md workflow on a work branch, including --dirty and --newdo safety behavior (see [dtask-and-do-file-tasks](../../dev/spec/usecases/dtask-and-do-file-tasks.md) and [using-do](../../dev/spec/usecases/using-do.md)).
- Pull prioritized stories/tasks from backlog into active work context with dtask pop and provider-backed TODO handling (see [dtask-and-do-file-tasks](../../dev/spec/usecases/dtask-and-do-file-tasks.md), [backlog-usage](../../dev/spec/usecases/backlog-usage.md), and [todo-usage](../../dev/spec/usecases/todo-usage.md)).
- Bootstrap local shell environment and project stubs with reusable env templates and helper functions.
- Transform line/delimited lists for shell workflows, including command-line tab-completion-friendly saved list patterns (see [tab-completion-lists](../../dev/spec/usecases/tab-completion-lists.md)).
- Preserve in-progress local work by shoving uncommitted changes onto a safety branch for remote backup.

## Candidate Activities To Script Next

- One-command feature open flow that chains branch creation, dtask init, and backlog pop into a single repeatable command (inspired by [proposed-dtask-close-feature](../../dev/spec/usecases/proposed-dtask-close-feature.md)).
- Reusable directory skeleton packaging and restoration for fast project cloning across experiments (from [proposed-dir-skel](../../dev/spec/usecases/proposed-dir-skel.md)).
- Guided task archive workflow for completed story summaries and backlog carry-forward of incomplete work.

## Script and Artifact Index

- [dtask](dtask.md)
- [backlog.py](backlog.md)
- [bltodo.py](bltodo.md)
- [gshove.sh](gshove.md)
- [enable_env_local.sh](enable-env-local.md)
- [.env.local template](env-local-template.md)
- [helperfuncs.env](helperfuncs-env.md)
- [list](list.md)

# maintenance

Update this page with the prompt below:

"Refresh docs/user/project-setup/README.md using current setup and task workflow behavior. Preserve top navigation links, keep activity sections concise, and link to script pages for command-level details."
