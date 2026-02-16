
# shell things to work with a .env.local  
especially for use in vscode terminal.

The scripts are in a bin/ directory that is a child of the directory with the .env.local file.
A code snipped shows what to 
put in a shell profile to source the .env.local 
when a shell starts in the curent directory, as
vscode does when launching a terminal.

The name .env.local is conventional for some
Javascript frameworks to store variable in the 
environment that should not be committed to 
source control.

Similarly, the intent here is to use it for project needs
that may be installed outside the project, and coupled to the local
computer, such as a path to Java.  Local installations of things like nvm and python
can be set up here too. 

# Also included
Some of the script content is for inrospecting installation specifics like 
home brew to reduce the amount of text in .env.local

Some utilities that may help developers and sys admins are also included, but may be pushed to 
a different repo at some time. (like the list script)

# Source and AI
This project has the opinion that the specification of softwares belongs in the source tree, but that the hooks for any specific AI platform like Copilot or Gemini are more like IDEs, and should be in separate source control.

## Reasoning
See spec/what-is-where.md
