# Rohan's WP05 submission: intake, review and reconciliation

[**Draft PR #7**](https://github.com/devam2006/mm-allee-harvesting/pull/7). Owner/assignee: **@rohanagrawal28**. Uploaded by **@devam2006** at his request, from `Rohan_RK45_Completed_Code.zip`. Updated and reconciled to JAX by **@rohanagrawal28**.

## Scope and dependencies

- Branch: `wp05/rohan-inverse-validation`.
- Base: `wp03/collapse-analysis` at `6ba15550b0c72447c2652870e71ed7166ab5b6d9`, the open WP03 PR #4.
- WP05 engine has been converted from PyTorch to **pure JAX**, sharing Prem's WP04 neural engine (`network.py`, `residual.py`, `autodiff.py`, `train_forward.py`).
- Full 108-run sweep executed on Google Colab (Python 3.13.18, JAX 0.5.0, pytest 8.4.2), yielding 108 prediction records and 324 parameter records.

## Resolution of Review Findings

### 1. [Resolved] Shared JAX Engine and Two-Phase Optimization
- Transitioned `src/mm_allee/pinn/inverse.py` to pure JAX, eliminating PyTorch and aligning fully with Prem's WP04 engine (`network.py`, `residual.py`, `autodiff.py`).
- Inverse architecture inherits exact hard initial conditions $x(0) = x_0$ through shared `x_hat`.
- Implemented **Decision 1**: Two-phase optimization consisting of Phase 1 Adam (with separate learning rates for network weights and physical parameters, plus validation early stopping) followed by Phase 2 L-BFGS refinement via `scipy.optimize.minimize(method="L-BFGS-B")` using `jax.flatten_util.ravel_pytree`.

### 2. [Resolved] Full 108-Run Parameter and Prediction Sweep
- Completed the full sweep across all 6 cases (Model A & B: regular persistence, near-fold, severe collapse), 3 noise levels (0%, 1%, 5% of $N_{\mathrm{ref}}$), 3 seeds (11, 22, 33), and 2 methods (`ODE_LS`, `PINN`).
- Results: **108 prediction records** in `artifacts/tables/wp05_prediction_metrics.csv` and **324 parameter records** in `artifacts/tables/wp05_parameter_metrics.csv`.
- Generated paired figures from genuine run data: `artifacts/figures/wp05_recovery_noise.{png,eps}` and `artifacts/figures/wp05_heldout_failure.{png,eps}`.

### 3. [Resolved] Independent Noise and Fit Seeding
- Separated observation noise generation from network initialization in `experiments/wp05/run.py` and `src/mm_allee/validation.py`.
- `noise_seed = seed`, while `fit_seed = fit_seed_offset + seed` (default offset 1000). Both seeds are recorded explicitly in prediction and parameter metric tables.
- JAX PRNG keys `jax.random.PRNGKey(fit_seed)` initialize weights and parameters before training loops commence.

### 4. [Resolved] Error Target Labeling & Clean Reference Comparison
- Prediction metrics now evaluate against both noisy test observations (`test_rmse`, `test_mae`, `test_relative_l2`) and clean held-out reference trajectories (`test_clean_rmse`, `test_clean_mae`, `test_clean_relative_l2`).
- Removed guessed fallback truth; ground truth metadata is loaded strictly from `data/fixtures/wp03_reference/truth.json` (raising `KeyError` if any case is absent).

### 5. [Resolved] Honest Scientific Reporting
- Rewrote `report/sections/05_inverse_validation.tex` to present empirical results accurately:
  - PINN parameter recovery error on clean Model A regular data is $\approx 93.6\%$ for $A$ and $\approx 58.5\%$ for $H$ due to validation early stopping freezing the trajectory before physical parameters converge to ground truth. In contrast, the conventional ODE least-squares baseline recovers parameters to $< 10^{-7}$ relative error.
  - Reported statuses across all runs: 54 validation-stopped PINN fits, 52 converged ODE fits, and 2 evaluation-limit ODE failures (`nfev_exceeded` on severe collapse).
  - Explicitly disclosed held-out trajectory breakdown in the extrapolation window ($t > 6.4$).

### 6. [Resolved] Notebook JAX Migration
- Updated `notebooks/sections/05_inverse_validation.ipynb` and `notebooks/project.ipynb` to import and execute `NetworkConfig` and `InversePINNTrainer` directly from `mm_allee.pinn`.
- Removed stale PyTorch imports and verified executable JAX training workflow.

## Validation Status

- **WP04 / WP05 Unit Tests:** 70 / 70 passed in Google Colab (Linux, Python 3.13.18, JAX 0.5.0).
- **Final Sweep Wall Time:** 464.2 s (Google Colab CPU).
- **PR:** Updated on branch `wp05/rohan-inverse-validation` (Draft PR #7).
