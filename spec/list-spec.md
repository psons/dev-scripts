list is a python script that manipulates string lists that are either delimited values on a single line or newline separated lines.

```
Usage: list [options]  <command> [data...]

where options include:
    -f <filename>
        filename is the file to read
    -d <delimiter>
        delimiter is the value to separate lits tems o a single line

<command> is one of:
    flat    reads stdin by default and replaces newlines with the delimiter
            Output is a single line with the list values separated by the delimiter.

    tall    reads stdin by default and replaces the delimiter with newlines
            Output is a set of lines with each line containing a list item.

Example:

echo a b c | list tall
a
b
c

echo a:b:c | list -d : tall
a
b
c

echo "a
b
c" | list flat
a b c

echo a:b:c | list -d : tall
a
b
c

```