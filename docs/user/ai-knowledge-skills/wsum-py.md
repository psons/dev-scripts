# wsum.py

Python module entrypoint for wsum command-line behavior.

## Usage

```text
usage: wsum [-h] [--all | --update] [--base REF] [--model MODEL]
            [--max-sentences MAX_SENTENCES] [--stdin] [--file FILE_PATHS]
            [--extra-diff-arg EXTRA_DIFF_ARG]

Summarize git diff changes into work-summary markdown
```

## Notes

- This command interface matches wsum.
- Maintain one canonical behavior definition in wsum docs and keep this page as a focused alias/reference.

## Example

```bash
wsum.py --base HEAD~1 --max-sentences 5
```

# maintenance

Update this page with the prompt below:

"Refresh docs/user/ai-knowledge-skills/wsum-py.md to mirror current wsum.py CLI parity with wsum. Keep this page short and reference the main wsum page for full option detail."
