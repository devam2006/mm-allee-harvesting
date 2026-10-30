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
    jax = pytest.importorskip("jax")
    import jax.numpy as jnp

    from mm_allee.pinn.autodiff import derivative

    t = jnp.array([0.2, 0.7])

    def total(weight):
        return jnp.sum(derivative(lambda s: weight * s**3, t))

    # d/dt (w t^3) = 3 w t^2, so d/dw of its sum is 3 * sum(t^2): a hand-derived expectation.
    np.testing.assert_allclose(derivative(lambda s: 2.0 * s**3, t), 3 * 2.0 * np.asarray(t) ** 2)
    assert float(jax.grad(total)(2.0)) == pytest.approx(3 * float(jnp.sum(t**2)))
