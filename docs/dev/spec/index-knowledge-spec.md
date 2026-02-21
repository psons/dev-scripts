# Technical Specification: `index_knowledge.py`

This specification defines the requirements and implementation for a Python-based automation script designed to synchronize AI context across a repository by generating a centralized `AGENTS.md` file.

---

### 1. Objective
The primary goal is to transform static documentation into an "active map" for AI agents (such as GitHub Copilot). By parsing **YAML frontmatter**, the script ensures that AI tools prioritize the most relevant, up-to-date architectural decisions and project descriptions.

### 2. Requirements

* **Priority Entry**: The file located at `docs/dev/project-description.md` must be extracted and placed at the very top of the generated index to establish core project context.
* **Metadata Extraction**: The script must use a YAML parser to identify `title`, `status`, and `description` from the head of each Markdown file.
* **Dynamic Discovery**: All `.md` files within the `docs/` directory must be recursively discovered and indexed.
* **Generic Context**: The script and its output (`AGENTS.md`) must remain project-agnostic, referring only to architectural patterns and document types.
* **Relative Linking**: All references in `AGENTS.md` must use relative Markdown links to allow AI agents to navigate the file system effectively.

---

### 3. Logic Flow and Structure

The generated `AGENTS.md` will follow this internal hierarchy:
1.  **Header**: A generic warning that the file is automated.
2.  **Core Context**: High-level project intent (from `docs/dev/project-description.md`).
3.  **Shared Knowledge**: Cross project shared knowledge ( from ${KNOWLEDGE_HOME}/shared-knowledge.md)
4.  **Knowledge Index**: A list of all other documentation (ADRs, Patterns, Specs) sorted alphabetically.

---

### 4. Implementation Script

The implementation script should be bin/index-knowledge
