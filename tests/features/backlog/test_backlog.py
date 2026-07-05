"""Pytest-BDD scenario tests for the backlog CLI command."""

from pytest_bdd import scenario


@scenario("backlog/backlog.feature", "prioritized uses the default provider and emits mdgbdf by default")
def test_backlog_prioritized_default_mdgbdf(backlog_cli):
    pass


@scenario("backlog/backlog.feature", "prioritized supports json output")
def test_backlog_prioritized_json(backlog_cli):
    pass


@scenario("backlog/backlog.feature", "poptask returns the highest-priority task")
def test_backlog_poptask(backlog_cli):
    pass


@scenario("backlog/backlog.feature", "help prints command usage summary")
def test_backlog_help(backlog_cli):
    pass
