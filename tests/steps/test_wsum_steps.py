"""Pytest-BDD step definitions for wsum CLI behavior (no dtask integration)."""

from __future__ import annotations

import os
import pty
import re
import stat
import subprocess
import sys
from pathlib import Path

import frontmatter
import yaml
from pytest_bdd import given, parsers, then, when

WSUM_SCRIPT = Path(__file__).resolve().parents[2] / "bin" / "wsum.py"


@given("a git repository with tracked files for wsum")
def given_repo_with_tracked_files(git_repo):
    for name in ["file-one.txt", "file-two.txt"]:
        (git_repo.repo_dir / name).write_text(f"initial-{name}\n")
    git_repo.run_git_command(["add", "file-one.txt", "file-two.txt"])
    git_repo.run_git_command(["commit", "-m", "Add tracked files for wsum tests"])


@given("a fake gemini cli is available for wsum tests")
def given_fake_gemini_cli(git_repo):
    fake_bin = git_repo.repo_dir / "fake-bin"
    fake_bin.mkdir(parents=True, exist_ok=True)
    gemini_script = fake_bin / "gemini"
    gemini_script.write_text(
        "#!/usr/bin/env python3\n"
        "import sys\n"
        "args = sys.argv[1:]\n"
        "prompt = ''\n"
        "if '-p' in args:\n"
        "    i = args.index('-p')\n"
        "    if i + 1 < len(args):\n"
        "        prompt = args[i + 1]\n"
        "if 'single-line, information-dense summary suitable as a git commit message' in prompt:\n"
        "    print('fake-headline-for-tests')\n"
        "else:\n"
        "    data = sys.stdin.read()\n"
        "    print('SUMMARY:' + data)\n"
    )
    gemini_script.chmod(gemini_script.stat().st_mode | stat.S_IEXEC)

    env = os.environ.copy()
    env["PATH"] = f"{fake_bin}:{env.get('PATH', '')}"
    git_repo.wsum_env = env


@given(parsers.parse('the tracked file "{filename}" has staged changes with content "{content}"'))
def given_staged_change(git_repo, filename, content):
    path = git_repo.repo_dir / filename
    path.write_text(f"{content}\n")
    git_repo.run_git_command(["add", filename])


@given(parsers.parse('the tracked file "{filename}" has unstaged changes with content "{content}"'))
def given_unstaged_change(git_repo, filename, content):
    path = git_repo.repo_dir / filename
    path.write_text(f"{content}\n")


@given(parsers.parse('the untracked file "{filename}" exists with content "{content}"'))
def given_untracked_file(git_repo, filename, content):
    path = git_repo.repo_dir / filename
    path.write_text(f"{content}\n")


@given(parsers.parse('I have committed a tracked file change "{filename}" with content "{content}"'))
def given_committed_change(git_repo, filename, content):
    path = git_repo.repo_dir / filename
    path.write_text(f"{content}\n")
    git_repo.run_git_command(["add", filename])
    git_repo.run_git_command(["commit", "-m", "Commit tracked change for base ref scenario"])


@given("there are no staged or unstaged changes")
def given_clean_working_tree(git_repo):
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=git_repo.repo_dir,
        capture_output=True,
        text=True,
        check=True,
    )
    lines = [line for line in result.stdout.splitlines() if "fake-bin/" not in line]
    assert not lines, f"Expected clean tree (excluding fake-bin), got:\n{result.stdout}"


@when(parsers.parse('I run wsum command "{command}"'))
def when_run_wsum(git_repo, command):
    args = command.split()
    assert args[0] == "wsum", f"Expected command to start with wsum, got: {command}"
    master_fd, slave_fd = pty.openpty()
    try:
        proc = subprocess.Popen(
            [sys.executable, str(WSUM_SCRIPT), *args[1:]],
            cwd=git_repo.repo_dir,
            stdin=slave_fd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=git_repo.wsum_env,
        )
        stdout, stderr = proc.communicate()
    finally:
        os.close(master_fd)
        os.close(slave_fd)

    git_repo.last_wsum_result = subprocess.CompletedProcess(
        [sys.executable, str(WSUM_SCRIPT), *args[1:]],
        proc.returncode,
        stdout,
        stderr,
    )


@when(parsers.parse('I run wsum command "{command}" with stdin diff:'))
def when_run_wsum_with_stdin(git_repo, command, docstring):
    args = command.split()
    assert args[0] == "wsum", f"Expected command to start with wsum, got: {command}"
    git_repo.last_wsum_result = subprocess.run(
        [sys.executable, str(WSUM_SCRIPT), *args[1:]],
        cwd=git_repo.repo_dir,
        capture_output=True,
        text=True,
        input=docstring,
        env=git_repo.wsum_env,
    )


@then("the wsum command succeeds")
def then_wsum_command_succeeds(git_repo):
    result = git_repo.last_wsum_result
    assert result.returncode == 0, (
        f"Expected success, got exit code {result.returncode}\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )


@then("the wsum command fails with a non-zero exit code")
def then_wsum_command_fails(git_repo):
    result = git_repo.last_wsum_result
    assert result.returncode != 0, (
        f"Expected failure, got exit code {result.returncode}\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )


@then(parsers.parse('the wsum error output mentions "{text}"'))
def then_wsum_error_mentions(git_repo, text):
    result = git_repo.last_wsum_result
    combined = f"{result.stdout}\n{result.stderr}"
    assert text in combined, (
        f"Expected '{text}' in output.\n"
        f"stdout:\n{result.stdout}\n"
        f"stderr:\n{result.stderr}"
    )


@then(parsers.parse('the markdown output contains "{text}"'))
def then_output_contains(git_repo, text):
    result = git_repo.last_wsum_result
    assert text in result.stdout, f"Expected '{text}' in stdout:\n{result.stdout}"


@then(parsers.parse('the markdown output does not contain "{text}"'))
def then_output_not_contains(git_repo, text):
    result = git_repo.last_wsum_result
    assert text not in result.stdout, f"Did not expect '{text}' in stdout:\n{result.stdout}"


@then("the markdown output starts with a timestamp heading")
def then_output_has_timestamp_heading(git_repo):
    result = git_repo.last_wsum_result
    assert re.search(r"^## \d{4}-\d{2}-\d{2} \d{2}:\d{2}", result.stdout, re.MULTILINE), (
        f"Expected timestamp heading in output:\n{result.stdout}"
    )


@then("the markdown output includes workHeadline frontmatter")
def then_output_has_workheadline_frontmatter(git_repo):
    result = git_repo.last_wsum_result
    match = re.search(r"\n---\n(.*?)\n---\n", result.stdout, re.DOTALL)
    assert match, f"Expected YAML frontmatter block in output:\n{result.stdout}"
    metadata = yaml.safe_load(match.group(1)) or {}
    assert "workHeadline" in metadata, (
        f"Expected workHeadline frontmatter in output:\n{result.stdout}"
    )
