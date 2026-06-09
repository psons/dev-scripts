# Background
## integration between dev-scripts and gb-data: the gbdata module.
The dev-scripts project will own the code implementations of the file parsing capabilities for the backlog.py module by using the gbdata.py module.
The short single character "val" code to represent the status of stories in short hand and tasks will be owned by the [gb-data project](https://github.com/psons/gb-data) as they are now, along with the formal string enum values.
The "pat_str" attributes that must correspond 1 for 1 with the enum values and the short hand "val" codes, but due to the securiy risk of client code being generated to use the patterns directly in code, they will be part of the specification text and treated as source code. 

# Requirements
Develop a detailed code implementation design as docs/dev/spec/code-ready/gbdata-spec-ready.md to be the single source of truth for implementation for bin/gbdata.py.
The purpose for files in docs/dev/spec/code-ready/ should be guided by the README.md there.

bin/gbdata.py should no be generated from this file and should only be generated from docs/dev/spec/code-ready/gbdata-spec-ready.md after it has been reviewed with a separate prompt issued to generate bin/gbdata.py

The code-ready/gbdata-spec-ready.md spec should contain all the design details and facts to generate a python module bin/gbdata.py that contains the types described in https://github.com/psons/gb-data/blob/main/goalBlotter.schema.json.

gbdata.py should include a class or method to be used for parsing mark down file to build Story objects containing Tasks according to the use cases and rules in docs/dev/spec/usecases/story-task-parsing-md.md.  The parsers should use the status text patterns in:
 - docs/dev/spec/code-ready/story_status_metadata.json
 - docs/dev/spec/code-ready/task_status_metadata.json


