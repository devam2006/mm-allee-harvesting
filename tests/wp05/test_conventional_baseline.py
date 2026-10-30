"""Tests for the conventional SciPy ODE least-squares baseline."""

import pytest

from mm_allee.data import generate_noisy_observations
from mm_allee.inference import fit_ode_least_squares
from mm_allee.models import Parameters
from mm_allee.solver import solve_trajectory


def test_conventional_baseline_clean_recovery_model_a():
    """Verify that SciPy least-squares accurately recovers parameters on clean synthetic data."""
    r_true, K_true, A_true, H_true = 0.7, 100.0, 20.0, 10.0
    p = Parameters(r=r_true, K=K_true, A=A_true, H=H_true)
    d = p.dimensionless()

    sol = solve_trajectory(
        "A", a=d["a"], harvest=d["q"], x0=45.0 / K_true, tau_end=p.r * 8.0, n_points=101
    )
    times = sol.tau / p.r
    pops = sol.x * p.K

    obs = generate_noisy_observations(
        times, pops, trajectory_id="a_clean_test", model="A", noise_sigma=0.0, noise_seed=11
    )

    known_conditions = {"known_K": 100.0, "known_initial_population": 45.0}
    fit_params = ["r", "A", "H"]
    initial_guess = {"r": 0.5, "A": 30.0, "H": 5.0}

    res = fit_ode_least_squares(
        "A",
        observations=obs,
        known_conditions=known_conditions,
        fit_params=fit_params,
        initial_guess=initial_guess,
        max_nfev=300,
    )

    assert res.success
    assert res.status == "converged"
    assert res.estimated_parameters["r"] == pytest.approx(r_true, rel=0.05)
    assert res.estimated_parameters["A"] == pytest.approx(A_true, rel=0.05)
    assert res.estimated_parameters["H"] == pytest.approx(H_true, rel=0.05)

    # Test error metrics on held-out test split
    assert res.test_metrics["rmse"] < 1.0


def test_conventional_baseline_noisy_data_model_b():
    """Verify baseline behavior under 1% measurement noise on Model B."""
    r_true, K_true, A_true, h_true = 0.7, 100.0, 20.0, 0.21
    p = Parameters(r=r_true, K=K_true, A=A_true, h=h_true)
    d = p.dimensionless()

    sol = solve_trajectory(
        "B", a=d["a"], harvest=d["e"], x0=45.0 / K_true, tau_end=p.r * 8.0, n_points=101
    )
    times = sol.tau / p.r
    pops = sol.x * p.K

    obs = generate_noisy_observations(
        times, pops, trajectory_id="b_noise_test", model="B", noise_sigma=0.01, noise_seed=22
    )

    known_conditions = {"known_K": 100.0, "known_initial_population": 45.0}
    res = fit_ode_least_squares(
        "B",
        observations=obs,
        known_conditions=known_conditions,
        fit_params=["r", "A", "h"],
        initial_guess={"r": 0.9, "A": 15.0, "h": 0.1},
        max_nfev=300,
    )

    assert res.success
    assert res.wall_seconds > 0
    # Parameters recovered within reasonable range under noise
    assert abs(res.estimated_parameters["r"] - r_true) / r_true < 0.2
    assert abs(res.estimated_parameters["A"] - A_true) / A_true < 0.2
    assert abs(res.estimated_parameters["h"] - h_true) / h_true < 0.2
