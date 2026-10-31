"""Core delivery must skip extensions without changing shared evidence."""

import importlib.util
import json
from copy import deepcopy
from pathlib import Path

import numpy as np

from mm_allee import collapse_study

ROOT = Path(__file__).resolve().parents[2]


def small_config():
    config = json.loads((ROOT / "configs/wp03.json").read_text())
    for name in ("curve_points", "basin_control_points", "basin_initial_points"):
        config[name] = 7
    config["a_sweep"] = [0.2]
    return config


def test_core_skips_extension_calculations_and_preserves_core_results(monkeypatch):
    config = small_config()
    historical = collapse_study.build_study(deepcopy(config))

    def forbidden(*args, **kwargs):
        raise AssertionError("An optional calculation ran in core-only mode")

    for name in (
        "threshold_sensitivity",
        "maximum_yields",
        "sustainable_yield_b",
        "safety_margins",
    ):
        monkeypatch.setattr(collapse_study, name, forbidden)
    core = collapse_study.build_study(config, core_only=True)
    assert set(core["tables"]) == {"thresholds", "extinction", "basins", "event_validation"}
    for name, rows in core["tables"].items():
        assert rows == historical["tables"][name]
    for model in ("A", "B"):
        np.testing.assert_array_equal(core["basin_grids"][model], historical["basin_grids"][model])
    for (fraction, result), (old_fraction, old) in zip(
        core["trajectories"], historical["trajectories"], strict=True
    ):
        assert fraction == old_fraction
        np.testing.assert_array_equal(result.x, old.x)
        np.testing.assert_array_equal(result.tau, old.tau)
    assert core["msy"] is None and core["policies"] == []
    assert historical["msy"]["h_MSY"] < historical["msy"]["h_c"]


def test_core_export_has_only_core_evidence_and_trajectory_bottleneck(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location(
        "wp03_core_export", ROOT / "experiments/wp03/run.py"
    )
    runner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(runner)
    captured = {}
    original = runner.save_figure

    def observe(figure, path):
        captured[Path(path).name] = {
            "axes": len(figure.axes),
            "labels": [line.get_label() for axis in figure.axes for line in axis.lines],
        }
        return original(figure, path)

    monkeypatch.setattr(runner, "save_figure", observe)
    manifest = runner.run(small_config(), tmp_path, core_only=True)
    assert set(captured) == {"wp03_basins", "wp03_extinction", "wp03_bottleneck"}
    assert captured["wp03_bottleneck"]["axes"] == 1
    assert not any("square-root" in label for label in captured["wp03_bottleneck"]["labels"])
    assert set(manifest["validation"]) == {"threshold_maxima", "event_integrations"}
    assert all(value == "passed" for value in manifest["validation"].values())
    assert not (tmp_path / "wp03_summary.json").exists()
    assert not (tmp_path / "wp03_sensitivity.csv").exists()
    assert not (tmp_path / "wp03_yield.csv").exists()
    assert not (tmp_path / "wp03_bottleneck.csv").exists()
    assert (tmp_path / "wp03_bottleneck.eps").read_bytes().startswith(b"%!PS-Adobe")
