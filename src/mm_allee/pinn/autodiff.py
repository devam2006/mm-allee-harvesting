"""One implemented autograd primitive; this is not a completed PINN trainer."""


def derivative(output, time):
    """Elementwise derivative for independent batch samples, retaining the graph.

    Network outputs must not mix time samples across the batch (no batch coupling).
    Torch is imported here so classical users do not need the optional dependency.
    """
    import torch

    return torch.autograd.grad(
        output, time, grad_outputs=torch.ones_like(output), create_graph=True
    )[0]
