import importlib.util
import json
import re
import shutil
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("sync_team", ROOT / "scripts/sync_team.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def roster():
    return {
        "members": [
            {"id": f"member{i}", "github": handle, "work_package": None}
            for i, handle in enumerate(
                ["devam2006", "Prem-Mehta03", "rohanagrawal28", "AshChan07", "RaghavSinghal15"], 1
            )
        ]
    }


def copied_docs(tmp_path):
    paths = ["README.md", "STATUS.md", "docs/tasks/README.md", "presentation/outline.md"]
    paths += ["docs/tasks/" + info["brief"] for info in MODULE.TASKS.values()]
    for name in paths:
        target = tmp_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    return tmp_path


def test_unassigned_roster_and_other_four_reviewers_remain_possible():
    value = roster()
    assert MODULE.validate_roster(value) == {}
    assert MODULE.owner_label({}, "WP03") == "Unclaimed"


@pytest.mark.parametrize(
    "problem",
    [
        "duplicate_handle",
        "duplicate_task",
        "unknown_task",
        "bad_handle",
        "duplicate_id",
        "missing_member",
    ],
)
def test_invalid_rosters_fail_before_document_updates(problem):
    value = roster()
    members = value["members"]
    if problem == "duplicate_handle":
        members[1]["github"] = "DEVAM2006"
    elif problem == "duplicate_task":
        members[0]["work_package"] = members[1]["work_package"] = "WP02"
    elif problem == "unknown_task":
        members[0]["work_package"] = "WP06"
    elif problem == "bad_handle":
        members[0]["github"] = "not a handle"
    elif problem == "duplicate_id":
        members[1]["id"] = members[0]["id"]
    else:
        members.pop()
    with pytest.raises(ValueError):
        MODULE.validate_roster(value)


def test_choices_update_every_ownership_surface_and_preserve_progress(tmp_path):
    root = copied_docs(tmp_path)
    value = roster()
    value["members"][0]["work_package"] = "WP05"
    value["members"][3]["work_package"] = "WP01"
    status = root / "STATUS.md"
    # Set fixture progress independently of the live roster's current owner/state.
    text, count = re.subn(
        r"(?m)^(\| WP01 \|[^|\n]*\|)[^|\n]*(\|)",
        r"\1 In progress \2",
        status.read_text(),
        count=1,
    )
    assert count == 1
    status.write_text(text)
    updates = MODULE.render_updates(root, value)
    assert len(updates) == 9
    for name in ["README.md", "docs/tasks/README.md", "presentation/outline.md"]:
        assert "@devam2006" in updates[root / name]
        assert "@AshChan07" in updates[root / name]
    assert "**Owner:** @devam2006" in updates[root / "docs/tasks/WP05_inverse_pinn.md"]
    assert "**Owner:** @AshChan07" in updates[root / "docs/tasks/WP01_foundations.md"]
    assert "| WP01 | @AshChan07 | In progress |" in updates[status]
    assert "**Owner:** Unclaimed" in updates[root / "docs/tasks/WP03_collapse.md"]
    for path, text in updates.items():
        path.write_text(text)
    assert MODULE.render_updates(root, value) == updates


def test_missing_marker_does_not_write_any_files(tmp_path):
    root = copied_docs(tmp_path)
    target = root / "presentation/outline.md"
    target.write_text(target.read_text().replace("<!-- team-sync:presentation:end -->", ""))
    before = {p: p.read_bytes() for p in root.rglob("*.md")}
    with pytest.raises(ValueError):
        MODULE.render_updates(root, roster())
    assert {p: p.read_bytes() for p in root.rglob("*.md")} == before


def test_repository_ownership_blocks_are_current():
    value = json.loads((ROOT / "team.json").read_text())
    for path, rendered in MODULE.render_updates(ROOT, value).items():
        assert path.read_text() == rendered, f"Run python scripts/sync_team.py: {path.name}"
