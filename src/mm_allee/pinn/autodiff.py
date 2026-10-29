"""Autodiff derivative primitive for physics-informed neural networks."""


def derivative(output, time):
    """Elementwise derivative for independent batch samples, retaining the autograd graph.

    Network outputs must not mix time samples across the batch (no batch coupling).
    Torch is imported dynamically inside the function so that non-PINN routines
    and environments without PyTorch installed can import the package safely.
    """
    import torch

    if not time.requires_grad:
        raise ValueError("time tensor must have requires_grad=True")

    return torch.autograd.grad(
        output,
        time,
        grad_outputs=torch.ones_like(output),
        create_graph=True,
        retain_graph=True,
    )[0]
