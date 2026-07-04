# Modules and Scripts
dtask 
 - has a top level user CLI
 - own update of do.md
 - calls wsum.py 
 - calles backlog.py to pop task from backlog 

backlog.py
 - has a top level user CLI 
- implements a module API for callers to use (such as dtask).
 - uses bl*.py plugins to interact with a backlog of tasks
    - bltodo.py is the default plungin.

bltodo.py
 - implements a module API for callers.
 - implements the 'Backlog Plugin Protocols' for backlog.py.
 - is the plugin for a simple TODO.md file backlog

gbdata.py
 - implements goal, story, and task related domain model types used bt the API contract between backlog.py and its plugins.
 - owns the shared status enum(s).

`mdgbdata.py`
 - owns markdown/text parsing behavior for 'Markdown GB Data Form' (MDGBDF).
 - must import `TaskStatus`, `Task`, and `Story` from `gbdata.py`.
 - owns serialization of the domain model to MDGBDF.


