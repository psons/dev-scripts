---
"description": "Prioritized development tasks and improvements pending implementation."
"use": "This file is for TODOs that might not get done in the `dtask commit --final` command\
  \ that will remove do.md from the working tree and get into commits for the do.md:workBranch\
  \ that will get merged to a trunk of archive branch."
---

d - rework `backlog prioritized` to keep stories instead of attempting to list tasks without stories.
 - or put the story title and story ID as attributes under the task
    - which might be needed to integrate with taskwarrior.

# d - story: dtask integration with backlog.py
d - update dtask with a pop subcommand that pops a story by default from backlog.py and inserts it at the top of do.md, below the frontmatter.
    d - add a --task option to pop just 1 task instead of a whole story.

# d - Story - bugfix: dtask should allow existing branch with -b
error when backlog-command branch already exists.
 $ dtask init -b backlog-command -i "simple Filesystem based backlog implmentation using TODO.md" --dirty
fatal: a branch named 'backlog-command' already exists
Error: git checkout -b backlog-command failed.