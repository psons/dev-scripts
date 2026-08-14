Navigation:
- [Feature Based Work Story and Source Commit Workflows](README.md)

# Feature Based Work Story and Source Commit Workflows Process Documentation

## Goals of the Feature Based Work Story and Source Commit Workflows Processes

## Goals of the Feature Workflow Processes
#### Mission level goals
 - Enable developers to decompose a desired software feature into small development task that produce a series of git commits
 - Improve focus on exactly the next task, but with the flexibility to assure that it evolves is necessary to is sensibly efficiently aligned with intent of the feature and the bigger picture goals. 
 - encourage a 'specify and generate' work flow that feeds back to improved automation and a consistent project structure.
#### Convenience level goals
 - ease branch creation and management with features
 - Optionally provide visibility to outside work tracking systems (by flexibly plugging into work tracking systems)
 - Connect Features build out, Stories, and source commits in a consistent relationship


### Decomposing tasks and Improving Focus
the dtask command uses a do.md file to facilitate organizing task work so that it has the absolute tip top of the work pile in the same place all the time.  An easy to write extension of markdown and YAML is used as a work blotter to refine and elaborate task descriptions and work to do.

dtask has a 'pop' subcommand that takes a story at a time from the work planning system and writes it with task detail into the do.md file.   The task syntax makes it easy to further write sub tasks and even sub-sub-tasks to clarify at a personal level how to tackle ones own chunk of the work.  As one works, the descriptions of the sub tasks naturally become prompts so that describing the task is a big part of completing the task. 

To reduce clutter and further keep focus, when a feature (or one or more stories, or just a key task) is completed dtask makes a special commit to save the do.md file, and then deletes it to start fresh for the next feature.

dtask has a commit subcommand that wraps gitcommit to generate a reasonable commit message to avoid cognitive load and improve commit messages.  
TODO - there is a backlog item to further improve the messages that wsum.py creates for dtask.
TODO - There is a backlog item to wrap dtask in a "feature based" command that will know about branching strategy and tag the commit when it runs dtask --final.
TODO - a backlog item may exist to support squashing commits from a detailed branch to the main branch on feature completion.
TODO - There is a backlog item to pull the gshove pilot into the "feature based" command to quickly push the branch to a remote for temporarily storage safety.
TODO - a new backlog item is needed to adjust task status in do.md and create a commit.
TODO - there is a new backlog item needed to update a story status and report back to the work tracking system.

- frequent dtask commits and the role of wsum
 - to save local work
 - to represent task completion.

 Refer to [Using do.md](../../dev/spec/usecases/using-do.md)


### Spec(ify) and Gen(erate) flow
Some times a prompt for AI become large and is really a specification.  As this happens it is good to instead write te spec as a file so the [prompt becomes trivially "implement {specFileName}".

A feature then becomes a cycle of just a few generic tasks:  
 - Write the spec, generate the BDD and code, Review results
 - repeat the cycle with refinements
 - commit the feature

 Refer to [Specification and Control Structures around AI](../ai-knowledge-skills/ai-k-s-process.md#specification-and-control-structures-around-ai) for more information.

### Work tracking 
The dtask command uses a plugin architecture so that the simple TODO.md file backlog can be replaced with amn integration with a more sophisticated work tracking system, such as Taskwarrior or Jira.

If desired, the plugins can be used to create visibility to progress, challenges or expanded effort on work. 

TODO - write content if not already covered:
    - Describe the repeatable feature delivery and source-commit outcomes this process is meant to support.
    - Summarize how the scripts and artifacts in this topical area reduce manual task tracking, status drift, or commit-flow mistakes.

## Feature Workflow Process

### pop behavior may differ across plugin implementations.
    bltodo avoids duplicate story maintenance by removing popped stories from TODO.md. Other providers may keep popped stories marked in progress. In both cases, dtask --final unpops incomplete work back into the backlog.


# maintenance

Updates to this page will typically be done manually to explain how the behaviors of the scripts fit into a bigger picture process.


```
Refresh docs/user/feature-workflow/f-w-process.md as a write up of the process to achieve users outcomes.  That process will likely be a blend of use cases and the BDD tests built for them that exercise the the scripts in the same document topical area as docs/user/feature-workflow/f-w-process.md 

Keep a navigation link at the top to the main document for the topical area that this document is a part of.  Maintaining the  DRY principle is less important for this type of document, but link references to existing script pages, should be included for any material that may be partially duplicative.
```