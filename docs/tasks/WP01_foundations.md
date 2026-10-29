# WP01 — Foundations, logistic baseline and Model A

<!-- team-sync:owner:start -->
**Owner:** @RaghavSinghal15. See [team.json](../../team.json) for the current choice.
<!-- team-sync:owner:end -->

**Effort guide:** 18–22 h including report integration. **Dependencies:** none for initial work; freeze interfaces with WP03 before consumers merge.

## Task 1 in plain language

You will explain the basic population model and ask: if we keep catching the same amount, what population levels can remain steady? You will work out which steady levels recover after a small disturbance and which move away from it. Start with one simple population-versus-growth sketch, then connect it to the equations, tests and branch plot. You also help assemble the final report.

**Using an agent?** It should read this full brief, explain a small example first, then work through one meaningful piece at a time: explain -> implement -> test -> interpret. Tell it whether you want guided implementation, explanation only or hints while you code. See the [first-session guide](../START_HERE.md); the shared agent workflow is [AGENTS.md](../../AGENTS.md). The detailed deliverables below are its checklist as well as yours.

**Testing requirement:** implement this brief's core acceptance tests and follow the [shared evidence rules](../TESTING.md#required-evidence-for-every-task). Map each completed claim to named tests or reproducible experiments, use independent checks and justify tolerances; report/notebook/figure and integration duties are also required.

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

- [x] Dimensional RHS equals `r*K` times dimensionless RHS across A/B/logistic, multiple parameters/populations; invalid `r,K,A,H,h` rejected.
- [x] Logistic roots satisfy residual tolerance below/at/above `q=1/4`; correct zero-harvest signs.
- [x] A has `0,a,1` at `q=0`; two positive roots for representative `0<q<q_c`; one double root at `q_c`; none above.
- [x] Every reported root has small RHS residual and correct physical-domain status; negative cubic root never returned as a physical population.
- [x] Stable/unstable labels agree with independently perturbed trajectories away from a fold; fold classified via one-sided signs, not derivative equality alone.
- [x] Branch output retains close roots without silently deleting one near the fold; labels/units and exported table align.

## Handoff and done checklist

- [ ] Foundation API reviewed by WP03 and communicated to WP02/WP04/WP05.
- [x] Code/tests/config, two paired figures, table, report and notebook section committed with manifests.
- [ ] Report assembly passes compilation; every page inspected; EPS files and bibliography complete.
- [ ] One other member reproduced the command; all four approved the current PR; status updated honestly.
- [ ] AI log and citations updated. Owner can explain scaling, root stability, semistability and why A has no zero equilibrium for H>0.

**Presentation:** 0–5 min: problem, assumptions, logistic recap, scaling, Model A geometry. Prepare one baseline slide, one model/assumption slide and one A branch figure. Know how your section connects to the collapse proof and PINNs.

## Current handoff

- **Owner:** Raghav (`RaghavSinghal15`).
- **Branch / PR:** PR #3 (`wp01/foundations-model-a`) was merged and then reverted on main with WP03 PR #2. The corrected work is restored on `wp01/foundations-restored` (PR link in STATUS.md), with all four other members requested as reviewers.
- **Review fixes (30 Oct):** relative fold tolerance and cancellation-free `q_c` (Ash, Devam); tiny negative root kept negative and excluded (Ash, Devam); probes bounded by all roots and `x=0`, labels independent of `include_excluded` (Devam); WP01 solver settings validated and passed to RK45 (Ash, Devam); report sentence on shocks qualified by the basin margin (Devam). Regressions in `tests/wp01/test_review_regressions.py`.
- **Done (with evidence):** every acceptance test above, mapped in the PR evidence table to `tests/wp01/test_scaling.py`, `test_logistic.py`, `test_model_a_equilibria.py`, `test_stability_dynamics.py`, `test_branch_output.py` and `test_review_regressions.py` (186 tests). Figures `wp01_logistic_vs_allee`, `wp01_model_a_branches` and an extra `wp01_model_a_perturbations` (PNG + EPS + PDF), `artifacts/tables/wp01_equilibria.csv`, `wp01_thresholds.json`, manifest `artifacts/manifests/wp01_run.json`. Report section 1 and notebook section 1 written; section 1 compiles inside `report/main.tex` with no warnings. Slide content and a five-minute script are in `presentation/wp01_contribution.md`.
- **Reproduce:** `python experiments/wp01/run.py --config configs/wp01.json --output results/wp01` then `python -m pytest tests/wp01 -q`.
- **Interface decisions:** see DECISIONS.md (24 Oct): `Equilibrium` record schema, one-sided sign classification, relative fold tolerance (revised 30 Oct after review), `fold_a` vs WP03 `critical_a`, extensionless figure includes for pdflatex.
- **Still open:** (1) WP03 review of the foundation API and its communication to WP02/WP04/WP05; (2) **report assembly** of all five sections, unified notation/citations, compile and page-by-page inspection and the EPS audit, which can only finish once the other sections land; (3) another member's reproduction and four approvals.
- **Key points to be able to explain:** scaling to (a, q); phase-line stability; why x=0 is not an equilibrium of A for q>0; derivation of x* and q_c from G'(x)=0; why the fold is semistable although f'=0; why bracketing + Brent rather than polynomial eigenvalues near the fold.
