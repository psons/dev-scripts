
# backlog.py
Implement backlog.py as a command module according to the pattern docs/dev/spec/python-command-module-pattern.md.

backlog.py should invoke plugin modules to implement the 'Backlog Plugin Protocols'.

## Plugin modules
backlog.py should support a plugin architecture that uses typing.Protocol to define the capabilities needed by backlog.

backlog_types.py should be created to define the types needed by backlog.py and any plugins.

### Integration with plugins

#### Support of Protocols by plugins
plugins should use the @runtime_checkable decorator so that backlog.py can use isinstance() to determine if required protocols are implemented by a plugin, and raise an error as appropriate to the user. 

#### Plugin selection
backlog.py should support a --provider flag to indicate which plugin to use.

If the --provider flag is not present, use a string value from the environment setting BACKLOG_PROVIDER to determine which plugin to use.

If BACKLOG_PROVIDER is not set, default to bltodo.

#### Future Plugins
Other possible future plugins are to implement the backlog protocols against:
 - Taskwarrior as bltw.py
 - Jira as bljira.py
 - Goal Blotter as blgb.py

## Backlog Plugin Protocols

* Prioritized implements prioritized which returns a listing of tasks, which are assumed to be in priority order
* PopTask implements pop_task which returns the highest priority task
* PopStory implements pop_story which returns the highest priority story, including all of its tasks. If there are no Stories, but there are tasks, an anonymous story with only a task list is returned.

## Future Backlog Plugin Protocols
These plugin protocols are not to be implemented yet, but are enumerated here for design planning.

* UpdateTask implements update_task which finds the task with the same id as the task argument and replaces it in the backlog attribute by attribute.  The previous state will be save in some TBD way.

* UpdateStory implements update_story which finds the Story with same id as the required Story argument and replaces it in the backlog attribute by attribute including the full list of stories.  The previous state will be save in some TBD way.


## subcommands of backlog.py 


# bltodo.py - The default plugin.

bltodo.py should be created to implement the first plugin.

bltodo.py should use the pattern docs/dev/spec/python-command-module-pattern.md.

bltodo.py will be a plugin that  
 - implements the 'Backlog Plugin Protocols'
 - uses gbdata.py to read (and in the future write) tasks and stories from (and in the future to) a markdown TODO.md file.

 The path to the TODO.md file can be passed on the command line with a --todofile option

If the --todofile option is not present, use a string value from the environment setting BL_TODO_FILE to determine which the todo file path.

If BL_TODO_FILE is not set, default to the path relative to the running program file ../docs/dev/work/TODO.md.

 ## bltodo.py command line

bltodo.py supports a subcommand for each of the 'Backlog Plugin Protocols'

bltodo.py supports a load subcommand which takes a in-file argument, and writes the TODO file in 'Markdown GB Data Form' (MDGBDF)
 - the load subcommand supports a --dryrun option that writes the staory and task data to stdout as MDGBDF.

All command invocations reports the full absolute path for the TODO file it is using on stdout.
 
With no arguments, bltodo.py runs the pop_story subcommand.
 - The output is the returned object written in its Markdown serialized form.

# Output Format -'Markdown GB Data Form' (MDGBDF)
MDGBDF is described in docs/dev/spec/mdgbdata-spec.md.


## potential data loss from files not already in Markdown Story Form
Markdown files may contain content that is not part of stories and tasks.
Initial implementations of bltodo.py will not have the capability to update or recreate files that are not already in 'Markdown GB Data Form'.  Therefore the load subcommand can be used to create TODO.md, from stories in other files, but not write back to those files. 


 
