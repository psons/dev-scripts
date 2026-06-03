# Testing the wsum.summarize_work Integration with dtask

This document outlines the recommended approach for testing the `wsum.summarize_work` function and ensuring a strict integration contract when it is called dynamically by `dtask`. 

## Testing Strategies: Complementary Approaches

The project uses two complementary testing strategies:

1. **BDD/CLI Tests** (existing in `tests/features/wsum/wsum.feature`): Test `wsum.py` as a command-line utility, covering:
   - User-facing CLI behavior (diff selection modes, markdown output format)
   - Integration with git commands
   - Output validation (YAML frontmatter, timestamps)

2. **Unit Tests** (proposed in this document): Test the internal Python API (`wsum.summarize_work`) and its integration with `dtask`, covering:
   - Function-level logic isolation
   - Edge cases and error conditions
   - Contract enforcement between modules
   - Integration with `dtask`'s dynamic import pattern

Since the project already uses `pytest-bdd` to cover high-level CLI workflows, unit testing the internal Python API is the most efficient strategy for ensuring contract compliance and catching regressions in the `dtask` ↔ `wsum` integration.

## 1. Testing `wsum.summarize_work` in Isolation

The `summarize_work` function relies on external dependencies: `subprocess.run` for git commands, and LLM calls via `run_gemini` and `headline_from_summary`. To avoid slow, flaky tests and API dependencies, mock these external functions directly rather than patching `subprocess.run` globally.

### Approach: Mock External Function Calls

Patch specific functions that `wsum` calls, not the lower-level `subprocess.run`. This approach is:
- **More robust**: Immune to internal refactoring that changes subprocess call count
- **More maintainable**: Each mock corresponds to a clear dependency
- **More secure**: Avoids writing fake executables or modifying PATH

### Code Example: Unit Testing wsum

```python
# tests/test_wsum_unit.py
import pytest
from unittest.mock import patch
from bin.wsum import summarize_work, WorkSummaryResult, WsumError


@patch('bin.wsum.headline_from_summary')
@patch('bin.wsum.run_gemini')
@patch('bin.wsum.collect_diff')
def test_summarize_work_success(mock_collect_diff, mock_run_gemini, mock_headline):
    """Test summarize_work produces correct WorkSummaryResult with mocked dependencies."""
    mock_collect_diff.return_value = "file.txt\n+new content\n"
    mock_run_gemini.return_value = "Added new content to file.txt."
    mock_headline.return_value = "feat(file): Add new content"
    
    result = summarize_work()
    
    assert isinstance(result, WorkSummaryResult)
    assert result.headline == "feat(file): Add new content"
    assert result.summary == "Added new content to file.txt."
    assert "workHeadline: feat(file): Add new content" in result.markdown
    assert "## " in result.markdown  # Timestamp heading


@patch('bin.wsum.collect_diff')
def test_summarize_work_empty_diff(mock_collect_diff):
    """Test summarize_work raises WsumError when diff is empty."""
    mock_collect_diff.return_value = ""
    
    with pytest.raises(WsumError, match="No changes found"):
        summarize_work()


@patch('bin.wsum.run_gemini')
@patch('bin.wsum.collect_diff')
def test_summarize_work_respects_parameters(mock_collect_diff, mock_run_gemini):
    """Test summarize_work passes parameters to collect_diff correctly."""
    mock_collect_diff.return_value = "diff output"
    mock_run_gemini.return_value = "Summary text"
    
    # Call with specific parameters
    summarize_work(
        staged_only=False,
        include_unstaged=True,
        include_untracked=True,
        base_ref="origin/main"
    )
    
    # Verify collect_diff was called with the correct parameters
    mock_collect_diff.assert_called_once()
    call_kwargs = mock_collect_diff.call_args[1]
    assert call_kwargs['staged_only'] is False
    assert call_kwargs['include_unstaged'] is True
    assert call_kwargs['include_untracked'] is True
    assert call_kwargs['base_ref'] == "origin/main"
```

## 2. Assuring the `dtask` Contract with wsum

`dtask` dynamically imports `wsum` inside `call_wsum_with_timeout()` to call `summarize_work`. It must be guaranteed that:

1. `call_wsum_with_timeout` calls `wsum.summarize_work` with the correct parameters based on commit scope
2. `dtask` only accesses properties that exist on `WorkSummaryResult`
3. Timeout and error handling work correctly
4. `dtask` integrates the returned markdown into `do.md` properly

### A. Testing `call_wsum_with_timeout` in Isolation

When testing `call_wsum_with_timeout`, mock only `wsum.summarize_work`, not the entire wsum module. This validates that dtask correctly invokes wsum and handles its response, while allowing wsum's implementation to be tested separately.

```python
# tests/test_dtask_wsum_integration.py
import pytest
from unittest.mock import patch, MagicMock
from bin.dtask import call_wsum_with_timeout
from bin.wsum import WorkSummaryResult


@patch('bin.dtask.wsum.summarize_work')
def test_call_wsum_with_timeout_calls_summarize_work(mock_summarize):
    """Test that call_wsum_with_timeout invokes wsum.summarize_work with correct parameters."""
    expected_result = WorkSummaryResult(
        timestamp="2026-06-03 14:30",
        headline="Fixed the thing",
        summary="Summary of fixes.",
        markdown="## 2026-06-03 14:30\n\n---\nworkHeadline: Fixed the thing\n---\n\nSummary of fixes."
    )
    mock_summarize.return_value = expected_result
    
    result = call_wsum_with_timeout(
        repo_root="/tmp/test-repo",
        include_unstaged=True,
        include_untracked=False,
        timeout_sec=45
    )
    
    # Verify call_wsum_with_timeout returned the result
    assert result == expected_result
    
    # Verify wsum.summarize_work was called with the correct parameters
    mock_summarize.assert_called_once()
    call_kwargs = mock_summarize.call_args[1]
    assert call_kwargs['staged_only'] is False  # Not staged_only because include_unstaged=True
    assert call_kwargs['include_unstaged'] is True
    assert call_kwargs['include_untracked'] is False


@patch('bin.dtask.wsum.summarize_work')
def test_call_wsum_with_timeout_respects_commit_scope(mock_summarize, tmp_path):
    """Test that dtask --all mode maps correctly to wsum include_unstaged/include_untracked."""
    mock_summarize.return_value = WorkSummaryResult(
        timestamp="2026-06-03 14:30",
        headline="Test",
        summary="Test",
        markdown="Test"
    )
    
    # Test --all semantics
    call_wsum_with_timeout(tmp_path, include_unstaged=True, include_untracked=True)
    call_kwargs = mock_summarize.call_args[1]
    assert call_kwargs['staged_only'] is False
    assert call_kwargs['include_unstaged'] is True
    assert call_kwargs['include_untracked'] is True


@patch('bin.dtask.wsum.summarize_work')
def test_call_wsum_with_timeout_error_handling(mock_summarize):
    """Test that call_wsum_with_timeout returns None on exception."""
    mock_summarize.side_effect = Exception("LLM API failed")
    
    result = call_wsum_with_timeout(
        repo_root="/tmp/test-repo",
        timeout_sec=45
    )
    
    assert result is None
```

### B. Return Real Dataclass Instances in Mock Tests

**Critical rule**: When writing tests for `dtask`, mock `call_wsum_with_timeout` (or `wsum.summarize_work`), but **return real instantiated `WorkSummaryResult` objects**, not generic `MagicMock` instances.

Why? If `dtask` attempts to access a property that does not exist on `WorkSummaryResult` (e.g., `wsum_result.unsupported_prop`), Python will raise `AttributeError` and fail the test immediately. This acts as a live contract check.

```python
# tests/test_dtask.py
from unittest.mock import patch
from bin.wsum import WorkSummaryResult


@patch('bin.dtask.call_wsum_with_timeout')
def test_dtask_wsum_commit_inserts_markdown(mock_wsum, tmp_path):
    """Test that dtask inserts wsum markdown into do.md correctly."""
    # Return a REAL instance to enforce the property contract
    mock_wsum.return_value = WorkSummaryResult(
        timestamp="2026-06-02 12:00",
        headline="Fixed the thing",
        summary="Summary of fixes.",
        markdown="## 2026-06-02 12:00\n\n---\nworkHeadline: Fixed the thing\n---\n\nSummary of fixes."
    )
    
    # Create test do.md file
    do_md_path = tmp_path / "do.md"
    do_md_path.write_text("# Work Summary\n\n## Old Summary\n\nOld content.\n")
    
    # Call dtask with --wsum option
    # (Verify that dtask calls insert_work_summary_into_do_md with the result)
    # This is pseudocode; actual implementation depends on dtask's command structure
    result = mock_wsum.return_value
    assert "workHeadline: Fixed the thing" in result.markdown


@patch('bin.dtask.call_wsum_with_timeout')
def test_dtask_wsum_timeout_handling(mock_wsum):
    """Test that dtask handles None return from call_wsum_with_timeout (timeout/error)."""
    mock_wsum.return_value = None
    
    # Verify dtask handles the None case gracefully
    # (Actual assertions depend on dtask's behavior with None result)
    pass
```

### C. Static Type Hinting for IDE Support (Optional Best Practice)

Because `dtask` imports `wsum` dynamically inside `call_wsum_with_timeout`, static type checkers and IDEs lose context. You can restore this context using Python's `TYPE_CHECKING` flag. This allows `mypy` or `pyright` to catch contract violations before the code runs.

```python
# In bin/dtask
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bin.wsum import WorkSummaryResult

# Later in insert_work_summary_into_do_md or other functions...
def insert_work_summary_into_do_md(do_md_path: str, result: 'WorkSummaryResult | None') -> None:
    if result is None:
        return
    
    # IDE will now warn if you access result.invalid_prop
    headline = result.workHeadline  # ✓ IDE knows this exists
    summary = result.markdown       # ✓ IDE knows this exists
```
