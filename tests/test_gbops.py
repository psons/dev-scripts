"""Unit tests for bin/gbops.py pure operations over gbdata types."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

_bin_dir = Path(__file__).resolve().parents[1] / "bin"
if str(_bin_dir) not in sys.path:
    sys.path.insert(0, str(_bin_dir))

_gb_spec = importlib.util.spec_from_file_location("gbdata", _bin_dir / "gbdata.py")
gbdata = importlib.util.module_from_spec(_gb_spec)
sys.modules["gbdata"] = gbdata
_gb_spec.loader.exec_module(gbdata)

_gbops_spec = importlib.util.spec_from_file_location("gbops", _bin_dir / "gbops.py")
gbops = importlib.util.module_from_spec(_gbops_spec)
sys.modules["gbops"] = gbops
_gbops_spec.loader.exec_module(gbops)

Task = gbdata.Task
Story = gbdata.Story
TaskStatus = gbdata.TaskStatus
StoryStatus = gbdata.StoryStatus


def _task(id_, status=TaskStatus.DO, name="task", attributes=None):
    return Task(id=id_, status=status, name=name, attributes=attributes)


def _story(id_="s1", name="Story", status=StoryStatus.DO, tasks=None, attributes=None):
    return Story(id=id_, name=name, status=status, tasks=tasks, attributes=attributes)


def test_tag_tasks_with_story_sets_attributes():
    story = _story(id_="s1", name="My Story", tasks=[_task("t1")])
    tagged = gbops.tag_tasks_with_story(story)
    assert tagged[0].attributes == {"storyID": "s1", "storyName": "My Story"}


def test_tag_task_with_story_does_not_overwrite_existing():
    task = _task("t1", attributes={"storyID": "keep-me"})
    story = _story(id_="s1", name="My Story")
    tagged = gbops.tag_task_with_story(task, story)
    assert tagged.attributes["storyID"] == "keep-me"
    assert tagged.attributes["storyName"] == "My Story"


def test_story_ref_reads_attributes():
    task = _task("t1", attributes={"storyID": "s1", "storyName": "My Story"})
    assert gbops.story_ref(task) == ("s1", "My Story")


def test_story_ref_returns_none_when_absent():
    assert gbops.story_ref(_task("t1")) == (None, None)


def test_regroup_tasks_by_story_groups_by_story_id():
    t1 = _task("t1", attributes={"storyID": "s1", "storyName": "Story A"})
    t2 = _task("t2", attributes={"storyID": "s1", "storyName": "Story A"})
    t3 = _task("t3", attributes={"storyID": "s2", "storyName": "Story B"})
    anon = _task("t4")

    stories = gbops.regroup_tasks_by_story([t1, t2, t3, anon])

    assert [s.id for s in stories] == ["s1", "s2", gbops.ANONYMOUS_STORY_ID]
    assert [t.id for t in stories[0].tasks] == ["t1", "t2"]
    assert stories[1].name == "Story B"
    assert stories[2].tasks[0].id == "t4"


def test_upsert_tasks_replaces_matching_and_appends_new_without_deleting():
    existing = [_task("t1", status=TaskStatus.DO), _task("t2", status=TaskStatus.DO)]
    incoming = [_task("t1", status=TaskStatus.COMPLETED), _task("t3", status=TaskStatus.DO)]

    merged = gbops.upsert_tasks(existing, incoming)

    assert [t.id for t in merged] == ["t1", "t2", "t3"]
    assert merged[0].status == TaskStatus.COMPLETED
    assert merged[1].status == TaskStatus.DO


def test_upsert_story_merges_fields_and_tasks():
    existing = _story(id_="s1", name="Old Name", tasks=[_task("t1", status=TaskStatus.DO)])
    incoming = _story(id_="s1", name="New Name", tasks=[_task("t1", status=TaskStatus.COMPLETED)])

    merged = gbops.upsert_story(existing, incoming)

    assert merged.name == "New Name"
    assert merged.tasks[0].status == TaskStatus.COMPLETED


def test_find_story_matches_by_id():
    stories = [_story(id_="s1", name="A"), _story(id_="s2", name="B")]
    found = gbops.find_story(stories, _story(id_="s2", name="Different Name"))
    assert found.id == "s2"


def test_find_story_falls_back_to_name_when_id_missing():
    stories = [_story(id_="s1", name="Match Me")]
    found = gbops.find_story(stories, _story(id_="", name="match me"))
    assert found.id == "s1"


def test_find_story_returns_none_when_no_match():
    stories = [_story(id_="s1", name="A")]
    assert gbops.find_story(stories, _story(id_="zzz", name="Nope")) is None


def test_lift_story_to_top_places_story_first():
    stories = [_story(id_="s1"), _story(id_="s2")]
    lifted = gbops.lift_story_to_top(stories, _story(id_="s3"))
    assert [s.id for s in lifted] == ["s3", "s1", "s2"]


def test_incomplete_and_finished_task_classification():
    incomplete = _task("t1", status=TaskStatus.IN_PROGRESS)
    done = _task("t2", status=TaskStatus.COMPLETED)
    story = _story(tasks=[incomplete, done])

    assert gbops.incomplete_tasks(story) == [incomplete]
    assert gbops.finished_tasks(story) == [done]


def test_unfinished_task_is_harvestable_but_not_incomplete():
    unfinished = _task("t1", status=TaskStatus.UNFINISHED)
    story = _story(tasks=[unfinished])

    assert gbops.incomplete_tasks(story) == []
    assert gbops.finished_tasks(story) == [unfinished]


def test_stories_with_incomplete_tasks_filters():
    with_incomplete = _story(id_="s1", tasks=[_task("t1", status=TaskStatus.DO)])
    all_done = _story(id_="s2", tasks=[_task("t2", status=TaskStatus.COMPLETED)])

    result = gbops.stories_with_incomplete_tasks([with_incomplete, all_done])

    assert [s.id for s in result] == ["s1"]
