# dev-scripts

Tools for managing .env.local and project tools that are not part of the project.

## Overview

These script tools are biased toward developing on MACOS where Homebrew is present, but can be tweaked for any bash like shell environment.

This repository provides utilities for:
- Managing `.env.local` files for project-specific environment variables
- Project tools that should not be committed to source control
- Shell utilities for developers and system administrators

## Contents

- [bin/](bin/README.md) - Executable scripts and utilities
- [spec/](spec/) - Specifications and documentation for the tools
- [enable_env_local.sh](enable_env_local.sh) - Shell script to enable .env.local support

## Quick Start

Source the `enable_env_local.sh` script to enable .env.local support in your shell:

```bash
source /path/to/enable_env_local.sh
```

This will:
- Set the `DEV_SCRIPTS` environment variable to the bin directory
- Add the bin directory to your PATH
- Source any `.env.local` file in your current directory
