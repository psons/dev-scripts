---
"description": "Prioritized development tasks and improvements pending implementation."
"use": "This file is for TODOs that might not get done in the `dtask commit --final` command\
  \ that will remove do.md from the working tree and get int commits for the do.m:workBranch\
  \ that will get merged to a trunk of archive branch."
---


# python testing framework
d - finish saving the gemini web response into the project tree.
d - get an LLM to set up the framework and tools.
d - buils a few tasks in TODO.md to step toward getting a first pyest BDD working.
    d - refine the scaffolding directories. make a few directories perhaps tar'd up to set state.

# Misc tasks
Try to get a testing framework before too may real changes

d - move the creations of te '# Work Summary' heading in do.md to the init command.
    - it should always be there, to make tings easier if a manual wsum is added.

d - bug fix: using the --workbranch switch might not in some case be checking out the newly created branch.

d - bug fix: 

    given: 
    when: uses: $ dtask commit -u
        Error: workHeadline is empty. Use --wsum to generate it, or set workHeadline in do.md.



        commit_message = frontmatter.get("workHeadline", "").strip()
        if not commit_message:
            print(
                "Error: workHeadline is empty. Use --wsum to generate it, or set workHeadline in do.md.",
                file=sys.stderr
            )



# branch strategy enhancements story.
d - build out tool specs to support ../spec/usecases/dtask-branch-enhancements-1-spec.md 
 - [proposed-branching-strategy.md](../spec/usecases/proposed-branching-strategy.md)
 - based on docs/dev/spec/usecases/branch-strategy-request.md
 