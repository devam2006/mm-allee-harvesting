# Shared interfaces and file contracts

Freeze names before independent implementations. Existing scaffold APIs below are implemented; the **planned** analysis/PINN APIs are package deliverables and are not falsely exported yet.

## Implemented shared foundation

- `models.Parameters(r,K,A,H=0,h=0)`: immutable dimensional parameters, validated positive/range constraints; `.dimensionless()` returns `a,q,e`.
- `models.growth(x,a)`, `rhs(x,model,a=...,harvest=...)`: dimensionless NumPy-compatible scalar/array functions; model is exactly `logistic`, `A` or `B`; harvest is q for logistic/A and e for B. Negative x are allowed in the algebraic RHS for event location, never as a reported physical trajectory.
- `models.dimensional_rhs(N,model,p)`: dimensional equivalent. No implicit unit conversions.
- `solver.solve_trajectory(model,*,a,harvest,x0,tau_end,n_points=301,rtol=1e-9,atol=1e-11,max_step=0.1,tau_eval=None) -> Trajectory`. Nonnegative constant harvest only. A/logistic with positive constant yield use a terminal downward zero event. B and zero-yield cases do not declare finite zero events. Returns `.tau`, `.x`, `.extinction_tau`, `.model`, `.boundary_policy`; no post-event samples. Initial zero is handled under the explicit boundary convention. Optional tau_eval strictly increases from zero within the horizon; post-event times are dropped and the numerical event endpoint appended. Otherwise n_points uniformly covers the physical interval. Output times do not prescribe RK steps.
- `datasets.generate_reference(case,solver=None) -> ReferenceTrajectory`: implemented clean A/B export in dimensional time/population, configurable n_points/time_points, with explicit event metadata. `write_reference_files` writes clean CSVs, declared known conditions and separate evaluation truth. No noise/splits/inverse fitting. See [RK45 handoff](WP03_RK45_HANDOFF.md).
- `reference_validation.validate_reference(...)`: implemented independent dimensional-polynomial DOP853, tighter RK45 and guarded A quadrature checks. This supports the reference milestone, not general basin classification or rigorous interval certification.
- `metrics.errors(prediction,reference) -> {rmse,mae,relative_l2}`; relative L2 is `None` for a zero reference norm. Shapes must match and be nonempty finite arrays.
- `data.validate_splits(train_ids,val_ids,test_ids)`: rejects overlap, duplicates or empty splits. IDs identify individual observations, not merely row numbers reset per file.
- `plotting.save_figure(fig,stem)`: writes paired `.png` and `.eps` to the supplied stem. Caller supplies labels/style and a provenance manifest.

All numerical code lives in `src/mm_allee/`; scripts import it. Core NumPy functions must not import Torch. Do not use `Parameters` for trainable inverse values: float validation would detach/autograd-break them.

## Planned work-package modules

| Owner | Planned module/API | Handoff |
|---|---|---|
| WP01 | `equilibria.py`: `equilibria_a(a,q)`, `equilibria_logistic(q)`, `classify_equilibrium(...)`; list of root/stability/derivative records with a documented tolerance | WP02/WP03 reuse stability conventions and data schema |
| WP02 | `model_b.py`: B equilibrium records; `history.py`: segmented ramp and explicit restocking policy | History output includes segment, control, time, population, event/intervention labels |
| WP03 | Implemented: `thresholds.py`: `critical_a(a) -> (x_star,q_c)`, `critical_b(a) -> e_c`; `collapse.py`: full basin/extinction analysis. Clean `datasets.py` and numerical-reference validation are implemented above | Clean reference CSV + manifest + stable observation IDs; WP05 prepares observation/noise/split files |
| WP04 | `pinn/network.py`, `pinn/residual.py`, `pinn/train_forward.py`: small network, differentiable A/B residual, forward trainer | Frozen model/config/checkpoint format, history/metrics schema, trainable-parameter extension hook |
| WP05 | `pinn/inverse.py`, `inference.py`, `validation.py`: constrained parameters, ODE least-squares baseline, noise/held-out analysis | Recovery and prediction metrics, identifiability demo and failure tables |

Names are agreed starting points; update the contract in a separate reviewed change if an API needs refinement. No placeholder functions return invented scientific outputs. Analysis modules must return data for tests and plots, not only write images.

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
- `collapse.classify_basin(model,*,a,harvest,x0,root_tol=2e-12) -> Basin`: regime, physical outcome, limiting state and boundary. Exact returned roots are equilibria; non-exact starts within root_tol of the unstable/semistable boundary are unresolved. Controls have no fold-merging tolerance.
- `collapse.extinction_time_a(*,a,q,x0,...) -> ExtinctionTime`: finite dimensionless time or None with basin status. Initial extinction has time 0. Zero-harvest/non-reaching paths are not integrated through poles. An above-fold tangent substitution resolves the bottleneck; a logarithmic substitution resolves close subcritical endpoints. At the computed fold, an elementary antiderivative has `method="fold_closed_form"` and `quadrature_error=None`. Other finite integrations carry QUADPACK's error estimate, which excludes root/input rounding. Physical time is tau/r.
- `collapse.safety_margins(model,Parameters,N0)`: control fraction, dimensional barrier/population margin and outcome. A stable-branch yield supremum and B interior realised-yield maximum are distinct from maximum effort.
- `collapse_study.build_study(config)` returns analysis data and enforces its budget before publication. `experiments/wp03/run.py` writes tables, paired figures, summary and a hash manifest.

Precision, evidence mapping and commands: [WP03_ANALYSIS.md](WP03_ANALYSIS.md). This PR restores the prior clean CSV contract after main's revert; WP05 still owns noise/splits.


## WP05 submitted interface (pending review)

The ZIP adds `data.generate_noisy_observations(...)`, returning arrays plus train/val/test indices; `inference.fit_ode_least_squares(...) -> FitResult`; and `pinn.inverse.{TrainableParameters, InversePINNTrainer, InversePINNResult}` with `pinn.network.PINN`. `validation.py` audits splits, writes metric tables and creates figures. Imports and definitions are preserved from the submission.

**Integration blocker:** these are independent PyTorch dimensional-population APIs. PR #6 replaces the same `pinn/{__init__,network,residual,autodiff}.py` paths with JAX dimensionless-population APIs. They cannot be combined by copying files over each other. WP04/WP05 owners must agree a shared framework/API or explicit coexistence before merge; this submission does not implement that decision.
