import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/open_pr.py"
SPEC = importlib.util.spec_from_file_location("open_pr", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_request_exactly_other_four_members():
    roster = {
        "members": [{"github": name} for name in ["alpha", "beta", "gamma", "delta", "epsilon"]]
    }
    assert MODULE.reviewers_for(roster, "BETA") == ["alpha", "gamma", "delta", "epsilon"]


@pytest.mark.parametrize("handles", [[None] * 5, ["a", "A", "b", "c", "d"], ["a", "b"]])
def test_missing_duplicate_or_incomplete_roster_is_rejected(handles):
    roster = {"members": [{"github": handle} for handle in handles]}
    with pytest.raises(ValueError):
        MODULE.reviewers_for(roster, "a")
