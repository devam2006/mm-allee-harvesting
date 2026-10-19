import numpy as np
import pytest

from mm_allee.data import validate_splits
from mm_allee.models import Parameters, dimensional_rhs


def test_disjoint_observation_ids():
    validate_splits(["run1:0", "run1:1"], ["run1:2"], ["run1:3"])


@pytest.mark.parametrize(
    "splits", [([1], [1], [3]), ([1, 1], [2], [3]), ([], [2], [3]), ([1], [2], [2])]
)
def test_invalid_splits_rejected(splits):
    with pytest.raises(ValueError):
        validate_splits(*splits)


def test_four_b_parameters_are_not_uniquely_determined():
    p1 = Parameters(r=1.0, A=0.2, K=1.0, h=0.5)
    p2 = Parameters(r=1.35, A=0.3, K=0.9, h=0.15)
    N = np.linspace(0, 1.2, 31)
    np.testing.assert_allclose(dimensional_rhs(N, "B", p1), dimensional_rhs(N, "B", p2), atol=1e-14)
    assert p1 != p2
