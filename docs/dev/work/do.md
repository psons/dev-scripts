---
"actualCommitMessage": "clean up usecases to match backlog grooming"
"description": "A list of small, focused tasks guiding the current commit with detailed\
  \ microsected activities."
"intendedCommitMessage": "clean up usecases to match backlog grooming"
"priorCommit": "5000c03253d544629f9bcdd0f2683974002f95ff"
"title": "do.md"
"workBranch": "usecase-grooming"
---



a - Tech tests: Fill in tests for implementation behaviors and prevent future breakage
    - What is he best way to discover the need for such tests?  Run coverage?
    - abandoned due to complexity running coverage and getting a report from tests that run in subprocesses.
        The subprocesses are part of the tests that use monkey patching on return attributes to make the tests deterministic.

