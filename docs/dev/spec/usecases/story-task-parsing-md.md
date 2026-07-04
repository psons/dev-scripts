# Context / Background
That module also contains domain data model for the gb-data schema.

Stories and tasks authored within markdown files per this doc should be available vis the bin/gbdata.py module to a backlog.py plugin implementation that will provide abilities to read and possibly write tasks.

# Stories
Users should quickly begin to enumerate tasks in a markdown file to begin analyzing and executing work.

Tasks should be easy to group into stories.

Some times in writing a a spec, a user begins to write stories inside the spec because sometimes there is little or no distinction between the wording of a use case, and the wording of the same idea written as a story description. For small focused efforts, it can be nice to keep them in the same file.

Story headers are the ^# text lines that match the patterns based on the gb-data enums.

Lines following a story header that are not part of a story or new mark down section at the same level or higher constitute the description of the story.

Stories objects may not be nested in other story objects, so a story header found at a lower heading level within a story should be treated as part of the story description, not a new story.

The story header contains a story status and a story name.


# tasks
Tasks headers are text than matches the task status metadata pattern enums.

Lines following a task header that are not part of a a new task, story, or non-story mark down section at the same level or higher than te current story constitute the description of the task.

Task objects may not be nested in other task objects.

Tasks can be written bare without stories, but it makes organizing them hard, and they end up in some default collection. If they really don't have a story, users should open an unnamed section with ^#, ^##, ^###, ^####, ^#####, ^###### corresponding to the 6 heading levels supported by markdown.

The task header contains a task status and a task name.


## non tasks
Tasks are part of the heading section they are in, and always are anchored at the left margin.   Task-like leaders that are not at the left margin are microsected parts of a task, or possibly a preliminary breakdown of story definition work.

# Non pattern matched stories 
A heading that is not part of a previous story that contains tasks is a story even if it does not match a pattern. This is a corner case where a story must be created to hold tasks under that heading. The heading line should be used for the name of the story.

If the heading text does not match a story status pattern, the story still exists and a default story status of 'do' must be applied.

A heading has '[Ss]tory: ' as the the first or second non-white space string after '^#' is a story even id it doesn't have any tasks under it.

The next heading after the heading that begins a story that is the same level as a story is the beginning of something else, and is not part of the same story.

# the `id` property.
if the string `id:` appears at the left margin immediately after a story or task header, then the next non-whitespace strring after the `:` charachter should be treated as he `id` property for the story or task.

users should not set the `id`, and should allow mdgbdata.py to assign the ID.