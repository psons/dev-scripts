# gbdata.py

Typed domain model definitions for goal/story/task planning artifacts.

## Runtime Help Behavior

gbdata.py is a model module and currently does not expose command-line help for --help, -h, or help.

## Exported Types

- TaskStatus
- StoryStatus
- Task
- Story
- Goal
- TimePriorityBlock
- WorkHierarchy

## Example

```bash
python -c "from bin.gbdata import TaskStatus; print(TaskStatus.DO.value)"
```

# maintenance

Update this page with the prompt below:

"Refresh docs/user/ai-knowledge-skills/gbdata.md from current module exports and dataclass/type definitions. Keep this page focused on model intent and exported symbols."
