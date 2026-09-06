# ddf.py Phase 1 Specification: Development Description Format Parser and Serializer

## Document Status

**Status**: Authoritative  
**Version**: Phase 1  
**Last Updated**: 2026-08-27

This specification is the sole authoritative source for implementing `bin/ddf.py` Phase 1 in this repository. If any rule here differs from referenced source documents, this file takes precedence.

---

## Table of Contents

1. [Purpose](#purpose)
2. [Python Requirements](#python-requirements)
3. [DDF Object Model](#ddf-object-model)
4. [Markdown Parsing Rules](#markdown-parsing-rules)
5. [Front-Matter Handling](#front-matter-handling)
6. [Serialization Rules](#serialization-rules)
7. [API Surface](#api-surface)
8. [Command-Line Interface](#command-line-interface)
9. [Examples](#examples)
10. [Error Handling](#error-handling)
11. [Implementation Guidelines](#implementation-guidelines)
12. [Test Requirements](#test-requirements)
13. [Acceptance Criteria](#acceptance-criteria)

---

## Purpose

### Purpose of This Document

This specification defines the complete requirements for the `ddf.py` module Phase 1: a Python-based parser and serializer for Development Description Format (DDF) markdown documents.

**Key Goal**: Enable lossless round-trip conversion between markdown and structured object representation, so that any markdown document can be:
1. Parsed into an in-memory object model (`DDFDoc`)
2. Re-serialized to markdown with no content loss
3. Serialized to JSON for integration with APIs and services

### Purpose of ddf.py

The `ddf.py` module provides foundational document structure parsing that preserves all document content (front-matter, headings, nested sections, and body text) as structured data. This enables:

- **Script automation**: Local scripts can read, manipulate, and write structured markdown documents
- **AI integration**: Documents can be processed by AI while maintaining their original structure
- **Work management**: Tools like `dtask` can programmatically manage task lists in [do.md](../work/do.md) and [TODO.md](../work/TODO.md)
- **API integration**: Documents can be serialized to JSON for service APIs

### Implementation Phases

**Phase 1** (this spec): Basic DDF parsing and serialization
- Parse markdown documents to `DDFDoc` object model
- Support document and section front-matter (YAML)
- Support arbitrary heading nesting (H1-H6)
- Serialize to markdown and JSON with lossless round-trip

**Phase 2** (future - see [ddf-plugin-spec.md](./ddf-plugin-spec.md)): Plugin architecture
- Register plugins for specialized formats (e.g., MDGBDF for stories/tasks)
- Plugin-based section parsing via `ddfType` attribute
- Preserve specialized object models within DDF structure

**Phase 3** (future): Full MDGBDF compatibility
- Replace `mdgbdata.py` with `ddf.py` for all existing use cases
- Support story and task extraction/manipulation
- Backward compatibility with existing MDGBDF workflows

### Source Documents

This specification consolidates and supersedes content from:
- [ddf-basic-spec.md](./ddf-basic-spec.md)
- [development-description-format-uses.md](./usecases/development-description-format-uses.md)
- [script-ai-friendly-texts-development-description-format.md](./adr/script-ai-friendly-texts-development-description-format.md)

These documents provide background context only. This document is normative and self-contained for implementation.

---

## Python Requirements

### Python Version and Dependencies

- **Target Python**: 3.11+
- **Required external libraries**: 
  - `PyYAML` >= 6.0 (same library used by `bin/dtask`)
- **Required stdlib modules**: 
  - `typing`, `pathlib`, `json`, `re`, `dataclasses`, `sys`, `argparse`

### Installation

```bash
pip install pyyaml
```

---

## DDF Object Model

### Type Definitions

The DDF object model consists of two core types: `DDFDoc` (document) and `DDFSection` (section).

#### DDFDoc

Represents a complete DDF document.

```python
from dataclasses import dataclass, field
from typing import Any

@dataclass
class DDFDoc:
    """A complete DDF document with optional front-matter, preamble, and nested sections."""
    attributes: dict[str, Any] | None = None
    preamble: str | None = None
    sections: list['DDFSection'] = field(default_factory=list)
```

**Properties:**

- `attributes` (optional): Dictionary of YAML front-matter key-value pairs from the document start
- `preamble` (optional): Text content before the first heading (after front-matter if present)
- `sections`: Ordered list of top-level sections

**Rules:**

- If the document begins with `---` delimited YAML front-matter, it populates `attributes`
- Text between front-matter (or file start) and the first heading becomes `preamble`
- If no headings exist, all non-front-matter content is `preamble` with empty `sections`
- Document-level sections can be any heading level (H1-H6); nesting is determined by relative levels
- Empty preamble or attributes should be `None`, not empty string or empty dict

#### DDFSection

Represents a markdown section (any heading level H1-H6) with optional nested subsections.

```python
@dataclass
class DDFSection:
    """A markdown section with heading, optional attributes, preamble, and nested sections."""
    heading: str
    attributes: dict[str, Any] | None = None
    preamble: str | None = None
  sections: list['DDFSection'] | None = field(default_factory=list)
```

**Properties:**

- `heading` (required): The complete heading line including markers (e.g., `"## My Section"`)
- `attributes` (optional): Dictionary of YAML section front-matter key-value pairs
- `preamble` (optional): Text content after front-matter and before first subsection
- `sections` (optional): Ordered list of nested subsections (lower heading levels), or `None` when there are no nested subsections

**Rules:**

- Heading level is determined by counting leading `#` characters (1-6)
- Lines with >6 `#` characters are not valid headings and treated as regular text
- Section nesting follows heading hierarchy:
  - Lower-level headings (more `#`) nest within higher-level sections
  - Same or higher-level headings close the current section
  - Example: H3 nests under H2, but another H2 or H1 closes the current H2 section
- The `heading` property must store the complete heading line including `#` characters and text
- Parsers may use either an empty list or `None` when a section has no nested subsections

### JSON Schema Reference

The canonical JSON schema is maintained at:  
[ddf-object-structure.schema.json](./ddf-object-structure.schema.json)

This schema should be kept synchronized with the object model defined above.

---

## Markdown Parsing Rules

### Heading Detection

**Heading Pattern**: `^#{1,6}\s+(.+)$`

- Headings must start at the left margin (column 0)
- 1-6 `#` characters followed by at least one whitespace, then heading text
- Lines with >6 leading `#` characters are NOT headings and treated as regular text
- Trailing `#` characters in headings should be preserved as part of the heading text

**Heading Level**:
- Count leading `#` characters: H1 = `#`, H2 = `##`, ..., H6 = `######`
- Heading level determines nesting behavior

**Examples**:
```markdown
# H1 Heading           → level 1
## H2 Heading          → level 2
### H3 Heading         → level 3
#### H4 with trailing ##   → level 4 (trailing ## preserved in text)
####### Not a heading  → regular text (>6 #)
  ## Not a heading     → regular text (not at margin)
```

### Section Nesting Rules

Sections nest based on **relative** heading levels:

**Rule 1: Lower-level headings nest**
- When a heading has MORE `#` than current section → create nested subsection

**Rule 2: Same/higher-level headings close**
- When a heading has SAME or FEWER `#` than current section → close current, create sibling/parent

**Rule 3: First heading determines document sections**
- The first heading encountered defines the base level for `DDFDoc.sections`
- All subsequent same-level headings create sibling sections in `DDFDoc.sections`

**Example**:
```markdown
### First heading (H3)      → DDFDoc.sections[0]
#### Nested (H4)            → DDFDoc.sections[0].sections[0]
### Second heading (H3)     → DDFDoc.sections[1]
## Higher level (H2)        → DDFDoc.sections[2]
```

**Important**: The first heading can be ANY level (H1-H6). All subsequent headings nest relative to it.

### Document Preamble

Text before the first heading (excluding front-matter) becomes `DDFDoc.preamble`:

```markdown
---
title: My Doc
---
This is preamble text.
It appears before any heading.

# First Heading
This is in the section.
```

Result:
```python
DDFDoc(
    attributes={"title": "My Doc"},
    preamble="This is preamble text.\nIt appears before any heading.\n",
    sections=[DDFSection(heading="# First Heading", preamble="This is in the section.\n")]
)
```

### Section Preamble

Text after section front-matter and before first subsection becomes `DDFSection.preamble`:

```markdown
## Section

---
key: value
---

This is section preamble.

### Subsection
This is in the subsection.
```

Result:
```python
DDFSection(
    heading="## Section",
    attributes={"key": "value"},
    preamble="This is section preamble.\n",
    sections=[DDFSection(heading="### Subsection", preamble="This is in the subsection.\n")]
)
```

### Empty Document Handling

**No headings**: Document with no headings has all non-front-matter text as preamble

```markdown
---
title: Simple
---
Just some text.
No headings here.
```

Result:
```python
DDFDoc(
    attributes={"title": "Simple"},
    preamble="Just some text.\nNo headings here.\n",
    sections=[]
)
```

---

## Front-Matter Handling

### YAML Front-Matter Format

Front-matter is a YAML block delimited by `---` lines:

```markdown
---
key1: value1
key2: value2
nested:
  subkey: subvalue
---
```

### Document Front-Matter

**Location**: Must be at the very start of the file (column 0, line 1)

**Rules**:
1. Opens with `---` on its own line
2. Contains valid YAML mapping (dict/object)
3. Closes with `---` on its own line
4. Parsed with `yaml.safe_load()`
5. Becomes `DDFDoc.attributes`

**Invalid front-matter** (treated as regular text):
- Missing closing `---`
- YAML parsing error
- Not a mapping (e.g., YAML list or scalar)
- Not at file start (e.g., preceded by text)

### Section Front-Matter

**Location**: Immediately after section heading

**Rules**:
1. Same format as document front-matter
2. Opens with `---` on its own line immediately after heading
3. Contains valid YAML mapping
4. Closes with `---` on its own line
5. Parsed with `yaml.safe_load()`
6. Becomes `DDFSection.attributes`

**Example**:
```markdown
## My Section

---
status: active
priority: high
---

Section content here.
```

### Multiple Front-Matter Blocks

**Rule**: Only the FIRST valid front-matter block after a heading (or at document start) is parsed as attributes.

**Example - Second block becomes text**:
```markdown
---
doc: front-matter
---

Some text.

---
not: parsed
---

# Heading
```

Result: The second `---` block is part of `preamble` as regular text.

### YAML Parsing Semantics

- Use `yaml.safe_load()` from PyYAML
- All YAML types supported: strings, numbers, booleans, nulls, lists, nested maps
- Attribute values store parsed YAML objects, not raw text
- Quote delimiters in YAML are syntax only, not part of values

**Example**:
```yaml
---
string: "hello"
number: 42
boolean: true
null_value: null
list: [1, 2, 3]
---
```

Parsed attributes:
```python
{
    "string": "hello",        # str (quotes removed)
    "number": 42,              # int
    "boolean": True,           # bool
    "null_value": None,        # None
    "list": [1, 2, 3]          # list
}
```

---

## Serialization Rules

### Markdown Serialization

Convert `DDFDoc` back to markdown text with identical structure.

#### Document Front-Matter Output

If `DDFDoc.attributes` is not `None`:
```python
output = "---\n"
output += yaml.safe_dump(doc.attributes, default_flow_style=False, allow_unicode=True)
output += "---\n"
```

#### Preamble Output

If `DDFDoc.preamble` is not `None`:
```python
output += doc.preamble
if not doc.preamble.endswith('\n'):
    output += '\n'
```

#### Section Output (Recursive)

For each section in `sections`:
```python
def serialize_section(section: DDFSection) -> str:
    output = section.heading
    if not output.endswith('\n'):
        output += '\n'
    
    # Section front-matter
    if section.attributes:
        output += "\n---\n"
        output += yaml.safe_dump(section.attributes, ...)
        output += "---\n"
    
    # Section preamble
    if section.preamble:
        output += "\n" + section.preamble
    
    # Nested sections
    for subsection in section.sections or []:
        output += "\n" + serialize_section(subsection)
    
    return output
```

### JSON Serialization

Convert `DDFDoc` to JSON using standard Python `json.dumps()`:

```python
def doc_to_dict(doc: DDFDoc) -> dict:
    result = {}
    if doc.attributes is not None:
        result["attributes"] = doc.attributes
    if doc.preamble is not None:
        result["preamble"] = doc.preamble
    if doc.sections:
        result["sections"] = [section_to_dict(s) for s in doc.sections]
    return result

def section_to_dict(section: DDFSection) -> dict:
    result = {"heading": section.heading}
    if section.attributes is not None:
        result["attributes"] = section.attributes
    if section.preamble is not None:
        result["preamble"] = section.preamble
    if section.sections:
        result["sections"] = [section_to_dict(s) for s in section.sections]
    return result
```

Output with `json.dumps(doc_to_dict(doc), indent=2, ensure_ascii=False)`.

### JSON Deserialization

Parse JSON back to `DDFDoc`:

```python
def dict_to_doc(data: dict) -> DDFDoc:
    return DDFDoc(
        attributes=data.get("attributes"),
        preamble=data.get("preamble"),
        sections=[dict_to_section(s) for s in data.get("sections", [])]
    )

def dict_to_section(data: dict) -> DDFSection:
  sections = data.get("sections", [])
    return DDFSection(
        heading=data["heading"],  # required
        attributes=data.get("attributes"),
        preamble=data.get("preamble"),
    sections=None if sections is None else [dict_to_section(s) for s in sections]
    )
```

---

## API Surface

### Core Parsing Functions

#### parse_from_markdown

```python
def parse_from_markdown(text: str) -> DDFDoc:
    """
    Parse markdown text into a DDFDoc object.
    
    Args:
        text: Markdown text to parse
        
    Returns:
        DDFDoc object representing the parsed document
        
    Raises:
        ValueError: If YAML front-matter is invalid
    """
```

#### parse_from_markdown_file

```python
def parse_from_markdown_file(
    path: str | Path, 
    encoding: str = "utf-8"
) -> DDFDoc:
    """
    Parse a markdown file into a DDFDoc object.
    
    Args:
        path: Path to markdown file
        encoding: File encoding (default: utf-8)
        
    Returns:
        DDFDoc object representing the parsed document
        
    Raises:
        FileNotFoundError: If file doesn't exist
        UnicodeDecodeError: If file can't be decoded
        ValueError: If YAML front-matter is invalid
    """
```

#### parse_from_json

```python
def parse_from_json(text: str) -> DDFDoc:
    """
    Parse JSON text into a DDFDoc object.
    
    Args:
        text: JSON text conforming to DDF schema
        
    Returns:
        DDFDoc object
        
    Raises:
        json.JSONDecodeError: If JSON is invalid
        ValueError: If JSON doesn't match DDF schema
    """
```

#### parse_from_json_file

```python
def parse_from_json_file(
    path: str | Path,
    encoding: str = "utf-8"
) -> DDFDoc:
    """
    Parse a JSON file into a DDFDoc object.
    
    Args:
        path: Path to JSON file
        encoding: File encoding (default: utf-8)
        
    Returns:
        DDFDoc object
        
    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If JSON is invalid
        ValueError: If JSON doesn't match DDF schema
    """
```

### Core Serialization Functions

#### serialize_to_markdown

```python
def serialize_to_markdown(doc: DDFDoc) -> str:
    """
    Serialize a DDFDoc object to markdown text.
    
    Args:
        doc: DDFDoc object to serialize
        
    Returns:
        Markdown text representation
    """
```

#### serialize_to_markdown_file

```python
def serialize_to_markdown_file(
    doc: DDFDoc,
    path: str | Path,
    encoding: str = "utf-8"
) -> None:
    """
    Serialize a DDFDoc object to a markdown file.
    
    Args:
        doc: DDFDoc object to serialize
        path: Path to output file
        encoding: File encoding (default: utf-8)
    """
```

#### serialize_to_json

```python
def serialize_to_json(doc: DDFDoc, indent: int = 2) -> str:
    """
    Serialize a DDFDoc object to JSON text.
    
    Args:
        doc: DDFDoc object to serialize
        indent: JSON indentation (default: 2)
        
    Returns:
        JSON text representation
    """
```

#### serialize_to_json_file

```python
def serialize_to_json_file(
    doc: DDFDoc,
    path: str | Path,
    encoding: str = "utf-8",
    indent: int = 2
) -> None:
    """
    Serialize a DDFDoc object to a JSON file.
    
    Args:
        doc: DDFDoc object to serialize
        path: Path to output file
        encoding: File encoding (default: utf-8)
        indent: JSON indentation (default: 2)
    """
```

---

## Command-Line Interface

### Script Name

`bin/ddf.py` (or `bin/ddf`)

### Subcommands

#### tomd

Convert JSON to markdown.

```bash
ddf.py tomd [OPTIONS] [FILE]
```

**Arguments**:
- `FILE` (optional): Path to JSON file. If omitted, reads from stdin.

**Behavior**:
- Parse JSON as DDF document
- Output markdown to stdout
- Exit code 0 on success, 1 on error

**Example**:
```bash
# From file
ddf.py tomd input.json > output.md

# From stdin
cat input.json | ddf.py tomd > output.md
```

#### tojson

Convert markdown to JSON.

```bash
ddf.py tojson [OPTIONS] [FILE]
```

**Arguments**:
- `FILE` (optional): Path to markdown file. If omitted, reads from stdin.

**Behavior**:
- Parse markdown as DDF document
- Output JSON to stdout (pretty-printed with 2-space indent)
- Exit code 0 on success, 1 on error

**Example**:
```bash
# From file
ddf.py tojson input.md > output.json

# From stdin
cat input.md | ddf.py tojson > output.json
```

#### help

Display help message.

```bash
ddf.py help
ddf.py --help
ddf.py -h
```

**Behavior**:
- Print usage summary
- List all subcommands with descriptions
- Exit code 0

**Required Output Format**:
```
usage: ddf.py <subcommand> [options] [file]

Development Description Format (DDF) parser and serializer.

subcommands:
  tomd      Convert JSON to markdown
  tojson    Convert markdown to JSON
  help      Show this help message

For markdown ↔ JSON conversion with lossless round-trip.
Read from FILE or stdin if FILE is omitted.

Examples:
  ddf.py tojson doc.md > doc.json
  ddf.py tomd doc.json > doc.md
  cat doc.md | ddf.py tojson
```

### Error Handling

**Errors should output to stderr** with descriptive messages:

```bash
# File not found
ddf.py tojson missing.md
# stderr: Error: File not found: missing.md
# exit code: 1

# Invalid JSON
echo "not json" | ddf.py tomd
# stderr: Error: Invalid JSON: Expecting value: line 1 column 1 (char 0)
# exit code: 1

# Invalid YAML front-matter
echo -e "---\nnot: valid: yaml\n---" | ddf.py tojson
# stderr: Error: Invalid YAML front-matter: <yaml error details>
# exit code: 1
```

---

## Examples

### Example 1: Basic Document

**Input Markdown** ([normal-ddf.md](./usecases/ddf/normal-ddf.md)):
```markdown
---
attribute1: This is an attribute of the DDF document
---

This is text that is part of the document preamble because it is before any section headings.

### Non H-1 for Document.sections
Because this H-2 is before any H1, it this Section goes in the Document.sections[] list.
This text is part of the It should be Document.sections[0].preamble

#### Descending Header Content
---
attribute1: This is section front-mater.  In the DDF object it is Document.sections[0].sections[0].attributes.attribute1
--- 
Because this is descending to a lower level, it this section is part of the first entry in Document.sections.  
It should be Document.sections[0].sections[0].  This text is part of the It should be Document.sections[0].preamble

## Ascending Section header.
Because this H-2 is an ascending level (higher than any H-n level so far) it goes in the Document.sections[] list
as Document.sections[1].  This block of text is the Document.sections[1].preamble

# First H1 Section header.
This section header is the first H1, so no further Ascension of the heading level is possible, and all subsequent entries in the 
Document.sections list will be H1 level.  Further, all lower section levels will be nested within those sections.
This texti is part of is Document.sections[2].preamble

# Second H1 Section header
This section header is the second H1, but would be Document.sections[3].
```

**Output JSON** ([normal-ddf.json](./usecases/ddf/normal-ddf.json)):
```json
{
  "attributes": {
    "attribute1": "This is an attribute of the DDF document"
  },
  "preamble": "This is text that is part of the document preamble because it is before any section headings.",
  "sections": [
    {
      "heading": "### Non H-1 for Document.sections",
      "preamble": "Because this H-2 is before any H1, it this Section goes in the Document.sections[] list.\nThis text is part of the It should be Document.sections[0].preamble",
      "sections": [
        {
          "heading": "#### Descending Header Content",
          "attributes": {
            "attribute1": "This is section front-mater.  In the DDF object it is Document.sections[0].sections[0].attributes.attribute1"
          },
          "preamble": "Because this is descending to a lower level, it this section is part of the first entry in Document.sections.\nIt should be Document.sections[0].sections[0].  This text is part of the It should be Document.sections[0].preamble"
        }
      ]
    },
    {
      "heading": "## Ascending Section header.",
      "preamble": "Because this H-2 is an ascending level (higher than any H-n level so far) it goes in the Document.sections[] list\nas Document.sections[1].  This block of text is the Document.sections[1].preamble"
    },
    {
      "heading": "# First H1 Section header.",
      "preamble": "This section header is the first H1, so no further Ascension of the heading level is possible, and all subsequent entries in the \nDocument.sections list will be H1 level.  Further, all lower section levels will be nested within those sections.\nThis texti is part of is Document.sections[2].preamble"
    },
    {
      "heading": "# Second H1 Section header",
      "preamble": "This section header is the second H1, but would be Document.sections[3]."
    }
  ]
}
```

### Example 2: Multiple Front-Matter Blocks

**Input**:
```markdown
---
attrib1: value1
---
raw text
---
attrib2: value2
---
## a section
```

**Output**:
```json
{
  "attributes": {
    "attrib1": "value1"
  },
  "preamble": "raw text\n---\nattrib2: value2\n---\n",
  "sections": [
    {
      "heading": "## a section"
    }
  ]
}
```

**Explanation**: Only the first front-matter block is parsed. The second becomes part of preamble text.

### Example 3: No Headings

**Input**:
```markdown
---
title: Simple Doc
---
Just plain text.
No sections.
```

**Output**:
```json
{
  "attributes": {
    "title": "Simple Doc"
  },
  "preamble": "Just plain text.\nNo sections.\n"
}
```

### Example 4: Section with Front-Matter

**Input**:
```markdown
# My Section

---
status: active
priority: high
---

Section content here.

## Subsection
More content.
```

**Output**:
```json
{
  "sections": [
    {
      "heading": "# My Section",
      "attributes": {
        "status": "active",
        "priority": "high"
      },
      "preamble": "Section content here.\n",
      "sections": [
        {
          "heading": "## Subsection",
          "preamble": "More content.\n"
        }
      ]
    }
  ]
}
```

---

## Error Handling

### Required Error Behavior

1. **Invalid YAML front-matter**: Raise `ValueError` with YAML error details
2. **File not found**: Raise `FileNotFoundError` with path
3. **Encoding errors**: Propagate `UnicodeDecodeError`
4. **Invalid JSON**: Raise `json.JSONDecodeError`
5. **Missing required fields in JSON**: Raise `ValueError` naming the field

### Parser Robustness

**Never raise errors for**:
- Unmatched markdown lines (treat as text)
- Empty documents
- Documents with no headings
- Missing optional properties (attributes, preamble)
- Any valid markdown structure

### CLI Error Output

- Write errors to **stderr**, not stdout
- Include descriptive error messages
- Exit with code **1** on error, **0** on success

---

## Implementation Guidelines

### Performance

- **Single-pass parsing**: Parse input in O(n) time with one pass over lines
- **Avoid recursion**: Use iterative parsing with explicit state
- **Compile regex once**: Compile heading pattern once per parse call

### Code Organization

**Recommended structure**:
```python
# bin/ddf.py

# 1. Imports and dataclasses
from dataclasses import dataclass, field
from typing import Any
import yaml, json, re, sys, argparse
from pathlib import Path

# 2. Data model
@dataclass
class DDFDoc: ...
@dataclass
class DDFSection: ...

# 3. Parsing functions
def parse_from_markdown(text: str) -> DDFDoc: ...
def parse_from_markdown_file(path, encoding) -> DDFDoc: ...
def parse_from_json(text: str) -> DDFDoc: ...
def parse_from_json_file(path, encoding) -> DDFDoc: ...

# 4. Serialization functions
def serialize_to_markdown(doc: DDFDoc) -> str: ...
def serialize_to_markdown_file(doc, path, encoding): ...
def serialize_to_json(doc: DDFDoc, indent) -> str: ...
def serialize_to_json_file(doc, path, encoding, indent): ...

# 5. Helper functions
def _extract_front_matter(lines: list[str]) -> tuple[dict | None, int]: ...
def _get_heading_level(line: str) -> int | None: ...
def _parse_sections(lines: list[str], start: int, base_level: int) -> list[DDFSection]: ...

# 6. CLI
def main(argv: list[str] | None = None) -> int: ...

if __name__ == "__main__":
    sys.exit(main())
```

### Module Docstring

Include this at the top of `bin/ddf.py`:

```python
"""ddf.py - Development Description Format parser and serializer.

This module provides lossless parsing and serialization for DDF markdown documents.
DDF preserves all document structure (front-matter, headings, sections, text) as
structured data for script automation and API integration.

Usage as module:
    from ddf import parse_from_markdown, serialize_to_json
    doc = parse_from_markdown(text)
    json_output = serialize_to_json(doc)

Usage as command:
    python ddf.py tojson doc.md > doc.json
    python ddf.py tomd doc.json > doc.md
"""
```

---

## Test Requirements

### Test Coverage

Implement tests in `tests/test_ddf.py` covering:

#### 1. Basic Parsing
- Document with front-matter
- Document without front-matter
- Document with preamble
- Document without headings
- Single section
- Multiple sections at same level
- Nested sections

#### 2. Heading Nesting
- H3 as first heading
- H1 following H3 (ascending)
- H4 following H2 (descending)
- Multiple nesting levels
- Adjacent same-level sections

#### 3. Front-Matter
- Valid YAML object
- YAML with nested structures
- YAML with lists
- YAML with various scalar types
- Invalid YAML (should fail)
- Missing closing `---` (treated as text)
- Second front-matter block (treated as text)

#### 4. Section Front-Matter
- Section with front-matter
- Multiple sections with front-matter
- Nested section with front-matter

#### 5. Round-Trip
- Parse markdown → serialize markdown (should match)
- Parse markdown → serialize JSON → parse JSON → serialize markdown (should match)

#### 6. Edge Cases
- Empty file
- File with only front-matter
- File with only preamble
- Lines with >6 `#` characters
- Headings not at margin
- Unicode content
- Windows line endings (`\r\n`)

#### 7. Error Handling
- Invalid YAML syntax
- Invalid JSON input
- Missing file

#### 8. Acceptance Test
- Parse [normal-ddf.md](./usecases/ddf/normal-ddf.md)
- Verify output matches [normal-ddf.json](./usecases/ddf/normal-ddf.json)

### Test Framework

Use `pytest`:

```bash
pytest tests/test_ddf.py -v
```

---

## Acceptance Criteria

This specification is considered complete and implementation is accepted when:

1. ✅ `bin/ddf.py` implements all required functions with correct signatures
2. ✅ Parsing behavior follows all rules in this specification
3. ✅ Serialization produces correct markdown and JSON output
4. ✅ Round-trip conversion is lossless (markdown → object → markdown preserves content)
5. ✅ Command-line interface works as specified
6. ✅ All test cases pass under `pytest`
7. ✅ Acceptance test parses [normal-ddf.md](./usecases/ddf/normal-ddf.md) correctly
8. ✅ Error handling behaves as specified

---

## Version History

- **2026-08-27**: Phase 1 specification created (this document)
- Earlier drafts: [ddf-basic-spec.md](./ddf-basic-spec.md), [ddf-spec.md](./ddf-spec.md)
