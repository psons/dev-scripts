#!/bin/bash
# This script should be sourced, not executed
# It discovers its own absolute path and adds it to PATH

# Get the directory where this script is located
if [ -n "${BASH_SOURCE[0]}" ]; then
    # Get the absolute path of the bin subdirectory
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    DEV_SCRIPTS="$SCRIPT_DIR/bin"
    export DEV_SCRIPTS
    
    # Add DEV_SCRIPTS to PATH if it exists and is not already in PATH
    if [ -d "$DEV_SCRIPTS" ]; then
        if [[ ":$PATH:" != *":$DEV_SCRIPTS:"* ]]; then
            export PATH="$DEV_SCRIPTS:$PATH"
        fi
    fi
else
    echo "Warning: Unable to determine script location. Please source this script in bash." >&2
fi

# snippet suggested for .vscode to load .env.local variables in a project directory.
if [ -f "$PWD/.env.local" ]; then
  set -a
  . "$PWD/.env.local"
  set +a
fi