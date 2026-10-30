"""Logistic constant-yield baseline: dx/dtau = x(1-x) - q, critical q_c = 1/4.

Independent checks: NumPy's companion-matrix polynomial roots, hand-derived values,
direct residual evaluation via ``models.rhs`` and the derivative sign 1-2x.
"""

import numpy as np
import pytest

from mm_allee.equilibria import equilibria_logistic, extinction_boundary
from mm_allee.models import rhs

RESIDUAL_TOL = 1e-13  # values of f are O(1); a few ulps of roundoff are expected


def polynomial_roots(q):
    roots = np.roots([-1.0, 1.0, -q])
    return np.sort(roots.real[np.abs(roots.imag) < 1e-12])


@pytest.mark.parametrize("q", [1e-10, 0.01, 0.1, 0.2, 0.249])
def test_two_roots_below_threshold_match_polynomial(q):
    records = equilibria_logistic(q)
    assert [r.multiplicity for r in records] == [1, 1]
    xs = np.array([r.x for r in records])
    np.testing.assert_allclose(xs, polynomial_roots(q), rtol=1e-9, atol=1e-12)
    for rec in records:
        assert abs(rhs(rec.x, "logistic", a=0.5, harvest=q)) < RESIDUAL_TOL
        assert rec.residual < RESIDUAL_TOL
        assert rec.physical and 0 < rec.x < 1
    lower, upper = records
    assert (lower.stability, upper.stability) == ("unstable", "stable")
    assert lower.derivative > 0 > upper.derivative
    # Hand formula for the derivative at the roots: f'(x_pm) = -/+ sqrt(1-4q).
    assert upper.derivative == pytest.approx(-np.sqrt(1 - 4 * q), rel=1e-9)


def test_small_root_has_no_cancellation_error():
    q = 1e-12
    lower = equilibria_logistic(q)[0]
    # Series: x_minus = q + q^2 + 2q^3 + ...
    assert lower.x == pytest.approx(q + q**2, rel=1e-12)


def test_critical_double_root_is_semistable_from_signs():
    (rec,) = equilibria_logistic(0.25)
    assert rec.x == 0.5 and rec.multiplicity == 2
    assert rec.derivative == 0.0  # derivative test is inconclusive here ...
    assert (rec.left_sign, rec.right_sign) == (-1, -1)  # ... signs decide
    assert rec.stability == "semistable" and rec.attracts_from == "above"


@pytest.mark.parametrize("q", [0.25 + 1e-9, 0.3, 1.0, 10.0])
def test_no_equilibrium_above_threshold(q):
    assert equilibria_logistic(q) == []
    grid = np.linspace(-0.5, 1.5, 2001)
    assert np.all(rhs(grid, "logistic", a=0.5, harvest=q) < 0)


def test_zero_harvest_signs():
    zero, one = equilibria_logistic(0.0)
    assert (zero.x, one.x) == (0.0, 1.0)
    # Unlike strong Allee growth, zero is unstable for logistic growth.
    assert zero.stability == "unstable" and zero.derivative == 1.0
    assert one.stability == "stable" and one.derivative == -1.0
    assert zero.left_sign is None  # x<0 is outside the physical domain


def test_zero_not_equilibrium_for_positive_harvest():
    assert all(r.x > 0 for r in equilibria_logistic(0.1))
    boundary = extinction_boundary("logistic", 0.1)
    assert boundary["is_equilibrium"] is False and boundary["rhs_at_zero"] == -0.1


@pytest.mark.parametrize("q", [-0.1, float("nan"), float("inf")])
def test_invalid_harvest_rejected(q):
    with pytest.raises(ValueError):
        equilibria_logistic(q)
