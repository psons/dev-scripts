Build a markdown linked set of user documentation under docs/user.

There should be a collection of process oriented documentation for the following topical areas addressed by the development script user artifacts in in this repo.

* Node JS based development
* Firebase project development
* Development Project Setup
* AI Knowledge indexing and Skills

Each topical area should have a subdirectory containing a main topical markdown page.  The markdown page with 

Each main topical markdown pages should have:
 - navigation links at the top to the main topical markdown pages for each of the other topical areas.
 - explanation of how to use the included scripts and artifacts.  The explanations should focus on the development activities they facilitate, and be initially drafted based on specifications and use cases for the scripts and artifacts in the topical areas.   The development activities should be in two sections.  The first section contains activities already facilitated by scripts and artifacts in the repository.  The second section enumerates developer activities that can be rebatable and efficiently scripted to enhance AI driven development. 
 - an index of the user documentation page for the scripts and artifacts for the topical area.

The user documentation page for each script and artifacts should inline the help text from the script if available, except that if the script help command expands environment variables or builds strings at run time, they should be replaces with tokens to represent the strings such as the environment variable used, or the function name used to determine the string at run time.

Each script or artifact in the bin directory plus enable_env_local.sh and .env.local should have a user documentation page, except that README files should not have user documentation pages.

There should be a top level page with navigation to all the main topical markdown pages for each of the other topical areas.

Each documentation page should have a '# maintenance' section at the bottom whose content is the prompt instructions to efficiently update the documentation for the page.

The documentation set should embody the DRY principle and favor references to other content over repetition.