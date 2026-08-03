# gshove.sh

Git helper that moves current uncommitted work to a new branch, commits, pushes, then restores original branch state.

## Usage

```text
Usage: gshove "your commit message"
```

## Runtime Help Behavior

gshove.sh does not implement a standard --help flag. Invoking it with --help currently runs normal validation and can produce branch-state errors such as:

```text
Error: Target branch '<derived_target_branch>' already exists.
```

## Notes

- Derived target branch format is shove-<start_branch>.
- Runtime branch names were tokenized to avoid machine-specific output snapshots.

## Example

```bash
gshove.sh "checkpoint: preserve unpushed work before risky rebase"
```

# maintenance

Update this page with the prompt below:

"Refresh docs/user/project-setup/gshove.md from current script behavior. Keep the standard usage line, document non-standard help behavior, and keep dynamic branch names tokenized."
