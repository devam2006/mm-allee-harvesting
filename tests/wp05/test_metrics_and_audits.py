"""Tests for WP05 metric calculations, parameter error reporting, and audit verification."""

import numpy as np
import pytest

from mm_allee.metrics import errors
from mm_allee.validation import audit_splits_and_leakage, compute_parameter_metrics


def test_hand_calculated_trajectory_errors():
    pred = [10.0, 20.0, 30.0]
    ref = [12.0, 18.0, 30.0]
    # deltas: [-2, +2, 0]
    # MSE = (4 + 4 + 0) / 3 = 8/3; RMSE = sqrt(8/3)
    # MAE = (2 + 2 + 0) / 3 = 4/3
    # norm(ref) = sqrt(144 + 324 + 900) = sqrt(1368)
    # relative L2 = sqrt(8) / sqrt(1368) = sqrt(8 / 1368)
    res = errors(pred, ref)
    assert res["rmse"] == pytest.approx(np.sqrt(8.0 / 3.0))
    assert res["mae"] == pytest.approx(4.0 / 3.0)
    assert res["relative_l2"] == pytest.approx(np.sqrt(8.0 / 1368.0))


def test_zero_reference_norm_handled():
    res = errors([2.0, -1.0], [0.0, 0.0])
    assert res["relative_l2"] is None
    assert res["rmse"] == pytest.approx(np.sqrt(2.5))
    assert res["mae"] == pytest.approx(1.5)


def test_compute_parameter_metrics():
    p_true = {"r": 0.7, "A": 20.0, "K": 100.0, "H": 10.0}
    p_est = {"r": 0.77, "A": 18.0, "K": 100.0, "H": 10.5}

    recs = compute_parameter_metrics(p_true, p_est, ["r", "A", "H"])
    rec_dict = {r["parameter"]: r for r in recs}

    assert rec_dict["r"]["absolute_error"] == pytest.approx(0.07)
    assert rec_dict["r"]["relative_error"] == pytest.approx(0.10)
    assert rec_dict["A"]["absolute_error"] == pytest.approx(2.0)
    assert rec_dict["A"]["relative_error"] == pytest.approx(0.10)
    assert rec_dict["H"]["absolute_error"] == pytest.approx(0.5)
    assert rec_dict["H"]["relative_error"] == pytest.approx(0.05)


def test_audit_splits_and_leakage_guards():
    valid_obs = {
        "observation_id": ["t1:0", "t1:1", "t1:2", "t1:3", "t1:4"],
        "time": np.array([0.0, 1.0, 2.0, 3.0, 4.0]),
        "train_indices": [0, 1, 2],
        "val_indices": [3],
        "test_indices": [4],
    }
    # Should pass without error
    audit_splits_and_leakage(valid_obs)

    # Overlapping indices
    invalid_obs = dict(valid_obs, val_indices=[2, 3])
    with pytest.raises(ValueError):
        audit_splits_and_leakage(invalid_obs)
