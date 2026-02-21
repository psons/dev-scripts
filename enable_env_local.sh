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
  . "$PWD/.env.local"
fi

# Function to copy .env.local template to current directory
getenvlocal() {
    local source_file="$DEV_SCRIPTS/../.env.local"
    local dest_file="$PWD/.env.local"
    
    if [ -z "$DEV_SCRIPTS" ]; then
        echo "Error: DEV_SCRIPTS is not set. Please source enable_env_local.sh first." >&2
        return 1
    fi
    
    if [ ! -f "$source_file" ]; then
        echo "Error: Source file $source_file not found." >&2
        return 1
    fi
    
    if [ -f "$dest_file" ]; then
        echo "Error: $dest_file already exists in current directory." >&2
        return 1
    fi
    
    cp "$source_file" "$dest_file"
    if [ $? -eq 0 ]; then
        echo "Copied .env.local to $PWD"
    else
        echo "Error: Failed to copy .env.local" >&2
        return 1
    fi
}