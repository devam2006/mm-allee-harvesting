import pytest

from mm_allee.comparison import compare_policies, comparison_controls
from mm_allee.models import Parameters


def test_protocols_have_distinct_meanings_and_correct_units():
    p = Parameters(r=0.5, K=1000, A=200)
    rows = compare_policies(p, x0=0.9, fraction=0.5, protocol="initial_catch", tau_end=2)
    assert len({r["initial_catch"] for r in rows}) == 1
    a, b, logistic = rows
    assert a["H"] == pytest.approx(b["h"] * 900)
    controls = comparison_controls(p, 0.9, 0.5, "threshold_fraction")
    assert controls["B"] == pytest.approx(0.4)
    assert controls["logistic"] == 0.125
    assert controls["B"] != pytest.approx(b["control"])
    assert a["h"] is None and b["H"] is None
    assert logistic["critical_initial_population"] is None  # H exceeds logistic threshold


def test_outcomes_do_not_depend_on_short_observation_horizon():
    p = Parameters(1, 1, 0.2)
    rows = compare_policies(p, x0=0.9, fraction=1.2, protocol="threshold_fraction", tau_end=0.01)
    assert all(r["extinction_time"] is None for r in rows)
    assert rows[0]["theoretical_outcome"] == "finite_extinction"
    assert rows[1]["theoretical_outcome"] == "asymptotic_decline"


def test_realised_catch_quadrature_converges():
    p = Parameters(0.5, 1000, 200)
    args = dict(x0=0.9, fraction=0.5, protocol="threshold_fraction", tau_end=20)
    coarse = compare_policies(p, **args, n_points=601)
    fine = compare_policies(p, **args, n_points=1201, rtol=1e-11, atol=1e-13, max_step=0.05)
    assert coarse[1]["total_catch"] == pytest.approx(fine[1]["total_catch"], rel=2e-5)
    assert coarse[0]["total_catch"] == pytest.approx(coarse[0]["H"] * 40)


def test_ambiguous_upstream_fold_band_is_explicitly_rejected():
    p = Parameters(1, 1, 0.2)
    with pytest.raises(ValueError, match="fold tolerance band"):
        comparison_controls(p, 0.9, 1 + 1e-13, "threshold_fraction")
    # A is outside its absolute band, but logistic is still inside its own.
    with pytest.raises(ValueError, match="Logistic control"):
        comparison_controls(p, 0.9, 1 + 3e-12, "threshold_fraction")
