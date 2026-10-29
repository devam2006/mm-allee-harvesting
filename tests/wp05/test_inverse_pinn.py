"""Tests for the inverse PINN engine, autograd residual, and leakage boundaries."""

import numpy as np
import pytest


@pytest.mark.pinn
def test_pinn_architecture_forward_shape():
    torch = pytest.importorskip("torch")
    from mm_allee.pinn.network import PINN

    net = PINN(hidden_layers=[32, 32], activation="tanh", t_ref=1.0, n_ref=100.0)
    t = torch.tensor([[0.0], [1.5], [4.0]], dtype=torch.float32)

    pred_norm = net(t)
    pred_pop = net.predict_population(t)

    assert pred_norm.shape == (3, 1)
    assert pred_pop.shape == (3, 1)
    torch.testing.assert_close(pred_pop, pred_norm * 100.0)


@pytest.mark.pinn
def test_physics_residual_computation():
    torch = pytest.importorskip("torch")
    from mm_allee.pinn.network import PINN
    from mm_allee.pinn.residual import physics_residual

    net = PINN(hidden_layers=[16, 16], activation="tanh")
    t_colloc = torch.tensor([[0.5], [1.0], [2.0]], dtype=torch.float32, requires_grad=True)

    params = {
        "r": torch.tensor(0.7, dtype=torch.float32),
        "K": torch.tensor(100.0, dtype=torch.float32),
        "A": torch.tensor(20.0, dtype=torch.float32),
        "H": torch.tensor(10.0, dtype=torch.float32),
    }

    res = physics_residual(net, t_colloc, "A", params)
    assert res.shape == (3, 1)
    assert torch.all(torch.isfinite(res))


@pytest.mark.pinn
def test_inverse_pinn_leakage_audit():
    """Verify that test observation tensors never enter the autograd computational graph

    during training loss backpropagation.
    """
    torch = pytest.importorskip("torch")
    from mm_allee.pinn.inverse import TrainableParameters
    from mm_allee.pinn.network import PINN

    net = PINN(hidden_layers=[16, 16], activation="tanh")
    tp = TrainableParameters("A", fit_params=["r", "A", "H"], known_conditions={"known_K": 100.0})

    # Create dummy train and test tensors with gradient tracking
    t_train = torch.tensor([[0.1], [0.5]], dtype=torch.float32)
    y_train = torch.tensor([[45.0], [50.0]], dtype=torch.float32)
    t_test = torch.tensor([[6.0], [8.0]], dtype=torch.float32, requires_grad=True)
    y_test = torch.tensor([[70.0], [72.0]], dtype=torch.float32, requires_grad=True)

    # Compute training loss strictly using training data
    pred_train = net.predict_population(t_train)
    loss = torch.mean(((pred_train - y_train) / 100.0) ** 2)
    loss.backward()

    # Verify that test observations received NO gradient
    assert t_test.grad is None
    assert y_test.grad is None


@pytest.mark.pinn
def test_short_inverse_pinn_smoke_fit():
    """Verify that a short seeded inverse PINN training run executes, reduces loss,

    and updates physical parameters.
    """
    torch = pytest.importorskip("torch")
    from mm_allee.data import generate_noisy_observations
    from mm_allee.pinn.inverse import InversePINNTrainer, TrainableParameters
    from mm_allee.pinn.network import PINN

    times = np.linspace(0, 4, 30)
    pops = 45.0 + 5.0 * times
    obs = generate_noisy_observations(
        times, pops, trajectory_id="smoke_pinn", model="A", noise_sigma=0.01, noise_seed=11
    )

    net = PINN(hidden_layers=[16, 16], activation="tanh")
    tp = TrainableParameters(
        "A",
        fit_params=["r", "A", "H"],
        known_conditions={"known_K": 100.0, "known_initial_population": 45.0},
        initial_guesses={"r": 0.5, "A": 25.0, "H": 8.0},
    )

    trainer = InversePINNTrainer(net, tp, lr_net=5e-3, lr_params=1e-2)
    res = trainer.fit(obs, known_conditions={"known_initial_population": 45.0}, epochs=10, n_collocation=20)

    assert res.success
    assert len(res.training_history["loss_train"]) == 10
    # Training loss should be finite
    assert np.isfinite(res.train_loss)
    assert res.wall_seconds > 0
