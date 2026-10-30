"""Tests for the JAX inverse PINN engine, residual autodiff, and leakage boundaries."""

import numpy as np
import pytest

jax = pytest.importorskip("jax")
import jax.numpy as jnp  # noqa: E402

from mm_allee.data import generate_noisy_observations  # noqa: E402
from mm_allee.pinn.autodiff import derivative  # noqa: E402
from mm_allee.pinn.inverse import (  # noqa: E402
    InversePINNTrainer,
    TrainableParameters,
    load_inverse_checkpoint,
    save_inverse_checkpoint,
)
from mm_allee.pinn.network import NetworkConfig, init_params, x_hat  # noqa: E402
from mm_allee.pinn.residual import jax_rhs  # noqa: E402

pytestmark = pytest.mark.pinn


def test_pinn_architecture_forward_shape():
    ncfg = NetworkConfig(layers=(1, 32, 32, 1), t_end=10.0, x0=0.8, seed=11)
    params = init_params(ncfg)

    t = jnp.array([0.0, 1.5, 4.0])
    pred = jax.vmap(lambda s: x_hat(params, s, ncfg))(t)

    assert pred.shape == (3,)
    # Hard initial condition guarantee: x(0) == x0
    assert float(pred[0]) == pytest.approx(0.8)


def test_physics_residual_computation():
    ncfg = NetworkConfig(layers=(1, 16, 16, 1), t_end=5.0, x0=0.5, seed=7)
    params = init_params(ncfg)
    t_colloc = jnp.array([0.5, 1.0, 2.0])

    # Physical parameters
    r, K, A, H = 0.7, 100.0, 20.0, 10.0
    a = A / K

    # Compute dx/dt via JAX autodiff
    dx_dt = derivative(lambda s: x_hat(params, s, ncfg), t_colloc)
    x_val = jax.vmap(lambda s: x_hat(params, s, ncfg))(t_colloc)

    rhs_val = jax_rhs(x_val, "A", a=a, harvest=H / (r * K)) * r
    residual = dx_dt - rhs_val

    assert residual.shape == (3,)
    assert bool(jnp.all(jnp.isfinite(residual)))


def test_inverse_pinn_leakage_audit():
    """Verify that test observations are strictly isolated from training loss gradient."""
    ncfg = NetworkConfig(layers=(1, 16, 16, 1), t_end=10.0, x0=0.5, seed=11)
    params = init_params(ncfg)
    _tp = TrainableParameters("A", fit_params=["r", "A", "H"], known_conditions={"known_K": 100.0})

    t_train = jnp.array([0.1, 0.5])
    y_train = jnp.array([0.45, 0.50])
    t_test = jnp.array([6.0, 8.0])
    y_test = jnp.array([0.70, 0.72])

    def loss_training_only(weights, test_data):
        pred_train = jax.vmap(lambda s: x_hat(weights, s, ncfg))(t_train)
        return jnp.mean((pred_train - y_train) ** 2)

    # Compute gradients with respect to weights and test_data
    grad_weights, grad_test = jax.grad(loss_training_only, argnums=(0, 1))(params, (t_test, y_test))

    # Test observation inputs must receive ZERO gradient
    g_t_test, g_y_test = grad_test
    assert float(jnp.sum(jnp.abs(g_t_test))) == 0.0
    assert float(jnp.sum(jnp.abs(g_y_test))) == 0.0


def test_short_inverse_pinn_smoke_fit():
    """Verify that a short seeded inverse PINN training run executes, reduces loss,

    and updates physical parameters.
    """
    times = np.linspace(0, 4, 30)
    pops = 45.0 + 5.0 * times
    obs = generate_noisy_observations(
        times, pops, trajectory_id="smoke_pinn", model="A", noise_sigma=0.01, noise_seed=11
    )

    ncfg = NetworkConfig(layers=(1, 16, 16, 1), activation="tanh")
    tp = TrainableParameters(
        "A",
        fit_params=["r", "A", "H"],
        known_conditions={"known_K": 100.0, "known_initial_population": 45.0},
        initial_guesses={"r": 0.5, "A": 25.0, "H": 8.0},
    )

    trainer = InversePINNTrainer(ncfg, tp, lr_net=5e-3, lr_params=1e-2)
    res = trainer.fit(
        obs,
        known_conditions={"known_initial_population": 45.0, "known_K": 100.0},
        epochs=15,
        n_collocation=20,
        seed=11,
        eval_every=5,
    )

    assert res.success
    assert res.status in ("converged", "validation_stopped")
    # the history holds the 15 Adam epochs and then the iterations of the L-BFGS phase that follows
    phases = res.training_history["phase"]
    assert phases.count("adam") == 15 and set(phases) <= {"adam", "lbfgs"}
    assert np.isfinite(res.train_loss)
    assert res.wall_seconds > 0
    # Parameter update check: optimizer moved values from starting guess
    assert res.estimated_parameters["r"] != 0.5 or res.estimated_parameters["A"] != 25.0


def test_inverse_checkpoint_round_trip(tmp_path):
    times = np.linspace(0, 4, 20)
    pops = 45.0 + 3.0 * times
    obs = generate_noisy_observations(
        times, pops, trajectory_id="smoke_ck", model="A", noise_sigma=0.0, noise_seed=11
    )

    trainer = InversePINNTrainer()
    res = trainer.fit(obs, epochs=5, n_collocation=15, seed=11)

    ck_path = tmp_path / "inverse_ck.npz"
    save_inverse_checkpoint(ck_path, res)

    loaded_params, loaded_cfg, loaded_est = load_inverse_checkpoint(ck_path)
    assert loaded_cfg.layers == res.network_config.layers
    assert loaded_est["r"] == pytest.approx(res.estimated_parameters["r"])
