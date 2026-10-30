import numpy as np
import pytest

from mm_allee.history import ramp_schedule, run_history
from mm_allee.solver import solve_trajectory


def test_segments_match_uninterrupted_constant_control():
    hist = run_history("B", a=0.2, x0=0.9, times=[0, 2, 4], controls=[0.3, 0.3])
    direct = solve_trajectory("B", a=0.2, harvest=0.3, x0=0.9, tau_end=4)
    assert hist.rows[-1]["x"] == pytest.approx(direct.x[-1], abs=2e-9)
    at_boundary = [r["x"] for r in hist.rows if r["tau"] == 2]
    assert len(at_boundary) == 2 and at_boundary[0] == at_boundary[1]


@pytest.mark.parametrize("model", ["A", "B"])
def test_shutdown_and_declared_restock(model):
    times, controls = [0, 20, 30, 50], [2, 0, 0]
    plain = run_history(model, a=0.2, x0=1, times=times, controls=controls)
    stocked = run_history(model, a=0.2, x0=1, times=times, controls=controls, restocking={2: 0.6})
    assert plain.rows[-1]["x"] < 1e-7
    assert stocked.rows[-1]["x"] == pytest.approx(1, abs=1e-7)
    before = next(r for r in stocked.rows if r["label"] == "restock_before")
    after = next(r for r in stocked.rows if r["label"] == "restock_after")
    assert after["x"] - before["x"] == pytest.approx(0.6)
    if model == "A":
        assert len(plain.extinction_times) == 1
        after_hit = [r for r in plain.rows if r["tau"] > plain.extinction_times[0]]
        assert all(r["x"] == r["effective_control"] == 0 for r in after_hit)
    else:
        assert plain.extinction_times == []
        assert all(r["x"] > 0 for r in plain.rows)


def test_zero_stays_zero_and_insufficient_restock_fails():
    for model in ["A", "B"]:
        h = run_history(model, a=0.2, x0=0, times=[0, 10, 30], controls=[1, 0])
        assert all(r["x"] == 0 for r in h.rows)
        h = run_history(model, a=0.2, x0=0, times=[0, 10, 30], controls=[1, 0], restocking={1: 0.1})
        assert h.rows[-1]["x"] < 1e-7


@pytest.mark.parametrize("dwell", [1, 3])
@pytest.mark.parametrize("model,critical", [("A", 0.5251380432417552), ("B", 0.8)])
def test_ramp_carryover_and_tolerance_convergence(model, critical, dwell):
    times, controls, last = ramp_schedule(critical, steps=8, dwell=dwell)
    kwargs = dict(a=0.2, x0=1, times=times, controls=controls, restocking={last: 0.6})
    base = run_history(model, **kwargs)
    tight = run_history(model, **kwargs, rtol=1e-11, atol=1e-13, max_step=0.05)
    np.testing.assert_allclose(
        [r["x"] for r in base.rows], [r["x"] for r in tight.rows], atol=2e-7, rtol=0
    )
    np.testing.assert_allclose(base.extinction_times, tight.extinction_times, atol=2e-7, rtol=0)
    for left, r in zip(base.rows[:-1], base.rows[1:], strict=True):
        if left["tau"] == r["tau"] and r["label"] != "restock_after":
            assert left["x"] == r["x"]


@pytest.mark.parametrize(
    "times,controls,restocking",
    [
        ([0, 0], [1], {}),
        ([0, 1], [-1], {}),
        ([0, 1, 2], [1], {}),
        ([0, 1], [1], {1: 0.6}),
        ([0, 1], [1], {0: -0.2}),
    ],
)
def test_invalid_schedules(times, controls, restocking):
    with pytest.raises(ValueError):
        run_history("B", a=0.2, x0=1, times=times, controls=controls, restocking=restocking)
