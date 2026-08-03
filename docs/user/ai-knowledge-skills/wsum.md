# wsum

Summarizes git diff scope into do.md-ready markdown work summaries.

## Usage

```text
usage: wsum [-h] [--all | --update] [--base REF] [--model MODEL]
            [--max-sentences MAX_SENTENCES] [--stdin] [--file FILE_PATHS]
            [--extra-diff-arg EXTRA_DIFF_ARG]

Summarize git diff changes into work-summary markdown

options:
  -h, --help            show this help message and exit
  --all, -a             Include staged, tracked unstaged, and untracked
                        changes (dtask --all semantics)
  --update, -u          Include staged and tracked unstaged changes (matches
                        git add -u semantics)
  --base REF            Compare against a base ref (default: HEAD)
  --model MODEL         Gemini model name to use (example: gemini-2.5-pro)
  --max-sentences MAX_SENTENCES
                        Upper bound for sentence count guidance in the prompt
                        (default: 6)
  --stdin               Read diff from stdin even if stdin is a TTY
  --file FILE_PATHS     Limit diff to a specific path (repeatable)
  --extra-diff-arg EXTRA_DIFF_ARG
                        Additional validated git diff option (repeatable)
```

## Example

```bash
wsum --update --file docs/dev/work/do.md
```

# maintenance

Update this page with the prompt below:

"Refresh docs/user/ai-knowledge-skills/wsum.md from current CLI help output and dtask integration semantics. Keep option names exact and keep scope notes aligned with staged/update/all behavior."
