Feature: dtask init with --workbranch flag
  As a developer
  I want to initialize a new feature branch with a stubbed do.md file
  So that I can start working on a focused task with proper branch and task tracking

  Background:
    Given a clean git repository with initial commit
    And a clean working tree

  Scenario: Initialize feature branch with workbranch flag
    When I run "dtask init --workbranch my-feature"
    Then a new branch "my-feature" is created
    And the branch "my-feature" is checked out
    And a "docs/dev/work/do.md" file is created
    And the do.md file body contains the "# Work Summary" heading
    And the do.md file contains frontmatter with "workBranch": "my-feature"
    And the do.md file is not staged

  Scenario: Workbranch frontmatter is properly set
    When I run "dtask init --workbranch experimental-feature"
    Then the do.md file contains:
      | frontmatter key | value |
      | workBranch | experimental-feature |
      | description | A list of small, focused tasks guiding the current commit with detailed microsected activities. |
      | title | do.md |

  Scenario: Workbranch creates branch from current HEAD
    Given I have made 2 commits
    When I run "dtask init --workbranch feature-from-commit"
    Then the branch "feature-from-commit" points to the same commit as "HEAD@{-1}"
    And the working tree remains clean
