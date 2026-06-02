Feature: wsum command behavior without dtask integration
  As a developer
  I want predictable wsum CLI behavior for diff selection and markdown output
  So that work summaries are generated consistently from git diffs

  Background:
    Given a git repository with tracked files for wsum
    And a fake gemini cli is available for wsum tests

  Scenario: default invocation summarizes staged changes only
    Given the tracked file "file-one.txt" has staged changes with content "staged-change-one"
    And the tracked file "file-two.txt" has unstaged changes with content "unstaged-change-two"
    And the untracked file "notes.txt" exists with content "untracked-change"
    When I run wsum command "wsum"
    Then the wsum command succeeds
    And the markdown output contains "file-one.txt"
    And the markdown output does not contain "file-two.txt"
    And the markdown output does not contain "notes.txt"

  Scenario: --all includes staged, tracked unstaged, and untracked changes
    Given the tracked file "file-one.txt" has staged changes with content "staged-change-one"
    And the tracked file "file-two.txt" has unstaged changes with content "unstaged-change-two"
    And the untracked file "notes.txt" exists with content "untracked-change"
    When I run wsum command "wsum --all"
    Then the wsum command succeeds
    And the markdown output contains "file-one.txt"
    And the markdown output contains "file-two.txt"
    And the markdown output contains "notes.txt"

  Scenario: --update includes tracked unstaged changes but excludes untracked files
    Given the tracked file "file-one.txt" has staged changes with content "staged-change-one"
    And the tracked file "file-two.txt" has unstaged changes with content "unstaged-change-two"
    And the untracked file "notes.txt" exists with content "untracked-change"
    When I run wsum command "wsum --update"
    Then the wsum command succeeds
    And the markdown output contains "file-one.txt"
    And the markdown output contains "file-two.txt"
    And the markdown output does not contain "notes.txt"

  Scenario: --base compares against a different ref
    Given I have committed a tracked file change "file-two.txt" with content "committed-against-base"
    When I run wsum command "wsum --base HEAD~1"
    Then the wsum command succeeds
    And the markdown output contains "file-two.txt"

  Scenario: stdin diff input takes precedence over internal git diff
    Given the tracked file "file-one.txt" has staged changes with content "staged-change-one"
    When I run wsum command "wsum" with stdin diff:
      """
      diff --git a/custom.txt b/custom.txt
      index 1111111..2222222 100644
      --- a/custom.txt
      +++ b/custom.txt
      @@ -1 +1 @@
      -old
      +new
      """
    Then the wsum command succeeds
    And the markdown output contains "custom.txt"
    And the markdown output does not contain "file-one.txt"

  Scenario: command fails when there is no diff to summarize
    Given there are no staged or unstaged changes
    When I run wsum command "wsum"
    Then the wsum command fails with a non-zero exit code
    And the wsum error output mentions "No changes found in diff"

  Scenario: command fails when an unsupported extra diff arg is provided
    Given the tracked file "file-one.txt" has staged changes with content "staged-change-one"
    When I run wsum command "wsum --extra-diff-arg bogus-flag"
    Then the wsum command fails with a non-zero exit code
    And the wsum error output mentions "unsupported extra diff argument"

  Scenario: markdown output is compatible with do.md work summary format
    Given the tracked file "file-one.txt" has staged changes with content "staged-change-one"
    When I run wsum command "wsum"
    Then the wsum command succeeds
    And the markdown output starts with a timestamp heading
    And the markdown output includes workHeadline frontmatter
