
# d - Story: dtask \--final should move all stories in the ‘do.md\#current work’ section that are not completed, back into TODO.md.
---
id: e8f82a4e-19cd-7b91-acf5-c3797e7dc7fa-b3bfd5aa
estimate: 4p
---

Just at the top for now. This can mess up a DDF document a little because it will take work stories out of the document, but only put them back at the top, which may not be where they came from.   But if pop is taking them out of the DDF doc, it is getting ripped apart anyway.   This can be fixed when there are markers in the DDF doc.

d \- build a dtask unpop subcommand and module capability to:  

- get the current work stories after ‘\#current work’ and before ‘\#completed work’  
- load TODO.md as mdgbdata  
- prepend the tasks to the TODO story list in memory, and write it back


# d - Story: Document things - Doc a feature lifecycle
---
id: 3255d54d-3700-7327-80a9-485eea97677c-25e2ae98
estimate: '2p  '
---
in user docs.  
In a typical development environment, a developer:

* creates a git branch representing a feature.  
* does several commit on the feature branch  
* which maybe iterations of the ‘Task, Spec, and Prompt’ work flow, including results review.  
* Does UAT, and merged back into the ‘main’ branch.

d - address TODOs in user docs docs/user/feature-workflow/f-w-process.md

d - Write AI controls user process documentation.
    see docs/user/ai-knowledge-skills/ai-k-s-process.md
        ### Specification ad Control Structures around AI
        TODO write this section to honor a link from docs/user/feature-workflow/f-w-process.md

# d - Story: Work on stuff \- improve dtask to support a full feature life cycle per the documented work flow
---
id: 17438af7-a350-71ff-a4f2-f1a9e3f99f81-268d874b
---
requires
 - dtask -- final improvement do.md back to TODO.md  
 - Story: Document things - Doc a feature lifecycle

d - dtask init captures the original branch into front-matter as a default to merge back to.
---
id: 579a01ed-abbe-7217-a81a-e48a522d698d-236a3170
---
	d - spec  
	estimate: 2p  
	d - run prompt and review  
	estimate: 1p  
	d - extra iteration to fix  
	estimate: 2p

d - merge the feature branch back to main
---
id: 4cf320f7-214e-7c06-a52f-9b03019bfca2-fdb24a20
---
 At this point, \--mergeback \<branch\> would be a command allowed with \--final, or it could be a front-matter attribute managed similar to the “actual commit message” which uses the front-matter value, but can be overridden with command line.  
	d - spec  
	estimate: 2p  
	d - run prompt and review  
	estimate: 1p  
	d - extra iteration to fix  
	estimate: 2p


# d - Story: bugfix: dtask should allow existing branch with -b
---
id: 140748b0-1c3f-79e4-bb30-b20a7c8de67f-d89c4805
fatal: a branch named 'backlog-command' already exists
Error: git checkout -b backlog-command failed.
---
error when backlog-command branch already exists.
 $ dtask init -b backlog-command -i "simple Filesystem based backlog implementation using TODO.md" --dirty


# d - Story: Document things \- Do prerequisites.
---
id: cd73dbad-9938-7298-a21d-c1f51e208296-af4f93fc
---


# / - Story: Document things \- Create a README that points to user docs
---
id: 5630f069-1e53-7620-bdf4-47657822a6c3-391f807e
---
without the non included things, but with a bin index, and higher level "applicability" info than the common help statements.

This may be complete based on docs/dev/spec/user-documentation-structure.md

# d - Story: Document things \- Do User Docs for all included script pieces
---
id: 3a75ebb3-0db9-7a52-8321-c59cac40676e-e6481463
estimate: '22p  '
---
for each capability of each included piece.

* 8 big pieces of dtask suite  
* 1 big piece of clean\_node\_modules  
*  overall \+ 3 sm pieces \- ../enable\_env\_local.sh (3 small pieces)  / helper functions (2 small pieces)


# d - Story: Document things \- Doc a Task Spec and Prompt Workflow
---
id: b5404589-f376-78c0-9062-86690d242bbb-be2a6b98
estimate: 1p
---
d \- 1 paragraph user doc explaining Task, Spec, and Prompt work flow.  


# d - Story: Document things \- Doc task and story syntax
---
id: d6235bf1-0a8b-7fac-9b85-fbe214135539-045edcbb
estimate: '2p '
---
d \- AI to extract from some relevant docs  


# d - Story: Document things \- Doc the bltodo flow around TODO.md and do.md,
---
id: ec63f72b-9071-75f1-95fe-8bdb337aca32-bc980987
estimate: '1p  '
---
in principle, and with a lead to dtask help

d - update use case documentation per comment in the google doc version of the spec.
---
id: 679a9b93-40dd-7dce-9171-207e9b01075f-088efbc0
---
     - is it docs/dev/spec/mdgbdata-spec.md
     from spec:
     ##### Summary of Round trip handling of the story marker.
        ...
            story marker is not lost on stories, even though the story marker is not stored internally. 
        - The comment is: 
            This should be added to a use case source and get into user documentation if it isn't already.
            It is important for fast story capture, without the need to write in a story status, but to assure that the bltodo.py backlog plugin will pop stories that need elaboration and tasks identified.

d - update help text in bltodo.py
---
id: fc55f6f0-4b0a-7552-b765-c98b69275bdc-3546b48d
---
 - bltodo.py has knowledge of work queue management and is closer to the user, whereas mdgbdata.py is just a parser / serializer.
    - Text in the TODO file will be ignored for heading sections that do not represent work stories. 
 - users would interact with mdgbdata.py rarely if ever.


# d - Story: improve project directory structure user docs
---
id: f056719b-2221-7ff9-b3c8-e88dd19765eb-6681d6ea
---

d - create a story that allows a project directory structure to be defined as a series of environment exports.
---
id: 36177175-b1fc-7e9c-a746-aa19569fa116-8f65d6bf
---
 - create an example file.
 d - start by documenting my default project tree
 - there should be a series of env exported names to define all the real locations that the tools in this suite use.
    - this gives rise to two approached:
        1 - scheme to find project root (based on git by default) and use default relative paths
        2 - piecemeal scheme to absolutely define locations, or craft a layot with sever user provided base locations used to set the official script supported paths from, #1. 

