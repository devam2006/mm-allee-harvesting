import numpy as np
import pytest

from mm_allee.models import rhs
from mm_allee.solver import solve_trajectory


@pytest.mark.parametrize("e", [0, 0.1, 1, 5])
def test_zero_is_equilibrium_for_b(e):
    assert rhs(0.0, "B", a=0.2, harvest=e) == 0


def test_analytic_positive_b_roots_have_zero_residual():
    a, e = 0.2, 0.3
    roots = (1 + a + np.array([-1, 1]) * np.sqrt((1 - a) ** 2 - 4 * a * e)) / 2
    np.testing.assert_allclose(rhs(roots, "B", a=a, harvest=e), 0, atol=1e-14)


def test_zero_cannot_restart_without_intervention():
    solution = solve_trajectory("B", a=0.2, harvest=0, x0=0, tau_end=10)
    assert np.all(solution.x == 0)
    assert solution.extinction_tau is None
