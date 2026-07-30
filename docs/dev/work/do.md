---
"actualCommitMessage": "groom backlog for dtask pop and unpop work"
"description": "A list of small, focused tasks guiding the current commit with detailed\
  \ microsected activities."
"intendedCommitMessage": "dtask(Feat) to rm popped stoies from backlog, but put unfinished\
  \ work back when --final"
"priorCommit": "f3412883272fe6ab6df7a4973fefe14f388d7ecd"
"title": "do.md"
"workBranch": "pop-n-unpop"
---


# Work Summary
# Work Ordering Decisions

The ability to serialize Markdown Sections to a model to preserve other document content will be addressed to prepare for popping stories out of TODO.md and into do.md.

 - dev-scripts-backlog/stories/d-tlog-and-task-pop-in-dtask.md
 - dev-scripts-backlog/stories/Specify-development-description-format.md
    - references: analysis/proposals/script-ai-friendly-texts.md

# x - story: dtask integration with backlog.py
x - early version of dtask pop which does not remove content from the backlog
    x - update dtask with a pop subcommand that reads 1 story by default from backlog.py and inserts it at the top of do.md, below the front-matter.
    - refer to the plugin api in docs/dev/spec/backlog-spec.md 
        / - update the spec docs/dev/spec/dtask-spec.md
         - [dtask spec](../spec//dtask-spec.md#pop-subcommand)
        / - update the program.
        prompt: implement the pop subcommand per ../spec//dtask-spec.md#pop-subcommand.


a - add a '--number (-n) n' option to take more than 1 Story or task object.  
 - possibly don't do this

a - add a --task option to `dtask pop` to just 1 task instead of a whole story.
 - possibly don't do this
 ### analysis
 popping a single task creates focus, whereas seeing the whole story lends context and helps avoid overlap in the way things are written.
 ### judgement 
 favor popping the whole story.  Allow the focus to come via the act of marking a single task as in progress '/', and likely adding prompts or elaboration

## limitations and assumptions 
Data in the TODO.md that is not part of a Task or Story will may be lost subject to the progress on support for DDF, todo.md, linking back to backlogs, and placeholders in the backlog.
 - this feature avoids the need to build document preserving functionality.  The document preserving  in what I am calling for the future Dev Description Format (DDF). docs/dev/spec/adr/dev-description-format.md


# x - story: mdgbdata.py or bltodo.py should only return work stories 
 - presently, stories tagged with the string "story:" are not considered work stories if they do not have a status or tasks. 
    - need to reverse this decision, but make sure text stories do not get flagged as 'story:'
        - do it by adding a status if the story marker is present.
x - update the spec withe respect to the rules for round trip handling of the story marker.
x - update the program
prompt: update mdgbdata.py per the updated spec docs/dev/spec/mdgbdata-spec.md, particularly to treat headings with the story marker as work stories.
x - implement an flag so bltodo can ask for only work stories
    - the logic for identifying work stories should stay encapsulated in mdgbdata.py
    - bltodo.py will use the flag to filter stories, for popstory
    - later when bltodo.py will update a story, it should be done by ID so that the distinction of being a work story does not matter.
    x - update the spec docs/dev/spec/mdgbdata-spec.md
    x - update the program mdgbdata.py per the updated spec docs/dev/spec/mdgbdata-spec.md
    x - update the program mdgbdata.py per the updated spec docs/dev/spec/mdgbdata-spec.md for the new 'Command line Requirements' to support the new --work subcommand
    x - update the docs/dev/spec/mdgbdata-spec.md to require that the help subcommand shows all subcommand and subcommand options.
    x - per the updated spec docs/dev/spec/mdgbdata-spec.md for the new 'Command line Requirements' update the help subcommand behavior

###
# x - Story: Estimate and plan
---
id: b7b8d03d-2885-7def-8ea0-c441ffd6256b-9de46822
estimate: 3:p
---
x - rough define and swag everything  

