---
"description": "Prioritized development tasks and improvements pending implementation."
"use": "This file is for TODOs that might not get done in the `dtask commit --final` command\
  \ that will remove do.md from the working tree and get into commits for the do.md:workBranch\
  \ that will get merged to a trunk of archive branch."
---

x - Tech tests: Fill in tests for implementation behaviors and prevent future breakage
    - What is he best way to discover the need for such tests?  Run coverage?


# Misc tasks
Try to get a testing framework before too may real changes

d - move the creations of the '# Work Summary' heading in do.md to the init command.
    - it should always be there, to make tings easier if a manual wsum is added.


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

# story: BDD process
d - update ai/skills/pytest-bdd-from-command/SKILL.md so that it runs successfuly for commands that have not been implemented yet.
 - a  goal is to use the spec to run BDD prior to implementation.
 - currently the skill has a quality gate that says: "- Generated tests pass locally with pytest."
    When BDD happens before implementation, this quality gate has to be deferred to be part of the implementation step.


 