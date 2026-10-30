# WP02 validation and PR handoff

## Problem and result

WP02 owner: @AshChan07. Implement Model B equilibrium records, two explicitly distinct comparison protocols, and state-continuous harvesting histories for A/B with separate restocking. Add tests, reproducible synthetic evidence, section 2 of report/notebook, three editable slides and a five-minute script.

Dependency: this branch restores WP01 PR #3 via 9a1132a. Its changes will appear in a main-based diff. This is not approval of WP01 or a bypass of its review; coordinate restoration separately before merging. WP02 comparison guards exclude WP01's unresolved near-fold/domain regimes. WP03 helpers are absent locally; its owner should review the proposed interfaces in docs/DECISIONS.md.

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

Run from repository root with .venv:

- `.venv/bin/python -m pytest tests/wp02 -q`: 38 passed.
- `.venv/bin/python -m pytest -q`: 204 passed, 1 skipped (optional Torch test; Torch absent).
- `.venv/bin/ruff check .`; `.venv/bin/ruff format --check .`: pass.
- `.venv/bin/python scripts/sync_team.py --check`: current.
- `.venv/bin/python scripts/assemble_notebook.py`: 34 cells assembled.
- `JUPYTER_CONFIG_DIR=/private/tmp/wp02-jupyter-config JUPYTER_RUNTIME_DIR=/private/tmp/wp02-jupyter IPYTHONDIR=/private/tmp/wp02-ipython MPLCONFIGDIR=/private/tmp/wp02-mpl .venv/bin/jupyter nbconvert --to notebook --execute notebooks/project.ipynb --output project.executed.ipynb --output-dir results --ExecutePreprocessor.timeout=120`: succeeds after approved local kernel networking. Earlier sandbox attempts failed on config writes/port binding.
- `MPLCONFIGDIR=/private/tmp/wp02-mpl .venv/bin/python experiments/wp02/run.py --config configs/wp02.json --output results/wp02 --curate`: success, approximately 1.4 seconds; actual duration in manifest.
- `latexmk -pdf -interaction=nonstopmode -halt-on-error -cd report/main.tex`: 12 pages, WP02 pages 7–11 visually inspected; other-package scaffolds remain.
- `git diff --check`: pass.
- Three slide renders inspected; PPTX contains native charts/table/text. PDF companion is raster because native PDF export encountered a font-runtime error.

CI has not been run for this unpublished change. Optional relaxation-time analysis deferred. Final five-person slide assembly awaits missing contributions; actual rehearsal, another human's reproduction and all four approvals remain outstanding.

## Handoff checklist

- [x] Code, meaningful tests, config and reproduction instructions included.
- [x] Completed core acceptance items mapped to independent evidence with limitations.
- [x] Report/notebook section and PNG + EPS figures included.
- [ ] Proposed interfaces reviewed by affected owners.
- [x] Actual AI use and synthetic-data limitations recorded.
- [x] No environment, secret, bulk trajectories or weights included.
- [ ] Request reviewers: @devam2006, @Prem-Mehta03, @rohanagrawal28, @RaghavSinghal15; assign @AshChan07.
- [ ] Independent reproduction, four human approvals, green CI, and non-author merge.
