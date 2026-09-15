"""Contract tests: bin/gbdata.py must keep the fields this repo depends on.

gbdata.py is regenerated from docs/dev/spec/gbdata-spec-2.md; a regeneration that drops or
renames a field used elsewhere in this repo should fail here first.
"""

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


def _field_names(dataclass_type) -> set[str]:
    return {f.name for f in dataclass_type.__dataclass_fields__.values()}


def test_task_has_required_fields():
    assert _field_names(gbdata.Task) >= {"id", "status", "name", "detail", "attributes"}


def test_story_has_required_fields():
    assert _field_names(gbdata.Story) >= {
        "id",
        "name",
        "status",
        "description",
        "maxTasks",
        "tasks",
        "attributes",
    }


def test_task_status_members_used_by_gbops_exist():
    required = {"do", "in_progress", "scheduled", "unfinished", "completed", "abandoned"}
    actual = {member.value for member in gbdata.TaskStatus}
    assert required <= actual


def test_story_status_members_exist():
    required = {"do", "in_progress", "scheduled", "unfinished", "completed", "abandoned"}
    actual = {member.value for member in gbdata.StoryStatus}
    assert required <= actual
