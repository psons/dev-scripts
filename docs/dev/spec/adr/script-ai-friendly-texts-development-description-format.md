# Development Description Format (DDF)
Development Description Format (DDF) should be a human author friendly text convention on top of Markdown to synthesize what do.md is being used for and TODO.md is being used for (writing stories and tasks).

The idea is that when writing markdown documents for specs and other things, stories and tasks can be included inline.

DDF extends MDGBDF to include text that are not Stories, in that they have no tasks or status to track.

## File Scoped Story
Files should be viewed as containing the following structure, which can be structured as a list of section / story objects:

'''
    A file scope Story that may be empty from the beginning of the file until an H1 section is encountered (matching ^#).  
    One or more non-file scope Stories    
'''

The File scope Story is different from the non file scope Stories as follows:
    It had no H1 at its beginning
    A front-matter section if found is the front-matter as will also be seen according to conventional front-matter rules.
    It's name is the filename stripped of any directory elements or file extension.

Tools parsing the DDF of a markdown file will yield an ordered list of Story objects matching the file order.

Every H1 in the markdown file causes a Story object to be created
Story objects that do not have any status or tasks are informational Story objects.

# Formalized DDF
Once parsed from the originally authored text format, DDF will be serialized in a more formal format.  MDGBDF describes a more formal treatment of Task Attributes.

Sections in DDF in can have key value attributes handled as Task.attributes are handled.
Informal DDF input can have task objects interspersed within the description.  When parsed, DDF will place task markers in the text of the decription propert where the tasks should be inserted when re-serializing the DDF document. 

## Task Markers 
Task Markers consist of a line matching:
'''
^\{task:{id}\}$
''' 
Where {id} is the ID if a task in the Tasks list.

If a Task does not have an {id} market in te description, it is serialized to the output DDF document after the description.

DECISION: Stories should support attributes when they are loaded to task and story systems. More sophisticated systems will have many attributes, though some will not support them.   

# Work Stories
Stories that have either Tasks or a Status to track are 'work Stories'.
If a markdown H1 heading section has tasks, but no Status was parsed from the header, it defaults to a 'do' status.   

# Whole Document Preservation
When a markdown document is read as DDF not text information will bew lost because all information will be preserved as a list of Stories.
 - If no H1 markers are found, the whole document will be read as a single file scoped Story.
 - If H1 markers are found, but there is content before the first H1, the content before the H1 marker will be in a a single file scoped Story, and subsequent H1 markers constitute a list of Stories.
 - If the file begins with an H1 marker, there is no file scoped story

# Symmetry of parsing and serialization.
Attributes read in according to the Informal rules of MDGBDF will not be serialized according to the formal rules, so parsing and serializing in this case is not symmetrical.

Once a file is converted to formal MDGBDF / DDF, its serialized markdown will be the same as the formal fomat that was read.

If a markdown document is saved as JSON, and then converted back to markdown the ordering of tasks and attributes must be the same, so json libraries ad methods that preserve object ordering must be used.

# See also
analysis/proposals/development-description-format-uses.md

# Action from this
See: docs/dev/spec/adr/dev-description-format.md 
