Feature: dtask init with --dirty and --newdo flags
  As a developer
  I want to initialize a new do.md while handling an existing uncommitted one
  So that I can start fresh task tracking without losing prior task context

  Background:
    Given a git repository with initial commit and tracked files

  Scenario: newdo commits a dirty do.md before replacing it
    Given the working tree has an uncommitted do.md file
    When I run "dtask init --workbranch new-feature --dirty --newdo"
    Then the command succeeds
    And a commit exists with a message containing "do.md when"
    And a new "docs/dev/work/do.md" file is created
    And the new do.md priorCommit matches the commit that saved the old do.md
    And the do.md file is not staged

  Scenario: newdo has no effect when do.md is already committed
    Given the working tree has a committed do.md file
    And the working tree is clean
    When I run "dtask init --workbranch new-feature --dirty --newdo"
    Then the command succeeds
    And no commit was made with a message containing "do.md when"
    And a new "docs/dev/work/do.md" file is created
    And the new do.md priorCommit matches the commit before dtask ran
    And the do.md file is not staged

  Scenario: dirty without newdo exits with error when do.md is dirty
    Given the working tree has an uncommitted do.md file
    When I run "dtask init --workbranch new-feature --dirty"
    Then the command fails with a non-zero exit code
    And the error output mentions "--newdo"
    And the existing do.md content is unchanged

  Scenario: dirty allows init when only non-do.md files are dirty
    Given the working tree has a modified tracked file "file-one.txt"
    And there is no existing do.md file
    When I run "dtask init --workbranch new-feature --dirty"
    Then the command succeeds
    And a new "docs/dev/work/do.md" file is created
    And the file "file-one.txt" is still modified in the working tree
