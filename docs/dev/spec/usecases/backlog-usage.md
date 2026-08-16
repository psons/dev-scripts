dtask --final may find some incomplete tasks in do.md, which should be pushed to the backlog (such as the bltodo.py plugin's use of the file TODO.md) since the do.md file will be deleted and re-initialized for the next feature.

    more specific use flow 1: Sometime there are incomplete tasks because the feature for the branch and intended commit message actually have grown to include a set of work that can stand as a feature in its own rite that is now complete, so a new unexpected feature commit is being made, and the work for the original commit is still needed, and should be temporarily "pushed" back to the backlog.


    more specific use flow 2: Some times new work, or follow in feature integration work is defined but is to be deferred to later in order to preserve focus on the current feature.  In this case, the story can be authored into do.md as a Story, and pushed into te backlog where it will receive prioritization scrutiny after the current feature is completed and committed to source control. 

