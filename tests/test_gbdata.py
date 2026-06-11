"""Unit tests for gbdata model and markdown parsing behavior."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import re
import sys

import pytest

# Add bin directory to sys.path so we can import gbdata.py
_bin_dir = Path(__file__).resolve().parents[1] / "bin"
if str(_bin_dir) not in sys.path:
    sys.path.insert(0, str(_bin_dir))

_spec = importlib.util.spec_from_file_location("gbdata", _bin_dir / "gbdata.py")
if _spec is None or _spec.loader is None:
    raise RuntimeError("Unable to load gbdata module for tests")
gbdata = importlib.util.module_from_spec(_spec)
sys.modules["gbdata"] = gbdata
_spec.loader.exec_module(gbdata)

TaskStatus = gbdata.TaskStatus
Task = gbdata.Task
compile_status_patterns = gbdata.compile_status_patterns
detect_status = gbdata.detect_status
load_status_map = gbdata.load_status_map
parse_stories_from_markdown = gbdata.parse_stories_from_markdown
parse_stories_from_markdown_file = gbdata.parse_stories_from_markdown_file
strip_status_prefix = gbdata.strip_status_prefix


def _status_maps() -> tuple[dict[TaskStatus, object], dict[TaskStatus, object]]:
    repo_root = Path(__file__).resolve().parents[1]
    story = load_status_map(repo_root / "docs/dev/spec/story_status_metadata.json")
    task = load_status_map(repo_root / "docs/dev/spec/task_status_metadata.json")
    return story, task


def test_load_status_map_valid_json_loads_expected_keys():
    story_map, _ = _status_maps()

    assert set(story_map.keys()) == set(TaskStatus)


def test_load_status_map_invalid_key_raises_value_error(tmp_path: Path):
    bad = tmp_path / "bad.json"
    bad.write_text('{"not_a_status": {"val": "n", "pat_str": "^n *-"}}', encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid status key"):
        load_status_map(bad)


def test_load_status_map_invalid_entry_shape_raises_value_error(tmp_path: Path):
    bad = tmp_path / "bad.json"
    bad.write_text('{"do": {"val": "d"}}', encoding="utf-8")

    with pytest.raises(ValueError, match="missing field 'pat_str'"):
        load_status_map(bad)


def test_detect_status_matches_patterns_and_unknown_returns_none():
    _, task_map = _status_maps()
    compiled = compile_status_patterns(task_map)

    assert detect_status("x - done", compiled) == TaskStatus.COMPLETED
    assert detect_status("/ - in progress", compiled) == TaskStatus.IN_PROGRESS
    assert detect_status("unknown content", compiled) is None


def test_strip_status_prefix_removes_only_leading_marker():
    _, task_map = _status_maps()
    compiled = compile_status_patterns(task_map)

    assert strip_status_prefix("x - build parser", TaskStatus.COMPLETED, compiled) == "build parser"


def test_status_matched_heading_creates_story_and_persists_status():
    story_map, task_map = _status_maps()
    text = "# d - Build parser\nx - write tests\n"

    stories = parse_stories_from_markdown(text, story_map, task_map)

    assert len(stories) == 1
    assert stories[0].name == "Build parser"
    assert stories[0].status == TaskStatus.DO
    assert stories[0].tasks is not None
    assert stories[0].tasks[0].status == TaskStatus.COMPLETED


def test_non_pattern_heading_with_tasks_still_creates_story_default_do():
    story_map, task_map = _status_maps()
    text = "# Planning\nx - decide approach\n"

    stories = parse_stories_from_markdown(text, story_map, task_map)

    assert len(stories) == 1
    assert stories[0].name == "Planning"
    assert stories[0].status == TaskStatus.DO


def test_story_prefix_heading_creates_story_without_tasks():
    story_map, task_map = _status_maps()
    text = "## Story: Parser Boundary Behavior\nNo tasks yet.\n"

    stories = parse_stories_from_markdown(text, story_map, task_map)

    assert len(stories) == 1
    assert stories[0].name == "Parser Boundary Behavior"
    assert stories[0].status == TaskStatus.DO
    assert stories[0].tasks is None


def test_nested_heading_does_not_create_nested_story():
    story_map, task_map = _status_maps()
    text = "# d - Parent\n## d - Nested heading is description context\nx - real task\n"

    stories = parse_stories_from_markdown(text, story_map, task_map)

    assert len(stories) == 1
    assert stories[0].name == "Parent"
    assert stories[0].tasks is not None
    assert len(stories[0].tasks) == 1


@pytest.mark.parametrize("level", [1, 2, 3, 4, 5, 6])
def test_heading_levels_1_through_6_supported(level: int):
    story_map, task_map = _status_maps()
    heading = "#" * level
    text = f"{heading} d - Story L{level}\nx - task\n"

    stories = parse_stories_from_markdown(text, story_map, task_map)

    assert len(stories) == 1
    assert stories[0].name == f"Story L{level}"


def test_left_margin_task_is_recognized_and_indented_is_not():
    story_map, task_map = _status_maps()
    text = "# d - Story\n  x - indented not task\nx - real task\n"

    stories = parse_stories_from_markdown(text, story_map, task_map)

    assert len(stories) == 1
    assert stories[0].tasks is not None
    assert len(stories[0].tasks) == 1
    assert stories[0].tasks[0].name == "real task"


def test_task_detail_accumulates_until_boundary():
    story_map, task_map = _status_maps()
    text = "# d - Story\nx - first\n\nline one\nline two\nx - second\n"

    stories = parse_stories_from_markdown(text, story_map, task_map)

    first = stories[0].tasks[0]
    assert first.detail == "line one\nline two"


def test_empty_task_name_defaults_to_unnamed_task():
    story_map, task_map = _status_maps()
    text = "# d - Story\nx -   \n"

    stories = parse_stories_from_markdown(text, story_map, task_map)

    assert stories[0].tasks is not None
    assert stories[0].tasks[0].name == "(unnamed task)"


def test_same_or_higher_level_heading_closes_current_story():
    story_map, task_map = _status_maps()
    text = "## d - One\nx - t1\n# d - Two\nx - t2\n"

    stories = parse_stories_from_markdown(text, story_map, task_map)

    assert len(stories) == 2
    assert stories[0].name == "One"
    assert stories[1].name == "Two"


def test_deeper_heading_does_not_close_current_story():
    story_map, task_map = _status_maps()
    text = "# d - One\nx - t1\n## details\nstill details\nx - t2\n"

    stories = parse_stories_from_markdown(text, story_map, task_map)

    assert len(stories) == 1
    assert stories[0].tasks is not None
    assert len(stories[0].tasks) == 2


def test_bare_tasks_before_first_heading_go_to_unscoped_story():
    story_map, task_map = _status_maps()
    text = "x - boot\nd - plan\n# d - Real Story\nx - do real\n"

    stories = parse_stories_from_markdown(text, story_map, task_map)

    assert len(stories) == 2
    assert stories[0].name == "Unscoped"
    assert stories[0].status == TaskStatus.DO
    assert stories[0].tasks is not None
    assert len(stories[0].tasks) == 2


def test_ids_are_deterministic_and_match_format():
    story_map, task_map = _status_maps()
    text = "# d - Alpha Story\nx - Build\n"

    first = parse_stories_from_markdown(text, story_map, task_map)
    second = parse_stories_from_markdown(text, story_map, task_map)

    assert first[0].id == second[0].id
    assert first[0].tasks[0].id == second[0].tasks[0].id
    assert re.match(r"^story-1-[0-9a-f]{8}$", first[0].id)
    assert re.match(r"^task-1-1-[0-9a-f]{8}$", first[0].tasks[0].id)


def test_parse_stories_from_markdown_file_reads_and_parses(tmp_path: Path):
    story_map, task_map = _status_maps()
    md = tmp_path / "sample.md"
    md.write_text("# d - Story\nx - task\n", encoding="utf-8")

    stories = parse_stories_from_markdown_file(md, story_map, task_map)

    assert len(stories) == 1
    assert stories[0].name == "Story"


def test_task_attribs_defaults_to_none():
    task = Task(id="t1", name="demo")

    assert task.attribs is None


def test_task_attribs_accepts_string_map():
    task = Task(id="t1", name="demo", attribs={"prompt": "build parser"})

    assert task.attribs == {"prompt": "build parser"}
