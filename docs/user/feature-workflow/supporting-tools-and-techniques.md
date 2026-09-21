
### To see the do.md from a feature branch that has just been finalized

Use the porcelain git command:

```bash
git show HEAD~2:docs/dev/work/do.md
````

If the commit was farther back, and has a tag, use the tag name and ~2 to access the commit before it.
In this example, basic-ddf is the tag visible in `git log --oneline`:

```bash
git show basic-ddf~2:docs/dev/work/do.md
```

