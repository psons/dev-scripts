# Markdown GB Data Background and Rationale

## Status and Authority
This document is the authoritative reasoning and governance context for the separated gb-data specifications.

For implementation work on [bin/gbdata.py](bin/gbdata.py) and [bin/mdgbdata.py](bin/mdgbdata.py), the sources-of-truth set are:
- [docs/dev/spec/gbdata-spec-2.md](docs/dev/spec/gbdata-spec-2.md) for domain model requirements.
- [docs/dev/spec/mdgbdata-spec.md](docs/dev/spec/mdgbdata-spec.md) for markdown parsing and status metadata behavior.
- [docs/dev/spec/md-gb-data-background.md](docs/dev/spec/md-gb-data-background.md) for rationale, source hierarchy, and architectural intent.

## Source Hierarchy
The source hierarchy for gb-data implementation is:
1. [docs/dev/spec/gbdata-spec-2.md](docs/dev/spec/gbdata-spec-2.md)
2. [docs/dev/spec/mdgbdata-spec.md](docs/dev/spec/mdgbdata-spec.md)
3. [docs/dev/spec/md-gb-data-background.md](docs/dev/spec/md-gb-data-background.md)

Supporting and contextual references:
- [docs/dev/spec/backlog-spec.md](docs/dev/spec/backlog-spec.md)
- [docs/dev/spec/usecases/story-task-parsing-md.md](docs/dev/spec/usecases/story-task-parsing-md.md)

The use-case document remains valid for user-facing documentation and examples, but is not a required dependency for future changes to [bin/gbdata.py](bin/gbdata.py) or [bin/mdgbdata.py](bin/mdgbdata.py).

## Obsolescence of gbdata-spec.md
The content of gbdata-spec.md has been fully absorbed by the above specs because the parser is no longer built into the same ,module as te shared model.

Remaining facts from [docs/dev/spec/gbdata-spec.md](docs/dev/spec/gbdata-spec.md) that are intentionally retained here:
- Status shorthand ownership (`val`) and enum semantics are governed by gb-data contracts.
- Status regex pattern strings (`pat_str`) are specification data now kept as source for security because they become executable in client apps.

## Architectural Reasoning
gb-data is the source repo for the data model common to various software tools to model tasks, stories, an goals as a hierarchy for planning and achieving outcomes. 
gbdata.py is the python module in this repo to implement the types as a shared model for integration. 
The backlog.py module and all of the plugins to be built need to import gbdata.py, whereas the markdown parser is only needed by bltodo (TODO file) plugin, and a possible future plugin that uses a directory of markdown files.  

### 1) gbdata as a Domain Contract Layer
gbdata is a domain contract boundary used by Backlog providers and related tooling.

`mdgbdata` is the markdown parsing layer that consumes and returns gbdata model types.

Implications:
- Data-model behavior must be based on gb-data and gbdata.py
- Changes must preserve interoperability with provider workflows based on gbdata.
- Parsing in `mdgbdata` must remain robust against mixed markdown authoring patterns.
- Object identity and normalization behavior are treated as compatibility features.

### 3) Security and Contract Integrity for Metadata Patterns
Pattern definitions are contract data and must remain validated and controlled in the markdown parsing layer.

### 4) Backlog Integration Intent
Backlog workflows, including story-first and task-first interactions, depend on gbdata model semantics and mdgbdata parsing behavior.

Definitions used in this document:
- story-first: the user writes or promotes a story container before adding tasks, so tasks are parsed beneath an explicit story heading.
- task-first: the user starts with task headers before any story exists, so the parser may create a synthetic "Unscoped" story to hold those tasks.

Implications:
- Synthetic story behavior for bare tasks is intentional compatibility behavior in parsing.
- Parser and model decisions should be evaluated for protocol compatibility, not only local correctness.

## Independence From Legacy Inputs
Future regeneration and revision of [bin/gbdata.py](bin/gbdata.py) and [bin/mdgbdata.py](bin/mdgbdata.py) must be possible using only:
- [docs/dev/spec/gbdata-spec-2.md](docs/dev/spec/gbdata-spec-2.md)
- [docs/dev/spec/mdgbdata-spec.md](docs/dev/spec/mdgbdata-spec.md)
- [docs/dev/spec/md-gb-data-background.md](docs/dev/spec/md-gb-data-background.md)

## Role of story-task-parsing-md.md Going Forward
[docs/dev/spec/usecases/story-task-parsing-md.md](docs/dev/spec/usecases/story-task-parsing-md.md) is retained for user documentation and explanatory use cases.

It may be referenced for narrative examples, but future parser behavior revisions for [bin/mdgbdata.py](bin/mdgbdata.py) should be authored directly in:
- [docs/dev/spec/mdgbdata-spec.md](docs/dev/spec/mdgbdata-spec.md)
- [docs/dev/spec/md-gb-data-background.md](docs/dev/spec/md-gb-data-background.md)

## Foundation for Parser/Types Separation
This document establishes the basis for a refactor that separates markdown parsing concerns from gb domain types.

Refactor direction:
- Keep domain type contracts stable and independently versionable.
- Isolate markdown parsing policy and boundary logic into a dedicated module.
- Preserve behavior compatibility through focused parser tests and contract tests at the type boundary.

This separation is now established at the specification level. Current behavior is governed by [docs/dev/spec/gbdata-spec-2.md](docs/dev/spec/gbdata-spec-2.md) and [docs/dev/spec/mdgbdata-spec.md](docs/dev/spec/mdgbdata-spec.md), with rationale from this document.
