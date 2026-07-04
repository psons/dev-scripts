"""Unit tests for mdgbdata parsing and status metadata behavior."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re
import sys

import pytest

# Add bin directory to sys.path so we can import gbdata.py and mdgbdata.py
_bin_dir = Path(__file__).resolve().parents[1] / "bin"
if str(_bin_dir) not in sys.path:
    sys.path.insert(0, str(_bin_dir))

_gb_spec = importlib.util.spec_from_file_location("gbdata", _bin_dir / "gbdata.py")
if _gb_spec is None or _gb_spec.loader is None:
    raise RuntimeError("Unable to load gbdata module for tests")
gbdata = importlib.util.module_from_spec(_gb_spec)
sys.modules["gbdata"] = gbdata
_gb_spec.loader.exec_module(gbdata)

_mdgb_spec = importlib.util.spec_from_file_location("mdgbdata", _bin_dir / "mdgbdata.py")
if _mdgb_spec is None or _mdgb_spec.loader is None:
    raise RuntimeError("Unable to load mdgbdata module for tests")
mdgbdata = importlib.util.module_from_spec(_mdgb_spec)
sys.modules["mdgbdata"] = mdgbdata
_mdgb_spec.loader.exec_module(mdgbdata)

TaskStatus = gbdata.TaskStatus
StoryStatus = gbdata.StoryStatus

compile_status_patterns = mdgbdata.compile_status_patterns
detect_status = mdgbdata.detect_status
load_status_map = mdgbdata.load_status_map
parse_stories_from_markdown = mdgbdata.parse_stories_from_markdown
parse_stories_from_markdown_file = mdgbdata.parse_stories_from_markdown_file
strip_status_prefix = mdgbdata.strip_status_prefix
convert_markdown_file_to_json_text = mdgbdata.convert_markdown_file_to_json_text
stories_to_markdown_text = mdgbdata.stories_to_markdown_text


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
    text = "# d - Story: Build parser\nx - write tests\n"

    stories = parse_stories_from_markdown(text, story_map, task_map)

    assert len(stories) == 1
    assert stories[0].name == "Build parser"
    assert stories[0].status == StoryStatus.DO
    assert stories[0].tasks is not None
    assert stories[0].tasks[0].status == TaskStatus.COMPLETED


def test_non_pattern_heading_with_tasks_still_creates_story_default_do():
    story_map, task_map = _status_maps()
    text = "# Planning\nx - decide approach\n"

    stories = parse_stories_from_markdown(text, story_map, task_map)

    assert len(stories) == 1
    assert stories[0].name == "Planning"
    assert stories[0].status == StoryStatus.DO


def test_status_matched_heading_strips_story_prefix_from_story_name():
    story_map, task_map = _status_maps()
    text = "# d - Story: Build parser\nx - write tests\n"

    stories = parse_stories_from_markdown(text, story_map, task_map)

    assert len(stories) == 1
    assert stories[0].name == "Build parser"


def test_story_prefix_heading_creates_story_without_tasks():
    story_map, task_map = _status_maps()
    text = "## Story: Parser Boundary Behavior\nNo tasks yet.\n"

    stories = parse_stories_from_markdown(text, story_map, task_map)

    assert len(stories) == 1
    assert stories[0].name == "Parser Boundary Behavior"
    assert stories[0].status == StoryStatus.DO
    assert stories[0].tasks is None


def test_story_description_is_parsed_and_preserved():
    story_map, task_map = _status_maps()
    text = "# d - Build parser\nContext line one\n\nContext line two\nx - write tests\n"

    stories = parse_stories_from_markdown(text, story_map, task_map)

    assert len(stories) == 1
    assert stories[0].description == "Context line one\n\nContext line two"


def test_non_pattern_heading_description_before_tasks_is_preserved():
    story_map, task_map = _status_maps()
    text = "# Planning\nStory context\nx - decide approach\n"

    stories = parse_stories_from_markdown(text, story_map, task_map)

    assert len(stories) == 1
    assert stories[0].name == "Planning"
    assert stories[0].description == "Story context"


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
    assert stories[0].status == StoryStatus.DO
    assert stories[0].tasks is not None
    assert len(stories[0].tasks) == 2


def test_ids_are_deterministic_and_match_format():
    story_map, task_map = _status_maps()
    text = "# d - Alpha Story\nx - Build\n"

    first = parse_stories_from_markdown(text, story_map, task_map)
    second = parse_stories_from_markdown(text, story_map, task_map)

    assert first[0].id == second[0].id
    assert first[0].tasks[0].id == second[0].tasks[0].id
    assert re.match(r"^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}-[0-9a-f]{8}$", first[0].id)
    assert re.match(r"^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}-[0-9a-f]{8}$", first[0].tasks[0].id)


def test_immediate_left_margin_id_lines_override_generated_ids():
    story_map, task_map = _status_maps()
    text = "# d - Alpha Story\nid: story-123\nx - Build\nid: task-456\n"

    stories = parse_stories_from_markdown(text, story_map, task_map)

    assert stories[0].id == "story-123"
    assert stories[0].tasks is not None
    assert stories[0].tasks[0].id == "task-456"


def test_non_immediate_or_indented_id_lines_are_not_parsed_as_ids():
    story_map, task_map = _status_maps()
    text = "# d - Alpha Story\n\nid: ignored-story-id\nx - Build\n  id: ignored-task-id\n"

    stories = parse_stories_from_markdown(text, story_map, task_map)

    assert stories[0].id != "ignored-story-id"
    assert stories[0].description == "id: ignored-story-id"
    assert stories[0].tasks is not None
    assert stories[0].tasks[0].id != "ignored-task-id"
    assert stories[0].tasks[0].detail == "  id: ignored-task-id"


def test_parse_stories_from_markdown_file_reads_and_parses(tmp_path: Path):
    story_map, task_map = _status_maps()
    md = tmp_path / "sample.md"
    md.write_text("# d - Story\nx - task\n", encoding="utf-8")

    stories = parse_stories_from_markdown_file(md, story_map, task_map)

    assert len(stories) == 1
    assert stories[0].name == "Story"


def test_task_attribs_default_to_none_from_parsing():
    story_map, task_map = _status_maps()
    text = "# d - Story\nx - parser task\n"

    stories = parse_stories_from_markdown(text, story_map, task_map)

    assert stories[0].tasks is not None
    assert stories[0].tasks[0].attribs is None


def test_stories_to_markdown_writes_story_prefix_in_story_header():
    story_map, task_map = _status_maps()
    stories = parse_stories_from_markdown("# d - Story: Build parser\nx - write tests\n", story_map, task_map)

    markdown = stories_to_markdown_text(stories, story_map, task_map)

    assert "# Story: Build parser" in markdown


def test_stories_to_markdown_keeps_status_marker_for_non_do_story_status():
    story_map, task_map = _status_maps()
    stories = parse_stories_from_markdown("# x - Story: Done Story\n", story_map, task_map)

    markdown = stories_to_markdown_text(stories, story_map, task_map)

    assert "# x - Story: Done Story" in markdown


def test_stories_to_markdown_serializes_story_and_task_ids_after_headers():
    story_map, task_map = _status_maps()
    stories = parse_stories_from_markdown("# d - Story: Build parser\nx - write tests\n", story_map, task_map)

    markdown = stories_to_markdown_text(stories, story_map, task_map)

    assert f"# Story: Build parser\nid: {stories[0].id}" in markdown
    assert stories[0].tasks is not None
    assert f"x - write tests\nid: {stories[0].tasks[0].id}" in markdown


def test_tojson_includes_story_description_without_warning(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    story_map, task_map = _status_maps()
    md = tmp_path / "sample.md"
    md.write_text("# d - Story\ncontext line\nx - task\n", encoding="utf-8")

    out = convert_markdown_file_to_json_text(md, story_map, task_map)
    payload = json.loads(out)
    stderr = capsys.readouterr().err

    assert payload[0]["description"] == "context line"
    assert "some non story text will be ignored" not in stderr
