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
Some inverse cases were not reliably recovered by the tested PINN settings and budgets even on clean data; poor conditioning magnifies small trajectory-fitting errors into large parameter errors (the Jacobian condition number of A near-fold, B near-fold and B decline is 1e3 to 2e4, and r and A can both collapse to 0 along a valley that keeps r/A). No hyperparameter is expected to recover them (the ODE fit recovers all six cases, so they are not structurally unidentifiable; the limit is the PINN's data fit), so the maximum attainable inverse score may be well below 18; candidates are compared on the same footing. Selecting on the same seeds that are reported is optimistic; the confirmation stage uses other seeds.

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
- **They cannot be told apart with these small seed samples** (this does not establish equivalence). On the selection seeds (0/1/42) the counts were 10 (tanh) vs 7 (swish, lr 1e-2); on the fresh seeds 8 vs 11. Pooled over the six seeds both recover 18 of 36 clean fits. Forward: 36/36 vs 35/36. Differences of 1 to 3 fits between seed sets show how noisy these counts are. The "selected" label printed by the driver in the confirmation run is only its tie-break, not a selection.
- Where they differ: `shared_final` recovers fewer B near-fold (1/3 vs 3/3) and A extinction (1/3 vs 3/3) fits but is more precise when it recovers (median 7.8e-5 vs 3.8e-3) and faster (3.4 s vs 4.7 s per forward run).
- The same three cases stay unrecovered with every setting on clean data: A near-fold (0/3) and B decline (0/3 for both new settings), as the identifiability analysis predicts.

### The noisy-data criterion was too lenient (correction)
The protocol above defined noisy recovery as every parameter within max(5%, 2 x its Cramer-Rao bound). For ill-conditioned cases the bound is huge, so the tolerance is huge: median loosest tolerance 108% at sigma = 0.01 and 540% at sigma = 0.05, worst case above 100000%. The driver's noisy counts (for example 38/54 for `shared_final`) therefore say very little and must not be quoted as success. **Post-hoc refinement (chosen after seeing the results):** count only the case/noise combinations where the best possible estimator could pin the parameters down, that is every parameter's bound <= 25%, and ask whether every parameter error is within 2 x its bound.
- sigma = 0.01: informative cases are only A regular (bound 12%) and B regular (15%). `shared_final` 6/6 fits within 2 x bound, `wp04_pr6_setting` 4/6, `wp05_original` 0/6.
- sigma = 0.05: no case is informative (bounds 58% to 3200%): at this noise level the training window cannot determine the parameters for any estimator, so no setting can be judged.

## Changes made to existing code on this branch
- `src/mm_allee/pinn/inverse.py` (Rohan's file): two optional constructor arguments `lbfgs_ftol` and `lbfgs_gtol` (defaults unchanged: 1e-12 and 1e-8); 0 lets L-BFGS run its full iteration budget, as the forward trainer does. Nothing else in the trainer was changed.

## Noise study (owner request, 31 Oct 2026; protocol written before running)
Question: is the synthetic observation noise the reason some inverse fits do not converge? Setup: tanh and swish with an otherwise identical shared setting (32x32, network lr 1e-3, lr_params 1e-3, lambda_phys 0.1, 300 points, Adam 1000 + L-BFGS 2500 without tolerance stop), noise sigma in {0, 0.001, 0.005, 0.01} (absolute noise sd = sigma x 100), fresh seeds 11/22/33, six WP03 fixture cases, 24 fits per (setting, sigma) pair.
Two separate notions of "converged": (1) **optimiser convergence**: the training RMSE divided by the noise sd (`noise_floor_ratio`); about 1 means the fit reached the noise floor, much larger means the optimiser did not fit the data, much smaller means the network overfits the noise; (2) **parameter recovery** relative to the Cramer-Rao bound (`err_over_crb`, the worst parameter's error divided by its bound; about 1 or less is what a good estimator achieves). Cases are *informative* at a given sigma if every parameter's bound is <= 25%.
Predictions: (a) clean-data failures (A near-fold, B decline; A extinction and B near-fold partly) will persist at sigma = 0.001, because they exist without any noise; (b) the noise floor ratio of converged fits will be about 1 or below; (c) lowering sigma makes more cases informative (the bound scales linearly with sigma), and recovery within 2 x bound will hold for informative cases.


## Noise study result (validation selection ON, the trainer's default)
- Optimiser convergence under noise is mostly fine: 14 to 17 of 18 fits per (setting, sigma) reach the noise floor (training RMSE about 0.9 x the noise sd); none overfit. Parameter recovery for the well-conditioned cases (A regular, B regular) follows statistics: the worst-parameter error is about 1.3 to 1.4 x its Cramer-Rao bound at every sigma and grows in proportion to sigma.
- Noise is not what makes fits fail: the share of collapsed fits (r or A driven to ~0) is the same with and without noise (6/36 at sigma 0; 9, 9, 7 of 36 at sigma 0.001, 0.005, 0.01), and A near-fold collapses in 22 of 24 fits at every sigma.
- **The fits that do not reach the noise floor (12 of 144) have a common cause: they all end with status `validation_stopped` (except one) and their parameters never left their starting guess** (worst-parameter error exactly 0.5, the error of A = 30 against the true 20). The trainer restores the "best validation" checkpoint and rejects an L-BFGS result whose validation loss is more than 5% worse; on a flat late-time validation window an early near-initial state can win that comparison.
- Test: with the new optional `validation_selection=False` (default True = unchanged) four such fits reach the noise floor (floor ratio 0.9 to 1.2 instead of 5 to 47) and three of four parameter errors fall (0.50 -> 0.13, 0.53 -> 0.10, 0.50 -> 0.07; the fourth, 0.50 -> 0.64, now sits at its Cramer-Rao limit). The full noise study is repeated with the switch off in `configs/shared_noise_nosel.json`.

## Noise study result with validation selection OFF
Same 144 fits (2 activations x 4 noise levels x 6 cases x 3 seeds) with the trainer's validation-based early stopping and checkpoint selection switched off (`validation_selection=False`; default True = unchanged), compared fit by fit with the default run.
- **Optimiser convergence is fully fixed:** the fits that stayed far above the noise floor with selection on (tanh 8, swish 4) drop to **0**; every fit in both settings reaches the noise floor (training RMSE about 0.9 x the noise sd, none overfit). The validation-based selection was returning near-initial states.
- **Parameter recovery does not improve overall:** recovered within 5% (sigma 0 / 0.001 / 0.005 / 0.01): tanh 8/8/2/1 -> 10/7/2/1, swish 10/6/2/1 -> 9/6/1/1; within 2 x Cramer-Rao bound for informative fits: tanh 8/6/6 -> 8/6/6, swish 8/5/5 -> 6/4/5 (out of 15/6/6). Paired over all fits: tanh better 18 / worse 10 / same 44; swish better 16 / worse 17 / same 39. The fits that used to sit at their starting guess (error exactly 0.5) now converge into the degenerate valley and can land further from the truth (for example B near-fold, sigma 0.01: 0.5 -> 1.85, which is about 3.6 x its bound of 0.51). Collapsed fits (r or A -> ~0) stay at 14 to 19 of 72.
- **Conclusion for the question 'is the noise why some runs do not converge':** no. Noise does not stop the optimiser (convergence to the noise floor is the norm), and failures do not depend on sigma. The convergence failures that did exist came from the trainer's validation-based checkpoint selection and are fixed by the switch; the remaining recovery failures come from the poorly conditioned cases (ill-conditioning and the r/A valley), not from noise or from the proven structural ambiguity of Model B with four unknowns and are the same with and without noise.
- Tanh is at least as good as swish in every cell, consistent with the stage 1 and confirmation results.

## Adopted setting and final numbers (31 Oct 2026)
**One setting for both problems:** tanh, two hidden layers of 32, network learning rate 1e-3, 300 collocation points, hard-embedded initial condition, Adam 1000 then L-BFGS 2500 with no tolerance stop; inverse only: lambda_phys 0.1, lr_params 1e-3, validation selection off. Applied in `configs/wp04_{final,smoke,confirm}.json` and `configs/wp05_final.json` (Rohan's original in `configs/wp05_final_original_settings.json`; the swish / lr 1e-2 forward evidence of PR #6 is kept as `*_swish_lr1e-2_*`).
- **Forward** (`wp04_final.json`, seeds 0/1/42): 18/18 accurate, relative L2 from 2.9e-7 to 4.1e-3 (median 6.4e-6; worst case A near-fold); 3.2 to 4.6 s per PINN run against 4 to 10 ms for RK45 (6e-11 to 1e-9). **Fresh seeds 11/22/33** (`wp04_confirm.json`): 18/18 accurate, 1.4e-7 to 2.3e-3 (median 5.8e-6). All L-BFGS runs stopped at the iteration limit.
- **Inverse** (`wp05_final.json`, 54 PINN fits, seeds 11/22/33): all 54 fits ended with status `converged` (the Adam phase finished and a finite solution was returned), L-BFGS stopped at its iteration limit in every one (no tolerance reached, no optimiser error or abnormal exit; see the `lbfgs_outcome` column), and the 36 noisy fits are at the noise floor (training RMSE 0.65 to 1.15 times the noise sd, median 0.87); Rohan's original: all 54 `validation_stopped`. Clean data, every parameter within 5%: **10/18 (original 0/18)**; ODE least squares 18/18. Per case, median worst-parameter error (original -> shared): A regular 1.0 -> 3.7e-5, B regular 0.93 -> 2.7e-5, B near-fold 0.52 -> 1.0e-3, A extinction 0.67 -> 0.13, B decline 0.42 -> 0.29, A near-fold 0.52 -> 1.0 (still collapses). Noisy: only A regular and B regular at sigma 0.01 are informative (Cramer-Rao bound <= 25%); there 6/6 fits are within 2 x bound (original 0/6); at sigma 0.05 no case is informative. PINN test-window error vs the clean reference: sigma 0 1.1e-1 -> 1.6e-4, sigma 0.01 1.0e-1 -> 3.8e-3, sigma 0.05 1.4e-1 -> 4.9e-2. ODE baseline unchanged (52 converged, 2 evaluation-limit failures).
- A near-fold and B decline were not reliably recovered by any of the tested settings and budgets (small trajectory-fitting errors are magnified by their poor conditioning); the noisy-data criterion is post hoc (see above).
