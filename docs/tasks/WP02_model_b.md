# WP02 — Model B, fair comparison and harvesting history

<!-- team-sync:owner:start -->
**Owner:** @AshChan07. See [team.json](../../team.json) for the current choice.
<!-- team-sync:owner:end -->

**Effort guide:** 18–22 h including presentation assembly. **Dependencies:** shared conventions from WP01, threshold helpers from WP03; begin symbolic derivations immediately.

## Task 2 in plain language

You will compare catching a fixed number with catching a fraction of the current population. Then you will raise harvesting and lower it again to see what the population does. The important question is whether a collapsed population recovers by itself; keep any restocking clearly labelled. You also bring the group’s slides together.

**Using an agent?** It should read this full brief, explain a small example first, then work through one meaningful piece at a time: explain -> implement -> test -> interpret. Tell it whether you want guided implementation, explanation only or hints while you code. See the [first-session guide](../START_HERE.md); the shared agent workflow is [AGENTS.md](../../AGENTS.md). The detailed deliverables below are its checklist as well as yours.

**Testing requirement:** implement this brief's core acceptance tests and follow the [shared evidence rules](../TESTING.md#required-evidence-for-every-task). Map each completed claim to named tests or reproducible experiments, use independent checks and justify tolerances; report/notebook/figure and integration duties are also required.

## Goal and scope

Own B equilibria/stability and branch plots (items 2(B), 6(B)), logistic/Allee and A/B comparisons (10), history experiments (7), optional slowing down (8). This redistribution gives WP04 space for forward PINNs.

## Subtasks

1. Factor B, derive `x_plus/minus`, discriminant, zero stability and critical semistability. Show phase lines and the unstable root's basin role; cite WP03's threshold proof rather than redoing it in a different convention.
2. Implement B equilibrium records and branch diagrams compatible with WP01's schema.
3. Define **two explicit comparison protocols**: matched initial realised harvest (`H=h*N_ref`) and matched fraction of each threshold. Use common initial conditions/units. Compare persistence/collapse, critical initial population and realised yield; explain why these protocols answer different questions. A single universal risk ranking is not justified.
4. Implement slow up/down harvesting schedules for both A/B, with state carried between segments. Compare two ramp speeds or dwell times. Distinguish dynamic delay from equilibrium thresholds. Record A extinction and harvest shutdown; distinguish B practical-smallness from exact finite extinction.
5. Show failed spontaneous recovery after a nonnegative down-ramp; add **explicit restocking** above the current basin boundary as a separately labelled run. Do not manufacture a closed hysteresis loop by resetting population at the turning point.
6. **Optional:** compute local relaxation `-1/f'` on the populated stable branch and check with small-perturbation trajectories; discuss its divergence near the fold without evaluating at the fold itself.
7. Assemble all five slide contributions into a coherent 25-minute talk plus 5-minute Q&A. Standardise notation, figure legends, main conclusions and AI/data disclosure. Rehearse transitions and record timings.

## Deliverables

| Output | Content |
|---|---|
| `src/mm_allee/model_b.py`, `history.py` | B root/stability records; ramp and declared intervention logic |
| `experiments/wp02/run.py`, `configs/wp02.json` | Reproduce branches, comparisons and history runs |
| `tests/wp02/test_*.py` | Starter B invariants plus acceptance below |
| `artifacts/figures/wp02_b_branches.png/.eps` | Populated/zero branches and stability |
| `artifacts/figures/wp02_history.png/.eps` | Time/control history, both ramp directions, restocking labels |
| `artifacts/tables/wp02_comparison.csv` | Matched-protocol outcomes and realised harvest, with units |
| `report/sections/02_model_b_history.tex` | Derivations, comparison definitions, results, caveats |
| `notebooks/sections/02_model_b_history.ipynb` | Equations/algorithms before executable results |
| `presentation/` | Editable final slide source and PDF, timed script/outline and five speakers |

Deliver future command `python experiments/wp02/run.py --config configs/wp02.json --output results/wp02`. Slowing plots are extras, not a condition for history to be correct.

## Acceptance tests

- [x] Zero RHS at zero for B for several efforts; derivative at zero negative. Positive equilibrium residuals and discriminant cases below/at/above threshold, including `e=0`.
- [x] Stable/unstable/semistable labels agree with signs and local numerical perturbations. Compare to WP01's conventions.
- [x] Matched harvest protocol checks equality of initial realised rates in dimensional units; threshold-normalised protocol is explicitly separate.
- [x] Schedule times strictly ordered; state carried continuously at ordinary segment boundaries, with no hidden restart at down-ramp.
- [x] Extinct A run stays at declared absorbing zero after shutdown; B zero remains zero, and no unlabelled intervention creates recovery.
- [x] Restocking introduces exactly the documented jump; above-threshold restart can reach the populated branch when such a branch exists.
- [x] Two ramp speeds reported, with appropriate integration-tolerance checks; conclusions do not rely on one arbitrary schedule.
- [ ] If slowing added: analytical local relaxation agrees with small perturbation decay away from the fold and units are correct.

## Handoff and done

- [x] Reproducible command/config, two paired figures, comparison table, report/notebook section and manifests.
- [x] Explicit statement of history dependence versus closed-loop hysteresis; no claim of automatic ecological recovery.
- [ ] Slides assembled from all members, 25+5 timing rehearsed, final source/PDF placed in bundle.
- [ ] Other member reproduces; four approvals; AI/citations/status updated.
- [ ] Owner can explain B zero stability, roots, fair risk comparisons and why restocking is necessary after collapse.

**Presentation:** 5–10 min: B geometry, fair A/B risk comparison, ramp/history and restocking. Give WP03 the transition from history to the quantitative collapse threshold.


## Current handoff

- **Owner / branch / PR:** @AshChan07; `codex/wp02/model-b-history`;
  [PR #9](https://github.com/devam2006/mm-allee-harvesting/pull/9).
- **Review follow-up:** fast-forwarded integration PR #11 at `649e0c1`, preserving
  corrected WP01 `b83bba8`, WP03 `16a05ce`, and WP02 `879b110`. Shared thresholds
  and basin uncertainty now agree in the combined tree. Corrected stale fold
  wording, reused the shared RK45 minimum and recorded new dependency hashes.
  The latest review's Windows provenance issue is fixed by writing dependency
  hash keys with POSIX separators and asserting the format in the regression.
- **Evidence:** full suite 421 passed / one optional Torch skip; all three default
  classical experiments succeed; combined 43-cell notebook executes in a fresh
  kernel. WP02 rerun took 1.396 s within its 120-second budget; extinction times
  and recovery conclusions are unchanged. Detailed named evidence and commands:
  [WP02 validation](WP02_validation.md). Curated provenance records source hashes
  and dirty development state honestly.
- **Latest fix evidence:** the focused provenance test passes on macOS; native
  Windows execution is unavailable in this environment.
- **Next step:** review the updated #9 diff and CI; request all four teammates'
  latest-head reviews. Raghav's reproduction/approval at `879b110` is recorded
  separately from the new changes. A non-author human performs any main merge
  after the project review requirements are met.
- **Pending:** four current approvals, final group-slide assembly and real
  rehearsal; optional slowing analysis deferred. The group's Overleaf report
  is maintained separately. No human understanding or rehearsal is certified.
- **Explain:** proportional harvest falls with biomass but does not remove the
  Allee recovery barrier. Why does returning effort to zero fail below A?

### Final notebook additions

Added explicit total/mean catch formulas, a six-row dimensional comparison table
including yield and basin boundary, and a four-row history/recovery table with
years and refinement errors. The full 36-row CSV remains available. Source:
`notebooks/sections/02_model_b_history.ipynb`; assembled notebooks (`notebooks/project.ipynb`,
`notebooks/wp01_wp03.ipynb` and `notebooks/wp01_wp03_standalone.ipynb`) and
`report/sections/02_model_b_history.tex` updated.
Apply these six WP02 cells to the final small Colab notebook; Devam owns final
publication/runtime packaging. Local handoff: `results/project_colab_wp02_updated.ipynb`
uses the final integration snapshot with only WP02 cells replaced. Other five-package
code was not rerun here; the local combined classical notebook was verified.
