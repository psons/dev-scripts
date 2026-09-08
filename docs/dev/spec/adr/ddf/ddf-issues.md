
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

For a simple new project being built out rapidly, a user should be able to just start typing tasks in TODO.md.   The user surely will eventually elaborate and make some of them stories wit headings, but they shouldn't have to.  Quick prototyping for example may just be a bunch of tasks.  This would be a core use of dev-scripts, and a key start for users.

Can the template design, call for a plugin for preamble, or should it be passed in as a setting from the caller? In any case, the calling program is responsible.

### DDF Markdown parsing
For a DDF markdown document, that has front matter at the beginning of the file, that set of front-matter key value pairs defines the attributes for the top level document.


#### preamble (Simplification)
If text is found before any H1 heading that isn't part of the Front-matter and its delimiters, that text is assumed to be the preamble for the document, and by default has no special parsing or processing.  The preamble attribute is of type String.

##### ddfType in preamble
A front-matter attribute 'ddfType' may be specified to before any section headings and if a plugin is registered that handles that type, the preamble text should be parsed with that plugin.  Since there is no section heading, the plugin must have a convention to find a value for the section heading.  The plugin should also deal with the lack of a heading on serialization, possibly stripping it out. 

A parser should accept an argument or command line parameter to tel it what the the preamble text ddfType is.

## issue: subsections in a single plugin call pass or separate calls?
Should a section with a special plugin be passed all subsections at lower levels to be parsed also? Or should each subsection be a call to the plugin to parse?
Answer: For current Feature iteration, same or descending H levels should be passed to the same plugin call.  MDGBDF will make gbdataStory and gbdata.Task structures preserving sub heading levels in the description text.

The future vision is that documents can commingle different types of sections.
 - some how, an app that uses a ddf document has to do what it is supposed to do with the sections it has a functional responsibility for.
    - get the tasks and stories.  dtask pop and push
    - read a business process and build a document (using AI) to propose the Business Process Information Graph (BPIG). 
    - what other analytical steps and artifacts might run scripts as side affects and might use DDF to anchor those scripts?

### Thinking:
From A DDF perspective and a user expectation, any Section object will have any subsection nested inside of it.  So the returned objects **should** be nested within it in the domain model.
Presently no gbdata.Story within a gbdata.Story  
- gb-data.Story does not have any 'sections?: [],' property, and can not store Stories (or any other sections) within Stories.  Elsewhere (such as in Goal Blotter) there is some desire to have more, or even un unbounded number of levels to the decomposition model TPB->Goal(s)->Story(ies)->Task(s).  
  - HTML and Markdown imposes a practical constraint of 6 heading levels
  - Stories nested within another story must drop down one heading level.
  - There is no need to limit to the number of stories that may appear at the 1 level down nesting level.
  - gb-data should be enhanced in the future to have something like a 'sections?: [],' property.  Perhaps it would be good to use a name like "subParts" to escape the markdown sections and headers semantic.
  - there is no support for higher parts of the gb-data model such as "Goal" or "Time Priority Block:" (TPB) in MDGBDF, but it could be added formally or in user structures to DDF by callng the file or directory the TPB, and using a file or H1 as the Goal.  These things could also be managed as attributes on stories or even tasks.   A Task Warrior plugin likely would use attributes, and not support the nesting of stories within stories. 
    - See https://github.com/psons/gb-data/blob/main/docs/ar-spec/Work-Hierarchy-Goal-Story-Task.md   
#### for the current iteration
---
status: accepted
statusNote: check the rules against existing MDGBDF behavior and try to align.
statusDate: 2026-09-06
---
##### Current state Story
 - A story may have subsections (Lower H level headings)
    - currently MDGBDF only supports H1 level stories, and that has to change as part of this work.
        1 - - Stories cannot nest. A heading deeper than current story level is part of description text, 

##### Current state Task

    - A task may have headings, but they must be lower than the H-level of the story 
 not a new story, and they are not parsed
        2 - Task detail definition:
        
```
- `detail` is all subsequent lines excluding parsed object front-matter, until one of: 
    -a heading at the same or higher level than the current story. 
```
### Decisions

#### For the current iteration (Feature "workBranch": "plugin-ddf" )
By default, any section encountered uses the same parser and context as the "parent object" and enclosing section.  This means by default it is the same object as MDGBDF currently does.
 - New, the Story pattern won't always be an H1, as already specified elsewhere.

The gb-data model remains unchanged, so there is no nested sections still.

With no nested Object model, or separate lower down plugins called by plugins, the whole section text will be passed to the plugin according to the rules DDF rules, but the object model built is different:
    - Descending H levels are passes to the parser, but the MDGBDF plugin puts the text in gbdata.Story.Description text, and sifts out the tasks to  gbdata.Story.tasks
    - Same or ascending sections begin a new Section object.
For comparison, this excerpt from ddf-spec.md
``` 
    - Sections lower than that level should be passed as text to the parser for that section. i.e. descending sections should be nested.
    - Same or ascending sections are not nested.  

```

#### For future 
Parsing should check each time a section header is encountered to see if a template match, or a ddfType attribute is calling for a different parser plugin, and such parsing would return an object with a  'sections?: [],' list.
    - This would define full DDF compatibility and implies a needed improvement either to make the gb-data model to be an extension of the DDF model, or to duck type the DDFSection and the gbdata.Story and gbdata.Task together into objects that still serialize ad Markdown, and JSON, andstill can interact with the Goal Blotter API(s)s. 
    - This would require likely enhancements to the state that get's passed to a DDF plugin:  For example would a call to DDF plugin by MDGBDF be allowed, and could it create a story under a Task?  It would either need to know to throw an error, or support it with a new set of business rules allowing a whole hierarchy to be nested with in another hierarchy.  Markdown H levels would run out quickly and it may amount o embedding a document within a document. 



# Plugin Design Analysis note.
The types and plug in's here are not functionally the same as MIME types or similar things for rendering markdown.  For DDF, Markdown is the presentation type. The parsers and serializer plugins are to expose object types to other scripts and software.

      