"""Pytest-BDD scenario tests for the bltodo CLI command."""

from pytest_bdd import scenario


@scenario("bltodo/bltodo.feature", "command prints the TODO path and mdgbdf output")
def test_bltodo_prints_path_and_markdown(bltodo_cli):
    pass


@scenario("bltodo/bltodo.feature", "command uses BL_TODO_FILE content")
def test_bltodo_uses_env_file(bltodo_cli):
    pass


@scenario("bltodo/bltodo.feature", "command fails when TODO file does not exist")
def test_bltodo_missing_file_fails(bltodo_cli):
    pass
