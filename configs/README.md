# Configurations

JSON configs with schema version, model/scales/controls, seed, solver or training budget, noise and split design. `reference.json` is an environment fixture, not the final experimental design. Each task adds its smoke/final config named in its assignment.

WP04 (forward PINNs): `wp04_smoke.json` (short CPU smoke run), `wp04_final.json` (frozen final sweep: swish, 300 uniform collocation points, seeds 0/1/42, six cases), `wp04_act_{tanh,swish,sigmoid}.json` (the activation-selection sweeps behind the choice of swish) and `wp04_diagnose.json` (exploratory diagnostic of the earlier tanh / 100-point failures, seeds 11-100). Run with `python experiments/wp04/run.py --config CONFIG --output results/wp04` (the diagnostic uses `experiments/wp04/diagnose.py`).
