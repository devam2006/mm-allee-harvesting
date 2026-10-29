# Data provenance and labels

Default data are **synthetic population trajectories generated from the stated ODEs**, not field measurements. The project studies mathematical and numerical behaviour and parameter recovery under an assumed model. It does not validate an ecological law for a real species.

WP03 owns reference generation and manifests; WP05 owns inverse observation/noise/split validation. Their shared CSV/manifest schema is in `INTERFACES.md`. Use a seeded NumPy generator; default additive noise is `N_observed=N_reference+sigma*N_ref*epsilon`, `epsilon~Normal(0,1)`, with fixed externally declared `N_ref`. Do not clip negative noisy observations silently: either retain them as measurement noise or predeclare a different observation model and describe its statistical effects. Dynamics remain physically nonnegative up to the declared boundary.

Record generating parameters, solver/tolerances, initial conditions, interval, sampling grid, units/scales, seed, noise level, split IDs, code commit and file SHA256. Keep generator truth in evaluation metadata separate from the data passed to the optimiser. Test data must not enter parameter fitting, hyperparameter selection, loss weighting or early stopping.

WP04 (forward PINNs) uses no observation files: `experiments/wp04/run.py` generates its noise-free reference trajectories on the fly with SciPy DOP853 (rtol 1e-12, atol 1e-14) from the parameters in the `configs/wp04_*.json` files, only to *score* predictions (never as training labels). It has no noise, no train/validation/test split and no dataset files; this stands in for WP03's reference fixtures, which are not yet on `main`, and should be replaced by them when they merge. Its curated outputs are `artifacts/tables/wp04_*.csv` with manifests in `artifacts/manifests/wp04_*.json`; all are synthetic.

Any later external dataset requires original URL, author/provider, download date, license/usage terms, units, preprocessing decisions, train/val/test design and a bibliography entry. Every external/adapted figure or published formula needs a verified citation. No claim that synthetic benchmark success establishes reliable real-world prediction.
