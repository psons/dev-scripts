The command module pattern is specified here.

To direct python program structure that implements the python Script Module Idiom.

The pattern should include generation of a python module with key structural elements that have been built into wsum.py in this project as an example implementation.

The behaviors of the command invocation are implemented using argparse with help text documenting the usage.

The capabilities of the command line are available using a primary implementation function.

The primary implementation function is to be called by the command with the options of the command available as arguments to the function.

The command invocation calls the same primary implementation function that is available to callers of the module directly.

The return value of the primary implementation function is a typed object containing all of the values used in the command output, as well as the output that would be formatted on stdout as a result of command invocation.

The primary implementation function contains full unit testing using pytest.

The command has full BDD testing using pytest-bdd.


