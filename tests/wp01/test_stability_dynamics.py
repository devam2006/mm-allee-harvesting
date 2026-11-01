"""Stability labels checked against actual perturbed trajectories (independent of signs).

Each equilibrium is perturbed by +/-DELTA and integrated with the shared RK45 solver.
A stable label requires both perturbations to return; an unstable one requires both to
leave; the fold must attract from above and lead to extinction from below.
"""

import numpy as np
import pytest

from mm_allee.equilibria import equilibria_a, equilibria_logistic, fold_a
from mm_allee.solver import solve_trajectory

DELTA = 0.01  # small vs root gaps here (>= 0.15), large vs solver error (~1e-9)


def run(model, a, q, x0, tau_end):
    return solve_trajectory(model, a=a, harvest=q, x0=x0, tau_end=tau_end, n_points=401)


def assert_label_matches_dynamics(model, a, q, rec, tau_end=60.0):
    above = run(model, a, q, rec.x + DELTA, tau_end)
    below = run(model, a, q, max(rec.x - DELTA, 0.0), tau_end) if rec.x > 0 else None
    if rec.stability == "stable":
        # Relaxation time 1/|f'| <= ~1.3 here, so 60 time units shrink errors by >e^40.
        assert above.extinction_tau is None and abs(above.x[-1] - rec.x) < 1e-6
        if below is not None:
            assert below.extinction_tau is None and abs(below.x[-1] - rec.x) < 1e-6
    elif rec.stability == "unstable":
        assert abs(above.x[-1] - rec.x) > 10 * DELTA
        if below is not None:
            assert abs(below.x[-1] - rec.x) > 10 * DELTA or below.extinction_tau is not None
    else:
        raise AssertionError(f"unexpected label {rec.stability}")


@pytest.mark.parametrize("q", [0.0, 0.1, 0.3, 0.45])
def test_model_a_labels_agree_with_trajectories(q):
    a = 0.2
    for rec in equilibria_a(a, q):
        assert_label_matches_dynamics("A", a, q, rec)


def test_model_a_unstable_root_is_the_collapse_threshold():
    a, q = 0.2, 0.3
    lower, upper = equilibria_a(a, q)
    survive = run("A", a, q, lower.x + DELTA, 60)
    collapse = run("A", a, q, lower.x - DELTA, 60)
    assert survive.extinction_tau is None and abs(survive.x[-1] - upper.x) < 1e-6
    assert collapse.extinction_tau is not None  # finite-time hit of x=0 (q>0)


def test_zero_harvest_subthreshold_decline_has_no_finite_extinction():
    collapse = run("A", 0.2, 0.0, 0.2 - DELTA, 60)
    assert collapse.extinction_tau is None and 0 < collapse.x[-1] < 1e-6


@pytest.mark.parametrize("q", [0.0, 0.1, 0.2])
def test_logistic_labels_agree_with_trajectories(q):
    for rec in equilibria_logistic(q):
        # The solver validates a for every model; the logistic field ignores it.
        assert_label_matches_dynamics("logistic", 0.5, q, rec)


def test_fold_one_sided_behaviour_matches_trajectories():
    """At q_c f'=0: linearisation says nothing; trajectories confirm the sign test."""
    a = 0.2
    x_star, q_c = fold_a(a)
    from_above = run("A", a, q_c, x_star + 0.05, 400)
    from_below = run("A", a, q_c, x_star - 0.05, 400)
    assert from_below.extinction_tau is not None
    assert from_above.extinction_tau is None
    # Approach is algebraic (~1/tau), not exponential: monotone, stays above, gets close.
    assert np.all(np.diff(from_above.x) <= 1e-12) and np.all(from_above.x > x_star)
    assert from_above.x[-1] - x_star < 5e-3


def test_semistable_logistic_fold_from_both_sides():
    from_above = run("logistic", 0.5, 0.25, 0.55, 400)
    from_below = run("logistic", 0.5, 0.25, 0.45, 400)
    assert from_above.extinction_tau is None and from_above.x[-1] - 0.5 < 5e-3
    assert from_below.extinction_tau is not None
