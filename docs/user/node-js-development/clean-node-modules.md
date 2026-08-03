# clean_node_modules

Node project maintenance tool for lockfile alignment and safe node_modules cleanup.

## Usage

```text
usage: clean_node_modules [-h] {help,list,addlock,delete} ...

Safely delete node_modules and manage package-lock.json files in Node.js projects.

positional arguments:
  {help,list,addlock,delete}
    help                Show this help message and exit.
    list                List all Node projects and their lockfile/node_modules status.
    addlock             Add package-lock.json to projects missing one.
    delete              Safely delete node_modules in projects that have a valid lockfile.

options:
  -h, --help            show this help message and exit

Global option (applies to list, addlock, and delete):
  --find <root>, -f <root>
      Root directory to begin the search. Defaults to the current working directory.
```

## Example

```bash
clean_node_modules list --find ~/dev
```

# maintenance

Update this page with the prompt below:

"Refresh docs/user/node-js-development/clean-node-modules.md from current CLI help output. Keep subcommand descriptions aligned to behavior and preserve the global --find option description."
