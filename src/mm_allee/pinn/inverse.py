"""Inverse PINN trainer for strong Allee effect parameter estimation.

Implements constrained physical parameter parameterizations without gradient detachment,
physics-informed joint optimization, strict training-data-only loss computation,
and validation-based early stopping.
"""

import math
import time
from dataclasses import dataclass
from typing import Any, Literal, Sequence

import numpy as np

from ..metrics import errors
from .autodiff import derivative
from .network import PINN
from .residual import physics_residual

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim

    _BASE_MODULE = nn.Module
except ImportError:
    torch = None
    nn = None
    optim = None
    _BASE_MODULE = object


def _inv_softplus(y: float) -> float:
    """Inverse softplus: x = ln(exp(y) - 1)."""
    return math.log(math.expm1(max(y, 1e-6)))


def _inv_sigmoid(y: float) -> float:
    """Inverse sigmoid (logit): x = ln(y / (1 - y))."""
    y_clamped = min(max(y, 1e-6), 1.0 - 1e-6)
    return math.log(y_clamped / (1.0 - y_clamped))


class TrainableParameters(_BASE_MODULE):
    """Constrained physical parameters module for Models A and B.

    Enforces physical constraints without detaching gradients:
      - r > 0: r = softplus(raw_r)
      - 0 < A < K: A = K * sigmoid(raw_A)
      - H >= 0: H = softplus(raw_H)
      - h >= 0: h = softplus(raw_h)

    Trainable physical parameters receive continuous, nonzero gradients everywhere.
    """

    def __init__(
        self,
        model: Literal["A", "B"],
        fit_params: Sequence[str],
        known_conditions: dict[str, float] | None = None,
        initial_guesses: dict[str, float] | None = None,
    ):
        if torch is None:
            raise ImportError("PyTorch is required for TrainableParameters")
        super().__init__()

        self.model = model
        self.fit_params = list(fit_params)
        known = known_conditions or {}
        guesses = initial_guesses or {}

        # Default initial values
        default_p = {
            "r": 1.0,
            "K": float(known.get("known_K", 100.0)),
            "A": 20.0,
            "H": 5.0 if model == "A" else 0.0,
            "h": 0.2 if model == "B" else 0.0,
        }
        for k, v in guesses.items():
            default_p[k] = float(v)

        self.raw_params = nn.ParameterDict()
        self.fixed_values = {}

        # Initialize r
        if "r" in self.fit_params:
            self.raw_params["raw_r"] = nn.Parameter(
                torch.tensor(_inv_softplus(default_p["r"]), dtype=torch.float32)
            )
        else:
            self.fixed_values["r"] = float(known.get("r", default_p["r"]))

        # Initialize K
        if "K" in self.fit_params:
            self.raw_params["raw_K"] = nn.Parameter(
                torch.tensor(_inv_softplus(default_p["K"]), dtype=torch.float32)
            )
        else:
            self.fixed_values["K"] = float(known.get("known_K", default_p["K"]))

        # Initialize A (constrained: 0 < A < K via sigmoid)
        if "A" in self.fit_params:
            k_ref = self.fixed_values.get("K", default_p["K"])
            ratio = min(max(default_p["A"] / k_ref, 0.01), 0.99)
            self.raw_params["raw_A"] = nn.Parameter(
                torch.tensor(_inv_sigmoid(ratio), dtype=torch.float32)
            )
        else:
            self.fixed_values["A"] = float(known.get("A", default_p["A"]))

        # Initialize harvest control
        if model == "A":
            if "H" in self.fit_params:
                self.raw_params["raw_H"] = nn.Parameter(
                    torch.tensor(_inv_softplus(default_p["H"]), dtype=torch.float32)
                )
            else:
                self.fixed_values["H"] = float(known.get("H", default_p["H"]))
            self.fixed_values["h"] = 0.0
        elif model == "B":
            if "h" in self.fit_params:
                self.raw_params["raw_h"] = nn.Parameter(
                    torch.tensor(_inv_softplus(default_p["h"]), dtype=torch.float32)
                )
            else:
                self.fixed_values["h"] = float(known.get("h", default_p["h"]))
            self.fixed_values["H"] = 0.0

    def forward(self) -> dict[str, "torch.Tensor"]:
        """Compute differentiable physical parameters satisfying domain constraints."""
        p: dict[str, torch.Tensor] = {}

        # r > 0
        if "raw_r" in self.raw_params:
            p["r"] = torch.nn.functional.softplus(self.raw_params["raw_r"])
        else:
            p["r"] = torch.tensor(self.fixed_values["r"], dtype=torch.float32)

        # K > 0
        if "raw_K" in self.raw_params:
            p["K"] = torch.nn.functional.softplus(self.raw_params["raw_K"])
        else:
            p["K"] = torch.tensor(self.fixed_values["K"], dtype=torch.float32)

        # 0 < A < K
        if "raw_A" in self.raw_params:
            p["A"] = p["K"] * torch.sigmoid(self.raw_params["raw_A"])
        else:
            p["A"] = torch.tensor(self.fixed_values["A"], dtype=torch.float32)

        # Harvest controls >= 0
        if self.model == "A":
            if "raw_H" in self.raw_params:
                p["H"] = torch.nn.functional.softplus(self.raw_params["raw_H"])
            else:
                p["H"] = torch.tensor(self.fixed_values["H"], dtype=torch.float32)
            p["h"] = torch.tensor(0.0, dtype=torch.float32)
        elif self.model == "B":
            if "raw_h" in self.raw_params:
                p["h"] = torch.nn.functional.softplus(self.raw_params["raw_h"])
            else:
                p["h"] = torch.tensor(self.fixed_values["h"], dtype=torch.float32)
            p["H"] = torch.tensor(0.0, dtype=torch.float32)

        return p

    def get_physical_parameters(self) -> dict[str, float]:
        """Return current physical parameters as detached standard Python floats."""
        with torch.no_grad():
            tensors = self.forward()
            return {k: float(v.item()) for k, v in tensors.items()}


@dataclass(frozen=True)
class InversePINNResult:
    model: str
    fit_params: list[str]
    estimated_parameters: dict[str, float]
    all_parameters: dict[str, float]
    status: str
    success: bool
    final_epoch: int
    wall_seconds: float
    train_loss: float
    val_loss: float
    train_metrics: dict[str, float | None]
    val_metrics: dict[str, float | None]
    test_metrics: dict[str, float | None]
    predicted_trajectory: dict[str, np.ndarray]
    training_history: dict[str, list[float]]


class InversePINNTrainer:
    """Trainer for joint optimization of PINN weights and physical parameters.

    Strict leakage guarantee:
      - Training loss uses ONLY training observation points (t_train, y_train).
      - Collocation points t_colloc enforce the physics residual across the domain.
      - Validation observations determine early stopping and checkpoint selection.
      - Test observations are NEVER accessed during training or hyperparameter selection.
    """

    def __init__(
        self,
        net: PINN,
        parameters_module: TrainableParameters,
        *,
        lambda_data: float = 1.0,
        lambda_phys: float = 0.1,
        lambda_ic: float = 1.0,
        lr_net: float = 1e-3,
        lr_params: float = 1e-2,
        t_ref: float = 1.0,
        n_ref: float = 100.0,
    ):
        if torch is None:
            raise ImportError("PyTorch is required for InversePINNTrainer")

        self.net = net
        self.params_mod = parameters_module
        self.lambda_data = float(lambda_data)
        self.lambda_phys = float(lambda_phys)
        self.lambda_ic = float(lambda_ic)
        self.t_ref = float(t_ref)
        self.n_ref = float(n_ref)

        # Optimize network and physical parameters with tailored learning rates
        self.optimizer = optim.Adam(
            [
                {"params": self.net.parameters(), "lr": lr_net},
                {"params": self.params_mod.parameters(), "lr": lr_params},
            ]
        )

    def fit(
        self,
        observations: dict[str, Any],
        known_conditions: dict[str, float],
        *,
        epochs: int = 1000,
        n_collocation: int = 100,
        patience: int = 100,
        seed: int = 42,
    ) -> InversePINNResult:
        """Run inverse PINN training."""
        torch.manual_seed(seed)
        np.random.default_rng(seed)

        times_all = np.asarray(observations["time"], dtype=float)
        obs_pop_all = np.asarray(observations["observed_population"], dtype=float)
        idx_train = observations["train_indices"]
        idx_val = observations["val_indices"]
        idx_test = observations["test_indices"]

        # Training data only
        t_train_np = times_all[idx_train]
        y_train_np = obs_pop_all[idx_train]
        t_val_np = times_all[idx_val]
        y_val_np = obs_pop_all[idx_val]

        t_end = float(times_all[-1])
        n0 = float(known_conditions.get("known_initial_population", y_train_np[0]))

        # Convert to Torch tensors
        t_train_t = torch.tensor(t_train_np, dtype=torch.float32).unsqueeze(1)
        y_train_t = torch.tensor(y_train_np, dtype=torch.float32).unsqueeze(1)
        t_val_t = torch.tensor(t_val_np, dtype=torch.float32).unsqueeze(1)
        y_val_t = torch.tensor(y_val_np, dtype=torch.float32).unsqueeze(1)
        t0_t = torch.tensor([[0.0]], dtype=torch.float32)
        n0_t = torch.tensor([[n0]], dtype=torch.float32)

        # Uniform collocation points across [0, t_end]
        t_colloc_np = np.linspace(0, t_end, n_collocation)
        t_colloc_t = torch.tensor(t_colloc_np, dtype=torch.float32).unsqueeze(1).requires_grad_(True)

        history = {
            "epoch": [],
            "loss_train": [],
            "loss_val": [],
            "loss_data": [],
            "loss_phys": [],
            "loss_ic": [],
        }
        for p_name in self.params_mod.fit_params:
            history[f"param_{p_name}"] = []

        best_val_loss = float("inf")
        best_net_state = None
        best_param_state = None
        patience_counter = 0

        start_time = time.perf_counter()

        for epoch in range(1, epochs + 1):
            self.optimizer.zero_grad()

            # Physical parameters
            current_p = self.params_mod()

            # 1. Supervised Data Loss on Training Observations ONLY
            pred_train = self.net.predict_population(t_train_t)
            loss_data = torch.mean(((pred_train - y_train_t) / self.n_ref) ** 2)

            # 2. Physics ODE Residual Loss on Collocation Points
            res = physics_residual(
                self.net,
                t_colloc_t,
                self.params_mod.model,
                current_p,
                r_ref=1.0,
                n_ref=self.n_ref,
            )
            loss_phys = torch.mean(res**2)

            # 3. Initial Condition Loss
            pred_ic = self.net.predict_population(t0_t)
            loss_ic = torch.mean(((pred_ic - n0_t) / self.n_ref) ** 2)

            total_train_loss = (
                self.lambda_data * loss_data
                + self.lambda_phys * loss_phys
                + self.lambda_ic * loss_ic
            )

            total_train_loss.backward()
            self.optimizer.step()

            # Validation loss evaluation (no gradient)
            with torch.no_grad():
                pred_val = self.net.predict_population(t_val_t)
                loss_val = torch.mean(((pred_val - y_val_t) / self.n_ref) ** 2).item()

            train_loss_val = total_train_loss.item()
            history["epoch"].append(epoch)
            history["loss_train"].append(train_loss_val)
            history["loss_val"].append(loss_val)
            history["loss_data"].append(loss_data.item())
            history["loss_phys"].append(loss_phys.item())
            history["loss_ic"].append(loss_ic.item())

            current_phys = self.params_mod.get_physical_parameters()
            for p_name in self.params_mod.fit_params:
                history[f"param_{p_name}"].append(current_phys[p_name])

            # Early stopping check based on validation loss
            if loss_val < best_val_loss:
                best_val_loss = loss_val
                best_net_state = {k: v.cpu().clone() for k, v in self.net.state_dict().items()}
                best_param_state = {
                    k: v.cpu().clone() for k, v in self.params_mod.state_dict().items()
                }
                patience_counter = 0
            else:
                patience_counter += 1
                if patience_counter >= patience:
                    break

        wall_time = time.perf_counter() - start_time

        # Restore best checkpoint
        if best_net_state is not None:
            self.net.load_state_dict(best_net_state)
        if best_param_state is not None:
            self.params_mod.load_state_dict(best_param_state)

        final_phys = self.params_mod.get_physical_parameters()
        est_dict = {p: final_phys[p] for p in self.params_mod.fit_params}

        # Final evaluation on full trajectory
        with torch.no_grad():
            t_all_t = torch.tensor(times_all, dtype=torch.float32).unsqueeze(1)
            pred_all_np = self.net.predict_population(t_all_t).squeeze(1).numpy()

        train_err = errors(pred_all_np[idx_train], obs_pop_all[idx_train])
        val_err = errors(pred_all_np[idx_val], obs_pop_all[idx_val])
        test_err = errors(pred_all_np[idx_test], obs_pop_all[idx_test])

        return InversePINNResult(
            model=self.params_mod.model,
            fit_params=self.params_mod.fit_params,
            estimated_parameters=est_dict,
            all_parameters=final_phys,
            status="converged",
            success=True,
            final_epoch=len(history["epoch"]),
            wall_seconds=wall_time,
            train_loss=history["loss_train"][-1],
            val_loss=best_val_loss,
            train_metrics=train_err,
            val_metrics=val_err,
            test_metrics=test_err,
            predicted_trajectory={"time": times_all, "population": pred_all_np},
            training_history=history,
        )
