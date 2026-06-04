Feature: dtask commit with --wsum flag
  As a developer
  I want to commit staged changes with automatic work summary generation
  So that I can create meaningful commit messages backed by AI-generated summaries inserted into do.md

  Background:
    Given a clean git repository with initial commit for --wsum
    And a work branch initialized with do.md for --wsum
    And a clean working tree for --wsum

  Scenario: Commit staged changes with auto-generated work summary
    Given I have modified file-one.txt
    And I have staged file-one.txt
    When I run dtask commit --wsum command
    Then the dtask commit --wsum command succeeds
    And a commit is created
    And the commit message contains the work headline from do.md
    And the do.md file contains a Work Summary section
    And the actualCommitMessage is updated in do.md frontmatter
    And do.md is staged in the commit

  Scenario: Commit with --wsum and --update includes tracked unstaged changes
    Given I have modified file-one.txt
    And I have staged file-one.txt
    And I have modified file-two.txt (unstaged)
    When I run dtask commit --wsum --update command
    Then the dtask commit --wsum --update command succeeds
    And a commit is created
    And the commit includes both staged and unstaged tracked changes
    And the do.md file contains a Work Summary section
    And the commit message is from the generated work headline

  Scenario: Commit with --wsum and --all includes all changes
    Given I have modified file-one.txt
    And I have staged file-one.txt
    And I have modified file-two.txt (unstaged)
    And I have created file-three.txt (untracked)
    When I run dtask commit --wsum --all command
    Then the dtask commit --wsum --all command succeeds
    And a commit is created
    And the commit includes staged, unstaged tracked, and untracked changes
    And the do.md file contains a Work Summary section
    And the work summary reflects all changes

  Scenario: Commit with --wsum and --actual uses explicit message
    Given I have modified file-one.txt
    And I have staged file-one.txt
    When I run dtask commit --wsum --actual "Custom commit message" command
    Then the dtask commit --wsum --actual command succeeds
    And a commit is created
    And the commit message is "Custom commit message"
    And the do.md file contains a Work Summary section
    And the actualCommitMessage in do.md frontmatter is "Custom commit message"

  Scenario: Error handling when wsum times out
    Given I have modified file-one.txt
    And I have staged file-one.txt
    When I run dtask commit --wsum command with wsum timeout
    Then the dtask commit --wsum command fails with exit code 1
    And the error output mentions "wsum.summarize_work() did not complete"
    And the error output mentions "45 seconds"
    And the do.md file is NOT modified

  Scenario: Error handling when wsum returns no changes
    Given I have modified file-one.txt
    And I have staged file-one.txt
    When I run dtask commit --wsum command with wsum error response
    Then the dtask commit --wsum command fails with exit code 1
    And the error output mentions "wsum"
    And the error output suggests setting actualCommitMessage
    And the do.md file is NOT modified

  Scenario: Error handling when no staged changes to commit
    Given a clean working tree with no staged changes
    When I run dtask commit --wsum command
    Then the dtask commit --wsum command fails with exit code 1
    And the error output mentions "no staged changes"

  Scenario: Verify do.md structure after successful commit
    Given I have modified file-one.txt
    And I have staged file-one.txt
    When I run dtask commit --wsum command
    Then the dtask commit --wsum command succeeds
    And the do.md frontmatter contains workHeadline with a non-empty value
    And the do.md frontmatter contains actualCommitMessage matching the work headline
    And the do.md body contains the "# Work Summary" section
    And the work summary is inserted before any older summaries

  Scenario: Work headline is generated and matches expected format
    Given I have modified file-one.txt with description "Add new feature"
    And I have staged file-one.txt
    When I run dtask commit --wsum command
    Then the dtask commit --wsum command succeeds
    And the work headline is a single line summary
    And the work headline is used as the commit message
    And the commit is recorded in git log

  Scenario: Multiple consecutive commits with --wsum
    Given I have modified file-one.txt
    And I have staged file-one.txt
    When I run dtask commit --wsum command
    Then the dtask commit --wsum command succeeds
    And a commit is created with message from work headline
    Given I have modified file-two.txt
    And I have staged file-two.txt
    When I run dtask commit --wsum command
    Then the dtask commit --wsum command succeeds
    And a new commit is created
    And the do.md file contains multiple Work Summary entries
    And each entry is in chronological order (newest first)
