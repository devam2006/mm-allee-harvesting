"""Torch parity, autograd, initial-condition, training, checkpoint and reference tests."""

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest

torch = pytest.importorskip("torch")

from mm_allee.metrics import errors  # noqa: E402
from mm_allee.models import rhs  # noqa: E402
from mm_allee.pinn.network import ForwardMLP, NetworkConfig  # noqa: E402
from mm_allee.pinn.residual import collocation_residual, pinn_loss, torch_rhs  # noqa: E402
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
F64 = torch.float64
ROOT = Path(__file__).resolve().parents[2]


def col(values):
    return torch.tensor(values, dtype=F64)[:, None]


# ---- 1. Torch RHS parity with the NumPy reference --------------------------------------


@pytest.mark.parametrize("model", ["logistic", "A", "B"])
@pytest.mark.parametrize("harvest", [0.0, 0.1, 0.78])
def test_torch_rhs_matches_numpy_including_edge_populations(model, harvest):
    a = 0.2
    x = np.array([-0.1, 0.0, a, 0.5, 0.9162277660167949, 1.0, 1.3])  # roots/edges of B
    expected = rhs(x, model, a=a, harvest=harvest)
    actual = torch_rhs(torch.tensor(x, dtype=F64), model, a=a, harvest=harvest).numpy()
    np.testing.assert_allclose(actual, expected, rtol=1e-14, atol=1e-15)


def test_torch_rhs_hand_values():
    x = torch.tensor(0.5, dtype=F64)
    # G(0.5)=0.5*0.5*(0.5/0.2-1)=0.375 by hand
    assert torch_rhs(x, "A", a=0.2, harvest=0.1).item() == pytest.approx(0.275)
    assert torch_rhs(x, "B", a=0.2, harvest=0.3).item() == pytest.approx(0.225)
    assert torch_rhs(x, "logistic", a=0.2, harvest=0.1).item() == pytest.approx(0.15)
    zero = torch.tensor(0.0, dtype=F64)
    assert torch_rhs(zero, "A", a=0.2, harvest=0.1).item() == pytest.approx(-0.1)  # f(0)=-q
    assert torch_rhs(zero, "B", a=0.2, harvest=0.3).item() == 0.0  # zero is a B equilibrium


def test_torch_rhs_rejects_unknown_model():
    with pytest.raises(ValueError):
        torch_rhs(torch.tensor(0.1, dtype=F64), "C", a=0.2, harvest=0.1)


# ---- 2. Residual, derivative and time scaling ------------------------------------------


def test_residual_of_analytic_function_matches_hand_derivative():
    # x(tau)=0.5+0.3 sin(2 tau)  =>  dx/dtau = 0.6 cos(2 tau), differentiated by hand.
    tau = col([0.0, 0.4, 1.1, 2.5])
    x, res = collocation_residual(
        lambda t: 0.5 + 0.3 * torch.sin(2 * t), tau, "A", a=0.2, harvest=0.1
    )
    t = tau.numpy()[:, 0]
    expected = 0.6 * np.cos(2 * t) - rhs(0.5 + 0.3 * np.sin(2 * t), "A", a=0.2, harvest=0.1)
    np.testing.assert_allclose(res.detach().numpy()[:, 0], expected, atol=1e-13)


def test_exact_logistic_solution_has_zero_residual_and_wrong_harvest_is_detected():
    x0 = 0.3
    exact = lambda t: 1 / (1 + ((1 - x0) / x0) * torch.exp(-t))  # noqa: E731  closed form
    tau = col(np.linspace(0, 8, 41))
    _, ok = collocation_residual(exact, tau, "logistic", a=0.2, harvest=0.0)
    assert ok.abs().max().item() < 1e-13
    # A sign or harvest error must be visible: with q=0.1 the residual is exactly +0.1.
    _, bad = collocation_residual(exact, tau, "logistic", a=0.2, harvest=0.1)
    np.testing.assert_allclose(bad.detach().numpy(), 0.1, atol=1e-13)


def test_network_time_scaling_chain_rule():
    net = ForwardMLP(NetworkConfig(t_end=4.0, x0=0.0))
    net.body = torch.nn.Sequential(_Square())  # N(s)=s^2 so x=(tau/4)^2, dx/dtau=2 tau/16
    tau = col([0.5, 1.0, 3.0])
    _, res = collocation_residual(net, tau, "B", a=0.2, harvest=0.0)
    x = (tau / 4) ** 2
    expected = 2 * tau / 16 - rhs(x.numpy()[:, 0], "B", a=0.2, harvest=0.0)[:, None]
    np.testing.assert_allclose(res.detach().numpy(), expected, atol=1e-13)


class _Square(torch.nn.Module):
    def forward(self, s):
        return s**2


# ---- 3. Gradients reach weights and physical parameters --------------------------------


def test_backprop_reaches_weights_and_trainable_physical_parameters():
    net = ForwardMLP(NetworkConfig(width=8, depth=2, t_end=5.0))
    q = torch.nn.Parameter(torch.tensor(0.1, dtype=F64))
    a = torch.nn.Parameter(torch.tensor(0.2, dtype=F64))
    tau = col(np.linspace(0, 5, 25))
    total, _, _ = pinn_loss(net, tau, 0.8, "A", a=a, harvest=q)
    total.backward()
    for p in net.parameters():
        assert p.grad is not None and torch.isfinite(p.grad).all() and p.grad.abs().sum() > 0
    # Independent expectation: R = dx - G(x) + q, so dL/dq = 2*mean(R) with a fixed network.
    _, res = collocation_residual(net, tau, "A", a=0.2, harvest=0.1)
    assert q.grad.item() == pytest.approx(2 * res.mean().item(), rel=1e-9)
    assert a.grad is not None and torch.isfinite(a.grad) and a.grad.abs() > 0


def test_residual_keeps_graph_for_tensor_parameters():
    q = torch.nn.Parameter(torch.tensor(0.1, dtype=F64))
    _, res = collocation_residual(lambda t: 0.5 * t, col([0.2, 0.9]), "A", a=0.2, harvest=q)
    assert res.requires_grad and res.grad_fn is not None


# ---- 4. Initial condition ---------------------------------------------------------------


def test_hard_ic_is_exact_for_any_weights_and_soft_ic_term_matches_hand_value():
    zero = col([0.0])
    for seed in (1, 2, 3):
        hard = ForwardMLP(NetworkConfig(x0=0.8, hard_ic=True, seed=seed))
        assert hard(zero).item() == 0.8  # exact, not approximate
    soft = ForwardMLP(NetworkConfig(x0=0.8, hard_ic=False, seed=1))
    _, _, ic = pinn_loss(soft, col(np.linspace(0, 10, 11)), 0.8, "B", a=0.2, harvest=0.3)
    assert ic.item() == pytest.approx((soft(zero).item() - 0.8) ** 2)


# ---- 5. Training behaviour (short, generous, seeded) -----------------------------------

SMOKE = dict(model="B", a=0.2, harvest=0.3, x0=0.8, t_end=10.0, width=16, adam_epochs=400)


def test_short_seeded_run_reduces_loss_and_is_reproducible():
    first = train_forward(ForwardConfig(**SMOKE))
    again = train_forward(ForwardConfig(**SMOKE))
    other = train_forward(ForwardConfig(**{**SMOKE, "seed": 22}))
    h = first.history
    assert first.status == "ok" and len(h["loss"]) == 400
    assert h["loss"][-1] < 0.05 * h["loss"][0]  # generous: the real drop is far larger
    assert again.history["loss"] == h["loss"]  # same seed -> identical run
    assert other.history["loss"][0] != h["loss"][0]  # different seed -> different init


def test_trainer_hook_updates_extra_physical_parameter():
    q = torch.nn.Parameter(torch.tensor(0.3, dtype=F64))
    cfg = ForwardConfig(**{**SMOKE, "adam_epochs": 30})
    train_forward(cfg, parameters={"harvest": q}, extra_parameters=[q])
    assert q.item() != 0.3  # the optimiser moved it: the graph reached the hook


def test_budget_and_validation():
    capped = train_forward(ForwardConfig(**{**SMOKE, "adam_epochs": 5000, "time_budget_s": 0.05}))
    assert capped.status == "budget_exhausted" and len(capped.history["loss"]) < 5000
    with pytest.raises(ValueError):
        ForwardConfig(**{**SMOKE, "model": "C"}).validate()
    with pytest.raises(ValueError):
        ForwardConfig(**{**SMOKE, "a": 1.2}).validate()


# ---- 6. Metrics and evaluation ----------------------------------------------------------


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


# ---- 7. Checkpoints ---------------------------------------------------------------------


def test_checkpoint_round_trip_predictions_agree(tmp_path):
    result = train_forward(ForwardConfig(**{**SMOKE, "adam_epochs": 20}))
    path = tmp_path / "ck.pt"
    save_checkpoint(path, result)
    net, config = load_checkpoint(path)
    tau = np.linspace(0, 10, 33)
    np.testing.assert_array_equal(predict(net, tau), predict(result.net, tau))
    assert config == result.config


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
    colloc = np.linspace(0, 10.0, 200)
    assert not np.any(np.isin(tau[1:-1], colloc[1:-1]))  # scoring grid is not the training grid


def test_a_training_horizon_is_the_event_not_the_full_window():
    run = load_run()
    case = dict(model="A", a=0.2, harvest=0.55, x0=0.8, tau_end=10.0)
    _, _, hit = run.reference_trajectory(case, REF)
    cfg = {"training": {"width": 8, "adam_epochs": 1}}
    result = run.run_pinn(case, 11, cfg, hit)
    assert result.config.t_end == hit < case["tau_end"]
