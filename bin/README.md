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

See [../spec/list-spec.md](../spec/list-spec.md) and [../spec/list-fileset-spec.md](../spec/list-fileset-spec.md) for full documentation.

## Additional Content

Some of the script content is for introspecting installation specifics like Homebrew to reduce the amount of text in `.env.local`.

Some utilities that may help developers and system administrators are also included, but may be pushed to a different repository at some time (like the `list` script).

## Source and AI

This project has the opinion that the specification of software belongs in the source tree, but that the hooks for any specific AI platform like Copilot or Gemini are more like IDEs and should be in separate source control.

### Reasoning

See [../spec/what-is-where.md](../spec/what-is-where.md)
