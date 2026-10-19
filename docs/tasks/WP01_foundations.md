# WP01 — Foundations, logistic baseline and Model A

<!-- team-sync:owner:start -->
**Owner:** Unclaimed. See [team.json](../../team.json) for the current choice.
<!-- team-sync:owner:end -->

**Effort guide:** 18–22 h including report integration. **Dependencies:** none for initial work; freeze interfaces with WP03 before consumers merge.

## Task 1 in plain language

You will explain the basic population model and ask: if we keep catching the same amount, what population levels can remain steady? You will work out which steady levels recover after a small disturbance and which move away from it. Start with one simple population-versus-growth sketch, then connect it to the equations, tests and branch plot. You also help assemble the final report.

**Using an agent?** It should read this full brief, explain a small example first, then work through one meaningful piece at a time: explain -> implement -> test -> interpret. Tell it whether you want guided implementation, explanation only or hints while you code. See the [first-session guide](../START_HERE.md); the shared agent workflow is [AGENTS.md](../../AGENTS.md). The detailed deliverables below are its checklist as well as yours.

## Goal and scope

Explain the class result and how strong Allee growth changes the geometry. Own nondimensionalisation, A equilibria/stability and A branch diagram (original items 1, 2(A), 6(A)), plus the overall report narrative. Do not implement the inverse trainer or duplicate WP03's collapse maps.

## Subtasks in order

1. **Foundation PR:** inspect the scaffold equations/parameter validation; derive units and `x,tau,a,q,e`. Explain assumptions and minimum viable population. Add/check all dimensional-to-dimensionless conversion tests and document API decisions with WP03.
2. **Baseline:** derive the logistic roots, `H_c=rK/4`, derivative signs, critical semistability and zero-harvest exception. Plot its production curve and phase lines.
3. **Model A:** analyse the cubic and its physically admissible roots for zero, subcritical, critical and supercritical harvest. Distinguish negative algebraic roots from populations, and A's zero-event boundary from an equilibrium. Use derivative signs and phase lines; at a repeated root use signs on either side.
4. **Numerical branch module:** implement reusable root/classification records, export data and plot stable branches solid, unstable dashed, semistable points marked. Include x=0 only where mathematically an equilibrium; a separate extinction-policy marker must have a distinct legend.
5. **Write/explain:** motivation, objectives, assumptions, formulation and the Model A interpretation. Find and verify a small set of ecological/model references.
6. **Report assembly:** merge all five `.tex` sections via `report/main.tex`, remove duplication, unify notation/citations, link curated figures/tables, compile and visually inspect every page. Verify original EPS exports accompany every reported generated figure.

## Files and concrete deliverables

| Output | Required content |
|---|---|
| `src/mm_allee/equilibria.py` | Logistic/A root and stability APIs from interfaces; documented critical tolerances |
| `experiments/wp01/run.py` + `configs/wp01.json` | One noninteractive command recreating owned figures/tables |
| `tests/wp01/test_*.py` | Starter scaling tests plus acceptance cases below |
| `artifacts/figures/wp01_logistic_vs_allee.png/.eps` | Production/sign geometry with parameters and units |
| `artifacts/figures/wp01_model_a_branches.png/.eps` | Equilibrium branches and fold; stability labels |
| `artifacts/tables/wp01_equilibria.csv` | Example roots, derivatives, classification and residual |
| `report/sections/01_foundations.tex` | Derivations, assumptions, baseline and A results with interpretation |
| `notebooks/sections/01_foundations.ipynb` | Maths/algorithm before code, labelled plots and explanation |
| `report/main.tex`, `references.bib` | Final integrated editable report and verified citations |

Implement the future reproduction command `python experiments/wp01/run.py --config configs/wp01.json --output results/wp01`; this command is a **deliverable**, not already present in the scaffold.

## Required acceptance tests

- [ ] Dimensional RHS equals `r*K` times dimensionless RHS across A/B/logistic, multiple parameters/populations; invalid `r,K,A,H,h` rejected.
- [ ] Logistic roots satisfy residual tolerance below/at/above `q=1/4`; correct zero-harvest signs.
- [ ] A has `0,a,1` at `q=0`; two positive roots for representative `0<q<q_c`; one double root at `q_c`; none above.
- [ ] Every reported root has small RHS residual and correct physical-domain status; negative cubic root never returned as a physical population.
- [ ] Stable/unstable labels agree with independently perturbed trajectories away from a fold; fold classified via one-sided signs, not derivative equality alone.
- [ ] Branch output retains close roots without silently deleting one near the fold; labels/units and exported table align.

## Handoff and done checklist

- [ ] Foundation API reviewed by WP03 and communicated to WP02/WP04/WP05.
- [ ] Code/tests/config, two paired figures, table, report and notebook section committed with manifests.
- [ ] Report assembly passes compilation; every page inspected; EPS files and bibliography complete.
- [ ] One other member reproduced the command; all four approved the current PR; status updated honestly.
- [ ] AI log and citations updated. Owner can explain scaling, root stability, semistability and why A has no zero equilibrium for H>0.

**Presentation:** 0–5 min: problem, assumptions, logistic recap, scaling, Model A geometry. Prepare one baseline slide, one model/assumption slide and one A branch figure. Know how your section connects to the collapse proof and PINNs.
