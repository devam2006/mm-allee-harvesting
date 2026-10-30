# Task 3: completed analysis and reproduction

**Owner:** Devam (`devam2006`). **Branch:** `wp03/collapse-analysis`. **Review:** [PR #4](https://github.com/devam2006/mm-allee-harvesting/pull/4) (open, unmerged).
The core mathematical/computational WP03 deliverables and optional sensitivity/MSY are implemented.
Human understanding, reviews, non-author reproduction and final group integration remain pending.

**Learning guide:** [WP03 explained from the beginning](https://github.com/devam2006/mm-allee-harvesting/blob/wp03/collapse-analysis/docs/WP03_EXPLAINED.md), with plain-language
derivations, RK45, worked examples, code navigation and presentation questions.

## Run it

From the repository root, activate the ignored `.venv` from [setup](SETUP.md), then:

```bash
python -m pip install -e ".[dev,notebook]"
python experiments/wp03/run.py --config configs/wp03.json --output results/wp03
python experiments/wp03/generate_reference.py --config configs/wp03_reference.json --output results/wp03-reference
python -m pytest tests/wp03 -q
```

The first experiment writes seven CSV tables, four PNG/EPS/vector-PDF figure sets, a summary and a manifest.
The second retains the early six-case reference handoff. Add `--curate` only to intentionally refresh
their small versioned outputs. Both fail rather than publish unchecked numerical results.
The study config declares a 60-second analysis budget and caps grid sizes; the observed default
run, including plotting/export, takes a few seconds on the recorded CPU.

The [environment snapshot](../artifacts/manifests/wp03_environment.txt) records the successful WP03
Python environment, not a final five-task environment. It omits the editable package's absolute
local path: install those versions with `pip install -r artifacts/manifests/wp03_environment.txt`,
then install this checkout with `pip install -e .`. Actual reproduction checks are recorded in
[wp03_reproduction.json](../artifacts/manifests/wp03_reproduction.json).

## Read the results

| Question | Evidence |
|---|---|
| Where are the harvesting cliffs? | [threshold table](../artifacts/tables/wp03_thresholds.csv), [threshold API](../src/mm_allee/thresholds.py) |
| Which initial populations persist? | [basin figure](../artifacts/figures/wp03_basins.png), [representative cases](../artifacts/tables/wp03_basins.csv), [classifier](../src/mm_allee/collapse.py) |
| How long does A take to hit zero? | [extinction figure](../artifacts/figures/wp03_extinction.png), [427 evaluations](../artifacts/tables/wp03_extinction.csv), [event checks](../artifacts/tables/wp03_event_validation.csv) |
| Why can collapse look delayed? | [bottleneck figure](../artifacts/figures/wp03_bottleneck.png), [scaled-time table](../artifacts/tables/wp03_bottleneck.csv) |
| How do r,K,A affect the cliff? | [sensitivity table](../artifacts/tables/wp03_sensitivity.csv), [optional figure](../artifacts/figures/wp03_sensitivity_yield.png) |
| What is maximum sustainable yield? | [yield curve](../artifacts/tables/wp03_yield.csv), [MSY and margins](../artifacts/manifests/wp03_summary.json) |
| Where are derivations and algorithms? | [report section](../report/sections/03_collapse.tex), [executable fragment](../notebooks/sections/03_collapse.ipynb) |
| Where are source/config/file hashes? | [analysis manifest](../artifacts/manifests/wp03_analysis.json), [config](../configs/wp03.json) |
| What is left for the final submission? | [readiness audit](../artifacts/manifests/wp03_submission_audit.json), [integration guide](INTEGRATION.md) |

Every new PNG has EPS and vector PDF partners with the same stem. All data are synthetic in declared model
units; there is no real-world species dataset here. Four new figures are supported by tables;
full basin colour grids are generated analytically in memory, with exact boundary curves overlaid.

For r=0.7, K=100, A=20: N_star=70.55050463, H_c=36.75966303, h_c=0.56, logistic H_c=17.5.
H is population/time; h is inverse time. These different numbers are not a unit-consistent risk ranking.
The largest default event-time disagreement among quadrature, two RK45 tolerances and independent
DOP853 is below 4.6e-8 dimensionless time. B's MSY effort is 0.5210404, about 6.96% below its
effort cliff. Initial-state basin margins must still be checked.

## Scientific decisions to preserve

- A with positive constant catch stops at zero; zero is not an equilibrium. No artificial zero
  tail belongs in the original ODE residual. Zero-catch A and positive-start B decline asymptotically.
- Classify before quadrature. Below the fold, an intervening root prevents extinction; at the
  double root, distinguish below/exactly at/above. Never integrate through an equilibrium pole.
- `classify_basin` recognises exact returned roots. A non-exact initial state within 2e-12
  dimensionless population units of the unstable/semistable boundary is explicitly unresolved.
  This tolerance does not merge distinct harvest controls into the fold. Disable it only with
  an explicit precision justification. Extreme parameter limits can exceed float resolution.
- Blank extinction-time cells mean no finite extinction or unresolved classification, with a
  separate outcome label. They do not mean zero or failure to observe an event within a chosen horizon.
- The 28 October recheck fixed tiny-positive-catch brackets and near-boundary integral evaluation.
  A roots use product-form brackets away from the fold and the stable offset form near it.
  Near a subcritical barrier the integral uses a logarithmic variable; at the fold it uses an
  elementary antiderivative (`fold_closed_form`, with no quadrature-error estimate). Rounded
  endpoint roots at positive catch are not certified as exact A equilibria.
- The inverse-square-root bottleneck applies when a fixed start above the fold passes through
  it after collapse. It is distinct from local pre-collapse relaxation and need not hold for a
  start already below the slow region. The transformed quadrature resolves the narrow peak.
- Sensitivities hold other dimensional r,K,A fixed. The a sweep holds r,K fixed and changes A.
- A's stable-branch yield supremum is at the semistable cliff. B's upper-branch realised-yield
  maximum is interior in effort. Both still require the initial population to exceed its barrier.
- The two illustrative policy margins use different catches and do not establish universal A/B risk.

## Claims mapped to executable evidence

| Claim | Named independent check |
|---|---|
| A/B critical controls and curvature | `test_thresholds_match_independent_bounded_maxima` |
| Distinct near-critical controls retained | `test_adjacent_controls_are_not_silently_merged_into_fold` |
| Zero/subcritical/fold/supercritical basins and exact roots | `test_all_basin_regimes_and_exact_initial_roots`, `test_basin_labels_agree_with_independent_polynomial_dynamics` |
| Finite A times and tolerance convergence | `test_extinction_quadrature_matches_two_rk45_tolerances_and_independent_dop853` |
| Tiny catch and rounded endpoints | `test_small_positive_catch_preserves_brackets_and_reaching_zero_paths`, `test_rounded_endpoint_roots_are_not_called_exact_positive_catch_equilibria` |
| Near-boundary integral conditioning | `test_close_below_fold_time_matches_independent_rescaled_rational_integral`, `test_subcritical_near_boundary_integral_matches_high_precision_polynomial` |
| Non-finite paths never integrated as extinction | `test_no_quadrature_is_attempted_through_equilibria_or_on_nonfinite_paths` |
| Bottleneck asymptotic | `test_bottleneck_inverse_square_root_asymptotic` |
| Dimensional sensitivity and scale identities | `test_dimensional_sensitivity_matches_central_differences_and_homogeneity` |
| Interior B MSY | `test_b_msy_is_interior_maximum_yield_not_maximum_effort` |
| Clean CSVs and independent error detection | [reference/sampling tests](../tests/wp03), including deliberate wrong-RHS corruption |
| Import safety, failed-run publication, budget, hashes and readiness blockers | [study/readiness tests](../tests/wp03/test_study_and_readiness.py) |

Root tests use independently expanded polynomials and trajectories, not just a duplicated closed form.
After the 28 October recheck: **142 WP03 tests passed; full suite 185 passed, one optional Torch
test skipped locally**. All seven refreshed numerical tables and the summary repeat byte-for-byte
in the second isolated venv; the six clean reference CSVs remain unchanged.
Event acceptance is 2e-7 + 5e-7*tau_ext in dimensionless time. Population reference tolerances and
the original six-case results remain in the [RK45 handoff](WP03_RK45_HANDOFF.md). Numerical error
estimates do not constitute interval-arithmetic certification or a guarantee for every possible parameter.

## Final integration duty

```bash
python scripts/assemble_notebook.py
jupyter nbconvert --to notebook --execute notebooks/project.ipynb --output project.executed.ipynb --output-dir results
python scripts/check_submission_ready.py --output results/submission-readiness.json
```

The readiness command returns 1 when blockers exist and lists all of them. That is the expected
current result: other group sections are unfinished and final metadata/artifacts are missing.
After all five tasks integrate, freeze the final environment, reproduce the full notebook/experiments,
compile and visually check the final report, then run `python scripts/package_submission.py` and
reproduce the extracted ZIP. A final ZIP is not fabricated from the incomplete group scaffold.

On 28 October 2026 the current main tree matched the original scientific scaffold after a revert
on 26 October. This branch restores only the prior WP03 numerical/handoff change from PR #2 before
adding the remaining analysis. It does not restore or rewrite the other members' implementations.
The earlier portable Rohan notebook remains pinned to its original source snapshot; this PR does not
change his noise/split/inverse ownership.

Learning later: [five-minute presentation notes and defence questions](../presentation/wp03.md).
Those notes are a study aid, not certification that the human owner has learned the material.

## Raghav's PR #4 review follow-up, 30 October 2026

[Review addressed](https://github.com/devam2006/mm-allee-harvesting/pull/4#pullrequestreview-5705535562).

| Point | Change and evidence |
|---|---|
| B small lower root loses relative precision | Compute `upper` first and `lower=a*(1+e)/upper`; retain an explicit repeated fold. `test_b_lower_root_matches_high_precision_polynomial_at_small_allee_ratio` checks 80-digit independent polynomial bisection, relative error within 8 eps, and basin outcomes on both sides, including both reported examples. |
| Persistence strip above critical harvest | Plot the two control regions separately with an exact edge at 1; the fold is a line. `test_basin_mesh_cannot_draw_persistence_above_the_fold` inspects actual coloured-cell coordinates for A/B with and without a sampled fold. PNG and vector PDF inspected. |
| WP01/WP03 fold convention | Preserve WP03's exact computed-control equality. Document WP01 #8's current 64*eps relative band and possible API disagreement in INTERFACES/DECISIONS; unification is a reviewed integration item. |
| Raster report figures | Export/curate/hash all four vector PDFs alongside PNG/EPS. Report references omit extensions. All four PDFs contain zero embedded raster images; revised six-page report compiled with Tectonic and WP03 pages visually inspected. One underfull table-cell warning remains; no overfull boxes or undefined citations. |
| Merge order | Preserve both PRs' interface/decision entries and notebook fragments; reassemble and execute the combined notebook when the second PR merges. Not attempted ahead of human reviews. |
| Extinction conditioning | Report/notebook state `d tau_ext/d x0 ~ 1/[f'_A(x_-)*(x_--x0)]`: rounding is amplified near the barrier, separately from integration error. |

Observed on Windows / Python 3.14.3 with the existing ignored review environment:
**150 WP03 tests; 194 full-suite tests passed**, including the optional Torch test.
Ruff lint/format, ownership sync, smoke and whitespace checks passed. The default
experiment retained all seven table row counts (6/427/34/7/6/61/6). The six clean
reference CSVs remain unchanged. Historical 28 October environment/reproduction
records above describe that earlier run; the current run's versions, source and
output hashes are in `wp03_analysis.json`, with follow-up checks/limitations in
[wp03_review_followup.json](../artifacts/manifests/wp03_review_followup.json).
Curated text outputs are normalised to LF before hashing so Git's line-ending conversion
does not invalidate its checksum on another platform.
The assembled notebook's nine code cells passed in order in a fresh Python
process (10.68 s), including analysis and six-case reference regeneration.
Local Jupyter/nbconvert launch attempts stalled and were stopped; a full local
kernel run is unverified. GitHub CI checks the real kernel on the updated PR.

## Latest-head integration and tolerance follow-up (31 October 2026)

Verified by GitHub API and fresh Git fetch: Raghav's original WP01 PR #3 is
merged/closed (then reverted on main); its replacement is PR #8 at f427d5f,
including the original fixes in c47084e and regenerated evidence in 350cd7c.
WP03 PR #4 was at 2a2f673 and WP02 PR #9 at a6ad5d3. The original WP01 review
examples pass at #8's current head; the old code restored in #9 is not that head.

An additional probe found our own configurable reference API accepted
`rtol=1e-16` while initialized RK45 used 2.220446049250313e-14. The shared solver
and dataset configuration validator now reject unsupported small requests.
Eight new tests cover early rejection (including initial-zero fast paths),
reference CLI rejection before output creation, and the actual initialized
integrator tolerance at the accepted floor. This is a preflight/provenance fix:
the default settings, exact-control fold convention and numerical algorithms
are unchanged.

The follow-up also checks validation at the accepted floor: the refinement
uses the supported minimum rtol, still tightens atol/max_step, and records the
actual refinement rtol and whether it is at the floor. Its evidence CSV gains
these two fields; the six observation CSVs and their numerical arrays do not
change. This avoids rejecting a valid accurate baseline during verification.

Observed checks in the existing Windows/Python 3.14.3 review environment, with
UTF-8 and this checkout's source selected explicitly:

- `python -m pytest tests/wp03 -q`: **158 passed**.
- `python -m pytest -q`: **201 passed, 1 skipped** (Torch absent).
- Ruff lint/format, ownership sync, smoke and whitespace checks: passed.
- Default analysis run: all seven tables reproduced, with row counts
  6/427/34/7/6/61/6. All seven CSVs are byte-identical to the pre-fix run in
  this same environment.
- Clean reference generation: six trajectories passed independent validation.
  Exact arrays and event values match the original 2a2f673 implementation in
  all six cases. Existing curated fixtures were not rewritten.
- A temporary combined tree used current WP01/WP02 owned sources on WP03,
  plus this tolerance fix and one proposed **WP02-only** import repair:
  remove the deleted `FOLD_TOL` import and retain WP02's existing absolute
  input-exclusion guard as its own named constant. **408 tests passed,
  1 skipped**, lint/format passed, and WP02's default experiment reproduced.
  All **17 combined notebook code cells** passed in a fresh headless Python
  process (41.86 s in the final check). This is not a Jupyter kernel claim or a merged-tree claim;
  the WP02 proposal has not been applied to Ashwath's branch. An initial
  sequential run with an interactive plotting backend was stopped; the
  successful check explicitly used Agg.

The exact fold-policy agreement remains pending. Do not broaden WP03's control
classification merely to match a plotting tolerance: a genuinely supercritical
path has finite extinction, whereas a true fold has an equilibrium pole.
The concrete proposal is shared threshold values and exact computed-control
equality for topology, with any floating-point band reported separately as
numerical uncertainty; WP03's initial-state `root_tol` stays separate. Raghav
must confirm the WP01 convention before claiming unified edge-case outputs.
Ashwath and Devam can continue regular-regime integration using the current
reviewed sources and a conservative exclusion guard without waiting for that
decision. Two narrow WP01 follow-up examples remain documented in #8's review;
they do not invalidate the default experiments or require repeating the original
fixes. Source hashes and measured evidence are in
[wp03_tolerance_followup.json](../artifacts/manifests/wp03_tolerance_followup.json).
