#!/usr/bin/env python3
"""ddfmdgbdf - DDF plugin bridging DDF sections to MDGBDF stories/tasks.

Registers itself for ddfType "MDGBDF" on import (see ddf.register_plugin). A section
matched to MDGBDF (via template or ddfType attribute) is parsed by mdgbdata.py as a list
of gbdata.Story objects held on MDGBDFSection.stories, at a heading level one deeper than
the enclosing section (per docs/dev/spec/dtask-final-modules-spec.md and
docs/dev/spec/adr/ddf/ddf-issues.md).

Public API:
- MDGBDFSection: DDFSection subclass holding a `stories` list instead of `sections`.
- parse_section / serialize_section_markdown / serialize_section_json: the DDFPlugin protocol.
- register(): idempotently register this plugin with ddf.py.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import ddf
import mdgbdata
from gbdata import Story, StoryStatus, TaskStatus

DDF_TYPE = "MDGBDF"


@dataclass
class MDGBDFSection(ddf.DDFSection):
    """A DDFSection whose content is a list of gbdata.Story objects, not nested sections."""

    stories: list[Story] = field(default_factory=list)
    ddfType: str = DDF_TYPE
    heading_level: int = 1


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _load_status_maps() -> tuple[mdgbdata.StatusMap, mdgbdata.StatusMap]:
    repo_root = _repo_root()
    story_map = mdgbdata.load_status_map(repo_root / "docs/dev/spec/story_status_metadata.json", StoryStatus)
    task_map = mdgbdata.load_status_map(repo_root / "docs/dev/spec/task_status_metadata.json", TaskStatus)
    return story_map, task_map


def parse_section(heading: str, level: int, text: str) -> MDGBDFSection:
    """Parse a DDF section's body text as MDGBDF, with stories at heading level `level + 1`."""
    story_map, task_map = _load_status_maps()
    stories = mdgbdata.parse_stories_from_markdown(
        text,
        story_map,
        task_map,
        story_heading_level=level + 1,
    )
    return MDGBDFSection(heading=heading, stories=stories, heading_level=level)


def serialize_section_markdown(section: MDGBDFSection) -> str:
    """Serialize an MDGBDFSection back to a markdown section (heading + MDGBDF story list)."""
    story_map, task_map = _load_status_maps()
    body = mdgbdata.stories_to_markdown_text(
        section.stories,
        story_map,
        task_map,
        story_heading_level=section.heading_level + 1,
    )
    heading = section.heading.rstrip()
    body = body.rstrip("\n")
    return f"{heading}\n\n{body}" if body else heading


def serialize_section_json(section: MDGBDFSection) -> dict:
    """Serialize an MDGBDFSection to a JSON-compatible dict (never a bare list)."""
    result: dict[str, Any] = {
        "heading": section.heading,
        "ddfType": section.ddfType,
    }
    if section.attributes:
        result["attributes"] = section.attributes
    result["stories"] = [mdgbdata._story_to_dict(story) for story in section.stories]
    return result


def register() -> None:
    """Register this plugin for ddfType MDGBDF. Safe to call more than once."""
    ddf.register_plugin(DDF_TYPE, _Plugin())


class _Plugin:
    """Thin adapter exposing this module's functions as a ddf.DDFPlugin."""

    def parse_section(self, heading: str, level: int, text: str) -> MDGBDFSection:
        return parse_section(heading, level, text)

    def serialize_section_markdown(self, section: MDGBDFSection) -> str:
        return serialize_section_markdown(section)

    def serialize_section_json(self, section: MDGBDFSection) -> dict:
        return serialize_section_json(section)


register()

__all__ = [
    "DDF_TYPE",
    "MDGBDFSection",
    "parse_section",
    "serialize_section_markdown",
    "serialize_section_json",
    "register",
]
