Feature: backlog command line support
  As a developer
  I want backlog to query backlog data from a provider plugin
  So that I can view prioritized work in markdown or JSON

  Scenario: prioritized uses the default provider and emits mdgbdf by default
    Given a backlog TODO file named "todo.md" with content:
      """
      # d - Story: Alpha
      ---
      id: story-a
      ---
      d - first task
      ---
      id: task-1
      ---
      x - second task
      ---
      id: task-2
      ---
      """
    And BL_TODO_FILE points to that backlog TODO file
    When I run backlog command "backlog prioritized"
    Then the backlog command succeeds
    And the backlog stdout contains "# Story: Prioritized Tasks"
    And the backlog stdout contains "d - first task"

  Scenario: prioritized supports json output
    Given a backlog TODO file named "todo.md" with content:
      """
      # d - Story: Alpha
      ---
      id: story-a
      ---
      d - first task
      ---
      id: task-1
      ---
      """
    And BL_TODO_FILE points to that backlog TODO file
    When I run backlog command "backlog prioritized --json"
    Then the backlog command succeeds
    And the backlog stdout JSON contains a task id "task-1"

  Scenario: poptask returns the highest-priority task
    Given a backlog TODO file named "todo.md" with content:
      """
      # d - Story: Alpha
      ---
      id: story-a
      ---
      d - first task
      ---
      id: task-1
      ---
      # d - Story: Beta
      ---
      id: story-b
      ---
      d - second task
      ---
      id: task-2
      ---
      """
    And BL_TODO_FILE points to that backlog TODO file
    When I run backlog command "backlog poptask"
    Then the backlog command succeeds
    And the backlog stdout contains "# Story: Top Task"
    And the backlog stdout contains "d - first task"

  Scenario: help prints command usage summary
    When I run backlog command "backlog help"
    Then the backlog command succeeds
    And the backlog stdout contains "prioritized"
    And the backlog stdout contains "poptask"
    And the backlog stdout contains "popstory"
