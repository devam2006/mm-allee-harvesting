"""Regression tests for the numerical issues raised in the PR #3 reviews.

1. Fold tolerance must scale with q_c, and q_c must stay accurate as a -> 1.
2. A tiny excluded negative root must stay negative and excluded.
3. Sign probes must not cross x = 0 or an omitted root; physical labels must not
   depend on ``include_excluded``.
4. Solver settings in the WP01 config must reach the solver, and unsupported
   settings must be rejected.

Independent references: exact-binary Decimal arithmetic at 60 digits for q_c,
the series of the small negative root, and RK45 trajectories for local behaviour.
"""

import importlib.util
import json
from decimal import Decimal, getcontext
from pathlib import Path

import numpy as np
import pytest

from mm_allee import equilibria_plots
from mm_allee.equilibria import (
    FOLD_RTOL,
    equilibria_a,
    equilibria_logistic,
    fold_a,
)
from mm_allee.models import rhs
from mm_allee.solver import solve_trajectory

ROOT = Path(__file__).resolve().parents[2]


def decimal_qc(a):
    """q_c from the unrationalised definition G(x*) in 60-digit arithmetic."""
    getcontext().prec = 60
    A = Decimal(a)  # exact binary value of the float, not its decimal repr
    s = (1 - A + A * A).sqrt()
    x = (1 + A + s) / 3
    return x * (1 - x) * (x / A - 1)


EDGE_A = [1e-6, 1e-3, 0.2, 0.5, 0.9, 0.999, 0.999999, 1 - 2.0**-30]


@pytest.mark.parametrize("a", EDGE_A)
def test_qc_has_full_relative_accuracy_across_the_domain(a):
    _, q_c = fold_a(a)
    ref = decimal_qc(a)
    # A few ulps; FOLD_RTOL (64 eps) is chosen to sit well above this.
    assert abs(Decimal(q_c) / ref - 1) < 8 * np.finfo(float).eps


@pytest.mark.parametrize("a", EDGE_A)
def test_fold_classification_scales_with_qc(a):
    _, q_c = fold_a(a)
    assert len(equilibria_a(a, 0.5 * q_c)) == 2
    assert [r.multiplicity for r in equilibria_a(a, q_c)] == [2]
    assert equilibria_a(a, 2 * q_c) == []
    # Just outside the relative tolerance the two roots are still resolved.
    assert len(equilibria_a(a, q_c * (1 - 4 * FOLD_RTOL))) == 2
    assert equilibria_a(a, q_c * (1 + 4 * FOLD_RTOL)) == []


def test_absolute_offsets_near_ordinary_folds_are_not_merged():
    _, q_c = fold_a(0.2)
    assert len(equilibria_a(0.2, q_c - 1e-13)) == 2
    assert equilibria_a(0.2, q_c + 1e-13) == []
    assert len(equilibria_logistic(0.25 - 1e-13)) == 2
    assert equilibria_logistic(0.25 + 1e-13) == []


@pytest.mark.parametrize("q", [1e-15, 1e-12, 1e-8])
def test_tiny_negative_root_stays_excluded(q):
    a = 0.2
    records = equilibria_a(a, q, include_excluded=True)
    excluded = [r for r in records if not r.physical]
    assert len(excluded) == 1
    neg = excluded[0]
    assert neg.x < 0 and neg.stability == "excluded"
    # Series: G(x) = -x + (1+a)x^2/a + O(x^3), so x = -q - (1+a)q^2/a + O(q^3).
    assert neg.x == pytest.approx(-q - (1 + a) * q**2 / a, rel=1e-12)
    physical = [r for r in records if r.physical]
    assert all(r.x > 0 for r in physical)
    assert not any(r.x == 0 for r in records)


def test_probes_stay_inside_physical_interval_for_tiny_roots():
    a, q = 1e-5, 1e-8
    lower, upper = equilibria_a(a, q)
    assert lower.derivative > 0
    assert (lower.left_sign, lower.right_sign) == (-1, 1)
    assert lower.stability == "unstable"
    assert upper.stability == "stable"
    # Independent local trajectories: both sides move away from the lower root.
    # Short upward run: near capacity this a gives f' ~ -1e5 (stiff), irrelevant here.
    up = solve_trajectory("A", a=a, harvest=q, x0=lower.x * 1.1, tau_end=1.0, atol=1e-16)
    down = solve_trajectory("A", a=a, harvest=q, x0=lower.x * 0.9, tau_end=30, atol=1e-16)
    assert up.extinction_tau is None and up.x[-1] > 1.2 * lower.x  # deviation grows
    assert down.extinction_tau is not None


@pytest.mark.parametrize("a", [1e-5, 1e-3, 0.2, 0.7, 0.999])
@pytest.mark.parametrize("frac", [1e-9, 1e-3, 0.3, 0.9, 1.0])
def test_physical_records_do_not_depend_on_excluded_flag(a, frac):
    _, q_c = fold_a(a)
    q = q_c if frac == 1.0 else frac * q_c
    plain = equilibria_a(a, q)
    shown = [r for r in equilibria_a(a, q, include_excluded=True) if r.physical]
    assert plain == shown


@pytest.mark.parametrize("a", [1e-3, 0.2, 0.999999])
def test_internal_vector_field_matches_shared_rhs(a):
    """Records use the cancellation-free form; residuals agree with models.rhs."""
    _, q_c = fold_a(a)
    for rec in equilibria_a(a, 0.4 * q_c):
        shared = rhs(rec.x, "A", a=a, harvest=0.4 * q_c)
        assert abs(shared) < 1e-12 * max(1.0, q_c)


def test_perturbation_figure_passes_solver_settings(monkeypatch):
    seen = []
    real = equilibria_plots.solve_trajectory

    def spy(*args, **kwargs):
        seen.append({k: kwargs[k] for k in ("rtol", "atol", "max_step")})
        return real(*args, **kwargs)

    monkeypatch.setattr(equilibria_plots, "solve_trajectory", spy)
    fig = equilibria_plots.perturbation_figure(0.2, 0.3, rtol=1e-6, atol=1e-8, max_step=0.5)
    equilibria_plots.plt.close(fig)
    assert len(seen) == 4
    assert all(s == {"rtol": 1e-6, "atol": 1e-8, "max_step": 0.5} for s in seen)


def load_run():
    spec = importlib.util.spec_from_file_location("wp01_run", ROOT / "experiments/wp01/run.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize(
    "block",
    [
        {"method": "DOP853", "rtol": 1e-9, "atol": 1e-11, "max_step": 0.1},
        {"method": "RK45", "rtol": -1.0},
        {"method": "RK45", "first_step": 0.1},
    ],
)
def test_run_rejects_unsupported_solver_settings(block, tmp_path):
    run = load_run()
    config = json.loads((ROOT / "configs/wp01.json").read_text())
    config["solver"] = block
    path = tmp_path / "bad.json"
    path.write_text(json.dumps(config))
    with pytest.raises(ValueError):
        run.main(["--config", str(path), "--output", str(tmp_path / "out")])
    assert not (tmp_path / "out" / "manifest.json").exists()


def test_run_records_and_uses_effective_solver_settings(monkeypatch, tmp_path):
    run = load_run()
    seen = {}
    real = run.perturbation_figure

    def spy(*args, **kwargs):
        seen.update(kwargs)
        return real(*args, **kwargs)

    monkeypatch.setattr(run, "perturbation_figure", spy)
    config = json.loads((ROOT / "configs/wp01.json").read_text())
    config["solver"] = {"method": "RK45", "rtol": 1e-7, "atol": 1e-10, "max_step": 0.2}
    path = tmp_path / "cfg.json"
    path.write_text(json.dumps(config))
    manifest = run.main(["--config", str(path), "--output", str(tmp_path / "out")])
    assert seen == {"rtol": 1e-7, "atol": 1e-10, "max_step": 0.2}
    eff = manifest["solver_effective"]
    assert (eff["method"], eff["rtol"], eff["atol"], eff["max_step"]) == ("RK45", 1e-7, 1e-10, 0.2)
