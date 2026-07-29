
# Work Ordering Decisions

The ability to serialize Markdown Sections to a model to preserve other document content will be addressed to prepare for popping stories out of TODO.md and into do.md.

 - dev-scripts-backlog/stories/d-tlog-and-task-pop-in-dtask.md
 - dev-scripts-backlog/stories/Specify-development-description-format.md
    - references: analysis/proposals/script-ai-friendly-texts.md


# d - Story: bugfix: dtask should allow existing branch with -b
error when backlog-command branch already exists.
 $ dtask init -b backlog-command -i "simple Filesystem based backlog implementation using TODO.md" --dirty
fatal: a branch named 'backlog-command' already exists
Error: git checkout -b backlog-command failed.