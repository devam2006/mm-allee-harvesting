# Current integrated classical contract

WP01–WP03 in this integration branch share `thresholds.critical_a/critical_b` and `collapse.positive_branches`. Only exact equality to the common computed critical control denotes the fold; a nearby uncertainty scale never creates a root. WP02 comparisons propagate `boundary_unresolved` for initial-state uncertainty. Historical source-branch notes below are retained as provenance and do not override this contract.

# Shared interfaces and file contracts

Freeze names before independent implementations. Existing scaffold APIs below are implemented; the **planned** analysis/PINN APIs are package deliverables and are not falsely exported yet.

## Implemented shared foundation

- `models.Parameters(r,K,A,H=0,h=0)`: immutable dimensional parameters, validated positive/range constraints; `.dimensionless()` returns `a,q,e`.
- `models.growth(x,a)`, `rhs(x,model,a=...,harvest=...)`: dimensionless NumPy-compatible scalar/array functions; model is exactly `logistic`, `A` or `B`; harvest is q for logistic/A and e for B. Negative x are allowed in the algebraic RHS for event location, never as a reported physical trajectory.
- `models.dimensional_rhs(N,model,p)`: dimensional equivalent. No implicit unit conversions.
- `solver.solve_trajectory(model,*,a,harvest,x0,tau_end,n_points=301,rtol=1e-9,atol=1e-11,max_step=0.1,tau_eval=None) -> Trajectory`. Nonnegative constant harvest only. A/logistic with positive constant yield use a terminal downward zero event. B and zero-yield cases do not declare finite zero events. Returns `.tau`, `.x`, `.extinction_tau`, `.model`, `.boundary_policy`; no post-event samples. Initial zero is handled under the explicit boundary convention. Optional tau_eval strictly increases from zero within the horizon; post-event times are dropped and the numerical event endpoint appended. Otherwise n_points uniformly covers the physical interval. Output times do not prescribe RK steps.
- `datasets.generate_reference(case,solver=None) -> ReferenceTrajectory`: implemented clean A/B export in dimensional time/population, configurable n_points/time_points, with explicit event metadata. `write_reference_files` writes clean CSVs, declared known conditions and separate evaluation truth. No noise/splits/inverse fitting. See [RK45 handoff](WP03_RK45_HANDOFF.md).
- `reference_validation.validate_reference(...)`: implemented independent dimensional-polynomial DOP853, tighter RK45 and guarded A quadrature checks. This supports the reference milestone, not general basin classification or rigorous interval certification.

- `equilibria` (WP01, implemented): `equilibria_logistic(q)`, `equilibria_a(a,q,include_excluded=False)`, `classify_equilibrium(model,x_eq,a=,q=)`, `fold_a(a) -> (x_star,q_c)`, `rhs_derivative`, `growth_derivative`, `extinction_boundary(model,q)`, `branch_rows(model,q_values,a=)`. Each root is an immutable `Equilibrium` record: `model,a,q,x,physical,multiplicity,derivative,left_sign,right_sign,stability,attracts_from,residual,note`; `stability` is `stable|unstable|semistable|excluded`, decided from one-sided signs of f (not f' alone). Physical roots only by default; negative cubic roots are returned only with `include_excluded=True` and `physical=False`. For q>0, x=0 is never returned as an equilibrium. Physical records never depend on `include_excluded`. Tolerances: fold `|q-q_c| <= FOLD_RTOL*q_c` (`FOLD_RTOL=64*eps`), Brent relative tolerance `4*eps`, sign probe `min(1e-4,d/4)` with `d` the distance to the nearest other real root or to `x=0`. `fold_a` uses the rationalised, cancellation-free `q_c` (agrees with WP03 `thresholds.critical_a`). Plotting helpers live in `equilibria_plots` and return figures without writing files.

- `solver.solve_trajectory(model,*,a,harvest,x0,tau_end,n_points=301,rtol=1e-9,atol=1e-11,max_step=0.1) -> Trajectory`. Nonnegative constant harvest only. A/logistic with positive constant yield use a terminal downward zero event. B and zero-yield cases do not declare finite zero events. Returns `.tau`, `.x`, `.extinction_tau`, `.model`, `.boundary_policy`; no post-event samples. Initial zero is handled under the explicit boundary convention.
- `equilibria` (WP01, implemented): `equilibria_logistic(q)`, `equilibria_a(a,q,include_excluded=False)`, `classify_equilibrium(model,x_eq,a=,q=)`, `fold_a(a) -> (x_star,q_c)`, `rhs_derivative`, `growth_derivative`, `extinction_boundary(model,q)`, `branch_rows(model,q_values,a=)`. Each root is an immutable `Equilibrium` record: `model,a,q,x,physical,multiplicity,derivative,left_sign,right_sign,stability,attracts_from,residual,note`; `stability` is `stable|unstable|semistable|excluded`, decided from one-sided signs of f (not f' alone). Physical roots only by default; negative cubic roots are returned only with `include_excluded=True` and `physical=False`. For q>0, x=0 is never returned as an equilibrium. Tolerances: fold `|q-q_c|<=1e-12`, Brent `xtol=1e-14`, sign probe `min(1e-4,gap/4)`. Plotting helpers live in `equilibria_plots` and return figures without writing files.
- `metrics.errors(prediction,reference) -> {rmse,mae,relative_l2}`; relative L2 is `None` for a zero reference norm. Shapes must match and be nonempty finite arrays.
- `data.validate_splits(train_ids,val_ids,test_ids)`: rejects overlap, duplicates or empty splits. IDs identify individual observations, not merely row numbers reset per file.
- `plotting.save_figure(fig,stem)`: writes paired `.png` and `.eps` to the supplied stem. Caller supplies labels/style and a provenance manifest.

All numerical code lives in `src/mm_allee/`; scripts import it. Core NumPy functions must not import JAX (or any other optional PINN dependency). Do not use `Parameters` for trainable inverse values: float validation would detach/autograd-break them.

## Planned work-package modules

| Owner | Planned module/API | Handoff |
|---|---|---|
| WP01 | Implemented above (`equilibria.py`, `equilibria_plots.py`) | WP02 mirrors the `Equilibrium` record for Model B; WP03's `thresholds.critical_a` should agree with `equilibria.fold_a` (independent maximisation check) |
| WP02 | `model_b.py`: B equilibrium records; `history.py`: segmented ramp and explicit restocking policy | History output includes segment, control, time, population, event/intervention labels |
| WP03 | Implemented: `thresholds.py`: `critical_a(a) -> (x_star,q_c)`, `critical_b(a) -> e_c`; `collapse.py`: full basin/extinction analysis. Clean `datasets.py` and numerical-reference validation are implemented above | Clean reference CSV + manifest + stable observation IDs; WP05 prepares observation/noise/split files |
| WP04 (**implemented, JAX; PR pending review**) | `pinn/network.py`, `pinn/residual.py`, `pinn/train_forward.py`: small network, differentiable A/B residual, forward trainer | Frozen model/config/checkpoint format, history/metrics schema, trainable-parameter extension hook |
| WP05 | `pinn/inverse.py`, `inference.py`, `validation.py`: constrained parameters, ODE least-squares baseline, noise/held-out analysis | Recovery and prediction metrics, identifiability demo and failure tables |

Names are agreed starting points; update the contract in a separate reviewed change if an API needs refinement. No placeholder functions return invented scientific outputs. Analysis modules must return data for tests and plots, not only write images.

## Forward PINN engine (WP04, implemented; JAX)

JAX, CPU, float64 (importing `mm_allee.pinn.autodiff` enables x64). Dimensionless `x=N/K`, `tau=r t`; import from `mm_allee.pinn.*`. Owner decisions of 29-30 Oct 2026: JAX replaces the originally planned PyTorch; network `(1,32,32,1)`; hard initial condition; physics loss only; Adam then L-BFGS; final sweep uses 300 uniform collocation points and the swish activation (selected from tanh/swish/sigmoid by a pre-declared rule).

- `network.NetworkConfig(layers,t_end,x0,seed,activation="tanh")` (`activation` is `tanh | swish | sigmoid`, see `network.ACTIVATIONS`; the default keeps earlier results reproducible), `network.init_params(config)` (Glorot-normal, seeded from `config.seed`), `network.x_hat(params,tau,config)`: scalar physical time in, scalar state out, `x0 + s*N(s)` with `s=tau/t_end`, so `x_hat(0)=x0` exactly. Vectorise with `jax.vmap`.
- `autodiff.derivative(fn,time)`: elementwise `d fn/d time` via `vmap(grad)`; `fn` is a scalar function that may close over weights or physical parameters.
- `residual.jax_rhs(x,model,*,a,harvest)`: JAX twin of `models.rhs` (q for logistic/A, e for B); `a`/`harvest` may be numbers or traced arrays; no validation, no casts. `residual.collocation_residual(x_fn,tau,model,*,a,harvest) -> (x, dx/dtau - f(x))`; `residual.physics_loss(x_fn,tau,model,*,a,harvest)` is the mean squared residual (the whole loss).
- `train_forward.ForwardConfig` (JSON-serialisable: model,a,harvest,x0,t_end,layers,seed,activation="tanh",n_collocation=100,adam_iters=1000,lbfgs_iters=2500,lr=1e-2,time_budget_s), `train_forward(config,*,physical=None,tau=None) -> ForwardResult(params,config,physical,history{loss,phase},wall_seconds,status,lbfgs)`. Adam is hand-written; L-BFGS is SciPy L-BFGS-B on the JAX gradient (its exit `{status,message,iterations}` is recorded in `result.lbfgs`; with `ftol=gtol=0` an `ABNORMAL` exit is the usual benign stop at floating-point precision, so it is reported, not treated as failure). `tau` optionally replaces the default uniform collocation grid (1-D, inside `[0,t_end]`; used by diagnostics).
- **Trainable physical parameters (the WP05 hook).** `physical={"a":a0,"harvest":h0}` trains those values jointly with the weights and **keeps them in range through both Adam and L-BFGS**: the optimisers update unconstrained internal values and the loss converts them on every evaluation (`harvest = raw**2 >= 0`, `a = sigmoid(raw) in (0,1)`), so gradients flow through the transform and no step can leave the range. Starting values must already be valid (`ValueError` otherwise; unknown keys too); a harvest start below 1e-6, including exactly 0, is lifted to 1e-6 (raw = 0 has zero gradient). `result.physical` holds the trained *physical* (valid) values. Rohan's inverse trainer uses its own transforms (softplus/sigmoid, A in (0,K)); the two owners should agree one set of transforms and tests when the engines are integrated (see `DECISIONS.md`).
- `predict(params,config,tau_numpy)`; `physics_residual(params,config,tau_numpy,physical=None)` returns `dx/dtau - f(x)` of a trained or loaded network using the trained physical values where given.
- `evaluate_prediction(pred,ref,norm_floor=1e-8,near_zero=0.05) -> {valid,n_invalid,rmse,mae,relative_l2,max_abs,max_abs_near_zero,boundary_violations}`. **A prediction containing NaN or +-inf is invalid: it is never repaired, `valid` is False and every error score is None** (it must never count as accurate). `relative_l2` is also None when the reference norm is below `norm_floor`; `max_abs_near_zero` is the largest absolute error where the reference is below `near_zero` (None if there is no such point).
- `save_checkpoint(path,result)` / `load_checkpoint(path) -> ForwardResult`: the saved model is the weights, the config, **the learned physical parameters (`.physical`)**, the training status and the L-BFGS exit; the loss history and runtime are not saved (they come back empty/zero). Schema 2, pickle-free `.npz` (schema 1 was the retired PyTorch format; older schema-2 files without status/lbfgs load with defaults).
- **Run statuses.** `train_forward` returns `ok` (finite loss, iteration budget completed), `budget_exhausted` (wall-clock cap hit) or `nonfinite_loss` (loss or weights became NaN/inf). The experiment runner adds `invalid_prediction` (output contains NaN/inf, no error score exists) and `failed` (training or scoring raised an exception, recorded with its message in the `note` column; it does not stop the sweep), and labels a finished run `inaccurate` when its relative L2 error (or, if that is undefined, its maximum absolute error) exceeds the pre-declared threshold. There is no separate "converged" label: the forward trainer runs a fixed iteration budget and reports the loss and L-BFGS exit instead. (The inverse trainer additionally has `validation_stopped` and, since review round 2, `lbfgs_failed` (an L-BFGS exception, with the Adam state kept as a labelled fallback); its `status` describes the Adam phase and whether the run finished, while how L-BFGS ended is in `result.optimizer["lbfgs_outcome"]` (tolerance_reached, iteration_limit, abnormal_exit, ...) and in the `lbfgs_outcome` / `lbfgs_message` columns of the WP05 prediction table; the two vocabularies should still be unified at integration.)
- Metrics CSV adds columns `case,max_abs,max_abs_near_zero,boundary_violations,final_loss,iterations,lbfgs_status,lbfgs_message,lbfgs_iterations,note,t_end,extinction_tau` to the schema below; floats are written in scientific notation; forward rows have empty `noise_sigma` and `split=dense_reference`; an undefined score is an empty cell, never 0.

### Units: forward (dimensionless) versus dimensional equations

The forward engine works in `x=N/K`, `tau=r t`, `a=A/K`, `q=H/(rK)` (Model A), `e=h/r` (Model B). A dimensional implementation that keeps the original time `t` and puts the growth rate `r` inside the right-hand side is mathematically equivalent: for any smooth `N_hat(t) = K x_hat(r t)`,

`dN_hat/dt - f_dim(N_hat) = r K ( dx_hat/dtau - f(x_hat) )`, with `f_dim` = `models.dimensional_rhs`.

This chain-rule identity (including the scalings above) is checked independently, using the NumPy `dimensional_rhs` against the forward residual in tau, by `tests/wp04/test_review_fixes.py::test_dimensional_residual_equals_rK_times_dimensionless_residual` for both models. Different time conventions are therefore not a bug, but each trainer must state which one it uses. Observation scaling must use fixed, externally declared reference scales (`N_ref`, `t_ref`), never the unknown true `r` or `K` (see `SCIENTIFIC_CONTRACT.md`). A parity test between the WP04 forward residual and the WP05 inverse residual itself still has to be added when the two engines are integrated.

## Run/config contract

Experiment scripts use `argparse --config PATH --output PATH` and run from the repository root; JSON configs are the default. They must be import-safe (no training at module import), seedable and runnable without opening Jupyter. `configs/reference.json` is a starter fixture, not the final experimental design.

Every run writes `manifest.json` with schema version, run ID, UTC timestamp, git SHA/dirty status, full configuration, seeds, model and units, `r,K,A,H/h` or their fixed scales, solver type/tolerances/event policy, split IDs, noise definition, dependency versions and hardware, elapsed time, success/failure status and output file checksums. Use JSON null plus an explanatory status when a metric is undefined, not a fake zero or non-standard NaN.

## Data and metrics

**WP03 clean reference CSV (implemented):** `observation_id,trajectory_id,model,time,population,is_synthetic`. It carries no split or noisy-label columns. Known-K experimental conditions/fixed scales are separate from true unknown parameters/events and evaluation metadata.

**WP05 fitting-observation CSV (to implement):** `observation_id,trajectory_id,model,time,observed_population,split,noise_sigma,noise_seed,is_synthetic`. Clean `population` truth stays in separate reference/evaluation data, not in the trainer's observation dictionary. WP05 chooses observation subsets, applies seeded noise, freezes splits and tests leakage. Stable source IDs allow audit without copying truth into fitting inputs. This boundary clarification replaces the earlier combined reference/observation CSV suggestion.

Use consistent **dimensional** time/population columns and declare units/reference scales in the manifest; dimensionless variants require clearly named `tau,x` columns and must not masquerade as dimensional ones. Store the noise-free reference separately from fitting observations; training code cannot inspect final-test truth or simulator parameters held as evaluation metadata. At sigma zero the observations are exact but the split still applies.

Metrics CSV: `run_id,model,regime,method,seed,split,noise_sigma,rmse,mae,relative_l2,wall_seconds,status`; inverse runs add parameter true/estimated/error values in a separate long-form table. Record seed-level results before aggregate mean/std. Do not average away failures; show their count and cause. The notebook and report read the same curated tables.

Figure names: `wpNN_short_description.png/.eps`; add a manifest mapping figure/table to command/config/run/seed. Text interpretation must state whether results are analytical, simulated, fitted or held-out evaluation.

## Team ownership metadata

`team.json` is the source for the five GitHub accounts and optional `work_package` choices. `null` means unassigned; otherwise use WP01–WP05, one distinct task per person. `python scripts/sync_team.py` renders ownership into nine documentation files. Generated regions are delimited by `team-sync` comments. The script preserves the status table’s scientific state/evidence and changes only its owner column. `--check` is read-only and is required by CI. Owner-authorised assignment administration may reach `main` under the setup exception in `CONTRIBUTING.md`; the script neither commits nor grants collaborator access.

## Implemented WP03 analysis APIs

- `thresholds.critical_a(a) -> (x_star,q_c)` and `critical_b(a) -> e_c`; dimensional thresholds and optional sensitivity/MSY use validated Parameters.
- `collapse.positive_branches(model,*,a,harvest) -> (lower,upper) | None`: positive basin/upper branches, repeated pair at the exact computed fold, or None above it. WP01/WP02 retain full equilibrium-record/stability APIs.
  For B, the lower branch is evaluated via the root product `a*(1+e)/upper` to preserve relative accuracy at small a; the exact fold returns `(centre,centre)` explicitly.
- `collapse.classify_basin(model,*,a,harvest,x0,root_tol=2e-12) -> Basin`: regime, physical outcome, limiting state and boundary. Exact returned roots are equilibria; non-exact starts within root_tol of the unstable/semistable boundary are unresolved. Controls have no fold-merging tolerance.
- `collapse.extinction_time_a(*,a,q,x0,...) -> ExtinctionTime`: finite dimensionless time or None with basin status. Initial extinction has time 0. Zero-harvest/non-reaching paths are not integrated through poles. An above-fold tangent substitution resolves the bottleneck; a logarithmic substitution resolves close subcritical endpoints. At the computed fold, an elementary antiderivative has `method="fold_closed_form"` and `quadrature_error=None`. Other finite integrations carry QUADPACK's error estimate, which excludes root/input rounding. Physical time is tau/r.
- `collapse.safety_margins(model,Parameters,N0)`: control fraction, dimensional barrier/population margin and outcome. A stable-branch yield supremum and B interior realised-yield maximum are distinct from maximum effort.
- `collapse_study.build_study(config)` returns analysis data and enforces its budget before publication. `experiments/wp03/run.py` writes tables, paired figures, summary and a hash manifest.

Precision, evidence mapping and commands: [WP03_ANALYSIS.md](WP03_ANALYSIS.md). This PR restores the prior clean CSV contract after main's revert; WP05 still owns noise/splits.

### WP01/WP03 fold and merge handoff (30 October 2026)

WP03's exact computed-control equality convention remains unchanged. WP01 PR #8
currently uses `abs(q-q_c) <= 64*eps*q_c`, so its equilibrium records and WP03's
basin classification can differ for controls within that band. The population
uncertainty `root_tol` in WP03 is separate and never changes the control regime.
Do not assume the two APIs agree in this band until the affected owners reconcile
the convention in a reviewed integration change. This documents the difference;
it does not change WP01 or claim an agreed unified convention.

WP03 exports vector PDF alongside each PNG/EPS, tracks all three in the analysis
manifest, and uses extensionless report figure references. The shared
`plotting.save_figure` PNG/EPS return contract is unchanged.

PRs #4 and #8 both change `docs/INTERFACES.md`, `docs/DECISIONS.md` and the assembled
notebook. Whichever merges second must preserve both sets of documentation and
notebook fragments, rerun `python scripts/assemble_notebook.py`, and execute the
combined notebook/tests. These steps remain pending until the branches integrate.

### RK45 tolerance validation (31 October 2026)

The WP03-owned shared solver and reference configuration validator reject
`rtol < MIN_RK45_RTOL`, where `MIN_RK45_RTOL = 100*np.finfo(float).eps`
(about 2.220446049250313e-14). SciPy otherwise increases such requests while
experiment configurations can still record the smaller requested value.
Rejection occurs before integration, including initial-zero fast paths, and
before the reference CLI writes outputs. The minimum itself is accepted and
tested against the initialized RK45 object's actual tolerance. Default settings,
the six clean CSV fixtures, threshold/basin conventions and outcomes are unchanged.

WP01 and WP02 must validate requested solver blocks before creating their own
outputs when adopting this shared solver. This does not change either owner's
branch or certify their existing preflight validation.

Reference validation still accepts a baseline at the supported minimum. Its
refinement caps the requested relative tolerance at that minimum, continues to
reduce atol/max_step, and records `refinement_rtol` and
`refinement_rtol_at_floor` in its evidence. It never silently requests an
unsupported refinement tolerance.

## WP05 submitted interface (pending review)

The ZIP adds `data.generate_noisy_observations(...)`, returning arrays plus train/val/test indices; `inference.fit_ode_least_squares(...) -> FitResult`; and `pinn.inverse.{TrainableParameters, InversePINNTrainer, InversePINNResult}` with `pinn.network.PINN`. `validation.py` audits splits, writes metric tables and creates figures. Imports and definitions are preserved from the submission.

**Integration blocker:** these are independent PyTorch dimensional-population APIs. PR #6 replaces the same `pinn/{__init__,network,residual,autodiff}.py` paths with JAX dimensionless-population APIs. They cannot be combined by copying files over each other. WP04/WP05 owners must agree a shared framework/API or explicit coexistence before merge; this submission does not implement that decision.

### 31 October integration follow-up (WP01)

189 WP01 tests passed, including 90-digit independent roots for both reported close-fold examples and rejection of unsupported rtol before any output. Near-fold roots are solved in offsets; simple-root signs/derivatives use the factored cubic. The existing standalone fold-band policy is unchanged pending the separate integration PR. No human approval or merge is supplied.

### 31 October integration follow-up (WP02)

40 WP02 tests passed. Removed the deleted WP01 constant import while keeping the conservative comparison exclusion local; reject unsupported tiny rtol before output; exported notebook provenance no longer requires Git. The older restored WP01 dependency is replaced by current WP01 only in the separate integration PR. No human approval or merge is supplied.
