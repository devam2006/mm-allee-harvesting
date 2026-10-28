# Harvesting under a strong Allee effect

> **Working draft for group review.** WP03 is implemented here. The other task fragments still contain labelled gaps. This notebook is not the completed five-task submission.

We study how harvesting affects a population that loses net growth below a minimum viable density. We compare a fixed catch with harvesting proportional to population, then test forward/inverse PINNs against checked numerical references once those work packages arrive.

## Objectives

- Derive the harvesting and initial-population boundaries between persistence and collapse.
- Explain finite-time extinction, recovery barriers and delayed collapse.
- Measure forward-PINN errors against independently checked numerical solutions.
- Test inverse parameter recovery, noisy-data sensitivity and held-out prediction honestly.

## Model and assumptions

Assume one deterministic, well-mixed population with constant parameters, no age structure or delays, and $r>0$, $0<A<K$. Natural growth is

$$g(N)=rN(1-N/K)(N/A-1).$$

Model A is $N'=g(N)-H$, where $H$ has population/time units. Model B is $N'=g(N)-hN$, where $h$ has inverse-time units. All current examples are synthetic, with no species-specific validation.

Use $x=N/K$, $\tau=rt$, $a=A/K$, $q=H/(rK)$ and $e=h/r$ for known-parameter forward analysis. Then $x'=G(x)-q$ or $x'=G(x)-ex$. Inverse scaling must use declared fixed reference scales if true $r$ or $K$ is hidden.

## Current content

| Section | Present in this draft |
|---|---|
| WP01 | Scaffold awaiting corrected/restored equilibria section |
| WP02 | Scaffold awaiting B comparison and harvesting-history section |
| WP03 | Thresholds, basins, A extinction integral/RK45 checks, bottleneck, optional sensitivity/MSY and clean A/B references |
| WP04 | Scaffold awaiting actual forward-PINN evidence |
| WP05 | Scaffold awaiting actual inverse/held-out/noise evidence |

Algorithms and equations precede each implemented code section. Cells call shared modules instead of reproducing the solver in the notebook. Changes belong in the numbered source fragments, followed by `python scripts/assemble_notebook.py`.

The [WP03 learning guide](https://github.com/devam2006/mm-allee-harvesting/blob/wp03/collapse-analysis/docs/WP03_EXPLAINED.md) stays on its own branch. See `DRAFT_DELIVERABLES.md` for integration commands and `docs/DRAFT_SOURCES.md` for imported versions and gaps.
