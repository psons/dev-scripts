# Full Manual do.md
The do.md file started as a place to write down te current task and thought about how to get it done.

Pasting the task into a file that might not even be saved when the task was done became a useful lace to jot down some more detailed thoughts, or 
do some module design or pseudo code.  

It evolved to a place to jot down clearly what was not in the current task, but the next task in order to kep focus, without loosing clear thoughts that would be needed soon.   Jotting those thins down helps put them out of mind with confidence that they aren't lost, and clarify the flow between tasks.

It seemed like information about a few near at hand tasks was good to have for context.  Also 

# Tool help.
As tools were developed a few common development practices could benefit from bits of information about what is being worked on.  Also, with AI, frequent source commits to some restorable known state became important, and it emerged that a relationship between commit messages and the planned task was a nice idea.  Write the commit message first seemed like a useful idea.  Immediately it became clear that there was always new clarity when the work was done and a better commit message could be written.  The difference between the intendedCommit message and the actual commit message often shows user learning over a tiny work increment.

The dtask command became a tool to simplify frequent commits using frontmatter settings to optionally use a pre set commit message.

A simple obvious AI opportunity to provide the commit message and track completed changes was implemented with the wsum module and the --wsum option of dtask. 

Incorporating tasks into the workflow that already included a feature branch and frequent commits came with the backlog protocol and plugin API to integrate with issue systems, and by default a simple TODO.md file with stories and tasks is provided.

The result is evolving simple command tool to support a common story and feature work flow connected to tasks, commits, and facilitated AI usage.

For detail, see documentation on the 
 - DDF (Development Description Format) and MDGBDF (Mark Down Goal Blotter Data Format)