Improve the bin/index-knowledge script, making suure it still conforms to docs/dev/spec/index-knowledge-spec.md
 
Add an option --copilot 
which will create a .github/copilot-instructions.md file with the following content:

````instructions
# AI Assistant Instructions

**For detailed project context and development guidelines, see [AGENTS.md](../../AGENTS.md) at the project root.**

This file is automatically loaded by GitHub Copilot when working in this repository. It references the centralized agent instructions to avoid duplication while ensuring both Copilot and other AI assistants have access to the same context.

````

