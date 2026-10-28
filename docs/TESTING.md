# Testing and scientific acceptance

## Existing checks versus project completion

`python -m pytest -q` exercises the shared scaffold plus the implemented **WP03 clean RK45 reference milestone**. WP03 adds exact-logistic, sampling/event, dimensional-scaling, independent-polynomial DOP853, refinement/quadrature, export/provenance and fault-detection checks, plus maxima, exact/near-fold basins, bottleneck asymptotics, sensitivity, MSY and readiness/publication checks. [Full evidence map](WP03_ANALYSIS.md). The other packages still have starter checks for scaling, B roots, metrics/autograd and split/identifiability invariants. This is not a substitute for the remaining scientific acceptance tests listed in each task brief.

No unimplemented feature is marked as a fake passing test or hidden behind permanent xfail. When adding a feature, implement its acceptance tests in the same PR. `STATUS.md` remains not started/in progress until its core evidence exists.

## Required evidence for every task

Every owner and coding agent must turn the task brief's core acceptance checklist into implemented tests and reproducible scientific evidence. This is part of the deliverable, not an optional clean-up step.

1. **Map claims to evidence.** In the task PR, map each completed core acceptance item to named test cases or a saved experiment with its command, config, manifest and observed result. Long training/performance claims belong in recorded experiments; deterministic correctness and small smoke cases belong in CI. Leave unsupported items unchecked.
2. **Use independent expectations.** Check against hand calculations, derived identities, independently expanded equations, quadrature or another numerical method as appropriate. Calling the same implementation to generate both actual and expected values cannot independently establish mathematical correctness. Derivations in the report/notebook must explain the identity being tested.
3. **Cover meaningful regimes.** Use representative parameter scales and initial populations, zero harvest/zero population, invalid inputs, exact equilibria and below/at/above threshold cases where relevant. Include near-boundary cases without pretending numerical rounding resolves every critical classification. Each brief lists the task-specific cases.
4. **Justify numerical comparisons.** Explain tolerances using units, scale, solver error or statistical uncertainty. Check convergence where a numerical reference supports a conclusion. For stochastic training, fix seeds, retain all run statuses and separate a short behaviour test from final measured accuracy.
5. **Make tests able to detect mistakes.** Inspect whether a wrong sign, wrong scale, mislabelled branch, detached parameter or leaked split would be caught by the relevant assertion. Do not pad counts with repeated assertions, assert only that code runs, loosen tolerances merely to obtain green CI, or skip required tests to hide a failure. Test quantity is not a substitute for coverage of the mathematical claims.
6. **Check the delivered product.** Run the task command, inspect figures/tables and their interpretation, execute the notebook from a clean kernel, and obtain another member's reproduction. Report, EPS exports, notebook, citations, AI/data disclosure and the speaking contribution remain required alongside tests; see [integration](INTEGRATION.md).

Use a compact evidence table in each project PR:

| Core claim or acceptance item | Independent check / test name | Command and config / manifest | Observed result and limitation |
|---|---|---|---|

Populate the table with actual evidence; an empty template or passing starter suite does not complete a task. Reviewers check both the assertions and the scientific argument. Agents must explain what the tests establish and what remains untested, without certifying the human's understanding for them.

## Commands

```bash
python -m pytest tests/wp01 -q
python -m pytest tests/wp02 -q
python -m pytest tests/wp03 -q
python -m pytest tests/wp04 -q
python -m pytest tests/wp05 -q
python -m pytest -q
ruff check .
ruff format --check .
python scripts/assemble_notebook.py
python scripts/smoke.py
```

CI `core` installs the classical + notebook/dev dependencies, checks style, runs the fast suite, assembles and executes the notebook. CI `pinn` installs CPU Torch and runs tests marked `pinn`; WP04 must add real residual/autograd and short optimiser tests before declaring the forward engine complete. The initial `pinn` job also checks import availability, so an empty optional selection cannot masquerade as trainer validation. Long training/convergence sweeps are experiments, not default unit tests.

## Independent validation

- Analytical roots: polynomial residuals, derivative signs and local trajectory perturbations; test below/at/above critical values and zero harvest.
- Thresholds: calculus formula against an independent bounded maximiser and finite-difference derivatives; avoid just coding the formula twice.
- Extinction: event-time RK45 against quadrature on paths certified to reach zero, and a tighter-tolerance/higher-order reference. Event time must be returned even if outside the requested sample grid.
- History: time/control continuity, carry-over initial conditions, no spontaneous zero recovery, explicit restocking jump and at least two ramp speeds.
- PINNs: tensor/NumPy RHS parity, analytic-function derivative/residual checks, nonzero gradients on trainable parameters, initial-condition loss, short deterministic loss reduction and correct physical time chain rule. Accuracy claims come from repeated measured runs, not fragile hardcoded training thresholds in CI.
- Inverse: disjoint IDs/times, reproducible noise, constrained parameters, no test-set access during training, the B nonidentifiability counterexample, identifiable reduced recovery on clean data, and a separately reported ODE-fit baseline. Do not expect unique all-four B recovery.
- End-to-end: one CPU smoke configuration exercises the assembled artifact; clean execution has no hidden state or absolute personal paths. Final scientific reproduction checks all required plots/tables against manifests.

Use numerical tolerances tied to solver error and scale. Exact float equality is appropriate only for deliberately exact algebraic invariants. A short horizon with no event means `not observed within horizon`, not `never extinct`. Any stochastic test has a fixed seed and an intentionally generous behaviour-based assertion.

## CI and release distinction

CI must stay fast enough for every PR. It does not train all final models. At release, WP03 owner independently runs the frozen final experiments and notebook, WP01 owner compiles and visually inspects the report, and WP02 owner rehearses the 25+5-minute presentation with all five members. The final packaging script refuses obvious unfinished templates; humans still check scientific completeness and EPS/PDF rendering.
