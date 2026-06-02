
Commands I use when closing out a feature and starting another one.
  526  git status
  527  git add docs/dev/work/TODO.md bin/dtask bin/README.md.gitignore
  528  git add docs/dev/work/TODO.md bin/dtask bin/README.md .gitignore
  529  git add docs/dev/work/TODO.md bin/dtask bin/README.md .gitignore
  530  git status
  531  dtask help
  532  dtask commit --final --actual
  533  git log --oneline -n5
  534  git show docs/dev/work/do.md
  535  git show aed73a1:docs/dev/work/do.md
  536  git branch
  537  git checkout main
  538  git merge dtask-commit
  539  git tag dtask-commit
  540  git log --oneline -n5
  541  dtask 
  542  dtask init -b "worksum-module" -i "implement wksum pythonmodule" --dirty 
  543  git branch
  544  git branch -d dtask-commit

This process can be put into a higher level script to automate branch management
perhapse call it `work`.  It amy also make sense to just add it to dtask.
with sub commands
    close - which closes out the feature with dtask --final and merges the branch to somthing aligned with the branch strategy
    open - which does a dtask init and pops tasks or stories off of TODO.md to build do.md.

Begin to support some frontmatter in tasks to drive AI implementation.
  - some tasks can run just from the info in te task.
  -  some tasks wil have a spec generation step, and then an implementation step.
  -  some tasks will have a spec generation step, an implementation step, and a test generation step.
  -  some tasks will have a spec generation step, an implementation step, a test generation step, and a documentation generation step.
  -  some tasks will have a spec generation step, an implementation step, a test generation step, a documentation generation step, and a release note generation step.
  -  some tasks will have a spec generation step, an implementation step, a test generation step, a documentation generation step, a release note generation step, and a changelog generation step.

