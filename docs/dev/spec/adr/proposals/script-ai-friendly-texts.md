Development Description Format should be a human author friendly text convention on top of Markdown to synthesize what do.md is being used for and TODO.md is bing used for (writing stories and tasks).

Perhaps this consists of a tolerant parsable spec for MDGBDF. with a more formal syntax that can be parsed with slight extensions of existing Markdown and YAML libraries.


The idea is tha  when writing markdown documents for specs and other things, stories and tasks can be included inline.

Stories and tasks may include properties or attributes, ad if it looks like a property or attribute, it an a property or attribute. it would be nice to avoid building a whole new parsing and escaping language, but also support the rich capabilities of YAML, and ultimately be able to get to the object model of gbdata.py, and formally serialize as JSON.

A big philosophical question come in as to how to deal with those original documents that stories and tasks came out of.   Going forward do we maintain them, and keep them connected with the stories and tasks? 

    - there should e a refinement of them into more precise specifications and prompts that can be fed to AI.
    - they are a begining of the relationship between:
        - ideas and problems
        - elaborations to begin building ideas and solving problems.
            - user cases and needs traceable to the ideas and problems. (with review and feedback to the ideas and problems)
        - tasks and specifications
            - specifications describe the things to be built.
            - tasks describe work to build specs and work to implement them
                Elaborations or refinements of tasks can be prompts.
         - tests to prevent revisions from mangling the original intent.
        - working generated code
            - user acceptance (with review and feedback to the ideas and problems)

A big benefit of Markdown Dev Description Format is that AI friendly markdown documents evol;ve into a format where scripts that are cheaper to run and faster shoulder a lot of load, and bring efficiency to development processes.

# Action from this
Allow simple to type attributes in stories and tasks in MDGBDF without forcing them to use Section front-matter.

Serializing the gbdata model will write more formal MDGBDF pulling all the attribute definitions into section front-matter.

An extension of mdgbdata.py (Same script with more functionality and maybe a new name like Mdddf.py) should be built that treats top level sections as a simple Markdown "DOM" that
    - Also keeps the sections that are not stories
    - adds link objects with title and link to th IDs of stories and task (sort of like the google doc chips)