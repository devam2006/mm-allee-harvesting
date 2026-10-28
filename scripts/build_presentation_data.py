"""Refresh only implemented WP03 data for the evolving draft slides."""

import csv
import json
from pathlib import Path

import numpy as np

from mm_allee.collapse import positive_branches
from mm_allee.thresholds import critical_a, critical_b

ROOT = Path(__file__).resolve().parents[1]


def main():
    config = json.loads((ROOT / "configs/wp03.json").read_text())
    a = config["parameters"]["A"] / config["parameters"]["K"]
    controls = np.linspace(0, 1, 61).tolist()
    branches = {}
    for model in ["A", "B"]:
        critical = critical_a(a)[1] if model == "A" else critical_b(a)
        roots = [positive_branches(model, a=a, harvest=f * critical) for f in controls]
        branches[model] = {
            "control_fraction": controls,
            "lower": [r[0] for r in roots],
            "upper": [r[1] for r in roots],
        }
    with (ROOT / "artifacts/tables/wp03_event_validation.csv").open() as stream:
        events = list(csv.DictReader(stream))
    summary = json.loads((ROOT / "artifacts/manifests/wp03_summary.json").read_text())
    value = {
        "is_synthetic": True,
        "parameters": config["parameters"],
        "branches": branches,
        "events": events,
        "summary": summary,
        "scope": "WP03 only; no PINN results supplied",
    }
    output = ROOT / "presentation/data/draft_results.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")
    print(output.relative_to(ROOT))


if __name__ == "__main__":
    main()
