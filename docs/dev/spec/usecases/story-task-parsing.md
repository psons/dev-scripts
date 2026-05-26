Tasks will be parsed as tlog style tasks in markdown files
Tasks begin with lines that match the patterns that match the "pat_str" attribute of any top level status attribute of the the following JSON object:
{
    "abandoned": { "val": "a", "pat_str": "^[aA] *-" },
    "completed": { "val": "x", "pat_str": "^[xX] *-" },
    "scheduled": { "val": "s", "pat_str": "^[sS] *-" },
    "in_progress": { "val": "/", "pat_str": "^[\\/\\\\] *-" },
    "unfinished": { "val": "u", "pat_str": "^[uU] *-" },
    "do": { "val": "d", "pat_str": "^[dD] *-" }
}
This object comes from a source repo at https://github.com/psons/gb-data/blob/main/task_status_metadata.json
Tasks include any lines that follow them from the matched lime until a line that starts another markdown section or another task.
Tasks may include a front matter section that immediately follows the line matching the task "pat_str" 

There are two situations that cause a markdown section to be considered a story
1 - any markdown header with tasks under them.
2 - Any markdown section where the '# characters that identify it as a markdown header are followed by the string "Story:" before any other non whitespace or newline characters.   
        