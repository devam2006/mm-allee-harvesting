"""Forward PINN trainer (JAX): physics loss only, hard initial condition, Adam -> L-BFGS.

The shared engine for WP04 and WP05. No solver solution is ever used as a label. WP05
extends it through ``physical`` (initial values of ``a``/``harvest`` that are then trained
jointly with the weights, e.g. after the caller's own fixed-scale reparametrisation).
"""

import json
import math
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

import jax
import jax.numpy as jnp
import numpy as np
from jax.flatten_util import ravel_pytree
from scipy.optimize import minimize

from ..metrics import errors
from .network import NetworkConfig, init_params, x_hat
from .residual import MODELS, physics_loss

CHECKPOINT_SCHEMA = 2  # 1 was the retired PyTorch format


@dataclass(frozen=True)
class ForwardConfig:
    """One forward problem plus its training recipe. All fields are JSON-serialisable."""

    model: str = "B"
    a: float = 0.2
    harvest: float = 0.3  # q for logistic/A, e for B
    x0: float = 0.8
    t_end: float = 10.0  # for A: the pre-extinction horizon, never beyond the event
    layers: tuple = (1, 32, 32, 1)
    seed: int = 11
    n_collocation: int = 100  # fixed uniform grid on [0, t_end], both ends included
    adam_iters: int = 1000  # 2/7 of the 3500-iteration budget
    lbfgs_iters: int = 2500
    lr: float = 1e-2  # Adam learning rate
    time_budget_s: float | None = None  # wall-clock cap; status becomes "budget_exhausted"

    def validate(self):
        if self.model not in MODELS:
            raise ValueError("model must be 'logistic', 'A' or 'B'")
        if not 0 < self.a < 1 or self.harvest < 0 or self.x0 < 0 or self.t_end <= 0:
            raise ValueError("Require 0<a<1, harvest>=0, x0>=0, t_end>0")
        if self.n_collocation < 2:
            raise ValueError("n_collocation must be >=2")
        if self.adam_iters < 0 or self.lbfgs_iters < 0 or self.lr <= 0:
            raise ValueError("Require nonnegative iteration counts and lr>0")
        self.network_config().validate()

    def network_config(self):
        return NetworkConfig(
            layers=tuple(self.layers), t_end=self.t_end, x0=self.x0, seed=self.seed
        )


@dataclass
class ForwardResult:
    params: list
    config: ForwardConfig
    physical: dict = field(default_factory=dict)  # trained a/harvest when a hook was used
    history: dict = field(default_factory=lambda: {"loss": [], "phase": []})
    wall_seconds: float = 0.0
    status: str = "ok"  # ok | nonfinite_loss | budget_exhausted


def train_forward(config: ForwardConfig, *, physical=None):
    """Train ``x_hat`` on the ODE residual alone (initial condition is hard-coded).

    ``physical`` may map ``"a"``/``"harvest"`` to starting values that are optimised
    together with the weights; otherwise the config values are fixed constants.
    """
    config.validate()
    ncfg = config.network_config()
    tau = jnp.linspace(0.0, config.t_end, config.n_collocation)
    theta = (
        init_params(ncfg),
        {k: jnp.asarray(v, dtype=jnp.float64) for k, v in (physical or {}).items()},
    )

    def loss(theta):
        params, phys = theta
        a = phys.get("a", config.a)
        harvest = phys.get("harvest", config.harvest)
        return physics_loss(
            lambda t: x_hat(params, t, ncfg), tau, config.model, a=a, harvest=harvest
        )

    result = ForwardResult(params=theta[0], config=config)
    start = time.perf_counter()

    def over_budget():
        return bool(config.time_budget_s) and time.perf_counter() - start > config.time_budget_s

    # ---- phase 1: Adam, a short push into a good basin ----
    zeros = jax.tree_util.tree_map(jnp.zeros_like, theta)
    m, v = zeros, zeros
    b1, b2, eps = 0.9, 0.999, 1e-8

    @jax.jit
    def adam_step(theta, m, v, t):
        value, grad = jax.value_and_grad(loss)(theta)
        m = jax.tree_util.tree_map(lambda m_, g: b1 * m_ + (1 - b1) * g, m, grad)
        v = jax.tree_util.tree_map(lambda v_, g: b2 * v_ + (1 - b2) * g * g, v, grad)
        theta = jax.tree_util.tree_map(
            lambda p, m_, v_: (
                p - config.lr * (m_ / (1 - b1**t)) / (jnp.sqrt(v_ / (1 - b2**t)) + eps)
            ),
            theta,
            m,
            v,
        )
        return theta, m, v, value

    for step in range(1, config.adam_iters + 1):
        theta, m, v, value = adam_step(theta, m, v, step)
        result.history["loss"].append(float(value))
        result.history["phase"].append("adam")
        if not math.isfinite(result.history["loss"][-1]):
            result.status = "nonfinite_loss"
            break
        if over_budget():
            result.status = "budget_exhausted"
            break

    # ---- phase 2: L-BFGS takes over from the Adam solution ----
    if result.status == "ok" and config.lbfgs_iters:
        flat0, unravel = ravel_pytree(theta)
        flat_vg = jax.jit(jax.value_and_grad(lambda flat: loss(unravel(flat))))

        def fun(flat):
            value, grad = flat_vg(jnp.asarray(flat))
            return float(value), np.asarray(grad, dtype=np.float64)

        def callback(intermediate_result):
            result.history["loss"].append(float(intermediate_result.fun))
            result.history["phase"].append("lbfgs")
            if over_budget():
                result.status = "budget_exhausted"
                raise StopIteration

        fit = minimize(
            fun,
            np.asarray(flat0, dtype=np.float64),
            jac=True,
            method="L-BFGS-B",
            callback=callback,
            options={
                "maxiter": config.lbfgs_iters,
                "maxfun": 20 * config.lbfgs_iters,
                "maxcor": 50,
                "ftol": 0.0,
                "gtol": 0.0,
            },
        )
        if np.all(np.isfinite(fit.x)):
            theta = unravel(jnp.asarray(fit.x))
        else:
            result.status = "nonfinite_loss"

    result.params, result.physical = theta[0], {k: float(val) for k, val in theta[1].items()}
    if result.status == "ok" and not math.isfinite(float(loss(theta))):
        result.status = "nonfinite_loss"
    result.wall_seconds = time.perf_counter() - start
    return result


def predict(params, config: ForwardConfig, tau):
    """NumPy in, NumPy out."""
    ncfg = config.network_config()
    fn = jax.jit(jax.vmap(lambda t: x_hat(params, t, ncfg)))
    return np.asarray(fn(jnp.asarray(np.asarray(tau, dtype=float))))


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
    """Write config + weights to a pickle-free ``.npz`` file."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    arrays = {}
    for i, (weight, bias) in enumerate(result.params):
        arrays[f"W{i}"], arrays[f"b{i}"] = np.asarray(weight), np.asarray(bias)
    meta = {
        "schema": CHECKPOINT_SCHEMA,
        "config": asdict(result.config),
        "physical": result.physical,
    }
    np.savez(path, meta=np.array(json.dumps(meta)), **arrays)


def load_checkpoint(path):
    """Return ``(params, config)`` from a checkpoint written by ``save_checkpoint``."""
    with np.load(Path(path), allow_pickle=False) as data:
        meta = json.loads(str(data["meta"]))
        if meta["schema"] != CHECKPOINT_SCHEMA:
            raise ValueError(f"Unsupported checkpoint schema {meta['schema']}")
        n_layers = len([k for k in data.files if k.startswith("W")])
        params = [(jnp.asarray(data[f"W{i}"]), jnp.asarray(data[f"b{i}"])) for i in range(n_layers)]
    return params, ForwardConfig(**{**meta["config"], "layers": tuple(meta["config"]["layers"])})
