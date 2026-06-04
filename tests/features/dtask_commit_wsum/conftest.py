"""pytest configuration for dtask commit --wsum feature tests

This conftest provides fixtures for dtask commit --wsum scenarios.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from wsum import WorkSummaryResult

# Import the shared GitRepoTestFixture
from tests.steps.conftest import GitRepoTestFixture


@pytest.fixture(scope="function")
def mock_gemini_in_path():
    """Create a temporary directory with a fake gemini CLI script, add it to PATH.
    
    Function-scoped so it doesn't interfere with other feature tests.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        fake_gemini = Path(tmpdir) / "gemini"
        
        # Create a minimal gemini CLI that echoes deterministic output
        fake_gemini.write_text("""#!/bin/sh
# Fake gemini CLI for testing dtask --wsum scenarios
# Returns deterministic output based on stdin

# Read prompt and input from stdin
INPUT=$(cat)

# Extract the prompt portion to create output
# Simple implementation: return a deterministic summary
echo "Mocked gemini summary: Work completed successfully. Key changes made and tested."
""")
        
        fake_gemini.chmod(0o755)
        
        # Prepend to PATH
        old_path = os.environ.get('PATH', '')
        os.environ['PATH'] = f"{tmpdir}:{old_path}"
        
        try:
            yield tmpdir
        finally:
            # Restore original PATH
            os.environ['PATH'] = old_path


@pytest.fixture(autouse=True)
def mock_wsum_summarize():
    """Autouse fixture that patches wsum.summarize_work for all tests in this feature.
    
    This prevents tests from calling the real Gemini CLI and provides deterministic results.
    """
    with patch('wsum.summarize_work') as mock_summarize:
        # Default mock returns a valid WorkSummaryResult
        mock_summarize.return_value = WorkSummaryResult(
            timestamp="2026-06-03 14:30",
            headline="Work summary from mocked wsum",
            summary="This is a mocked work summary.",
            markdown="## 2026-06-03 14:30\n\n---\nworkHeadline: Work summary from mocked wsum\n---\n\nThis is a mocked work summary."
        )
        yield mock_summarize


@pytest.fixture
def commit_wsum_repo(tmp_path, mock_gemini_in_path, mock_wsum_summarize):
    """Fixture providing a git repository initialized with do.md for commit testing.
    
    Uses pytest's tmp_path which retains temp directories from the last 3 runs.
    Configure retention with: pytest --basetemp=<dir> or in pytest.ini via tmp_path_retention_count.
    """
    repo = GitRepoTestFixture(tmp_path)
    
    # Initialize a work branch with do.md (mimics dtask init --workbranch)
    repo.run_git_command(["checkout", "-b", "work-branch"])
    
    # Create docs/dev/work directory
    docs_path = repo.repo_dir / "docs" / "dev" / "work"
    docs_path.mkdir(parents=True, exist_ok=True)

    # Seed tracked files used by --update/--all scenarios.
    (repo.repo_dir / "file-one.txt").write_text("Initial file-one content\n")
    (repo.repo_dir / "file-two.txt").write_text("Initial file-two content\n")
    
    # Create do.md with proper frontmatter
    do_md_path = docs_path / "do.md"
    frontmatter_dict = {
        "workBranch": "work-branch",
        "title": "do.md",
        "description": "A list of small, focused tasks guiding the current commit with detailed microsected activities.",
    }
    body = "\n# Work Summary\n\n"
    
    fm_str = "---\n"
    for key, value in frontmatter_dict.items():
        fm_str += f"{key}: {value}\n"
    fm_str += "---"
    
    do_md_path.write_text(fm_str + body)
    repo.run_git_command(["add", "docs/dev/work/do.md", "file-one.txt", "file-two.txt"])
    repo.run_git_command(["commit", "-m", "Initialize do.md and tracked files"])
    
    # Store reference to the mock for customization in tests
    repo.mock_wsum_summarize = mock_wsum_summarize
    
    yield repo


@pytest.fixture(autouse=True)
def ensure_mock_gemini(request, mock_gemini_in_path):
    """Autouse fixture to ensure fake gemini is in PATH for all tests in this feature."""
    if 'dtask_commit_wsum' in str(request.fspath):
        yield
    else:
        yield
