
# DDF Plugin Issues

## Tracking Heading Level, serializing, deserializing, and programs that manipulate the document.  
## issue: 
DDF keeps the leading '#' characters in headings in order to preserve the H-level.  This will be awkward in other systems that just keep data as objects or JSON.

## analysis: 
A way forward is to accept an architecture where external systems do not have the document, and local documents can use ddfTypes in sections and use IDs to match data shared with external systems to update local documents.  But this does not allow for JSON MDGBDF within DDF to suddenly allow free usage of section levels for stories, unless the '#' are retained.  Further, if a Story is at one heading level in a document like do.md, but a different heading level in something under docs/dev/spec, then the H level may be different.  So pushing story data into and out of external systems should not attempt to preserve format.
    Stories and tasks are data.
    *Place holder documents or sections* : Documents or sections that own a layout may have data injected into a custom layout one by one by ID, where there is an ID place holder for the data object.
    *Data List Documents or sections * : Documents may have lists of data, but should own the layout, such as the H-level that stories would be at.

    --> Therefore, 
        - the do.md '# Current Work' and '# Completed Work' sections fit the "lists of data" pattern above because a story will move between those sections.
        - the TODO.md must also be a flat list of Story objects.
                Why: if higher H level things like Goals or Epics, are written into TODO.md, operations like pop and unpop will mess them up when removing them or pushing them back into the document.  TODO.md *could* be structured as a place holder 

                TODO.md can have both Text Stories and Work Stories, but they have to all be at the same level.
                    That level will be he level below the heading that invokes ddfType=MDGBDF

## issue: Different treatment of headings between DDF and MDGBDF
DDF Documents are Documents First, and contain data, so keeping document form is important, and in DDF parsed sections, the '#' characters should be retained in the header.

MDGBDF Sections are data first, and may appear at different H-levels in different in different documents.
    --> Therefore,
        The enclosing DDFSection should keep its header and use the DDF method of knowing the H-level in the document.
            - when serializing within markdown/DDF, mdgbdata.py should be told the H-level of the enclosing section 
            - The H level of the enclosing section must be 0-5.  
            - H-level 6 enclosing a 7th level is an error because it may cause the header to be treated as regular text.


## issue: Bare task lists in DDF documents

The use case for this feature is to allow a file to be a very simple list of tasks, without any stories, to be parsed as MDGBDF.  

For a simple new project being built out rapidly, a user should be able to just start typing tasks in TODO.md.   The user surely will eventually elaborate and make some of them stories wit headings, but they shouldn't have to.  Quick prototyping for exampe may just be a bunch of tasks.  This would be a core use od dev-scripts, and a key start for users.

Can the template design, call for a plugin for preamble, or should it be passed in as a setting from the caller?

### DDF Markdown parsing
For a DDF markdown document, that has front matter at the beginning of the file, that set of front-matter key value pairs defines the attributes for the top level document.


#### preamble (Simplification)
If text is found before any H1 heading that isn't part of the Front-matter and its delimiters, that text is assumed to be the preamble for the document, and by default has no special parsing or processing.  The preamble attribute is of type String.

##### ddfType in preamble
A front-matter attribute 'ddfType' may be specified to before any section headings and if a plugin is registered that handles that type, the preamble text should be parsed with that plugin.  Since there is no section heading, the plugin must have a convention to find a value for the section heading.  The plugin should also deal with the lack of a heading on serialization, possibly stripping it out. 

A parser should accept an argument or command line parameter to tel it what the the preamble text ddfType is.

## issue: subsections in a single plugin call pass or separate calls?
Should a section with a special plugin be passed all subsections at lower levels to be parsed also? Or should each subsection be a call to the plugin to parse?
Answer: Each section should call a plugin if there is one.  The vision is that documents can commingle different types of sections.
 - some how, an app that uses a ddf document has to do what it is supposed to do with the sections it has a functional responsibility for.
    - get the tasks and stories.  dtask pop ans push
    - read a business process and build a document (using AI) to propose the 




# Plugin Design Analysis note.
The types and plug in's here are not functionally the same as MIME types or similar things for rendering markdown.  For DDF, Markdown is the presentation type. The parsers and serializer plugins are to expose object types to other scripts and software.

      