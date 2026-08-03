# bltodo.py

Default backlog provider backed by a markdown TODO file.

## Usage

```text
usage: bltodo [-h] {show,showrecovery,recovery,help} ...

Default backlog provider reading stories/tasks from a TODO.md file

positional arguments:
  {show,showrecovery,recovery,help}
    show                Print TODO path and MDGBDF backlog
    showrecovery        Show backlog path, recovery dir, and directory listing
    recovery            Save a recovery copy of the TODO file
    help                Show command usage summary

options:
  -h, --help            show this help message and exit

Environment variables:
  BL_TODO_FILE  Absolute or relative path to the TODO markdown file.
                If unset, bltodo uses git-root-relative path: <git_root>/docs/dev/work/TODO.md
```

## Notes

- Runtime-expanded default path was tokenized to avoid embedding machine-specific absolute paths.
- Provider behavior may differ across backlog plugins; this implementation removes popped content from TODO.md as part of pop operations.

## Example

```bash
bltodo.py showrecovery
```

# maintenance

Update this page with the prompt below:

"Refresh docs/user/project-setup/bltodo.md from current bltodo.py help output and behavior. Keep runtime-derived paths tokenized and keep plugin-specific behavior notes up to date."
