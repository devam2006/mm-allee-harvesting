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

Add interface changes, chosen experiment budgets, fixed inverse parameters, final environment lock and presentation date here as reviewed decisions.

Task choices finalised by the user on 19 October 2026: Raghav (`RaghavSinghal15`) → WP01, `AshChan07` → WP02, Devam → WP03, Prem → WP04, Rohan → WP05. Integration duties and speaking slots follow the chosen WP, not roster order; `team.json` remains the current ownership source.

Review scope clarification (user, 19 October 2026): the four-other-member approval rule applies to PRs raised during project work. Owner-authorised repository configuration and task-assignment administration do not require those approvals. The current setup PR may be merged by the owner's agent after checks; scientific code, experiments, results and final deliverable integration keep the four-review rule.

Validation guidance confirmed during final setup: every task maps core claims to independent executable tests or recorded experiments and includes the report/notebook/figures/disclosures/integration handoff. Meaningful coverage and justified tolerances matter more than a target test count. This guidance does not claim that scientific task implementations or their final validation are complete.

RK45 milestone scope (Devam, 19 October 2026): implement only the numerical-reference part of WP03 now for both A/B, with clean fixtures, independent checks and methods/handoff documentation. WP05 owns observation/noise/split construction and inverse studies. Full threshold/basin/extinction sweeps, optional extensions, packaging and Devam's detailed understanding review remain pending. The Task 3 PR is assigned to Rohan with only his initial review requested; the other reviews remain due before merge. The separate clean/observation schemas in INTERFACES.md resolve earlier overlapping wording.

28 October 2026, full WP03: no control tolerance merges the fold. Exact returned roots are classified explicitly; non-exact initial states within 2e-12 dimensionless units of an unstable/semistable barrier are unresolved. Quadrature follows analytical basin classification, with a tangent substitution for the above-fold peak. Sensitivities hold other dimensional parameters fixed. B MSY is realised yield on the upper branch. The final audit exposes missing group artifacts/human checks. This branch restores only WP03's prior dependency removed by main's revert.
