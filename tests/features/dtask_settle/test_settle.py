"""BDD scenarios for dtask settle."""

from pytest_bdd import scenario


@scenario(
    "dtask_settle/settle.feature",
    "settle records completed work and pushes unfinished work",
)
def test_settle_records_completed_and_pushes_unfinished():
    pass


@scenario(
    "dtask_settle/settle.feature",
    "settle preserves do.md when the backlog provider fails",
)
def test_settle_preserves_do_md_on_backlog_failure():
    pass