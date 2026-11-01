"""Two explanatory figures for Section 5 (not part of the saved sweep artifacts)."""

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from mm_allee.data import generate_noisy_observations
from mm_allee.models import Parameters
from mm_allee.solver import solve_trajectory

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output", type=Path, default=Path("results/report-illustrations"))
args = parser.parse_args()
args.output.mkdir(parents=True, exist_ok=True)
OUT = str(args.output.resolve()) + "/"
# --- splits
p = Parameters(r=0.7, K=100.0, A=20.0, H=10.0)
d = p.dimensionless()
tr = solve_trajectory("A", a=d["a"], harvest=d["q"], x0=0.45, tau_end=0.7 * 8.0, n_points=101)
times = tr.tau / 0.7
clean = tr.x * 100.0
obs = generate_noisy_observations(
    times, clean, trajectory_id="a_regular", model="A", noise_sigma=0.05, noise_seed=11, n_ref=100.0
)
itr, iva, ite = obs["train_indices"], obs["val_indices"], obs["test_indices"]
fig, ax = plt.subplots(figsize=(7.2, 3.8))
ax.axvspan(0, times[itr[-1]], color="#dbe7f5")
ax.axvspan(times[itr[-1]], times[iva[-1]], color="#dcefdc")
ax.axvspan(times[iva[-1]], times[-1], color="#f6dcdc")
ax.plot(times, clean, "k-", lw=2, label="Clean reference")
ax.scatter(
    times, obs["observed_population"], s=14, color="#1f3b73", label="Noisy observations (5%)"
)
ymax = max(clean.max(), np.max(obs["observed_population"]))
for x, t in (
    (times[itr[-1]] / 2, "Training\n61 points"),
    ((times[itr[-1]] + times[iva[-1]]) / 2, "Validation\n20"),
    ((times[iva[-1]] + times[-1]) / 2, "Held-out\n20"),
):
    ax.text(x, ymax * 1.02, t, ha="center", va="bottom", fontsize=8)
ax.set_xlabel("Time $t$")
ax.set_ylabel("Population $N(t)$")
ax.grid(True, alpha=0.3)
ax.legend(loc="lower right", fontsize=8)
ax.set_ylim(min(0, np.min(obs["observed_population"])), ymax * 1.18)
fig.tight_layout()
fig.savefig(OUT + "wp05_splits.eps")
fig.savefig(OUT + "wp05_splits.png", dpi=150)
plt.close(fig)
# --- counterexample
p1 = Parameters(r=1.0, A=0.2, K=1.0, h=0.5)
p2 = Parameters(r=1.35, A=0.3, K=0.9, h=0.15)
d1, d2 = p1.dimensionless(), p2.dimensionless()
fig, ax = plt.subplots(figsize=(7.2, 3.8))
for n0, c in zip([0.4, 0.7, 1.1], ["#1f77b4", "#d62728", "#2ca02c"]):
    a = solve_trajectory(
        "B", a=d1["a"], harvest=d1["e"], x0=n0 / p1.K, tau_end=p1.r * 4.0, n_points=81
    )
    b = solve_trajectory(
        "B", a=d2["a"], harvest=d2["e"], x0=n0 / p2.K, tau_end=p2.r * 4.0, n_points=81
    )
    ax.plot(a.tau / p1.r, a.x * p1.K, color=c, lw=3, label=f"Set 1, $N_0={n0}$")
    ax.plot(b.tau / p2.r, b.x * p2.K, "k--", lw=1.2, label="Set 2" if n0 == 0.4 else None)
    print(n0, float(np.max(np.abs(a.x * p1.K - b.x * p2.K))))
ax.set_xlabel("Time $t$")
ax.set_ylabel("Population $N(t)$")
ax.grid(True, alpha=0.3)
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(OUT + "wp05_counterexample.eps")
fig.savefig(OUT + "wp05_counterexample.png", dpi=150)
plt.close(fig)
