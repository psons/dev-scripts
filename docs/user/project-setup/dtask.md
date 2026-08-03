# dtask

Task-focused git workflow helper centered on docs/dev/work/do.md.

## Usage

```text
dtask - manage git branch and commit messages for the current task

Subcommands:
  help    Print this help message.

  init    Initialize a new docs/dev/work/do.md file for the current task.
          Sets priorCommit to the current HEAD commit hash.

  pop     Insert the top story returned by backlog popstory at the top of
          the '# Current work' section in docs/dev/work/do.md.

  commit  Commit staged changes on workBranch using workHeadline as the commit message.

Core options include:
  --workbranch/-b, --intended/-i, --actual/-a, --dirty, --newdo
  --wsum, --all, --update/-u, --final
```

## Notes

- pop uses backlog popstory output from the active backlog provider.
- pop behavior can vary by provider (for example, whether popped stories are removed or marked in-progress in the backlog source).
- On pop write failure to do.md, dtask exits with error and writes popped content to stderr for recovery.

## Example

```bash
dtask pop
```

# maintenance

Update this page with the prompt below:

"Refresh docs/user/project-setup/dtask.md from current dtask help text and dtask spec. Keep subcommand descriptions concise, keep provider-variance note for pop, and include the do.md write-failure recovery behavior for pop."
