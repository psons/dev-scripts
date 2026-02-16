what-is-where.md

#
Specification of softwareis strictly required, and must be always true for the project.  AI tools by contrast are non-deterministic, and will not produce the same project given the same spec because they use training that changes over time. Therfore, spec info should be in the source repository of a project.   AI prompts should be simple requests to read the spec.   Propriteary AI platform hooks should be simple guiodance to efficiently find the AI tool agnostic specs.

This script environment related source code up should be outside of the source repository of the project so that humans and AI working on the projects that use itdo not need to spend energy looking at it when understanding a project.

The .env.local file inside a project

 - should not have coupling to the compute environment hosting the project.

 - should produce an error if the bin tools and environmet of this project are not available to the 
 shell that is sourcing .env.local.  Therefore the .env.local file should report an error on stderr if the DEV_SCRIPTS environment variable is not set.

 



