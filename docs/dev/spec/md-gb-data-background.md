# Markdown GB Data Background for gbdata.py

## Purpose
This document captures background information that is relevant to gbdata.py but is not currently explicit in docs/dev/spec/code-ready/gbdata-spec-ready.md.

Audited sources:
- [docs/dev/spec/gbdata-spec.md](docs/dev/spec/gbdata-spec.md)
- [docs/dev/spec/code-ready/gbdata-spec-ready.md](docs/dev/spec/code-ready/gbdata-spec-ready.md)
- [docs/dev/spec/backlog-spec.md](docs/dev/spec/backlog-spec.md)
- [docs/dev/spec/usecases/story-task-parsing-md.md](docs/dev/spec/usecases/story-task-parsing-md.md)

## Missing Background Added

### 1) Primary Consumer Context
From backlog-spec.md and story-task-parsing-md.md, gbdata.py is not only a parser utility; it is intended as a domain-and-parsing layer consumed by backlog providers (initially bltodo.py, later others).

Why this matters:
- Parser decisions in gbdata.py define the in-memory shape consumed by backlog workflows.
- Stability of parser behavior is important for provider interoperability.

### 2) Backlog Protocol Coupling Expectations
backlog-spec.md defines provider behavior such as pop_story and pop_task. One key expectation is that a provider can return a story even when only tasks exist (anonymous story behavior).

Why this matters:
- This aligns with gbdata.py synthetic story handling for bare tasks.
- The synthetic story behavior is not only a parser convenience; it is compatible with backlog protocol semantics.

### 3) Markdown TODO.md as Initial Operational Source
backlog-spec.md sets the default operational source to docs/dev/work/TODO.md (via bltodo defaults and environment fallback).

Why this matters:
- gbdata.py parsing rules are expected to work robustly against real-world TODO.md authoring patterns.
- Parser tolerance for mixed markdown content is part of practical operation, not only unit-test scenarios.

### 4) Forward Compatibility for Read/Write Workflows
backlog-spec.md states initial backlog plugin behavior is read-focused, with future write/update support.

Why this matters:
- gbdata.py should preserve deterministic parsing and IDs so future round-trip/update logic can rely on stable object identity.
- Current non-goals (no full markdown AST, no broad rewrite support) are consistent with this phased approach.

### 5) MDGBDF Relationship (Context Only)
backlog-spec.md references Markdown GB Data Form (MDGBDF) as output/input framing for backlog flows.

Why this matters:
- gbdata.py currently provides parse-oriented foundations that are a prerequisite for MDGBDF serialization workflows.
- This explains why parser boundary rules and story/task normalization are strict.

## Notes on Existing Coverage
The code-ready spec already covers most parser mechanics from story-task-parsing-md.md (story boundaries, status detection, left-margin task rules, default do status, bare-task handling, and heading-level behavior).

The primary missing content is operational background and integration intent from backlog-spec.md, not parser algorithm details.

## Suggested Use
Use this document as supporting context while keeping docs/dev/spec/code-ready/gbdata-spec-ready.md as the implementation source of truth for generating bin/gbdata.py.

## Additional Background From gbdata-spec.md Not Explicit In gbdata-spec-ready.md

### 1) Ownership Boundary For Status Shorthand
gbdata-spec.md states that the short status codes (`val`) and formal status values are owned by the gb-data project.

Why this matters:
- gbdata.py should treat these values as externally governed data contracts and avoid local drift in meaning.

### 2) Security Rationale For Pattern Handling
gbdata-spec.md states `pat_str` must correspond 1:1 with enum values and shorthand codes, and highlights security risk in blindly generating client code from regex patterns.

Why this matters:
- Pattern strings should be treated as specification source data with explicit validation/controlled use, not as untrusted code generation inputs.

### 3) Process Constraint For Code-Ready Specs
gbdata-spec.md states that files under docs/dev/spec/code-ready/ are governed by their local README guidance.

Why this matters:
- Implementation-spec maintenance should follow the code-ready documentation process, not ad hoc edits.

### 4) Separate-Prompt Generation Workflow
gbdata-spec.md explicitly calls out that bin/gbdata.py generation should happen from the reviewed code-ready spec via a separate prompt-driven step.

Why this matters:
- Maintains a review gate between requirement/background updates and generated implementation changes.
