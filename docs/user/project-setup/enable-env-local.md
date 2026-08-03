# enable_env_local.sh

Shell bootstrap script intended to be sourced into an interactive shell.

## Usage

```text
source enable_env_local.sh
```

## Included Functions

- getenvlocal: copy template .env.local into current directory.
- projectstub <dirname> [spec]: create project directory, copy env template, optionally copy a markdown spec into docs/dev/spec, and optionally run index-knowledge --copilot.

## Runtime Help Behavior

enable_env_local.sh does not provide a built-in --help command. Usage is inferred from function behavior in the script.

## Example

```bash
source enable_env_local.sh && projectstub my-new-project docs/dev/spec/enable-env-local-project-stub.md
```

# maintenance

Update this page with the prompt below:

"Refresh docs/user/project-setup/enable-env-local.md from the current shell script functions and behavior. Keep command examples minimal and reflect any changes to getenvlocal or projectstub."
