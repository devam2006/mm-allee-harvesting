"""Custom Physics-Informed Neural Network (PINN) architecture.

Engineered independently for WP05 inverse parameter estimation and forward surrogates.
Includes fixed-reference scale conditioning, Xavier initialization, and CPU/GPU portability.
"""

from typing import Sequence

try:
    import torch
    import torch.nn as nn

    _BASE_CLASS = nn.Module
except ImportError:
    torch = None
    nn = None
    _BASE_CLASS = object


class PINN(_BASE_CLASS):
    """Fully-connected multi-layer perceptron for scalar ODE population dynamics.

    Maps time t -> population N(t).
    Uses fixed external reference scales (t_ref, N_ref) to ensure that internal network
    activations operate on O(1) dimensionless variables:
        tau_scaled = t / t_ref
        N_hat = N / N_ref
    """

    def __init__(
        self,
        hidden_layers: Sequence[int] = (64, 64),
        activation: str = "tanh",
        t_ref: float = 1.0,
        n_ref: float = 100.0,
    ):
        if torch is None:
            raise ImportError("PyTorch is required to instantiate PINN")
        super().__init__()

        if t_ref <= 0 or n_ref <= 0:
            raise ValueError("t_ref and n_ref must be positive")

        self.t_ref = float(t_ref)
        self.n_ref = float(n_ref)

        activations = {
            "tanh": nn.Tanh(),
            "silu": nn.SiLU(),
            "gelu": nn.GELU(),
            "sigmoid": nn.Sigmoid(),
        }
        if activation.lower() not in activations:
            raise ValueError(f"Activation '{activation}' not supported. Choose from {list(activations.keys())}")
        act_fn = activations[activation.lower()]

        layers: list[nn.Module] = []
        in_dim = 1
        for out_dim in hidden_layers:
            linear = nn.Linear(in_dim, out_dim)
            nn.init.xavier_normal_(linear.weight)
            nn.init.zeros_(linear.bias)
            layers.append(linear)
            layers.append(act_fn)
            in_dim = out_dim

        final_linear = nn.Linear(in_dim, 1)
        nn.init.xavier_normal_(final_linear.weight)
        nn.init.zeros_(final_linear.bias)
        layers.append(final_linear)

        self.net = nn.Sequential(*layers)

    def forward(self, t: "torch.Tensor") -> "torch.Tensor":
        """Forward pass taking dimensional time t [shape: (B, 1)] and returning

        dimensionless population N_hat = N / N_ref [shape: (B, 1)].
        """
        # Dimensionless normalized time input
        t_scaled = t / self.t_ref
        return self.net(t_scaled)

    def predict_population(self, t: "torch.Tensor") -> "torch.Tensor":
        """Evaluate dimensional population N(t) = N_hat(t) * N_ref."""
        return self.forward(t) * self.n_ref
