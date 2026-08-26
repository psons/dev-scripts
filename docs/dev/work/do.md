---
"actualCommitMessage": "Refactor DDF docs for AI integration; update do.md with story\
  \ ID, DDF parsing details & 'Completed' section"
"description": "A list of small, focused tasks guiding the current commit with detailed\
  \ microsected activities."
"intendedCommitMessage": "wsum.py split out work planning and specification"
"priorCommit": "2916447c0f56ff83cc4756ea77e7541218b2766d"
"title": "do.md"
"workBranch": "wsum-sep-work-spec"
---




# Current work

# x - Story: wsum enhancements for features and to separate work planning.
---
id: 9eb4ee8e-717a-779b-aa31-39af5113c86a-2e2b8f4f
---

# d - Story: task aware do.md parsing
---
id: 91a26399-8297-714a-a897-7495e0fb9e2e-087a353f
---
scripts that use do.md, such as especially wsum should recognize task syntax.
Specifically, wsum, should be able to recognize changes in task status.  Perhapse a script can generate a summary of task changes?
    this would be examining previous task status against current task status; parsing the git diff output, or actually reading the file from the prior commit, and comparing the task statuses... I do not think this is what I really want.  
     - (longer term)It would be good to know the elaboration;the improvement in task definition
     - (shorter term) I just want the work summary to stop confusing work actually done from work plan definition.
Prerequisite, do.md parsing should be as mdgbdf and wsum should recognize task status changes in do.md

depends on parsing do.md as DDF to objects.  

# Completed work

x - finalize the pop-doc feature, and do the wsum enhancement story below.
---
id: 2e684872-603d-7142-978b-4b3f0cdc7b26-ba07e445
---

x - improve wsum to keep work planning, specification, separate from everything else.
---
id: bafda5c9-ae5f-7503-af80-68079a558b51-359d55b7
---
prompt...
update the spec docs/dev/spec/wsum-module-spec.md for wsum.py with an enhancement section to improve the full work summary to separate 3 areas of change:
        work planning - files under docs/dev/work
        specification - files under docs/dev/spec
        implementation - everything else

    Any of the areas of change may be have no content to summarize, so that part of the full summary should be silently omitted.

    The workHeadline should include elements of all 3 areas.
    additional quoted YAML front-matter attributes should be provided if the areas have any changes:
        specChanges is a single line summary of the specification changes.
        workChanges is a single line summary of the work planning.


# Work Summary

## 2026-08-26 07:17

---
workHeadline: "Refactor DDF docs for AI integration; update do.md with story ID, DDF parsing details & 'Completed' section"
specChanges: "DDF documentation has been refactored, replacing `dev-description-format.md` with `script-ai-friendly-texts-development-description-format.md` to define DDF's integration of fast scripts with AI specification files, and `spec-mechanics-with-ddf-and-skills.md` introduces DDF's role in templating AI skill output for structured development workflows."
workChanges: "`TODO.md` was formatted by removing a blank line, while `do.md` had a story identifier changed from 'd' to 'x' for \"wsum enhancements,\" with new text added to distinguish work from work plan definitions and a DDF parsing prerequisite, and a \"Completed work\" section created to move an existing task."
---

**Work Planning**: The `TODO.md` file saw a minor formatting adjustment with the removal of a blank line. More significantly, the `do.md` file was updated to change a story identifier from 'd' to 'x' for "wsum enhancements." This story was further elaborated with new text clarifying the need to distinguish between actual work and work plan definitions, and a prerequisite for parsing `do.md` as DDF. Additionally, a new "Completed work" section was added to `do.md`, and an existing task related to finalizing the pop-doc feature and wsum enhancement was moved into this new section.

**Specification**: The Development Description Format (DDF) documentation has been refactored, removing the `docs/dev/spec/adr/dev-description-format.md` file in favor of an updated and more comprehensive definition. The file `docs/dev/spec/adr/script-ai-friendly-texts-development-description-format.md` now clarifies DDF's role in integrating fast scripts with AI-driven specification files, balancing AI flexibility with formal SDLC processes. Additionally, a new document, `docs/dev/spec/usecases/spec-mechanics-with-ddf-and-skills.md`, introduces how DDF will facilitate templated AI skill output to ensure structured, consistent, and easily reviewable content within development workflows.


## 2026-08-17 17:56

---
workHeadline: 

specChanges: "`wsum-module-spec.md` was updated, enhancing `wsum.py` to categorize content changes into \"Work Planning,\" \"Specification,\" and \"Implementation\" areas, generate YAML front-matter with `specChanges` and `workChanges` summaries, and create a comprehensive `workHeadline` reflecting all categories."
workChanges: "Active `wsum` enhancements and task-aware `do.md` parsing work items were migrated from `TODO.md` to a new `do.md` file, now featuring YAML front-matter for commit message generation and outlining current `wsum-sep-work-spec` branch progress, to separate immediate work from the long-term backlog."
---

**Work Planning**: The active work items, including stories for `wsum` enhancements and task-aware `do.md` parsing, have been migrated from `TODO.md` to a newly created `do.md` file. This change aims to separate long-term backlog items in `TODO.md` from immediate, detailed work planning for the current commit, which will now reside in `do.md`. The new `do.md` file includes YAML front-matter to support commit message generation and clearly outlines the current work in progress for the `wsum-sep-work-spec` branch, facilitating a more structured development workflow.

**Specification**: The `wsum-module-spec.md` file has been updated to introduce significant enhancements for the `wsum.py` script. The key changes involve refining how work summaries are generated, requiring `wsum.py` to categorize content changes into "Work Planning" (for `docs/dev/work`), "Specification" (for `docs/dev/spec`), and "Implementation" (for all other files). Additionally, the YAML front-matter generated by `wsum.py` will now include `specChanges` and `workChanges` attributes, providing single-line summaries for changes within their respective areas, if applicable. The main `workHeadline` will also be a more comprehensive synthesis reflecting changes across all three categories.

**Implementation**: The `wsum.py` script has been significantly enhanced to provide more granular and informative work summaries. Key changes include the introduction of `WorkSummaryResult` fields for `work_changes` and `spec_changes`, enabling the generation of distinct single-line summaries for changes in `docs/dev/work/` and `docs/dev/spec/` directories, respectively. The script now categorizes `git diff` output by file path into 'work', 'spec', and 'implementation' sections. These categorized diffs are then used to generate individual summaries, which are combined into a comprehensive full summary and a synthesized headline. The `render_markdown` function has also been updated to incorporate these new categorized summaries into the generated markdown output.