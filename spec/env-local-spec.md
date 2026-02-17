This project should have file at .env.local in its project root.

The .env.local file should 
 - echo a message from its first line indicating that it is beig sourced inot the shell.
 - print a message on stderr indicating that "The DEV_SCRIPTS location is not set inthe environment." if the DEV_SCRIPTS variable is not exported and set to a path that exists.
