# Node JS Based Development

Navigation:
- [User Docs Home](../README.md)
- [Firebase Project Development](../firebase-development/README.md)
- [Development Project Setup](../project-setup/README.md)
- [Feature Based Work Story and Source Commit Workflows](../feature-workflow/README.md)
- [AI Knowledge Indexing and Skills](../ai-knowledge-skills/README.md)

## Activities Currently Facilitated

- Audit lockfile and node_modules hygiene across a project tree.
- Add missing package-lock.json files in Node projects.
- Safely remove node_modules only when lockfile preconditions are met.

## Candidate Activities To Script Next

- Automated lockfile drift checks in CI with actionable fix suggestions.
- Scripted node_modules cleanup for mono-repos with opt-in directory filters.
- Preflight checks for npm version compatibility across projects.

## Script and Artifact Index

- [clean_node_modules](clean-node-modules.md)

# maintenance

Update this page with the prompt below:

"Refresh docs/user/node-js-development/README.md using current command behavior for Node workflows. Keep the five-area navigation block at the top and keep this page focused on activity-level guidance, with links to per-script pages instead of repeated details."
