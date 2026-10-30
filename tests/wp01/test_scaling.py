"""Nondimensionalisation checks: x=N/K, tau=r t, a=A/K, q=H/(rK), e=h/r.

Independent expectations: the dimensional equations are written out by hand here
(not via ``models``), dimensionless groups are checked against hand arithmetic, and
the time scaling is checked by integrating the dimensional ODE directly with SciPy.
"""

import numpy as np
import pytest
from scipy.integrate import solve_ivp

from mm_allee.models import Parameters, dimensional_rhs, rhs
from mm_allee.solver import solve_trajectory

PARAMETER_SETS = [
    dict(r=0.7, K=150, A=30, H=3, h=0.1),
    dict(r=0.05, K=2.0e6, A=1.5e5, H=4.0e3, h=0.01),  # large population scale
    dict(r=3.0, K=1.0, A=0.6, H=0.2, h=1.2),  # fast growth, a close to 1
    dict(r=1.0, K=500, A=5, H=0.0, h=0.0),  # zero harvest, small a
]


def hand_rhs(N, model, p):
    production = p["r"] * N * (1 - N / p["K"])
    if model != "logistic":
        production = production * (N / p["A"] - 1)
    return production - (p["h"] * N if model == "B" else p["H"])


@pytest.mark.parametrize("model", ["logistic", "A", "B"])
@pytest.mark.parametrize("values", PARAMETER_SETS)
def test_dimensional_rhs_is_rK_times_dimensionless(model, values):
    p = Parameters(**values)
    d = p.dimensionless()
    N = values["K"] * np.array([0.0, 0.05, 0.1, 0.3, 0.5, 0.9, 1.0, 1.2])
    u = d["e"] if model == "B" else d["q"]
    expected = hand_rhs(N, model, values)
    scale = values["r"] * values["K"]
    # Relative tolerance: values span many orders of magnitude across parameter sets.
    tol = 1e-12 * scale
    np.testing.assert_allclose(dimensional_rhs(N, model, p), expected, rtol=1e-12, atol=tol)
    np.testing.assert_allclose(
        scale * rhs(N / p.K, model, a=d["a"], harvest=u), expected, rtol=1e-12, atol=tol
    )


def test_dimensionless_groups_match_hand_arithmetic():
    p = Parameters(r=0.5, K=200, A=40, H=5, h=0.1)
    d = p.dimensionless()
    assert d["a"] == pytest.approx(0.2)
    assert d["q"] == pytest.approx(5 / (0.5 * 200))  # 0.05
    assert d["e"] == pytest.approx(0.2)


@pytest.mark.parametrize(
    "kwargs",
    [
        dict(r=0),
        dict(r=-1),
        dict(K=0),
        dict(K=-5),
        dict(A=0),
        dict(A=100),  # A == K
        dict(A=150),  # A > K
        dict(H=-1),
        dict(h=-1),
        dict(r=float("nan")),
        dict(K=float("inf")),
        dict(H=float("nan")),
    ],
)
def test_invalid_parameters(kwargs):
    values = dict(r=1, K=100, A=20)
    values.update(kwargs)
    with pytest.raises(ValueError):
        Parameters(**values)


@pytest.mark.parametrize("bad", [dict(a=0), dict(a=1), dict(a=1.5), dict(harvest=-0.1)])
def test_invalid_dimensionless_inputs(bad):
    args = dict(a=0.2, harvest=0.1)
    args.update(bad)
    with pytest.raises(ValueError):
        rhs(0.5, "A", **args)


def test_model_a_zero_is_not_equilibrium_with_harvest():
    assert rhs(0.0, "A", a=0.2, harvest=0.1) == -0.1


@pytest.mark.parametrize("model,control", [("A", 0.3), ("logistic", 0.1), ("B", 0.2)])
def test_time_scaling_matches_direct_dimensional_integration(model, control):
    """N(t) from the dimensional ODE equals K*x(tau=r t) from the scaled solver."""
    r, K, A = 0.4, 1000.0, 200.0
    H = control * r * K if model != "B" else 0.0
    h = control * r if model == "B" else 0.0
    p = dict(r=r, K=K, A=A, H=H, h=h)
    N0 = 0.85 * K
    t_end = 15.0
    t_eval = np.linspace(0, t_end, 31)
    direct = solve_ivp(
        lambda t, y: [hand_rhs(y[0], model, p)],
        (0, t_end),
        [N0],
        method="DOP853",
        t_eval=t_eval,
        rtol=1e-11,
        atol=1e-9,
    )
    scaled = solve_trajectory(
        model, a=A / K, harvest=control, x0=N0 / K, tau_end=r * t_end, n_points=31
    )
    assert scaled.extinction_tau is None  # this start persists in all three models
    # Different integrators at tolerances ~1e-9: agreement to 1e-6 of K is ample.
    np.testing.assert_allclose(scaled.tau / r, t_eval, rtol=0, atol=1e-12)
    np.testing.assert_allclose(K * scaled.x, direct.y[0], rtol=0, atol=1e-6 * K)
