# enable_env_local.sh spec - improved
[enable_env_local.sh](../enable_env_local.sh) when sourced into a bash shell, must be able to discover the absolute path it is located in.

The absolute path to the bin subdirectory of enable_env_local.sh must be exported in a variable named DEV_SCRIPTS.

DEV_SCRIPS must be added to the path.

code must be included so that when a login shell sources enable_env_local.sh is sourced from 
.bash_profile, and the curent directory contains includes a file named .env.local, .env.local is also  sourced into the current shell.  The specific intent of this feature is to set up environmet for vscode.
