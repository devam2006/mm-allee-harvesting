# Testing and scientific acceptance

## Existing checks versus project completion

`python -m pytest -q` currently exercises the **scaffold**: scaling, B root/zero invariants, extinction stopping, error metrics, split rejection and the Model B coefficient ambiguity. Each of the five packages already has executable tests under its owned directory. These are a starting point, not a substitute for the additional acceptance tests listed in the five task briefs.

No unimplemented feature is marked as a fake passing test or hidden behind permanent xfail. When adding a feature, implement its acceptance tests in the same PR. `STATUS.md` remains not started/in progress until its core evidence exists.

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
