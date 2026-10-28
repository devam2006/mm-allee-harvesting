# RK45 reference handoff for Rohan (WP05) and Prem (WP04)

**Implemented milestone:** clean, independently checked numerical references for Models A and B. This page describes the early milestone; the [remaining Task 3 analysis is now implemented](WP03_ANALYSIS.md), with human review/learning and final integration pending. No PINN training, noisy observation files, split selection, full basin maps or threshold study is claimed here. Devam's detailed understanding/review is still pending.

[PR #2](https://github.com/devam2006/mm-allee-harvesting/pull/2) was the early reference handoff. It was merged, but a later main revert removed its files. The current wp03/collapse-analysis branch restores those WP03 files and adds the full analysis.

## Start with these files

| Need | Location |
|---|---|
| Clean regular trajectories (start here) | [A](../data/fixtures/wp03_reference/a_regular.csv), [B](../data/fixtures/wp03_reference/b_regular.csv) |
| Additional numerical cases | [A extinction](../data/fixtures/wp03_reference/a_extinction.csv), [B decline](../data/fixtures/wp03_reference/b_decline.csv), [A near fold](../data/fixtures/wp03_reference/a_near_fold.csv), [B near fold](../data/fixtures/wp03_reference/b_near_fold.csv) |
| Declared known conditions and fixed scales | [conditions.json](../data/fixtures/wp03_reference/conditions.json) |
| Evaluation-only generating parameters/events | [truth.json](../data/fixtures/wp03_reference/truth.json) |
| Config / exact provenance and file hashes | [config](../configs/wp03_reference.json), [manifest](../data/fixtures/wp03_reference/manifest.json) |
| Numerical evidence | [validation table](../artifacts/tables/wp03_reference_validation.csv), [figure](../artifacts/figures/wp03_rk45_reference.png), [EPS](../artifacts/figures/wp03_rk45_reference.eps) |
| Implementation | [solver](../src/mm_allee/solver.py), [generator](../src/mm_allee/datasets.py), [independent checks](../src/mm_allee/reference_validation.py), [CLI](../experiments/wp03/generate_reference.py) |
| Executable checks | [sampling tests](../tests/wp03/test_solver_sampling.py), [reference tests](../tests/wp03/test_reference_datasets.py), [original event tests](../tests/wp03/test_reference_events.py) |

All six CSVs contain 101 **clean synthetic** points (606 total); they are not six independent ecological experiments or a final inverse benchmark. Columns are `observation_id,trajectory_id,model,time,population,is_synthetic`. IDs are stable and unique. Values use arbitrary declared `model_time_unit` and `population_unit`; these are continuous population equivalents, not measurements of a real species. All cases use generating r=0.7, K=100, A=20; controls, starts and horizons differ:

| Case | H (A) / h (B) | N0 | Requested end time |
|---|---:|---:|---:|
| a_regular | 10 | 45 | 8 |
| b_regular | 0.21 | 45 | 8 |
| a_extinction | 70 | 80 | 5 |
| b_decline | 0.21 | 10 | 5 |
| a_near_fold | 36.5 | 85 | 30 |
| b_near_fold | 0.5544 | 85 | 30 |

The regular cases contain a transient followed by approach to equilibrium. Rohan must assess information/conditioning and can resample a shorter window or choose different initial conditions; no parameter-recovery accuracy is guaranteed. Near-fold labels are chosen benchmark regimes (about 99.3% and 99% of the A/B critical controls), not a completed threshold/basin analysis.

## Ownership boundary and data use

- **WP03:** clean solver/generator, independent numerical accuracy, stable IDs, units and provenance. No noise or splitting has been applied (`noise/splits/seeds` are null in the manifest).
- **WP05:** choose observation times/subsets, implement noise at the prescribed levels/seeds, create/freeze and validate contiguous train/validation/test splits, fit PINN and the conventional ODE baseline, and report recovery/prediction/failures. Store those observation files separately and keep the same observations for both methods.
- CSV `population` is the clean reference from which WP05 constructs observations. At zero noise it may become the target **only after splitting**. Never pass the unsplit full reference to the trainer or treat held-out clean values as additional supervision.
- `conditions.json` declares independently known K and initial population for the agreed main inverse design. Its fixed reference scales are time=1 and population=100. Do not normalise time by hidden true r. If attempting all-four A as an extension, do not read known_K; define a valid independent scale/design first. All-four B at one unknown fixed effort remains structurally nonidentifiable.
- `truth.json`, the full generation config and manifest are **evaluation/provenance metadata**, not optimiser inputs. They include true unknown parameters; inspecting them in an evaluation script does not authorise using them for initialisation, bounds, tuning, stopping or losses. A file cannot enforce this boundary by itself; WP05 must test its loader/trainer separation.
- Prem may use the references for forward evaluation, not supervised labels in a claimed physics-only forward PINN run. Evaluate only on matching physical intervals and record the reference config.

## Regenerate or change sampling

From the repository root, with the ignored venv active:

```bash
python experiments/wp03/generate_reference.py --config configs/wp03_reference.json --output results/wp03-reference
python -m pytest tests/wp03 -q
```

The output includes CSVs, known conditions, separate truth, a validation CSV, PNG/EPS figure and manifest. The run fails if its numerical acceptance checks fail. Add `--curate` to refresh the small versioned fixtures, paired figure, table and manifests; inspect and commit all those changes together. Without it, all outputs stay under ignored `results/`.

Change a copied JSON config to vary `initial_population`, `time_end`, `n_points` or dimensional `time_points` (strictly increasing, starting at zero and within time_end). `time_points` overrides the uniform output grid; it does not prescribe RK integration steps. Numerical evidence runs require at least two physical samples. A zero-initial-population boundary is supported by the solver but is intentionally not an informative validation/data-generation case.

```python
import json
from pathlib import Path
from mm_allee.datasets import generate_reference

config = json.loads(Path("configs/wp03_reference.json").read_text())
case = dict(config["cases"][0], time_points=[0, 0.1, 0.3, 0.7, 1.5, 3.0])
reference = generate_reference(case, config["solver"])
time, population = reference.time, reference.population
```

For A with H>0, the solver truncates at its first downward zero event and includes the event endpoint. Default n_points samples are uniformly spaced over that shortened interval; custom times after the event are dropped and the event endpoint is appended. **Do not append an absorbing zero tail to the original ODE data.** For B, positive populations approach zero asymptotically; no exact finite extinction is declared. A finite horizon without an event only means no event was observed within that horizon.

## Numerical evidence and limits

Default dimensionless RK45 settings are rtol=1e-9, atol=1e-11, max_step=0.1. DOP853 independently integrates the **expanded dimensional polynomial**, at rtol=1e-12 and atol=K*1e-14, and is sampled only before its own event. Tighter RK45 reduces both tolerances by 100 and max_step by two. Comparisons require sampled population differences <=5e-8*K (5e-6 here) and event-time differences <=1e-7 model_time_unit. These numerical targets are much smaller than the planned 1%/5% measurement noise, but are not guarantees about PINN accuracy or all possible parameter values.

For the supplied six cases, the largest RK45/DOP853 sampled difference is about 6.11e-7 population_unit. A extinction occurs at approximately 1.643289435 model_time_unit; the quadrature difference is below 6e-10. The actual per-case numbers are in the table. The tests also compare against an exact unharvested logistic solution and deliberately corrupt the production RHS to verify that the independent check fails.

Quadrature is used only when endpoints and interior critical points show the expanded A cubic is negative over the whole path, with a conservative margin. This avoids integrating through an equilibrium pole. It is a numerical safety check, not a rigorous interval certificate or the later full basin derivation. The figure and table support this milestone only.

CSV, conditions and truth bytes repeat in the same dependency environment. Manifests contain actual UTC time, checkout SHA/dirty state, dependency/hardware information and source/file SHA256; timestamps/runtime and figure metadata vary. Curated manifest paths are relative to the repository root. Dirty-generation records are retained honestly, and source hashes identify the exact numerical code used. Do not infer a final dependency lock or completed scientific submission from this small fixture.

## What was verified for this milestone

| Claim | Executable evidence |
|---|---|
| All six configured A/B references meet the population/event targets | `test_each_fixture_has_independent_numerical_evidence` in the reference tests linked above |
| The comparison can catch an incorrect shared ODE implementation | `test_independent_check_detects_a_wrong_production_rhs` deliberately changes the production RHS |
| Dimensional time/population conversion is consistent | `test_dimensionful_rescaling_preserves_dynamics` checks both models under changed units |
| Exports are deterministic, clean and traceable | `test_reference_exports_are_reproducible_and_do_not_create_inverse_inputs` and `test_curated_handoff_matches_manifest_and_configured_trajectories` |
| Sampling and extinction obey the physical boundary | Sampling tests plus the original event tests; quadrature rejects paths with equilibrium poles |

On 19 October 2026, the ignored `.venv` passed `python -m pytest tests/wp03 -q` (52 tests), `python -m pytest -q` (96 tests), `ruff check .`, `ruff format --check .`, `python scripts/smoke.py`, `python scripts/sync_team.py --check` and `git diff --check`. The assembled notebook's seven code cells also ran successfully in a fresh Python process. Local `jupyter nbconvert --execute` could not start its kernel because this execution environment blocks the required sockets; full notebook-kernel execution is checked separately by GitHub CI. Do not describe direct cell execution as a successful Jupyter-kernel run.

The report was compiled with `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=../results/wp03-report-check main.tex` from `report/`; its WP03 method/table/figure pages were rendered and visually checked. The remaining report sections are still scaffolds, so the compiled preview is not a completed submission. The paired PNG/EPS figure, per-case validation table and manifests are committed with this milestone.

## Current Task 3 state

Threshold proofs/APIs, basins, extinction sweeps, bottleneck and optional sensitivity/MSY are implemented in the [full analysis handoff](WP03_ANALYSIS.md). Final group reproduction/packaging depends on the other packages; human understanding and approvals remain pending. The original reference PR requested only Rohan's initial review; the full analysis uses the normal four-teammate review policy.
