"""Branch data, exported table and the reproduction command."""

import csv
import importlib.util
import json
from pathlib import Path

import numpy as np
import pytest

from mm_allee.equilibria import branch_rows, fold_a
from mm_allee.models import rhs

ROOT = Path(__file__).resolve().parents[2]


def load_run_module():
    spec = importlib.util.spec_from_file_location("wp01_run", ROOT / "experiments/wp01/run.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # import-safe: no work at import time
    return module


def test_branch_rows_labels_and_counts():
    a = 0.2
    x_star, q_c = fold_a(a)
    q = [0.0, 0.2, q_c - 1e-8, q_c, 0.7]
    rows = branch_rows("A", q, a=a)
    by_q = {}
    for row in rows:
        by_q.setdefault(row["q"], []).append(row)
    assert [r["branch"] for r in by_q[0.0]] == ["zero", "threshold", "capacity"]
    assert [r["branch"] for r in by_q[0.2]] == ["lower", "upper"]
    near = by_q[q_c - 1e-8]
    assert [r["branch"] for r in near] == ["lower", "upper"]  # close roots both kept
    assert near[1]["x"] - near[0]["x"] > 1e-5
    assert [r["branch"] for r in by_q[q_c]] == ["fold"]
    assert 0.7 not in by_q  # no physical equilibrium above the fold
    for row in rows:
        assert abs(rhs(row["x"], "A", a=a, harvest=row["q"])) < 1e-12
        assert row["x"] >= 0


def test_upper_branch_decreases_and_lower_increases_with_harvest():
    a = 0.3
    _, q_c = fold_a(a)
    q = np.linspace(1e-3, q_c * 0.999, 200)
    rows = branch_rows("A", q, a=a)
    upper = np.array([r["x"] for r in rows if r["branch"] == "upper"])
    lower = np.array([r["x"] for r in rows if r["branch"] == "lower"])
    assert len(upper) == len(lower) == 200
    # Implicit differentiation: dx/dq = 1/G'(x): negative on the upper, positive on the lower.
    assert np.all(np.diff(upper) < 0) and np.all(np.diff(lower) > 0)


def test_experiment_writes_all_promised_outputs(tmp_path):
    run = load_run_module()
    manifest = run.main(["--config", str(ROOT / "configs/wp01.json"), "--output", str(tmp_path)])
    for stem in ["wp01_logistic_vs_allee", "wp01_model_a_branches", "wp01_model_a_perturbations"]:
        for ext in (".png", ".eps"):
            path = tmp_path / "figures" / f"{stem}{ext}"
            assert path.stat().st_size > 1000
    eps = (tmp_path / "figures/wp01_model_a_branches.eps").read_text(errors="ignore")
    assert eps.startswith("%!PS-Adobe") and "%%BoundingBox" in eps
    saved = json.loads((tmp_path / "manifest.json").read_text())
    assert saved["status"] == "success" and saved["run_id"] == manifest["run_id"]
    for key in [
        "git_sha",
        "config",
        "versions",
        "hardware",
        "root_finding",
        "solver",
        "elapsed_seconds",
        "outputs",
        "units",
    ]:
        assert key in saved
    assert set(saved["outputs"]) >= {"tables/wp01_equilibria.csv", "tables/wp01_thresholds.json"}

    with (tmp_path / "tables/wp01_equilibria.csv").open() as fh:
        rows = list(csv.DictReader(fh))
    assert rows and list(rows[0]) == run.TABLE_COLUMNS
    for row in rows:
        if row["domain_status"] == "physical_population":
            model, a, q, x = row["model"], row["a"], float(row["q"]), float(row["x"])
            value = rhs(x, model, a=float(a) if a else 0.5, harvest=q)
            assert abs(value) < 1e-12 and x >= 0
            assert row["stability"] in {"stable", "unstable", "semistable"}
        elif row["domain_status"] == "excluded_negative_root":
            assert float(row["x"]) < 0 and row["stability"] == "excluded"
    critical = [
        r for r in rows if r["regime"] == "critical" and r["domain_status"] == "physical_population"
    ]
    assert critical and all(
        r["multiplicity"] == "2" and r["stability"] == "semistable" for r in critical
    )
    # 0.999999 q_c keeps two physical roots rather than merging them into the fold.
    near = [
        r
        for r in rows
        if r["model"] == "A"
        and r["a"] == "0.2"
        and r["q_over_qc"].startswith("0.999999")
        and r["domain_status"] == "physical_population"
    ]
    assert len(near) == 2

    thresholds = json.loads((tmp_path / "tables/wp01_thresholds.json").read_text())
    ex = thresholds["dimensional_example"]
    assert thresholds["model_A"]["H_c_tonnes_per_year"] == pytest.approx(
        ex["r_per_year"] * ex["K_tonnes"] * fold_a(0.2)[1]
    )
    assert thresholds["logistic"]["H_c_tonnes_per_year"] == pytest.approx(
        ex["r_per_year"] * ex["K_tonnes"] / 4
    )
