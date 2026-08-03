# Feature Based Work Story and Source Commit Workflows

Navigation:
- [User Docs Home](../README.md)
- [Node JS Based Development](../node-js-development/README.md)
- [Firebase Project Development](../firebase-development/README.md)
- [Development Project Setup](../project-setup/README.md)
- [AI Knowledge Indexing and Skills](../ai-knowledge-skills/README.md)

## Activities Currently Facilitated

- Author stories/tasks in markdown with explicit status parsing rules and story inference behavior (see [story-task-status-parsing](../../dev/spec/usecases/story-task-status-parsing.md) and [story-task-parsing-md](../../dev/spec/usecases/story-task-parsing-md.md)).
- Run feature work as a do.md lifecycle: init, iterative commits, work summaries, and final cleanup (see [dtask-and-do-file-tasks](../../dev/spec/usecases/dtask-and-do-file-tasks.md) and [using-do](../../dev/spec/usecases/using-do.md)).
- Carry incomplete feature tasks back to backlog on finalization so unfinished work remains traceable (see [backlog-usage](../../dev/spec/usecases/backlog-usage.md)).
- Use specification-first and test-driven iteration patterns to stabilize AI-assisted feature delivery (see [specification-workflow](../../dev/spec/usecases/specification-workflow.md)).

## Candidate Activities To Script Next

- A higher-level feature open/close command that automates dtask finalization, branch transitions, and next-feature initialization (from [proposed-dtask-close-feature](../../dev/spec/usecases/proposed-dtask-close-feature.md)).
- Branch strategy automation for detailed development history with squashed release history and safe ancestry updates (from [proposed-squash-n-detail-branch-strategy](../../dev/spec/usecases/proposed-squash-n-detail-branch-strategy.md)).
- Policy checks that require story status transitions before final commits, plus structured release-note/changelog generation from story metadata.

## Script and Artifact Index

- [Task Workflow Status Meaning](../task-workflow/status-meaning.md)
- [dtask](../project-setup/dtask.md)
- [backlog.py](../project-setup/backlog.md)
- [bltodo.py](../project-setup/bltodo.md)
- [wsum](../ai-knowledge-skills/wsum.md)

# maintenance

Update this page with the prompt below:

"Refresh docs/user/feature-workflow/README.md from current feature-story and commit workflow behavior. Keep five-area navigation links at the top, preserve DRY references to existing script pages, and keep workflow activities split into facilitated and candidate sections."