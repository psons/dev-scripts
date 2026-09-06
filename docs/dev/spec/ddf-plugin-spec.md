## Specialized Plugins to parse or serialize sections

### Parsing and Serializing with Plugins
The DDF parser in some cases must pass responsibility for the parsing of a section to a specialized plugin.  
The ddf.py script must determine the ddfType and use the ddfType to identify a plugin to use for parsing and serialization. 
 - The ddfType is determined either by an attribute in the document or a template provided by the calling program.
 - The plugin is determined by searching for the ddfType in the plugin registry.

#### Default
If no plugin is registered for the type, or there is no template pattern match or type attribute, the section is parsed as a DDF Section. 

#### Parsing Call
If a plugin is registered that handles the ddfType, the section header and text up to but not including any of the following will be passed to the plugin to parse:
 - A header of the same H level
 - end of file or end of input

#### Parsing Return
When parsing, the plugin returns an object type of DDFSection, or a class derived from DDFSection.

#### Model Requirements

##### Heading Level
The DDFSection should keep its header and use the DDF method of knowing the H-level in the document.
- when serializing within markdown/DDF, The call to the plugin must pass the H-level of the enclosing DDFSection. 
- The H level of the enclosing section must be 0-5.  
- H-level 6 enclosing a 7th level is an error because it may cause the header to be treated as regular text.

##### ddfType
The object model for DDFSection or derived class should include the ddfType determined at run time separate from any attribute that may be present.  
Template DDF types supersede attributes that are discovered, and a warning should be printed if a ddfType Attribute is being ignored.  
The ignored ddfType attribute should be preserved.

##### Design background
---TODO, move this section
The reason to preserve DDF type attributes even if they are being ignored, is that some other program may use or even update the document, and need the ddfType as set.
TRhe reason te template takes precedence is that a calling program may be the owner of the document, and require a specific plugin for program functionality or validation, and may even need to add content in an expected conventional place in the document. 

#### Serialization Call
When serializing, the entire DDFSection object will be passed to the plugin. (See **Model Requirements above**)

#### Serialization Return

When serializing a DDFSection or a class derived from DDFSection to JSON, the text returned by the plugin must form a valid JSON Object, not a list.

When serializing a DDFSection or a class derived from DDFSection to markdown, the text returned by the plugin must form a markdown Section with a header. 

### Plugin Registry
The plugin registry will be hard coded for Phase 2 and Phase 3, and will only include module mdgbdf to parse ddfType MDGBDF.
DDF is built in an supported without a plugin.

### Determining DDF type 
A DDF parsing template can be made available to the parser as a map of regular expression heading patterns keys and ddfTypes as values, or an attribute can set the ddfType for a section.
The The template order represents precedence if there is more than pattern that may match a heading in the document being parsed.

#### Document template creation
User documentation must describe how to write DDF templates, including the pattern syntax, rule precedence, and how to escape regular-expression special characters that are intended to match literally.

#### DDF Template example for do.md used by dtask

```yaml
# YAML DDF template text example for do.md
rules:
  - pattern: '^# Current work\s*$'
    ddfType: MDGBDF

  - pattern: '^# Completed Work\s*$'
    ddfType: MDGBDF
```

#### The ddfType Attribute
sections may contain an attribute 'ddfType' and if a plugin is registered that handles that type, the section header and text will passed to the plugin to return the section object.


### Calling program design.
Observe that a plugin may be called based on a ddfType attribute *internal* to the document, or a template *external* to the document, therefore it will be necessary to parse the header and object front-matter to see if there is a ddfType, and than in some cases pass the header and front-matter to a plugin that may parse them a second time and extract additional information when building a DDFSection. 

# =============  Need Review below.

# MDGBDF within DDF Documents

MDGBDF sections must return an object, not a list, so the list[Story] returned by mdgbdata.py must be enclosed in a type derived from DDFSection.

When called as a ddf plugin, the story heading pattern must be updated in mdgbdata.py to allow non H1 headings to be recognized as stories.


# User Acceptance example
---
prompt1: create a JSON file docs/dev/spec/usecases/ddf/do-dot-md-example.json that would result from running ddf.py tojson on the file docs/dev/spec/usecases/ddf/do-dot-md-example.md using the ddf template example from the section above titled '#### DDF Template example for do.md used by dtask'
---