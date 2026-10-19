# WP03 numerical-reference entry point

`generate_reference.py` implements the clean RK45 handoff for both A/B. See [the guide](../../docs/WP03_RK45_HANDOFF.md) for output/data boundaries, configuration, validation and pending work.

```bash
python experiments/wp03/generate_reference.py --config configs/wp03_reference.json --output results/wp03-reference
```

Add `--curate` to refresh the small committed fixtures and evidence. The future full `run.py` for threshold/extinction/basin sweeps remains a separate pending Task 3 deliverable. This script does not create noisy observations, select splits or fit inverse parameters.
