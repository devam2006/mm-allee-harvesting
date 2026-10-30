"""Identifiability proofs, counterexamples, and observation split tests for WP05."""

import numpy as np
import pytest

from mm_allee.data import (
    create_contiguous_splits,
    generate_noisy_observations,
    validate_splits,
    validate_time_windows,
)
from mm_allee.models import Parameters, dimensional_rhs
from mm_allee.solver import solve_trajectory


def test_disjoint_observation_ids():
    validate_splits(["run1:0", "run1:1"], ["run1:2"], ["run1:3"])


@pytest.mark.parametrize(
    "splits", [([1], [1], [3]), ([1, 1], [2], [3]), ([], [2], [3]), ([1], [2], [2])]
)
def test_invalid_splits_rejected(splits):
    with pytest.raises(ValueError):
        validate_splits(*splits)


def test_time_window_ordering():
    # Valid contiguous splits
    validate_time_windows([0.0, 1.0, 2.0], [2.0, 3.0], [3.0, 4.0, 5.0])

    # Overlapping or backward windows rejected
    with pytest.raises(ValueError):
        validate_time_windows([0.0, 2.5], [2.0, 3.0], [3.0, 4.0])
    with pytest.raises(ValueError):
        validate_time_windows([0.0, 1.0], [1.0, 4.5], [4.0, 5.0])
    with pytest.raises(ValueError):
        validate_time_windows([], [1.0], [2.0])


def test_contiguous_split_ratios():
    idx_train, idx_val, idx_test = create_contiguous_splits(100, 0.6, 0.2, 0.2)
    assert len(idx_train) == 60
    assert len(idx_val) == 20
    assert len(idx_test) == 20
    assert idx_train[-1] < idx_val[0]
    assert idx_val[-1] < idx_test[0]


def test_reproducible_noise_generation():
    times = np.linspace(0, 10, 50)
    pops = 45.0 + 10.0 * np.sin(times)

    obs1 = generate_noisy_observations(
        times, pops, trajectory_id="test_traj", model="A", noise_sigma=0.05, noise_seed=42
    )
    obs2 = generate_noisy_observations(
        times, pops, trajectory_id="test_traj", model="A", noise_sigma=0.05, noise_seed=42
    )
    obs3 = generate_noisy_observations(
        times, pops, trajectory_id="test_traj", model="A", noise_sigma=0.05, noise_seed=99
    )

    np.testing.assert_allclose(obs1["observed_population"], obs2["observed_population"])
    assert not np.allclose(obs1["observed_population"], obs3["observed_population"])


def test_zero_noise_observations_match_clean_reference_with_valid_splits():
    times = np.linspace(0, 8, 101)
    pops = 45.0 + 2.0 * times

    obs = generate_noisy_observations(
        times, pops, trajectory_id="test_exact", model="B", noise_sigma=0.0, noise_seed=11
    )
    np.testing.assert_allclose(obs["observed_population"], pops, atol=1e-14)
    assert len(obs["train_indices"]) + len(obs["val_indices"]) + len(obs["test_indices"]) == 101


def test_model_b_three_polynomial_combinations():
    """Verify B's RHS expansion: dN/dt = c1*N + c2*N^2 + c3*N^3.

    c1 = -(r + h)
    c2 = r * (1/A + 1/K)
    c3 = -r / (A * K)
    """
    r, A, K, h = 0.7, 20.0, 100.0, 0.21
    p = Parameters(r=r, A=A, K=K, h=h)

    c1 = -(r + h)
    c2 = r * (1.0 / A + 1.0 / K)
    c3 = -r / (A * K)

    N_grid = np.linspace(0.1, 120.0, 50)
    rhs_ode = dimensional_rhs(N_grid, "B", p)
    rhs_poly = c1 * N_grid + c2 * N_grid**2 + c3 * N_grid**3

    np.testing.assert_allclose(rhs_ode, rhs_poly, rtol=1e-12, atol=1e-14)


def test_model_b_counterexample_identical_rhs_and_trajectories():
    """Explicit counterexample in the scientific contract:

    Set 1: (r, A, K, h) = (1.0, 0.2, 1.0, 0.5)
    Set 2: (r, A, K, h) = (1.35, 0.3, 0.9, 0.15)
    Both produce c1 = -1.5, c2 = 6.0, c3 = -5.0.
    """
    p1 = Parameters(r=1.0, A=0.2, K=1.0, h=0.5)
    p2 = Parameters(r=1.35, A=0.3, K=0.9, h=0.15)
    assert p1 != p2

    # Check polynomial coefficients match exactly
    c1_1 = -(p1.r + p1.h)
    c2_1 = p1.r * (1.0 / p1.A + 1.0 / p1.K)
    c3_1 = -p1.r / (p1.A * p1.K)

    c1_2 = -(p2.r + p2.h)
    c2_2 = p2.r * (1.0 / p2.A + 1.0 / p2.K)
    c3_2 = -p2.r / (p2.A * p2.K)

    assert c1_1 == pytest.approx(-1.5)
    assert c1_2 == pytest.approx(-1.5)
    assert c2_1 == pytest.approx(6.0)
    assert c2_2 == pytest.approx(6.0)
    assert c3_1 == pytest.approx(-5.0)
    assert c3_2 == pytest.approx(-5.0)

    # Check vector field match across population range
    N = np.linspace(0, 1.2, 101)
    rhs1 = dimensional_rhs(N, "B", p1)
    rhs2 = dimensional_rhs(N, "B", p2)
    np.testing.assert_allclose(rhs1, rhs2, atol=1e-14)

    # Solve trajectories from the same initial state
    d1 = p1.dimensionless()
    d2 = p2.dimensionless()
    t_end = 4.0
    traj1 = solve_trajectory("B", a=d1["a"], harvest=d1["e"], x0=0.6 / p1.K, tau_end=p1.r * t_end, n_points=101)
    traj2 = solve_trajectory("B", a=d2["a"], harvest=d2["e"], x0=0.6 / p2.K, tau_end=p2.r * t_end, n_points=101)

    # Convert to dimensional time and population
    time1 = traj1.tau / p1.r
    pop1 = traj1.x * p1.K
    time2 = traj2.tau / p2.r
    pop2 = traj2.x * p2.K

    np.testing.assert_allclose(time1, time2, atol=1e-14)
    np.testing.assert_allclose(pop1, pop2, rtol=1e-6, atol=1e-8)


def test_multiple_initial_states_do_not_resolve_model_b_ambiguity():
    """Demonstrate that multiple initial conditions do not break Model B ambiguity

    because all solutions trace the identical ODE defined by (c1, c2, c3).
    """
    p1 = Parameters(r=1.0, A=0.2, K=1.0, h=0.5)
    p2 = Parameters(r=1.35, A=0.3, K=0.9, h=0.15)

    d1, d2 = p1.dimensionless(), p2.dimensionless()
    for n0 in [0.3, 0.5, 0.8, 1.1]:
        sol1 = solve_trajectory("B", a=d1["a"], harvest=d1["e"], x0=n0 / p1.K, tau_end=p1.r * 2.0, n_points=51)
        sol2 = solve_trajectory("B", a=d2["a"], harvest=d2["e"], x0=n0 / p2.K, tau_end=p2.r * 2.0, n_points=51)
        np.testing.assert_allclose(sol1.x * p1.K, sol2.x * p2.K, rtol=1e-6, atol=1e-8)


def test_model_a_polynomial_identifiability():
    """Model A polynomial expansion: dN/dt = c0 + c1*N + c2*N^2 + c3*N^3.

    c0 = -H
    c1 = -r
    c2 = r * (1/A + 1/K)
    c3 = -r / (A * K)
    Given 0 < A < K, all 4 parameters are algebraically identifiable.
    """
    r_true, K_true, A_true, H_true = 0.7, 100.0, 20.0, 10.0
    p = Parameters(r=r_true, K=K_true, A=A_true, H=H_true)

    c0 = -H_true
    c1 = -r_true
    c2 = r_true * (1.0 / A_true + 1.0 / K_true)
    c3 = -r_true / (A_true * K_true)

    # Algebraic inversion
    H_rec = -c0
    r_rec = -c1
    P_rec = -r_rec / c3  # A * K
    S_rec = -c2 / c3  # A + K

    # Roots of z^2 - S*z + P = 0
    discriminant = S_rec**2 - 4.0 * P_rec
    assert discriminant > 0
    root1 = (S_rec - np.sqrt(discriminant)) / 2.0
    root2 = (S_rec + np.sqrt(discriminant)) / 2.0

    # Physical ordering 0 < A < K resolves root permutation
    A_rec = root1
    K_rec = root2

    assert H_rec == pytest.approx(H_true)
    assert r_rec == pytest.approx(r_true)
    assert A_rec == pytest.approx(A_true)
    assert K_rec == pytest.approx(K_true)
