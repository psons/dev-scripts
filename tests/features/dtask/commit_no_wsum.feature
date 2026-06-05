Feature: dtask commit without --wsum
  As a developer
  I want to commit task work using do.md metadata without generating a work summary
  So that staged and tracked changes are committed with the expected task message

  Background:
    Given a git repository with initial commit and tracked files
    And a committed do.md file for the current branch with frontmatter:
      | key | value |
      | title | do.md |
      | description | A list of small, focused tasks guiding the current commit with detailed microsected activities. |
      | workBranch | current branch |
      | priorCommit | current HEAD |

  Scenario: default commit uses Work Summary workHeadline and keeps untracked files out of scope
    Given the committed do.md file has frontmatter:
      | key | value |
      | intendedCommitMessage | planned staged work |
      | actualCommitMessage | stale actual message |
    And do.md has a Work Summary entry with workHeadline "feat: commit staged files without wsum"
    And the tracked file "file-one.txt" has staged changes with content "file-one staged update"
    And the untracked file "notes.txt" exists with content "temporary notes"
    When I run "dtask commit"
    Then the command succeeds
    And the latest commit message is "feat: commit staged files without wsum"
    And do.md frontmatter value "actualCommitMessage" is "feat: commit staged files without wsum"
    And the commit includes "file-one.txt"
    And the commit does not include "notes.txt"

  Scenario: --actual with an explicit message updates do.md before committing
    Given the committed do.md file has frontmatter:
      | key | value |
      | intendedCommitMessage | planned work |
      | actualCommitMessage | stale actual message |
    And the tracked file "file-one.txt" has staged changes with content "file-one staged update"
    When I run "dtask commit --actual explicit actual message"
    Then the command succeeds
    And the latest commit message is "explicit actual message"
    And do.md frontmatter value "actualCommitMessage" is "explicit actual message"
    And the commit includes "file-one.txt"

  Scenario: --actual without an argument copies intendedCommitMessage
    Given the committed do.md file has frontmatter:
      | key | value |
      | intendedCommitMessage | copied intended message |
      | actualCommitMessage | stale actual message |
    And the tracked file "file-one.txt" has staged changes with content "file-one staged update"
    When I run "dtask commit --actual"
    Then the command succeeds
    And the latest commit message is "copied intended message"
    And do.md frontmatter value "actualCommitMessage" is "copied intended message"
    And the commit includes "file-one.txt"

  Scenario: --update includes tracked unstaged changes but excludes untracked files
    Given the committed do.md file has frontmatter:
      | key | value |
      | intendedCommitMessage | planned update work |
      | actualCommitMessage | stale actual message |
    And do.md has a Work Summary entry with workHeadline "feat: include tracked updates only"
    And the tracked file "file-one.txt" has staged changes with content "file-one staged update"
    And the tracked file "file-two.txt" has unstaged changes with content "file-two tracked update"
    And the untracked file "notes.txt" exists with content "temporary notes"
    When I run "dtask commit --update"
    Then the command succeeds
    And the latest commit message is "feat: include tracked updates only"
    And do.md frontmatter value "actualCommitMessage" is "feat: include tracked updates only"
    And the commit includes "file-one.txt"
    And the commit includes "file-two.txt"
    And the commit does not include "notes.txt"

  Scenario: --final removes do.md after committing dirty task changes
    Given the committed do.md file has frontmatter:
      | key | value |
      | actualCommitMessage | feat: finalize dirty task |
      | intendedCommitMessage | planned final work |
    And the tracked file "file-one.txt" has staged changes with content "file-one staged update"
    And the do.md file has dirty text "Additional notes that must be committed first."
    When I run "dtask commit --final"
    Then the command succeeds
    And the last 2 commit messages are:
      | message |
      | removed do.md for finalized tasks |
      | feat: finalize dirty task |
    And the previous commit includes "docs/dev/work/do.md"
    And the previous commit includes "file-one.txt"
    And the do.md file no longer exists

  Scenario: --final removes do.md even when the working tree is clean
    Given the committed do.md file has frontmatter:
      | key | value |
      | actualCommitMessage | feat: finalize clean task |
      | intendedCommitMessage | planned clean final work |
    When I run "dtask commit --final"
    Then the command succeeds
    And the latest commit message is "removed do.md for finalized tasks"
    And the do.md file no longer exists

  Scenario: --final falls back to Work Summary workHeadline when actualCommitMessage is empty
    Given the committed do.md file has frontmatter:
      | key | value |
      | intendedCommitMessage | planned clean final work |
      | actualCommitMessage | |
    And do.md has a Work Summary entry with workHeadline "feat: final fallback headline"
    And the tracked file "file-one.txt" has staged changes with content "file-one staged update"
    When I run "dtask commit --final"
    Then the command succeeds
    And the last 2 commit messages are:
      | message |
      | removed do.md for finalized tasks |
      | feat: final fallback headline |
    And the do.md file no longer exists

  Scenario: --all and --update cannot be combined
    Given the committed do.md file has frontmatter:
      | key | value |
      | actualCommitMessage | feat: invalid flag combination |
      | intendedCommitMessage | planned work |
    When I run "dtask commit --all --update"
    Then the command fails with a non-zero exit code
    And the error output mentions "not allowed with argument"
