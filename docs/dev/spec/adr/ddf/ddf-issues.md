
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

      