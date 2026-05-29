"""
Pytest-BDD step definitions for dtask init --workbranch scenarios

This module implements the step definitions for testing the dtask init command
with the --workbranch flag in a sandboxed git repository environment.
"""

import subprocess
from pathlib import Path
from typing import Optional

import pytest
import yaml
from pytest_bdd import given, when, then, parsers


class GitRepoTestFixture:
    """Manages a sandboxed git repository for testing"""
    
    def __init__(self, temp_dir: Path):
        self.repo_dir = temp_dir
        self._initialize_repo()
    
    def _initialize_repo(self):
        """Initialize a clean git repository with initial commit"""
        self.run_git_command(["init"])
        self.run_git_command(["config", "user.email", "test@example.com"])
        self.run_git_command(["config", "user.name", "Test User"])
        
        # Create initial commit
        (self.repo_dir / "README.md").write_text("# Test Repo\n")
        self.run_git_command(["add", "README.md"])
        self.run_git_command(["commit", "-m", "Initial commit"])
    
    def run_git_command(self, args: list[str]) -> subprocess.CompletedProcess:
        """Run a git command in the test repo"""
        result = subprocess.run(
            ["git"] + args,
            cwd=self.repo_dir,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"Git command failed: {' '.join(args)}\n"
                f"stdout: {result.stdout}\n"
                f"stderr: {result.stderr}"
            )
        return result
    
    def run_dtask_command(self, args: list[str]) -> subprocess.CompletedProcess:
        """Run a dtask command in the test repo"""
        result = subprocess.run(
            ["dtask"] + args,
            cwd=self.repo_dir,
            capture_output=True,
            text=True
        )
        return result
    
    def get_current_branch(self) -> str:
        """Get the currently checked out branch"""
        result = self.run_git_command(["rev-parse", "--abbrev-ref", "HEAD"])
        return result.stdout.strip()
    
    def get_file_content(self, path: str) -> str:
        """Get the content of a file in the repo"""
        file_path = self.repo_dir / path
        if file_path.exists():
            return file_path.read_text()
        return ""
    
    def file_exists(self, path: str) -> bool:
        """Check if a file exists in the repo"""
        return (self.repo_dir / path).exists()
    
    def is_file_staged(self, path: str) -> bool:
        """Check if a file is staged in git"""
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            cwd=self.repo_dir,
            capture_output=True,
            text=True
        )
        return path in result.stdout
    
    def is_working_tree_clean(self) -> bool:
        """Check if the working tree is clean (ignoring do.md)"""
        result = subprocess.run(
            ["git", "status", "--porcelain", "-uall"],
            cwd=self.repo_dir,
            capture_output=True,
            text=True
        )
        # Filter out do.md since dtask init intentionally creates it
        lines = [line for line in result.stdout.splitlines() if line and "docs/dev/work/do.md" not in line]
        print(f"git status: -->> \n {result.stdout}")
        return len(lines) == 0
    
@pytest.fixture
def git_repo(tmp_path):
    """Fixture providing a clean, sandboxed git repository.

    Uses pytest's tmp_path which retains temp directories from the last 3 runs.
    Configure retention with: pytest --basetemp=<dir> or in pytest.ini via tmp_path_retention_count.
    """
    repo = GitRepoTestFixture(tmp_path)
    yield repo


# Step definitions

@given("a clean git repository with initial commit")
def given_clean_git_repo(git_repo):
    """Ensure repository is initialized with an initial commit"""
    assert git_repo.file_exists("README.md")
    assert git_repo.get_current_branch() == "master" or git_repo.get_current_branch() == "main"


@given("a clean working tree")
def given_clean_working_tree(git_repo):
    """Verify that the working tree is clean"""
    assert git_repo.is_working_tree_clean()


@given("I have made 2 commits")
def given_multiple_commits(git_repo):
    """Create 2 additional commits beyond the initial one"""
    (git_repo.repo_dir / "file1.txt").write_text("Content 1\n")
    git_repo.run_git_command(["add", "file1.txt"])
    git_repo.run_git_command(["commit", "-m", "Add file1"])
    
    (git_repo.repo_dir / "file2.txt").write_text("Content 2\n")
    git_repo.run_git_command(["add", "file2.txt"])
    git_repo.run_git_command(["commit", "-m", "Add file2"])


@when(parsers.parse('I run "dtask init --workbranch {branch_name}"'))
def when_run_dtask_init_workbranch(git_repo, branch_name):
    """Execute dtask init with the --workbranch flag"""
    result = git_repo.run_dtask_command(["init", "--workbranch", branch_name])
    git_repo.last_command_result = result
    
    # Store branch name for later assertions
    git_repo.test_branch_name = branch_name


@then(parsers.parse('a new branch "{branch_name}" is created'))
def then_branch_created(git_repo, branch_name):
    """Verify that the specified branch exists"""
    result = subprocess.run(
        ["git", "rev-parse", "--verify", branch_name],
        cwd=git_repo.repo_dir,
        capture_output=True
    )
    assert result.returncode == 0, f"Branch '{branch_name}' was not created"


@then(parsers.parse('the branch "{branch_name}" is checked out'))
def then_branch_checked_out(git_repo, branch_name):
    """Verify that the specified branch is currently checked out"""
    current_branch = git_repo.get_current_branch()
    assert current_branch == branch_name, f"Expected branch '{branch_name}', got '{current_branch}'"


@then('a "docs/dev/work/do.md" file is created')
def then_do_file_created(git_repo):
    """Verify that do.md exists"""
    assert git_repo.file_exists("docs/dev/work/do.md"), "do.md file was not created"


@then(parsers.parse('the do.md file contains frontmatter with "{key}": "{value}"'))
def then_do_file_contains_frontmatter(git_repo, key, value):
    """Verify that do.md contains a specific frontmatter key-value pair"""
    content = git_repo.get_file_content("docs/dev/work/do.md")
    
    fm = {}
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm = yaml.safe_load(parts[1]) or {}
            
    assert key in fm, f"Frontmatter missing key '{key}'\nContent:\n{content}"
    assert str(fm[key]) == value, f"Frontmatter key '{key}' has value '{fm[key]}', expected '{value}'"


@then('the do.md file is not staged')
def then_do_file_not_staged(git_repo):
    """Verify that do.md is not in the staging area"""
    assert not git_repo.is_file_staged("docs/dev/work/do.md"), "do.md should not be staged"


@then("the do.md file contains:")
def then_do_file_contains_table(git_repo, datatable):
    """Verify that do.md contains expected frontmatter entries from table"""
    content = git_repo.get_file_content("docs/dev/work/do.md")
    
    fm = {}
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm = yaml.safe_load(parts[1]) or {}
            
    # datatable is a nested list, with the first row being the header
    for row in datatable[1:]:
        key = row[0]
        value = row[1]
        
        assert key in fm, f"Frontmatter missing key '{key}'\nContent:\n{content}"
        assert str(fm[key]) == value, f"Frontmatter key '{key}' has value '{fm[key]}', expected '{value}'"


@then(parsers.parse('the branch "{branch_name}" points to the same commit as "HEAD@{-1}"'))
def then_branch_at_same_commit(git_repo, branch_name):
    """Verify that the new branch points to the previous HEAD"""
    result_branch = subprocess.run(
        ["git", "rev-parse", branch_name],
        cwd=git_repo.repo_dir,
        capture_output=True,
        text=True
    )
    
    result_head = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=git_repo.repo_dir,
        capture_output=True,
        text=True
    )
    
    branch_commit = result_branch.stdout.strip()
    head_commit = result_head.stdout.strip()
    
    assert branch_commit == head_commit, \
        f"Branch '{branch_name}' points to {branch_commit}, expected {head_commit}"


@then("the working tree remains clean")
def then_working_tree_clean(git_repo):
    """Verify that the working tree is still clean"""
    assert git_repo.is_working_tree_clean(), "Working tree should be clean"
