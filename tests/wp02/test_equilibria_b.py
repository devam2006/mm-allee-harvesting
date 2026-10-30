from decimal import Decimal, localcontext

import numpy as np
import pytest
from scipy.optimize import minimize_scalar

from mm_allee.model_b import critical_effort, equilibria_b
from mm_allee.models import rhs
from mm_allee.solver import solve_trajectory


@pytest.mark.parametrize("a", [1e-6, 0.1, 0.2, 0.8, 0.999999])
def test_discriminant_regimes_and_independent_polynomial(a):
    ec = critical_effort(a)
    assert [r.x for r in equilibria_b(a, 0)] == [0, a, 1]
    for fraction in [0.1, 0.5, 0.999]:
        e = fraction * ec
        roots = equilibria_b(a, e)
        # High-precision expanded polynomial avoids cancellation in a double-precision oracle.
        with localcontext() as ctx:
            ctx.prec = 60
            da, de = Decimal(a), Decimal(e)
            discriminant = (1 + da) ** 2 - 4 * da * (1 + de)
            expected = [float((1 + da + sign * discriminant.sqrt()) / 2) for sign in [-1, 1]]
        np.testing.assert_allclose([r.x for r in roots[1:]], expected, atol=2e-14, rtol=2e-14)
        for root in roots:
            assert root.residual < 1e-9 * max(1, e)
        assert [r.stability for r in roots] == ["stable", "unstable", "stable"]
    assert len(equilibria_b(a, 2 * ec)) == 1
    fold = equilibria_b(a, ec)[1]
    assert fold.multiplicity == 2 and fold.attracts_from == "above"
    assert fold.left_sign == fold.right_sign == -1
    # Fixed absolute fold tolerances must not erase the near-a=1 topology.
    assert len(equilibria_b(a, 0.5 * ec)) == 3


def test_threshold_by_independent_maximisation():
    for a in [0.1, 0.2, 0.8]:
        result = minimize_scalar(lambda x: -(1 - x) * (x / a - 1), bounds=(a, 1), method="bounded")
        assert critical_effort(a) == pytest.approx(-result.fun, rel=1e-12)


def test_phase_signs_and_perturbed_trajectories():
    for e in [0, 0.4, critical_effort(0.2)]:
        for root in equilibria_b(0.2, e):
            for side, expected in [(1, root.right_sign), (-1, root.left_sign)]:
                if expected is None:
                    continue
                start = root.x + side * 0.005
                assert np.sign(rhs(start, "B", a=0.2, harvest=e)) == expected
                sol = solve_trajectory("B", a=0.2, harvest=e, x0=start, tau_end=0.2)
                assert np.sign(sol.x[-1] - start) == expected
    zero = equilibria_b(0.2, 1.5)[0]
    assert zero.derivative == -2.5
    # Central difference from the shared RHS independently checks the linearisation.
    eps = 1e-6
    deriv = (rhs(eps, "B", a=0.2, harvest=1.5) - rhs(-eps, "B", a=0.2, harvest=1.5)) / (2 * eps)
    assert deriv == pytest.approx(zero.derivative, abs=1e-9)


def test_near_fold_roots_remain_distinct():
    ec = critical_effort(0.2)
    roots = equilibria_b(0.2, ec * (1 - 1e-10))
    assert roots[1].x < roots[2].x
    assert len(equilibria_b(0.2, ec * (1 + 1e-10))) == 1


@pytest.mark.parametrize(
    "a,e", [(0, 0.1), (1, 0.1), (0.2, -1), (0.2, float("nan")), (float("inf"), 0)]
)
def test_invalid_inputs(a, e):
    with pytest.raises(ValueError):
        equilibria_b(a, e)
