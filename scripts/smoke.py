"""Fast CPU environment/event/figure check; not a completed project experiment."""

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from mm_allee.plotting import save_figure
from mm_allee.solver import solve_trajectory

ROOT = Path(__file__).resolve().parents[1]


def main():
    output = ROOT / "results" / "scaffold-smoke"
    output.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots()
    summary = {"scope": "Scaffold smoke only, not final scientific evidence", "models": {}}
    for model, harvest in [("A", 1.0), ("B", 0.3)]:
        result = solve_trajectory(model, a=0.2, harvest=harvest, x0=0.8, tau_end=10)
        ax.plot(result.tau, result.x, label=f"{model}, control={harvest}")
        summary["models"][model] = {
            "extinction_tau": result.extinction_tau,
            "boundary_policy": result.boundary_policy,
            "last_x": float(result.x[-1]),
        }
    ax.set(
        xlabel=r"Dimensionless time $\tau$",
        ylabel="Population fraction x=N/K",
        title="Scaffold solver check (a=0.2, x0=0.8)",
    )
    ax.legend(framealpha=1)
    save_figure(fig, output / "solver_check")
    plt.close(fig)
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
