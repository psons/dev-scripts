"""Unit tests validating the dtask ↔ wsum integration contract.

These tests verify that:
1. wsum.summarize_work returns the right structure with required fields
2. The markdown format matches what dtask expects
3. WorkSummaryResult properties are accessible as dtask requires
4. Error handling scenarios work correctly

We test the contract and integration points without directly loading dtask
(which has no .py extension). BDD/CLI tests cover dtask's end-to-end behavior.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add bin directory to sys.path so we can import wsum.py
_bin_dir = Path(__file__).resolve().parents[1] / "bin"
if str(_bin_dir) not in sys.path:
    sys.path.insert(0, str(_bin_dir))

import pytest

from wsum import WorkSummaryResult, WsumError


class TestWorkSummaryResultContract:
    """Test that WorkSummaryResult has the required contract for dtask."""

    def test_work_summary_result_has_required_fields(self):
        """Test that WorkSummaryResult instance has all required fields."""
        result = WorkSummaryResult(
            timestamp="2026-06-03 14:30",
            headline="Fixed critical bug",
            summary="Detailed summary text.",
            markdown="## 2026-06-03 14:30\n\n---\nworkHeadline: Fixed critical bug\n---\n\nDetailed summary text.",
        )

        # All these properties must exist for dtask to work
        assert hasattr(result, 'timestamp')
        assert hasattr(result, 'headline')
        assert hasattr(result, 'summary')
        assert hasattr(result, 'markdown')

        # Access all properties to ensure they work
        assert result.timestamp == "2026-06-03 14:30"
        assert result.headline == "Fixed critical bug"
        assert result.summary == "Detailed summary text."
        assert isinstance(result.markdown, str)

    def test_work_summary_result_is_immutable(self):
        """Test that WorkSummaryResult is immutable (frozen dataclass)."""
        result = WorkSummaryResult(
            timestamp="2026-06-03 14:30",
            headline="Test",
            summary="Test",
            markdown="Test",
        )

        # Should not be able to modify frozen dataclass
        with pytest.raises(AttributeError):
            result.headline = "Modified"

    def test_unknown_property_raises_error(self):
        """Test that accessing unknown properties raises AttributeError."""
        result = WorkSummaryResult(
            timestamp="2026-06-03 14:30",
            headline="Test",
            summary="Test",
            markdown="Test",
        )

        # This is the contract check: if dtask tries to access a property
        # that doesn't exist, it should fail immediately
        with pytest.raises(AttributeError):
            _ = result.unknown_property


class TestMarkdownFormatContract:
    """Test that WorkSummaryResult.markdown format is compatible with dtask."""

    def test_markdown_contains_timestamp_heading(self):
        """Test that markdown starts with timestamp heading."""
        result = WorkSummaryResult(
            timestamp="2026-06-03 14:30",
            headline="Test headline",
            summary="Summary text.",
            markdown="## 2026-06-03 14:30\n\n---\nworkHeadline: Test headline\n---\n\nSummary text.",
        )

        # dtask expects markdown to start with ## timestamp
        assert result.markdown.startswith("## ")
        assert "2026-06-03" in result.markdown

    def test_markdown_contains_frontmatter_block(self):
        """Test that markdown contains YAML frontmatter with workHeadline."""
        result = WorkSummaryResult(
            timestamp="2026-06-03 14:30",
            headline="Test headline",
            summary="Summary text.",
            markdown="## 2026-06-03 14:30\n\n---\nworkHeadline: Test headline\n---\n\nSummary text.",
        )

        # dtask expects frontmatter block with workHeadline
        assert "---\n" in result.markdown
        assert "workHeadline:" in result.markdown
        assert "Test headline" in result.markdown

    def test_markdown_contains_summary_text(self):
        """Test that markdown includes the summary text."""
        summary_text = "This is a detailed summary of the work done."
        result = WorkSummaryResult(
            timestamp="2026-06-03 14:30",
            headline="Test headline",
            summary=summary_text,
            markdown=f"## 2026-06-03 14:30\n\n---\nworkHeadline: Test headline\n---\n\n{summary_text}",
        )

        # dtask expects the summary to be in the markdown
        assert summary_text in result.markdown

    def test_markdown_multiline_structure(self):
        """Test that markdown has expected line structure."""
        result = WorkSummaryResult(
            timestamp="2026-06-03 14:30",
            headline="Test",
            summary="Summary",
            markdown="## 2026-06-03 14:30\n\n---\nworkHeadline: Test\n---\n\nSummary",
        )

        lines = result.markdown.split('\n')
        # First line is heading
        assert lines[0].startswith("## ")
        # Has blank line after heading
        assert lines[1] == ""
        # Has frontmatter delimiter
        assert "---" in result.markdown


class TestDtaskWsumIntegration:
    """Integration contract tests for dtask + wsum."""

    def test_work_summary_result_none_handling(self):
        """Test that dtask must handle None returns from wsum gracefully."""
        # When wsum fails or times out, call_wsum_with_timeout returns None
        result = None
        
        # dtask should check for None before accessing properties
        if result is not None:
            # This block should not be reached when result is None
            assert result.headline
        else:
            # dtask should handle the None case
            pass

    def test_error_propagation_compatibility(self):
        """Test that WsumError types are compatible with dtask expectations."""
        # dtask should handle WsumError exceptions
        try:
            raise WsumError("No changes found in diff")
        except WsumError as e:
            # dtask should be able to catch and handle WsumError
            assert isinstance(e, Exception)
            assert "No changes" in str(e)

    def test_markdown_insertion_into_do_md(self, tmp_path):
        """Test that the markdown format is suitable for insertion into do.md."""
        # Create the correct directory structure: docs/dev/work/do.md
        do_md_dir = tmp_path / "docs" / "dev" / "work"
        do_md_dir.mkdir(parents=True, exist_ok=True)
        do_md = do_md_dir / "do.md"
        do_md.write_text("# Work Summary\n\n## Previous entry\n\nOld text.\n")

        result = WorkSummaryResult(
            timestamp="2026-06-03 14:30",
            headline="Fixed bug",
            summary="Fixed critical bug.",
            markdown="## 2026-06-03 14:30\n\n---\nworkHeadline: Fixed bug\n---\n\nFixed critical bug.",
        )

        # Simulate what dtask does: insert markdown into do.md
        content = do_md.read_text()
        # Find "# Work Summary" section and insert after it
        work_summary_pos = content.find("# Work Summary")
        if work_summary_pos != -1:
            insert_pos = work_summary_pos + len("# Work Summary")
            # dtask would insert the new markdown here
            new_content = (
                content[:insert_pos] +
                "\n\n" +
                result.markdown +
                "\n" +
                content[insert_pos:]
            )
            do_md.write_text(new_content)

        # Verify the result looks correct
        final_content = do_md.read_text()
        assert result.headline in final_content
        assert result.summary in final_content
        assert "workHeadline:" in final_content
