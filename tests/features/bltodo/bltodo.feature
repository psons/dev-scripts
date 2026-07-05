Feature: bltodo command line support
  As a developer
  I want bltodo to read markdown backlog data from a TODO file
  So that I can inspect the plugin's current source data

  Scenario: command prints the TODO path and mdgbdf output
    Given a bltodo TODO file named "todo.md" with content:
      """
      # d - Story: Alpha
      id: story-a
      d - first task
      id: task-1
      """
    And BL_TODO_FILE points to that bltodo TODO file
    When I run bltodo command "bltodo"
    Then the bltodo command succeeds
    And the bltodo stdout contains "TODO file:"
    And the bltodo stdout contains "# Story: Alpha"
    And the bltodo stdout contains "d - first task"

  Scenario: command uses BL_TODO_FILE content
    Given a bltodo TODO file named "custom.md" with content:
      """
      # d - Story: Custom Source
      id: story-custom
      x - done task
      id: task-done
      """
    And BL_TODO_FILE points to that bltodo TODO file
    When I run bltodo command "bltodo"
    Then the bltodo command succeeds
    And the bltodo stdout contains "# Story: Custom Source"
    And the bltodo stdout contains "x - done task"

  Scenario: command fails when TODO file does not exist
    Given BL_TODO_FILE points to a missing bltodo file
    When I run bltodo command "bltodo"
    Then the bltodo command fails with a non-zero exit code
    And the bltodo stdout contains "Error:"
