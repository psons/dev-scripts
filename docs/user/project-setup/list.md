# list

Utility for converting between delimited flat lists and newline-delimited tall lists.

## Usage

```text
usage: list [-h] [-f FILENAME] [-d DELIMITER] [--save LIST_NAME]
            [--load LIST_NAME]
            {flat,tall} [args ...]

Manipulate string lists that are either delimited values on a single line or
newline separated lines

positional arguments:
  {flat,tall}           flat: convert newlines to delimiter; tall: convert
                        delimiter to newlines
  args                  list items as command line arguments (when provided,
                        stdin is ignored)

options:
  -h, --help            show this help message and exit
  -f, --file FILENAME   filename to read from
  -d, --delimiter DELIMITER
                        delimiter for list items on a single line (default:
                        space)
  --save LIST_NAME      save the output to a named list in ~/.lists/
  --load LIST_NAME      load a named list from ~/.lists/
```

## Example

```bash
printf 'alpha\nbeta\ngamma\n' | list tall -d ','
```

# maintenance

Update this page with the prompt below:

"Refresh docs/user/project-setup/list.md from current list CLI help output. Keep examples concise and maintain exact option names and meanings from --help."
