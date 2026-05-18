---
description: Prioritized development tasks and improvements pending implementation for the TaskForm application.
---



# branch strategy enhancements story.

d - build out tool specs to support ../spec/usecases/dtask-branch-enhancements-1-spec.md 
 - [proposed-branching-strategy.md](../spec/usecases/proposed-branching-strategy.md)
 - based on docs/dev/spec/usecases/branch-strategy-request.md
 
# Archive worksum story
d - remove the summary-message command and the worksum command, and their specs.
 - use dtask and a do.md file to explicitly mention them in a commit message for the last commit to include them.

# Story: Implement dtask pop sub command 
d - generate a spec in the section called '# pop subcommand'
 - by default reads the first task found in the TODO.md file in the same directory as the do.md file.
    - if a --story switch is given, the first whole story markdown stoey section including all of its tasks and any other text are read
 - The story and task material read from TODO.md is added to do.md after the initial frontmatter at the top of the file
 - The story and task lines material added to do.md are removed from TODO.md
 -  Stories and tasks are to be identified in files according to docs/dev/spec/usecases/story-task-parsing.md

   
