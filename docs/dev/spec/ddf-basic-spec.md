To fulfil backlog item in stories/ddf-work.md

A goal of this spec is to get a Development Description Format (DDF) parser / serializer that will accept all markdown so that it could be parsed to an in memory object model and then re-serialized as either markdown or json with no loss of content from the originally read document.  

Another Goal of this spec is to allow for lower section parsing below the H1 level, such as for do.md, which has 'Current work' and 'Completed work' as H1 sections, and has story sections within them at H2 or lower.

Consistent with this goal, all *Object Front-matter* as defined in mdgbdata-spec.md becomes *parsed object front-matter*. (i.e. there is no longer any distinction between H1 an other heading levels) 

## Sections before the First H1
Sections before the first H1 are added to the Sections list.

Once an H-n section is encountered, that is not an H1, 
    - Sections lower than that level should be passed as text to the parser for that section. i.e. descending sections should be nested.
    - Same or ascending sections are not nested.  

### DDF Sections deduce their h-level 
DDF Sections deduce their h-level objects in the memory model by pattern matching the heading string, thus it is not necessary to create empty nesting levels for an H6 to directly follow an H1.
This is why the heading string is required. If it were niot required, all sections would need an attribute in serialized text to indicate the heading level. 

# DDF Object Structure

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


#### The Document Object
    may or may not have a name.
    Document front-matter defines the attributes.
    Text before any H-n headings is the Document.preamble.

    Any H-n heading causes a section object to be created and appended to the section list by passing in all text until an H- line is detected at the same or higher -n level, or end of input is reached.
        lines with more that 6 '#' characters should be treated as part of Document.text, not as section headings.   Creating a section with such headings will cause an error.
    
    When a same or higher -n level is found, a new section object is created by passing in all subsequent text until an H- line is detected at the same or higher -n level, or end of input is reached.
    
Observe that the H-n levels in the Document.sections list are always the same or ascending.

#### Sections Objects 
    Must have a heading, even if it is only a string of '#' characters.
        The number of '#' character determines the -n level of the section and may not be larger than 6.
        More than 6 '#' characters beginning a heading are an error an should not have been passed into a section constructor.

    Section front-matter defines the attributes.

    Any H-n heading causes a section object to be created and appended to the section list by passing in all text until any H- line is detected, or end of input is reached.
        If an H- line was detected and is at the same or higher -n level, an error should be raised. (It should not have been passed in ti his Section)
        If an H- line was detected and is at a lower -n level, a sub Section object should be created and appended to the Section.sections list, by passing in all subsequent text until another H- line of the new lower -n level is detected, or end of input is reached.
    
Observe that the H-n levels in the Section.sections list are always the same level, because lower -n levels cause nesting into Section.sections.sections.  Higher level will not be passed in.


# DDF parsing design

### Parser behaviors
The calling program (module or script) will tell the parser that this is by default document to be parsed as text/markdown/DDF.

The DDF will by default parse documents as DDF, a top level object 

An additional spec docs/dev/spec/ddf-plugin-spec.md will address how sections may be passed to more specialized parsers and serializers to create and serialize specialized objects.


### Future issue
The document object has no tracking of the parsed section levels if the  

## H1 headings define sections (Simplification)
If a document has no H1 headings, all of it's non-front-matter text is the preamble 

The first H1 and all subsequent H1 lines define the document sections


# Cases

## Basic File example
The ddf parser should parse the contents of docs/dev/spec/usecases/ddf/normal-ddf.md to yield the 
JSON contents in docs/dev/spec/usecases/ddf/normal-ddf.json

## Additional examples
File begins with two front1matter blocks (not separated by content or a header)

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
