# Specification: safe-node-modules-cleanup

# TODO - Testing needed to assure that projects can be restored with npm install after cleaning up modules.

## 1. Project Overview
**File Name:** `bin/safe_node_modules_cleanup`
**File Type:** Executable script (with `#!/usr/bin/env python3` shebang)
**Target Environment:** Python 3.x (Cross-platform: Unix/macOS/Windows)
**Primary Goal:** To provide a safe utility for reclaiming disk space by deleting `node_modules` only when the project can be 100% reconstituted via an existing lockfile.

---

## 2. CLI Requirements

The script must support the following command-line interface using `argparse`:

| Option | Short | Description |
| :--- | :--- | :--- |
| `--find <root>` | `-f` | **Optional.** The root directory to begin searching for Node projects. Defaults to current working directory if not specified. |
| `--list` | `-l` | **Optional.** If set, the script will only identify and list projects/status without deleting anything. Works with or without `--find`. |
| `--addlock` | | **Optional.** If set, the script will add a `package-lock.json` file if one does not already exist by running `npm install --package-lock-only`. If `package-lock.json` already exists, a status message is printed. |

### Example Usage
```bash
# Preview all node projects in the current directory and their safety status
bin/safe_node_modules_cleanup --list

# Preview node projects in a specific directory
bin/safe_node_modules_cleanup --find ~/Documents/code --list

# Add a package-lock.json to projects that are missing one
bin/safe_node_modules_cleanup --addlock

# Perform safe deletion of node_modules in the current directory
bin/safe_node_modules_cleanup

# Perform safe deletion across a specific directory
bin/safe_node_modules_cleanup --find .
```

---

## 3. Output Format and Behavior

### With `--list` Option
When `--list` is specified, the script identifies and displays all Node projects along with their safety status without performing any deletions.

### With `--addlock` Option
When `--addlock` is specified, for each Node project found, the script checks for `package-lock.json`.
- If `package-lock.json` is missing, it runs `npm install --package-lock-only` in the project's directory.
- If `package-lock.json` already exists, it prints a message indicating so.
This option can be combined with `--find`.


### Deletion Mode (Without `--list`)
When the script runs without `--list`, it processes each Node project found and outputs:
1. **Project path** — The relative path from the search-root to the project
2. **Status message** — One of:
   - `node_modules deleted.` — If deletion was successful
   - A single-line explanation of why deletion was unsafe (e.g., "No lockfile found", "Lockfile outdated", etc.)

The search-root defaults to the current working directory if `--find` is not specified.

**Example output:**
```
docs/my-app node_modules deleted.
src/legacy-project No lockfile found
utils/web-app node_modules deleted.
```