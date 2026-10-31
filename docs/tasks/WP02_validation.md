# WP02 validation and PR handoff

## Problem and result

WP02 owner: @AshChan07. Implement Model B equilibrium records, two explicitly distinct comparison protocols, and state-continuous harvesting histories for A/B with separate restocking. Add tests, reproducible synthetic evidence, section 2 of report/notebook, three editable slides and a five-minute script.

Dependency: [PR #9](https://github.com/devam2006/mm-allee-harvesting/pull/9)
now incorporates integration PR #11 at `649e0c1`, including corrected WP01
`b83bba8`, WP03 `16a05ce` and WP02 compatibility fixes `879b110`.
The fast-forward preserves all three owned report/notebook fragments and the
integration decisions. Shared thresholds use exact computed-control equality;
initial-state uncertainty remains `boundary_unresolved`. WP02 retains its
conservative input exclusion independently of equilibrium topology. Raghav's
review of #11 accepts the shared convention. All four latest-head approvals
are still required; no PR has been merged into main.

## Review corrections (31 October 2026)

- Adopt current WP01/WP03 via #11, including shared threshold/basin regressions.
- Preserve the obsolete-import fix and reject unsupported RK45 rtol before output,
  using the shared minimum constant.
- Correct stale absolute-fold wording, document unrepresentable-root
  `ArithmeticError`, and hash the newly shared threshold/basin dependencies.
- Regenerate WP02 evidence and the portable classical notebook; replace publishing
  blockers and the PR template with actual evidence.

## Portability follow-up (31 October 2026)

The latest review found that dependency hashes used native `Path` string formatting,
which yields backslash keys on Windows while the provenance test expects stable
slash-separated names. The manifest now serializes keys with
`Path.relative_to(root).as_posix()`, and the regression asserts that all source
hash keys contain no backslashes while checking both shared dependency hashes.
The focused test was rerun on macOS; a native Windows run was unavailable here.

## Scientific evidence

Config: configs/wp02.json; manifest: artifacts/manifests/wp02_run.json (source hashes and dirty development state recorded). Deterministic CPU run, 120-second budget; no neural training or empirical observations.

At a=0.2, unassisted populations fail to recover after both tested harvest ramps. A extinction tau: 13.436601 / 34.612578 for dwell 1 / 3. B first sampled x<=1e-6: 20.4 / 42.0; these are not exact extinction times. Explicit addition of 0.6K at zero harvest restores x approximately 1. Refinement population/event errors are below 2e-9 versus declared 2e-7 limits. Changing dwell changes both speed and exposure, so this is not an isolated causal speed estimate.

| Core claim | Independent evidence | Command / observed result and limits |
|---|---|---|
| B equilibria, discriminant and zero stability | test_discriminant_regimes_and_independent_polynomial; test_threshold_by_independent_maximisation; test_near_fold_roots_remain_distinct | pytest tests/wp02; 60-digit expanded-polynomial roots and independent bounded maximisation, including near a=1 |
| Stability / semistability | test_phase_signs_and_perturbed_trajectories | Direct shared RHS signs and perturbed RK45 trajectories; finite-difference derivative at zero |
| Fair comparison and units | test_protocols_have_distinct_meanings_and_correct_units; test_outcomes_do_not_depend_on_short_observation_horizon | Initial catch equality H=hN0; threshold fraction separate; theoretical outcome distinct from short-horizon events |
| Realised catch | test_realised_catch_quadrature_converges | Double sample density and tighter solver, relative catch agreement 2e-5 |
| Continuous history and shutdown | test_segments_match_uninterrupted_constant_control; test_shutdown_and_declared_restock; test_zero_stays_zero_and_insufficient_restock_fails | Uninterrupted-solve comparison, exact boundary carry-over, absorbing A shutdown, no B cutoff reset |
| Explicit restocking and two ramp speeds | test_ramp_carryover_and_tolerance_convergence; test_experiment_outputs_and_provenance | Both models, dwell 1 and 3, exact declared addition, refinement and curated summary |
| Effective settings and provenance | test_invalid_solver_settings_fail_instead_of_only_entering_manifest; test_experiment_outputs_and_provenance | Invalid solver settings fail; output checksums verified; failed-run manifest recorded |

## Validation

Run from repository root with .venv (31 October 2026):

- `.venv/bin/python -m pytest -q`: 421 passed, 1 skipped (optional Torch absent).
- `.venv/bin/python -m pytest tests/wp02 tests/test_classical_integration.py -q`:
  48 passed after the final source edits (40 WP02 plus 8 integration cases).
- `.venv/bin/ruff check .`; `.venv/bin/ruff format --check .`: pass.
- `.venv/bin/python scripts/sync_team.py --check`: current.
- `.venv/bin/python scripts/assemble_notebook.py`: 43 cells.
- `JUPYTER_CONFIG_DIR=/private/tmp/wp02-jupyter-config JUPYTER_RUNTIME_DIR=/private/tmp/wp02-jupyter IPYTHONDIR=/private/tmp/wp02-ipython MPLCONFIGDIR=/private/tmp/wp02-mpl .venv/bin/jupyter nbconvert --to notebook --execute notebooks/project.ipynb --output project.review-executed.ipynb --output-dir results --ExecutePreprocessor.timeout=120`: fresh-kernel execution succeeds.
- `MPLCONFIGDIR=/private/tmp/wp02-mpl .venv/bin/python experiments/wp02/run.py --config configs/wp02.json --output results/wp02-review --curate`: success, 1.465 s, within the recorded 120-second budget.
- `MPLCONFIGDIR=/private/tmp/wp02-mpl .venv/bin/python experiments/wp01/run.py --config configs/wp01.json --output results/wp01-review`: succeeds, 11 files and manifest.
- `MPLCONFIGDIR=/private/tmp/wp02-mpl .venv/bin/python experiments/wp03/run.py --config configs/wp03.json --output results/wp03-review`: succeeds, 1.974 s within the 60-second budget; seven analysis CSVs.
- `.venv/bin/python scripts/assemble_notebook.py --packages 1 2 3 --output notebooks/wp01_wp03.ipynb`
  and `.venv/bin/python scripts/export_standalone_notebook.py --packages 1 2 3`:
  portable classical snapshot rebuilt with current sources and evidence.
- `git diff --check`: pass.

Cross-package evidence: `test_shared_thresholds_and_adjacent_control_topology`
checks below/at/above-fold roots and stability for both models;
`test_logistic_adjacent_controls_are_not_merged` checks logistic topology;
`test_comparison_propagates_basin_uncertainty` checks the starting-population
uncertainty contract. `test_unsupported_rtol_is_rejected_before_creating_output`
checks early rejection, and `test_experiment_outputs_and_provenance` checks the
new dependency hashes.

Portability follow-up command:
`.venv/bin/python -m pytest tests/wp02/test_experiment.py::test_experiment_outputs_and_provenance -q`;
result: passed on macOS. Windows path normalization is covered by the explicit
forward-slash assertion, but this checkout did not run on Windows.

Raghav reported independent reproduction of 40 WP02 tests and the default
experiment on `879b110`, and approved that snapshot. This is not approval of
the later branch updates. CI passed on that earlier head; new-head CI must be
checked after publication. All four latest-head human approvals remain required.

The report is now maintained separately in Overleaf by the group; this pass
preserves its owned repository sections but does not claim a new report compile.
Existing three editable WP02 slides and raster PDF companion remain available.
Final five-person slide assembly and actual rehearsal remain pending; optional
relaxation-time analysis is deferred. No human understanding is certified.

## Handoff checklist

- [x] Code, meaningful tests, config and reproduction instructions included.
- [x] Completed core acceptance items mapped to independent evidence with limitations.
- [x] Report/notebook section and PNG + EPS figures included.
- [ ] Proposed interfaces reviewed by affected owners.
- [x] Actual AI use and synthetic-data limitations recorded.
- [x] No environment, secret, bulk trajectories or weights included.
- [x] Request reviewers: @devam2006, @Prem-Mehta03, @rohanagrawal28, @RaghavSinghal15; assign @AshChan07.
- [ ] Independent reproduction, four human approvals, green CI, and non-author merge.
