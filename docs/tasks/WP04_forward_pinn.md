# WP04 — Forward PINNs and the shared neural engine

<!-- team-sync:owner:start -->
**Owner:** @Prem-Mehta03. See [team.json](../../team.json) for the current choice.
<!-- team-sync:owner:end -->

**Effort guide:** 18–22 h, focused on implementation and evaluation. **Dependencies:** WP01 conventions, WP03 reference fixtures. Freeze the engine interface with WP05 early.

## Task 4 in plain language

Here the equation and its parameters are known. Your job is to train a small neural network to predict the population over time while respecting that equation, then compare its answers with a standard numerical solver. Explain what the network’s loss means before tuning it, and show failures honestly. Task 5 will reuse your neural engine.

**Using an agent?** It should read this full brief, explain a small example first, then work through one meaningful piece at a time: explain -> implement -> test -> interpret. Tell it whether you want guided implementation, explanation only or hints while you code. See the [first-session guide](../START_HERE.md); the shared agent workflow is [AGENTS.md](../../AGENTS.md). The detailed deliverables below are its checklist as well as yours.

**Testing requirement:** implement this brief's core acceptance tests and follow the [shared evidence rules](../TESTING.md#required-evidence-for-every-task). Map each completed claim to named tests or reproducible experiments, use independent checks and justify tolerances; report/notebook/figure and integration duties are also required.

## Goal and scope

Implement item 12 for **both A and B** and provide the engine WP05 extends. Demonstrate what the network solves, how derivatives enter its loss and where it succeeds/fails. Hysteresis/sensitivity/MSY are assigned elsewhere to keep this package feasible.

## Subtasks

1. Agree a small differentiable JAX MLP `(1,32,32,1)` (owner decision, 29 Oct 2026; replaces the original PyTorch wording), seeded initialisation, CPU/float64, fixed input scaling and trainable-parameter interface. Start with one trajectory per model; parameter-conditioned surrogates are optional scope expansion.
2. Derive physics residual and loss `L=MSE(dx/dtau-f)`, with the initial condition enforced exactly by the hard embedding `x_hat=x0+s*N(s)` (owner decision; the soft-IC form `L=lambda_phys*MSE(dx/dtau-f)+lambda_ic*MSE(x(0)-x0)` is explained but not used). Explain collocation sampling and the Adam-then-L-BFGS optimiser. Use `jax.grad`/`vmap` or an equivalent correctly differentiable method. Never detach parameter tensors in residuals.
3. Implement/verify JAX RHS parity with NumPy reference for both models; handle input rescaling chain rules explicitly. No supervised RK45 solution labels in a claimed physics-only forward run.
4. Train bounded CPU-budget experiments for regular, near-fold and subthreshold/extinction regimes; seeds 11/22/33. For A train/evaluate only on the pre-extinction interval. An optional piecewise boundary-aware model must state the modified residual and event handling.
5. Compare on a separate dense reference grid with tight RK45/DOP853. Report RMSE, MAE, global relative L2, runtime, training losses, boundary violations, and all seed failures. A tiny mean loss alone does not establish trajectory accuracy.
6. Deliver shared engine/config/checkpoint API to WP05 after the first short, tested A/B run. Collaborate on gradients and constraints, rather than letting two agents create incompatible PINN stacks.
7. Write an understandable derivation/algorithm and an honest comparison. On this scalar ODE, a conventional solver is a strong baseline; a slower or less accurate PINN is an informative result, not something to hide.

## Deliverables

| Output | Content |
|---|---|
| `src/mm_allee/pinn/{network,residual,train_forward}.py` | Shared network/loss/trainer with extension hooks for trainable physical parameters |
| `experiments/wp04/run.py`, `configs/wp04_smoke.json`, `wp04_final.json` | Budgeted smoke and frozen final sweep |
| `tests/wp04/test_*.py` | Core metric tests plus JAX parity/autodiff/training tests |
| `artifacts/figures/wp04_forward.png/.eps` | Both models, reference vs prediction, regular and difficult cases |
| `artifacts/figures/wp04_error_loss.png/.eps` | Absolute errors and optimisation history |
| `artifacts/tables/wp04_forward_metrics.csv` | Per seed/model/regime error/runtime/status before aggregates |
| `artifacts/manifests/wp04_*.json` | Seeds, hardware, epochs, loss weights, optimizer, runtime budget and references |
| `report/sections/04_forward_pinn.tex`, `notebooks/sections/04_forward_pinn.ipynb` | Maths, algorithm before code, outputs and limitations |

Deliver future command `python experiments/wp04/run.py --config configs/wp04_smoke.json --output results/wp04`. Keep model weights and lengthy raw training logs ignored; retain hashes and regeneration commands.

## Acceptance tests

- [x] JAX RHS matches NumPy for A/B arrays and edge populations/harvests.
- [x] Analytic test function produces the expected derivative/residual, including time scaling.
- [x] Backpropagation reaches network weights and optional physical-parameter tensors with finite, nonzero expected gradients; no accidental float cast or detach.
- [x] Initial-condition handling correct; a short seeded optimiser smoke run reduces a meaningful loss, with generous numerical tolerances.
- [x] Reference grid/data are independent of supervised labels; A's post-event zero tail never enters the original ODE residual or error metric.
- [x] Error metrics checked against simple hand-calculated vectors; near-zero reference norm handled explicitly.
- [x] Save/load predictions agree for a small checkpoint; script import has no training side effect.
- [x] Final evidence includes both models, three seeds, difficult regimes, measured runtime and failed-run counts. Accuracy is reported, not fabricated to pass a fixed target.

## Handoff and done

- [ ] Shared PINN API documented and tested with WP05 before long sweeps.
- [ ] Two paired figures, metrics table, configs/manifests, report/notebook section, real JAX CI tests.
- [x] Forward notebook runs from a clean kernel under its declared budget; all equations/methods cited or derived.
- [ ] Other member reproduction; four approvals; AI log/citations/status current.
- [ ] Owner can explain automatic differentiation, physics/IC losses, collocation, RK45 comparison and why failure near a fold matters.

**Presentation:** 15–20 min: PINN construction, loss/derivative, forward results for A/B, quantitative comparison and a failure example.

## Current handoff

- **Owner:** Prem (`Prem-Mehta03`), Task 4. **Branch:** `wp04/forward-pinn-engine`; branch pushed to origin; PR not opened yet (`gh` is not installed on the author machine: use the GitHub web form with the text in `pr-body.md`, or `python scripts/open_pr.py` once `gh` is installed and authenticated).
- **Owner decisions (29-30 Oct 2026):** JAX instead of PyTorch; network (1,32,32,1); hard initial condition and physics loss only; Adam 1000 then L-BFGS 2500 (about 2/7 Adam); errors in scientific notation; **300 uniform collocation points, seeds 0/1/42, activation swish (selected from tanh/swish/sigmoid)**, no input centring or input map.
- **Done (evidence):** engine `src/mm_allee/pinn/{network,residual,train_forward,autodiff}.py`; `experiments/wp04/{run,diagnose,select_activation}.py`; `configs/wp04_{smoke,final,act_tanh,act_swish,act_sigmoid,diagnose}.json`; `tests/wp04/` (42 tests; mutation-checked: B sign, residual sign, stop-gradient on the physical parameter, dropped product-rule term, forgotten hard-IC factor); final sweep (18 PINN runs + 6 RK45 baselines, 97 s CPU) in `artifacts/{figures,tables,manifests}/wp04_*`; report section and notebook fragment written.
- **Activation selection (pre-declared rule, 54 runs):** swish 17/18 accurate (geometric-mean relative L2 2.3e-5), tanh 11/18 (2.9e-4), sigmoid 10/18 (1.4e-3). Evidence: `artifacts/tables/wp04_activation_{selection,runs_*}.csv`. Selected on the same seeds as the final sweep, so optimistic; confirmation on other seeds not done.
- **Final result (swish):** 17 accurate / 1 inaccurate / 0 diverged. Relative L2 from 8e-8 to 4e-4 except A near-fold seed 0 at 5.8e-2 (threshold 5e-2). Regular cases accurate for all seeds (A 1.8e-5 to 3.6e-5; B 1.3e-6 to 5.0e-5). RK45 is about 1e-10 accurate in about 1e-2 s vs 4.8 to 6.0 s per PINN run. Some runs predict small negative populations (B decay: 83 and 114 of 1001 samples).
- **Diagnostic (exploratory, on the earlier tanh / 100-point design, 10 seeds):** `experiments/wp04/diagnose.py`; failures are spurious equilibria hidden between collocation points (every accurate run has dense-grid residual <= 1.2e-3, every failed run >= 8.4e-1; 45 of 55 failures had training-point residual < 1e-1); 100 points clustered near tau=0 gave 10/10 accurate for A and B regular while denser uniform grids and more L-BFGS iterations did not; outcomes are round-off sensitive.
- **Not done:** shared API check with WP05 (owner Rohan; the framework change and the new `activation`/`tau` options affect them); other-member reproduction; four approvals; GitHub CI (Linux, Python 3.11) not run; LaTeX not compiled; confirmation of the activation choice on other seeds; why swish works better is not understood; WP03 reference fixtures are not on main, so the reference is generated independently by DOP853 in `run.py`.
- **Next command:** `python -m pytest tests/wp04 -q`, then `python experiments/wp04/run.py --config configs/wp04_smoke.json --output results/wp04_smoke`.
- **Open understanding question for the owner:** why can the physics loss be tiny while the trajectory is wrong, and what did the failed tanh trajectories converge to in terms of equilibria?
