"""Pytest-BDD scenario tests for the wsum CLI command."""

from pytest_bdd import scenario


@scenario("wsum/wsum.feature", "default invocation summarizes staged changes only")
def test_wsum_default_staged_only(git_repo):
    pass


@scenario("wsum/wsum.feature", "--all includes staged, tracked unstaged, and untracked changes")
def test_wsum_all_includes_untracked(git_repo):
    pass


@scenario("wsum/wsum.feature", "--update includes tracked unstaged changes but excludes untracked files")
def test_wsum_update_excludes_untracked(git_repo):
    pass


@scenario("wsum/wsum.feature", "--base compares against a different ref")
def test_wsum_base_ref(git_repo):
    pass


@scenario("wsum/wsum.feature", "stdin diff input takes precedence over internal git diff")
def test_wsum_stdin_precedence(git_repo):
    pass


@scenario("wsum/wsum.feature", "command fails when there is no diff to summarize")
def test_wsum_empty_diff_fails(git_repo):
    pass


@scenario("wsum/wsum.feature", "command fails when an unsupported extra diff arg is provided")
def test_wsum_unsupported_extra_diff_arg(git_repo):
    pass


@scenario("wsum/wsum.feature", "markdown output is compatible with do.md work summary format")
def test_wsum_markdown_format(git_repo):
    pass
