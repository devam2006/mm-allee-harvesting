import importlib.util
import json
from copy import deepcopy
from pathlib import Path

import numpy as np
import pytest

from mm_allee.collapse_study import build_study
from mm_allee.datasets import sha256

ROOT = Path(__file__).resolve().parents[2]
CONFIG = json.loads((ROOT / "configs/wp03.json").read_text())


def load_script(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_study_cli_is_import_safe_and_invalid_config_publishes_nothing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    module = load_script("wp03_study", "experiments/wp03/run.py")
    assert not list(tmp_path.iterdir())
    config = deepcopy(CONFIG)
    config["parameters"]["A"] = -1
    with pytest.raises(ValueError):
        module.run(config, tmp_path / "results")
    assert not (tmp_path / "results").exists()


def test_runtime_budget_is_enforced_before_study_publication():
    config = deepcopy(CONFIG)
    config["runtime_budget_seconds"] = 1e-12
    with pytest.raises(RuntimeError, match="budget"):
        build_study(config)


def test_curated_analysis_files_have_matching_hashes_and_configuration():
    manifest = json.loads((ROOT / "artifacts/manifests/wp03_analysis.json").read_text())
    assert manifest["configuration"] == CONFIG
    for relative, expected in manifest["files_sha256"].items():
        assert sha256(ROOT / relative) == expected, relative
    assert all(v == "passed" for v in manifest["validation"].values())


@pytest.mark.parametrize("points", [60, 61])
@pytest.mark.parametrize("extinction_code", [0, 1])
def test_basin_mesh_cannot_draw_persistence_above_the_fold(points, extinction_code):
    # Exercise both a sampled fold and a fold between samples, for A and B.
    # Inspect actual coloured-cell coordinates, not just the input basin labels.
    module = load_script("wp03_basin_plot", "experiments/wp03/run.py")
    controls = np.linspace(0, 1.25, points)
    initials = np.array([0.1, 0.6, 1.1])
    grid = np.tile(np.where(controls <= 1, 2, extinction_code), (len(initials), 1))
    fig, axis = module.plt.subplots()
    try:
        meshes = module.plot_basin_grid(axis, controls, initials, grid, ["red"] * 5)
        assert len(meshes) == 2
        for mesh in meshes:
            coordinates = mesh.get_coordinates()
            values = np.asarray(mesh.get_array()).reshape(len(initials), -1)
            left, right = coordinates[:-1, :-1, 0], coordinates[:-1, 1:, 0]
            assert np.all(right[values == 2] <= 1)
            assert np.all(left[values == extinction_code] >= 1)
        assert np.all(meshes[0].get_coordinates()[:, -1, 0] == 1)
        assert np.all(meshes[1].get_coordinates()[:, 0, 0] == 1)
    finally:
        module.plt.close(fig)


def test_submission_audit_exposes_all_relevant_blockers_and_never_claims_approval(tmp_path):
    module = load_script("submission_audit", "scripts/check_submission_ready.py")
    (tmp_path / "report").mkdir()
    (tmp_path / "report/main.tex").write_text(r"SCAFFOLD\_ONLY")
    (tmp_path / "report/main.pdf").write_text("not a pdf")
    figures = tmp_path / "artifacts/figures"
    figures.mkdir(parents=True)
    (figures / "result.png").write_bytes(b"image")
    roster = json.loads((ROOT / "team.json").read_text())
    for member in roster["members"]:
        member["name"] = None  # This fixture tests missing names, independently of the live roster.
    (tmp_path / "team.json").write_text(json.dumps(roster))
    result = module.audit(tmp_path)
    assert not result["automated_ready"]
    kinds = {row["kind"] for row in result["blockers"]}
    assert {
        "missing_file",
        "invalid_pdf",
        "unfinished_content",
        "missing_eps",
        "missing_eps_partner",
        "missing_author_names",
        "missing_presentation_datetime",
    } <= kinds
    assert "four current human approvals" in result["human_verification_required"]


def test_existing_packager_refuses_incomplete_project_without_creating_a_zip(tmp_path, monkeypatch):
    module = load_script("submission_packager", "scripts/package_submission.py")
    monkeypatch.setattr(module, "ROOT", tmp_path)
    with pytest.raises(SystemExit, match="Not ready"):
        module.main()
    assert not (tmp_path / "submission/mm-allee-submission.zip").exists()
