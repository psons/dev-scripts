
# DDF Plugin Issues

## issue: How should heading level be tracked for document sections and data sections? 
DDF keeps the leading '#' characters in headings in order to preserve the H-level.  This will be awkward in other systems that just keep data as objects or JSON.


### Thinking: 
A way forward is to accept an architecture where external systems do not have the document, and local documents can use ddfTypes in sections and use IDs to match data shared with external systems to update local documents.  But this does not allow for JSON MDGBDF within DDF to suddenly allow free usage of section levels for stories, unless the '#' are retained.  Further, if a Story is at one heading level in a document like do.md, but a different heading level in something under docs/dev/spec, then the H level may be different.  So pushing story data into and out of external systems should not attempt to preserve format.

Concept: 
 - DDF documents keep Absolute H-levels, and use the '#' characters in headings to do it.
 - MDGBDF and other section parsers use H levee relative to enclosing sections

### Decisions
---
status: accepted
statusDate: 2026-08-06
---

    Stories and tasks are data.

    Definition: *Place holder documents or sections* : Documents or sections that own a layout may have data injected into a custom layout one by one by ID, where there is an ID place holder for the data object.

    Definition:  *Data List Documents or sections * : Documents may have lists of data, but the documents should own the layout, including such attributes as the H-level that stories would be at.

    --> Therefore, 
        - the do.md is itself a document and may have sections at varying levels.
            - The '# Current Work' and '# Completed Work' sections fit the "lists of data" pattern above.  Any given story may also appear in other documents at other levels.  The list of stories may appear at H2 in do.md, but H1 in TODO.md, and even H3, 4, 5, or 6 in some other document containing analysis relevant for the story.

        - the Stories in TODO.md must also be a flat list of Story objects.
                Why: if higher H level things like Goals or Epics, are written into TODO.md, operations like pop and unpop will mess them up when removing them or pushing them back into the document.  TODO.md *could* be structured as a place holder 

                TODO.md can have both Text Stories and Work Stories, but they have to all be at the same level.
                    That level will be he level below the heading that invokes ddfType=MDGBDF
#### For the current iteration 
---
status: accepted
statusDate: 2026-09-14
---
TODO.md will be a flat list of H1 stories

Some stories in TODO.md are text Stories, used tro preserve content that is not part of Work Stories.

#### For future 
---
status: accepted
statusDate: 2026-09-14
---
TODO.md may be a DDF documet with a '# Backlog' Heading section that contains stories.


## issue: Different treatment of headings between DDF and MDGBDF
### Decisions
---
status: accepted
---

DDF Documents are Documents First, and contain data, so keeping document form is important, and in DDF parsed sections, the '#' characters should be retained in the header.

MDGBDF Sections are data first, and may appear at different H-levels in different in different documents.
    --> Therefore,
        The enclosing DDFSection should keep its header and use the DDF method of knowing the H-level in the document.
            - when serializing within markdown/DDF, mdgbdata.py should be told the H-level of the enclosing section 
            - The H level of the enclosing section must be 0-5.  
            - H-level 6 enclosing a 7th level is an error because it may cause the header to be treated as regular text.


## issue: Bare task lists in DDF documents
### Decisions
---
status: open
statusDate: 2026-09-11
---

See backlog stories/d-bare-task-lists-in-ddf.md

The use case for this feature is to allow a file to be a very simple list of tasks, without any stories, to be parsed as MDGBDF.  

For a simple new project being built out rapidly, a user should be able to just start typing tasks in TODO.md.   The user surely will eventually elaborate and make some of them stories wit headings, but they shouldn't have to.  Quick prototyping for example may just be a bunch of tasks.  This would be a core use of dev-scripts, and a key start for users.

Can the template design, call for a plugin for preamble, or should it be passed in as a setting from the caller? In any case, the calling program is responsible.

#### DDF Markdown parsing
For a DDF markdown document, that has front matter at the beginning of the file, that set of front-matter key value pairs defines the attributes for the top level document.


#### preamble (Simplification)
If text is found before any H1 heading that isn't part of the Front-matter and its delimiters, that text is assumed to be the preamble for the document, and by default has no special parsing or processing.  The preamble attribute is of type String.

##### ddfType in preamble
A front-matter attribute 'ddfType' may be specified to before any section headings and if a plugin is registered that handles that type, the preamble text should be parsed with that plugin.  Since there is no section heading, the plugin must have a convention to find a value for the section heading.  The plugin should also deal with the lack of a heading on serialization, possibly stripping it out. 

A parser should accept an argument or command line parameter to tell it what the the preamble text ddfType is.

## issue: Should subsections of a plugin parsed section all be passed to the plugin?
Should a section with a special plugin be passed all subsections at lower levels to be parsed also? Or should each subsection be a call to the plugin to parse?
### Thinking:
From A DDF perspective and a user expectation, any Section object will have any subsection nested inside of it.  So the returned objects **should** be nested within it in the domain model.

Presently no gbdata.Story within a gbdata.Story  
- gb-data.Story does not have any 'sections?: [],' property, and can not store Stories (or any other sections) within Stories.  Elsewhere (such as in Goal Blotter) there is some desire to have more, or even un unbounded number of levels to the decomposition model TPB->Goal(s)->Story(ies)->Task(s).  
  - HTML and Markdown imposes a practical constraint of 6 heading levels
  - Stories nested within another story must drop down one heading level.
  - There is no need to limit to the number of stories that may appear at the 1 level down nesting level.
  - gb-data should be enhanced in the future to have something like a 'sections?: [],' property.  Perhaps it would be good to use a name like "subParts" to escape the markdown sections and headers semantic.
  - there is no support for higher parts of the gb-data model such as "Goal" or "Time Priority Block:" (TPB) in MDGBDF, but it could be added formally or in user structures to DDF by calling the file or directory the TPB, and using a file or H1 as the Goal.  These things could also be managed as attributes on stories or even tasks.   A Task Warrior plugin likely would use attributes, and not support the nesting of stories within stories. 
    - See https://github.com/psons/gb-data/blob/main/docs/ar-spec/Work-Hierarchy-Goal-Story-Task.md   

The future vision is that documents can commingle different types of sections.
 - some how, an app that uses a ddf document has to do what it is supposed to do with the sections it has a functional responsibility for. Here are some use cases:
    - get the tasks and stories.  dtask pop and push
    - read a business process and build a document (using AI) to propose the Business Process Information Graph (BPIG). 
    - what other analytical steps and artifacts might run scripts as side affects and might use DDF to anchor those scripts?

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
    
### Decisions

#### For the current iteration
Answer: For current Feature iteration, same or descending H levels should be passed to the same plugin call.  MDGBDF will make gbdataStory and gbdata.Task structures preserving sub heading levels in the description text.

#### For future 
---
status: accepted
statusDate: 2026-09-11
---

By default, any section encountered uses the same parser and context as the "parent object" and enclosing section.  This means by default it is the same object as MDGBDF currently does.
 - New, the Story pattern won't always be an H1, as already specified elsewhere.

The gb-data model remains unchanged, so there is no nested sections still.

With no nested Object model, and no lower down plugins called by plugins, the whole section text will be passed to the plugin according to the DDF rules, but the object built by parsing it is different between MDGBDF and DDF.  For MDGBDF:
    - Descending H levels are passed to the parser, but the MDGBDF plugin puts the text in gbdata.Story.Description text, and sifts out the tasks as gbdata.Story.tasks
    - Same or ascending sections begin a new Story object.
For comparison, this excerpt from ddf-spec.md
``` 
    - Sections lower than that level should be passed as text to the parser for that section. i.e. descending sections should be nested.
    - Same or ascending sections are not nested.  
```

#### For future 
---
status: pending
statusNote: Still thinking about the requirements driver for this
statusDate: 2026-09-14
---
Parsing should check each time a section header is encountered to see if a template match, or a ddfType attribute is calling for a different parser plugin, and such parsing would return an object with a  'sections?: [],' list.
    - This would define full DDF compatibility and implies a needed improvement either to make the gb-data model to be an extension of the DDF model, or to duck type the DDFSection and the gbdata.Story and gbdata.Task together into objects that still serialize asd Markdown, and JSON, and still can interact with the Goal Blotter API(s)s. 
    - This would require likely enhancements to the state that get's passed to a DDF plugin:  For example would a call to DDF plugin by MDGBDF be allowed, and could it create a story under a Task?  It would either need to know to throw an error, or support it with a new set of business rules allowing a whole hierarchy to be nested with in another hierarchy.  Markdown H levels would run out quickly and it may amount o embedding a document within a document. 

## issue: Should the section returned by mdgbdata.py be a DDFSection with preamble?
The section returned has to have a shape compliant as a DDF section.  Should it be an actual DDFSection?  Should text before the first Story object be in preamble of the returned DDFSection?

The current --final spec has mdgbdata stories assigned to a semantically appropriate 'stories:' attribute instead of using the 'sections:' attribute of the parent class.  Should the the plugin object write data that can be serialized an parsed as DDF even if the more specific plugin type is not available? 

### Thinking:
At present, a gbdata.Story serialized to Markdown is also a section.  A gbdata.Task serialized to markdown is not a section.

mdgbdata.py only has types compatible with the gbdata schema, and currently represents whole documents without loss of content as stories.   mdgbdata.py does not use preamble attributes, but rather stores Preamble content in a text story at the beginning of the list.

    Nested consideration: if an MDGBDF parser or serializer is not present, the stories attribute can not be handled without raising an error because it is an object, not a simple attribute value.
    --> Could Stories and Tasks be designed to be parsed and serialized as generic DDF sections if a DDF parser ad serializer is not present? 
        --> Proposal: Yes with the limitation that if a markdown document is loaded into memory as a DDFDocument ad DDF sections even though it contains stories and tasks, it sould be parsed to DDF, and re-serialized to DDF such that he re-serialized DDF could still be parsed with a DDF parser using an MDGBDF plugin, and the stories and tasks would till be intact.  
        --> likewise, if a parser uses an MDGBDF plugin to load a document, then an MDGBDF serializer is needed too, so that special model attributes like 'stories' and H-level will be handled correctly.

### Decisions:
---
status: accepted
statusDate: 2026-09-11
---

A plugin does not need to store content in memory using a model that is compatible with DDF as ling as it can both parse and serialize the content to both markdown and JSON.

The 'class MDGBDFSection(DDFSection):' may use a stories attribute to hold stories instead of using the 'sections' attribute of te base class.

In an MDGBDF section 
```markdown
when text precedes the first heading at `story_heading_level`
```
a plugin may store the text in some way other than using the DDFSection.preamble

#### for the current iteration
The ddfmdgbdf.py plugin will use the gbdata compatible text Story as the first story in a 'list of Stories' instead of the DDFSection.preamble for text preceding the first heading at at `story_heading_level`.


## issue: Should plugins be able to call other plugins??
### Decisions
#### For the current iteration
---
status: accepted
statusDate: 2026-09-11
---
No.  Plugin calling is flat, non nested, per above, descending H levels will be passed to the same parser.
#### For future 
---
status: accepted
statusDate: 2026-09-11
---
Yes.  For example a small DDF document may be nested inside a Story, and support other embedded document types.

# Plugin Design Analysis note.
The types and plug in's here are not functionally the same as MIME types or similar things for rendering markdown.  For DDF, Markdown is the presentation type. The parsers and serializer plugins are to expose object types to other scripts and software.

      