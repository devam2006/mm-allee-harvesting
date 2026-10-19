import numpy as np
import pytest

from mm_allee.metrics import errors


def test_metrics_against_hand_calculation():
    result = errors([2, 4], [1, 2])
    assert result["rmse"] == pytest.approx(np.sqrt(2.5))
    assert result["mae"] == 1.5
    assert result["relative_l2"] == 1


def test_zero_reference_norm_is_explicitly_undefined():
    assert errors([1, 0], [0, 0])["relative_l2"] is None


@pytest.mark.parametrize("pred,ref", [([], []), ([1], [1, 2]), ([float("nan")], [1])])
def test_bad_metric_inputs(pred, ref):
    with pytest.raises(ValueError):
        errors(pred, ref)


@pytest.mark.pinn
def test_derivative_retains_parameter_gradient():
    torch = pytest.importorskip("torch")
    from mm_allee.pinn.autodiff import derivative

    t = torch.tensor([[0.2], [0.7]], dtype=torch.float64, requires_grad=True)
    weight = torch.tensor(2.0, dtype=torch.float64, requires_grad=True)
    value = weight * t**3
    dvalue = derivative(value, t)
    torch.testing.assert_close(dvalue, 3 * weight * t**2)
    dvalue.sum().backward()
    assert weight.grad is not None and weight.grad.item() > 0
