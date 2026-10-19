# WP04 — Forward PINNs and the shared neural engine

<!-- team-sync:owner:start -->
**Owner:** @Prem-Mehta03. See [team.json](../../team.json) for the current choice.
<!-- team-sync:owner:end -->

**Effort guide:** 18–22 h, focused on implementation and evaluation. **Dependencies:** WP01 conventions, WP03 reference fixtures. Freeze the engine interface with WP05 early.

## Task 4 in plain language

Here the equation and its parameters are known. Your job is to train a small neural network to predict the population over time while respecting that equation, then compare its answers with a standard numerical solver. Explain what the network’s loss means before tuning it, and show failures honestly. Task 5 will reuse your neural engine.

**Using an agent?** It should read this full brief, explain a small example first, then work through one meaningful piece at a time: explain -> implement -> test -> interpret. Tell it whether you want guided implementation, explanation only or hints while you code. See the [first-session guide](../START_HERE.md); the shared agent workflow is [AGENTS.md](../../AGENTS.md). The detailed deliverables below are its checklist as well as yours.

## Goal and scope

Implement item 12 for **both A and B** and provide the engine WP05 extends. Demonstrate what the network solves, how derivatives enter its loss and where it succeeds/fails. Hysteresis/sensitivity/MSY are assigned elsewhere to keep this package feasible.

## Subtasks

1. Agree a small differentiable PyTorch MLP, seeded initialisation, CPU-first dtype/device choice, fixed input scaling and trainable-parameter interface. Start with one trajectory per model; parameter-conditioned surrogates are optional scope expansion.
2. Derive physics residual and loss `L=lambda_phys*MSE(dx/dtau-f)+lambda_ic*MSE(x(0)-x0)`. Explain soft versus hard IC enforcement, collocation sampling and optimiser. Use `autograd.grad(...,create_graph=True)` or an equivalent correctly differentiable method. Never detach parameter tensors in residuals.
3. Implement/verify Torch RHS parity with NumPy reference for both models; handle input rescaling chain rules explicitly. No supervised RK45 solution labels in a claimed physics-only forward run.
4. Train bounded CPU-budget experiments for regular, near-fold and subthreshold/extinction regimes; seeds 11/22/33. For A train/evaluate only on the pre-extinction interval. An optional piecewise boundary-aware model must state the modified residual and event handling.
5. Compare on a separate dense reference grid with tight RK45/DOP853. Report RMSE, MAE, global relative L2, runtime, training losses, boundary violations, and all seed failures. A tiny mean loss alone does not establish trajectory accuracy.
6. Deliver shared engine/config/checkpoint API to WP05 after the first short, tested A/B run. Collaborate on gradients and constraints, rather than letting two agents create incompatible PINN stacks.
7. Write an understandable derivation/algorithm and an honest comparison. On this scalar ODE, a conventional solver is a strong baseline; a slower or less accurate PINN is an informative result, not something to hide.

## Deliverables

| Output | Content |
|---|---|
| `src/mm_allee/pinn/{network,residual,train_forward}.py` | Shared network/loss/trainer with extension hooks for trainable physical parameters |
| `experiments/wp04/run.py`, `configs/wp04_smoke.json`, `wp04_final.json` | Budgeted smoke and frozen final sweep |
| `tests/wp04/test_*.py` | Core metric tests plus Torch parity/autograd/training tests |
| `artifacts/figures/wp04_forward.png/.eps` | Both models, reference vs prediction, regular and difficult cases |
| `artifacts/figures/wp04_error_loss.png/.eps` | Absolute errors and optimisation history |
| `artifacts/tables/wp04_forward_metrics.csv` | Per seed/model/regime error/runtime/status before aggregates |
| `artifacts/manifests/wp04_*.json` | Seeds, hardware, epochs, loss weights, optimizer, runtime budget and references |
| `report/sections/04_forward_pinn.tex`, `notebooks/sections/04_forward_pinn.ipynb` | Maths, algorithm before code, outputs and limitations |

Deliver future command `python experiments/wp04/run.py --config configs/wp04_smoke.json --output results/wp04`. Keep model weights and lengthy raw training logs ignored; retain hashes and regeneration commands.

## Acceptance tests

- [ ] Torch RHS matches NumPy for A/B arrays and edge populations/harvests.
- [ ] Analytic test function produces the expected derivative/residual, including time scaling.
- [ ] Backpropagation reaches network weights and optional physical-parameter tensors with finite, nonzero expected gradients; no accidental float cast or detach.
- [ ] Initial-condition handling correct; a short seeded optimiser smoke run reduces a meaningful loss, with generous numerical tolerances.
- [ ] Reference grid/data are independent of supervised labels; A's post-event zero tail never enters the original ODE residual or error metric.
- [ ] Error metrics checked against simple hand-calculated vectors; near-zero reference norm handled explicitly.
- [ ] Save/load predictions agree for a small checkpoint; script import has no training side effect.
- [ ] Final evidence includes both models, three seeds, difficult regimes, measured runtime and failed-run counts. Accuracy is reported, not fabricated to pass a fixed target.

## Handoff and done

- [ ] Shared PINN API documented and tested with WP05 before long sweeps.
- [ ] Two paired figures, metrics table, configs/manifests, report/notebook section, real Torch CI tests.
- [ ] Forward notebook runs from a clean kernel under its declared budget; all equations/methods cited or derived.
- [ ] Other member reproduction; four approvals; AI log/citations/status current.
- [ ] Owner can explain automatic differentiation, physics/IC losses, collocation, RK45 comparison and why failure near a fold matters.

**Presentation:** 15–20 min: PINN construction, loss/derivative, forward results for A/B, quantitative comparison and a failure example.
