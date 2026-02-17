# What Is Where

## Philosophy

Specification of software is strictly required and things it descxribes must always be true for the project. AI tools by contrast are non-deterministic and will not produce the same project given the same spec because they use training that changes over time. Therefore, spec information should be in the source repository of a project, and AI prompts that are not specifications should not. AI prompts should be simple requests to read the spec. Proprietary AI platform hook files should be simple guidance to efficiently find the AI tool-agnostic specs.

## Script Environment Location

This script environment-related source code should be outside of the source repository of the project so that humans and AI working on the projects that use it do not need to spend energy looking at it when understanding a project.

## The .env.local File

The `.env.local` file inside a project:

- **Should not have coupling** to the compute environment hosting the project.

- **Should produce an error** if the bin tools and environment of this project are not available to the shell that is sourcing `.env.local`. Therefore, the `.env.local` file should report an error on stderr if the `DEV_SCRIPTS` environment variable is not set.

 



