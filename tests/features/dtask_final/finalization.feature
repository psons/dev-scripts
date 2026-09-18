Feature: dtask finalization of do.md work
  As a developer
  I want finalization to preserve unfinished work and completed task history
  So that no task disappears when do.md is removed

  Background:
    Given a git repository with initial commit and tracked files

  Scenario: --final pushes unfinished work and commits completed work before removing do.md
    Given do.md contains current work with active and completed tasks
    And TODO.md contains an existing story for the current work
    And a tracked work file has staged changes
    When I run "dtask commit --final --all" for finalization
    Then the finalization command succeeds
    And the backlog has the finalized story at the top
    And the backlog story contains the active task and its existing task
    And the first finalization commit contains completed task "completed task" with story ID "story-active" and story name "Active Story"
    And the first finalization commit contains completed task "unfinished task" with story ID "story-active" and story name "Active Story"
    And the finalization do.md file no longer exists

  Scenario: --final pushes an unfinished current-work story into TODO.md
    Given do.md contains current work with active and completed tasks
    When I run "dtask commit --final --all" for finalization
    Then the finalization command succeeds
    And TODO.md contains the unfinished current-work story at the top
    And TODO.md contains active task "active task" in story "Active Story"

  Scenario: --final keeps do.md when pushing unfinished work fails
    Given do.md contains current work with active and completed tasks
    And the backlog provider is unavailable
    When I run "dtask commit --final" for finalization
    Then the finalization command fails
    And the do.md file remains unchanged
    And no final removal commit was created
