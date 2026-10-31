# WP03 — Collapse thresholds, basins and numerical reference

<!-- team-sync:owner:start -->
**Owner:** @devam2006. See [team.json](../../team.json) for the current choice.
<!-- team-sync:owner:end -->

**Effort guide:** 18–22 h including reproducibility/package audit. **Dependencies:** agree foundations with WP01. Deliver reference data early to WP04/WP05.

## Task 3 in plain language

You will calculate how much harvesting the population can tolerate, which starting populations survive, and how long extinction takes when collapse occurs. You will check those calculations against a reliable numerical solver and generate the synthetic data used by the neural-network tasks. You also check that the final submission can be reproduced and packaged.

**Background:** no PINN training experience is required. This task uses calculus and numerical ODE solving with NumPy/SciPy. Tasks 4 and 5 own neural-network training; agree the reference-data format with them. The main care is in classifying boundary cases and checking numerical accuracy.

**Using an agent?** It should read this full brief, explain a small example first, then work through one meaningful piece at a time: explain -> implement -> test -> interpret. Tell it whether you want guided implementation, explanation only or hints while you code. See the [first-session guide](../START_HERE.md); the shared agent workflow is [AGENTS.md](../../AGENTS.md). The detailed deliverables below are its checklist as well as yours.

**Testing requirement:** implement this brief's core acceptance tests and follow the [shared evidence rules](../TESTING.md#required-evidence-for-every-task). Map each completed claim to named tests or reproducible experiments, use independent checks and justify tolerances; report/notebook/figure and integration duties are also required.

## Goal and scope

Own finite-time extinction (item 3), threshold derivations (4), basins (5), and the reliable numerical data used by both PINN packages. Sensitivity (9) and sustainable-yield safety margins (11) are optional extensions. Own the final independent reproduction and submission bundle.

## Subtasks

1. Differentiate the production cubic, choose the maximum in `(A,K)`, derive `N_star,H_c`. Derive B's `h_c` using its per-capita growth maximum; check the logistic `rK/4` limit/reference separately. Convert consistently to dimensionless thresholds.
2. Extend/review the event-aware RK45 wrapper and derive the extinction quadrature. Classify starts/harvests before integration: below/at/above fold and basin boundaries, `H=0`, `N0=0`. Never integrate through an equilibrium pole or label a finite horizon as proof of no extinction.
3. Compute extinction-time curves/maps versus `N0,H` in extinction regimes, compare RK45 event times with quadrature, and verify tolerance convergence. Plot the bottleneck close to the threshold. B time to a small cutoff must be distinctly named if included.
4. Produce basin diagrams with initial state and harvest; mark the unstable root, fold cases and exact equilibria. Share root interfaces with WP01/WP02.
5. Implement the **clean synthetic reference generator**: regular persistence, subthreshold/extinction and near-fold regimes for A/B, high-accuracy independent reference checks, stable observation IDs and manifests. Agree units/scales with WP05; hand over an early small fixture before a large sweep. WP05 chooses observation subsets, constructs seeded noise and train/validation/test splits, and validates leakage; do not implement its inverse pipeline here. See [the implemented RK45 handoff](../WP03_RK45_HANDOFF.md).
6. **Optional:** threshold elasticities checked by finite differences; MSY for A/B and harvest/basin safety margins. Distinguish B maximum sustainable realised yield from maximum admissible effort. Keep extras short if core or integration needs attention.
7. Freeze a successful clean environment, rerun all final commands independently, execute the final notebook, audit output manifests and build the submission zip using `scripts/package_submission.py`. Check its contents against course requirements.

## Deliverables

| Output | Content |
|---|---|
| `src/mm_allee/thresholds.py`, `collapse.py`, `datasets.py` | Thresholds, analytically classified extinction quadrature/basins, clean generator; numerical error is not interval certification |
| `experiments/wp03/run.py`, `configs/wp03.json` | Reproduce threshold/extinction/basin results and reference data |
| `tests/wp03/test_*.py` | Existing event checks plus independent acceptance below |
| `artifacts/figures/wp03_extinction.png/.eps` | Extinction time vs state/harvest with impossible/no-event cases labelled |
| `artifacts/figures/wp03_basins.png/.eps` | Basin boundary and regime interpretation |
| `artifacts/tables/wp03_thresholds.csv` | Analytic/numeric threshold and event/quadrature comparisons |
| `artifacts/manifests/wp03_reference.json` | Reference generator provenance and split/noise contract |
| `report/sections/03_collapse.tex`, `notebooks/sections/03_collapse.ipynb` | Proofs, algorithms, evidence and interpretations |
| `artifacts/manifests/wp03_environment.txt`, `wp03_reproduction.json` | WP03 environment/reproduction; final group snapshot waits for integration |
| `submission/mm-allee-submission.zip` | Complete tested hand-in bundle, after all packages integrate |

Implemented analysis command `python experiments/wp03/run.py --config configs/wp03.json --output results/wp03`. Generated bulk observations stay under ignored `data/generated/` or `results/`; commit only a small documented fixture and manifests.

## Acceptance tests

- [x] Threshold formulas match independent bounded numerical maximisation over the correct intervals for several a values; critical RHS and derivative vanish within stated tolerances.
- [x] A event time agrees with independently evaluated quadrature; convergence checked at two tolerances and at least one alternate solver/reference.
- [x] `q=0` subthreshold decline has no finite zero event; equilibrium/supercritical/fold cases classified correctly. At the fold, distinguish starts above and below the double root.
- [x] Solver never emits negative physical populations and includes the exact event endpoint; initial zero and invalid inputs handled explicitly.
- [x] Basin labels agree with long-enough trajectories away from boundaries and exact roots are not misclassified by numerical drift.
- [x] Same clean-generator config gives identical reference CSVs/IDs in the same environment; units/true parameters/provenance are explicit. Noise/split generation and its seed/leakage tests belong to WP05.
- [x] Small clean synthetic fixture contains both models and nontrivial dynamics; evaluation truth is separate from declared known conditions. WP05 still must test its trainer's leakage boundary.
- [x] Optional sensitivity and MSY claims have numerical checks and correct units/holding-fixed conventions.

## Handoff and done

- [x] Early clean reference fixture/schema is available on the Task 3 branch for WP04/WP05. Threshold/basin APIs are implemented; affected owners review the interface in this PR.
- [x] Paired plots/tables, report/notebook and tests complete; threshold/extinction claims independently checked.
- [ ] Final bundle contains all required `.tex/.bib/.pdf/.eps/.ipynb` files, reproduction instructions and no credentials or bulk weights.
- [ ] Four approvals, other member reproduction, AI log/citations/status current.
- [ ] Owner can derive both thresholds, explain finite versus asymptotic extinction and demonstrate why the quadrature is valid only on a reaching-zero path.

**Presentation:** 10–15 min: thresholds, finite-time collapse, basin boundary and reference generation. Use extras only if core story and timing are clear.

## Current handoff

- **Colab entry-point fix:** the small public `project_colab.ipynb` replaces the
  multi-megabyte encoded code cell for browser use. It downloads a pinned,
  checksum-verified runtime (or uses the copy in the handoff ZIP). Anonymous
  retrieval and a fresh 32-code-cell run passed; all 531 tests passed. Public
  hosting was explicitly requested by Devam; scientific code/results are
  unchanged. See `docs/COLAB_QUICKSTART.md` for the public notebook and rebuild
  steps. Private development history/reviews are not part of the public snapshot.

- **Latest reporting-fix update:** PR #5 now incorporates Prem's PR #10
  `00393cd` with verified validation-loss and L-BFGS reporting fixes. All ten
  source regression tests and 301 source tests passed; the integrated suite
  passed 525 tests, including four new direct forward/inverse parity cases.
  The previous statement below that two reporting defects remain open is
  historical and superseded. Next steps are owner review of shared conventions,
  settings and status vocabulary, followed by human approvals and final
  Overleaf/presentation work. See `docs/PREM_PR10_FINAL_REVIEW.md` and the E2E log.

- **31 October integration update:** source WP03 remains PR #4 `16a05ce`.
  Classical integration PR #11 `649e0c1` combines current WP01/WP02 fixes,
  shared thresholds/branches and basin conventions; 421 tests and a real
  16-code-cell portable kernel run passed. PR #5 now includes Prem PR #10
  `c84a0bf`, all five packages, and a tested notebook/data/EPS download.
  All 511 tests and both isolated 27-cell kernel runs passed. These are
  computational checks, not human scientific approval. The two WP05 reporting
  findings remain with Prem/Rohan. Next: review the shared conventions in
  `docs/CLASSICAL_INTEGRATION.md`, resolve those findings, then regenerate the
  five-package export and ZIP using `docs/END_TO_END_INTEGRATION.md`. Report
  authors work in Overleaf; no report assembly is required for this handoff.

- **Owner / branch:** Devam (`devam2006`), `wp03/collapse-analysis`; [PR #4](https://github.com/devam2006/mm-allee-harvesting/pull/4) is assigned to Devam with all four other roster members requested for review; it remains unmerged. Historical early reference handoff: [PR #2](https://github.com/devam2006/mm-allee-harvesting/pull/2).
- **Completed:** thresholds; exact/critical/zero-harvest basins; A extinction quadrature, RK45/DOP853/tolerance checks; extinction sweeps/maps; bottleneck; optional dimensional sensitivity and B realised-yield MSY/margins; clean references; report/notebook; paired figures/tables; speaking notes; WP03 environment/reproduction; submission-readiness audit.
- **Navigation/commands:** [analysis](../WP03_ANALYSIS.md), [early reference handoff](../WP03_RK45_HANDOFF.md), [speaking notes](../../presentation/wp03.md).
- **Learn the work:** [WP03 explained from the beginning](https://github.com/devam2006/mm-allee-harvesting/blob/wp03/collapse-analysis/docs/WP03_EXPLAINED.md). The 28 October recheck found and fixed tiny-catch bracketing, near-boundary integral conditioning and rounded-endpoint equilibrium labels. Post-fix evidence: 142 WP03 tests; 185 full-suite passes and one optional Torch skip locally; all seven tables repeat byte-for-byte in the second venv. Human understanding remains pending.
- **Recovery:** main at 3cfc606 matched the starter tree after a revert. This PR restores only the earlier WP03 dependency and adds the remaining work; it does not restore other packages.
- **Integration pending:** final group environment/PDF, all-task clean-kernel reproduction and submission ZIP require remaining packages, metadata and approvals. The audit lists those blockers.
- **30 October review follow-up:** addressed Raghav's PR #4 suggestions: stable B lower root, basin cells bounded at the exact critical control, vector PDF report figures and conditioning explanation. Added 8 regression cases: 150 WP03 and 194 full-suite passes. Fold convention differences and merge-order steps are documented in INTERFACES/DECISIONS; they await cross-package integration. Current evidence: [analysis follow-up](../WP03_ANALYSIS.md#raghavs-pr-4-review-follow-up-30-october-2026).
- **Next:** reviewers reproduce the exact commands; WP01/WP02 review the threshold/basin interface. When #4/#8 integrate, preserve both sets of documentation, rebuild and execute the combined notebook. WP05 retains noisy-observation/split/inverse ownership.
- **Human understanding:** pending at Devam's request. Speaking notes are study material; no human approval, understanding check or non-author reproduction is claimed.
- **31 October latest-head recheck:** verified WP01 PR #8 f427d5f, WP02 PR #9
  a6ad5d3 and WP03 PR #4 2a2f673 directly against GitHub/fetched refs. Fixed
  WP03's own unsupported-tolerance acceptance in the shared solver and reference
  config validator; 8 new regressions check early rejection and the initialized
  integrator. Original WP01 fixes remain fixed; cross-package fold policy still
  requires explicit owner agreement. See the new analysis follow-up for actual
  validation. No merge, scientific approval or final integration is claimed.
