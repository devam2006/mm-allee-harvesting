"""Contract checks spanning all three classical work packages."""

import numpy as np
import pytest

from mm_allee.collapse import classify_basin, positive_branches
from mm_allee.comparison import compare_policies
from mm_allee.equilibria import equilibria_a, equilibria_logistic, fold_a
from mm_allee.model_b import critical_effort, equilibria_b
from mm_allee.models import Parameters
from mm_allee.thresholds import critical_a, critical_b


@pytest.mark.parametrize("a", [1e-6, 0.05, 0.2, 0.95, 0.999999])
def test_shared_thresholds_and_adjacent_control_topology(a):
    assert fold_a(a) == critical_a(a)
    assert critical_effort(a) == critical_b(a)
    for model, critical in [("A", fold_a(a)[1]), ("B", critical_b(a))]:
        for control, expected in [
            (np.nextafter(critical, 0), 2),
            (critical, 1),
            (np.nextafter(critical, np.inf), 0),
        ]:
            records = equilibria_a(a, control) if model == "A" else equilibria_b(a, control)[1:]
            assert len(records) == expected
            roots = positive_branches(model, a=a, harvest=control)
            if roots is None:
                assert not records
            else:
                assert records[0].x == roots[0]
                assert records[-1].x == roots[1]
            if expected == 2:
                assert records[0].x < records[1].x
                assert [r.stability for r in records] == ["unstable", "stable"]


def test_logistic_adjacent_controls_are_not_merged():
    assert len(equilibria_logistic(np.nextafter(0.25, 0))) == 2
    assert equilibria_logistic(0.25)[0].multiplicity == 2
    assert equilibria_logistic(np.nextafter(0.25, np.inf)) == []


@pytest.mark.parametrize("model", ["A", "B"])
def test_comparison_propagates_basin_uncertainty(model):
    p = Parameters(0.5, 1000, 200)
    critical = critical_a(0.2)[1] if model == "A" else critical_b(0.2)
    lower = positive_branches(model, a=0.2, harvest=0.5 * critical)[0]
    x0 = lower + 1e-13
    assert (
        classify_basin(model, a=0.2, harvest=0.5 * critical, x0=x0).outcome == "boundary_unresolved"
    )
    rows = compare_policies(p, x0=x0, fraction=0.5, protocol="threshold_fraction", tau_end=0.01)
    assert (
        next(row for row in rows if row["model"] == model)["theoretical_outcome"]
        == "boundary_unresolved"
    )
