## Specialized Plugins to parse sections
A DDF parsing template can be made available to the parser as a map of heading patterns Types.  

If a plugin is registered that handles that type, the section object and content will be handled to the plugin to return the Section object. 

with matching plugins to recognize and parse markdown sections.

sections containing front-matter attributes may contain an attribute 'ddfType' and if a plugin is registered that handles that type, the section object and content will be handled to the plugin to return the content object.

If no plugin is registered for the type, or there is no template pattern match or type attribute, the section is parsed as a DDF Section. 

### Calling program functionality.
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