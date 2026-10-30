# WP01 experiment entry point

Task 1 (WP01) reproduction command, run from the repository root:

```bash
python experiments/wp01/run.py --config configs/wp01.json --output results/wp01
python experiments/wp01/run.py --config configs/wp01.json --output results/wp01 --curate  # also refresh artifacts/
```

Deterministic (no seeds), a few seconds on a CPU. Writes three figures (PNG + EPS + PDF), `tables/wp01_equilibria.csv`, `tables/wp01_thresholds.json` and `manifest.json` (config, git SHA, versions, tolerances, checksums). `--curate` copies them to `artifacts/figures`, `artifacts/tables` and `artifacts/manifests/wp01_run.json`.
