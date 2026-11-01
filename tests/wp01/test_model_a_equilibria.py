"""Model A equilibria: dx/dtau = G(x) - q, G(x) = x(1-x)(x/a-1).

Independent checks used here:
* fold location and q_c from bounded numerical maximisation of G (not the formula),
* all cubic roots from NumPy's companion-matrix solver (not Brent bracketing),
* residuals via ``models.rhs`` and derivatives via central finite differences,
* hand values at a=0.2 computed separately from the implementation.
"""

import numpy as np
import pytest
from scipy.optimize import minimize_scalar

from mm_allee.equilibria import (
    FOLD_RTOL,
    classify_equilibrium,
    equilibria_a,
    extinction_boundary,
    fold_a,
    growth_derivative,
)
from mm_allee.models import growth, rhs

A_VALUES = [0.05, 0.2, 0.35, 0.5, 0.8]
RESIDUAL_TOL = 1e-12  # f is O(1/a) at most here; a few hundred ulps of headroom


def cubic_roots(a, q):
    """All real roots of -x^3/a + (1+a)x^2/a - x - q via eigenvalues (independent)."""
    roots = np.roots([-1 / a, (1 + a) / a, -1.0, -q])
    return np.sort(roots.real[np.abs(roots.imag) < 1e-7])


@pytest.mark.parametrize("a", A_VALUES)
def test_fold_matches_independent_bounded_maximisation(a):
    x_star, q_c = fold_a(a)
    best = minimize_scalar(
        lambda x: -growth(x, a), bounds=(a, 1), method="bounded", options={"xatol": 1e-12}
    )
    assert x_star == pytest.approx(best.x, abs=1e-6)  # maximiser is flat: x error ~ sqrt
    assert q_c == pytest.approx(-best.fun, rel=1e-12)
    assert a < x_star < 1
    # At the fold both f and f' vanish.
    assert abs(rhs(x_star, "A", a=a, harvest=q_c)) < 1e-14
    assert abs(growth_derivative(x_star, a)) < 1e-13


def test_hand_values_at_a_0_2():
    x_star, q_c = fold_a(0.2)
    assert x_star == pytest.approx((1.2 + np.sqrt(0.84)) / 3, rel=1e-15)
    assert q_c == pytest.approx(0.525138043, abs=1e-9)


@pytest.mark.parametrize("a", A_VALUES)
def test_derivative_matches_finite_difference(a):
    xs = np.linspace(-0.3, 1.3, 17)
    h = 1e-6
    fd = (growth(xs + h, a) - growth(xs - h, a)) / (2 * h)
    np.testing.assert_allclose(growth_derivative(xs, a), fd, rtol=1e-7, atol=1e-6)


@pytest.mark.parametrize("a", A_VALUES)
def test_zero_harvest_roots_and_signs(a):
    zero, thr, cap = equilibria_a(a, 0.0)
    assert (zero.x, thr.x, cap.x) == (0.0, a, 1.0)
    assert [r.stability for r in (zero, thr, cap)] == ["stable", "unstable", "stable"]
    # Linearisation: f'(0)=-1, f'(a)=1-a, f'(1)=(a-1)/a (derived in the report).
    assert zero.derivative == pytest.approx(-1.0)
    assert thr.derivative == pytest.approx(1 - a)
    assert cap.derivative == pytest.approx((a - 1) / a)
    assert all(r.residual == 0.0 for r in (zero, thr, cap))


@pytest.mark.parametrize("a", A_VALUES)
@pytest.mark.parametrize("fraction", [0.01, 0.25, 0.5, 0.9, 0.999])
def test_two_positive_roots_below_fold(a, fraction):
    x_star, q_c = fold_a(a)
    q = fraction * q_c
    records = equilibria_a(a, q, include_excluded=True)
    physical = [r for r in records if r.physical]
    excluded = [r for r in records if not r.physical]
    assert len(physical) == 2 and len(excluded) == 1
    lower, upper = physical
    assert a < lower.x < x_star < upper.x < 1
    assert (lower.stability, upper.stability) == ("unstable", "stable")
    assert lower.derivative > 0 > upper.derivative
    np.testing.assert_allclose([r.x for r in records], cubic_roots(a, q), rtol=1e-8, atol=1e-10)
    for rec in records:
        assert abs(rhs(rec.x, "A", a=a, harvest=q)) < RESIDUAL_TOL
    assert excluded[0].x < 0 and excluded[0].stability == "excluded"


@pytest.mark.parametrize("a", A_VALUES)
def test_single_semistable_double_root_at_fold(a):
    x_star, q_c = fold_a(a)
    (rec,) = equilibria_a(a, q_c)
    assert rec.multiplicity == 2 and rec.x == x_star
    assert abs(rec.derivative) < 1e-12  # inconclusive linearisation
    assert (rec.left_sign, rec.right_sign) == (-1, -1)
    assert rec.stability == "semistable" and rec.attracts_from == "above"


@pytest.mark.parametrize("a", A_VALUES)
@pytest.mark.parametrize("excess", [1e-9, 1e-3, 0.5])
def test_no_physical_root_above_fold(a, excess):
    _, q_c = fold_a(a)
    q = q_c * (1 + excess)
    assert equilibria_a(a, q) == []
    records = equilibria_a(a, q, include_excluded=True)
    assert len(records) == 1 and records[0].x < 0 and not records[0].physical
    grid = np.linspace(0, 1.2, 4001)
    assert np.all(rhs(grid, "A", a=a, harvest=q) < 0)


def test_negative_root_is_never_physical():
    for a in A_VALUES:
        _, q_c = fold_a(a)
        for q in np.linspace(1e-6, 1.5 * q_c, 25):
            for rec in equilibria_a(a, float(q)):
                assert rec.x > 0 and rec.physical
            # q > 0: zero is the extinction boundary, not an equilibrium.
            assert all(rec.x != 0 for rec in equilibria_a(a, float(q)))


def test_close_roots_near_fold_are_both_retained():
    a = 0.2
    x_star, q_c = fold_a(a)
    for gap in [1e-4, 1e-7, 1e-10]:
        q = q_c - gap
        lower, upper = equilibria_a(a, q)
        # Local quadratic: separation ~ 2*sqrt(2*gap/|G''(x_star)|)
        g2 = abs(-6 * x_star / a + 2 * (1 + a) / a)
        expected = 2 * np.sqrt(2 * gap / g2)
        assert upper.x - lower.x == pytest.approx(expected, rel=1e-2)
        assert (lower.stability, upper.stability) == ("unstable", "stable")
    # The integrated topology preserves distinct controls inside the old band.
    lower, upper = equilibria_a(a, q_c * (1 - 0.5 * FOLD_RTOL))
    assert lower.x < upper.x
    assert lower.multiplicity == upper.multiplicity == 1


def test_zero_boundary_description():
    assert extinction_boundary("A", 0.0)["is_equilibrium"] is True
    info = extinction_boundary("A", 0.3)
    assert info["is_equilibrium"] is False and info["rhs_at_zero"] == -0.3
    assert "stop_at_zero" in info["policy"]


def test_classify_equilibrium_lookup():
    rec = classify_equilibrium("A", 0.2, a=0.2, q=0.0)
    assert rec.stability == "unstable"
    with pytest.raises(ValueError):
        classify_equilibrium("A", 0.5, a=0.2, q=0.0)


@pytest.mark.parametrize("bad", [dict(a=0.0), dict(a=1.0), dict(a=float("nan")), dict(q=-0.1)])
def test_invalid_inputs_rejected(bad):
    args = dict(a=0.2, q=0.1)
    args.update(bad)
    with pytest.raises(ValueError):
        equilibria_a(**args)
