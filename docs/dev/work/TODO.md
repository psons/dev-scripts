---
"description": "Prioritized development tasks and improvements pending implementation."
"use": "This file is for TODOs that might not get done in the `dtask commit --final` command\
  \ that will remove do.md from the working tree and get into commits for the do.md:workBranch\
  \ that will get merged to a trunk of archive branch."
---

# Misc tasks

# x story: initialize '# Work Summary' header as part of init when do.md is created.
---
"intendedCommitMessage": "resilience improvements for work summary insertion in do.md"    
---
    / - make dtask --wsum wsum behavior resilient to missing '# Work Summary' header in do.md by defaulting to inserting before any '## YYYY-MM-DD hh:mm' header
    / - if there is no '# Work Summary' header in do.md and no '## YYYY-MM-DD hh:mm' headers, create the '# Work Summary' header and insert the new work summary after it. 

    / - move the creations of the '# Work Summary' heading in do.md to the init command.
    - it should always be there, to make tings easier if a manual wsum is added.




 