Improve the enable_env_local.sh script, making sure it still conforms to docs/dev/spec/enable-env-local-spec.md
 
Add a shell function projectstub which will take 

Usage: projectstub <dirname> [spec]

the projectstub functiom will:
 - create dirname as a subdirectory of the curent directory.
 - change to dirname as the workig directory and run the getenvlocal function that already exists.
 - source the .env.local file in the working directory.
 - if the spec argument is provided, and is a markdown file, then 
    - create docs/dev/spec/ and copy the spec file into it.
    - run index-knowledge --copilot