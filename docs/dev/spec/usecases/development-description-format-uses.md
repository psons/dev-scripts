
# DDF usa and support in mdgbdata.py

## Dtask POP use case
Read do.md into memory as a DDF document.  Also read a TODO.md into memory as a DDF document.  Extract the the top story from TODO document and insert it into do document.  Write both files back to disk as DDF text.

Succeed if there is a story written to do.md to work on.
If TODO.md does not exist raise an error that there is no queue to pop stories from.
If do.md does not exist raise an error that there is no do.md file to hold popped stories. 
### mdgbdata.py requirements
read a markdown document to the full DDF model and return the model to a calling module as  


# Higher level context: DDF High level usage possibile usage /

DDF Documents may be gin with simple descriptions, but evolve as a project become better defined and gets built and run.
- there should be a refinement of them into more precise specifications and prompts that can be fed to AI.
- they are a beginning of the relationship between:
    - ideas and problems
    - elaborations to begin building ideas and solving problems.
        - user cases and needs traceable to the ideas and problems. (with review and feedback to the ideas and problems)
    - tasks and specifications
        - specifications describe the things to be built.
        - tasks describe work to build specs and work to implement them.
            Elaborations or refinements of tasks can be prompts.
        - Tests are defined from them to prevent revisions from mangling the original intent.
    - working generated code
        - user acceptance (with review and feedback to the ideas and problems)

A big benefit of Markdown Dev Description Format is that AI friendly markdown documents evolve into a format where scripts that are cheaper to run and faster shoulder a lot of load (avoiding wasteful use of AI tokens) and bring efficiency to development processes.
