---
"actualCommitMessage": "Refactor mdgbdata.py: expose API, enhance docs; update backlog-spec,\
  \ refine ADR; add mdgbdata JSON serialization test"
"description": "A list of small, focused tasks guiding the current commit with detailed\
  \ microsected activities."
"intendedCommitMessage": "simple Filesystem based backlog implmentation using TODO.md"
"priorCommit": "78d5d42cbbbd6af41ce6481954b365fc00e33efe"
"title": "do.md"
"workBranch": "backlog-module"
---



# / - story: Pilot a filesystem integration with TODO.md as a task store to start backlog.py and exercise interaction needed with do.md.

x - keep id in story parsing and serialization.
    prompt:
        add support for the id property to mdgbdata.py according to the '# the `id` property.' section of docs/dev/spec/usecases/story-task-parsing-md.md.  The id propert yshould be supported for both parsing and serialization.



x - Update gb-data to include a status in the story type.

/ - write a version of backlog that parses stories and tasks out of a file and loads them into the GB domain model in memory
    x - write a spec to support a building python apps as the command module pattern based on wsum.py.
        - [python-command-module-skill.md](../spec/python-command-module-pattern.md)

/ - define the interface needed for plugins that backlog.py uses
 - docs/dev/spec/backlog-spec.md 
 - [backlog-spec.md](../spec/backlog-spec.md)

/ - finish bltodo.py spec which was started in the backlog spec.
    x - decide if the plugin should have command like capabilities, such as might support more specific behaviors than backlog.py.
        - No. see docs/dev/spec/adr/relationship between CLI and plugin modules.md   
        - refer to the section '# bltodo.py - The default plugin.' in the docs/dev/spec/backlog-spec.md

# Work Summary


## 2026-07-04 16:00

---
workHeadline: "Refactor mdgbdata.py: expose API, enhance docs; update backlog-spec, refine ADR; add mdgbdata JSON serialization test"
---

This update refactors `bin/mdgbdata.py` by exposing several internal helper functions as a public API, including `stories_to_json_text` and `stories_to_markdown_text`, and enhances the module's docstrings for clarity. Correspondingly, `docs/dev/spec/backlog-spec.md` is updated to specify output options (`--mdgbdf`, `--json`) for subcommands and to clarify that the `bltodo.py` plugin will now use the refactored `mdgbdata.py` for markdown operations. Additionally, the `docs/dev/spec/adr/relationship between CLI and plugin modules.md` is refined to better explain the design philosophy for backlog plugins. Finally, `tests/test_mdgbdata.py` includes a new unit test to validate the correct JSON serialization of `Story` objects using the newly exposed `stories_to_json_text` function.
## 2026-07-04 14:29

---
workHeadline: "feat(mdgbdata): Implement explicit story/task ID parsing & serialization with docs & tests"
---

This change introduces explicit ID handling for stories and tasks within the `mdgbdata.py` script. The system now parses `id:` lines that immediately follow story or task headers in Markdown files, overriding any automatically generated IDs. Correspondingly, `mdgbdata.py` now serializes these explicit IDs back into Markdown format directly after their respective story and task headers. Documentation in `mdgbdata-spec.md` and `story-task-parsing-md.md` was updated to clarify these parsing and serialization rules, and new unit tests in `test_mdgbdata.py` validate this functionality, ensuring correct behavior for both valid and invalid `id` placements. The `do.md` and `TODO.md` files were also updated, highlighting this `id` property feature as a key development task.
