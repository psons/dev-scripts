Implement backlog.py as a command mocule according to the pattern docs/dev/spec/python-command-module-pattern.md.

backlog.py should invoke plugin modules to implement a backlog interface

# Plugin modules
backlog.py should support a plugin architecture that uses typing.Protocol to define the capabilities needed by backlog.

backlog-types.py should be created to define the types needed by backlog.py and any plugins.

bltodo.py should be created to implement the first plugin.
bltodo.py will implement a plugin using gbdata.py to read and write tasks and stories from a markdown file. 

Other possible future plugins are to implement the backlog protocols against:
 - Taskwarrior as bltw.py
 - Jira as bljira.py
 - Goal Blotter as blgb.py

## Plugin Protocols
The task-queue protocol requires the following methods:
 - prioritized_tasks produces a listing of tasks, which are assumed to be in priority order
 - pop

# subcommands 

# backlog-todo.py