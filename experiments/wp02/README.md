# Reproduce Task 2

From the repository root, after installing `.[dev,notebook]` into `.venv`:

```sh
.venv/bin/python -m pytest tests/wp02 -q
.venv/bin/python experiments/wp02/run.py --config configs/wp02.json --output results/wp02
```

Add `--curate` to copy small figures (PNG/EPS/PDF), equilibrium/comparison/history-summary
CSVs and a manifest to `artifacts/`. Bulk history samples stay under ignored `results/`.
The numerical run has a recorded 120-second CPU budget checked between solves;
it is deterministic and does not train a neural network. The first CPU smoke run
completed successfully; actual timings and source checksums are in the manifest.
If Matplotlib cannot write its usual cache, set `MPLCONFIGDIR=/private/tmp/wp02-mpl`.

## Evidence and units

- `wp02_b_branches`: positive/zero equilibrium branches, stable/unstable/fold labels.
- `wp02_b_equilibria.csv`: records with **e**, not A's q, plus residuals and signs.
- `wp02_comparison.csv`: two separate protocols, three models, three initial populations,
  two control fractions. Population/total catch are tonnes; time is years; catch is
  tonnes/year; effort h is per year. Parameters are illustrative, not observations.
- `wp02_history`: two staircase dwell times, both A/B, unassisted and explicitly restocked.
- `wp02_history_summary.csv`: dimensionless event/smallness times, final populations,
  restocking additions and integration-refinement errors. First sampled smallness is
  not exact extinction; tiny B tail values below absolute tolerance are not meaningful
  relative-accuracy estimates.
- `wp02_history_samples.csv`: dimensionless tau/x/control and effective catch. Duplicate
  boundary timestamps represent left/right limits. Labels identify intervention and
  extinction/shutdown rows. Only declared restocking jumps population.
- `manifest.json`: input config, source hashes, commit/dirty status, versions/hardware,
  applied solver settings, budget, outcome and output checksums, including failures.

`run_history` calls the existing constant-control solver separately for each segment.
Schedules start at zero, increase strictly and have one control per interval.
Restocking is a mapping from segment index to a positive **addition** in x units.

## Dependencies and limitations

This branch explicitly contains restored WP01 PR #3 as a dependency. Its known
near-boundary root issues are not silently repaired in WP02. Comparison APIs restrict
`0.05 <= a <= 0.95` and reject noncritical A/logistic controls inside WP01's fold
ambiguity band. The curated design uses a=0.2, fractions 0.5/1.2, away from that band.
WP03 helpers are not yet in this checkout; A uses WP01's fold helper and B uses its
own required discriminant derivation. Affected owners must review these interfaces.

Theory distinguishes persistence from a finite horizon without an event. The two
history schedules change total exposure as well as speed. They establish a recovery
barrier, not a universal policy ranking or spontaneous closed hysteresis loop.
Optional local relaxation experiments are deferred. Final group slide assembly
requires the WP03–WP05 contributions and human rehearsal; no timings are invented.
