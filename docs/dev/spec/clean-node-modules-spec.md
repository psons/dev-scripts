# Specification: clean_node_modulesp

## 1. Project Overview
**File Name:** `bin/clean_node_modules`
**File Type:** Executable script (with `#!/usr/bin/env python3` shebang)
**Target Environment:** Python 3.x (Cross-platform: Unix/macOS/Windows)
**Primary Goal:** To provide a safe utility for reclaiming disk space by deleting `node_modules` and to manage `package-lock.json` files.

---

## 2. CLI Requirements

The script must use a command-based interface, implemented using `argparse` with sub-parsers.

### Default Behavior
If no command is specified, the `help` command is executed by default, printing a usage summary and description of all available commands.

### Global Options
The following option can be used with the `list`, `addlock`, and `delete` commands:

| Option | Short | Description |
| :--- | :--- | :--- |
| `--find <root>` | `-f` | The root directory to begin the operation. Defaults to the current working directory. |

### Commands
The script must support the following commands:

| Command | Description |
| :--- | :--- |
| `help` | Displays the help message with usage and command descriptions. |
| `list` | Identifies and lists all Node projects and their lockfile status without changing anything. |
| `addlock` | Adds a `package-lock.json` file to projects where it is missing. |
| `delete` | Safely deletes `node_modules` directories in projects with a valid lockfile. |

---

## 3. Commands

### `help` (Default)
Prints a comprehensive help message that includes the script's description, usage patterns, and details for all commands and the global `--find` option.

**Example Usage:**
```bash
# Show the help message
bin/clean_node_modules
bin/clean_node_modules help
```

### `list`
Identifies and displays all Node projects found within the search scope (defaulting to CWD, or as specified by `--find`). No files are created or deleted.

**Node Project Detection**

A directory is considered a Node project if it contains any of the following files:
- `package-lock.json` (npm lockfile)
- `yarn.lock` (yarn lockfile)
- `pnpm-lock.yaml` (pnpm lockfile)
- `package.json` (fallback — indicates a Node project even without a lockfile)

A directory qualifies as a Node project and will appear in the `list` output **regardless of whether a `node_modules` directory is present**. The presence or absence of `node_modules` is reported as part of the output status, not used as a filter.

**Output Format**

For each discovered project, one line is printed:

```
<relative-path> [<node_modules-status> | <lockfile-status>]
```

Where:
- `<relative-path>` — The path relative to the search root.
- `<node_modules-status>` — Either `node_modules exists` or `no node_modules`.
- `<lockfile-status>` — Either `lockfile present` or `unsafe: <reason>` (e.g., `unsafe: No lockfile found`).

**Example Output:**
```
my-app [node_modules exists | lockfile present]
other-project [no node_modules | lockfile present]
legacy-app [node_modules exists | unsafe: No lockfile found]
```

**Example Usage:**
```bash
# Preview all node projects in the current directory
bin/clean_node_modules list

# Preview node projects in a specific directory
bin/clean_node_modules list --find ~/Documents/code
```

### `addlock`
For each Node project found, this command checks for `package-lock.json`.
- If `package-lock.json` is missing, it runs `npm install --package-lock-only` in the project's directory.
- If `package-lock.json` already exists, it prints a status message indicating so.

**Example Usage:**
```bash
# Add a package-lock.json to projects in the CWD that are missing one
bin/clean_node_modules addlock

# Add lockfiles in a specific directory
bin/clean_node_modules addlock --find /path/to/projects
```

### `delete`
For each Node project found, this command checks for a valid lockfile and deletes the `node_modules` directory if it is safe to do so. It outputs:
1. **Project path** — The relative path from the search-root to the project.
2. **Status message** — One of:
   - `node_modules deleted.` — If deletion was successful.
   - A single-line explanation of why deletion was unsafe (e.g., "No lockfile found").

**Example Usage:**
```bash
# Perform safe deletion of node_modules in the current directory
bin/clean_node_modules delete

# Perform safe deletion across a specific directory
bin/clean_node_modules delete --find .
```