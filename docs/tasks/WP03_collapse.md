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
5. Implement the **synthetic reference generator**: regular persistence, subthreshold/extinction and near-fold regimes for A/B, high-accuracy independent reference checks, train/validation/test observation IDs, fixed noise seeds and manifests. Agree units/scales with WP05; hand over an early small fixture before a large sweep.
6. **Optional:** threshold elasticities checked by finite differences; MSY for A/B and harvest/basin safety margins. Distinguish B maximum sustainable realised yield from maximum admissible effort. Keep extras short if core or integration needs attention.
7. Freeze a successful clean environment, rerun all final commands independently, execute the final notebook, audit output manifests and build the submission zip using `scripts/package_submission.py`. Check its contents against course requirements.

## Deliverables

| Output | Content |
|---|---|
| `src/mm_allee/thresholds.py`, `collapse.py`, `datasets.py` | Thresholds, certified extinction quadrature/basins, synthetic generator |
| `experiments/wp03/run.py`, `configs/wp03.json` | Reproduce threshold/extinction/basin results and reference data |
| `tests/wp03/test_*.py` | Existing event checks plus independent acceptance below |
| `artifacts/figures/wp03_extinction.png/.eps` | Extinction time vs state/harvest with impossible/no-event cases labelled |
| `artifacts/figures/wp03_basins.png/.eps` | Basin boundary and regime interpretation |
| `artifacts/tables/wp03_thresholds.csv` | Analytic/numeric threshold and event/quadrature comparisons |
| `artifacts/manifests/wp03_reference.json` | Reference generator provenance and split/noise contract |
| `report/sections/03_collapse.tex`, `notebooks/sections/03_collapse.ipynb` | Proofs, algorithms, evidence and interpretations |
| `artifacts/manifests/final_environment.txt`, reproduction log | Actual successful clean versions and commands |
| `submission/mm-allee-submission.zip` | Complete tested hand-in bundle, after all packages integrate |

Deliver future command `python experiments/wp03/run.py --config configs/wp03.json --output results/wp03`. Generated bulk observations stay under ignored `data/generated/` or `results/`; commit only a small documented fixture and manifests.

## Acceptance tests

- [ ] Threshold formulas match independent bounded numerical maximisation over the correct intervals for several a values; critical RHS and derivative vanish within stated tolerances.
- [ ] A event time agrees with independently evaluated quadrature; convergence checked at two tolerances and at least one alternate solver/reference.
- [ ] `q=0` subthreshold decline has no finite zero event; equilibrium/supercritical/fold cases classified correctly. At the fold, distinguish starts above and below the double root.
- [ ] Solver never emits negative physical populations and includes the exact event endpoint; initial zero and invalid inputs handled explicitly.
- [ ] Basin labels agree with long-enough trajectories away from boundaries and exact roots are not misclassified by numerical drift.
- [ ] Same generator seed/config gives identical observations and splits; different seeds change noise; truth/units/noise are explicit and all split IDs disjoint.
- [ ] Synthetic fixture contains both models and nontrivial dynamics; evaluation reference is not passed to training as labels by accident.
- [ ] Optional sensitivity and MSY claims have numerical checks and correct units/holding-fixed conventions.

## Handoff and done

- [ ] Early reference fixture/schema delivered to WP04/WP05; thresholds delivered to WP01/WP02.
- [ ] Paired plots/table, report/notebook and tests complete; threshold/extinction claims independently checked.
- [ ] Final bundle contains all required `.tex/.bib/.pdf/.eps/.ipynb` files, reproduction instructions and no credentials or bulk weights.
- [ ] Four approvals, other member reproduction, AI log/citations/status current.
- [ ] Owner can derive both thresholds, explain finite versus asymptotic extinction and demonstrate why the quadrature is valid only on a reaching-zero path.

**Presentation:** 10–15 min: thresholds, finite-time collapse, basin boundary and reference generation. Use extras only if core story and timing are clear.

## Current handoff

- **Owner:** Devam (`devam2006`) selected Task 3 on 19 October 2026.
- **Branch / PR:** `docs/agent-onboarding`, [PR #1](https://github.com/devam2006/mm-allee-harvesting/pull/1), records the choice and shared setup; scientific implementation has not started.
- **Completed:** task selection only; the acceptance checkboxes above remain open.
- **Next:** begin the WP03 derivation and review the existing solver/event tests, following the agent playbook. Coordinate roots with WP01/WP02 and an early reference-data fixture with WP04/WP05 once those owners choose.
- **Explanation to cover first:** why a positive constant catch permits finite-time extinction, and why the zero-harvest case is different.
