"""Exercise the inverse trainer's actual loss against the forward residual API."""

import numpy as np
import pytest

pytest.importorskip("jax")

from mm_allee.data import generate_noisy_observations  # noqa: E402
from mm_allee.pinn.inverse import InversePINNTrainer, TrainableParameters  # noqa: E402
from mm_allee.pinn.network import NetworkConfig, x_hat  # noqa: E402
from mm_allee.pinn.residual import collocation_residual  # noqa: E402

pytestmark = pytest.mark.pinn


@pytest.mark.parametrize("model", ["A", "B"])
@pytest.mark.parametrize("r,K", [(0.4, 80.0), (1.3, 170.0)])
def test_inverse_training_physics_loss_matches_forward_residual_with_time_scaling(model, r, K):
    """Inverse dx/dt residual = r * forward dx/dtau residual, where tau = r*t.

    Freeze both learning rates so the logged inverse physics loss and the returned
    network refer to the same state. Compare that *actual training loss* with the
    forward API on the identical physical curve; no copy of the inverse RHS is
    used as an oracle. Nonunit r and different K detect missing time/harvest scaling.
    """
    times = np.linspace(0.0, 3.0, 21)
    populations = K * (0.45 + 0.1 * times / times[-1])
    observations = generate_noisy_observations(
        times,
        populations,
        trajectory_id=f"parity_{model}",
        model=model,
        noise_sigma=0.0,
        noise_seed=11,
        n_ref=K,
    )
    known = {"known_K": K, "known_initial_population": populations[0]}
    harvest_name = "H" if model == "A" else "h"
    parameters = TrainableParameters(
        model,
        fit_params=["r", "A", harvest_name],
        known_conditions=known,
        initial_guesses={"r": r, "A": 0.23 * K, harvest_name: 7.0 if model == "A" else 0.17},
    )
    trainer = InversePINNTrainer(
        NetworkConfig(layers=(1, 4, 4, 1)),
        parameters,
        lr_net=0.0,
        lr_params=0.0,
        lbfgs_iters=0,
        validation_selection=False,
    )
    result = trainer.fit(
        observations,
        known_conditions=known,
        epochs=1,
        n_collocation=9,
        seed=7,
        eval_every=1,
    )
    physical = result.all_parameters
    actual_r = physical["r"]
    harvest = (
        physical["H"] / (actual_r * physical["K"]) if model == "A" else physical["h"] / actual_r
    )
    _, residual = collocation_residual(
        lambda tau: x_hat(result.network_params, tau / actual_r, result.network_config),
        actual_r * np.linspace(0.0, times[-1], 9),
        model,
        a=physical["A"] / physical["K"],
        harvest=harvest,
    )
    expected_loss = float(np.mean((actual_r * np.asarray(residual)) ** 2))
    assert np.isfinite(expected_loss)
    assert result.training_history["loss_phys"][0] == pytest.approx(
        expected_loss,
        rel=1e-11,
        abs=1e-12,
    )
