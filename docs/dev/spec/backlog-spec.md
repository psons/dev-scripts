
# backlog.py
Implement backlog.py as a command module according to the pattern docs/dev/spec/python-command-module-pattern.md.

backlog.py should invoke plugin modules to implement the 'Backlog Plugin Protocols' below.

## Plugin modules
backlog.py should support a plugin architecture that uses typing.Protocol to define the capabilities needed by backlog.

### Integration with plugins

#### Support of Protocols by plugins
plugins should use the @runtime_checkable decorator so that backlog.py can use isinstance() to determine if required protocols are implemented by a plugin, and raise an error as appropriate to the user. 

#### Plugin selection
backlog.py should support a --provider flag to indicate which plugin to use.

If the --provider flag is not present, use a string value from the environment setting BACKLOG_PROVIDER to determine which plugin to use.

If BACKLOG_PROVIDER is not set, default to bltodo.

#### Planning Roadmap:
The default plugin 
##### Future Plugins
Other possible future plugins are to implement the backlog protocols against:
 - Taskwarrior as bltw.py
 - Jira as bljira.py
 - Goal Blotter as blgb.py



## Backlog Plugin Protocols

The functions implementing the 'Backlog Plugin Protocols' should return types defined in bin/gbdata.py


* Prioritized implements prioritized which returns a listing of tasks, which are assumed to be in priority order
* PopTask implements pop_task which returns the highest priority task
* PopStory implements pop_story which returns the highest priority story, including all of its tasks. If there are no Stories, but there are tasks, an anonymous story that contains the task list is returned, and other attributes of the story are not set.

## Future Backlog Plugin Protocols
These plugin protocols are not to be implemented yet, but are enumerated here for design planning.

* UpdateTask implements update_task which finds the task with the same id as the task argument and replaces it in the backlog attribute by attribute.  The previous state will be save in some TBD way.

* UpdateStory implements update_story which finds the Story with same id as the required Story argument and replaces it in the backlog attribute by attribute including the full list of stories.  The previous state will be save in some TBD way.

* Load implements load, which takes a required URL argument of which defaults to the protocol and syntax forms supported by the plugin.  Load defaults rto the file:: protocol and the bltodo.py plugin.    portion of the URL if no protocol is specified, and  

## subcommands of backlog.py 
The subcommands output the data from the corresponding protocol methods according to the following options:
    --mdgbdf: outputs data as MDGBDF using a public API method of mdgbdf.py.
    --json: outputs data as JSON  using a public API method of mdgbdf.py.

The sub command prioritized invokes the 'prioritized' method of the Prioritized protocol of the configured backlog plugin. 
The sub command poptask invokes the 'pop_task' method of the PopTask protocol of the configured backlog plugin.
The sub command popstory invokes the 'pop_story' method of the PopStory protocol of the configured backlog plugin.

The help subcommand outputs a usage summary of subcommands and options.

# plugins do not implement user command line parsing and options
See docs/dev/spec/adr/relationship between CLI and plugin modules.md

# bltodo.py - The default plugin.

bltodo.py should be created to implement the first plugin.

bltodo.py will be a plugin that  
 - implements the 'Backlog Plugin Protocols'
 - uses mdgbdata.py to read (and in the future write) tasks and stories from (and in the future to) a markdown TODO.md file.

The path to the todo file can be set using and environment variable BL_TODO_FILE

If BL_TODO_FILE is not set, default to the path relative to the running program file ../docs/dev/work/TODO.md.

unit tests should be provided that do not read or write the ocs/dev/work/TODO.md file in the source repository.

bltodo.py provides an API function for each  of the 'Backlog Plugin Protocols' supported by backlog.py

bltodo.py when executed as a command:
 - reports the full absolute path for the TODO file it is using on stdout.
 - outputs the backlog contents in 'Markdown GB Data Form' (MDGBDF)


# Output Format -'Markdown GB Data Form' (MDGBDF)
MDGBDF is implemented in mdgbdata.py and is described in docs/dev/spec/mdgbdata-spec.md.


## potential data loss from files not already in Markdown Story Form
Markdown files may contain content that is not part of stories and tasks.
Initial implementations of bltodo.py will not have the capability to update or recreate files that are not already in 'Markdown GB Data Form'.  


 
