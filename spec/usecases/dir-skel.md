A new project mitght be stubbed out by reusing a set of files and directories from an existing project.
I'd like to keep environment and specification to make a new project keeping specification from a previous project.



tar cvf ../save.tar $(list --load fbase-mod-stub) && cd .. && mkdir fbase-mod-stub-2 && cd fbase-mod-stub-2 && tar xvf ../save.tar