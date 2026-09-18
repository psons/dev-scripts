Feature: dtask settle
  As a developer
  I want to settle completed and unfinished work without committing
  So that do.md and the backlog reflect the current task state

  Scenario: settle records completed work and pushes unfinished work
    Given the documented dtask settle fixture state
    When I run the dtask settle command
    Then the dtask settle command succeeds
    And the dtask settle do.md file remains
    And the dtask settle do.md records completed task "story 1 task 1" with its story attribution
    And the dtask settle backlog contains unfinished task "story 1 task 2" in story "story 1"
    And the dtask settle command creates no git commit

  Scenario: settle preserves do.md when the backlog provider fails
    Given the documented dtask settle fixture state
    And the dtask settle backlog provider is unavailable
    When I run the dtask settle command
    Then the dtask settle command fails
    And the dtask settle do.md is unchanged