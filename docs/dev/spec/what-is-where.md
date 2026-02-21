# What Is Where

## Philosophy

AI prompts should be requests to read specifications saved in the source tree.

Prompts themselves should be standard simple requests to implemet specifications.

Proprietary AI platform hook files should be simple guidance to efficiently find the AI tool-agnostic specs.

Some common use knowledge should be in a location shared by all projects.
The shared knowledge location should be set according to $KNOWLEDGE_HOME in .env.local

.env.local should export the $DEV_SCRIPTS variable to set te location of it's bin directory

## Script Environment Location

This script environment-related source code should be outside of the source repository of the project so that humans and AI working on the projects that use it do not need to spend energy looking at it when understanding a project.

## The .env.local File

The `.env.local` file inside a project:

- **Should not have coupling** to the compute environment hosting the project.

- **Should produce an error** if the bin tools and environment of this project are not available to the shell that is sourcing `.env.local`. Therefore, the `.env.local` file should report an error on stderr if the `DEV_SCRIPTS` environment variable is not set.

 



