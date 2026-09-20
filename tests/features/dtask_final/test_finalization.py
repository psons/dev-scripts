"""BDD scenarios for dtask commit --final do.md/backlog finalization."""

import subprocess

from pytest_bdd import scenario

from tests.steps.test_dtask_final_steps import DO_MD_RELATIVE, _backlog_stories, _do_md_path


def _commit_messages(git_repo, count: int) -> list[str]:
    result = subprocess.run(
        ["git", "log", "--format=%s", "-n", str(count)],
        cwd=git_repo.repo_dir,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.splitlines()


def _do_md_at_ref(git_repo, ref: str) -> str:
    result = subprocess.run(
        ["git", "show", f"{ref}:{DO_MD_RELATIVE}"],
        cwd=git_repo.repo_dir,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout


@scenario(
    "dtask_final/finalization.feature",
    "--final pushes unfinished work and commits completed work before removing do.md",
)
def test_finalization_persists_backlog_and_completed_work(git_repo):
    # Spec: backlog.py PushStory is implemented by bltodo.py as lift-to-top + task-wise upsert.
    stories = _backlog_stories(git_repo)
    assert stories[0].id == "story-active"
    assert stories[0].name == "Active Story"
    assert [task.id for task in stories[0].tasks or []] == ["task-existing", "task-active", "task-completed", "task-unfinished"]

    # Spec: completed/abandoned/unfinished tasks are recorded in '# Completed work' as a bare
    # list, tagged with attributes.storyID/attributes.storyName, in the do.md committed *before*
    # do.md is removed (HEAD~1), not merely in memory.
    committed_do_md = _do_md_at_ref(git_repo, "HEAD~1")
    assert "# Completed work" in committed_do_md
    for task_name in ("completed task", "unfinished task"):
        assert task_name in committed_do_md
    assert "storyID: story-active" in committed_do_md
    assert "storyName: Active Story" in committed_do_md

    # Spec: do.md is removed only in a second, separate commit after the finalized state
    # (with the pushed story already dropped from '# Current work') was committed.
    assert _commit_messages(git_repo, 2) == [
        "removed do.md for finalized tasks",
        "finalize current work",
    ]
    assert not _do_md_path(git_repo).exists()


@scenario(
    "dtask_final/finalization.feature",
    "--final pushes an unfinished current-work story into TODO.md",
)
def test_finalization_pushes_unfinished_story_to_todo(git_repo):
    # Spec: dtask commit --final finds incomplete work in '# Current work' and pushes the whole
    # story (not just the task) back into the backlog kept in TODO.md by the bltodo plugin.
    stories = _backlog_stories(git_repo)
    assert stories, "Expected the unfinished story to be pushed into TODO.md"
    top_story = stories[0]
    assert top_story.id == "story-active"
    assert top_story.name == "Active Story"
    assert "active task" in [task.name for task in top_story.tasks or []]


@scenario(
    "dtask_final/finalization.feature",
    "--final keeps do.md when pushing unfinished work fails",
)
def test_finalization_push_failure_preserves_do_md(git_repo):
    # Spec: push failures are fatal and do.md must not be modified or removed if a push fails.
    assert git_repo.last_finalization_result.returncode != 0
    assert _do_md_path(git_repo).exists()
    assert _do_md_path(git_repo).read_text(encoding="utf-8") == git_repo.finalization_do_md_before
    assert _commit_messages(git_repo, 1) != ["removed do.md for finalized tasks"]

