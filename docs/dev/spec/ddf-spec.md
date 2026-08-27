# ddf.py Code-Ready Specification (Markdown Parsing)

## Purpose
### Purpose of Doc
This specification should be the sole specification for the ddf.py module.

A goal of this spec is to get a Development Description Format (DDF) parser / serializer that will accept all markdown so that it could be parsed to an in memory object model and then re-serialized as either markdown or json with no loss of content from the originally read document.  

### Purpose of ddf.py

When complete and tested, the ddf module is to be called in all cases that currently call mdgbdf.py.
There adoption will be in phases as functional improvements are iteratively made to the basic ddf capability.

#### Implementation Phases
ddf.py will allow markdown documents to be read into an object model to be used by scripts, and then serialized back to markdown, or serialized to JSON to integrate local documents with service APIs 

In the end phase, ddf.py will have the capability to invoke mdgbdata.py as a module to parse sections of text to the object model it supports. 

The first phase, currently covered by this spec addresses only the ability to parse and serialize a basic DDF object model specified here.

A second phase will allow ddf.py to call mdgbdata.py as a module to parse and serialize document sections to its more specialized object model, and include them in context as objects within the DDF model. 

A third phase will support the needs of scripts that currently use mdgbdata.py, enabling them to call ddf.py instead to preserve the DDF document content, and also efficiently extract and update MDGBDF data in documents.


### Sources

This document uses the following sources and is to be maintained as the single source of truth for implementation of `bin/mdgbdata.py` in this repository.:

- [Basic Spec](../spec/ddf-basic-spec.md)
- [docs/dev/spec/usecases/development-description-format-uses.md](http://./usecases/development-description-format-uses.md)  
- [docs/dev/spec/adr/script-ai-friendly-texts-development-description-format.md](http://./adr/script-ai-friendly-texts-development-description-format.md)  
- [docs/dev/spec/gbdata-spec-2.md](http://./gbdata-spec-2.md)

Source files above are background context only. This document is normative and intentionally self-contained for implementation and test work.

### Output

`bin/mdgbdata.py` must be generated from this document.

`bin/mdgbdata.py` owns the implementation of MDGBDF parsing and serialization, and JSON parsing and serialization for the shared gb-data model.

### Module Requirements

The module must:

- Provide status metadata loading and status detection utilities using repository metadata files.  
- Provide MDGBDF markdown parsing that builds ordered `Story` objects containing optional `Task` objects.  
- Provide MDGBDF serialization that outputs markdown text from ordered `Story` objects and preserves non-task informational story content.  
- Provide JSON parsing and serialization for the gb-data schema representation of those objects.  
- Import domain classes from `bin/gbdata.py` so parsing output uses the shared gb-data model.  
- Expose an API to external modules to   
  - write json given a file name and an ordered list of story objects  
  - write markdown given a file name and an ordered list of story objects  
  - return a list of story objects given a markdown file.  
  - return a list of story objects given a JSON file.  
  - allow optional filtering of story objects to include only work stories for methods that return lists of stories.

The format described in this document that will be read and written by `bin/mdgbdata.py` will be referred to in other specifications as 'Markdown GB Data Form' (MDGBDF).

### Command line Requirements

Commandline support should be provided by `bin/mdgbdata.py`for the following sub commands:

tojson

   will read a file whose path is given as a command line argument, or is read from stdin if no path argument is given, and is presumed to be 'Markdown Development Description Format' and output JSON text representing a DDF Documet object conforming to the schema https://github.com/psons/dev-scripts/blob/main/docs/dev/spec/ddf-object-structure.schema.json

tomd

   will read a file whose path is given as a command line argument, or is read from stdin if no path argument is given, and is presumed to be json conforming to the schema https://github.com/psons/gb-data/blob/main/goalBlotter.schema.json and output Markdown Development Description Format'

   if the input file is not valid json, raise an error. 

help

   will print a command usage summary for all subcommands and subcommand options.

   The help output must include every supported subcommand and, for each subcommand,
   list all supported options for that subcommand.

   Example requirement: if `--option` is supported by `tojson` and `tomd`, then help
   output must show `--option` under both `tojson` and `tomd`.

Subcommand options should be supported as follows:

    There are no subcommand options at this time.

## Module Boundary

`ddf.py` owns markdown/text parsing and serialization behavior for DDF.

for the future plugin architecture `mdgbdata.py` owns markdown/text parsing and serialization behavior for MDGBDF.

## Inputs and Dependencies


### Python Version and Libraries

- Target Python: 3.11+  
- Required libraries include: `PyYAML` (same library used by `bin/dtask`).  
- Required stdlib modules include: `typing`, `pathlib`, `json`, `re`, `hashlib`.

`bin/ddf.py` requires `PyYAML` for front-matter parsing and serialization.

### Required Functions

Implement utility functions:


## Markdown Parsing Requirements: definition of DDF
### =========================================================================

Development Description Format (DDF) is defined here.

A Goal of this spec is to allow for lower section parsing below the H1 level, such as for do.md, which has 'Current work' and 'Completed work' as H1 sections, After more advanced phases of ddf.py,  stories in do.md can be nested under the H1 '# Current Work' or '#Completed Work' sections andstill be treated as MDGBDF. H2 or lower.

Consistent with this goal, *Object Front-matter* will be parsed after any level of H section.  In  mdgbdata-spec.md terms, all *Object Front-matter* becomes *parsed object front-matter*. (i.e. there is no longer any distinction between H1 an other heading levels) 

### Sections before the First H1
Sections before the first H1 are added to the Sections list.

Once an H-n section is encountered, that is not an H1, 
    - Sections lower than that level should be passed as text to the parser for that section. i.e. descending sections should be nested.
    - Same or ascending sections are not nested.  

#### DDF Sections deduce their h-level 
DDF Sections deduce their h-level objects in the memory model by pattern matching the heading string, thus it is not necessary to create empty nesting levels for an H6 to directly follow an H1.
This is why the heading string is required. If it were niot required, all sections would need an attribute in serialized text to indicate the heading level. 

## DDF Object Structure

The object schema docs/dev/spec/ddf-object-structure.schema.json should be maintained from this section of the spec.
DDF documents have the shape
{
attributes?: {},
preamble?: String,
sections?: [],
}

A trailing `?` means the property is optional and may be omitted.

The sections list is a list of objects.

Sections have an object shape: 
    {
        heading: String
        attributes?: {}
        preamble?: String,
        sections?: [],
    }

The sections list is a list of objects.


##### The Document Object
    may or may not have a name.
    Document front-matter defines the attributes.
    Text before any H-n headings is the Document.preamble.

    Any H-n heading causes a section object to be created and appended to the section list by passing in all text until an H- line is detected at the same or higher -n level, or end of input is reached.
        lines with more that 6 '#' characters should be treated as part of Document.text, not as section headings.   Creating a section with such headings will cause an error.
    
    When a same or higher -n level is found, a new section object is created by passing in all subsequent text until an H- line is detected at the same or higher -n level, or end of input is reached.
    
Observe that the H-n levels in the Document.sections list are always the same or ascending.

##### Sections Objects 
    Must have a heading, even if it is only a string of '#' characters.
        The number of '#' character determines the -n level of the section and may not be larger than 6.
        More than 6 '#' characters beginning a heading are an error an should not have been passed into a section constructor.

    Section front-matter defines the attributes.

    Any H-n heading causes a section object to be created and appended to the section list by passing in all text until any H- line is detected, or end of input is reached.
        If an H- line was detected and is at the same or higher -n level, an error should be raised. (It should not have been passed in ti his Section)
        If an H- line was detected and is at a lower -n level, a sub Section object should be created and appended to the Section.sections list, by passing in all subsequent text until another H- line of the new lower -n level is detected, or end of input is reached.
    
Observe that the H-n levels in the Section.sections list are always the same level, because lower -n levels cause nesting into Section.sections.sections.  Higher level will not be passed in.


## DDF parsing design

### Parser behaviors
The calling program (module or script) will tell the parser that this is by default document to be parsed as text/markdown/DDF.

The DDF will by default parse documents as DDF, a top level object 

An additional spec docs/dev/spec/plugin-ddf-spec.md will address how sections may be passed to more specialized parsers and serializers to create and serialize specialized objects.


#### Future issue
The document object has no tracking of the parsed section levels if the  

## No Headings
If a document has no H1 headings, all of it's non-front-matter text is the preamble 

The first H1 and all subsequent H1 lines define the document sections

## Cases

### Basic File example
The ddf parser should parse the contents of docs/dev/spec/usecases/ddf/normal-ddf.md to yield the 
JSON contents in docs/dev/spec/usecases/ddf/normal-ddf.json

### Additional examples
File begins with two front-matter blocks (not separated by content or a header)

File has front-matter, then raw text, then front-matter
    The second front-matter block is treated as raw text in the document preamble. 

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
```json
    {
    "attributes": {
        "attrib1": "value1",
    },
    "preamble": "raw text
    ---
    attrib2: value2
    ---
    ",
    "sections": [
        {
          "heading": "## a section"  
        }
    ],
    }
```

# =========================================================================
### Standalone Contract

This section is sufficient to implement and test `bin/ddf.py` without reading other documents. If any rule here differs from referenced source documents, this file takes precedence for this repository.

### Scope

`ddf.py` must include a parser focused on producing full ddf documents structures from markdown content.

Required entry points:

1. `parse_from_markdown(text: str) -> DDFDoc`  

2. `parse_from_markdown_file(path: str | Path, encoding: str = "utf-8") -> DDFDoc`

1. `parse_from_json(text: str) -> DDFDoc`  

2. `parse_from_json_file(path: str | Path, encoding: str = "utf-8") -> DDFDoc`

The file variant reads text then delegates to the text variant.

DDF parser/serializer scope must preserve whole-document information as a DDF Document.

### Markdown Interpretation Rules DDF

All markdown behavior required for implementation is specified below.

Any markdown H1 to H6 line starts a new section. 

Interpretation details:

- Heading marker must be at left margin to be considered a heading (`^#{1,6}\\s+`).  


#### Section

- Parsed markdown Sections default `attributes` to `None` if no Ad hoc attributes are found.

#### Properties and Attributes For Sections 
##### Model Terminology

***definition***: object property \- any key and its value that is explicitly supported in the data model schema.

***definition***: object attribute \- any key and its value that is not explicitly supported in the data model schema, but rather stored in the set of keys and values comprising an attributes object. 

YAML key/value pairs embedded in object front-matter are considered Object properties and Object attributes for DDFDoc and Section.

##### Parsing Terminology

###### *Informal key: value notation*

- Informal Markdown input must support a single-line `key: value` form.  
- A  `key: value`  line is recognized when non-whitespace text begins at the left margin and is followed by a colon.  
- The key is the non-whitespace text starting at the beginning of the line and ending with the character before the colon.  
- The value is the text after the colon up to the end of the line.  
- informal `key: value` definitions may appear anywhere in a task or story other than the header or the object front-matter section.

Informal ‘key: value’ notation can be used to parse object attributes and object properties, but will not be used for serializing object attributes and object properties. 

###### *Object Front-matter*

***definition***:   
object front-matter \- a block of text that is 

- delimited by lines matching the regex '`^---\W*$`'   
- as the first line excluding the header of a Story or a Task

  Object front-matter is to be interpreted as YAML

***definition***: parsed object front-matter \- object front-matter that is used for properties and attributes and is removed from text used for preamble values. 

In markdown documents, conventional front-matter is the special sub case of Object front-matter where there is no text before the first front-matter delimiter.

Formal Markdown input rules use real YAML parsing through `yaml.safe_load` (PyYAML), matching the YAML library usage in `bin/dtask`.

Front-matter parsing behavior:

- Parse the block as YAML object mapping.  
- Parse all keys and scalar values for properties and attributes using normal YAML semantics from `yaml.safe_load`.  
- Property and attribute values stored in the data model must be the parsed YAML values, not raw markdown token text.  
- A `---`\-delimited block qualifies as object front-matter only when it closes with a matching `---` delimiter and parses as a YAML object mapping.  
- If a `---`\-delimited block does not qualify as object front-matter (for example: missing closing delimiter, YAML parse error, or non-mapping YAML), it must be preserved as ordinary markdown text in the current section preamble

Pattern:  
```` ``` ````  
`# Section Heading`  
`---`  
`key: value`  
`key2: value2`  
`---`  
`Section body text.`  
`Example (a work summary entry inside # Work Summary):`

`# 2026-05-19 12:26`  
`---`  
`"workHeadline": "refactor(dtask): simplify do.md work summary insertion"`  
`---`  
`This update streamlines the dtask script's handling of work summary insertions.`  
```` ``` ````

##### Front-matter 
Object front-matter notation can be used to parse object attributes and object properties, and is also the way to serialize object attributes and object properties.



#### Task Header Detection


#### Formal Markdown Output Rules for properties and attributes

When attributes are serialized as markdown, they must be written as YAML front-matter using the object front-matter rules above.

Serialization behavior:

- Section or Document attributes are serialized inside a front-matter block immediately after the story header.  
- A front-matter block opens with `---` and closes with `---` on the left margin.  
- Front-matter is serialized with PyYAML (`yaml.safe_dump`) using block-style mapping and insertion-order key preservation.  
- Attribute serialization must follow normal YAML scalar quoting behavior as emitted by `yaml.safe_dump`.

JSON serialization behavior for YAML-derived attributes:

- Values parsed from YAML front-matter must be serialized to JSON using their parsed property and attribute values from the gb-data model.  
- JSON output must reflect YAML parsing semantics (for example, quote delimiters used only for YAML syntax are not part of the resulting string value).


## API Surface



## Error Handling

- Invalid metadata entry object shape: raise `ValueError` naming key and missing field.  
- File decode errors in markdown file parser: propagate `UnicodeDecodeError`.  
- Invalid YAML front-matter blocks: raise `ValueError`.

Parser robustness rules:

- Never raise for unmatched lines; treat as descriptive text.  
- Never raise for empty markdown; return empty list.  

## Implementation Notes

- Keep parsing algorithm single-pass over input lines (`O(n)`).  
- Avoid recursive parser design; use explicit state variables.  
- Compile regex once per parse call.  
- include this doc string for the file:  
  - “The program name mdgbdata is a mnemonic that stands for *Mark Down / Goal Blotter Data* since it is a parser and serializer for the 'Markdown GB Data Form' (MDGBDF)”

## Test Requirements for `tests/`

At minimum, include tests for:

5. YAML property mapping  
        
9. DDF whole-document preservation  
     
   - content before first any H level is preserved in Document preamble  
   - file with no H level headings is represented aDDF Document with no sections  
   - parsing then serializing preserves preamble text 

## Acceptance Criteria

This spec is accepted when:

1. A generated `bin/mdgbdata.py` exposes all required functions/types with required signatures.  
2. Parsing behavior follows this document.  
4. Tests covering parsing and metadata behavior pass under `pytest`.  

