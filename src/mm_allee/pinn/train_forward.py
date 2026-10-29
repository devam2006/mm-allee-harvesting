"""Forward PINN trainer: physics + initial-condition loss only, no solver labels.

The shared engine for WP04 and WP05. WP05 extends it through ``parameters`` (tensors
replacing the fixed ``a``/``harvest``) and ``extra_parameters`` (added to the optimiser).
"""

import math
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

import numpy as np
import torch

from ..metrics import errors
from .network import ForwardMLP, NetworkConfig
from .residual import MODELS, pinn_loss

CHECKPOINT_SCHEMA = 1


@dataclass(frozen=True)
class ForwardConfig:
    """One forward problem plus its training recipe. All fields are JSON-serialisable."""

    model: str = "B"
    a: float = 0.2
    harvest: float = 0.3  # q for logistic/A, e for B
    x0: float = 0.8
    t_end: float = 10.0  # for A: the pre-extinction horizon, never beyond the event
    width: int = 32
    depth: int = 3
    hard_ic: bool = False
    seed: int = 11
    n_collocation: int = 200
    sampling: str = "grid"  # "grid" (fixed, includes both ends) or "random" (Adam only)
    adam_epochs: int = 3000
    lr: float = 1e-2
    lbfgs_epochs: int = 0
    lambda_phys: float = 1.0
    lambda_ic: float = 1.0
    time_budget_s: float | None = None  # wall-clock cap; status becomes "budget_exhausted"

    def validate(self):
        if self.model not in MODELS:
            raise ValueError("model must be 'logistic', 'A' or 'B'")
        if not 0 < self.a < 1 or self.harvest < 0 or self.x0 < 0 or self.t_end <= 0:
            raise ValueError("Require 0<a<1, harvest>=0, x0>=0, t_end>0")
        if self.sampling not in ("grid", "random") or self.n_collocation < 2:
            raise ValueError("sampling must be 'grid'/'random' with n_collocation>=2")
        if self.adam_epochs < 0 or self.lbfgs_epochs < 0 or self.lr <= 0:
            raise ValueError("Require nonnegative epochs and lr>0")

    def network_config(self):
        return NetworkConfig(
            width=self.width,
            depth=self.depth,
            t_end=self.t_end,
            x0=self.x0,
            hard_ic=self.hard_ic,
            seed=self.seed,
        )


@dataclass
class ForwardResult:
    net: ForwardMLP
    config: ForwardConfig
    history: dict = field(default_factory=lambda: {"loss": [], "physics": [], "ic": []})
    wall_seconds: float = 0.0
    status: str = "ok"  # ok | nonfinite_loss | budget_exhausted


def train_forward(config: ForwardConfig, *, parameters=None, extra_parameters=()):
    """Train ``x_hat`` on the ODE residual and initial condition.

    ``parameters`` may map ``"a"``/``"harvest"`` to tensors (kept in the graph);
    ``extra_parameters`` are optimised together with the network weights.
    """
    config.validate()
    a = config.a if parameters is None else parameters.get("a", config.a)
    harvest = config.harvest if parameters is None else parameters.get("harvest", config.harvest)
    net = ForwardMLP(config.network_config())
    result = ForwardResult(net=net, config=config)
    gen = torch.Generator().manual_seed(config.seed)
    grid = torch.linspace(0, config.t_end, config.n_collocation, dtype=torch.float64)[:, None]
    params = list(net.parameters()) + list(extra_parameters)
    start = time.perf_counter()

    def loss_on(tau):
        return pinn_loss(
            net,
            tau,
            config.x0,
            config.model,
            a=a,
            harvest=harvest,
            lambda_phys=config.lambda_phys,
            lambda_ic=config.lambda_ic,
        )

    def record(total, phys, ic):
        result.history["loss"].append(float(total))
        result.history["physics"].append(float(phys))
        result.history["ic"].append(float(ic))
        if not math.isfinite(result.history["loss"][-1]):
            result.status = "nonfinite_loss"
        elif config.time_budget_s and time.perf_counter() - start > config.time_budget_s:
            result.status = "budget_exhausted"
        return result.status == "ok"

    optimiser = torch.optim.Adam(params, lr=config.lr)
    for _ in range(config.adam_epochs):
        if config.sampling == "random":
            tau = config.t_end * torch.rand(
                config.n_collocation, 1, dtype=torch.float64, generator=gen
            )
        else:
            tau = grid
        optimiser.zero_grad()
        total, phys, ic = loss_on(tau)
        total.backward()
        optimiser.step()
        if not record(total.detach(), phys.detach(), ic.detach()):
            break

    if result.status == "ok" and config.lbfgs_epochs:
        lbfgs = torch.optim.LBFGS(
            params, lr=1.0, max_iter=20, history_size=50, line_search_fn="strong_wolfe"
        )
        last = {}

        def closure():
            lbfgs.zero_grad()
            total, phys, ic = loss_on(grid)
            total.backward()
            last["terms"] = (total.detach(), phys.detach(), ic.detach())
            return total

        for _ in range(config.lbfgs_epochs):
            lbfgs.step(closure)
            if not record(*last["terms"]):
                break

    result.wall_seconds = time.perf_counter() - start
    return result


def predict(net, tau):
    """NumPy in, NumPy out; no gradient tracking."""
    with torch.no_grad():
        x = net(torch.as_tensor(np.asarray(tau, dtype=float), dtype=torch.float64)[:, None])
    return x[:, 0].numpy()


def evaluate_prediction(prediction, reference, *, norm_floor=1e-8):
    """Trajectory errors against a reference on the same grid.

    ``relative_l2`` is None (not a fake number) when the reference norm is below
    ``norm_floor``. ``boundary_violations`` counts negative or non-finite predictions.
    """
    pred = np.asarray(prediction, dtype=float)
    ref = np.asarray(reference, dtype=float)
    out = errors(np.nan_to_num(pred, nan=0.0, posinf=0.0, neginf=0.0), ref)
    out["max_abs"] = float(np.max(np.abs(np.nan_to_num(pred) - ref)))
    if np.linalg.norm(ref) < norm_floor:
        out["relative_l2"] = None
    out["boundary_violations"] = int(np.sum(~np.isfinite(pred) | (pred < 0)))
    return out


def save_checkpoint(path, result):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(
        {
            "schema": CHECKPOINT_SCHEMA,
            "config": asdict(result.config),
            "state_dict": result.net.state_dict(),
        },
        path,
    )


def load_checkpoint(path):
    """Rebuild the network from a checkpoint written by ``save_checkpoint``."""
    data = torch.load(Path(path), weights_only=True)
    if data["schema"] != CHECKPOINT_SCHEMA:
        raise ValueError(f"Unsupported checkpoint schema {data['schema']}")
    config = ForwardConfig(**data["config"])
    net = ForwardMLP(config.network_config())
    net.load_state_dict(data["state_dict"])
    return net, config
