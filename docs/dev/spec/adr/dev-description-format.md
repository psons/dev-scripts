A syntax for Development Description Format will be created per docs/dev/spec/adr/proposals/script-ai-friendly-texts.md

# goals

Allow simple to writing of attributes in stories and tasks in MDGBDF without forcing them to use Section front-matter.
 - see docs/dev/spec/mdgbdata-spec.md

Serializing the gbdata model will write more formal MDGBDF pulling all the attribute definitions into section front-matter.

An extension of mdgbdata.py (Same script with more functionality and maybe a new name like mdddf.py) should be built that treats top level sections as a simple Markdown "DOM" that
    - Also keeps the sections that are not stories
    - adds link objects with title and link to th IDs of stories and task (sort of like the google doc chips)