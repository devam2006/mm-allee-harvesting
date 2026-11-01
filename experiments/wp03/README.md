# WP03 experiments

Owner: Devam. Main analysis:
~~~bash
python experiments/wp03/run.py --config configs/wp03.json --output results/wp03
~~~
Both thresholds/basins, 427 extinction evaluations, event checks, bottleneck, optional sensitivity/MSY, PNG/EPS outputs. Deterministic; the config declares the analysis budget.

Early clean reference export:
~~~bash
python experiments/wp03/generate_reference.py --config configs/wp03_reference.json --output results/wp03-reference
~~~
Both accept --curate to refresh their small versioned evidence. No noise, splits or PINN fitting here. [Results, APIs, tests and handoff](../../docs/WP03_ANALYSIS.md).
