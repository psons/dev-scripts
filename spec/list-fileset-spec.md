# save named filesets

enhance the bin/list python utility with options to save and load named lists.  Lists will often be named set of files as they would be used on a shell command line such as they would be used arguments to the tar command, and may contain wild card globs, which should not be expanded by the list command, but might be expanded by the calling shell as normal, unless quoted. 

When a fileset is saved or loaded, the default behavior will be to save or load the fileset from ~/.filesets in a file with the same name as the file set.  

    --save <list-name>
        list-name is the name of a list to save.

    --load <list-name>
        list-name is the name of a list to load.

if the -f option is used, the name provided with the -f option will be used instead of the list-name, and the --load option is ignored.

