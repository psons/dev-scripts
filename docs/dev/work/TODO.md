---
"description": "Prioritized development tasks and improvements pending implementation."
"use": "This file is for TODOs that might not get done in the `dtask commit --final` command\
  \ that will remove do.md from the working tree and get into commits for the do.md:workBranch\
  \ that will get merged to a trunk of archive branch."
---

# Work Ordering Decisions

The ability to serialize Markdown Sections to a model to preserve other document content will be addressed to prepare for popping stories out of TODO.md and into do.md.

 - dev-scripts-backlog/stories/d-tlog-and-task-pop-in-dtask.md
 - dev-scripts-backlog/stories/Specify-development-description-format.md
    - references: analysis/proposals/script-ai-friendly-texts.md

# d - story: dtask integration with backlog.py
## limitations and assumptions 
Data in the TODO.md that is not part of a Task or Story will be lost
 - this assumption avoids te need to build document preserving functionality in what I am calling for te future Dev Description Format. docs/dev/spec/adr/dev-description-format.md

Pop will remove content from TODO.md, that it writes in do.md.
 - This simplifying assumption avoids the situation where users would see te same object in two files with possibly different state.
 - Take together with the previous assumption, it means state for the TODO list can be manipulated as objects in memory and written back to the TODO.md file in new state.   

d - update dtask with a pop subcommand that reads 1 story by default from backlog.py and inserts it at the top of do.md, below the front-matter.

d - add a '--number (-n) n' option to take more than 1 Story or task object.  - possibly don't do this


d - add a --task option to `dtask pop` to just 1 task instead of a whole story.
 - possibly don't do this

# d - Story: bugfix: dtask should allow existing branch with -b
error when backlog-command branch already exists.
 $ dtask init -b backlog-command -i "simple Filesystem based backlog implementation using TODO.md" --dirty
fatal: a branch named 'backlog-command' already exists
Error: git checkout -b backlog-command failed.