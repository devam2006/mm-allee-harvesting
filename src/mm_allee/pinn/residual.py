"""Differentiable ODE right-hand sides, residual and PINN loss (dimensionless x, tau).

Nothing here casts to Python floats or detaches: ``a`` and ``harvest`` may be plain
numbers or tensors (e.g. ``torch.nn.Parameter`` for WP05) and gradients flow to both.
"""

import torch

from .autodiff import derivative

MODELS = ("logistic", "A", "B")


def torch_rhs(x, model, *, a, harvest):
    """Torch twin of ``mm_allee.models.rhs`` (q for logistic/A, e for B).

    Unlike the NumPy version it does no range validation, because ``a`` or
    ``harvest`` may be trainable tensors whose values change during optimisation.
    """
    if model == "logistic":
        return x * (1 - x) - harvest
    if model == "A":
        return x * (1 - x) * (x / a - 1) - harvest
    if model == "B":
        return x * (1 - x) * (x / a - 1) - harvest * x
    raise ValueError("Model must be 'logistic', 'A' or 'B'")


def collocation_residual(x_fn, tau, model, *, a, harvest):
    """Return ``(x, dx/dtau - f(x))`` at times ``tau`` (shape (n, 1)).

    ``x_fn`` maps physical dimensionless time to the state. The derivative is taken
    with respect to ``tau`` itself, so any internal time rescaling is differentiated
    through by autograd. ``create_graph=True`` keeps the residual trainable.
    """
    tau = tau.detach().clone().requires_grad_(True)
    x = x_fn(tau)
    dx = derivative(x, tau)
    return x, dx - torch_rhs(x, model, a=a, harvest=harvest)


def pinn_loss(x_fn, tau, x0, model, *, a, harvest, lambda_phys=1.0, lambda_ic=1.0):
    """``L = lambda_phys*MSE(dx/dtau - f) + lambda_ic*MSE(x(0) - x0)``.

    Returns ``(total, physics_term, ic_term)`` as tensors. ``x(0)`` is evaluated by the
    network, so with a hard-constraint architecture the IC term is exactly zero.
    """
    _, residual = collocation_residual(x_fn, tau, model, a=a, harvest=harvest)
    phys = torch.mean(residual**2)
    zero = tau.new_zeros((1, 1))
    ic = torch.mean((x_fn(zero) - x0) ** 2)
    return lambda_phys * phys + lambda_ic * ic, phys, ic
