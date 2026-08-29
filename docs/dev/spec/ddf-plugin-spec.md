## Specialized Plugins to parse or serialize sections

### Parsing with Plugins
The DDF parser in some cases must pass responsibility for the parsing of a section to a specialized plugin.  ddf.py must determine the ddfType and use the ddfType to identify a parser / serializer plugin to use. 

The ddfType is determined either by an attribute in the document or a template provided by the calling program.

The plugin is determined by searching a ddfType plugin registry.

If a plugin is registered that handles the ddfType, the section header and text up to but not including any of the following will be passed to the plugin to parse:
 - A header of the same H level
 - end of file or end of input

The plugin returns an object type of DDFSection, or a class derived from DDFSection.

### Plugin Registry
The plugin registry will be hard coded for Phase 2 and Phase 3, and will only include module mdgbdf to parse ddfType MDGBDF.

### Determining DDF type 
A DDF parsing template can be made available to the parser as a map of heading patterns Types, or an attribute can set the ddfType.  Patterns me be regular expressions, or literals.

#### DDF Template example.
<Buid out a prototype of do.md see Issues below>



sections containing front-matter attributes may contain an attribute 'ddfType' and if a plugin is registered that handles that type, the section header and text will passed to the plugin to return the section object.

If no plugin is registered for the type, or there is no template pattern match or type attribute, the section is parsed as a DDF Section. 

The parsing template is a map of (pattern, ddfType) pairs where order in the map represents precedence if there is more than pattern that may match a heading in the document being parsed.

### Serializing with Plugins
The object model should include the ddfType of the DDFSection or derived class.

Serializing a DDFSection oa a class derived from DDFSection to JSON must yield an Object, not a list.

#### DDF Markdown Serialization.
See analysis in docs/dev/spec/adr/ddf/ddf-issues.md
The enclosing DDFSection should keep its header and use the DDF method of knowing the H-level in the document.
- when serializing within markdown/DDF, The call to the plugin must pass the H-level of the enclosing DDFSection. 
- The H level of the enclosing section must be 0-5.  
- H-level 6 enclosing a 7th level is an error because it may cause the header to be treated as regular text.



# =============  review and assimilate below

### Calling program design.
Observe that a plugin may be called based on a ddfType attribute *internal* to the document, or a template *external* to the document. An error should be raised if a ddfType attribute is provided and differs from a template that has been provided.

The default type, if there is no template pattern match or attributes.ddfType is DDF.

# Plugin Registration

# DDF Markdown parsing
For a DDF markdown document, that has front matter at the beginning of the file, that set of front-matter key value pairs defines the attributes for the top level document.


## preamble (Simplification)
If text is found before any H1 heading that isn't part of the Front-matter and its delimiters, that text is assumed to be the preamble for the document, and by default has no special parsing or processing.  The preamble attribute is of type String.

### ddfType in preamble
A front-matter attribute 'ddfType' may be specified to before any section headings and if a plugin is registered that handles that type, the preamble text should be parsed with that plugin.  Since there is no section heading, the plugin must have a convention to find a value for the section heading.  The plugin should also deal with the lack of a heading on serialization, possibly stripping it out. 

A parser should accept an argument or command line parameter to tel it what the the preamble text ddfType is.

The use case for this feature is to allow a file to be a very simple list of tasks, without any stories, to be parsed as MDGBDF.  

# Design Analysis note.
The types and plug in's here are not functionally the same as MIME types or similar things for rendering markdown.  For DDF, Markdown is the presentation type. The parsers and serializer plugins are to expose object types to other scripts and software.

# =============  review and assimilate above 

# MDGBDF within DDF Documents

MDGBDF sections must return an object, not a list, so the list[Story] returned by mdgbdata.py must be enclosed in a type derived from DDFSection.

When called as a ddf plugin, the story heading pattern must be updated in mdgbdata.py to allow non H1 headings to be recognized as stories.

