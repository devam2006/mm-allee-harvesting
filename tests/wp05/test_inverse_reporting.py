"""Regression tests for the two reporting bugs found in the review of PR #10.

1. With validation selection off the validation loss must still be measured and reported.
2. An L-BFGS failure, abnormal exit or iteration-limit exit must be visible on the result and in the
   exported table, never silently reported as a successful convergence.
"""

import csv
from types import SimpleNamespace

import numpy as np
import pytest

pytest.importorskip("jax")

import mm_allee.pinn.inverse as inverse  # noqa: E402
from mm_allee.data import generate_noisy_observations  # noqa: E402
from mm_allee.pinn.network import NetworkConfig  # noqa: E402
from mm_allee.validation import write_prediction_metrics_csv  # noqa: E402

pytestmark = pytest.mark.pinn
KNOWN = {"known_K": 100.0, "known_initial_population": 45.0}


def make_obs(shift_validation=0.0):
    times = np.linspace(0, 8, 41)
    pops = 45.0 + 50.0 * (1 - np.exp(-times / 1.5))
    obs = generate_noisy_observations(
        times, pops, trajectory_id="rep", model="A", noise_sigma=0.01, noise_seed=11, n_ref=100.0
    )
    if shift_validation:
        obs = dict(obs)
        y = np.array(obs["observed_population"], dtype=float)
        val = np.asarray(obs["val_indices"])
        y[val] += shift_validation * np.where(
            np.arange(len(val)) % 2 == 0, 1.0, -1.0
        )  # alternating sign
        obs["observed_population"] = y
    return obs


def fit(*, selection, epochs=5, lbfgs=0, obs=None, patience=50, **kw):
    tp = inverse.TrainableParameters(
        "A",
        fit_params=["r", "A", "H"],
        known_conditions=KNOWN,
        initial_guesses={"r": 0.5, "A": 25.0, "H": 8.0},
    )
    trainer = inverse.InversePINNTrainer(
        NetworkConfig(layers=(1, 8, 8, 1), activation="tanh"),
        tp,
        lr_net=5e-3,
        lr_params=1e-2,
        lbfgs_iters=lbfgs,
        validation_selection=selection,
        **kw,
    )
    return trainer.fit(
        obs if obs is not None else make_obs(),
        known_conditions=KNOWN,
        epochs=epochs,
        n_collocation=20,
        seed=11,
        eval_every=1,
        patience=patience,
    )


# ---- finding 1: the validation loss is measured whether or not it selects a checkpoint -----


def test_validation_loss_is_finite_and_matches_a_direct_calculation_with_selection_off():
    res = fit(selection=False)
    assert np.isfinite(res.val_loss)
    # direct calculation from the returned model's validation predictions (x = N / K, K = 100)
    assert res.val_loss == pytest.approx((res.val_metrics["rmse"] / 100.0) ** 2, rel=1e-9)
    losses = res.training_history["loss_val"]
    assert len(losses) == 5 and np.all(np.isfinite(losses))  # not the placeholder infinity


def test_validation_loss_history_is_finite_through_the_lbfgs_phase_too():
    res = fit(selection=False, epochs=3, lbfgs=4)
    losses = np.asarray(res.training_history["loss_val"])
    assert "lbfgs" in res.training_history["phase"] and np.all(np.isfinite(losses))


def test_validation_observations_do_not_change_the_model_when_selection_is_off():
    # patience 1 would stop training at the first non-improving validation check if validation data
    # reached the training logic; with selection off it must not
    base = fit(selection=False, epochs=30, lbfgs=3, patience=1)
    shifted = fit(
        selection=False, epochs=30, lbfgs=3, patience=1, obs=make_obs(shift_validation=40.0)
    )
    assert base.training_history["phase"].count("adam") == 30  # full budget in both runs
    assert shifted.training_history["phase"].count("adam") == 30
    assert shifted.estimated_parameters == base.estimated_parameters  # trained model is identical
    assert shifted.train_loss == base.train_loss
    assert shifted.val_loss != base.val_loss  # ... but the validation score reflects the new data


def test_default_selection_still_reports_the_validation_loss_of_the_returned_model():
    res = fit(selection=True, epochs=8)
    assert np.isfinite(res.val_loss)
    assert res.val_loss == pytest.approx((res.val_metrics["rmse"] / 100.0) ** 2, rel=1e-9)


# ---- finding 2: optimizer outcomes are visible ----------------------------------------------


def test_an_lbfgs_exception_is_a_labelled_failure_with_an_adam_fallback(monkeypatch):
    def boom(*args, **kwargs):
        raise RuntimeError("injected optimizer failure")

    monkeypatch.setattr(inverse, "minimize", boom)
    res = fit(selection=False, epochs=5, lbfgs=20)
    assert res.status == "lbfgs_failed" and res.success is False
    assert res.optimizer["lbfgs_outcome"] == "error"
    assert "injected optimizer failure" in res.optimizer["error"]
    assert res.training_history["phase"].count("adam") == 5  # the usable Adam state is the fallback
    assert all(np.isfinite(v) for v in res.estimated_parameters.values())


@pytest.mark.parametrize(
    "scipy_status,message,outcome",
    [
        (0, "CONVERGENCE: REL_REDUCTION_OF_F", "tolerance_reached"),
        (1, "STOP: TOTAL NO. OF ITERATIONS REACHED LIMIT", "iteration_limit"),
        (2, "ABNORMAL: LINE SEARCH FAILED", "abnormal_exit"),
    ],
)
def test_lbfgs_exit_kinds_are_distinguished(monkeypatch, scipy_status, message, outcome):
    def fake_minimize(fun, x0, **kwargs):
        return SimpleNamespace(x=np.asarray(x0), status=scipy_status, message=message, nit=7)

    monkeypatch.setattr(inverse, "minimize", fake_minimize)
    res = fit(selection=False, epochs=3, lbfgs=20)
    assert res.optimizer["lbfgs_outcome"] == outcome
    assert res.optimizer["lbfgs_status"] == scipy_status and res.optimizer["lbfgs_iterations"] == 7
    assert res.optimizer["lbfgs_message"] == message


def test_a_real_run_that_exhausts_its_budget_is_labelled_iteration_limit():
    res = fit(selection=False, epochs=5, lbfgs=3, lbfgs_ftol=0.0, lbfgs_gtol=0.0)
    assert res.optimizer["lbfgs_outcome"] == "iteration_limit"
    assert res.optimizer["lbfgs_iterations"] == 3
    # the Adam-phase status stays "converged": it does not claim L-BFGS reached a tolerance
    assert fit(selection=False, epochs=3, lbfgs=0).optimizer["lbfgs_outcome"] == "not_run"


def test_the_outcome_is_exported_in_the_prediction_table(tmp_path):
    record = {
        "run_id": "r1",
        "method": "PINN",
        "status": "converged",
        "lbfgs_outcome": "iteration_limit",
        "lbfgs_message": "STOP: LIMIT",
    }
    path = tmp_path / "pred.csv"
    write_prediction_metrics_csv(path, [record])
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    assert (
        rows[0]["lbfgs_outcome"] == "iteration_limit" and rows[0]["lbfgs_message"] == "STOP: LIMIT"
    )
