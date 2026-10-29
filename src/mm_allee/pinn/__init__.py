"""Physics-Informed Neural Network (PINN) subpackage for mm_allee.

Provides custom network architecture, autodiff, differentiable physics residuals,
and inverse parameter estimation modules.
"""

from .autodiff import derivative
from .network import PINN
from .residual import physics_residual, torch_growth, torch_rhs
from .inverse import TrainableParameters, InversePINNTrainer, InversePINNResult

__all__ = [
    "derivative",
    "PINN",
    "physics_residual",
    "torch_growth",
    "torch_rhs",
    "TrainableParameters",
    "InversePINNTrainer",
    "InversePINNResult",
]
