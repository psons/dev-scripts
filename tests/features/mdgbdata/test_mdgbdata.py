"""Pytest-BDD scenario tests for the mdgbdata CLI command."""

from pytest_bdd import scenario


@scenario("mdgbdata/mdgbdata.feature", "tojson converts markdown and warns about ignored prose")
def test_mdgbdata_tojson_warns_on_ignored_text(mdgbdata_cli):
    pass


@scenario("mdgbdata/mdgbdata.feature", "tojson fails when no markdown headers or tasks are present")
def test_mdgbdata_tojson_requires_structure(mdgbdata_cli):
    pass


@scenario("mdgbdata/mdgbdata.feature", "tomd converts JSON into markdown")
def test_mdgbdata_tomd_converts_json(mdgbdata_cli):
    pass


@scenario("mdgbdata/mdgbdata.feature", "tomd fails on invalid JSON")
def test_mdgbdata_tomd_rejects_invalid_json(mdgbdata_cli):
    pass


@scenario("mdgbdata/mdgbdata.feature", "help prints command usage summary")
def test_mdgbdata_help_shows_usage(mdgbdata_cli):
    pass