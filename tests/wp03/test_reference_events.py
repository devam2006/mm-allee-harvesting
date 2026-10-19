import numpy as np
import pytest
from scipy.integrate import quad

from mm_allee.models import growth
from mm_allee.solver import solve_trajectory


def test_supercritical_a_event_matches_independent_quadrature():
    a, q, x0 = 0.2, 1.0, 0.8
    solution = solve_trajectory("A", a=a, harvest=q, x0=x0, tau_end=20)
    reference = quad(lambda x: 1 / (q - growth(x, a)), 0, x0, epsabs=1e-12)[0]
    assert solution.extinction_tau == pytest.approx(reference, abs=1e-7)
    assert solution.tau[-1] == solution.extinction_tau
    assert solution.x[-1] == 0
    assert np.all(solution.x >= 0)
    assert np.all(np.diff(solution.tau) > 0)


@pytest.mark.parametrize("model,harvest", [("A", 0.0), ("B", 0.1)])
def test_asymptotic_decline_is_not_finite_extinction(model, harvest):
    solution = solve_trajectory(model, a=0.2, harvest=harvest, x0=0.1, tau_end=10)
    assert solution.extinction_tau is None
    assert 0 < solution.x[-1] < solution.x[0]


def test_initial_zero_a_uses_explicit_stop_policy():
    solution = solve_trajectory("A", a=0.2, harvest=0.1, x0=0, tau_end=10)
    assert solution.extinction_tau == 0
    assert solution.boundary_policy == "stop_at_zero"
    assert solution.tau.size == 1


@pytest.mark.parametrize("kwargs", [dict(x0=-1), dict(tau_end=0), dict(n_points=1), dict(atol=0)])
def test_bad_solver_inputs_fail(kwargs):
    values = dict(a=0.2, harvest=0.1, x0=0.8, tau_end=5)
    values.update(kwargs)
    with pytest.raises(ValueError):
        solve_trajectory("A", **values)
