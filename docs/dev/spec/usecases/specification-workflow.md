# Goal
Specify software as efficiently as possible, leveraging AI,
with minimal exposure to AI generated errors.

# Approach
 - The spec is authoritative for context and user behaviors.
 - The tests are authoritative for technical implementation.

## Init
Initialize a feature branch with previous work if any committed and pushed remotely (use dtask init -b).
    - include --intended <message> as a concise statement of what the feature work is

## Context step
Provide context (docs/dev/spec/usecases) about the big picture of what the user is doing to help AI correctly extrapolate and fill in blanks,
which is something it should be good at and where there is value add, allowing humans to leave out some detail.

Make a Git commit. (dtask commit --wsum)
 - wsum might say more about the files that have been modified than what the meaning is to the user
    - there is an opportunity to learn to write better context, 
    - and also to improve te prompt instructions that wsum has. 

## User specs and tests
Specify how the user interacts specifically with the software.
    - make a git commit within the feature
    - Ask AI to write the tests, 
        - but review to ensure that they are correct.

With tests written, AI should implement the code and pass the tests.

## Build phase
Solidify any extrapolation or interpolation tha may have occurred.
    - based on review, correct or redirect anything that is problematic.
        - iterate and do dtask commits as needed

## Tech tests.
 - Ask AI and or Pytest to fill in tests for the implementation behaviors that may have been filled in by AI based on its ability to extrapolate.
 - these tests are needed to prevent breakage in future iterations.

# Skill development
This file describes a workflow of the human tasks interacting with and reviewing AI tasks.

A skill can be built up around the prompt:
```
stub a few "do" tasks into docs/dev/work/do.md according to the activities in docs/dev/spec/usecases/specification-workflow.md.  The stub tasks should use the notation in docs/dev/spec/usecases/story-task-parsing.md and will be expanded by the user to describe the work for the feature with the same name as the workBranch in docs/dev/work/do.md
``` 