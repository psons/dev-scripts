# Status Meaning

| Status enum value | Shorthand character text leader | Meaning for Tasks | Meaning for Stories | Leader parsing regex |
| :---- | :---- | :---- | :---- | :---- |
| "do" | 'd \- '  | todo (or do) are un-started tasks in files that contain tasks.  | todo (or do) are un-started stories (collections of tasks) | "^\[dD\] \*-" |
| "in\_progress" | '/ \- '  | in progress are tasks that are being worked on.  | in progress are stories that have some tasks that are being worked on. | "^\[\\\\/\\\\\\\\\] \*-" |
| "completed" |  'x \- ' | completed task. | completed story | "^\[xX\] \*-"  |
| "abandoned" | 'a \- ' | abandoned are tasks that have been in the blotter or the backlog, but lost their relevance or  value, and will not be worked on, and will be removed from planning also.  | abandoned are stories that have had some tasks in the blotter or the backlog, but lost their relevance or  value, and will not be worked on, and will be removed from planning also.  | "^\[aA\] \*-"  |
| "scheduled" | 's \- ' | scheduled tasks that are to be ignored for daily sprint prioritization because they have apportioned time for work separately in the schedule.  | scheduled stories are deferred to some future sprint. and tasks they contain are to be ignored for daily sprint prioritization.  |  |
| "unfinished" | 'u \- ' | Tasks that were not finished yet, in a daily sprint, and should carry over to a new day sprint for completion.   | Stories that were not finished in a sprint where they were started, but do not have any in progress tasks.  | "^\[uU\] \*-"  |

Reference: [Status Meaning](https://docs.google.com/document/d/1icAlbeXJwcYxlPvDZ7OiOIqgXlNqjNLrEQ86CECM1kU/edit?usp=sharing) 

       
     

        
       
