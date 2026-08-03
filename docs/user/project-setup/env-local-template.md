# .env.local template

Project-local environment bootstrap file used after sourcing enable_env_local.sh.

## Current Template Behavior

- Validates DEV_SCRIPTS path is set.
- Loads Homebrew shell environment.
- Sources helper functions from helperfuncs.env.
- Exports JAVA_HOME via export_package_home openjdk@21 JAVA_HOME.
- Exports KNOWLEDGE_HOME.
- Adds JAVA_HOME/bin to PATH.
- Uses nvm use when .nvmrc is present.

## Notes

- This file is sourced by shell, so commands execute immediately when loaded.
- Project-specific values should stay local to each project copy.

## Example

```bash
cp .env.local ~/dev/my-project/.env.local
```

# maintenance

Update this page with the prompt below:

"Refresh docs/user/project-setup/env-local-template.md from the current .env.local template. Keep it behavior-oriented, note required environment assumptions, and avoid leaking machine-specific absolute paths."
