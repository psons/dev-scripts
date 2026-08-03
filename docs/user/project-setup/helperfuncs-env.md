# helperfuncs.env

Shared shell helper functions for resolving symlink targets and exporting package homes.

## Exported Functions

- export_link_path <link_path> <output_var>
- export_package_home <package_name> <output_var>

## Notes

- export_package_home validates package installation through Homebrew before exporting path variables.
- export_link_path supports both Linux and macOS resolution paths.

## Example

```bash
source bin/helperfuncs.env && export_package_home openjdk@21 JAVA_HOME
```

# maintenance

Update this page with the prompt below:

"Refresh docs/user/project-setup/helperfuncs-env.md from helperfuncs.env function behavior. Keep function signatures accurate and describe validation and portability behavior briefly."
