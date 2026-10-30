import csv
import importlib.util
import json
from copy import deepcopy
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from mm_allee.datasets import (
    REFERENCE_COLUMNS,
    generate_reference,
    sha256,
    solver_settings,
    validate_config,
    write_reference_files,
)
from mm_allee.models import Parameters
from mm_allee.reference_validation import extinction_quadrature, validate_reference

ROOT = Path(__file__).resolve().parents[2]
CONFIG = json.loads((ROOT / "configs/wp03_reference.json").read_text())


def test_curated_handoff_matches_manifest_and_configured_trajectories():
    fixture = ROOT / "data/fixtures/wp03_reference"
    manifest = json.loads((fixture / "manifest.json").read_text())
    assert manifest["configuration"] == CONFIG
    assert manifest == json.loads((ROOT / "artifacts/manifests/wp03_reference.json").read_text())
    for relative, expected in manifest["files_sha256"].items():
        assert sha256(ROOT / relative) == expected, relative
    for case in CONFIG["cases"]:
        actual = generate_reference(case, CONFIG["solver"])
        with (fixture / f"{actual.trajectory_id}.csv").open() as stream:
            rows = list(csv.DictReader(stream))
        assert len(rows) == len(actual.time)
        # CSV bytes are hashed above; allow small dependency/platform differences
        # when recomputing values rather than pinning a specific SciPy build.
        np.testing.assert_allclose(
            [float(row["time"]) for row in rows], actual.time, rtol=1e-8, atol=1e-8
        )
        np.testing.assert_allclose(
            [float(row["population"]) for row in rows], actual.population, rtol=0, atol=5e-6
        )


@pytest.mark.parametrize("case", CONFIG["cases"], ids=lambda c: c["trajectory_id"])
def test_each_fixture_has_independent_numerical_evidence(case):
    actual = generate_reference(case, CONFIG["solver"])
    evidence = validate_reference(case, actual, CONFIG["solver"], **CONFIG["validation"])
    assert evidence["status"] == "passed"
    assert len(actual.time) == 101
    assert actual.time[0] == 0
    assert actual.population[0] == pytest.approx(case["initial_population"])
    assert np.all(np.diff(actual.time) > 0)
    assert np.all(actual.population >= 0)
    assert np.all(np.isfinite(actual.population))
    if case["trajectory_id"] == "a_extinction":
        assert actual.extinction_time == actual.time[-1]
        assert actual.population[-1] == 0
        assert evidence["event_difference_quadrature"] < 1e-7
    else:
        assert actual.extinction_time is None
    if case["trajectory_id"] == "b_decline":
        assert 0 < actual.population[-1] < actual.population[0]


@pytest.mark.parametrize("model", ["A", "B"])
def test_dimensionful_rescaling_preserves_dynamics(model):
    case = deepcopy(
        next(c for c in CONFIG["cases"] if c["trajectory_id"] == model.lower() + "_regular")
    )
    original = generate_reference(case)
    scaled = deepcopy(case)
    for key in ["K", "A"]:
        scaled["parameters"][key] *= 3
    scaled["parameters"]["r"] *= 2
    scaled["parameters"]["H" if model == "A" else "h"] *= 6 if model == "A" else 2
    scaled["initial_population"] *= 3
    scaled["time_end"] /= 2
    actual = generate_reference(scaled)
    np.testing.assert_allclose(actual.time, original.time / 2, rtol=1e-14, atol=1e-14)
    np.testing.assert_allclose(actual.population, original.population * 3, rtol=1e-12, atol=1e-10)


def test_custom_dimensional_observation_times():
    case = deepcopy(CONFIG["cases"][0])
    case["time_points"] = [0, 0.11, 0.38, 1.17, 2.01]
    actual = generate_reference(case)
    np.testing.assert_allclose(actual.time, case["time_points"], rtol=0, atol=1e-15)
    assert validate_reference(case, actual)["status"] == "passed"


def test_reference_exports_are_reproducible_and_do_not_create_inverse_inputs(tmp_path):
    references = [generate_reference(c) for c in CONFIG["cases"][:2]]
    first, second = tmp_path / "one", tmp_path / "two"
    paths = write_reference_files(first, references, CONFIG)
    write_reference_files(second, references, CONFIG)
    ids = []
    for path in paths:
        assert path.read_bytes() == (second / path.name).read_bytes()
        if path.suffix == ".csv":
            with path.open() as stream:
                reader = csv.DictReader(stream)
                assert tuple(reader.fieldnames) == REFERENCE_COLUMNS
                rows = list(reader)
            assert len(rows) == 101
            ids.extend(row["observation_id"] for row in rows)
            assert all(row["is_synthetic"] == "true" for row in rows)
            assert not {"split", "observed_population", "noise_sigma"} & set(rows[0])
    assert len(ids) == len(set(ids))
    conditions = json.loads((first / "conditions.json").read_text())
    for known in conditions["trajectories"].values():
        assert set(known) == {"model", "known_K", "known_initial_population", "csv"}
    assert json.loads((first / "truth.json").read_text())["evaluation_only"] is True


@pytest.mark.parametrize("problem", ["schema", "duplicate", "units", "scale"])
def test_invalid_config_is_rejected(problem):
    config = deepcopy(CONFIG)
    if problem == "schema":
        config["schema_version"] = 2
    if problem == "duplicate":
        config["cases"].append(config["cases"][0])
    if problem == "units":
        config["units"]["time"] = ""
    if problem == "scale":
        config["fixed_reference_scales"]["population"] = float("nan")
    with pytest.raises(ValueError):
        validate_config(config)


@pytest.mark.parametrize(
    "problem", ["model", "identifier", "mixed_control", "negative_initial", "points"]
)
def test_invalid_reference_case_is_rejected(problem):
    case = deepcopy(CONFIG["cases"][0])
    if problem == "model":
        case["model"] = "logistic"
    if problem == "identifier":
        case["trajectory_id"] = "../escape"
    if problem == "mixed_control":
        case["parameters"]["h"] = 0.1
    if problem == "negative_initial":
        case["initial_population"] = -1
    if problem == "points":
        case["n_points"] = True
    with pytest.raises(ValueError):
        generate_reference(case)


@pytest.mark.parametrize(
    "settings", [{"rtol": 0}, {"rtol": 1e-16}, {"max_step": float("nan")}, {"method": "RK4"}]
)
def test_invalid_solver_settings(settings):
    with pytest.raises(ValueError):
        solver_settings(settings)


def test_quadrature_rejects_equilibrium_poles_and_zero_yield():
    assert extinction_quadrature(Parameters(0.7, 100, 20, H=10), 80) is None
    assert extinction_quadrature(Parameters(0.7, 100, 20), 10) is None
    assert extinction_quadrature(Parameters(0.7, 100, 20, H=10), 0) is None
    case = dict(deepcopy(CONFIG["cases"][0]), initial_population=10)
    actual = generate_reference(case)
    assert actual.extinction_time == pytest.approx(
        extinction_quadrature(actual.parameters, 10), abs=1e-7
    )


def test_independent_check_detects_a_wrong_production_rhs(monkeypatch):
    import mm_allee.solver as solver

    correct = solver.rhs
    monkeypatch.setattr(solver, "rhs", lambda *args, **kwargs: correct(*args, **kwargs) + 0.001)
    case = CONFIG["cases"][0]
    corrupted = generate_reference(case)
    assert validate_reference(case, corrupted)["status"] == "failed"


def test_independent_check_rejects_corrupted_population_and_event():
    case = CONFIG["cases"][2]
    actual = generate_reference(case)
    assert (
        validate_reference(case, replace(actual, population=actual.population + 0.1))["status"]
        == "failed"
    )
    assert (
        validate_reference(case, replace(actual, extinction_time=actual.extinction_time + 0.001))[
            "status"
        ]
        == "failed"
    )


def test_cli_module_is_import_safe_and_invalid_case_writes_nothing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    spec = importlib.util.spec_from_file_location(
        "wp03_reference_cli", ROOT / "experiments/wp03/generate_reference.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert not list(tmp_path.iterdir())
    config = deepcopy(CONFIG)
    config["cases"][-1]["parameters"]["A"] = -1
    with pytest.raises(ValueError):
        module.run(config, tmp_path / "invalid")
    assert not (tmp_path / "invalid").exists()


def test_reference_cli_rejects_unsupported_rtol_before_writing(tmp_path):
    spec = importlib.util.spec_from_file_location(
        "wp03_reference_rtol_cli", ROOT / "experiments/wp03/generate_reference.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    config = deepcopy(CONFIG)
    config["solver"]["rtol"] = 1e-16
    with pytest.raises(ValueError, match="RK45 rtol must be at least"):
        module.run(config, tmp_path / "invalid-rtol")
    assert not (tmp_path / "invalid-rtol").exists()
