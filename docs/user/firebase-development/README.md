# Firebase Project Development

Navigation:
- [User Docs Home](../README.md)
- [Node JS Based Development](../node-js-development/README.md)
- [Development Project Setup](../project-setup/README.md)
- [Feature Based Work Story and Source Commit Workflows](../feature-workflow/README.md)
- [AI Knowledge Indexing and Skills](../ai-knowledge-skills/README.md)

## Activities Currently Facilitated

- Restart local Firebase emulator stack after clearing stale listeners on emulator ports.
- Auto-discover firebase.json from current directory ancestry before startup.
- Support iterative project experimentation where repeated environment resets and local service restarts are part of short feature loops.

## Candidate Activities To Script Next

- Profile-based emulator boot (dev, test, integration).
- Optional selective restart of individual emulator services.
- Port conflict report with suggested remapping patch for firebase.json.
- Repeatable Firebase project skeleton cloning flow for A/B experiments (inspired by [proposed-dir-skel](../../dev/spec/usecases/proposed-dir-skel.md)).

## Script and Artifact Index

- [bounce-fbase](bounce-fbase.md)

# maintenance

Update this page with the prompt below:

"Refresh docs/user/firebase-development/README.md from current bounce-fbase behavior and Firebase workflows. Keep cross-links at the top and keep implementation details in linked script pages."
