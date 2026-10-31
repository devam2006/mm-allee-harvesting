# WP05 — Inverse PINNs, identifiability and held-out validation

<!-- team-sync:owner:start -->
**Owner:** @rohanagrawal28. See [team.json](../../team.json) for the current choice.
<!-- team-sync:owner:end -->

**Effort guide:** 18–22 h using WP04's shared engine; reduce optional joint fits before increasing compute. **Dependencies:** WP03 datasets, WP04 PINN API. Begin algebra, splits and the conventional fit baseline immediately.

## Task 5 in plain language

Here you start with noisy population observations and try to infer unknown model parameters. You will ask both whether predictions are good and whether the parameters are actually determined by the data—these are different questions. Reuse Task 3’s data and Task 4’s neural engine. You also combine the notebook and acknowledgements.

**Numerical handoff:** [WP03's clean RK45 references and generator](../WP03_RK45_HANDOFF.md) provide both A/B, stable IDs, units and separate truth. You own observation selection, noise construction, frozen train/validation/test splits and leakage tests; the supplied CSVs are clean references, not your final fitting dataset. Known-K conditions are separate from evaluation-only unknown parameters.

**Using an agent?** It should read this full brief, explain a small example first, then work through one meaningful piece at a time: explain -> implement -> test -> interpret. Tell it whether you want guided implementation, explanation only or hints while you code. See the [first-session guide](../START_HERE.md); the shared agent workflow is [AGENTS.md](../../AGENTS.md). The detailed deliverables below are its checklist as well as yours.

**Testing requirement:** implement this brief's core acceptance tests and follow the [shared evidence rules](../TESTING.md#required-evidence-for-every-task). Map each completed claim to named tests or reproducible experiments, use independent checks and justify tolerances; report/notebook/figure and integration duties are also required.

## Goal and scope

Own items 13–14, data-label auditing, AI acknowledgement consolidation and notebook assembly. Estimate unknown parameters under a valid experimental design, report noise/held-out errors, and explain when the observations cannot determine parameters uniquely.

## Core design and subtasks

1. **Identifiability first:** derive B's three polynomial combinations and reproduce the explicit two-parameter-set counterexample in the scientific contract. Explain why multiple initial states at the same unknown effort still do not identify all four `r,A,K,h`.
2. **Staged inference for both A/B:** begin a small known-scale subset (e.g. A/H or A/h with r,K fixed). Then use independently declared known K and fit `r,A,H` or `r,A,h` as the main multidimensional experiment. All-four A recovery is an extension, with practical-conditioning/multi-start checks. An all-four B fit is only a documented nonidentifiability demonstration unless the experiment design changes and is justified.
3. Use fixed known time/population reference scales; never use hidden true unknown K/r in data preprocessing. Implement positive/order constraints (e.g. positive r, nonnegative harvest, `0<A<K`) without detaching gradients. Do not claim a narrow artificial bound supplies identification from data.
4. Extend the shared engine with data loss using **training observations only**. Validation determines stopping/hyperparameters. Freeze choices before final test evaluation. Audit 60/20/20 contiguous time splits and distinguish physics-supported prediction from extrapolation outside a collocation domain.
5. Implement a SciPy nonlinear least-squares **ODE-fit baseline** using the same observations/unknowns/bounds/scales and separate runtime reporting. Compare parameter recovery and held-out trajectories, not only training loss.
6. Run noise levels 0, 1%, 5% of fixed N_ref, seeds 11/22/33, on nontrivial regular A/B trajectories. Use measured smoke budgets before full sweeps. For near-fold/extinction, add at least one failure case per model and report nonconvergence/ambiguity honestly.
7. Include parameter error by parameter, test RMSE/MAE/relative L2, train/val losses, seed-level tables, run status and runtime. If noise makes joint recovery unreliable, report that instead of changing the target secretly. A small trajectory error does not establish accurate parameters.
8. Assemble five notebook fragments into **one executable** `notebooks/project.ipynb`, ensuring explanations/equations/algorithms precede code. Consolidate data labels and actual AI-use records into report/notebook disclosure sections. All five provide entries; WP05 owner edits their shared presentation.

## Deliverables

| Output | Content |
|---|---|
| `src/mm_allee/pinn/inverse.py`, `inference.py`, `validation.py` | Inverse trainer, conventional fit and split/metric audits |
| `experiments/wp05/run.py`, `configs/wp05_smoke.json`, `wp05_final.json` | Reproducible staged inverse/noise/failure analysis |
| `tests/wp05/test_*.py` | Starter split/ambiguity tests plus inference acceptance below |
| `artifacts/figures/wp05_recovery_noise.png/.eps` | Parameter recovery/error versus noise for both models |
| `artifacts/figures/wp05_heldout_failure.png/.eps` | Disclosed train/val/test regions and near-fold failure examples |
| `artifacts/tables/wp05_parameter_metrics.csv`, `wp05_prediction_metrics.csv` | Per seed noise/model/method results, truth/fit/errors/status |
| `report/sections/05_inverse_validation.tex`, `notebooks/sections/05_inverse_validation.ipynb` | Inverse derivation, identifiability, validation, failures and limitations |
| `notebooks/project.ipynb`, `docs/AI_USAGE.md`, `docs/DATA_PROVENANCE.md` | Integrated executable notebook and complete acknowledgements/labels |

Deliver future command `python experiments/wp05/run.py --config configs/wp05_smoke.json --output results/wp05`. Do not include ground-truth simulator parameters in the dictionary passed to training; keep them in evaluation metadata.

## Acceptance tests

- [ ] Exact Model B counterexample gives identical cubic coefficients/RHS/trajectories despite different `r,A,K,h`.
- [ ] Split overlap/duplicates/empty cases rejected; time windows disjoint and ordered; noise reproducible and scale definition checked.
- [ ] Trainer reads only training data, early stopping reads validation, final test evaluation occurs after freezing; test timestamps/values never become data-loss targets.
- [ ] Constraint transform enforces `r>0,0<A<K,H/h>=0`; trainable physical parameters receive nonzero gradients.
- [ ] Fixed-reference scaling chain rule verified; no truth-dependent normalisation when K/r unknown.
- [ ] Clean-data identifiable subset recovers a well-conditioned synthetic case within a declared numerical tolerance with a documented budget; separate unit-level deterministic correctness from stochastic final PINN performance.
- [ ] Conventional ODE-fit baseline validated on clean identifiable data and uses the same noise observations and parameter subset as PINN.
- [ ] Metrics handle zero norms and failure statuses; all seeds and invalid fits retained; parameter error and trajectory error are separate.
- [ ] Assembled notebook executes top-to-bottom in a clean kernel with explanatory sections and no private paths, network calls or hidden state.

## Done and human defence

- [ ] Both models have noise/held-out results, a fair conventional baseline, and difficult-case analysis with honest limits.
- [ ] Two paired figures, tables, configs/manifests, report/notebook; all-four B nonidentifiability clearly stated.
- [ ] Notebook assembled and independently executed; disclosures/provenance complete; all actual platforms/resources cited.
- [ ] Other member reproduction; four approvals; status current.
- [ ] Owner can explain parameter versus trajectory accuracy, structural versus practical identifiability in plain terms, leakage, noise and why a PINN can fit data with wrong parameters.

**Presentation:** 20–25 min: inverse setup, identifiability warning, noisy recovery and held-out results, failure/limitations, final project conclusions. All five handle 25–30 min Q&A.


## Current handoff

- **Integration update (31 Oct 2026, [PR #10](https://github.com/devam2006/mm-allee-harvesting/pull/10), written by Prem's agent at his direction; Rohan to review):** the inverse problem now uses the **shared forward+inverse setting** (tanh, two hidden layers of 32, network lr 1e-3, 300 collocation points, Adam 1000 + L-BFGS 2500 with no tolerance stop, lambda_phys 0.1, lr_params 1e-3, validation selection off; `configs/wp05_final.json`, Rohan's original in `configs/wp05_final_original_settings.json`). The 54-fit sweep was regenerated: all 54 fits ended with status `converged` (the Adam phase finished and a finite solution was returned), L-BFGS stopped at its iteration limit in every one (no tolerance reached, no optimiser error or abnormal exit; see the `lbfgs_outcome` column), and the 36 noisy fits are at the noise floor (training RMSE 0.65 to 1.15 times the noise sd, median 0.87) (originally all 54 `validation_stopped`); clean data, every parameter within 5%: **10/18 (originally 0/18)**; ODE least squares 18/18. A near-fold and B decline were not reliably recovered by the tested settings (condition numbers 1e3 to 2e4, which magnify small trajectory-fitting errors; r and A collapse along a degenerate valley); under noise only A regular and B regular at sigma 0.01 are informative (Cramer-Rao bound <= 25%) and there 6/6 fits are within twice the bound. `InversePINNTrainer` gained two optional arguments with unchanged defaults (`lbfgs_ftol`/`lbfgs_gtol`, `validation_selection`); `experiments/wp05/run.py` passes them through; one stale smoke-test assertion and the lint/format errors were fixed. The report section (`05_inverse_validation.tex`, from "Experimental Design and Results" onward and the optimiser paragraphs) and the notebook fragment were rewritten for the new results; the identifiability theory sections are unchanged. The bullets below describe the state under Rohan's **original** settings and numbers (history).

- **Owner:** Rohan (`rohanagrawal28`); Devam requested uploading his supplied ZIP on his behalf. Technical PR author is Devam; Rohan stays assignee/code owner.
- **Branch/PR:** `wp05/rohan-inverse-validation`, [draft PR #7](https://github.com/devam2006/mm-allee-harvesting/pull/7), based on WP03 PR #4 (`wp03/collapse-analysis`, `6ba1555`); retarget to main after the dependency merges.
- **Status & Reconciled Implementation (original settings, before the integration update above):**
  - JAX engine unified with Prem's WP04 engine (`network.py`, `residual.py`, `autodiff.py`, `train_forward.py`).
  - Two-phase inverse optimization implemented: Phase 1 Adam (with separate learning rates for weights vs physical parameters, and validation early stopping) followed by Phase 2 L-BFGS refinement (`scipy.optimize.minimize` via `ravel_pytree`).
  - Noise generation seed (`seed`) separated from fit initialization seed (`seed + 1000`), both recorded in metric CSVs.
  - Evaluation against clean reference trajectories (`test_clean_*`) added alongside noisy observation metrics (`test_*`).
  - Guessed fallback truth removed; ground truth metadata loaded strictly from `data/fixtures/wp03_reference/truth.json`.
  - Full 108-run sweep reproduced in Colab: 108 prediction records and 324 parameter records generated in `artifacts/tables/wp05_{prediction,parameter}_metrics.csv`.
  - Figures regenerated with explicit scales and splits: `artifacts/figures/wp05_recovery_noise.{png,eps}` and `artifacts/figures/wp05_heldout_failure.{png,eps}`.
  - Report (`report/sections/05_inverse_validation.tex`) and notebooks (`notebooks/sections/05_inverse_validation.ipynb`, `notebooks/project.ipynb`) rewritten to document pure JAX execution, honest recovery errors (PINN relative error $A \approx 93.6\%$, $H \approx 58.5\%$ vs ODE $< 10^{-7}$ on clean Model A), and test extrapolation limits ($t > 6.4$).
- **Pending:** Peer review from teammates (Prem-Mehta03, AshChan07, RaghavSinghal15), WP03 PR #4 merge, and retargeting PR #7 to main.

- **WP05-only notebook handoff (31 October):** Rohan's supplied clean-data parameter-trajectory demo and 1% noisy ODE/PINN comparison are integrated only into WP05. The demos use their explicitly recorded illustrative settings; the frozen benchmark/config is unchanged. All non-WP05 cells are identical to the prior final version. Fresh kernel: 29 code cells, zero errors, 36.37 s; full suite 531 passes. New WP05 PNG/EPS figures and optimizer trace are recorded in [WP05 notebook update](../WP05_NOTEBOOK_UPDATE.md). Human review remains separate; the report template is still blank.
