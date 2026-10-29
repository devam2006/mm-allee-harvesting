"""Small seeded MLP x_hat(tau) with fixed input scaling and optional hard initial condition."""

from dataclasses import asdict, dataclass

import torch
from torch import nn


@dataclass(frozen=True)
class NetworkConfig:
    """Everything needed to rebuild a network; stored inside checkpoints."""

    width: int = 32
    depth: int = 3  # number of hidden layers
    t_end: float = 10.0  # fixed input scale: the network sees s = tau / t_end in [0, 1]
    x0: float = 0.8
    hard_ic: bool = False
    seed: int = 11


class ForwardMLP(nn.Module):
    """x_hat(tau) = x0 + s*N(s) (hard IC) or N(s) (soft IC), with s = tau / t_end.

    ``forward`` takes *physical* dimensionless time, so autograd differentiates
    through the scaling and ``dx/dtau = (1/t_end) dN/ds`` needs no manual chain rule.
    The scale ``t_end`` is a fixed constant, never trained. Calling this constructor
    seeds the global Torch RNG (``torch.manual_seed``) so initialisation is reproducible.
    """

    def __init__(self, config: NetworkConfig):
        super().__init__()
        if config.width < 1 or config.depth < 1 or config.t_end <= 0:
            raise ValueError("Require width>=1, depth>=1, t_end>0")
        self.config = config
        torch.manual_seed(config.seed)
        layers, size = [], 1
        for _ in range(config.depth):
            layers += [nn.Linear(size, config.width, dtype=torch.float64), nn.Tanh()]
            size = config.width
        layers.append(nn.Linear(size, 1, dtype=torch.float64))
        self.body = nn.Sequential(*layers)

    def forward(self, tau):
        s = tau / self.config.t_end
        out = self.body(s)
        return self.config.x0 + s * out if self.config.hard_ic else out


def config_dict(config: NetworkConfig) -> dict:
    return asdict(config)
