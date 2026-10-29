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
| 2026-10-24 | Report figures are included without file extension; pdflatex picks the vector PDF variant written next to the PNG/EPS pair. EPS files remain the submitted originals | Restricted pdflatex cannot convert EPS stored outside `report/`; this keeps `latexmk -pdf -cd report/main.tex` working without `-shell-escape` |

Add interface changes, chosen experiment budgets, fixed inverse parameters, final environment lock and presentation date here as reviewed decisions.

Task choices finalised by the user on 19 October 2026: Raghav (`RaghavSinghal15`) → WP01, `AshChan07` → WP02, Devam → WP03, Prem → WP04, Rohan → WP05. Integration duties and speaking slots follow the chosen WP, not roster order; `team.json` remains the current ownership source.

Review scope clarification (user, 19 October 2026): the four-other-member approval rule applies to PRs raised during project work. Owner-authorised repository configuration and task-assignment administration do not require those approvals. The current setup PR may be merged by the owner's agent after checks; scientific code, experiments, results and final deliverable integration keep the four-review rule.

Validation guidance confirmed during final setup: every task maps core claims to independent executable tests or recorded experiments and includes the report/notebook/figures/disclosures/integration handoff. Meaningful coverage and justified tolerances matter more than a target test count. This guidance does not claim that scientific task implementations or their final validation are complete.
