"""Differentiable physics residuals for strong Allee effect Models A and B.

Computes dN/dt - f(N) using autograd without detaching physical parameters.
"""

from typing import Literal

from .autodiff import derivative

try:
    import torch
except ImportError:
    torch = None


def torch_growth(N: "torch.Tensor", r: "torch.Tensor", K: "torch.Tensor", A: "torch.Tensor") -> "torch.Tensor":
    """Allee production vector field in PyTorch:

    g(N) = r * N * (1 - N/K) * (N/A - 1).
    Does not detach tensors or break the autograd computation graph.
    """
    return r * N * (1.0 - N / K) * (N / A - 1.0)


def torch_rhs(
    N: "torch.Tensor",
    model: Literal["A", "B"],
    r: "torch.Tensor",
    K: "torch.Tensor",
    A: "torch.Tensor",
    H: "torch.Tensor" = None,
    h: "torch.Tensor" = None,
) -> "torch.Tensor":
    """Differentiable dimensional right-hand side f(N) for Model A or Model B."""
    g = torch_growth(N, r, K, A)
    if model == "A":
        if H is None:
            raise ValueError("Model A requires harvest parameter H")
        return g - H
    elif model == "B":
        if h is None:
            raise ValueError("Model B requires harvest parameter h")
        return g - h * N
    raise ValueError(f"Model must be 'A' or 'B', got '{model}'")


def physics_residual(
    net: "torch.nn.Module",
    t_colloc: "torch.Tensor",
    model: Literal["A", "B"],
    parameters: dict[str, "torch.Tensor"],
    r_ref: float = 1.0,
    n_ref: float = 100.0,
) -> "torch.Tensor":
    """Compute the normalized physics ODE residual at collocation times t_colloc:

        Residual = (dN/dt - f(N; parameters)) / (r_ref * n_ref)

    Retains the computation graph for both network weights and physical parameters.
    """
    if torch is None:
        raise ImportError("PyTorch is required for physics_residual")

    if not t_colloc.requires_grad:
        t_colloc = t_colloc.clone().detach().requires_grad_(True)

    # Evaluate dimensional population prediction
    if hasattr(net, "predict_population"):
        N_pred = net.predict_population(t_colloc)
    else:
        # Fallback if raw module
        N_pred = net(t_colloc / 1.0) * n_ref

    # Compute time derivative dN/dt via autograd
    dN_dt = derivative(N_pred, t_colloc)

    # Compute ODE RHS
    r = parameters["r"]
    K = parameters["K"]
    A = parameters["A"]
    H = parameters.get("H")
    h = parameters.get("h")

    rhs_val = torch_rhs(N_pred, model, r, K, A, H=H, h=h)

    # Normalized residual to ensure O(1) physics loss gradient
    residual = (dN_dt - rhs_val) / (r_ref * n_ref)
    return residual
