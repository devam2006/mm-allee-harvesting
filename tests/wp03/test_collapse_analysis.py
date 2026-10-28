from decimal import Decimal, localcontext
from math import fsum, pi, sqrt

import numpy as np
import pytest
from numpy.polynomial import Polynomial
from scipy.integrate import quad, solve_ivp
from scipy.optimize import minimize_scalar

from mm_allee.collapse import (
    classify_basin,
    extinction_time_a,
    positive_branches,
    safety_margins,
)
from mm_allee.models import Parameters, growth
from mm_allee.solver import solve_trajectory
from mm_allee.thresholds import (
    critical_a,
    critical_b,
    dimensional_thresholds,
    maximum_yields,
    parameters_with,
    sustainable_yield_b,
    threshold_sensitivity,
)


@pytest.mark.parametrize("a", [0.01, 0.05, 0.2, 0.5, 0.8, 0.95])
def test_thresholds_match_independent_bounded_maxima(a):
    production = Polynomial([0, -1, (1 + a) / a, -1 / a])
    per_capita = Polynomial([-1, (1 + a) / a, -1 / a])
    x, qc = critical_a(a)
    numeric = minimize_scalar(lambda z: -production(z), bounds=(a, 1), method="bounded")
    numeric_b = minimize_scalar(lambda z: -per_capita(z), bounds=(a, 1), method="bounded")
    assert a < x < 1
    assert qc == pytest.approx(-numeric.fun, rel=2e-9, abs=1e-13)
    assert critical_b(a) == pytest.approx(-numeric_b.fun, rel=2e-9, abs=1e-13)
    assert abs(production.deriv()(x)) < 1e-12
    assert abs(production(x) - qc) < 1e-12
    assert production.deriv(2)(x) < 0
    assert per_capita((1 + a) / 2) == pytest.approx(critical_b(a), abs=1e-12)


@pytest.mark.parametrize("model", ["A", "B"])
def test_adjacent_controls_are_not_silently_merged_into_fold(model):
    a = 0.2
    critical = critical_a(a)[1] if model == "A" else critical_b(a)
    lower = positive_branches(model, a=a, harvest=np.nextafter(critical, 0))
    fold = positive_branches(model, a=a, harvest=critical)
    assert lower[0] < lower[1]
    assert fold[0] == fold[1]
    assert positive_branches(model, a=a, harvest=np.nextafter(critical, np.inf)) is None
    for x in lower:
        residual = growth(x, a) - (critical if model == "A" else critical * x)
        assert abs(residual) < 2e-14


@pytest.mark.parametrize("model", ["A", "B"])
@pytest.mark.parametrize("fraction", [0, 0.6, 1, 1.3])
def test_all_basin_regimes_and_exact_initial_roots(model, fraction):
    a = 0.2
    c = critical_a(a)[1] if model == "A" else critical_b(a)
    control = c * fraction
    roots = positive_branches(model, a=a, harvest=control)
    zero = classify_basin(model, a=a, harvest=control, x0=0)
    assert zero.outcome == ("initial_extinction" if model == "A" and control else "equilibrium")
    if roots is None:
        expected = "finite_extinction" if model == "A" else "asymptotic_extinction"
        assert classify_basin(model, a=a, harvest=control, x0=1.4).outcome == expected
        return
    low, high = roots
    exact = classify_basin(model, a=a, harvest=control, x0=low)
    assert exact.outcome == "equilibrium"
    assert exact.equilibrium_type == ("semistable" if fraction == 1 else "unstable")
    assert classify_basin(model, a=a, harvest=control, x0=high).outcome == "equilibrium"
    below = classify_basin(model, a=a, harvest=control, x0=low / 2)
    assert below.outcome == (
        "finite_extinction" if model == "A" and control else "asymptotic_extinction"
    )
    above = classify_basin(model, a=a, harvest=control, x0=1.4)
    assert above.outcome == "persistence"
    assert above.limiting_x == high
    assert (
        classify_basin(model, a=a, harvest=control, x0=low + 1e-13).outcome == "boundary_unresolved"
    )


@pytest.mark.parametrize("model", ["A", "B"])
@pytest.mark.parametrize("fraction", [0, 0.7, 1, 1.2])
def test_basin_labels_agree_with_independent_polynomial_dynamics(model, fraction):
    a = 0.2
    control = fraction * (critical_a(a)[1] if model == "A" else critical_b(a))
    polynomial = Polynomial(
        [-control if model == "A" else 0, -1 if model == "A" else -1 - control, (1 + a) / a, -1 / a]
    )

    def zero(t, y):
        return y[0]

    zero.terminal, zero.direction = True, -1
    boundary = positive_branches(model, a=a, harvest=control)
    initial_values = [0.1, 1.2] if boundary is None else [boundary[0] / 2, 1.2]
    for initial in initial_values:
        label = classify_basin(model, a=a, harvest=control, x0=initial)
        horizon = 40 if label.outcome == "asymptotic_extinction" else 250
        solution = solve_ivp(
            lambda t, y: polynomial(y),
            (0, horizon),
            [initial],
            method="DOP853",
            rtol=1e-11,
            atol=1e-13,
            max_step=0.5,
            events=zero if model == "A" and control else None,
        )
        assert solution.success
        if label.outcome == "finite_extinction":
            assert len(solution.t_events[0]) == 1
        elif label.outcome == "asymptotic_extinction":
            assert 0 < solution.y[0, -1] < 1e-8
        elif fraction == 1:
            # At the fold, attraction is algebraic, not exponential. Check
            # side/monotonic direction rather than pretending 250 is infinity.
            assert label.limiting_x < solution.y[0, -1] < initial
            assert abs(solution.y[0, -1] - label.limiting_x) < 0.005
        else:
            assert solution.y[0, -1] == pytest.approx(label.limiting_x, abs=2e-9)


@pytest.mark.parametrize("a", [0.05, 0.2, 0.5, 0.8])
@pytest.mark.parametrize("fraction", [0.25, 1, 1.01, 1.3])
def test_extinction_quadrature_matches_two_rk45_tolerances_and_independent_dop853(a, fraction):
    star, qc = critical_a(a)
    q = fraction * qc
    initial = (
        (a + positive_branches("A", a=a, harvest=q)[0]) / 2
        if fraction < 1
        else 0.4 * star
        if fraction == 1
        else 1.1
    )
    result = extinction_time_a(a=a, q=q, x0=initial)
    assert result.basin.outcome == "finite_extinction"
    assert result.tau_ext > 0
    horizon = result.tau_ext * 1.1 + 1
    events = []
    for tolerance in (1e-8, 1e-10):
        solution = solve_trajectory(
            "A",
            a=a,
            harvest=q,
            x0=initial,
            tau_end=horizon,
            rtol=tolerance,
            atol=tolerance / 100,
            max_step=0.2,
        )
        assert solution.extinction_tau is not None
        events.append(solution.extinction_tau)
        assert solution.extinction_tau == pytest.approx(result.tau_ext, rel=5e-7, abs=2e-7)
        assert np.all(solution.x >= 0)
        assert solution.x[-1] == 0
    assert abs(events[1] - events[0]) < 5e-7 * max(1, result.tau_ext)
    polynomial = Polynomial([-q, -1, (1 + a) / a, -1 / a])

    def zero(t, y):
        return y[0]

    zero.terminal, zero.direction = True, -1
    independent = solve_ivp(
        lambda t, y: polynomial(y),
        (0, horizon),
        [initial],
        method="DOP853",
        rtol=1e-12,
        atol=1e-14,
        events=zero,
        max_step=0.2,
    )
    assert independent.success
    assert independent.t_events[0][0] == pytest.approx(result.tau_ext, rel=2e-9, abs=2e-9)


def test_no_quadrature_is_attempted_through_equilibria_or_on_nonfinite_paths(monkeypatch):
    import mm_allee.collapse as collapse

    def prohibited(*args, **kwargs):
        raise AssertionError("Quadrature must not be called")

    monkeypatch.setattr(collapse, "quad", prohibited)
    star, qc = critical_a(0.2)
    for q, initial in [(0, 0.1), (0, 0.8), (qc, star), (qc, 1.2), (0.5 * qc, 0.95)]:
        assert extinction_time_a(a=0.2, q=q, x0=initial).tau_ext is None
    assert extinction_time_a(a=0.2, q=qc, x0=0).tau_ext == 0


@pytest.mark.parametrize("a", [0.1, 0.2, 0.5])
def test_bottleneck_inverse_square_root_asymptotic(a):
    star, qc = critical_a(a)
    beta = 3 * star / a - (1 + a) / a
    target = pi / sqrt(beta)
    scaled = []
    for fraction in [1e-3, 1e-4, 1e-5]:
        q = qc * (1 + fraction)
        result = extinction_time_a(a=a, q=q, x0=1.1)
        assert result.method == "bottleneck_tangent_quad"
        scaled.append(result.tau_ext * sqrt(q - qc))
    assert abs(scaled[-1] - target) < abs(scaled[0] - target)
    assert scaled[-1] == pytest.approx(target, rel=0.01)


@pytest.mark.parametrize("values", [(0.7, 100, 20), (0.05, 3, 0.6), (3, 10000, 8000)])
def test_dimensional_sensitivity_matches_central_differences_and_homogeneity(values):
    p = Parameters(*values)
    rows = threshold_sensitivity(p)
    for row in rows:
        key, name = row["parameter"], row["threshold"]
        step = getattr(p, key) * 1e-5
        plus = dimensional_thresholds(parameters_with(p, **{key: getattr(p, key) + step}))[name]
        minus = dimensional_thresholds(parameters_with(p, **{key: getattr(p, key) - step}))[name]
        assert row["partial"] == pytest.approx((plus - minus) / (2 * step), rel=2e-7, abs=1e-9)
    elasticities = {(r["threshold"], r["parameter"]): r["elasticity"] for r in rows}
    assert elasticities["H_c", "K"] + elasticities["H_c", "A"] == pytest.approx(1)
    assert elasticities["h_c", "K"] + elasticities["h_c", "A"] == pytest.approx(0, abs=1e-12)


@pytest.mark.parametrize("a", [0.05, 0.2, 0.5, 0.8])
def test_b_msy_is_interior_maximum_yield_not_maximum_effort(a):
    p = Parameters(0.7, 100, a * 100)
    result = maximum_yields(p)
    numeric = minimize_scalar(
        lambda e: -sustainable_yield_b(a, e)[1],
        bounds=(0, critical_b(a)),
        method="bounded",
        options={"xatol": 1e-14},
    )
    assert result["h_MSY"] / p.r == pytest.approx(numeric.x, rel=5e-5)
    assert result["Y_MSY_B"] == pytest.approx(-numeric.fun * p.r * p.K, rel=1e-8)
    assert 0 < result["h_MSY"] < result["h_c"]
    assert result["B_effort_margin_at_MSY"] > 0
    assert sustainable_yield_b(a, critical_b(a) * 1.01) is None
    margins = safety_margins("B", parameters_with(p, h=result["h_MSY"]), 0.99 * p.K)
    assert margins["population_margin"] > 0
    assert margins["outcome"] == "persistence"


@pytest.mark.parametrize("value", [-1, 0, 1, 2, float("nan"), float("inf"), True, None, "bad"])
def test_invalid_allee_ratios_are_rejected(value):
    with pytest.raises(ValueError):
        critical_a(value)
    with pytest.raises(ValueError):
        critical_b(value)


@pytest.mark.parametrize("updates", [dict(q=-1), dict(x0=-1), dict(epsabs=0), dict(root_tol=-1)])
def test_invalid_extinction_inputs(updates):
    with pytest.raises(ValueError):
        extinction_time_a(**(dict(a=0.2, q=1, x0=0.8) | updates))


def test_extinction_monotonicity_and_supercritical_upper_bound():
    a = 0.2
    qc = critical_a(a)[1]
    times = [extinction_time_a(a=a, q=1.2 * qc, x0=x).tau_ext for x in (0.1, 0.6, 1.2)]
    assert times[0] < times[1] < times[2]
    assert times[-1] <= 1.2 / (0.2 * qc)
    catches = [extinction_time_a(a=a, q=f * qc, x0=1.1).tau_ext for f in (1.01, 1.1, 1.5)]
    assert catches[0] > catches[1] > catches[2]
    lower = positive_branches("A", a=a, harvest=0.5 * qc)[0]
    near = [extinction_time_a(a=a, q=0.5 * qc, x0=f * lower).tau_ext for f in (0.9, 0.99, 0.999)]
    assert near[0] < near[1] < near[2]


def test_dimensional_thresholds_rescale_with_units_and_logistic_hand_calculation():
    p = Parameters(2, 8, 1)
    original = dimensional_thresholds(p)
    assert original["H_c_logistic"] == 4
    scaled = dimensional_thresholds(Parameters(2 * p.r, 3 * p.K, 3 * p.A))
    for key, factor in (("N_star", 3), ("H_c", 6), ("h_c", 2), ("H_c_logistic", 6)):
        assert scaled[key] == pytest.approx(factor * original[key])


@pytest.mark.parametrize("a", [0.05, 0.2, 0.8, 0.999999])
@pytest.mark.parametrize("fraction", [1e-20, 1e-16, 1e-12])
def test_small_positive_catch_preserves_brackets_and_reaching_zero_paths(a, fraction):
    q = fraction * critical_a(a)[1]
    lower, upper = positive_branches("A", a=a, harvest=q)
    assert a <= lower < upper <= 1  # endpoint rounding can be unavoidable.
    result = extinction_time_a(a=a, q=q, x0=a / 2)
    assert result.basin.outcome == "finite_extinction"
    # Independent expansion on a path strictly below a, with no equilibrium.
    expected = quad(
        lambda x: 1 / (q + x - (1 + a) * x**2 / a + x**3 / a),
        0,
        a / 2,
        epsabs=1e-9,
        epsrel=1e-10,
        limit=250,
    )[0]
    assert result.tau_ext == pytest.approx(expected, rel=2e-10)


def test_rounded_endpoint_roots_are_not_called_exact_positive_catch_equilibria():
    a = 0.2
    q = 1e-20 * critical_a(a)[1]
    assert classify_basin("A", a=a, harvest=q, x0=a).outcome == "boundary_unresolved"
    assert classify_basin("A", a=a, harvest=q, x0=1).outcome == "persistence"


@pytest.mark.parametrize("distance", [1e-6, 1e-8, 1e-10])
def test_close_below_fold_time_matches_independent_rescaled_rational_integral(distance):
    # a=3/8 has an EXACT representable fold (x*=3/4,qc=3/16).
    # Independently factor q-G(x)=(x-3/4)^2*(x+1/8)/(3/8).
    # z=1/(3/4-x) gives integrand (3/8)/(7/8-1/z). Geometric
    # subintervals resolve its full range without using the production formula.
    initial = 0.75 - distance
    start, stop = 1 / 0.75, 1 / (0.75 - initial)
    pieces = []
    while start < stop:
        end = min(2 * start, stop)
        pieces.append(quad(lambda z: 0.375 / (0.875 - 1 / z), start, end, epsrel=1e-12)[0])
        start = end
    result = extinction_time_a(a=0.375, q=0.1875, x0=initial)
    assert result.method == "fold_closed_form"
    assert result.quadrature_error is None  # never invent a quadrature error estimate.
    assert result.tau_ext == pytest.approx(fsum(pieces), rel=2e-14)
    assert result.tau_ext * (0.75 - initial) == pytest.approx(3 / 7, rel=2e-5)


@pytest.mark.parametrize("distance", [1e-6, 1e-8, 1e-10])
def test_subcritical_near_boundary_integral_matches_high_precision_polynomial(distance):
    a, q = 0.2, 0.5 * critical_a(0.2)[1]
    lower = positive_branches("A", a=a, harvest=q)[0]
    initial = lower - distance
    with localcontext() as context:
        context.prec = 75
        ad, qd, xd = map(Decimal.from_float, (a, q, initial))
        star = (1 + ad + (1 - ad + ad * ad).sqrt()) / 3

        def polynomial(x):
            return -(x**3) / ad + (1 + ad) * x**2 / ad - x - qd

        def root(left, right):
            left_sign = polynomial(left) < 0
            for _ in range(260):
                middle = (left + right) / 2
                if (polynomial(middle) < 0) == left_sign:
                    left = middle
                else:
                    right = middle
            return (left + right) / 2

        low, high = root(ad, star), root(star, Decimal(1))
        negative = -ad * qd / (low * high)
        roots = [negative, low, high]
        expected = Decimal(0)
        for i, value in enumerate(roots):
            others = [r for j, r in enumerate(roots) if j != i]
            coefficient = ad / ((value - others[0]) * (value - others[1]))
            expected += coefficient * abs((xd - value) / (-value)).ln()
    result = extinction_time_a(a=a, q=q, x0=initial)
    assert result.method == "boundary_log_quad"
    # Root rounding is amplified close to the basin boundary. This tolerance
    # covers that conditioning, separately from QUADPACK's integration estimate.
    assert result.tau_ext == pytest.approx(float(expected), abs=2e-6, rel=2e-9)
