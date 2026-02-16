#!/bin/bash
# This script should be sourced, not executed
# It discovers its own absolute path and adds it to PATH

# Get the directory where this script is located
if [ -n "${BASH_SOURCE[0]}" ]; then
    # Get the absolute path of the directory containing this script
    DEV_SCRIPTS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    export DEV_SCRIPTS
    
    # Add DEV_SCRIPTS/bin to PATH if it exists and is not already in PATH
    if [ -d "$DEV_SCRIPTS/bin" ]; then
        if [[ ":$PATH:" != *":$DEV_SCRIPTS/bin:"* ]]; then
            export PATH="$DEV_SCRIPTS/bin:$PATH"
        fi
    fi
else
    echo "Warning: Unable to determine script location. Please source this script in bash." >&2
fi

echo $DEV_SCRIPTS