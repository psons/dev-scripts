This use case arose when creating multiple similar project sto test how AI and code generation might result in different things under slightly different conditions. 

A new project might be stubbed out by reusing a set of files and directories from an existing project.
I'd like to keep environment and specification to make a new project keeping specification from a previous project.

The example command uses `list` to recall a collection of files.



tar cvf ../save.tar $(list --load fbase-mod-stub) && cd .. && mkdir fbase-mod-stub-2 && cd fbase-mod-stub-2 && tar xvf ../save.tar