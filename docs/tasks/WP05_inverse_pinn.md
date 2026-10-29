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

- **Owner:** Rohan (`rohanagrawal28`); Devam requested uploading his supplied ZIP on his behalf. Technical PR author is Devam; Rohan stays assignee/code owner.
- **Branch/PR:** `wp05/rohan-inverse-validation`, [draft PR #7](https://github.com/devam2006/mm-allee-harvesting/pull/7), based on WP03 PR #4 (`wp03/collapse-analysis`, `6ba1555`); retarget to main after the dependency merges.
- **Delivered for review:** constrained PyTorch inverse trainer, SciPy ODE fit, noise/split utilities, WP05 tests/configs/runner, submitted figures/tables/report/notebook. No acceptance checkbox or human understanding claim is marked complete solely from the ZIP.
- **Evidence and exact next steps:** see [submission review](../WP05_SUBMISSION_REVIEW.md) for actual checks, reproduction commands and blockers. First reconcile results (33 supplied prediction records vs 108 configured) and the independent PyTorch engine with WP04's JAX PR #6. Preserve failed seeds and disclose the physics-supported prediction domain.
- **Source record:** `artifacts/manifests/wp05_submission.json` contains archive/import hashes. Existing WP03 code/fixtures/sections are retained; assembled notebook is regenerated from current fragments.
- **Question for owner defence:** why can a fitted trajectory look accurate while the inferred parameters are wrong, and what additional information makes Model B identifiable?
- **Pending:** corrected evidence, final sweep, all core acceptance checks, framework/API agreement, non-owner reproduction and required human approvals. Never merge on the basis of the submitted `completed` manifest alone.

PR #7 is assigned to Rohan; review requests were verified for Prem-Mehta03, AshChan07 and RaghavSinghal15. Intake validation: 27 WP05 / 207 full-suite tests passed, CPU smoke completed and 13 notebook code cells ran. Lint/format, final result reconciliation, shared-engine integration and full Jupyter execution remain unresolved; see the linked review.
