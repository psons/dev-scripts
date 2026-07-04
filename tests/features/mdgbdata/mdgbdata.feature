Feature: mdgbdata command line support
  As a developer
  I want mdgbdata to convert between markdown and JSON from the command line
  So that I can round-trip gb-data documents and detect malformed inputs

  Scenario: tojson converts markdown and warns about ignored prose
    Given a markdown file named "sample.md" with content:
      """
      Intro prose that should be ignored.

      # d - Build parser
      Story context line
      x - write tests
        review this later
      """
    When I run mdgbdata command "tojson sample.md"
    Then the mdgbdata command succeeds
    And the mdgbdata stderr contains "some non story text will be ignored"
    And the mdgbdata stdout JSON contains a story named "Build parser" with status "do" and a task named "write tests" with status "completed"
    And the mdgbdata stdout JSON story description is "Story context line"

  Scenario: tojson fails when no markdown headers or tasks are present
    Given a markdown file named "prose.md" with content:
      """
      Just prose without headings or task markers.
      """
    When I run mdgbdata command "tojson prose.md"
    Then the mdgbdata command fails with a non-zero exit code
    And the mdgbdata stderr contains "does not contain any markdown headers or tasks"

  Scenario: tomd converts JSON into markdown
    Given a JSON file named "stories.json" with content:
      """
      [
        {
          "id": "11111111-1111-7111-8111-111111111111-aaaaaaaa",
          "status": "do",
          "name": "Build parser",
          "description": "Parser context",
          "tasks": [
            {
              "id": "22222222-2222-7222-8222-222222222222-bbbbbbbb",
              "status": "completed",
              "name": "write tests",
              "detail": "cover the happy path"
            }
          ]
        }
      ]
      """
    When I run mdgbdata command "tomd stories.json"
    Then the mdgbdata command succeeds
    And the mdgbdata stdout contains "# d - Build parser"
    And the mdgbdata stdout contains "Parser context"
    And the mdgbdata stdout contains "x - write tests"
    And the mdgbdata stdout contains "cover the happy path"

  Scenario: tomd fails on invalid JSON
    Given a JSON file named "broken.json" with content:
      """
      {not valid json}
      """
    When I run mdgbdata command "tomd broken.json"
    Then the mdgbdata command fails with a non-zero exit code
    And the mdgbdata stderr contains "Input file is not valid JSON"

  Scenario: help prints command usage summary
    When I run mdgbdata command "help"
    Then the mdgbdata command succeeds
    And the mdgbdata stdout contains "tojson"
    And the mdgbdata stdout contains "tomd"