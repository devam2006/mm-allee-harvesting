import numpy as np
import pytest

from mm_allee.models import Parameters, dimensional_rhs, rhs


@pytest.mark.parametrize("model", ["logistic", "A", "B"])
def test_dimensional_chain_rule(model):
    p = Parameters(r=0.7, K=150, A=30, H=3, h=0.1)
    d = p.dimensionless()
    N = np.array([0.0, 15, 30, 90, 150, 180])
    u = d["e"] if model == "B" else d["q"]
    production = p.r * N * (1 - N / p.K)
    if model != "logistic":
        production = production * (N / p.A - 1)
    expected = production - (p.h * N if model == "B" else p.H)
    np.testing.assert_allclose(dimensional_rhs(N, model, p), expected, atol=1e-12)
    np.testing.assert_allclose(
        p.r * p.K * rhs(N / p.K, model, a=d["a"], harvest=u), expected, atol=1e-12
    )


@pytest.mark.parametrize(
    "kwargs",
    [dict(r=0), dict(K=0), dict(A=0), dict(A=100), dict(H=-1), dict(h=-1), dict(r=float("nan"))],
)
def test_invalid_parameters(kwargs):
    values = dict(r=1, K=100, A=20)
    values.update(kwargs)
    with pytest.raises(ValueError):
        Parameters(**values)


def test_model_a_zero_is_not_equilibrium_with_harvest():
    assert rhs(0.0, "A", a=0.2, harvest=0.1) == -0.1
