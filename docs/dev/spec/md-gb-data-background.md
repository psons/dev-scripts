# Markdown GB Data Background and Rationale

## Status and Authority
This document is the authoritative reasoning and governance context for the gbdata implementation specification in [docs/dev/spec/gbdata-spec-ready.md](docs/dev/spec/gbdata-spec-ready.md).

For implementation work on [bin/gbdata.py](bin/gbdata.py), this document and [docs/dev/spec/gbdata-spec-ready.md](docs/dev/spec/gbdata-spec-ready.md) together form the complete source-of-truth pair:
- [docs/dev/spec/gbdata-spec-ready.md](docs/dev/spec/gbdata-spec-ready.md) defines executable requirements.
- [docs/dev/spec/md-gb-data-background.md](docs/dev/spec/md-gb-data-background.md) defines rationale, source hierarchy, and architectural intent.

[docs/dev/spec/gbdata-spec.md](docs/dev/spec/gbdata-spec.md) is superseded, should be moved to docs/dev/spec/obsolete, and is not required for future gbdata revisions.

## Source Hierarchy
The source hierarchy for gbdata is:
1. [docs/dev/spec/gbdata-spec-ready.md](docs/dev/spec/gbdata-spec-ready.md)
2. [docs/dev/spec/md-gb-data-background.md](docs/dev/spec/md-gb-data-background.md)

Supporting and contextual references:
- [docs/dev/spec/backlog-spec.md](docs/dev/spec/backlog-spec.md)
- [docs/dev/spec/usecases/story-task-parsing-md.md](docs/dev/spec/usecases/story-task-parsing-md.md)

The use-case document remains valid for user-facing documentation and examples, but is not a required dependency for future changes to [bin/gbdata.py](bin/gbdata.py).

## Obsolescence of gbdata-spec.md
The historical role of [docs/dev/spec/gbdata-spec.md](docs/dev/spec/gbdata-spec.md) has been fully absorbed by:
- implementation requirements in [docs/dev/spec/gbdata-spec-ready.md](docs/dev/spec/gbdata-spec-ready.md)
- rationale and governance in [docs/dev/spec/md-gb-data-background.md](docs/dev/spec/md-gb-data-background.md)

Remaining facts from [docs/dev/spec/gbdata-spec.md](docs/dev/spec/gbdata-spec.md) that are intentionally retained here:
- Status shorthand ownership (`val`) and enum semantics are governed by gb-data contracts.
- Status regex pattern strings (`pat_str`) are specification data with security-sensitive handling expectations.
- Code-ready documents are maintained under their local process guidance.
- Generation of [bin/gbdata.py](bin/gbdata.py) is performed from reviewed code-ready requirements, with this document as rationale.

## Architectural Reasoning

### 1) gbdata as a Domain Contract Layer
gbdata is a domain contract boundary used by Backlog providers and related tooling, not merely a parser utility.

Implications:
- Data-model and parser behavior must remain stable and deterministic.
- Changes must preserve interoperability with provider workflows.

### 2) Determinism as a Core Requirement
Deterministic status handling, boundary rules, and identifier generation are required to support predictable downstream behavior.

Implications:
- Parsing must remain robust against mixed markdown authoring patterns.
- Object identity and normalization behavior are treated as compatibility features.

### 3) Security and Contract Integrity for Metadata Patterns
Pattern definitions are contract data and must remain validated and controlled.

Implications:
- Metadata is interpreted through explicit validation.
- Pattern strings are not treated as general code-generation input.

### 4) Backlog Integration Intent
Backlog workflows, including story-first and task-first interactions, depend on gbdata semantics.

Implications:
- Synthetic story behavior for bare tasks is intentional compatibility behavior.
- Parser and model decisions should be evaluated for protocol compatibility, not only local correctness.

## Independence From Legacy Inputs
Future regeneration and revision of [bin/gbdata.py](bin/gbdata.py) must be possible using only:
- [docs/dev/spec/gbdata-spec-ready.md](docs/dev/spec/gbdata-spec-ready.md)
- [docs/dev/spec/md-gb-data-background.md](docs/dev/spec/md-gb-data-background.md)

[docs/dev/spec/gbdata-spec.md](docs/dev/spec/gbdata-spec.md) must not be required for implementation decisions.

## Role of story-task-parsing-md.md Going Forward
[docs/dev/spec/usecases/story-task-parsing-md.md](docs/dev/spec/usecases/story-task-parsing-md.md) is retained for user documentation and explanatory use cases.

It may be referenced for narrative examples, but future parser behavior revisions for [bin/gbdata.py](bin/gbdata.py) should be authored directly in:
- [docs/dev/spec/gbdata-spec-ready.md](docs/dev/spec/gbdata-spec-ready.md)
- [docs/dev/spec/md-gb-data-background.md](docs/dev/spec/md-gb-data-background.md)

## Foundation for Parser/Types Separation
This document establishes the basis for a future refactor that separates markdown parsing concerns from gb domain types.

Refactor direction:
- Keep domain type contracts stable and independently versionable.
- Isolate markdown parsing policy and boundary logic into a dedicated module boundary.
- Preserve behavior compatibility through focused parser tests and contract tests at the type boundary.

This separation is architectural intent. Until that refactor is executed, current behavior remains governed by [docs/dev/spec/gbdata-spec-ready.md](docs/dev/spec/gbdata-spec-ready.md), with rationale from this document.
