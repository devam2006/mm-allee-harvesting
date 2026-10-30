# WP04 experiment entry point

Owner: Task 4 (forward PINNs).

```bash
python experiments/wp04/run.py --config configs/wp04_smoke.json --output results/wp04_smoke   # ~20 s CPU
python experiments/wp04/run.py --config configs/wp04_final.json --output results/wp04 --artifacts artifacts   # ~3 min CPU
```

`--artifacts` additionally copies the curated figures, metrics table and manifest into `artifacts/`. Checkpoints and logs stay under the ignored `results/`. Importing `run.py` trains nothing.

## Diagnostic experiment (exploratory, separate from the frozen sweep)

```bash
python experiments/wp04/diagnose.py --config configs/wp04_diagnose.json --output results/wp04_diagnose --artifacts artifacts
```

**Question.** In the frozen sweep the *regular* cases fail for several seeds (B regular: all three; A regular: seeds 11 and 33) with a tiny training loss. Why? Cases: A regular and B regular only. 10 seeds (11, 22, 33, 44, 55, 66, 77, 88, 99, 100); the first three coincide with the frozen sweep, so the `U100` rows must reproduce it (consistency check). Variants: `U100` baseline (100 uniform points, 1000 Adam + 2500 L-BFGS), `U200`/`U400` (denser uniform), `P100` (100 points clustered near tau=0, tau=T*u^2) and `U100_long` (10000 L-BFGS iterations).

**Hypotheses and predictions, written before running:**
- **H1 (gap):** failures come from steep layers hiding between collocation points. Predict: failures fall with denser uniform collocation (`U100` > `U200` > `U400`), and `P100` is no worse than `U100`.
- **H2 (optimiser stall):** runs that finish with a high loss are stalls, not spurious solutions. Predict: more L-BFGS iterations (`U100_long`) rescues some of the `not_converged` runs but not the `unstable_root`/`zero` runs.
- **H3 (mechanism):** failing runs have max |R| over a dense grid much larger than max |R| at the training points; accurate runs do not. Predict: the median dense residual of failed runs is orders of magnitude above that of accurate runs.

Failure classes (from the state at tau=T/2, with a root found by an independent polynomial solve): `accurate` (relative L2 <= 5e-2), `not_converged` (final loss > 1e-3), `unstable_root` (within 0.03 of the unstable equilibrium), `zero` (within 0.03 of 0), `other`. Thresholds are set in the config before the run. Nothing here changes the frozen results; any proposed fix would need a new, separately frozen sweep.

**Disclosures about this experiment.** (i) A first pass of the same configuration used NumPy's `linspace` for the uniform grid; it differs from the engine's JAX grid by one rounding unit, which changed individual outcomes (A regular seed 11: 9.8e-1 vs the frozen 7.6e-1) while the pass/fail pattern for seeds 11/22/33 stayed the same. The script now builds the uniform grid exactly like the engine, so `U100` seeds 11/22/33 reproduce the frozen sweep. (ii) The class `negative_state` (state below -0.03 at tau=T/2, the unphysical negative root of the polynomial) was added after seeing that first pass, because several Model A runs ended there; it is a post-hoc label.

**Results (10 seeds per cell; outcome counts are accurate runs out of 10).**

| Case | U100 | U200 | U400 | P100 (clustered) | U100_long |
|---|---|---|---|---|---|
| A regular | 3 | 3 | 5 | **10** | 3 |
| B regular | 2 | 3 | 4 | **10** | 2 |

- **Consistency check passed:** `U100` seeds 11/22/33 reproduce the frozen sweep to the printed precision for both cases. Over all 100 runs: 45 accurate, 55 failed (22 on the unstable root, 6 at zero, 2 at the unphysical negative state, 10 not converged, 15 other).
- **H1 (gap), partly supported:** denser *uniform* collocation helps only a little (A 3 -> 3 -> 5, B 2 -> 3 -> 4 accurate; still 50-60% failing at 400 points), but the *same 100 points clustered near tau=0* (`P100`) gave 10/10 accurate in both cases (median relative L2 6.5e-6 for A, 5.3e-6 for B) at the same cost (about 2.5 s). So what matters is resolution near tau=0, not the number of points.
- **H2 (optimiser stall), not supported:** 10000 L-BFGS iterations (`U100_long`) left the accurate count unchanged (A 3, B 2); the 2 not-converged A runs of `U100` ended on other spurious solutions. All 10 not-converged runs are Model A with uniform grids (2 at 100, 4 at 200, 4 at 400 points).
- **H3 (mechanism), supported:** over all 100 runs every accurate run has max dense-grid residual <= 1.2e-3 and every failed run has >= 8.4e-1 (a gap of about 700x). 45 of the 55 failures had max residual < 1e-1 *at the training points*, so the training loss could not reveal them; the other 10 are the not-converged stalls.
- **Unexpected:** (a) the unphysical negative root (about -0.069) of the Model A polynomial attracts some runs; (b) outcomes are extremely sensitive to round-off: a grid that differs by one rounding unit flips A regular seed 11 from 7.6e-1 to 9.8e-1 error; (c) 10 seeds cannot exclude a failure rate up to about 25-30% for `P100`.
- **Limits:** only the two regular cases; `P100` was chosen after seeing failures (not pre-registered) and was not run on the near-fold/extinction cases; adopting it needs a new, separately frozen sweep.

## Activation selection (owner request, 30 Oct 2026)

```bash
for a in tanh swish sigmoid; do python experiments/wp04/run.py --config configs/wp04_act_$a.json --output results/wp04_act_$a; done
python experiments/wp04/select_activation.py --inputs results/wp04_act_tanh results/wp04_act_swish results/wp04_act_sigmoid --output artifacts/tables/wp04_activation_selection.csv
```

Setup chosen by the owner: 300 uniform collocation points, activations tanh / swish / sigmoid, input handling unchanged (fixed scaling s = tau/T in [0, 1]; no [-1, 1] centring and no log stretch), seeds 0, 1, 42, all six cases (A and B x regular / near-fold / extinction), everything else as before ((1,32,32,1) network, hard IC, 1000 Adam + 2500 L-BFGS iterations, learning rate 1e-2). 3 activations x 6 cases x 3 seeds = 54 PINN runs.

**Selection rule, fixed before running:** the activation with the largest number of accurate runs (relative L2 <= 5e-2) out of 18; ties are broken by the smaller geometric mean of the relative L2 over all 18 runs. Per-case counts, median errors, runtime and boundary violations are reported but do not enter the rule. **Caveat:** the winner is chosen on the same seeds that are then reported as the final sweep, so the reported accuracy of the winner is optimistic; a confirmation on other seeds is advisable. The previous n=100 / tanh / seeds 11, 22, 33 sweep is kept as `artifacts/tables/wp04_forward_metrics_n100_tanh_seeds11-22-33.csv` and its manifest; the diagnostic experiment above refers to that sweep.

