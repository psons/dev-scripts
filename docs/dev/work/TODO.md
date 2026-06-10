---
"description": "Prioritized development tasks and improvements pending implementation."
"use": "This file is for TODOs that might not get done in the `dtask commit --final` command\
  \ that will remove do.md from the working tree and get into commits for the do.md:workBranch\
  \ that will get merged to a trunk of archive branch."
---

# Misc tasks

d - improve the gb-data model to include an attribs dictionary that can hold unvalidated key-value data such as 'prompt: ' frontmatter like attributes for Goals, tasks, and stories.

# / story: Pilot a filesystem integration with TODO.md as a task store to start backlog and exercise interaction needed with do.md.
x - Update gb-data to include a status in the story type.
/ - write a version of backlog that parses stories and tasks out of a file and loads them into the GB domain model in memory
    / - write a generalized spec to support a skill to create a command module pattern based on wsum.py
        - [python-command-module-skill.md](../spec/python-command-module-pattern.md)
/ - define the interface needed for plugins that backlog.py will use:
    - pop task
    - pop story
    - list - dumps out the list of stories as though they were he stories in a Goal object
 

    
d - enhance gbdata to serialize structures as json according to the gb-data schema.

 