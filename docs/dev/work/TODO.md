
# Work Ordering Decisions

The ability to serialize Markdown Sections to a model to preserve other document content will be addressed to prepare for popping stories out of TODO.md and into do.md.

 - dev-scripts-backlog/stories/d-tlog-and-task-pop-in-dtask.md
 - dev-scripts-backlog/stories/Specify-development-description-format.md
    - references: analysis/proposals/script-ai-friendly-texts.md

# d - story: dtask integration with backlog.py
## limitations and assumptions 
Data in the TODO.md that is not part of a Task or Story will may be lost subject to the progress on support for DDF, todo.md, linking back to backlogs, and placeholders in the backlog.
 - this assumption avoids the need to build document preserving functionality in what I am calling for the future Dev Description Format (DDF). docs/dev/spec/adr/dev-description-format.md

d - early version of dtask pop which does not remove content from the backlog
 - refer to the plugin api in docs/dev/spec/backlog-spec.md 


Pop will remove content from TODO.md, that it writes in do.md.
 - This simplifying assumption avoids the situation where users would see the same object in two files with possibly different state.
 - Take together with the previous assumption, it means state for the TODO list can be manipulated as objects in memory and written back to the TODO.md file in new state.   

d - update dtask with a pop subcommand that reads 1 story by default from backlog.py and inserts it at the top of do.md, below the front-matter.

d - add a '--number (-n) n' option to take more than 1 Story or task object.  
 - possibly don't do this

d - add a --task option to `dtask pop` to just 1 task instead of a whole story.
 - possibly don't do this
 ### analysis
 popping a single task creates focus, whereas seeing the whole story lends context and helps avoid overlap in the way things are written.
 ### judgement 
 favor popping the whole story.  Allow the focus to come via the act of marking a single task as in progress '/', and likely adding prompts or elaboration

# d - Story: bugfix: dtask should allow existing branch with -b
error when backlog-command branch already exists.
 $ dtask init -b backlog-command -i "simple Filesystem based backlog implementation using TODO.md" --dirty
fatal: a branch named 'backlog-command' already exists
Error: git checkout -b backlog-command failed.