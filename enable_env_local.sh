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

# Function to create a project stub with optional spec file
projectstub() {
    local dirname="$1"
    local spec="$2"
    
    # add a check here to see if the spec argument is provided and is a valid file.
    # if spec is a valid file set a variable specpath to be its absolute path
    if [ -n "$spec" ] && [ -f "$spec" ]; then
        specpath="$(cd "$(dirname "$spec")" && pwd)/$(basename "$spec")"
    fi

    if [ -z "$dirname" ]; then
        echo "Usage: projectstub <dirname> [spec]" >&2
        return 1
    fi
    
    # Create the directory
    mkdir -p "$dirname"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create directory $dirname" >&2
        return 1
    fi
    
    # Change to the directory
    cd "$dirname"
    
    # Run getenvlocal
    getenvlocal
    if [ $? -ne 0 ]; then
        echo "Error: Failed to run getenvlocal" >&2
        cd ..
        return 1
    fi
    
    # Source the .env.local file
    if [ -f ".env.local" ]; then
        . "./.env.local"
    fi
    
    # Handle spec file if provided
    if [ -n "$specpath" ]; then
        # Check if specpath file exists and is a markdown file
        if [ -f "$specpath" ] && [[ "$specpath" == *.md ]]; then
            # Create docs/dev/spec directory
            mkdir -p "docs/dev/spec"
            if [ $? -ne 0 ]; then
                echo "Error: Failed to create docs/dev/spec directory" >&2
                cd ..
                return 1
            fi
            
            # Copy spec file
            spec_filename=$(basename "$spec")
            cp "$specpath" "docs/dev/spec/$spec_filename"
            if [ $? -ne 0 ]; then
                echo "Error: Failed to copy spec file" >&2
                cd ..
                return 1
            fi
            
            # Run index-knowledge --copilot
            if command -v index-knowledge &> /dev/null; then
                index-knowledge --copilot
            else
                echo "Warning: index-knowledge command not found in PATH" >&2
            fi
        else
            echo "Warning: Spec file '$spec' not found or is not a markdown file" >&2
        fi
    fi
}