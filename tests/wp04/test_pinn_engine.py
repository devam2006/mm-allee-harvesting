"""JAX parity, autodiff, hard-IC, training, checkpoint and reference tests."""

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest

jax = pytest.importorskip("jax")

import jax.numpy as jnp  # noqa: E402

from mm_allee.metrics import errors  # noqa: E402
from mm_allee.models import rhs  # noqa: E402
from mm_allee.pinn.network import NetworkConfig, init_params, x_hat  # noqa: E402
from mm_allee.pinn.residual import collocation_residual, jax_rhs, physics_loss  # noqa: E402
from mm_allee.pinn.train_forward import (  # noqa: E402
    ForwardConfig,
    evaluate_prediction,
    load_checkpoint,
    predict,
    save_checkpoint,
    train_forward,
)
from mm_allee.solver import solve_trajectory  # noqa: E402

pytestmark = pytest.mark.pinn
ROOT = Path(__file__).resolve().parents[2]


def test_float64_is_enabled():
    assert jnp.ones(1).dtype == jnp.float64


# ---- 1. JAX RHS parity with the NumPy reference ----------------------------------------


@pytest.mark.parametrize("model", ["logistic", "A", "B"])
@pytest.mark.parametrize("harvest", [0.0, 0.1, 0.78])
def test_jax_rhs_matches_numpy_including_edge_populations(model, harvest):
    a = 0.2
    x = np.array([-0.1, 0.0, a, 0.5, 0.9162277660167949, 1.0, 1.3])  # roots/edges of B
    expected = rhs(x, model, a=a, harvest=harvest)
    actual = np.asarray(jax_rhs(jnp.asarray(x), model, a=a, harvest=harvest))
    np.testing.assert_allclose(actual, expected, rtol=1e-14, atol=1e-15)


def test_jax_rhs_hand_values():
    x = jnp.asarray(0.5)
    # G(0.5)=0.5*0.5*(0.5/0.2-1)=0.375 by hand
    assert float(jax_rhs(x, "A", a=0.2, harvest=0.1)) == pytest.approx(0.275)
    assert float(jax_rhs(x, "B", a=0.2, harvest=0.3)) == pytest.approx(0.225)
    assert float(jax_rhs(x, "logistic", a=0.2, harvest=0.1)) == pytest.approx(0.15)
    zero = jnp.asarray(0.0)
    assert float(jax_rhs(zero, "A", a=0.2, harvest=0.1)) == pytest.approx(-0.1)  # f(0)=-q
    assert float(jax_rhs(zero, "B", a=0.2, harvest=0.3)) == 0.0  # zero is a B equilibrium


def test_jax_rhs_rejects_unknown_model():
    with pytest.raises(ValueError):
        jax_rhs(jnp.asarray(0.1), "C", a=0.2, harvest=0.1)


# ---- 2. Residual, derivative and time scaling ------------------------------------------


def test_residual_of_analytic_function_matches_hand_derivative():
    # x(tau)=0.5+0.3 sin(2 tau)  =>  dx/dtau = 0.6 cos(2 tau), differentiated by hand.
    tau = np.array([0.0, 0.4, 1.1, 2.5])
    _, res = collocation_residual(
        lambda t: 0.5 + 0.3 * jnp.sin(2 * t), tau, "A", a=0.2, harvest=0.1
    )
    expected = 0.6 * np.cos(2 * tau) - rhs(0.5 + 0.3 * np.sin(2 * tau), "A", a=0.2, harvest=0.1)
    np.testing.assert_allclose(np.asarray(res), expected, atol=1e-13)


def test_exact_logistic_solution_has_zero_residual_and_wrong_harvest_is_detected():
    x0 = 0.3
    exact = lambda t: 1 / (1 + ((1 - x0) / x0) * jnp.exp(-t))  # noqa: E731  closed form
    tau = np.linspace(0, 8, 41)
    _, ok = collocation_residual(exact, tau, "logistic", a=0.2, harvest=0.0)
    assert float(jnp.max(jnp.abs(ok))) < 1e-13
    # A sign or harvest error must be visible: with q=0.1 the residual is exactly +0.1.
    _, bad = collocation_residual(exact, tau, "logistic", a=0.2, harvest=0.1)
    np.testing.assert_allclose(np.asarray(bad), 0.1, atol=1e-13)


def test_network_time_scaling_chain_rule_against_finite_differences():
    cfg = NetworkConfig(t_end=4.0, x0=0.8, seed=3)
    params = init_params(cfg)
    tau = np.array([0.3, 1.0, 2.2, 3.7])
    _, res = collocation_residual(lambda t: x_hat(params, t, cfg), tau, "B", a=0.2, harvest=0.0)
    h = 1e-6
    fx = lambda t: np.array([float(x_hat(params, jnp.asarray(v), cfg)) for v in t])  # noqa: E731
    fd = (fx(tau + h) - fx(tau - h)) / (2 * h)  # independent of autodiff, in physical tau
    expected = fd - rhs(fx(tau), "B", a=0.2, harvest=0.0)
    np.testing.assert_allclose(np.asarray(res), expected, atol=1e-7)


# ---- 3. Gradients reach weights and physical parameters --------------------------------


def make_loss(cfg, model, tau):
    def loss(params, a, harvest):
        return physics_loss(lambda t: x_hat(params, t, cfg), tau, model, a=a, harvest=harvest)

    return loss


def test_gradients_reach_weights_and_physical_parameters():
    cfg = NetworkConfig(layers=(1, 8, 8, 1), t_end=5.0, seed=5)
    params = init_params(cfg)
    tau = jnp.linspace(0, 5, 25)
    loss = make_loss(cfg, "A", tau)
    g_params, g_a, g_q = jax.grad(loss, argnums=(0, 1, 2))(params, 0.2, 0.1)
    for weight_grad, bias_grad in g_params:
        for g in (weight_grad, bias_grad):
            assert bool(jnp.all(jnp.isfinite(g)))
        assert float(jnp.abs(weight_grad).sum()) > 0
    # Independent expectation: R = dx - G(x) + q, so dL/dq = 2*mean(R) for a fixed network.
    _, res = collocation_residual(lambda t: x_hat(params, t, cfg), tau, "A", a=0.2, harvest=0.1)
    assert float(g_q) == pytest.approx(2 * float(jnp.mean(res)), rel=1e-9)
    assert np.isfinite(float(g_a)) and float(g_a) != 0.0


# ---- 4. Hard initial condition ---------------------------------------------------------


def test_hard_ic_is_exact_for_any_weights():
    for seed in (1, 2, 3):
        cfg = NetworkConfig(x0=0.8, seed=seed)
        assert float(x_hat(init_params(cfg), jnp.asarray(0.0), cfg)) == 0.8  # exact equality
    # ... and stays exact when the weights are far from their initial values
    cfg = NetworkConfig(x0=0.8)
    big = [(10 * w, 10 * b + 1) for w, b in init_params(cfg)]
    assert float(x_hat(big, jnp.asarray(0.0), cfg)) == 0.8


def test_network_config_validation():
    with pytest.raises(ValueError):
        init_params(NetworkConfig(layers=(2, 8, 1)))
    with pytest.raises(ValueError):
        init_params(NetworkConfig(t_end=0.0))


# ---- 4b. Activation options -------------------------------------------------------------


def test_activation_functions_hand_values_and_validation():
    from mm_allee.pinn.network import ACTIVATIONS

    x = jnp.array([-2.0, 0.0, 1.5])
    np.testing.assert_allclose(ACTIVATIONS["tanh"](x), np.tanh(np.asarray(x)), atol=1e-15)
    sig = 1 / (1 + np.exp(-np.asarray(x)))
    np.testing.assert_allclose(ACTIVATIONS["sigmoid"](x), sig, atol=1e-15)
    np.testing.assert_allclose(
        ACTIVATIONS["swish"](x), np.asarray(x) * sig, atol=1e-15
    )  # x*sigmoid(x)
    with pytest.raises(ValueError):
        init_params(NetworkConfig(activation="relu"))


@pytest.mark.parametrize("activation", ["tanh", "swish", "sigmoid"])
def test_every_activation_keeps_hard_ic_and_gradients(activation):
    cfg = NetworkConfig(layers=(1, 8, 8, 1), t_end=5.0, seed=4, activation=activation)
    params = init_params(cfg)
    assert float(x_hat(params, jnp.asarray(0.0), cfg)) == cfg.x0  # exact for any activation
    tau = jnp.linspace(0, 5, 25)
    g = jax.grad(make_loss(cfg, "B", tau))(params, 0.2, 0.3)
    assert all(bool(jnp.all(jnp.isfinite(w))) and float(jnp.abs(w).sum()) > 0 for w, _ in g)
    # a different activation really changes the function (the option is wired through)
    other = NetworkConfig(layers=(1, 8, 8, 1), t_end=5.0, seed=4, activation="tanh")
    if activation != "tanh":
        assert float(x_hat(params, jnp.asarray(2.0), cfg)) != float(
            x_hat(params, jnp.asarray(2.0), other)
        )


# ---- 5. Training behaviour (short, generous, seeded) -----------------------------------

SMOKE = dict(model="B", a=0.2, harvest=0.3, x0=0.8, t_end=10.0, adam_iters=100, lbfgs_iters=500)


def test_short_seeded_run_reduces_loss_is_two_phase_and_reproducible():
    first = train_forward(ForwardConfig(**SMOKE))
    again = train_forward(ForwardConfig(**SMOKE))
    other = train_forward(ForwardConfig(**{**SMOKE, "seed": 22}))
    h = first.history
    assert first.status == "ok"
    assert h["phase"][:100] == ["adam"] * 100 and set(h["phase"][100:]) == {"lbfgs"}
    assert h["loss"][-1] < 1e-2 * h["loss"][0]  # generous: the real drop is far larger
    assert h["loss"][-1] <= h["loss"][99]  # L-BFGS never ends above the Adam hand-over loss
    assert again.history["loss"] == h["loss"]  # same seed -> identical run
    assert other.history["loss"][0] != h["loss"][0]  # different seed -> different init


def test_trainer_hook_updates_physical_parameter():
    cfg = ForwardConfig(**{**SMOKE, "adam_iters": 30, "lbfgs_iters": 0})
    result = train_forward(cfg, physical={"harvest": 0.5})
    assert result.physical["harvest"] != 0.5  # the optimiser moved it: gradient reached the hook


def test_custom_collocation_grid_is_used_and_validated():
    cfg = ForwardConfig(**{**SMOKE, "adam_iters": 5, "lbfgs_iters": 0})
    grid = np.linspace(0, 10, 7) ** 1.0
    custom = train_forward(cfg, tau=grid)
    default = train_forward(cfg)  # 100 uniform points, a different loss value
    assert custom.history["loss"][0] != default.history["loss"][0]
    same = train_forward(cfg, tau=np.linspace(0, 10, cfg.n_collocation))
    # default == explicit uniform grid (NumPy vs JAX linspace differ in the last bit)
    np.testing.assert_allclose(same.history["loss"], default.history["loss"], rtol=1e-12)
    for bad in (np.array([0.0]), np.array([-1.0, 1.0]), np.array([0.0, 11.0])):
        with pytest.raises(ValueError):
            train_forward(cfg, tau=bad)


def test_budget_and_validation():
    capped = train_forward(ForwardConfig(**{**SMOKE, "adam_iters": 5000, "time_budget_s": 0.05}))
    assert capped.status == "budget_exhausted" and len(capped.history["loss"]) < 5000
    with pytest.raises(ValueError):
        ForwardConfig(**{**SMOKE, "model": "C"}).validate()
    with pytest.raises(ValueError):
        ForwardConfig(**{**SMOKE, "a": 1.2}).validate()
    with pytest.raises(ValueError):
        ForwardConfig(**{**SMOKE, "n_collocation": 1}).validate()


# ---- 6. Metrics and evaluation ---------------------------------------------------------


def test_evaluate_prediction_hand_vectors_and_near_zero_reference():
    out = evaluate_prediction([2.0, 4.0], [1.0, 2.0])
    assert out["rmse"] == pytest.approx(np.sqrt(2.5)) and out["mae"] == 1.5
    assert out["relative_l2"] == pytest.approx(1.0) and out["max_abs"] == 2.0
    tiny = evaluate_prediction([1e-9, 0.0], [1e-9, 1e-12])  # ||ref|| ~ 1e-9 < floor
    assert tiny["relative_l2"] is None and tiny["mae"] < 1e-9
    assert errors([1.0], [1.0])["rmse"] == 0.0


def test_boundary_violations_count_negative_and_nonfinite():
    out = evaluate_prediction([0.1, -0.01, float("nan"), 0.2], [0.1, 0.0, 0.1, 0.2])
    assert out["boundary_violations"] == 2


# ---- 7. Checkpoints --------------------------------------------------------------------


def test_checkpoint_round_trip_predictions_agree(tmp_path):
    result = train_forward(ForwardConfig(**{**SMOKE, "adam_iters": 20, "lbfgs_iters": 0}))
    path = tmp_path / "ck.npz"
    save_checkpoint(path, result)
    loaded = load_checkpoint(path)
    tau = np.linspace(0, 10, 33)
    np.testing.assert_array_equal(
        predict(loaded.params, loaded.config, tau), predict(result.params, result.config, tau)
    )
    assert loaded.config == result.config


# ---- 8. Reference data are independent of training; no post-event tail -----------------


def load_run():
    path = ROOT / "experiments" / "wp04" / "run.py"
    spec = importlib.util.spec_from_file_location("wp04_run", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["wp04_run"] = module
    spec.loader.exec_module(module)
    return module


REF = {"method": "DOP853", "rtol": 1e-12, "atol": 1e-14, "n_points": 501}


def test_import_has_no_side_effects(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    load_run()
    assert list(tmp_path.iterdir()) == []


def test_reference_a_stops_at_event_with_no_zero_tail_and_matches_rk45():
    run = load_run()
    case = dict(model="A", a=0.2, harvest=0.55, x0=0.8, tau_end=10.0)
    tau, x, hit = run.reference_trajectory(case, REF)
    assert hit is not None and tau[-1] == hit and 7.6 < hit < 7.8
    assert np.all(x[:-1] > 0) and x[-1] == 0.0  # zero only at the exact event endpoint
    rk = solve_trajectory("A", a=0.2, harvest=0.55, x0=0.8, tau_end=10.0, n_points=501)
    assert rk.extinction_tau == pytest.approx(hit, abs=1e-7)  # two solvers agree on the event
    np.testing.assert_allclose(np.interp(tau, rk.tau, rk.x), x, atol=1e-7)


def test_reference_b_has_no_finite_extinction_and_grid_differs_from_collocation():
    run = load_run()
    case = dict(model="B", a=0.2, harvest=0.3, x0=0.1, tau_end=10.0)
    tau, x, hit = run.reference_trajectory(case, REF)
    assert hit is None and tau[-1] == 10.0 and np.all(x > 0)
    colloc = np.linspace(0, 10.0, 100)
    assert not np.any(np.isin(tau[1:-1], colloc[1:-1]))  # scoring grid is not the training grid


def test_a_training_horizon_is_the_event_not_the_full_window():
    run = load_run()
    case = dict(model="A", a=0.2, harvest=0.55, x0=0.8, tau_end=10.0)
    _, _, hit = run.reference_trajectory(case, REF)
    cfg = {"training": {"adam_iters": 1, "lbfgs_iters": 0}}
    result = run.run_pinn(case, 11, cfg, hit)
    assert result.config.t_end == hit < case["tau_end"]
