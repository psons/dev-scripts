# backlog.py

Backlog command dispatcher that calls a backlog provider plugin and emits prioritized work in markdown or JSON.

## Usage

```text
usage: backlog [-h] [--provider PROVIDER] [--mdgbdf | --json]
               {prioritized,poptask,popstory,help} ...

Query prioritized backlog data via a provider plugin

positional arguments:
  {prioritized,poptask,popstory,help}
    prioritized         Show prioritized tasks
    poptask             Show the highest-priority task
    popstory            Show the highest-priority story
    help                Show command usage summary

options:
  -h, --help            show this help message and exit
  --provider PROVIDER   Backlog provider module name (default:
                        BACKLOG_PROVIDER or bltodo)
  --mdgbdf              Output Markdown GB Data Form
  --json                Output JSON

Environment variables:
  BACKLOG_PROVIDER  Provider module name to use when --provider is not set.
                    If unset, the backlog provider defaults to: bltodo
```

## Notes

- Provider behavior is plugin-specific.
- popstory output used by dtask pop can differ by provider implementation.

## Example

```bash
backlog.py --mdgbdf prioritized
```

# maintenance

Update this page with the prompt below:

"Refresh docs/user/project-setup/backlog.md from current backlog.py CLI help and provider behavior. Keep the usage block in sync with --help output and keep provider-specific behavior notes concise."
