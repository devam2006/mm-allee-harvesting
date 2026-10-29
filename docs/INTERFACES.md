# Shared interfaces and file contracts

Freeze names before independent implementations. Existing scaffold APIs below are implemented; the **planned** analysis/PINN APIs are package deliverables and are not falsely exported yet.

## Implemented shared foundation

- `models.Parameters(r,K,A,H=0,h=0)`: immutable dimensional parameters, validated positive/range constraints; `.dimensionless()` returns `a,q,e`.
- `models.growth(x,a)`, `rhs(x,model,a=...,harvest=...)`: dimensionless NumPy-compatible scalar/array functions; model is exactly `logistic`, `A` or `B`; harvest is q for logistic/A and e for B. Negative x are allowed in the algebraic RHS for event location, never as a reported physical trajectory.
- `models.dimensional_rhs(N,model,p)`: dimensional equivalent. No implicit unit conversions.
- `solver.solve_trajectory(model,*,a,harvest,x0,tau_end,n_points=301,rtol=1e-9,atol=1e-11,max_step=0.1) -> Trajectory`. Nonnegative constant harvest only. A/logistic with positive constant yield use a terminal downward zero event. B and zero-yield cases do not declare finite zero events. Returns `.tau`, `.x`, `.extinction_tau`, `.model`, `.boundary_policy`; no post-event samples. Initial zero is handled under the explicit boundary convention.
- `metrics.errors(prediction,reference) -> {rmse,mae,relative_l2}`; relative L2 is `None` for a zero reference norm. Shapes must match and be nonempty finite arrays.
- `data.validate_splits(train_ids,val_ids,test_ids)`: rejects overlap, duplicates or empty splits. IDs identify individual observations, not merely row numbers reset per file.
- `plotting.save_figure(fig,stem)`: writes paired `.png` and `.eps` to the supplied stem. Caller supplies labels/style and a provenance manifest.

All numerical code lives in `src/mm_allee/`; scripts import it. Core NumPy functions must not import JAX (or any other optional PINN dependency). Do not use `Parameters` for trainable inverse values: float validation would detach/autograd-break them.

## Planned work-package modules

| Owner | Planned module/API | Handoff |
|---|---|---|
| WP01 | `equilibria.py`: `equilibria_a(a,q)`, `equilibria_logistic(q)`, `classify_equilibrium(...)`; list of root/stability/derivative records with a documented tolerance | WP02/WP03 reuse stability conventions and data schema |
| WP02 | `model_b.py`: B equilibrium records; `history.py`: segmented ramp and explicit restocking policy | History output includes segment, control, time, population, event/intervention labels |
| WP03 | `thresholds.py`: `critical_a(a) -> (x_star,q_c)`, `critical_b(a) -> e_c`; `collapse.py`: basin labels and extinction quadrature; `datasets.py`: generator | Reference CSV + manifest + train/val/test observation IDs |
| WP04 (**implemented, JAX; PR pending review**) | `pinn/network.py`, `pinn/residual.py`, `pinn/train_forward.py`: small network, differentiable A/B residual, forward trainer | Frozen model/config/checkpoint format, history/metrics schema, trainable-parameter extension hook |
| WP05 | `pinn/inverse.py`, `inference.py`, `validation.py`: constrained parameters, ODE least-squares baseline, noise/held-out analysis | Recovery and prediction metrics, identifiability demo and failure tables |

Names are agreed starting points; update the contract in a separate reviewed change if an API needs refinement. No placeholder functions return invented scientific outputs. Analysis modules must return data for tests and plots, not only write images.

## Forward PINN engine (WP04, implemented; JAX)

JAX, CPU, float64 (importing `mm_allee.pinn.autodiff` enables x64). Dimensionless `x=N/K`, `tau=r t`; import from `mm_allee.pinn.*`. Owner decisions of 29-30 Oct 2026: JAX replaces the originally planned PyTorch; network `(1,32,32,1)`; hard initial condition; physics loss only; Adam then L-BFGS; final sweep uses 300 uniform collocation points and the swish activation (selected from tanh/swish/sigmoid by a pre-declared rule).

- `network.NetworkConfig(layers,t_end,x0,seed,activation="tanh")` (`activation` is `tanh | swish | sigmoid`, see `network.ACTIVATIONS`; the default keeps earlier results reproducible), `network.init_params(config)` (Glorot-normal, seeded from `config.seed`), `network.x_hat(params,tau,config)`: scalar physical time in, scalar state out, `x0 + s*N(s)` with `s=tau/t_end`, so `x_hat(0)=x0` exactly. Vectorise with `jax.vmap`.
- `autodiff.derivative(fn,time)`: elementwise `d fn/d time` via `vmap(grad)`; `fn` is a scalar function that may close over weights or physical parameters.
- `residual.jax_rhs(x,model,*,a,harvest)`: JAX twin of `models.rhs` (q for logistic/A, e for B); `a`/`harvest` may be numbers or traced arrays; no validation, no casts. `residual.collocation_residual(x_fn,tau,model,*,a,harvest) -> (x, dx/dtau - f(x))`; `residual.physics_loss(x_fn,tau,model,*,a,harvest)` is the mean squared residual (the whole loss).
- `train_forward.ForwardConfig` (JSON-serialisable: model,a,harvest,x0,t_end,layers,seed,activation="tanh",n_collocation=100,adam_iters=1000,lbfgs_iters=2500,lr=1e-2,time_budget_s), `train_forward(config,*,physical=None,tau=None) -> ForwardResult(params,config,physical,history{loss,phase},wall_seconds,status)`. Adam is hand-written; L-BFGS is SciPy L-BFGS-B on the JAX gradient. **WP05 hook:** pass `physical={"a":value,"harvest":value}` and those entries are trained jointly with the weights (reparametrise with fixed external scales on the caller's side). `tau` optionally replaces the default uniform collocation grid (1-D, inside `[0,t_end]`; used by diagnostics). Status is `ok | nonfinite_loss | budget_exhausted`; `history["phase"]` is `"adam"` or `"lbfgs"` per iteration.
- `predict(params,config,tau_numpy)`, `evaluate_prediction(pred,ref,norm_floor=1e-8) -> {rmse,mae,relative_l2|None,max_abs,boundary_violations}`, `save_checkpoint(path,result)` / `load_checkpoint(path) -> (params, config)` (schema 2, pickle-free `.npz`; schema 1 was the retired PyTorch format).
- Metrics CSV adds columns `case,max_abs,boundary_violations,final_loss,iterations,t_end,extinction_tau` to the schema below; floats are written in scientific notation; forward rows have empty `noise_sigma` and `split=dense_reference`.

## Run/config contract

Experiment scripts use `argparse --config PATH --output PATH` and run from the repository root; JSON configs are the default. They must be import-safe (no training at module import), seedable and runnable without opening Jupyter. `configs/reference.json` is a starter fixture, not the final experimental design.

Every run writes `manifest.json` with schema version, run ID, UTC timestamp, git SHA/dirty status, full configuration, seeds, model and units, `r,K,A,H/h` or their fixed scales, solver type/tolerances/event policy, split IDs, noise definition, dependency versions and hardware, elapsed time, success/failure status and output file checksums. Use JSON null plus an explanatory status when a metric is undefined, not a fake zero or non-standard NaN.

## Data and metrics

Reference observations CSV: `observation_id,trajectory_id,model,time,population,observed_population,split,noise_sigma,noise_seed,is_synthetic`.

Use consistent **dimensional** time/population columns and declare units/reference scales in the manifest; dimensionless variants require clearly named `tau,x` columns and must not masquerade as dimensional ones. Store the noise-free reference separately from fitting observations; training code cannot inspect final-test truth or simulator parameters held as evaluation metadata. At sigma zero the observations are exact but the split still applies.

Metrics CSV: `run_id,model,regime,method,seed,split,noise_sigma,rmse,mae,relative_l2,wall_seconds,status`; inverse runs add parameter true/estimated/error values in a separate long-form table. Record seed-level results before aggregate mean/std. Do not average away failures; show their count and cause. The notebook and report read the same curated tables.

Figure names: `wpNN_short_description.png/.eps`; add a manifest mapping figure/table to command/config/run/seed. Text interpretation must state whether results are analytical, simulated, fitted or held-out evaluation.

## Team ownership metadata

`team.json` is the source for the five GitHub accounts and optional `work_package` choices. `null` means unassigned; otherwise use WP01–WP05, one distinct task per person. `python scripts/sync_team.py` renders ownership into nine documentation files. Generated regions are delimited by `team-sync` comments. The script preserves the status table’s scientific state/evidence and changes only its owner column. `--check` is read-only and is required by CI. Owner-authorised assignment administration may reach `main` under the setup exception in `CONTRIBUTING.md`; the script neither commits nor grants collaborator access.
