import numpy as np
import pytest

from mm_allee.solver import solve_trajectory


@pytest.mark.parametrize("initial", [0.2, 1.5])
def test_irregular_samples_match_exact_logistic_solution(initial):
    times = np.array([0, 0.01, 0.17, 0.5, 1, 2, 4])
    actual = solve_trajectory("logistic", a=0.2, harvest=0, x0=initial, tau_end=4, tau_eval=times)
    exact = 1 / (1 + (1 / initial - 1) * np.exp(-times))
    np.testing.assert_array_equal(actual.tau, times)
    np.testing.assert_allclose(actual.x, exact, rtol=2e-9, atol=2e-11)


def test_custom_grid_removes_post_event_samples_and_appends_event():
    actual = solve_trajectory("A", a=0.2, harvest=1, x0=0.8, tau_end=5, tau_eval=[0, 0.5, 2, 5])
    np.testing.assert_array_equal(actual.tau[:2], [0, 0.5])
    assert len(actual.tau) == 3
    assert 0.5 < actual.extinction_tau < 2
    assert actual.tau[-1] == actual.extinction_tau
    assert actual.x[-1] == 0
    assert np.all(actual.x >= 0)


@pytest.mark.parametrize("model,control", [("A", 0), ("B", 0.3)])
def test_zero_equilibrium_respects_requested_grid(model, control):
    actual = solve_trajectory(model, a=0.2, harvest=control, x0=0, tau_end=5, tau_eval=[0, 0.3, 1])
    np.testing.assert_array_equal(actual.tau, [0, 0.3, 1])
    np.testing.assert_array_equal(actual.x, [0, 0, 0])
    assert actual.extinction_tau is None


@pytest.mark.parametrize(
    "grid",
    [
        [],
        [0.1, 1],
        [-0.1, 0],
        [0, 0],
        [0, 2, 1],
        [0, float("nan")],
        [0, float("inf")],
        [0, 6],
        [[0, 1]],
    ],
)
def test_invalid_sampling_grids_are_rejected(grid):
    with pytest.raises(ValueError):
        solve_trajectory("A", a=0.2, harvest=0.1, x0=0.8, tau_end=5, tau_eval=grid)


@pytest.mark.parametrize("model,initial", [("A", 1.0), ("B", 0.2), ("B", 1.0)])
def test_unharvested_exact_equilibria_remain_constant(model, initial):
    actual = solve_trajectory(model, a=0.2, harvest=0, x0=initial, tau_end=5)
    np.testing.assert_allclose(actual.x, initial, rtol=0, atol=1e-12)
    assert actual.extinction_tau is None
