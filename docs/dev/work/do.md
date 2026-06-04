---
"actualCommitMessage": "fix: dtask can determine the current branch even if there\
  \ are no commits"
"description": "A list of small, focused tasks guiding the current commit with detailed\
  \ microsected activities."
"intendedCommitMessage": "fix: dtask can determine the current branch even if there\
  \ are no commits"
"priorCommit": "faa0a017fe94db30b88e88be2fc649cf33ae6710"
"title": "do.md"
"workBranch": "commit-message-handling"
---



# story: first-commit-branch-check-bug.md 
if there are no commits, dtask commit complains that there is no current branch, even though git knows about the branch.

$ dtask commit --all
Error: current branch '' does not match workBranch 'grooming-2026-06-04'.
$ git log
fatal: your current branch 'grooming-2026-06-04' does not have any commits yet

Th best fix approach:
The Plumbing Command (Best for Scripts/Utilities)
If you are writing repository maintenance scripts or need backward compatibility with older Git versions, use this plumbing command:

```
git symbolic-ref --short HEAD
```

Why it works: Plumbing commands are designed for scripts because their output format is guaranteed never to change. When you run git init, Git immediately creates a .git/HEAD file that points to refs/heads/main, even before any commit objects exist. git symbolic-ref simply reads this file, bypassing the need for a commit history entirely.

Edge Case: If the repository is in a detached HEAD state, this command will explicitly fail and throw an error (fatal: ref HEAD is not a symbolic ref), which is often preferable in automation so your script can catch the error rather than failing silently.
dtask should report the error from git if the git command fails.

d - fix the reported bug under '# story: first-commit-branch-check-bug.md' using  `git symbolic-ref --short HEAD` to determine the current branch.
