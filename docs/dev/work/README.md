This folder, docs/dev/work is for feature parcels (aka stories)
It should have do.md and TODO.md files.
  - This folder may have a docs/dev/backlog directory that is .gitignored because the backlog contains
    things that may never be built, an hence would be noise possibly conflicting with truth in the source tree.
    docs/dev/backlog may be a symlink to a repo that is elsewhere, such as to a peer repo of this repo (dev-scripts-backlog).



A different folder, docs/dev/workflow is for methodology: workflow for contributing to this project.
 
# TODO.md
The TODO file is an implementation file for a "simple" queue of stories and tasks that the bltodo.py plugin (Backlog Todo) knows how to manipulate for the backlog.py module.
The bltodo.py module uses the mdgbdata.py program to parse and serialize "Story" and "Task" objects out of .md files, so anything that is not clearly handled as part of how  
mdgbdata.py reads and writes those objects will get mutated.   Specifically, file front-matter will get messed up, so don't put it there.
 
# do.md
The do.md file should be saved immediately when edited manually because the dtask command also updates it.

The do.md file is a place to tie together all the things needed to work in the current task and story to improve focus.
Ideally do.md has information about where work was left off at the end of a session, the curent an recent source commits, and the next task or next few tasks to work on.


See also the [bin/README.md section on dtask](../../../bin/README.md#dtask). 