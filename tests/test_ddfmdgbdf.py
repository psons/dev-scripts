"""Unit tests for the ddfmdgbdf DDF<->MDGBDF plugin bridge."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

_bin_dir = Path(__file__).resolve().parents[1] / "bin"
if str(_bin_dir) not in sys.path:
    sys.path.insert(0, str(_bin_dir))


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, _bin_dir / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


gbdata = _load("gbdata")
mdgbdata = _load("mdgbdata")
ddf = _load("ddf")
ddfmdgbdf = _load("ddfmdgbdf")

DO_MD_TEMPLATE = {
    "rules": [
        {"pattern": r"^# Current work\s*$", "ddfType": "MDGBDF"},
        {"pattern": r"^# Completed work\s*$", "ddfType": "MDGBDF"},
    ]
}


def test_current_work_section_parses_as_mdgbdf_stories_at_h2():
    text = (
        "# Current work\n\n"
        "## Story One\n"
        "d - a task\n\n"
        "# Completed work\n\n"
        "x - a bare completed task\n"
    )

    doc = ddf.parse_from_markdown(text, template=DO_MD_TEMPLATE)

    assert len(doc.sections) == 2
    current_section = doc.sections[0]
    assert isinstance(current_section, ddfmdgbdf.MDGBDFSection)
    assert current_section.ddfType == "MDGBDF"
    assert [s.name for s in current_section.stories] == ["Story One"]
    assert current_section.stories[0].tasks[0].name == "a task"

    completed_section = doc.sections[1]
    assert isinstance(completed_section, ddfmdgbdf.MDGBDFSection)
    assert completed_section.stories[0].tasks[0].name == "a bare completed task"


def test_round_trip_markdown_serialization():
    text = "# Current work\n\n## Story One\nd - a task\n"

    doc = ddf.parse_from_markdown(text, template=DO_MD_TEMPLATE)
    rendered = ddf.serialize_to_markdown(doc)
    reparsed = ddf.parse_from_markdown(rendered, template=DO_MD_TEMPLATE)

    assert reparsed.sections[0].stories[0].name == "Story One"
    assert reparsed.sections[0].stories[0].tasks[0].name == "a task"


def test_json_serialization_returns_object_not_list():
    text = "# Current work\n\n## Story One\nd - a task\n"
    doc = ddf.parse_from_markdown(text, template=DO_MD_TEMPLATE)

    data = ddf._doc_to_dict(doc)

    section_dict = data["sections"][0]
    assert isinstance(section_dict, dict)
    assert section_dict["ddfType"] == "MDGBDF"
    assert isinstance(section_dict["stories"], list)
