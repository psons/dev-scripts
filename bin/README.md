# bin/

Executable scripts and utilities for working with `.env.local` files, especially for use in VS Code terminals.

## Overview

The scripts in this directory are meant to be added to your PATH and provide functionality for managing environment variables and project-specific configurations.

### .env.local Support

The name `.env.local` is conventional for some JavaScript frameworks to store environment variables that should not be committed to source control.

Similarly, the intent here is to use it for project needs that may be installed outside the project and coupled to the local computer, such as:
- Path to Java
- Local installations of nvm and Python
- Project-specific environment variables

A code snippet in the parent directory shows what to put in a shell profile to source the `.env.local` file when a shell starts in the current directory, as VS Code does when launching a terminal.

## Utilities

### list

A Python utility for manipulating string lists that are either delimited values on a single line or newline-separated lines.

**Features:**
- Convert between flat (delimited) and tall (newline-separated) formats
- Save and load named lists from `~/.lists/`
- Accept list items as command-line arguments
- Support custom delimiters
- Preserve glob patterns (wildcards)

**Usage:**
```bash
list [options] <command> [args...]
```

See [../docs/spec/list-spec.md](../spec/list-spec.md) and [../spec/list-fileset-spec.md](../spec/list-fileset-spec.md) for full documentation.

### clean_node_modules
- (See [../docs/spec/clean-node-modules-spec.md](../docs/dev/spec/clean-node-modules-spec.md)
Run with no args to show the help message.
Used to make sure there is a package-lock.json file and delete the node_modules directory to save space.
As long as there is a package-lock.json, then the npm install command cand re-download the node_modules.

### dtask

dtask helps users maintain a file called do.md to keep focus on help a single 'top of queue' task and assure the commit history and work record connected to the task, feature, and story.

It is a Python utility that manages git branches and commit messages for the current task by administering YAML frontmatter in `docs/dev/work/do.md`.   

The dtask script supports a work flow where a top task is popped off of a TODO.md into the do.md file.  Engineers add elaboration about the task that may for example suffice an AI prompt.  When complete, the do.md for the task gets committed into git history and then removed to make way for the next task.  It is purpise built to support a bigger 
picture workflow described in [specification-workflow.md](docs/dev/spec/usecases/specification-workflow.md)

**Features:**
- `dtask init` Initializes a `do.md` file capturing the current commit hash, branch, and intended/actual commit messages
- do.md is intended to capture the instructions for the task being worked on.
- Creates and checks out a work branch via `git checkout -b`
- Enforces a clean working tree before init, with `--dirty` and `--newdo` escape hatches
- Commits staged changes using the `actualCommitMessage` from `do.md`
- `--all` stages and commits both staged and unstaged changes
- `--actual` with no argument copies `intendedCommitMessage` to `actualCommitMessage` to signal the task proceeded as expected
- `--final` closes the task cycle: commits `do.md` with staged changes (or all changes with `--all`), then removes `do.md` in a second commit with the message `removed do.md for finalized tasks`. Works even with no staged changes, leaving the tree ready for the next `dtask init`

**Usage:**
```bash
dtask <subcommand> [options]

dtask help
dtask init [-b <branch>] [-i <intended>] [-a <actual>] [--dirty] [--newdo]
dtask commit [-a [message]] [--all] [--final]
```

See [../docs/dev/spec/dtask-spec.md](../docs/dev/spec/dtask-spec.md) for full documentation.


## Additional Content

Some of the script content is for introspecting installation specifics like Homebrew to reduce the amount of text in `.env.local`.

Some utilities that may help developers and system administrators are also included, but may be pushed to a different repository at some time (like the `list` script).

## Source and AI

This project has the opinion that the specification of software belongs in the source tree, but that the hooks for any specific AI platform like Copilot or Gemini are more like IDEs and should be in separate source control.

### Reasoning

See [../docs/spec/what-is-where.md](../docs/spec/what-is-where.md)
