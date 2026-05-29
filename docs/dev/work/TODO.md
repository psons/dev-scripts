---
"description": "Prioritized development tasks and improvements pending implementation."
"use": "This file is for TODOs that might not get done in the `dtask commit --final` command\
  \ that will remove do.md from the working tree and get into commits for the do.md:workBranch\
  \ that will get merged to a trunk of archive branch."
---


## story: Python BDD skill 
d - ask copilot to create an AI skill to generate BDD feature files for pytest-bdd
    - skill: generate BDD feature file from usage situation  and spec
    - using the file layout and other instructions for a generalized version of docs/dev/spec/testing-tools/test-tools-spec.md
    - using the app specific file use case for the next use case that isn't generated yet amongst the use cases under under a subsection of docs/dev/spec/usecases/dtask-and-do-file-tasks.md:'# usage situations'
    - given the spec for the app such as docs/dev/spec/usecases/dtask-and-do-file-tasks.md.
    - this workflow should assume the dtask command does not support the feature yet.


d - Tech tests: Fill in tests for implementation behaviors and prevent future breakage



# Misc tasks
Try to get a testing framework before too may real changes

d - move the creations of the '# Work Summary' heading in do.md to the init command.
    - it should always be there, to make tings easier if a manual wsum is added.

d - bug fix: using the --workbranch switch might not in some case be checking out the newly created branch.

d - bug fix: Work headline not quoted in the do.md work summary to be valid section frontmatter.

d - bug fix: commit wants the workHeadline to be file frontmatter instead of reading it from te lates subsection under '# Work Summary'.

    when: uses: $ dtask commit -u
        Error: workHeadline is empty. Use --wsum to generate it, or set workHeadline in do.md.



        commit_message = frontmatter.get("workHeadline", "").strip()
        if not commit_message:
            print(
                "Error: workHeadline is empty. Use --wsum to generate it, or set workHeadline in do.md.",
                file=sys.stderr
            )

 