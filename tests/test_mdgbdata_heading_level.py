"""Unit tests for mdgbdata story_heading_level parsing/serialization support."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import pytest

_bin_dir = Path(__file__).resolve().parents[1] / "bin"
if str(_bin_dir) not in sys.path:
    sys.path.insert(0, str(_bin_dir))

_gb_spec = importlib.util.spec_from_file_location("gbdata", _bin_dir / "gbdata.py")
gbdata = importlib.util.module_from_spec(_gb_spec)
sys.modules["gbdata"] = gbdata
_gb_spec.loader.exec_module(gbdata)

_mdgb_spec = importlib.util.spec_from_file_location("mdgbdata", _bin_dir / "mdgbdata.py")
mdgbdata = importlib.util.module_from_spec(_mdgb_spec)
sys.modules["mdgbdata"] = mdgbdata
_mdgb_spec.loader.exec_module(mdgbdata)

StoryStatus = gbdata.StoryStatus
TaskStatus = gbdata.TaskStatus


def _status_maps():
    repo_root = Path(__file__).resolve().parents[1]
    story = mdgbdata.load_status_map(repo_root / "docs/dev/spec/story_status_metadata.json", StoryStatus)
    task = mdgbdata.load_status_map(repo_root / "docs/dev/spec/task_status_metadata.json", TaskStatus)
    return story, task


def test_parse_at_h2_recognizes_stories_at_that_level():
    story_map, task_map = _status_maps()
    text = "## Story One\nd - task one\n\n## Story Two\nx - task two\n"

    stories = mdgbdata.parse_stories_from_markdown(text, story_map, task_map, story_heading_level=2)

    assert [s.name for s in stories] == ["Story One", "Story Two"]
    assert stories[0].tasks[0].name == "task one"


def test_deeper_heading_becomes_description_content():
    story_map, task_map = _status_maps()
    text = "## Story One\nSome intro\n### Sub heading\nmore text\nd - a task\n"

    stories = mdgbdata.parse_stories_from_markdown(text, story_map, task_map, story_heading_level=2)

    assert len(stories) == 1
    assert "### Sub heading" in stories[0].description
    assert stories[0].tasks[0].name == "a task"


def test_shallower_heading_raises_heading_level_error():
    story_map, task_map = _status_maps()
    text = "# Story One\nd - a task\n"

    with pytest.raises(mdgbdata.MdgbdataHeadingLevelError):
        mdgbdata.parse_stories_from_markdown(text, story_map, task_map, story_heading_level=2)


@pytest.mark.parametrize("bad_level", [0, 7, -1])
def test_invalid_story_heading_level_raises_on_parse(bad_level):
    story_map, task_map = _status_maps()
    with pytest.raises(mdgbdata.MdgbdataHeadingLevelError):
        mdgbdata.parse_stories_from_markdown("text", story_map, task_map, story_heading_level=bad_level)


@pytest.mark.parametrize("bad_level", [0, 7, -1])
def test_invalid_story_heading_level_raises_on_serialize(bad_level):
    story_map, task_map = _status_maps()
    story = gbdata.Story(id="s1", name="Story One", status=StoryStatus.DO, tasks=None)
    with pytest.raises(mdgbdata.MdgbdataHeadingLevelError):
        mdgbdata.stories_to_markdown_text([story], story_map, task_map, story_heading_level=bad_level)


def test_round_trip_at_h2():
    story_map, task_map = _status_maps()
    text = "## d - Story: Story One\nd - a task\n\n## Story Two\nx - done task\n"

    stories = mdgbdata.parse_stories_from_markdown(text, story_map, task_map, story_heading_level=2)
    rendered = mdgbdata.stories_to_markdown_text(stories, story_map, task_map, story_heading_level=2)
    reparsed = mdgbdata.parse_stories_from_markdown(rendered, story_map, task_map, story_heading_level=2)

    assert [s.name for s in reparsed] == [s.name for s in stories]
    assert reparsed[0].tasks[0].name == stories[0].tasks[0].name


def test_default_story_heading_level_is_h1_unchanged():
    story_map, task_map = _status_maps()
    text = "# Story One\nd - a task\n"

    stories = mdgbdata.parse_stories_from_markdown(text, story_map, task_map)
    rendered = mdgbdata.stories_to_markdown_text(stories, story_map, task_map)

    assert rendered.startswith("# ")
