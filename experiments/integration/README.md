# Shared-settings study (forward + inverse PINN)

Goal: find **one** PINN setting that works for both the forward (WP04) and the inverse (WP05) problem, and use it for both. Run on the separate branch `integration/shared-pinn-settings`; written down before any study run.

## What is shared and what is not
- **Shared (must be identical in both problems):** activation, hidden width (two hidden layers), network learning rate, number of collocation points (300), Adam/L-BFGS budget (Adam 1000, L-BFGS 2500 with no tolerance stop).
- **Inverse-only (do not exist in the forward problem):** physics-loss weight `lambda_phys`, learning rate of the physical parameters `lr_params`, validation early stopping (patience 150, kept as in WP05). These are tuned in stage 2, on the stage-1 winner.

## Design
- Forward: the six WP04 cases (A and B x regular / near-fold / extinction), scored exactly as in WP04 (relative L2 <= 5e-2 on the DOP853 reference; NaN/inf is never accurate).
- Inverse: Rohan's trainer, unchanged except for optional L-BFGS tolerance arguments, on the six WP03 fixture trajectories (`configs/wp05_final.json`), clean data (sigma = 0) in the selection stages. Noise-free data isolates optimisation from statistics.
- Seeds 0, 1, 42 for selection (forward seed = network seed; inverse: fit seed = 1000 + seed, noise seed = seed). Confirmation later on 11, 22, 33 and on noisy data.
- Stage 1 (shared knobs): activation {tanh, swish} x width {32, 64} x network learning rate {1e-3, 1e-2} = 8 candidates, with `lambda_phys` = 0.1 and `lr_params` = 1e-2.
- Stage 2 (inverse-only knobs) on the stage-1 winner: `lambda_phys` {0.1, 1, 10} x `lr_params` {1e-3, 1e-2}.

## Selection rule (fixed before running)
score = (forward runs accurate, of 18) + (inverse fits recovered, of 18). A fit is *recovered* if **every** fitted parameter has relative error <= 5e-2. The candidate with the highest score wins; ties go to the lower median parameter error over its recovered fits. Per-case counts, collapsed fits (r or A driven to ~0) and runtimes are reported but do not enter the rule.

## Known limits (from the pre-study diagnostics, see `docs/DECISIONS.md`)
Some inverse cases are practically unidentifiable on the 60% training window even on clean data (the Jacobian condition number of A near-fold, B near-fold and B decline is 1e3 to 2e4, and r and A can both collapse to 0 along a valley that keeps r/A). No hyperparameter is expected to recover them, so the maximum attainable inverse score may be well below 18; candidates are compared on the same footing. Selecting on the same seeds that are reported is optimistic; the confirmation stage uses other seeds.

## Width 64 dropped (owner rule, 31 Oct 2026)
The owner's rule was: run the first 64-wide candidate, and drop all larger networks if it takes more than 7 minutes or does not improve accuracy. `tanh_64x64_lr0.001` took 307 s (a 32x32 candidate takes about 130 s) and scored **23** (forward 15/18, inverse 8/18, 4 collapsed fits) against **28** for the same setting with 32x32 (forward 18/18, inverse 10/18, 3 collapsed fits): it was slower and less accurate, so all 64-wide candidates were dropped and only the four 32x32 candidates were run. That single 64-wide result comes from the console log of the first, interrupted stage-1 run (the driver writes its CSVs only at the end); it was not re-run. The 32x32 candidates were re-run in full for complete per-run tables.

## Stage 1 result (32x32 candidates, seeds 0/1/42)
| Candidate | forward accurate /18 | inverse recovered /18 | score | median recovered error |
|---|---|---|---|---|
| tanh_32x32_lr0.001 (**selected**) | 18 | 10 | 28 | 8.6e-5 |
| swish_32x32_lr0.001 | 17 | 11 | 28 | 7.4e-4 |
| swish_32x32_lr0.01 | 17 | 7 | 24 | 2.3e-3 |
| tanh_32x32_lr0.01 | 11 | 9 | 20 | 4.8e-5 |

The top two tie on score; the pre-declared tie-break (lower median recovered error) selects tanh. The network learning rate is the dominant factor (1e-3 beats 1e-2 for both activations). A near-fold is never recovered (0/3 for every candidate) and B decline almost never. Note for WP04: the earlier choice of swish was made comparing activations at learning rate 1e-2 only; at 1e-3 tanh reaches 18/18 on the forward problem. Stage 2 uses the winner (tanh, 32x32, lr 1e-3).

## Stage 2 result (inverse-only knobs on tanh_32x32_lr0.001, seeds 0/1/42, clean data)
lambda_phys x lr_params, inverse recovered /18: (0.1, 1e-3) 10 [selected by tie-break], (0.1, 1e-2) 10, (1, 1e-2) 10, (10, 1e-2) 9, (1, 1e-3) 8, (10, 1e-3) 8. The inverse-only knobs matter little; Rohan's defaults (0.1, 1e-2) tie for the best.

**Final shared setting:** tanh, two hidden layers of 32, network learning rate 1e-3, 300 collocation points, Adam 1000 then L-BFGS 2500 with no tolerance stop (shared); lambda_phys 0.1 and lr_params 1e-3 (inverse only).

## Confirmation protocol (fixed before running; no selection)
Fresh seeds 11, 22, 33 (never used for selection); inverse noise levels 0, 0.01, 0.05 (absolute noise = sigma x 100, the fixed population scale). Three settings on the same data: `shared_final`, `wp04_pr6_setting` (swish, lr 1e-2, what PR #6 used) and `wp05_original` (Rohan's final WP05 settings: tanh 64x64, 120 points, 1500 Adam epochs with validation stopping, 200 L-BFGS iterations with his tolerances; inverse only). Clean data: recovered = every parameter within 5%. Noisy data: recovered = every parameter within max(5%, 2 x its Cramer-Rao bound), where the bound is the best relative standard deviation any unbiased estimator could reach on the 60% training window (Fisher information of the ODE model). Forward: accurate = relative L2 <= 5e-2.

## Confirmation result (fresh seeds 11/22/33)
| Setting | forward accurate /18 | inverse recovered, clean /18 | collapsed (clean) | median error of recovered fits |
|---|---|---|---|---|
| `shared_final` (tanh 32x32, lr 1e-3, lr_params 1e-3) | 18 | 8 | 3 | 7.8e-5 |
| `wp04_pr6_setting` (swish 32x32, lr 1e-2) | 18 | 11 | 3 | 3.8e-3 |
| `wp05_original` (Rohan's final settings, inverse only) | n/a | **0** | 2 | n/a |

- Both new settings fix Rohan's clean-data failure (0/18 -> 8 or 11 of 18) and are perfect on the forward problem for these seeds (18/18 each).
- **They are statistically indistinguishable.** On the selection seeds (0/1/42) the counts were 10 (tanh) vs 7 (swish, lr 1e-2); on the fresh seeds 8 vs 11. Pooled over the six seeds both recover 18 of 36 clean fits. Forward: 36/36 vs 35/36. Differences of 1 to 3 fits between seed sets show how noisy these counts are. The "selected" label printed by the driver in the confirmation run is only its tie-break, not a selection.
- Where they differ: `shared_final` recovers fewer B near-fold (1/3 vs 3/3) and A extinction (1/3 vs 3/3) fits but is more precise when it recovers (median 7.8e-5 vs 3.8e-3) and faster (3.4 s vs 4.7 s per forward run).
- The same three cases stay unrecovered with every setting on clean data: A near-fold (0/3) and B decline (0/3 for both new settings), as the identifiability analysis predicts.

### The noisy-data criterion was too lenient (correction)
The protocol above defined noisy recovery as every parameter within max(5%, 2 x its Cramer-Rao bound). For ill-conditioned cases the bound is huge, so the tolerance is huge: median loosest tolerance 108% at sigma = 0.01 and 540% at sigma = 0.05, worst case above 100000%. The driver's noisy counts (for example 38/54 for `shared_final`) therefore say very little and must not be quoted as success. **Post-hoc refinement (chosen after seeing the results):** count only the case/noise combinations where the best possible estimator could pin the parameters down, that is every parameter's bound <= 25%, and ask whether every parameter error is within 2 x its bound.
- sigma = 0.01: informative cases are only A regular (bound 12%) and B regular (15%). `shared_final` 6/6 fits within 2 x bound, `wp04_pr6_setting` 4/6, `wp05_original` 0/6.
- sigma = 0.05: no case is informative (bounds 58% to 3200%): at this noise level the training window cannot determine the parameters for any estimator, so no setting can be judged.

## Changes made to existing code on this branch
- `src/mm_allee/pinn/inverse.py` (Rohan's file): two optional constructor arguments `lbfgs_ftol` and `lbfgs_gtol` (defaults unchanged: 1e-12 and 1e-8); 0 lets L-BFGS run its full iteration budget, as the forward trainer does. Nothing else in the trainer was changed.

