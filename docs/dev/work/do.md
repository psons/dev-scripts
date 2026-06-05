---
"actualCommitMessage": "dtask: Prioritize `workHeadline` from `do.md`'s `# Work Summary`\
  \ for commit messages; add parser, update tests & docs"
"description": "A list of small, focused tasks guiding the current commit with detailed\
  \ microsected activities."
"intendedCommitMessage": "resilience improvements for work summary insertion in do.md"
"priorCommit": "5ffe34cafe66c0f60da4e44d95562cbda81885de"
"title": "do.md"
"workBranch": "work-summary-do"
"workHeadline": "feat: wsum.py quotes and escapes workHeadline in do.md as single-line\
  \ YAML using JSON encoding, improving parsing; updates specs"
---



# / story: simple commit message enhancements.
 - workHeadline should not be a file frontMatter attribute
 - if there is no workSummary available at all, use the same actualCommit message logic as --final
 - if there is any work summary with a workHeadline, use the latest one (which should be at the top of the #w Work Summary section)


x - figure out: do I really want to use yaml rules for section attributes and task attributes, or would I rather have the more permissive tlog rules?
for now the workHeadline should be handled as section frontmatter to get on with this story without dgessing int o the task popping story.
Later, I expect to make a task and story parser that has a simpler more tolerant way of writting attributes in tasks and stories.

x - write docs/dev/spec/wsum-module-spec.md '## Enhancements for workHeadline as quoted YAML frontmatter 2026-06-03' to feed a prompt.
prompt: do the section docs/dev/spec/wsum-module-spec.md '## Enhancements for workHeadline as quoted YAML frontmatter' and provide unit tests as needed in tests/test_wsum_unit.py.

/ - write '## Enhancements for workHeadline in do.md work summaries and commit messages 2026-06-04' in docs/dev/spec/dtask-spec.md to feed a prompt.
prompt: do the section '## Enhancements for workHeadline in do.md work summaries and commit messages 2026-06-04' in docs/dev/spec/dtask-spec.md, and update BDD tests as needed.


x - bug fix: Work headline not quoted in the do.md work summary to be valid section frontmatter.

/ - bug fix: commit wants the workHeadline to be file frontmatter instead of reading it from te lates subsection under '# Work Summary'.

    when: uses: $ dtask commit -u
        Error: workHeadline is empty. Use --wsum to generate it, or set workHeadline in do.md.

        commit_message = frontmatter.get("workHeadline", "").strip()
        if not commit_message:
            print(
                "Error: workHeadline is empty. Use --wsum to generate it, or set workHeadline in do.md.",
                file=sys.stderr
            )



# x story: initialize '# Work Summary' header as part of init when do.md is created.
prompt: implement '## Enhancement for '# Work Summary' 2026-06-04' in docs/dev/spec/dtask-spec.md, and add BDD tests as needed to the existing dtask commit wsum and init scenarios.

/ - make dtask --wsum wsum behavior resilient to missing '# Work Summary' header in do.md by defaulting to inserting before any '## YYYY-MM-DD hh:mm' header

/ - if there is no '# Work Summary' header in do.md and no '## YYYY-MM-DD hh:mm' headers, create the '# Work Summary' header and insert the new work summary after it. 

/ - move the creations of the '# Work Summary' heading in do.md to the init command.
    - it should always be there, to make tings easier if a manual wsum is added.

# Work Summary

## 2026-06-04 21:43

---
workHeadline: "dtask: Prioritize `workHeadline` from `do.md`'s `# Work Summary` for commit messages; add parser, update tests & docs"
---

The `dtask` script has been updated to change the source of commit messages, now prioritizing the `workHeadline` found within the `# Work Summary` section's frontmatter in `do.md`. A new function, `extract_commit_message_work_headline`, was added to `bin/dtask` to parse this specific region for the topmost valid `workHeadline`, effectively deprecating the use of `workHeadline` in the file's main frontmatter for commit message generation. This shift is thoroughly documented in `dtask-spec.md`, outlining the new precedence rules for `dtask commit` with and without `--final`. The changes are validated by updates to existing BDD tests and the addition of a new scenario in `tests/features/dtask/commit_no_wsum.feature` and its corresponding Python test, ensuring the correct extraction and application of the work headline.
## 2026-06-04 20:01

---
workHeadline: "feat: wsum.py quotes and escapes workHeadline in do.md as single-line YAML using JSON encoding, improving parsing; updates specs"
---

This update enhances the `wsum.py` script to ensure that the `workHeadline` in generated `do.md` work summaries is correctly quoted and escaped as a single-line YAML scalar using JSON string encoding. This change resolves potential parsing issues for headlines containing special characters, aligning with new specifications in `dtask-spec.md` and `wsum-module-spec.md` for proper YAML frontmatter. Corresponding unit tests in `test_wsum_unit.py` have been added or updated to verify this new quoting and escaping behavior, improving the robustness of work summary generation. The `do.md` and `TODO.md` files reflect these changes with new tasks and bug fixes related to `workHeadline` handling and commit message generation.
## 2026-06-04 18:08

---
workHeadline: feat(dtask): Enhance work summary insertion, guarantee # Work Summary header in new do.md, add BDD tests
---

The `dtask` command's work summary insertion logic in `bin/dtask` has been enhanced to be more resilient when the `# Work Summary` header is missing from `do.md`. The system now intelligently inserts this header before any existing dated summaries or appends it to the end of the file if no summaries are present. Furthermore, the `dtask init` command now ensures that newly created `do.md` files always include the `# Work Summary` heading. Comprehensive BDD tests have been added and existing initialization tests updated to validate these new behaviors, ensuring correct placement and content for work summaries.
