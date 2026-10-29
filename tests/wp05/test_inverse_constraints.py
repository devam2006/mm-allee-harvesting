"""Tests for parameter constraint transforms, gradient propagation, and scaling chain rules."""

import numpy as np
import pytest

from mm_allee.pinn.inverse import TrainableParameters


@pytest.mark.pinn
def test_trainable_parameters_constraint_bounds():
    torch = pytest.importorskip("torch")

    # Model A: fit r, A, H with known K = 100
    tp_a = TrainableParameters(
        model="A",
        fit_params=["r", "A", "H"],
        known_conditions={"known_K": 100.0},
        initial_guesses={"r": 0.5, "A": 30.0, "H": 12.0},
    )

    p_a = tp_a()
    assert p_a["r"].item() > 0
    assert 0 < p_a["A"].item() < p_a["K"].item()
    assert p_a["K"].item() == 100.0
    assert p_a["H"].item() >= 0
    assert p_a["h"].item() == 0.0

    # Model B: fit r, A, h with known K = 100
    tp_b = TrainableParameters(
        model="B",
        fit_params=["r", "A", "h"],
        known_conditions={"known_K": 100.0},
        initial_guesses={"r": 1.2, "A": 15.0, "h": 0.3},
    )

    p_b = tp_b()
    assert p_b["r"].item() > 0
    assert 0 < p_b["A"].item() < p_b["K"].item()
    assert p_b["h"].item() >= 0
    assert p_b["H"].item() == 0.0


@pytest.mark.pinn
def test_trainable_parameters_receive_nonzero_gradients():
    torch = pytest.importorskip("torch")

    tp = TrainableParameters(
        model="A",
        fit_params=["r", "A", "H"],
        known_conditions={"known_K": 100.0},
    )

    p = tp()
    # Mock scalar objective function with non-zero residual to test gradient flow
    loss = (p["r"] - 0.7) ** 2 + (p["A"] - 25.0) ** 2 + (p["H"] - 10.0) ** 2
    loss.backward()

    for name, param in tp.raw_params.items():
        assert param.grad is not None, f"Gradient missing for {name}"
        assert torch.isfinite(param.grad), f"Gradient non-finite for {name}"
        assert param.grad.abs().item() > 0, f"Gradient is zero for {name}"


@pytest.mark.pinn
def test_all_four_parameters_constraint():
    torch = pytest.importorskip("torch")

    # Fit all 4: r, K, A, H
    tp = TrainableParameters(
        model="A",
        fit_params=["r", "K", "A", "H"],
        initial_guesses={"r": 0.8, "K": 120.0, "A": 25.0, "H": 8.0},
    )

    p = tp()
    assert p["r"].item() > 0
    assert p["K"].item() > 0
    assert 0 < p["A"].item() < p["K"].item()
    assert p["H"].item() >= 0


@pytest.mark.pinn
def test_fixed_reference_scaling_chain_rule():
    torch = pytest.importorskip("torch")
    from mm_allee.pinn.autodiff import derivative
    from mm_allee.pinn.network import PINN

    t_ref = 2.0
    n_ref = 50.0
    net = PINN(hidden_layers=[16], activation="tanh", t_ref=t_ref, n_ref=n_ref)

    t = torch.tensor([[1.0], [2.5]], dtype=torch.float32, requires_grad=True)

    # Dimensional population N(t) = net(t / t_ref) * n_ref
    N = net.predict_population(t)

    # dN/dt via autograd
    dN_dt = derivative(N, t)

    assert dN_dt.shape == t.shape
    assert torch.all(torch.isfinite(dN_dt))
