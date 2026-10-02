---
"description": "This is an issues document to record open issues, the analysis of te issues, and the accepted Architectural Decisions Record (ADR) to resolve the issues"
---
## issue: What should be done with old '#Current work' 
since dtask settle must clear all content out of the 'do.md # Completed work' section.
and only tasks get copied to the '#Completed work' section text stories and preamble text from completed stories would be lost by dtask settle 
### Thinking:
1st Proposal: 
    dtask final should do 3 commits:
        the first commit is the state when the command is run. it is needed to preserve text of completed stories that will otherwise be lost 
        the second commit is the state of the do.md after a dtask settle, where content might be lost
        the third commit is with do.md removed.
    the background is that an assumption of using the bltodo backlog is that the user does not want the the source tree to get junked up forever with work management, so the content **should** be lost unless a detailed commit branch is kept.

    A problem with that is that simply doing a settle will loose content unless a commit is also done.

2nd proposal:
    Reasoning: saving old stories seems like a logging function that is not needed for the long term, and should be constrained in space it takes up. 

    file recovery can be used to make sure content is not lost. - Save a couple dozen copies of do.md. no need to do anything with the stories themselves.
    The bltodo module has a recovery pattern, but its directory name is overly long and complex, and can be simplified.

3rd proposal:
    actually put the story objects in the '#Completed Work' section.
    A problem with this is that "competed work" is a thin listing of bare tasks.
    Stories only exist as attributes of tasks.
        text stories could be made as fragments of the actual stories.

4th proposal:
    keep completed stories in a subdir and file.
        the subdir can be a sym link to elsewhere or left out of source control if desired. 
        a future feature could include a setting to not keep them.

5th proposal (selected. See decisions):
    dtask settle should perform backlog PushStory.  The bltodo plugin should save completed stories to a stack in docs/dev/work/done/done.md
### Decisions
---
status: accepted
statusNote: more related behaviors are documented in docs/dev/spec/usecases/dtask/dtask-and-do-file-tasks.md
statusDate: 2026-09-22
---
#### For the current iteration
---
status: accepted
statusNote: more related behaviors are documented in docs/dev/spec/usecases/dtask/dtask-and-do-file-tasks.md
statusDate: 2026-09-22
---
dtask settle should perform backlog PushStory.  The bltodo plugin should save completed stories to a stack in docs/dev/work/done/done.md 
    