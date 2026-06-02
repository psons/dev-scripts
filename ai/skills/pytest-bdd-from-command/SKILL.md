---
name: pytest-bdd-from-command
description: 'Generate pytest-bdd artifacts from command usage plus an outcome description. Use when you need .feature Gherkin files, Python step definitions, and runnable pytest tests for CLI workflows.'
argument-hint: 'Command usage and expected outcome'
user-invocable: true
disable-model-invocation: false
---

# Pytest BDD From Command

Create complete pytest-bdd test assets from:
1. A command usage reference (flags, arguments, examples)
2. A short expected outcome description

This skill produces:
- Feature files under `tests/features/`
- Step files under `tests/steps/`
- Optional supporting test module updates when needed
- A runnable pytest command to validate the new coverage

## When to Use
- You have a CLI command and want behavior-focused tests quickly.
- You need Given/When/Then scenarios from terse acceptance criteria.
- You need reproducible BDD tests that run with `pytest`.

## Inputs
Provide:
1. Command reference: syntax, options, examples, and error behavior.
2. Outcome summary: what should happen for success and failure paths.
3. Constraints: target directories, naming style, fixtures to reuse.

## Required Defaults
- Always generate both success-path and failure-path scenarios, even when only one path is explicitly requested.
- Step definitions must execute commands through a shared helper/fixture layer; do not run command execution inline in individual step functions.
- Clarification for compliance with `docs/dev/spec/testing-tools/test-tools-spec.md`: share helper code, not runtime state. Command result objects, temp paths, and mutable context must be created per scenario (or per step as needed) and passed through fixtures/`target_fixture`, with no cross-scenario object reuse.
- Apply fixed file naming:
	- Feature file: `tests/features/<command_slug>/<command_slug>.feature`
	- Step file: `tests/steps/test_<command_slug>_steps.py`

## Procedure
1. Parse the command contract.
- Extract required args, optional flags, defaults, exit codes, and output channels (stdout/stderr/files).
- Identify external side effects (filesystem, git state, env vars).

2. Model the behavior as Gherkin.
- Create one feature per command capability.
- Create scenarios for happy path, validation failures, and edge cases.
- Use `Scenario Outline` when only input/output values vary.
- Add `Background` only for shared setup used by most scenarios.

3. Generate feature files.
- Write `.feature` files using fixed naming: `tests/features/<command_slug>/<command_slug>.feature`.
- Keep steps declarative and user-observable (avoid implementation details).
- Use stable, reusable wording for steps to maximize step reuse.

4. Generate step definitions.
- Add step modules using fixed naming: `tests/steps/test_<command_slug>_steps.py`.
- Reuse existing fixtures before introducing new fixtures.
- Execute commands through a single helper pattern so stdout/stderr/exit code are captured consistently.
- Assert outcomes in `then` steps only.

5. Wire imports and discovery.
- Ensure step modules are discoverable by pytest collection in this repo layout.
- Keep test naming aligned with existing patterns (`test_*.py`).

6. Validate by running tests.
- Run targeted tests first, then broader suite if requested.
- Example: `pytest tests/features/<topic> -q`

## Decision Points
- If command behavior changes by flag combinations: prefer multiple scenarios over one oversized scenario.
- If setup is expensive and repeated: use fixtures + `Background`.
- If output is dynamic (timestamps, random IDs): assert stable substrings or regex patterns.
- If command mutates repository state: isolate in temp directories and explicit cleanup fixtures.
- If the user requests only one path type (for example, success only), still include at least one failure-path scenario to preserve regression safety.

## Quality Gates
- Every `Given/When/Then` step in feature files has exactly one matching step implementation.
- Scenarios verify observable outcomes: exit code, output text, files created/changed.
- Failure-path scenarios assert clear error signals.
- Generated tests pass locally with pytest.
- New steps avoid duplication when equivalent wording already exists.
- Step implementations call a shared command execution helper/fixture instead of direct subprocess logic per step.
- Runtime objects are isolated per scenario: no shared mutable command-result objects, no shared mutable temp repo paths, and no leaked state between scenarios.
- Generated files follow the fixed naming convention for feature and step files.

## Output Contract
Return:
1. Created/updated file list
2. Short rationale for scenario coverage
3. Exact pytest command(s) to run
4. Any open assumptions that need user confirmation

## Prompt Pattern
Use this skill with prompts like:
- "From this command usage and expected behavior, generate pytest-bdd feature and step files."
- "Create happy-path and failure-path Gherkin plus pytest-bdd steps for this CLI command."
