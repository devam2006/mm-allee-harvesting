# Decisions

| Date | Decision | Reason |
|---|---|---|
| 2026-10-19 | Use `mm-allee-harvesting` as proposed private repository name | More descriptive than `mm-project` |
| 2026-10-19 | Five unclaimed tasks; member roster and chosen packages filled later | Avoid inventing assignments or sending invitations to the wrong people |
| 2026-10-19 | Move history/recovery to WP02, sensitivity/MSY to WP03 | Reduce overload on forward-PINN owner |
| 2026-10-19 | **Confirmed 30-minute extension slot includes Q&A; plan 25+5** | User explicitly confirmed this exception to the PDF's usual slot |
| 2026-10-19 | Fixed-K inverse B core; all-four B not uniquely recoverable under a single fixed effort | Three polynomial coefficient combinations for four unknowns |
| 2026-10-19 | Synthetic benchmark default, explicit provenance and held-out observation IDs | Clear reproducibility and honest interpretation |
| 2026-10-19 | Keep classical requirements and both PINN directions core; slowing/sensitivity/MSY optional | Preserve a deliverable project if training proves expensive |
| 2026-10-24 | WP01 equilibrium API and record schema as in INTERFACES.md; stability from one-sided signs, roots from calculus brackets + Brent, fold tolerance 1e-12 in q (revised 2026-10-30, below) | Avoids complex near-fold artefacts of companion-matrix solvers and keeps close roots separate; WP02 reuses the conventions |
| 2026-10-24 | `equilibria.fold_a(a)` provides the closed-form `(x_star, q_c)` for WP01 classification; WP03's planned `thresholds.critical_a` may wrap it but must keep its own independent maximisation test | WP01 needs q_c now and must not depend on an unmerged module |
| 2026-10-30 | After PR #3 review: fold test is relative, `abs(q-q_c) <= 64*eps*q_c`; `q_c` from the rationalised form; Brent runs to relative tolerance `4*eps`; sign probes are bounded by every real root and by `x=0`; WP01 solver settings are validated (RK45 only) and passed to the integrator | The absolute 1e-12 tolerance exceeded `q_c` itself for `a` near 1; tiny negative roots rounded to 0; probes could cross 0 for tiny roots; config tolerances were recorded but not used |

| 2026-10-24 | WP01 equilibrium API and record schema as in INTERFACES.md; stability from one-sided signs, roots from calculus brackets + Brent, fold tolerance 1e-12 in q | Avoids complex near-fold artefacts of companion-matrix solvers and keeps close roots separate; WP02 reuses the conventions |
| 2026-10-24 | `equilibria.fold_a(a)` provides the closed-form `(x_star, q_c)` for WP01 classification; WP03's planned `thresholds.critical_a` may wrap it but must keep its own independent maximisation test | WP01 needs q_c now and must not depend on an unmerged module |
| 2026-10-24 | Report figures are included without file extension; pdflatex picks the vector PDF variant written next to the PNG/EPS pair. EPS files remain the submitted originals | Restricted pdflatex cannot convert EPS stored outside `report/`; this keeps `latexmk -pdf -cd report/main.tex` working without `-shell-escape` |

Add interface changes, chosen experiment budgets, fixed inverse parameters, final environment lock and presentation date here as reviewed decisions.

Task choices finalised by the user on 19 October 2026: Raghav (`RaghavSinghal15`) → WP01, `AshChan07` → WP02, Devam → WP03, Prem → WP04, Rohan → WP05. Integration duties and speaking slots follow the chosen WP, not roster order; `team.json` remains the current ownership source.

Review scope clarification (user, 19 October 2026): the four-other-member approval rule applies to PRs raised during project work. Owner-authorised repository configuration and task-assignment administration do not require those approvals. The current setup PR may be merged by the owner's agent after checks; scientific code, experiments, results and final deliverable integration keep the four-review rule.

Validation guidance confirmed during final setup: every task maps core claims to independent executable tests or recorded experiments and includes the report/notebook/figures/disclosures/integration handoff. Meaningful coverage and justified tolerances matter more than a target test count. This guidance does not claim that scientific task implementations or their final validation are complete.

RK45 milestone scope (Devam, 19 October 2026): implement only the numerical-reference part of WP03 now for both A/B, with clean fixtures, independent checks and methods/handoff documentation. WP05 owns observation/noise/split construction and inverse studies. Full threshold/basin/extinction sweeps, optional extensions, packaging and Devam's detailed understanding review remain pending. The Task 3 PR is assigned to Rohan with only his initial review requested; the other reviews remain due before merge. The separate clean/observation schemas in INTERFACES.md resolve earlier overlapping wording.

28 October 2026, full WP03: no control tolerance merges the fold. Exact returned roots are classified explicitly; non-exact initial states within 2e-12 dimensionless units of an unstable/semistable barrier are unresolved. Quadrature follows analytical basin classification, with a tangent substitution for the above-fold peak. Sensitivities hold other dimensional parameters fixed. B MSY is realised yield on the upper branch. The final audit exposes missing group artifacts/human checks. This branch restores only WP03's prior dependency removed by main's revert.

28 October 2026, WP03 recheck: use product-form A root brackets away from the fold to preserve tiny-catch endpoint signs. Use a logarithmic variable for near-boundary subcritical extinction integrals and an elementary antiderivative at the computed fold. The latter returns no quadrature-error estimate. Positive-catch roots rounded to endpoints are not exact A equilibria. Independent high-precision polynomial and rational-fold integral checks cover the fixes. Devam requested a basics-first WP03 learning guide on this branch and a separate branch for evolving partial group deliverables; neither action supplies human scientific approvals or understanding certification.

30 October 2026, Raghav's PR #4 review follow-up: evaluate B's small lower branch
using the quadratic root product, retaining the explicit repeated fold root.
Draw basin colour cells separately on either side of control/critical=1, with
the fold as a line, so no persistence cell extends into the supercritical
region. Export vector PDF with WP03's PNG/EPS and use extensionless report
references without changing the shared plotting helper. Explain input/root
rounding amplification near the subcritical extinction boundary in report and
notebook. WP03 retains exact computed-control equality; document that WP01 #8
currently uses a 64*eps relative fold band. A unified convention requires owner
review at integration. Preserve both PRs' interface/decision notes and rebuild
the assembled notebook when the second PR merges. No merge or human approval
is supplied by these fixes.

31 October 2026, latest-head integration recheck: WP01 PR #8 at f427d5f already
fixes the original PR #3 findings in c47084e. WP02 PR #9 at a6ad5d3 still copies
the old restoration; that is a dependency-version issue, not an instruction to
Raghav to redo those completed fixes. WP03's shared solver/reference validator
now reject rtol below SciPy RK45's supported floor rather than allowing requested
and effective tolerances to diverge. Default numerical results and exact-fold
classification remain unchanged. Adoption by WP01/WP02 and a single cross-package
fold policy remain owner-reviewed integration steps; no owner agreement is invented.

## 2026-10-30 — WP02 proposed interfaces (affected-owner review pending)

- `model_b.EquilibriumB` mirrors the WP01 record but uses `e` instead of `q`; effort
  must not be mislabelled as yield. `equilibria_b(a,e)` and `critical_effort(a)` use
  the required discriminant derivation; no absolute fold band merges distinct controls.
- `history.run_history` reuses `solver.solve_trajectory` on constant-control segments.
  Restocking is an explicitly recorded positive addition at a segment index; boundary
  duplicate times preserve left/right limits. A shutdown persists until restocking;
  B smallness never triggers a reset. `ramp_schedule` supplies declared staircase controls.
- `comparison` and `wp02_experiment` are WP02-owned consumers, not changes to the
  existing shared APIs. WP01 PR #3 is restored on this branch as a declared dependency.
  Its reviewed numerical edge cases remain with WP01; comparison guards exclude the
  unresolved regimes. WP03 threshold-helper integration remains pending its availability.
- These are proposed additions for the WP02 PR, not a claim of affected-owner approval.

## Integrated classical convention, 31 October 2026

At Devam's explicit request, this separate integration PR implements one shared WP03 threshold and positive-branch provider, with exact computed-control equality for root topology. WP01 root records and WP02 comparisons consume it; population uncertainty remains separate. Source PRs retain their independently reviewed scope, and this integration change remains subject to the affected owners' PR review. No human agreement or approval is fabricated.

The report is maintained in Overleaf. Repository integration focuses on portable notebooks, synthetic data, figures (including EPS), source and reproducibility evidence. No repository LaTeX report assembly is part of this task.
