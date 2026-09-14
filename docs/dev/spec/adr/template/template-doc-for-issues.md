Several issues can be analyzed and documented where each issues has the structured markdown sections as follows.

Sections that are not pure question can have the section front-matter attributes 'status:', 'statusNote:', and 'statusDate:' to help AI discern open questions from firm decisions.  'status:' should be either 'accepted', or 'pending'

## issue: Simple question?
An H2 section should frame the issue question in the heading.  If possible it should be a single question.  If it isn't a single question, consider creating multiple issues and then tying them together with a single issue based on the analysis. 

The body text will begin with a clarified and and expanded ask of the question.
When the issue id resolved, the body text of this section may contain an 'answer:' line followed by an answer written at the aproximate detail level of the clarified and expanded question.

The body text of this section may contain a statement of the vision to be achieved by a good answer to the question.

### Thinking:
The body text of this section contains reasoning and proposals of why a particular solution direction might be best for an ultimate desired outcome.
After the fact, readers should be able to look at this section to understand why a decision was made the way it was.

#### for the current iteration
---
status: accepted
statusNote: check the rules against existing MDGBDF behavior and try to align.
statusDate: 2026-09-06
---
The body text of this section should describe the immediate actionable analysis that supports decisions below 

The section front-matter 'status:' attribute should indicate if the solution is accepted, pending, or in some cases rejected.

The section front-matter 'statusNote:' attribute should contain information to help align this decision with other things, possibly a follow on decision or activity.

The section front-matter 'statusDate:' indicates when the status was set, so as to help analyze conflicts with newer thinking.    

##### Current state ... 
Body text in this sub section may describe some aspect of current state for ... that is the basis of change for actionable decisions for te current iteration

##### Current state ... 
Body text in this sub section may describe some aspect of current state for ... that is the basis of change for actionable decisions for te current iteration

### Decisions

#### For the current iteration (Feature )
Body text in this subsection describes decisions as they affect the most near at hand feature to be delivered.

#### For future 
Body text in this subsection should describe decisions (and design concepts) as they are expected to be in the future based on ultimate objective.  These directions may imply a roadmap that comes after the current iteration feature of the previous section, and before the ultimate decision of this section.  That roadmap need not be documented here, but may be mentioned.  Decision here should support north star vision, but too much elaboration creates material that likely needs maintenance and revision as new learning unfolds.

# Issue Template in brief:
```markdown
## issue: Simple question?
### Thinking:
#### for the current iteration
##### Current state ... 
##### Current state ... 
### Decisions
#### For the current iteration 
---
status: pending
statusNote: 
statusDate: YYYY-MM-DD
---
#### For future 
---
status: pending
statusNote: 
statusDate: YYYY-MM-DD
---
```