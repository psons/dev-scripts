"""Unit tests for wsum.summarize_work and related functions.

These tests isolate wsum's internal logic by mocking external dependencies
(git commands, LLM calls) rather than patching subprocess.run globally.
This approach is robust against internal refactoring and maintains clear
dependency boundaries.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add bin directory to sys.path so we can import wsum.py
_bin_dir = Path(__file__).resolve().parents[1] / "bin"
if str(_bin_dir) not in sys.path:
    sys.path.insert(0, str(_bin_dir))

import pytest
from unittest.mock import patch, MagicMock

from wsum import (
    summarize_work,
    WorkSummaryResult,
    WsumError,
    collect_diff,
    run_gemini,
    headline_from_summary,
    _validate_extra_diff_args,
)


class TestValidateExtraDiffArgs:
    """Test the _validate_extra_diff_args allow-list enforcement."""

    def test_no_extra_args(self):
        """Test that empty list returns empty list."""
        result = _validate_extra_diff_args(None)
        assert result == []

    def test_allowed_flag_args(self):
        """Test that allowed flags pass through."""
        result = _validate_extra_diff_args(["--stat", "--name-only", "-w"])
        assert result == ["--stat", "--name-only", "-w"]

    def test_allowed_prefix_args(self):
        """Test that allowed prefix arguments pass through."""
        result = _validate_extra_diff_args(["--unified=5", "-U3"])
        assert result == ["--unified=5", "-U3"]

    def test_disallowed_arg_raises_error(self):
        """Test that disallowed arguments raise WsumError."""
        with pytest.raises(WsumError, match="unsupported extra diff argument"):
            _validate_extra_diff_args(["--disallowed-arg"])

    def test_mix_allowed_and_disallowed(self):
        """Test that any disallowed arg causes failure."""
        with pytest.raises(WsumError):
            _validate_extra_diff_args(["--stat", "--evil-arg"])


class TestSummarizeWork:
    """Test summarize_work end-to-end with mocked dependencies."""

    @patch('wsum.headline_from_summary')
    @patch('wsum.run_gemini')
    @patch('wsum.collect_diff')
    def test_summarize_work_success(
        self,
        mock_collect_diff,
        mock_run_gemini,
        mock_headline,
    ):
        """Test summarize_work produces correct WorkSummaryResult with mocked dependencies."""
        mock_collect_diff.return_value = "file.txt\n+new content\n"
        mock_run_gemini.return_value = "Added new content to file.txt."
        mock_headline.return_value = "feat(file): Add new content"

        result = summarize_work()

        assert isinstance(result, WorkSummaryResult)
        assert result.headline == "feat(file): Add new content"
        assert result.summary == "Added new content to file.txt."
        assert 'workHeadline: "feat(file): Add new content"' in result.markdown
        assert "## " in result.markdown  # Timestamp heading present

    @patch('wsum.collect_diff')
    def test_summarize_work_empty_diff(self, mock_collect_diff):
        """Test summarize_work raises WsumError when diff is empty."""
        mock_collect_diff.return_value = ""

        with pytest.raises(WsumError, match="No changes found"):
            summarize_work()

    @patch('wsum.collect_diff')
    def test_summarize_work_whitespace_only_diff(self, mock_collect_diff):
        """Test summarize_work raises WsumError when diff contains only whitespace."""
        mock_collect_diff.return_value = "   \n\n  "

        with pytest.raises(WsumError, match="No changes found"):
            summarize_work()

    @patch('wsum.run_gemini')
    @patch('wsum.collect_diff')
    def test_summarize_work_respects_parameters(
        self,
        mock_collect_diff,
        mock_run_gemini,
    ):
        """Test summarize_work passes parameters to collect_diff correctly."""
        mock_collect_diff.return_value = "diff output"
        mock_run_gemini.return_value = "Summary text"

        # Call with specific parameters
        summarize_work(
            staged_only=False,
            include_unstaged=True,
            include_untracked=True,
            base_ref="origin/main",
        )

        # Verify collect_diff was called with the correct parameters
        mock_collect_diff.assert_called_once()
        call_kwargs = mock_collect_diff.call_args[1]
        assert call_kwargs['staged_only'] is False
        assert call_kwargs['include_unstaged'] is True
        assert call_kwargs['include_untracked'] is True
        assert call_kwargs['base_ref'] == "origin/main"

    @patch('wsum.run_gemini')
    @patch('wsum.collect_diff')
    def test_summarize_work_with_diff_text_input(
        self,
        mock_collect_diff,
        mock_run_gemini,
    ):
        """Test summarize_work skips collect_diff when diff_text is provided."""
        mock_run_gemini.return_value = "Summary"

        custom_diff = "custom diff content"
        summarize_work(diff_text=custom_diff)

        # collect_diff should not be called when diff_text is provided
        mock_collect_diff.assert_not_called()
        # run_gemini should be called with the provided diff
        mock_run_gemini.assert_called_once()
        call_args = mock_run_gemini.call_args
        assert call_args[0][0] == custom_diff

    @patch('wsum.headline_from_summary')
    @patch('wsum.run_gemini')
    @patch('wsum.collect_diff')
    def test_summarize_work_max_sentences_parameter(
        self,
        mock_collect_diff,
        mock_run_gemini,
        mock_headline,
    ):
        """Test summarize_work passes max_sentences to run_gemini."""
        mock_collect_diff.return_value = "diff"
        mock_run_gemini.return_value = "Summary"
        mock_headline.return_value = "Headline"

        summarize_work(max_sentences=10)

        # Verify run_gemini was called with max_sentences
        call_kwargs = mock_run_gemini.call_args[1]
        assert call_kwargs['max_sentences'] == 10

    @patch('wsum.run_gemini')
    @patch('wsum.collect_diff')
    def test_summarize_work_gemini_error(
        self,
        mock_collect_diff,
        mock_run_gemini,
    ):
        """Test summarize_work propagates WsumError from run_gemini."""
        mock_collect_diff.return_value = "diff"
        mock_run_gemini.side_effect = WsumError("Gemini API failed")

        with pytest.raises(WsumError, match="Gemini API failed"):
            summarize_work()

    @patch('wsum.headline_from_summary')
    @patch('wsum.run_gemini')
    @patch('wsum.collect_diff')
    def test_summarize_work_markdown_contains_all_parts(
        self,
        mock_collect_diff,
        mock_run_gemini,
        mock_headline,
    ):
        """Test that returned markdown contains timestamp, frontmatter, and summary."""
        mock_collect_diff.return_value = "diff"
        mock_run_gemini.return_value = "This is the summary text."
        mock_headline.return_value = "Short headline"

        result = summarize_work()

        markdown = result.markdown
        # Check structure
        assert markdown.startswith("\n## ")  # Timestamp heading
        assert "---\n" in markdown  # Frontmatter delimiters
        assert 'workHeadline: "Short headline"' in markdown
        assert "This is the summary text." in markdown

    @patch('wsum.headline_from_summary')
    @patch('wsum.run_gemini')
    @patch('wsum.collect_diff')
    def test_summarize_work_markdown_quotes_and_escapes_headline(
        self,
        mock_collect_diff,
        mock_run_gemini,
        mock_headline,
    ):
        """Test that markdown renders workHeadline as quoted single-line YAML."""
        mock_collect_diff.return_value = "diff"
        mock_run_gemini.return_value = "Summary"
        mock_headline.return_value = 'Fix "quoted" value: path\\name'

        result = summarize_work()

        assert 'workHeadline: "Fix \\"quoted\\" value: path\\\\name"' in result.markdown


class TestRunGemini:
    """Test run_gemini function with mocked subprocess."""

    @patch('wsum.subprocess.run')
    def test_run_gemini_success(self, mock_run):
        """Test run_gemini returns summary text on success."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Generated summary text.",
            stderr="",
        )

        result = run_gemini("diff content")

        assert result == "Generated summary text."
        mock_run.assert_called_once()

    @patch('wsum.subprocess.run')
    def test_run_gemini_subprocess_not_found(self, mock_run):
        """Test run_gemini raises WsumError when gemini CLI not found."""
        mock_run.side_effect = FileNotFoundError("gemini not found")

        with pytest.raises(WsumError, match="gemini CLI not found in PATH"):
            run_gemini("diff")

    @patch('wsum.subprocess.run')
    def test_run_gemini_non_zero_exit(self, mock_run):
        """Test run_gemini raises WsumError on non-zero exit code."""
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="",
            stderr="API error: rate limit exceeded",
        )

        with pytest.raises(WsumError, match="gemini CLI failed: API error"):
            run_gemini("diff")

    @patch('wsum.subprocess.run')
    def test_run_gemini_empty_output(self, mock_run):
        """Test run_gemini raises WsumError when output is empty."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="",
            stderr="",
        )

        with pytest.raises(WsumError, match="empty summary"):
            run_gemini("diff")

    @patch('wsum.subprocess.run')
    def test_run_gemini_passes_model_parameter(self, mock_run):
        """Test run_gemini includes model parameter in command."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Summary",
            stderr="",
        )

        run_gemini("diff", model="gemini-2.0")

        # Verify -m model was included in command
        call_args = mock_run.call_args
        cmd = call_args[0][0]
        assert "-m" in cmd
        assert "gemini-2.0" in cmd


class TestHeadlineFromSummary:
    """Test headline_from_summary function."""

    @patch('wsum.subprocess.run')
    def test_headline_from_summary_success(self, mock_run):
        """Test headline_from_summary returns trimmed headline."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Fixed critical bug in auth module",
            stderr="",
        )

        result = headline_from_summary("Long summary text here.")

        assert result == "Fixed critical bug in auth module"

    @patch('wsum.subprocess.run')
    def test_headline_from_summary_removes_quotes(self, mock_run):
        """Test headline_from_summary strips surrounding quotes."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout='"Fixed the bug"',
            stderr="",
        )

        result = headline_from_summary("Summary")

        assert result == "Fixed the bug"
        assert '"' not in result

    @patch('wsum.subprocess.run')
    def test_headline_from_summary_max_length_truncation(self, mock_run):
        """Test headline_from_summary enforces max_len by word boundary."""
        long_headline = "This is a very long headline that should be truncated at word boundary to stay under max length"
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout=long_headline,
            stderr="",
        )

        result = headline_from_summary("Summary", max_len=50)

        assert len(result) <= 50
        # Should end at word boundary, not mid-word
        assert result.endswith(" ") is False or result == result.rstrip()

    @patch('wsum.subprocess.run')
    def test_headline_from_summary_subprocess_not_found(self, mock_run):
        """Test headline_from_summary raises WsumError when gemini CLI not found."""
        mock_run.side_effect = FileNotFoundError("gemini not found")

        with pytest.raises(WsumError, match="gemini CLI not found"):
            headline_from_summary("Summary")

    @patch('wsum.subprocess.run')
    def test_headline_from_summary_api_error(self, mock_run):
        """Test headline_from_summary propagates API errors."""
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="",
            stderr="Unauthorized",
        )

        with pytest.raises(WsumError, match="gemini CLI failed"):
            headline_from_summary("Summary")
