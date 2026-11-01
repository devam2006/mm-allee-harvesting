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

- **Owner:** Prem (`Prem-Mehta03`), Task 4. **Branches/PRs:** `wp04/forward-pinn-engine` ([PR #6](https://github.com/devam2006/mm-allee-harvesting/pull/6), carries a "do not merge yet" notice) and the integration branch `integration/shared-pinn-settings` ([PR #10](https://github.com/devam2006/mm-allee-harvesting/pull/10), draft, stacked on WP03 PR #4), which contains this work together with WP05 and is intended to supersede PR #6 and Rohan's PR #7 once approved.
- **Final setting (one setting for forward and inverse, owner decision 31 Oct 2026):** tanh, two hidden layers of 32, network learning rate 1e-3, 300 uniform collocation points, hard-embedded initial condition, physics loss only, Adam 1000 then L-BFGS 2500 with no tolerance stop; inverse only: lambda_phys 0.1, lr_params 1e-3, validation selection off. This **supersedes** the swish / lr 1e-2 choice of PR #6, which compared activations at one learning rate only (see `experiments/integration/README.md`).
- **Results (relative L2 against DOP853):** final sweep seeds 0/1/42 **18/18 accurate**, 2.9e-7 to 4.1e-3 (median 6.4e-6; worst A near-fold); fresh seeds 11/22/33 **18/18 accurate**, 1.4e-7 to 2.3e-3. 3.2 to 4.6 s per PINN run against 4 to 10 ms for RK45 (6e-11 to 1e-9). All L-BFGS runs stop at the 2500-iteration limit. Evidence in `artifacts/{figures,tables,manifests}/wp04_*`; the earlier swish (lr 1e-2) and tanh (100 points) evidence is kept under `*_swish_lr1e-2_*` and `*_n100_tanh_*` names.
- **Review fixes (PR #6 reviews, still in force):** NaN/inf predictions are never scored (label `invalid_prediction`); trained `a`/`harvest` stay in range through Adam and L-BFGS; `load_checkpoint` returns the learned parameters; near-zero error column; L-BFGS exit recorded; failed runs recorded; pinned versions in `artifacts/manifests/wp04_*_requirements.txt`; PDF figures; units-parity test.
- **Done (evidence):** engine `src/mm_allee/pinn/`; runners `experiments/wp04/{run,diagnose,select_activation}.py` and `experiments/integration/{shared_settings,noise_convergence}.py`; configs `configs/wp04_*.json`, `configs/shared_*.json`; tests (`tests/wp04`, mutation-checked); report section and notebook fragment rewritten for the final setting; the report compiles with plain `latexmk -pdf` and the assembled notebook executes. Diagnostic of the earlier design (spurious equilibria hidden between collocation points) in `experiments/wp04/README.md`.
- **Not done / needs people:** four approvals and another member's reproduction of the final tanh design (the reviewers' reruns covered the earlier swish design); decide whether PR #6 and PR #7 are closed in favour of PR #10; WP05 owner to confirm the shared setting and the two optional trainer arguments; unify the parameter transforms and status vocabulary; add a forward-versus-inverse residual parity test between the two engines.
- **Next command:** `python -m pytest tests/wp04 -q`, then `python experiments/wp04/run.py --config configs/wp04_smoke.json --output results/wp04_smoke`.
- **Open understanding question for the owner:** why can the physics loss be tiny while the trajectory is wrong, and why did lowering the learning rate remove the earlier regular-case failures (this was not isolated)?
