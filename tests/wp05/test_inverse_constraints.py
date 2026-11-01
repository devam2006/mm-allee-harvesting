"""Tests for parameter constraint transforms, JAX gradient propagation, and scaling chain rules."""

import pytest

jax = pytest.importorskip("jax")
import jax.numpy as jnp  # noqa: E402

from mm_allee.pinn.autodiff import derivative  # noqa: E402
from mm_allee.pinn.inverse import TrainableParameters  # noqa: E402
from mm_allee.pinn.network import NetworkConfig, init_params, x_hat  # noqa: E402

pytestmark = pytest.mark.pinn


def test_trainable_parameters_constraint_bounds():
    # Model A: fit r, A, H with known K = 100
    tp_a = TrainableParameters(
        model="A",
        fit_params=["r", "A", "H"],
        known_conditions={"known_K": 100.0},
        initial_guesses={"r": 0.5, "A": 30.0, "H": 12.0},
    )

    p_a = tp_a()
    assert float(p_a["r"]) > 0
    assert 0 < float(p_a["A"]) < float(p_a["K"])
    assert float(p_a["K"]) == 100.0
    assert float(p_a["H"]) >= 0
    assert float(p_a["h"]) == 0.0

    # Model B: fit r, A, h with known K = 100
    tp_b = TrainableParameters(
        model="B",
        fit_params=["r", "A", "h"],
        known_conditions={"known_K": 100.0},
        initial_guesses={"r": 1.2, "A": 15.0, "h": 0.3},
    )

    p_b = tp_b()
    assert float(p_b["r"]) > 0
    assert 0 < float(p_b["A"]) < float(p_b["K"])
    assert float(p_b["h"]) >= 0
    assert float(p_b["H"]) == 0.0


def test_trainable_parameters_receive_nonzero_gradients():
    tp = TrainableParameters(
        model="A",
        fit_params=["r", "A", "H"],
        known_conditions={"known_K": 100.0},
    )

    def loss(raw):
        p = tp(raw)
        return (p["r"] - 0.7) ** 2 + (p["A"] - 25.0) ** 2 + (p["H"] - 10.0) ** 2

    grads = jax.grad(loss)(tp.raw_params)

    for name in tp.fit_params:
        assert name in grads, f"Gradient missing for {name}"
        g = grads[name]
        assert bool(jnp.all(jnp.isfinite(g))), f"Gradient non-finite for {name}"
        assert float(jnp.abs(g)) > 0, f"Gradient is zero for {name}"


def test_all_four_parameters_constraint():
    # Fit all 4: r, K, A, H
    tp = TrainableParameters(
        model="A",
        fit_params=["r", "K", "A", "H"],
        initial_guesses={"r": 0.8, "K": 120.0, "A": 25.0, "H": 8.0},
    )

    p = tp()
    assert float(p["r"]) > 0
    assert float(p["K"]) > 0
    assert 0 < float(p["A"]) < float(p["K"])
    assert float(p["H"]) >= 0


def test_fixed_reference_scaling_chain_rule():
    t_end = 10.0
    x0 = 0.8
    ncfg = NetworkConfig(layers=(1, 16, 16, 1), t_end=t_end, x0=x0, seed=11)
    params = init_params(ncfg)

    t = jnp.array([1.0, 2.5, 5.0])
    # Exact reverse-mode autodiff with respect to physical time
    dx_dt = derivative(lambda s: x_hat(params, s, ncfg), t)

    assert dx_dt.shape == t.shape
    assert bool(jnp.all(jnp.isfinite(dx_dt)))
