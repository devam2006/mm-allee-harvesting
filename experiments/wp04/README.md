# WP04 experiment entry point

Owner: Task 4 (forward PINNs).

```bash
python experiments/wp04/run.py --config configs/wp04_smoke.json --output results/wp04_smoke   # ~20 s CPU
python experiments/wp04/run.py --config configs/wp04_final.json --output results/wp04 --artifacts artifacts   # ~3 min CPU
```

`--artifacts` additionally copies the curated figures, metrics table and manifest into `artifacts/`. Checkpoints and logs stay under the ignored `results/`. Importing `run.py` trains nothing.
