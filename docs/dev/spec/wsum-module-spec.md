Re work the worksum command as a python module and command as bin/wsum.py
The worksum program was originally implemented from docs/dev/spec/worksum-spec.md.


# Use / behavior:

## when used as a module
Create wsum.py which will be used both as a module, and directly as a command.
A function in the module should return a typed result object rather than a positional list.

Required result fields:
    1 - timestamp: a timestamp as shown in the markdown example below.
    2 - headline: a one-line work headline used in workHeadline front-matter.
    3 - summary: a 3 to 6 sentence summary of git diff results.
    4 - markdown: formatted markdown text matching command output.

Recommended implementation shape:
- Define a WorkSummaryResult dataclass with fields: timestamp, headline, summary, markdown.

### calling and parameters
The calling program will need to pass a parameter to indicate if the summarization should cover staged changes only, or both staged changes and unstaged changes.
The parameter name and default should match the semantics of -all option of dtask commit.
Specifically, the default behavior should be to only include staged changes.
By default, command and module invocation should diff staged changes in the index against the most recent commit (HEAD).
When all changes are requested, include both staged and unstaged working tree changes.

Recommended parameter contract:
- staged_only: bool = True
- base_ref: str = "HEAD"
- include_unstaged / all_changes: bool = False (maps to dtask --all semantics)
- diff_text: str | None = None (when provided, skip internal git diff generation)
- file_paths: list[str] | None = None (optional path filtering for internally generated diffs)
- extra_diff_args: list[str] | None = None (optional constrained escape hatch)

Diff input model requirements:
- Dual-source input is required.
- If diff_text is provided, summarize that diff directly.
- If diff_text is not provided, generate diff from staged_only/base_ref/include_unstaged and optional file paths.
- CLI should accept stdin diff input and map it to diff_text when provided.

## when run as a command
Output markdown formatted like the following example.  The data is the first 3 elements returned from the module function call.  The actual output is the 4th paramarter returned from the function call. 

Command behavior requirements:
- Default invocation summarizes staged changes versus HEAD.
- A command option aligned with dtask --all must include unstaged changes to tracked files and untracked files. (revised 2026-05-15)
- An optional base ref argument may be provided to compare against a branch, tag, or commit.
- Command should support stdin diff input; when stdin is provided, stdin takes precedence over internal git diff generation.
- Support explicit git diff options; do not implement unrestricted pass-through of arbitrary git diff arguments.
- If an escape hatch is provided, validate and document allowed values for extra_diff_args.

### wsum option alignment with dtask (revised 2026-05-15)
#### --all, -a
- The file inclusion of --all should be the same for dtask init is for git add.  
- wsum  --all should also align with git add and dtask init to allow user inference of how wsum works to be easy based on how dtask works.
- specifically, --all includes 
    - staged, 
    - tracked with unstaged changes.
    - untracked

#### --update, -u
- wsum should support a --update (or -u) option. The same option will be added to dtask. 
- --update matches the same option on git add.
- specifically, --all includes 
    - staged
    - tracked with unstaged changes.


'''markdown
## 2026-05-11 19:14

---
workHeadline: Doc corrections
---

The provided git diff contains several minor corrections across documentation files. In `bin/README.md`, typos like "cand re-do" were corrected to "can re-do", "cets committed" to "gets committed", and "instrctions" to "instructions". The `docs/dev/spec/index-knowledge-copilot-spec.md` file had "suure" corrected to "sure". Finally, `docs/dev/spec/usecases/do-file-tasks.md` and `docs/dev/spec/what-is-where.md` both received grammatical corrections, improving readability and clarity in descriptions of task microsectioning and AI prompt specifications respectively. These changes primarily enhance the accuracy and professionalism of the project's documentation.

'''

# Implementation guidance For both command and module invocation
The summary prompt should be similar to the existing prompt from bin/worksum.
            You are a technical writer. Summarize the git diff from stdin into a concise,
            human-readable work summary. Focus on what changed and why it matters, not raw diff
            mechanics. Use plain prose (no bullets unless there are clearly distinct work
            streams). Be specific about file names and functionality. Keep the summary to 3-6
            sentences. Return only the summary text.

Integration guidance for dtask:
- Implement a shared helper layer that both wsum and dtask call for diff selection, summarization, and markdown rendering.
- Keep output formatting consistent so work summaries have identical structure regardless of which command generated them.
- Keep staged-only as the shared default so dtask and wsum remain behaviorally aligned.

Recommended core API shape:
- Implement one core function and wrap it from CLI.
- Example signature: summarize_work(diff_text=None, staged_only=True, base_ref="HEAD", include_unstaged=False, file_paths=None, extra_diff_args=None, model=None, max_sentences=6)
- The function should return WorkSummaryResult.

Testability requirements:
- Separate pure functions (prompt assembly, headline generation, markdown rendering) from side-effect adapters (git diff collection and model invocation).
- Add tests for:
    - staged-only default behavior
    - base ref comparison behavior
    - stdin or diff_text input behavior
    - empty diff handling
    - markdown output compatibility with docs/dev/work/do.md format
    - validation behavior for extra_diff_args
    

# Design Review of this Spec 
An important principle is that the tools wsum and dtask provide a simple to use work flow with a highly professional commit and branch strategy.   The dtask script establishes a workflow that works well with task decomposition to implement well thought out project features.

Provide an analysis of this spec to determine where the overall design can be improved.  Focus on reusability opportunities and integration usability with planned dtask enhancements.

Does the existing worksum command provide the capability to compare staged changes to other branches or commits other than the most recent commit?

What design improvements can be made so that any git diff can be summarized?  Specifically should the wsum command support arbitrary arguments to pass through from its invocation to the git diff?   Or is it better to read the diff output from stdin and allow the invoking program to provide the diff?

## Design Review Results

1. Current capability assessment:
The existing `worksum` command already supports comparing against refs other than the most recent commit via `--base` (for example `main`, `HEAD~2`, or a commit SHA), and it supports staged-only mode via `--staged`. This means branch/commit comparison is already partially solved in the current implementation.
Action completed in this spec: the new wsum defaults to diffing staged changes against HEAD, and adopts item 5 integration guidance.


2. Reusability improvement:
Replace the "4-element list" module return contract with a typed result object (for example a dataclass with `timestamp`, `headline`, `summary`, and `markdown`). This is more stable for future additions and easier for `dtask` and other callers to consume safely.
Action completed in this spec: module output now requires a typed result object with named fields.

3. Input model improvement:
Use a dual-source design for diff input:
- default: module/command generates diff internally from explicit options (`staged_only`, `base_ref`, and optional file paths)
- optional: caller provides diff text directly (stdin for CLI, `diff_text` argument for module)
This gives high usability for normal workflows and maximum flexibility for advanced integrations.
Action completed in this spec: dual-source diff input requirements are now defined in calling and command behavior sections.

4. Git argument strategy:
Avoid unrestricted pass-through of arbitrary `git diff` arguments because it weakens contract clarity and complicates testing. Prefer explicit supported options plus a constrained escape hatch such as `extra_diff_args: list[str] | None` with validation and documented limits.
Action completed in this spec: explicit options are required and any escape hatch must be constrained and validated.

5. Integration with planned `dtask` enhancements:
Keep parameter semantics aligned with `dtask commit --all` by using `staged_only=True` as the default. Add a shared helper layer that `dtask` can call directly so both tools produce consistent summaries, timestamps, and markdown layout.
Action completed in this spec: dtask alignment and shared helper-layer requirements are now defined in the calling and implementation guidance sections.

6. Recommended module API shape:
Define one core function (for example `summarize_work(diff_text=None, staged_only=True, base_ref=None, model=None, max_sentences=6)`) and have the CLI wrap it. This keeps business logic in one place and makes automated tests straightforward.
Action completed in this spec: a core function contract and CLI-wrapper pattern are now defined in implementation guidance.

7. Testability improvements:
Split implementation into pure functions for formatting and prompt assembly, plus adapter functions for git and Gemini execution. Then add tests for: staged-only default behavior, base ref comparisons, stdin-fed diffs, empty diff handling, and markdown output format compatibility with `do.md`.
Action completed in this spec: testability architecture and required test coverage are now specified.


# Revision prompt
Update the wsum command as described in bulle titems and sections marked (revised 2026-05-15) and make updates to the help-text also.
