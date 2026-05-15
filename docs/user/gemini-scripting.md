# Gemini CLI Shell Scripting Guide

This guide provides instructions and best practices for interacting with the Gemini CLI from shell scripts. Automating tasks with Gemini CLI can significantly enhance your development workflow.

## 1. Basic Command Execution

You can execute Gemini CLI commands directly within your shell scripts. Always ensure you are in the correct directory or provide absolute paths where necessary.

```bash
# Example: Running a simple Gemini CLI command
gemini list-directory --dir_path="./src"
```

## 2. Capturing Output

To process the output of Gemini CLI commands in your scripts, you can capture it into variables. Gemini CLI typically outputs JSON, which can be parsed using tools like `jq`.

```bash
#!/bin/bash

# Capture output of a Gemini CLI command
output=$(gemini grep-search --pattern="TODO" --names_only --dir_path="." | jq -r '.')

# Iterate over the found files
echo "Files containing 'TODO':"
for file in $output; do
  echo "- $file"
done
```

## 3. Error Handling

It's crucial to handle errors gracefully in your scripts. Gemini CLI commands will typically exit with a non-zero status code on failure.

```bash
#!/bin/bash

# Example: Checking for command success
gemini read-file --file_path="non_existent_file.txt"

if [ $? -ne 0 ]; then
  echo "Error: Failed to read file."
  exit 1
fi

echo "File read successfully."
```

## 4. Using Gemini CLI with `xargs` and `find`

For more advanced scenarios, you can combine Gemini CLI with standard Unix utilities like `find` and `xargs` for powerful file processing.

```bash
#!/bin/bash

# Find all Markdown files and then use Gemini CLI to read them
find . -name "*.md" -print0 | xargs -0 -I {} gemini read-file --file_path="{}"
```

## 5. Environment Variables and Configuration

If your Gemini CLI usage relies on environment variables (e.g., API keys), ensure they are set correctly in your script's execution environment.

```bash
#!/bin/bash

# Example: Setting an environment variable (replace with your actual env var)
export GEMINI_API_KEY="your_api_key_here"

# Now execute a command that might use this key
gemini some-command-requiring-auth
```

## 6. Best Practices

*   **Idempotency:** Design your scripts to be idempotent, meaning running them multiple times produces the same result as running them once.
*   **Logging:** Use `echo` or a dedicated logging utility to provide clear feedback on script progress and any issues.
*   **Version Control:** Keep your scripts under version control (e.g., Git).
*   **Shebang:** Always start your scripts with a shebang (e.g., `#!/bin/bash`) to specify the interpreter.
*   **Permissions:** Ensure your scripts have execute permissions (`chmod +x your_script.sh`).
*   **Avoid Interactive Commands:** Prefer non-interactive Gemini CLI commands for scripting. If a command requires user input, consider if it's suitable for automation or if there's an alternative non-interactive option.
*   **Readability:** Write clear, well-commented scripts that are easy to understand and maintain.

By following these guidelines, you can effectively leverage the Gemini CLI to automate and streamline your development tasks.

## Appendix: Available Gemini CLI Commands

Here is a list of commands that can be executed via the `gemini` executable in your shell scripts:

*   `gemini activate-skill`
*   `gemini ask-user`
*   `gemini enter-plan-mode`
*   `gemini glob`
*   `gemini google-web-search`
*   `gemini grep-search`
*   `gemini invoke-agent`
*   `gemini list-background-processes`
*   `gemini list-directory`
*   `gemini read-background-output`
*   `gemini read-file`
*   `gemini replace`
*   `gemini run-shell-command`
*   `gemini update-topic`
*   `gemini web-fetch`
*   `gemini write-file`
