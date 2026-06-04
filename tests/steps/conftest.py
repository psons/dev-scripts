"""Pytest configuration for step definitions

This conftest.py provides shared fixtures for all step definition modules.
"""

import subprocess
from pathlib import Path

import pytest


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
        return len(lines) == 0
