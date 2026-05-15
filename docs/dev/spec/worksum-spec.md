# initial prompt to create worksum:

I would like a repeatable command to have an LLM summarize the changes shown by a git diff to generate a readable summary of the work and add it into into a '# work summary' section at the end of  a file 'docs/dev/work/do.md'.  Prototype this command as bin/worksum

## Notes:
This installed an extension
gh extension install github/gh-copilot 2>&1 | tail -3; gh copilot --help 2>&1 | head -20

# Re-prompt 1
I ran gh auth login as follows:
$ gh auth login
? What account do you want to log into? GitHub.com
? What is your preferred protocol for Git operations? HTTPS
? Authenticate Git with your GitHub credentials? Yes
? How would you like to authenticate GitHub CLI? Login with a web browser
...
Press Enter to open github.com in your browser... 
✓ Authentication complete.
- gh config set -h github.com git_protocol https
✓ Configured git protocol
✓ Logged in as psons.

When I run worksum, the following problem occurs:

$ worksum
Fetching Copilot token...
Error: could not obtain Copilot token via 'gh api'.
Ensure 'gh' is authenticated: run 'gh auth login'
gh: Not Found (HTTP 404)

# Adapt to gemini cli
The gemini cli has been installed and tested.  I also have an API key set up.

Adapt the bin/worksum script to use the gemini CLI to create the '#work summary'
