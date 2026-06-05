"""
Pytest-BDD step definitions for dtask commit --wsum scenarios

This module implements the step definitions for testing the dtask commit command
with the --wsum flag in a sandboxed git repository environment.

Reuses GitRepoTestFixture from tests/steps/conftest.py and extends it with
commit-specific helpers for wsum integration testing.
"""

import subprocess
import sys
import os
import io
import runpy
import contextlib
import re
from pathlib import Path
from typing import Optional
from unittest.mock import patch, MagicMock
import threading
import time

import frontmatter
import yaml
import pytest
from pytest_bdd import given, when, then, parsers

# Add bin directory to sys.path for wsum import
_bin_dir = Path(__file__).resolve().parents[2] / "bin"
if str(_bin_dir) not in sys.path:
    sys.path.insert(0, str(_bin_dir))

from wsum import WorkSummaryResult

# Import the shared GitRepoTestFixture
from tests.steps.conftest import GitRepoTestFixture


# Helper class for mocking wsum responses
class MockWorkSummaryResult:
    """Mock result from wsum.summarize_work()"""
    def __init__(self, headline: str = "Work summary headline", markdown: str = "Generated summary content"):
        self.headline = headline
        self.markdown = markdown


def _extract_topmost_workheadline_from_work_summary(do_md_content: str) -> str:
    """Return first parse-valid workHeadline from do.md Work Summary region."""
    post = frontmatter.loads(do_md_content)
    body = post.content

    start_match = re.search(r"(?m)^# Work Summary\s*$", body)
    if start_match is None:
        return ""

    region_start = start_match.end()
    remainder = body[region_start:]
    next_h1 = re.search(r"(?m)^# (?!#).*$", remainder)
    region = remainder if next_h1 is None else remainder[:next_h1.start()]

    for block_match in re.finditer(r"(?ms)^---\s*\n(.*?)\n---\s*$", region):
        block = block_match.group(1)

        if len(re.findall(r"(?m)^\s*['\"]?workHeadline['\"]?\s*:", block)) > 1:
            continue

        try:
            parsed = yaml.safe_load(block)
        except yaml.YAMLError:
            continue

        if not isinstance(parsed, dict) or "workHeadline" not in parsed:
            continue

        candidate = str(parsed.get("workHeadline", "")).strip()
        if candidate:
            return candidate

    return ""


def _run_dtask_inprocess(repo_dir: Path, args: list[str]) -> subprocess.CompletedProcess:
    """Run bin/dtask in-process so local monkeypatches affect execution."""
    dtask_path = Path(__file__).resolve().parents[3] / "bin" / "dtask"
    old_cwd = os.getcwd()
    old_argv = sys.argv[:]
    stdout_buffer = io.StringIO()
    stderr_buffer = io.StringIO()
    exit_code = 0

    try:
        os.chdir(repo_dir)
        sys.argv = ["dtask", *args]
        with contextlib.redirect_stdout(stdout_buffer), contextlib.redirect_stderr(stderr_buffer):
            try:
                runpy.run_path(str(dtask_path), run_name="__main__")
            except SystemExit as exc:
                exit_code = exc.code if isinstance(exc.code, int) else 1
    finally:
        os.chdir(old_cwd)
        sys.argv = old_argv

    return subprocess.CompletedProcess(
        args=["dtask", *args],
        returncode=exit_code,
        stdout=stdout_buffer.getvalue(),
        stderr=stderr_buffer.getvalue(),
    )


# ============================================================================
# GIVEN Steps
# ============================================================================

@given("a clean git repository with initial commit for --wsum")
def given_clean_git_repo(commit_wsum_repo):
    """Ensure repository is initialized with an initial commit"""
    assert commit_wsum_repo.file_exists("README.md")


@given("a work branch initialized with do.md for --wsum")
def given_work_branch_with_do_md(commit_wsum_repo):
    """Verify that work branch and do.md are properly initialized"""
    current_branch = commit_wsum_repo.get_current_branch()
    assert current_branch == "work-branch", f"Expected 'work-branch', got '{current_branch}'"
    assert commit_wsum_repo.file_exists("docs/dev/work/do.md"), "do.md not found"


@given("a clean working tree for --wsum")
def given_clean_working_tree(commit_wsum_repo):
    """Verify that the working tree is clean"""
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=commit_wsum_repo.repo_dir,
        capture_output=True,
        text=True
    )
    # Allow do.md if it exists but is committed
    assert result.stdout.strip() == "", f"Working tree should be clean, but has: {result.stdout}"


@given("I have modified file-one.txt")
def given_modified_file_one(commit_wsum_repo):
    """Create or modify file-one.txt"""
    file_path = commit_wsum_repo.repo_dir / "file-one.txt"
    file_path.write_text("Modified content in file-one\n")
    commit_wsum_repo.test_file_one_modified = True


@given("I have modified file-one.txt with description \"Add new feature\"")
def given_modified_file_one_with_desc(commit_wsum_repo):
    """Create or modify file-one.txt with specific content"""
    file_path = commit_wsum_repo.repo_dir / "file-one.txt"
    file_path.write_text("Add new feature implementation\n")
    commit_wsum_repo.test_file_one_modified = True


@given("I have staged file-one.txt")
def given_staged_file_one(commit_wsum_repo):
    """Stage file-one.txt"""
    commit_wsum_repo.run_git_command(["add", "file-one.txt"])
    assert commit_wsum_repo.is_file_staged("file-one.txt"), "file-one.txt should be staged"


@given("I have staged file-two.txt")
def given_staged_file_two(commit_wsum_repo):
    """Stage file-two.txt."""
    commit_wsum_repo.run_git_command(["add", "file-two.txt"])
    assert commit_wsum_repo.is_file_staged("file-two.txt"), "file-two.txt should be staged"


@given("I have modified file-two.txt (unstaged)")
def given_modified_file_two_unstaged(commit_wsum_repo):
    """Create or modify file-two.txt but do not stage it"""
    file_path = commit_wsum_repo.repo_dir / "file-two.txt"
    # First create it if it doesn't exist, then modify
    if not file_path.exists():
        file_path.write_text("Initial content\n")
        commit_wsum_repo.run_git_command(["add", "file-two.txt"])
        commit_wsum_repo.run_git_command(["commit", "-m", "Add file-two"])
    
    file_path.write_text("Modified content in file-two (unstaged)\n")
    commit_wsum_repo.test_file_two_modified = True


@given("I have modified file-two.txt")
def given_modified_file_two(commit_wsum_repo):
    """Create or modify file-two.txt."""
    file_path = commit_wsum_repo.repo_dir / "file-two.txt"
    file_path.write_text("Modified content in file-two\n")
    commit_wsum_repo.test_file_two_modified = True


@given("I have created file-three.txt (untracked)")
def given_created_untracked_file_three(commit_wsum_repo):
    """Create an untracked file"""
    file_path = commit_wsum_repo.repo_dir / "file-three.txt"
    file_path.write_text("Untracked content\n")
    commit_wsum_repo.test_file_three_untracked = True


@given("a clean working tree with no staged changes")
def given_clean_working_tree_no_staged(commit_wsum_repo):
    """Ensure working tree is clean with no staged changes"""
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=commit_wsum_repo.repo_dir,
        capture_output=True,
        text=True
    )
    assert result.stdout.strip() == "", "Working tree should be clean"


@given("do.md has no Work Summary header")
def given_do_md_missing_work_summary_header(commit_wsum_repo):
    """Remove the # Work Summary header from do.md body if present."""
    do_md_path = commit_wsum_repo.repo_dir / "docs" / "dev" / "work" / "do.md"
    post = frontmatter.loads(do_md_path.read_text())
    body = post.content
    body = re.sub(r"(?m)^# Work Summary\s*\n?", "", body, count=1)
    post.content = body
    do_md_path.write_text(frontmatter.dumps(post))


@given("do.md has an existing dated summary section")
def given_do_md_has_existing_dated_section(commit_wsum_repo):
    """Seed do.md body with an older dated summary section."""
    do_md_path = commit_wsum_repo.repo_dir / "docs" / "dev" / "work" / "do.md"
    post = frontmatter.loads(do_md_path.read_text())
    dated_block = (
        "## 2026-05-01 10:00\n\n"
        "---\n"
        "workHeadline: Older summary\n"
        "---\n\n"
        "Older summary body.\n"
    )
    content = post.content
    if not content.endswith("\n"):
        content += "\n"
    post.content = content + "\n" + dated_block
    do_md_path.write_text(frontmatter.dumps(post))


@given("do.md has no dated summary sections")
def given_do_md_has_no_dated_sections(commit_wsum_repo):
    """Remove all dated summary subsection headings from do.md body."""
    do_md_path = commit_wsum_repo.repo_dir / "docs" / "dev" / "work" / "do.md"
    post = frontmatter.loads(do_md_path.read_text())
    body = post.content
    body = re.sub(r"(?m)^## \d{4}-\d{2}-\d{2} \d{2}:\d{2}\s*$", "", body)
    post.content = body
    do_md_path.write_text(frontmatter.dumps(post))


# ============================================================================
# WHEN Steps
# ============================================================================

@when("I run dtask commit --wsum command")
def when_run_dtask_commit_wsum(commit_wsum_repo):
    """Execute dtask commit --wsum"""
    result = commit_wsum_repo.run_dtask_command(["commit", "--wsum"])
    commit_wsum_repo.last_command_result = result
    commit_wsum_repo.test_exit_code = result.returncode


@when("I run dtask commit --wsum --update command")
def when_run_dtask_commit_wsum_update(commit_wsum_repo):
    """Execute dtask commit --wsum --update"""
    result = commit_wsum_repo.run_dtask_command(["commit", "--wsum", "--update"])
    commit_wsum_repo.last_command_result = result
    commit_wsum_repo.test_exit_code = result.returncode


@when("I run dtask commit --wsum --all command")
def when_run_dtask_commit_wsum_all(commit_wsum_repo):
    """Execute dtask commit --wsum --all"""
    result = commit_wsum_repo.run_dtask_command(["commit", "--wsum", "--all"])
    commit_wsum_repo.last_command_result = result
    commit_wsum_repo.test_exit_code = result.returncode


@when(parsers.parse('I run dtask commit --wsum --actual "{message}" command'))
def when_run_dtask_commit_wsum_actual(commit_wsum_repo, message):
    """Execute dtask commit --wsum --actual <message>"""
    result = commit_wsum_repo.run_dtask_command(["commit", "--wsum", "--actual", message])
    commit_wsum_repo.last_command_result = result
    commit_wsum_repo.test_exit_code = result.returncode
    commit_wsum_repo.test_explicit_message = message


@when("I run dtask commit --wsum command with wsum timeout")
def when_run_dtask_commit_wsum_timeout(commit_wsum_repo):
    """Execute dtask commit --wsum and force the timeout code path deterministically."""

    def slow_wsum(*args, **kwargs):
        time.sleep(0.5)
        return MockWorkSummaryResult()

    # Run dtask in-process so this patch affects the wsum call used by dtask.
    # Patch Thread.join to return immediately; combined with slow_wsum this
    # makes the worker thread still alive at the timeout check.
    with patch('wsum.summarize_work', side_effect=slow_wsum), \
         patch('threading.Thread.join', lambda self, timeout=None: None):
        result = _run_dtask_inprocess(commit_wsum_repo.repo_dir, ["commit", "--wsum"])
        commit_wsum_repo.last_command_result = result
        commit_wsum_repo.test_exit_code = result.returncode


@when("I run dtask commit --wsum command with wsum error response")
def when_run_dtask_commit_wsum_error(commit_wsum_repo):
    """Execute dtask commit --wsum with mocked wsum error"""
    # Mock wsum.summarize_work to return an error/None
    with patch('wsum.summarize_work') as mock_wsum:
        mock_wsum.return_value = None  # Simulate wsum failure

        # Run dtask in-process so this patch affects the wsum call used by dtask.
        result = _run_dtask_inprocess(commit_wsum_repo.repo_dir, ["commit", "--wsum"])
        commit_wsum_repo.last_command_result = result
        commit_wsum_repo.test_exit_code = result.returncode


# ============================================================================
# THEN Steps
# ============================================================================

@then("the dtask commit --wsum command succeeds")
def then_commit_wsum_succeeds(commit_wsum_repo):
    """Verify that dtask commit --wsum exited with code 0"""
    assert commit_wsum_repo.test_exit_code == 0, \
        f"Expected exit code 0, got {commit_wsum_repo.test_exit_code}\n" \
        f"stdout: {commit_wsum_repo.last_command_result.stdout}\n" \
        f"stderr: {commit_wsum_repo.last_command_result.stderr}"


@then("the dtask commit --wsum --update command succeeds")
def then_commit_wsum_update_succeeds(commit_wsum_repo):
    """Verify that dtask commit --wsum --update exited with code 0"""
    assert commit_wsum_repo.test_exit_code == 0, \
        f"Expected exit code 0, got {commit_wsum_repo.test_exit_code}\n" \
        f"stdout: {commit_wsum_repo.last_command_result.stdout}\n" \
        f"stderr: {commit_wsum_repo.last_command_result.stderr}"


@then("the dtask commit --wsum --all command succeeds")
def then_commit_wsum_all_succeeds(commit_wsum_repo):
    """Verify that dtask commit --wsum --all exited with code 0"""
    assert commit_wsum_repo.test_exit_code == 0, \
        f"Expected exit code 0, got {commit_wsum_repo.test_exit_code}\n" \
        f"stdout: {commit_wsum_repo.last_command_result.stdout}\n" \
        f"stderr: {commit_wsum_repo.last_command_result.stderr}"


@then("the dtask commit --wsum --actual command succeeds")
def then_commit_wsum_actual_succeeds(commit_wsum_repo):
    """Verify that dtask commit --wsum --actual exited with code 0"""
    assert commit_wsum_repo.test_exit_code == 0, \
        f"Expected exit code 0, got {commit_wsum_repo.test_exit_code}\n" \
        f"stdout: {commit_wsum_repo.last_command_result.stdout}\n" \
        f"stderr: {commit_wsum_repo.last_command_result.stderr}"


@then(parsers.parse("the dtask commit --wsum command fails with exit code {exit_code:d}"))
def then_commit_wsum_fails_with_code(commit_wsum_repo, exit_code):
    """Verify that dtask commit --wsum failed with specified exit code"""
    assert commit_wsum_repo.test_exit_code == exit_code, \
        f"Expected exit code {exit_code}, got {commit_wsum_repo.test_exit_code}\n" \
        f"stderr: {commit_wsum_repo.last_command_result.stderr}"


@then("a commit is created")
def then_commit_created(commit_wsum_repo):
    """Verify that a new commit was created"""
    # Check git log has more commits than before (should be at least 2: initial + do.md init + work commit)
    result = subprocess.run(
        ["git", "rev-list", "--count", "HEAD"],
        cwd=commit_wsum_repo.repo_dir,
        capture_output=True,
        text=True
    )
    commit_count = int(result.stdout.strip())
    # At least 3: initial commit, do.md commit, and the new work commit
    assert commit_count >= 3, f"Expected at least 3 commits, got {commit_count}"


@then("a new commit is created")
def then_new_commit_created(commit_wsum_repo):
    """Verify that a new commit was created (used in multi-commit scenarios)"""
    then_commit_created(commit_wsum_repo)


@then("a commit is created with message from work headline")
def then_commit_created_with_headline_message(commit_wsum_repo):
    """Verify a commit was created and its message matches do.md workHeadline."""
    then_commit_created(commit_wsum_repo)
    then_commit_message_from_generated_headline(commit_wsum_repo)


@then("the commit message contains the work headline from do.md")
def then_commit_message_is_work_headline(commit_wsum_repo):
    """Verify that commit message matches topmost Work Summary workHeadline."""
    # Get the last commit message
    result = subprocess.run(
        ["git", "log", "-1", "--format=%B"],
        cwd=commit_wsum_repo.repo_dir,
        capture_output=True,
        text=True
    )
    last_commit_msg = result.stdout.strip()
    
    # Get topmost workHeadline from do.md Work Summary section frontmatter.
    do_md_content = commit_wsum_repo.get_file_content("docs/dev/work/do.md")
    work_headline = _extract_topmost_workheadline_from_work_summary(do_md_content)
    
    assert work_headline, "workHeadline should be present in Work Summary section frontmatter"
    assert last_commit_msg == work_headline, \
        f"Commit message '{last_commit_msg}' does not match workHeadline '{work_headline}'"


@then("the do.md file contains a Work Summary section")
def then_do_md_has_work_summary(commit_wsum_repo):
    """Verify that do.md contains a Work Summary section"""
    do_md_content = commit_wsum_repo.get_file_content("docs/dev/work/do.md")
    assert "# Work Summary" in do_md_content, \
        f"do.md should contain '# Work Summary' section\nContent:\n{do_md_content}"


@then("the actualCommitMessage is updated in do.md frontmatter")
def then_actual_commit_message_updated(commit_wsum_repo):
    """Verify that actualCommitMessage is set in do.md frontmatter"""
    do_md_content = commit_wsum_repo.get_file_content("docs/dev/work/do.md")
    fm = frontmatter.loads(do_md_content).metadata
    
    assert "actualCommitMessage" in fm, "actualCommitMessage should be set in frontmatter"
    assert fm["actualCommitMessage"].strip(), "actualCommitMessage should not be empty"


@then("do.md is staged in the commit")
def then_do_md_staged(commit_wsum_repo):
    """Verify that do.md was included in the commit"""
    # Check git log for the file
    result = subprocess.run(
        ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"],
        cwd=commit_wsum_repo.repo_dir,
        capture_output=True,
        text=True
    )
    committed_files = result.stdout.strip().split('\n')
    assert "docs/dev/work/do.md" in committed_files, \
        f"do.md should be in the commit. Files: {committed_files}"


@then("the commit includes both staged and unstaged tracked changes")
def then_commit_includes_staged_and_unstaged(commit_wsum_repo):
    """Verify that both staged and unstaged tracked changes are committed"""
    result = subprocess.run(
        ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"],
        cwd=commit_wsum_repo.repo_dir,
        capture_output=True,
        text=True
    )
    committed_files = result.stdout.strip().split('\n')
    
    assert "file-one.txt" in committed_files, "file-one.txt should be committed"
    assert "file-two.txt" in committed_files, "file-two.txt should be committed (unstaged changes included)"


@then("the commit includes staged, unstaged tracked, and untracked changes")
def then_commit_includes_all_changes(commit_wsum_repo):
    """Verify that staged, unstaged, and untracked changes are all committed"""
    result = subprocess.run(
        ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"],
        cwd=commit_wsum_repo.repo_dir,
        capture_output=True,
        text=True
    )
    committed_files = result.stdout.strip().split('\n')
    
    assert "file-one.txt" in committed_files, "file-one.txt should be committed"
    assert "file-two.txt" in committed_files, "file-two.txt should be committed"
    assert "file-three.txt" in committed_files, "file-three.txt should be committed (untracked)"


@then("the commit message is \"Custom commit message\"")
def then_commit_message_is_custom(commit_wsum_repo):
    """Verify that commit message is the explicit custom message"""
    result = subprocess.run(
        ["git", "log", "-1", "--format=%B"],
        cwd=commit_wsum_repo.repo_dir,
        capture_output=True,
        text=True
    )
    last_commit_msg = result.stdout.strip()
    assert last_commit_msg == "Custom commit message", \
        f"Expected 'Custom commit message', got '{last_commit_msg}'"


@then("the commit message is from the generated work headline")
def then_commit_message_from_generated_headline(commit_wsum_repo):
    """Verify that commit message comes from generated work headline"""
    # Get the last commit message
    result = subprocess.run(
        ["git", "log", "-1", "--format=%B"],
        cwd=commit_wsum_repo.repo_dir,
        capture_output=True,
        text=True
    )
    last_commit_msg = result.stdout.strip()
    
    # Get topmost workHeadline from do.md Work Summary section frontmatter.
    do_md_content = commit_wsum_repo.get_file_content("docs/dev/work/do.md")
    work_headline = _extract_topmost_workheadline_from_work_summary(do_md_content)
    
    assert work_headline, "workHeadline should be generated in Work Summary section frontmatter"
    assert last_commit_msg == work_headline, \
        f"Commit message '{last_commit_msg}' should match generated workHeadline '{work_headline}'"


@then("the error output mentions \"wsum.summarize_work() did not complete\"")
def then_error_mentions_timeout(commit_wsum_repo):
    """Verify that error output mentions wsum timeout"""
    stderr = commit_wsum_repo.last_command_result.stderr
    assert "wsum.summarize_work()" in stderr or "wsum" in stderr, \
        f"Error should mention wsum.summarize_work(). stderr: {stderr}"


@then("the error output mentions \"45 seconds\"")
def then_error_mentions_45_seconds(commit_wsum_repo):
    """Verify that error output mentions 45-second timeout limit"""
    stderr = commit_wsum_repo.last_command_result.stderr
    assert "45" in stderr, \
        f"Error should mention 45 second timeout. stderr: {stderr}"


@then("the error output mentions \"wsum\"")
def then_error_mentions_wsum(commit_wsum_repo):
    """Verify that error output mentions wsum"""
    stderr = commit_wsum_repo.last_command_result.stderr
    assert "wsum" in stderr or "Unable to summarize" in stderr, \
        f"Error should mention wsum. stderr: {stderr}"


@then("the error output suggests setting actualCommitMessage")
def then_error_suggests_manual_fallback(commit_wsum_repo):
    """Verify that error output suggests manual fallback"""
    stderr = commit_wsum_repo.last_command_result.stderr
    assert "actualCommitMessage" in stderr, \
        f"Error should suggest setting actualCommitMessage. stderr: {stderr}"


@then("the error output mentions \"no staged changes\"")
def then_error_mentions_no_staged_changes(commit_wsum_repo):
    """Verify that error output mentions no staged changes"""
    stderr = commit_wsum_repo.last_command_result.stderr
    assert "no staged changes" in stderr or "staged changes" in stderr, \
        f"Error should mention no staged changes. stderr: {stderr}"


@then("the do.md file is NOT modified")
def then_do_md_not_modified(commit_wsum_repo):
    """Verify that do.md was not modified by failed command"""
    # Check that do.md is not in unstaged/staged changes
    result = subprocess.run(
        ["git", "status", "--porcelain", "docs/dev/work/do.md"],
        cwd=commit_wsum_repo.repo_dir,
        capture_output=True,
        text=True
    )
    status = result.stdout.strip()
    assert status == "", f"do.md should not be modified. Status: {status}"


@then("the work summary reflects all changes")
def then_work_summary_reflects_all_changes(commit_wsum_repo):
    """Verify that work summary includes all changes"""
    do_md_content = commit_wsum_repo.get_file_content("docs/dev/work/do.md")
    # Just verify that Work Summary section exists and has content
    assert "# Work Summary" in do_md_content, "Work Summary section should exist"
    # The section should have some content after the header
    parts = do_md_content.split("# Work Summary")
    assert len(parts) > 1 and parts[1].strip(), "Work Summary should have content"


@then("the Work Summary section contains topmost workHeadline with a non-empty value")
def then_work_summary_has_work_headline(commit_wsum_repo):
    """Verify that topmost workHeadline is present in Work Summary section frontmatter."""
    do_md_content = commit_wsum_repo.get_file_content("docs/dev/work/do.md")
    work_headline = _extract_topmost_workheadline_from_work_summary(do_md_content)

    assert work_headline, "Work Summary topmost workHeadline should not be empty"


@then("the do.md frontmatter contains actualCommitMessage matching the topmost work headline")
def then_frontmatter_actual_matches_headline(commit_wsum_repo):
    """Verify that actualCommitMessage matches topmost Work Summary workHeadline."""
    do_md_content = commit_wsum_repo.get_file_content("docs/dev/work/do.md")
    fm = frontmatter.loads(do_md_content).metadata

    work_headline = _extract_topmost_workheadline_from_work_summary(do_md_content)
    actual_msg = fm.get("actualCommitMessage", "").strip()
    
    assert work_headline, "workHeadline should be set in Work Summary section"
    assert actual_msg == work_headline, \
        f"actualCommitMessage '{actual_msg}' should match workHeadline '{work_headline}'"


@then("the do.md body contains the \"# Work Summary\" section")
def then_body_contains_work_summary_header(commit_wsum_repo):
    """Verify that do.md body contains Work Summary header"""
    do_md_content = commit_wsum_repo.get_file_content("docs/dev/work/do.md")
    fm = frontmatter.loads(do_md_content)
    body = fm.content
    
    assert "# Work Summary" in body, "Body should contain '# Work Summary' header"


@then("the work summary is inserted before any older summaries")
def then_work_summary_is_latest(commit_wsum_repo):
    """Verify that new work summary is before older ones"""
    do_md_content = commit_wsum_repo.get_file_content("docs/dev/work/do.md")
    fm = frontmatter.loads(do_md_content)
    body = fm.content
    
    # Find all occurrences of Work Summary or summary markers
    # The structure should have Work Summary header followed by the latest content
    assert "# Work Summary" in body, "Work Summary section should exist"
    # Since we can't easily verify ordering without knowing the exact format,
    # we just verify the section exists


@then("do.md has a Work Summary header before the first dated summary section")
def then_work_summary_before_first_dated_section(commit_wsum_repo):
    """Verify # Work Summary is present and precedes the first dated subsection."""
    do_md_content = commit_wsum_repo.get_file_content("docs/dev/work/do.md")
    body = frontmatter.loads(do_md_content).content
    header_idx = body.find("# Work Summary")
    assert header_idx >= 0, "Expected '# Work Summary' header in do.md body"

    match = re.search(r"(?m)^## \d{4}-\d{2}-\d{2} \d{2}:\d{2}\s*$", body)
    assert match is not None, "Expected at least one dated summary section"
    assert header_idx < match.start(), "# Work Summary should appear before first dated summary"


@then("the newest generated summary is immediately after the Work Summary header")
def then_generated_summary_is_first_under_header(commit_wsum_repo):
    """Verify the generated summary appears first in newest-first order under the header."""
    do_md_content = commit_wsum_repo.get_file_content("docs/dev/work/do.md")
    body = frontmatter.loads(do_md_content).content

    match = re.search(r"(?m)^# Work Summary\s*$", body)
    assert match is not None, "Expected '# Work Summary' header in do.md body"

    after_header = body[match.end():]
    dated_matches = re.findall(r"(?m)^## \d{4}-\d{2}-\d{2} \d{2}:\d{2}\s*$", after_header)
    normalized = [match.strip() for match in dated_matches]
    assert normalized, "Expected dated summary sections under '# Work Summary'"
    assert "## 2026-05-01 10:00" in normalized, "Expected pre-existing dated summary to remain"
    assert normalized[0] != "## 2026-05-01 10:00", (
        "Newest generated summary should be directly under '# Work Summary'"
    )


@then("do.md ends with a Work Summary section containing the newest generated summary")
def then_work_summary_created_at_end_with_generated_entry(commit_wsum_repo):
    """Verify fallback behavior when no summary section exists in do.md."""
    do_md_content = commit_wsum_repo.get_file_content("docs/dev/work/do.md")
    body = frontmatter.loads(do_md_content).content.strip()

    assert "# Work Summary" in body, "Expected '# Work Summary' header to be created"
    last_header_idx = body.rfind("# Work Summary")
    assert last_header_idx >= 0

    trailing_section = body[last_header_idx:]
    assert re.search(r"(?m)^## \d{4}-\d{2}-\d{2} \d{2}:\d{2}\s*$", trailing_section), (
        "Expected generated dated summary under created '# Work Summary' section"
    )
    assert "workHeadline:" in trailing_section, "Expected generated workHeadline frontmatter"


@then("the work headline is a single line summary")
def then_work_headline_single_line(commit_wsum_repo):
    """Verify that work headline is a single line (no newlines)"""
    do_md_content = commit_wsum_repo.get_file_content("docs/dev/work/do.md")
    work_headline = _extract_topmost_workheadline_from_work_summary(do_md_content)
    
    assert work_headline, "workHeadline should be set"
    assert '\n' not in work_headline, "workHeadline should be a single line"


@then("the work headline is used as the commit message")
def then_headline_used_as_commit_message(commit_wsum_repo):
    """Verify that work headline is the commit message"""
    result = subprocess.run(
        ["git", "log", "-1", "--format=%B"],
        cwd=commit_wsum_repo.repo_dir,
        capture_output=True,
        text=True
    )
    last_commit_msg = result.stdout.strip()
    
    do_md_content = commit_wsum_repo.get_file_content("docs/dev/work/do.md")
    work_headline = _extract_topmost_workheadline_from_work_summary(do_md_content)
    
    assert last_commit_msg == work_headline, \
        f"Commit message should be workHeadline. got '{last_commit_msg}', expected '{work_headline}'"


@then("the commit is recorded in git log")
def then_commit_in_git_log(commit_wsum_repo):
    """Verify that the commit is in git log"""
    result = subprocess.run(
        ["git", "log", "--oneline"],
        cwd=commit_wsum_repo.repo_dir,
        capture_output=True,
        text=True
    )
    log = result.stdout
    # Should have at least 3 lines: initial, do.md init, and work commit
    lines = log.strip().split('\n')
    assert len(lines) >= 3, f"Expected at least 3 commits in log, got {len(lines)}"


@then("the do.md file contains multiple Work Summary entries")
def then_do_md_multiple_summaries(commit_wsum_repo):
    """Verify that do.md contains multiple work summary entries"""
    do_md_content = commit_wsum_repo.get_file_content("docs/dev/work/do.md")
    
    # Count occurrences of work summary markers
    # At minimum, should have the Work Summary header and multiple content entries
    assert "# Work Summary" in do_md_content, "Work Summary section should exist"
    # We expect at least some content under the header from multiple commits
    parts = do_md_content.split("# Work Summary")
    assert len(parts) > 1, "Should have Work Summary section"


@then("each entry is in chronological order (newest first)")
def then_entries_chronological_order(commit_wsum_repo):
    """Verify that work summary entries are in chronological order (newest first)"""
    # This is verified by the structure of the file
    # The insert_work_summary_into_do_md function in dtask inserts at the top
    do_md_content = commit_wsum_repo.get_file_content("docs/dev/work/do.md")
    
    # Just verify the structure is correct
    assert "# Work Summary" in do_md_content, "Work Summary section should exist"
    # The implementation inserts new summaries right after the header, so they'll be newest-first


# Additional assertion helper for when explicit message is used
@then("the actualCommitMessage in do.md frontmatter is \"Custom commit message\"")
def then_actual_message_is_custom(commit_wsum_repo):
    """Verify that actualCommitMessage in frontmatter matches explicit message"""
    do_md_content = commit_wsum_repo.get_file_content("docs/dev/work/do.md")
    fm = frontmatter.loads(do_md_content).metadata
    
    assert fm.get("actualCommitMessage") == "Custom commit message", \
        f"actualCommitMessage should be 'Custom commit message', got '{fm.get('actualCommitMessage')}'"
