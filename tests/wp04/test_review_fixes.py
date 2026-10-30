"""Regression tests for the PR #6 review findings (invalid scoring, parameter ranges, checkpoints,
units parity, run labelling). Each one fails on the code as it was before the fix."""

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest

jax = pytest.importorskip("jax")

import jax.numpy as jnp  # noqa: E402

from mm_allee.models import Parameters, dimensional_rhs  # noqa: E402
from mm_allee.pinn.network import NetworkConfig, init_params, x_hat  # noqa: E402
from mm_allee.pinn.residual import collocation_residual  # noqa: E402
from mm_allee.pinn.train_forward import (  # noqa: E402
    ForwardConfig,
    ForwardResult,
    evaluate_prediction,
    load_checkpoint,
    physics_residual,
    predict,
    save_checkpoint,
    train_forward,
)

pytestmark = pytest.mark.pinn
ROOT = Path(__file__).resolve().parents[2]


def load_run():
    spec = importlib.util.spec_from_file_location("wp04_run_rf", ROOT / "experiments/wp04/run.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["wp04_run_rf"] = module
    spec.loader.exec_module(module)
    return module


# ---- review 1: a broken prediction must not receive a perfect score -----------------------


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), float("-inf")])
def test_invalid_predictions_are_never_scored(bad):
    out = evaluate_prediction([1.0, bad], [1.0, 0.0])  # the review's example
    assert out["valid"] is False and out["n_invalid"] == 1
    for key in ("rmse", "mae", "relative_l2", "max_abs", "max_abs_near_zero"):
        assert out[key] is None  # undefined, not zero
    assert out["boundary_violations"] == 1


def test_valid_predictions_still_scored_and_flagged_valid():
    out = evaluate_prediction([2.0, 4.0], [1.0, 2.0])
    assert out["valid"] is True and out["n_invalid"] == 0
    assert out["rmse"] == pytest.approx(np.sqrt(2.5)) and out["relative_l2"] == pytest.approx(1.0)


def test_near_zero_error_hand_values():
    # reference values below 0.05: only the first point; |0.0 - 0.03| = 0.03, overall max 0.2
    out = evaluate_prediction([0.0, 0.5, 1.0], [0.03, 0.5, 1.2])
    assert out["max_abs"] == pytest.approx(0.2)
    assert out["max_abs_near_zero"] == pytest.approx(0.03)
    assert (
        evaluate_prediction([0.4, 0.9], [0.5, 1.0])["max_abs_near_zero"] is None
    )  # none near zero


def test_run_labels_invalid_and_undefined_scores_conservatively():
    run = load_run()
    valid = {"valid": True, "relative_l2": 1e-3, "max_abs": 2e-3}
    assert run.label_status("ok", valid, 5e-2) == "ok"
    assert run.label_status("ok", {**valid, "relative_l2": 0.2}, 5e-2) == "inaccurate"
    assert run.label_status("ok", {**valid, "valid": False, "relative_l2": None}, 5e-2) == (
        "invalid_prediction"
    )
    # undefined relative error (tiny reference): fall back to the max absolute error
    assert run.label_status("ok", {**valid, "relative_l2": None, "max_abs": 1e-3}, 5e-2) == "ok"
    assert run.label_status("ok", {**valid, "relative_l2": None, "max_abs": 0.5}, 5e-2) == (
        "inaccurate"
    )
    assert run.label_status("budget_exhausted", valid, 5e-2) == "budget_exhausted"  # kept


def test_nan_network_output_is_labelled_invalid_not_accurate(monkeypatch):
    run = load_run()
    cfg = {"inaccuracy_threshold_relative_l2": 5e-2, "training": {}}
    case = dict(model="B", a=0.2, harvest=0.3, x0=0.8, tau_end=10.0)

    def fake_run_pinn(case, seed, cfg, hit):
        fc = ForwardConfig(model="B", seed=seed, layers=(1, 4, 1))
        params = [(w * jnp.nan, b) for w, b in init_params(fc.network_config())]
        return ForwardResult(params=params, config=fc)

    monkeypatch.setattr(run, "run_pinn", fake_run_pinn)
    tau = np.linspace(0, 10, 11)
    _, _, ev, status, note = run.fit_and_score(case, 11, cfg, (tau, np.full(11, 0.5)), None)
    assert status == "invalid_prediction" and ev["relative_l2"] is None
    assert "non-finite" in note


def test_a_run_that_raises_is_recorded_as_failed_not_fatal():
    run = load_run()
    cfg = {"inaccuracy_threshold_relative_l2": 5e-2, "training": {"layers": [2, 3, 1]}}  # invalid
    case = dict(model="B", a=0.2, harvest=0.3, x0=0.8, tau_end=10.0)
    result, pred, ev, status, note = run.fit_and_score(
        case, 11, cfg, (np.linspace(0, 10, 11), np.full(11, 0.5)), None
    )
    assert result is None and pred is None and status == "failed" and "ValueError" in note
    assert ev["relative_l2"] is None


# ---- review 2: trained physical parameters stay in their allowed ranges --------------------

BASE = dict(model="B", x0=0.8, t_end=10.0, layers=(1, 8, 8, 1), seed=11)


def test_review_example_harvest_stays_nonnegative_after_one_adam_step():
    cfg = ForwardConfig(a=0.9, harvest=0.0, adam_iters=1, lbfgs_iters=0, **BASE)
    r = train_forward(cfg, physical={"harvest": 0.0})  # was -0.00999999 before the fix
    assert r.physical["harvest"] >= 0.0 and r.status == "ok"


@pytest.mark.parametrize("adam,lbfgs", [(60, 0), (0, 60), (30, 30)])
def test_ranges_hold_through_adam_and_lbfgs(adam, lbfgs):
    # aggressive learning rate and starts next to the boundaries push an unconstrained value out
    cfg = ForwardConfig(a=0.99, harvest=0.0, adam_iters=adam, lbfgs_iters=lbfgs, lr=0.5, **BASE)
    r = train_forward(cfg, physical={"harvest": 0.0, "a": 0.99})
    assert r.physical["harvest"] >= 0.0
    assert 0.0 < r.physical["a"] < 1.0
    assert np.isfinite(list(r.physical.values())).all()


def test_constrained_parameters_still_receive_gradients_and_move():
    cfg = ForwardConfig(a=0.5, harvest=0.3, adam_iters=40, lbfgs_iters=0, **BASE)
    r = train_forward(cfg, physical={"harvest": 0.3, "a": 0.5})
    assert r.physical["harvest"] != pytest.approx(0.3) and r.physical["a"] != pytest.approx(0.5)


def test_zero_harvest_start_is_lifted_to_the_documented_floor():
    cfg = ForwardConfig(a=0.5, harvest=0.0, adam_iters=0, lbfgs_iters=0, **BASE)
    r = train_forward(cfg, physical={"harvest": 0.0})
    assert r.physical["harvest"] == pytest.approx(1e-6)


@pytest.mark.parametrize(
    "bad",
    [{"harvest": -0.1}, {"a": 1.0}, {"a": 0.0}, {"a": 1.5}, {"r": 1.0}, {"harvest": float("nan")}],
)
def test_invalid_physical_starts_are_rejected(bad):
    cfg = ForwardConfig(a=0.5, harvest=0.3, adam_iters=1, lbfgs_iters=0, **BASE)
    with pytest.raises(ValueError):
        train_forward(cfg, physical=bad)


# ---- review 3: loading a model keeps its learned parameters --------------------------------


def test_checkpoint_round_trip_keeps_learned_parameters_and_residual(tmp_path):
    cfg = ForwardConfig(a=0.2, harvest=0.3, adam_iters=60, lbfgs_iters=20, **BASE)
    r = train_forward(cfg, physical={"harvest": 0.3})
    path = tmp_path / "m.npz"
    save_checkpoint(path, r)
    loaded = load_checkpoint(path)
    assert loaded.physical == r.physical and abs(loaded.physical["harvest"] - 0.3) > 1e-3
    assert loaded.config == r.config and loaded.status == r.status and loaded.lbfgs == r.lbfgs
    tau = np.linspace(0, 10, 41)
    np.testing.assert_array_equal(
        predict(loaded.params, loaded.config, tau), predict(r.params, r.config, tau)
    )
    before = physics_residual(r.params, r.config, tau, r.physical)
    after = physics_residual(loaded.params, loaded.config, tau, loaded.physical)
    np.testing.assert_array_equal(before, after)  # same equation residual after save/load
    # ... and it really is the learned harvest being used, not the config constant
    assert not np.allclose(after, physics_residual(loaded.params, loaded.config, tau))


def test_lbfgs_exit_is_recorded():
    cfg = ForwardConfig(a=0.2, harvest=0.3, adam_iters=5, lbfgs_iters=30, **BASE)
    r = train_forward(cfg)
    assert set(r.lbfgs) == {"status", "message", "iterations"} and r.lbfgs["iterations"] > 0
    assert (
        train_forward(ForwardConfig(a=0.2, harvest=0.3, adam_iters=3, lbfgs_iters=0, **BASE)).lbfgs
        is None
    )


# ---- units: forward (dimensionless) and dimensional equations agree ------------------------


@pytest.mark.parametrize(
    "model,kw,harvest_dimless",
    [("A", dict(H=10.0), 10.0 / (0.7 * 100.0)), ("B", dict(h=0.2), 0.2 / 0.7)],
)
def test_dimensional_residual_equals_rK_times_dimensionless_residual(model, kw, harvest_dimless):
    """For N(t)=K*x_hat(r t): dN/dt - dimensional_rhs(N) == r*K*(dx/dtau - f(x)).

    The left side uses the independent NumPy ``models.dimensional_rhs`` and autodiff in physical
    time t; the right side is the forward residual in tau=r*t. It checks the chain rule and the
    scalings x=N/K, q=H/(rK), e=h/r that connect the forward and the dimensional (inverse) forms.
    """
    r_, K, A = 0.7, 100.0, 20.0
    p = Parameters(r=r_, K=K, A=A, **kw)
    cfg = NetworkConfig(layers=(1, 8, 8, 1), t_end=5.6, x0=0.45, seed=3)
    params = init_params(cfg)
    t = np.linspace(0.0, 8.0, 17)
    N_fn = lambda tt: K * x_hat(params, r_ * tt, cfg)  # noqa: E731
    dNdt = np.asarray(jax.vmap(jax.grad(N_fn))(jnp.asarray(t)))
    N = np.asarray(jax.vmap(N_fn)(jnp.asarray(t)))
    lhs = dNdt - dimensional_rhs(N, model, p)
    _, R = collocation_residual(
        lambda tau: x_hat(params, tau, cfg), r_ * t, model, a=A / K, harvest=harvest_dimless
    )
    np.testing.assert_allclose(lhs, r_ * K * np.asarray(R), rtol=1e-9, atol=1e-9)


def test_figures_are_saved_as_png_eps_and_pdf_in_a_new_directory(tmp_path):
    """LaTeX includes the extensionless name, so the PDF must exist next to PNG/EPS (Raghav's
    review); regression for writing the PDF into a directory that does not exist yet."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    run = load_run()
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
    paths = run.save_figure_with_pdf(fig, tmp_path / "new" / "sub" / "wp04_demo")
    plt.close(fig)
    assert sorted(p.suffix for p in paths) == [".eps", ".pdf", ".png"]
    assert all(p.exists() and p.stat().st_size > 0 for p in paths)
