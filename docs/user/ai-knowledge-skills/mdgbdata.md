# mdgbdata.py

Converter between Markdown GB Data Form and JSON representations.

## Usage

```text
usage: mdgbdata [-h] {tojson,tomd,help} ...

Convert Markdown GB Data Form to and from JSON

positional arguments:
  {tojson,tomd,help}
    tojson            Convert Markdown GB Data Form to JSON
    tomd              Convert JSON to Markdown GB Data Form
    help              Show command usage summary

options:
  -h, --help          show this help message and exit
```

## Example

```bash
mdgbdata.py tojson docs/dev/work/TODO.md
```

# maintenance

Update this page with the prompt below:

"Refresh docs/user/ai-knowledge-skills/mdgbdata.md from current CLI help output and conversion behavior. Keep subcommands accurate and concise."
