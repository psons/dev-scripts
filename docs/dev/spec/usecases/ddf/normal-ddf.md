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