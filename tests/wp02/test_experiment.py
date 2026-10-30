import hashlib
import json
from pathlib import Path

import pytest

from mm_allee.wp02_experiment import run_experiment

ROOT = Path(__file__).resolve().parents[2]


def test_experiment_outputs_and_provenance(tmp_path):
    config = json.loads((ROOT / "configs/wp02.json").read_text())
    config["comparison"]["x0_values"] = [0.9]
    config["comparison"]["fractions"] = [0.5]
    result = run_experiment(config, tmp_path, ROOT)
    assert result["status"] == "success"
    assert len(result["summary"]) == 4
    for row in result["summary"]:
        assert row["final_unassisted"] < 1e-6
        assert row["final_restocked"] > 0.99
        assert row["max_refinement_x_error"] < 2e-7
        if row["model"] == "B":
            assert row["extinction_tau"] is None
    assert (tmp_path / "wp02_b_branches.eps").read_bytes().startswith(b"%!PS")
    for name, expected in result["output_sha256"].items():
        assert hashlib.sha256((tmp_path / name).read_bytes()).hexdigest() == expected
        if name.endswith(".csv"):
            assert b"\r\n" not in (tmp_path / name).read_bytes()
    assert result["config"]["solver"] == config["solver"]


def test_invalid_solver_settings_fail_instead_of_only_entering_manifest(tmp_path):
    config = json.loads((ROOT / "configs/wp02.json").read_text())
    config["solver"]["max_step"] = -1
    with pytest.raises(ValueError):
        run_experiment(config, tmp_path, ROOT)
    assert json.loads((tmp_path / "manifest.json").read_text())["status"] == "failed"
