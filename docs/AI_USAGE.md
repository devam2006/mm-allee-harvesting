# AI acknowledgement and human verification

The final report and notebook must acknowledge **every actually used platform and its role**, with external sources cited separately. WP05 owner consolidates the log; everyone supplies their own entries. Do not claim a platform was unused because only one member used it.

| Date | Member | Platform/model if known | Role and affected files | Human checks | PR |
|---|---|---|---|---|---|
| 2026-10-19 | Devam (repository setup requester; package unassigned) | OpenAI ChatGPT/Codex | Initial work allocation, repository scaffold, shared numerical functions, starter tests and documentation | Setup verification recorded in `BOOTSTRAP_VALIDATION.md`; team scientific review still required | Bootstrap upload `04332ecd913a808929fcb08fa9b2567aeb3e89b3`; all five task choices still pending |

| 2026-10-19 | Devam (repository guidance requester; task unassigned) | OpenAI ChatGPT/Codex | Shared agent onboarding, Claude entry file, plain-language task introductions and teaching workflow | Official entry-file docs checked; links, import target and repository checks recorded in the onboarding PR | Agent onboarding/team-setup PR |

| 2026-10-29 | Prem Mehta (`Prem-Mehta03`, WP04 owner) | Claude Code, Claude Sonnet 5.5 | Explained WP04, then implemented the JAX `pinn/{network,residual,train_forward}.py` (framework, architecture and optimiser split chosen by the owner), `experiments/wp04/run.py`, WP04 configs, tests, figures/table/manifest and the report/notebook section; also ran an exploratory diagnostic of the regular-case failures and an activation-selection experiment (tanh/swish/sigmoid) with settings chosen by the owner, and updated the shared docs and CI for the PyTorch-to-JAX change | Owner to rerun `pytest tests/wp04` and the smoke command, review derivations and results, and confirm they can explain them; agent's mutation checks are not a substitute | [PR #6](https://github.com/devam2006/mm-allee-harvesting/pull/6) |

Add actual usage rows as work happens. Do not invent model identifiers when unknown. Important prompts or short summaries can be retained in PR descriptions without credentials or unrelated personal material.

On 19 October 2026, Devam selected WP03. ChatGPT/Codex recorded the choice in `team.json`, regenerated ownership displays, clarified the task's calculus/ODE background and recorded Devam's report that collaborator invitations had been sent. This metadata update does not claim any WP03 scientific implementation or human understanding check.

Later the same day, Devam reported Prem → WP04 and Rohan → WP05, and clarified that four-member approval is for project work, not repository setup. ChatGPT/Codex updated the roster and generated docs, clarified that scope in the agent/human workflow files, and prepared the verified setup PR for owner-authorised merge. Scientific task checklists remain open.

At final task allocation on 19 October 2026, Devam assigned AshChan07 → WP02 and RaghavSinghal15 → WP01. ChatGPT/Codex synchronised the remaining owner displays and reviewed all five task briefs against testing/integration requirements. Shared instructions and the project PR template now explicitly require claim-to-test/experiment evidence, independent expectations, boundary cases and justified tolerances. The ownership-sync test fixture was corrected to preserve its progress assertion regardless of the live owner; notebook starter labels now describe pending implementation instead of unclaimed tasks. No scientific task was marked complete by this setup update.

Each owner confirms they can explain their section's equations, stability argument, numerical method, algorithm, configuration, test evidence and limitations. All members read the final integrated report and understand the complete story before presentation. AI-assisted review does not replace this understanding or the four human PR approvals.

On 19 October 2026, Devam explicitly requested direct implementation of the limited WP03 RK45 handoff while deferring his detailed learning and remaining task work. OpenAI ChatGPT/Codex extended sampling, implemented clean A/B generation and independent numerical validation, added tests/fixtures/evidence and methods documentation, and prepared the Task 3 PR for Rohan's initial review. The PDF skill was used to inspect report rendering; Resolve Recipients used the supplied GitHub handle/project roster for the PR handoff. Actual commands/results are recorded in the handoff and PR; no PINN/noise/split study or human understanding check is claimed.

Suggested final wording must be adapted to actual use: “We used [platforms] for [specific roles]. The authors checked the derivations, implementation and results and take responsibility for the submitted work.” Never submit the bracketed template unchanged.

On 28 October 2026, Devam requested direct completion of the remaining WP03 work while deferring learning. OpenAI ChatGPT/Codex restored only WP03's earlier dependency after main's revert, implemented thresholds/basins/extinction/bottleneck and optional sensitivity/MSY, added independent checks/figures, completed the owned report/notebook and speaking notes, and added a readiness audit. Venv/clean-environment reproduction and actual outcomes are recorded in WP03's handoff/manifest. Official SciPy docs were checked. The PDF skill supported report review; Resolve Recipients used exact roster handles and verified collaborator access. No PINN/noise/split work, human understanding, non-author reproduction or human approval is claimed; final group packaging awaits integrated work and metadata.

On 28 October 2026, Devam requested another WP03 correctness review, a simple comprehensive learning guide kept on the WP03 branch, and preparation for partial group assembly on a separate branch. OpenAI ChatGPT/Codex reproduced the existing results, probed additional parameter limits, fixed small-catch bracketing and near-boundary extinction evaluation, and added independent regression checks. It wrote `docs/WP03_EXPLAINED.md` from the governing equations through numerical methods, outputs and presentation questions. The guide and machine checks do not certify Devam's understanding or replace teammate review. Updated reproduction evidence records the actual post-fix checks.

On `integration/final-deliverables-draft`, OpenAI ChatGPT/Codex prepared shared report/notebook introductions, a source/status ledger, assembly instructions and a partial editable slide deck containing existing WP03 evidence and labelled gaps. The Presentations skill/Artifact Tool produced the PPTX with native charts/tables, package/layout/font/data validation and slide previews. LibreOffice supplied the PDF preview when the authoring runtime's direct PDF export could not resolve its standard-font module. The PDF skill supported report compilation/render review. No other member's missing numerical result, scientific approval, rehearsal or understanding was invented. These evolving drafts are not the final submission.

On 30 October 2026, Devam requested review and fixes for Raghav's comment on
PR #4. OpenAI ChatGPT/Codex read the actual GitHub review, fixed B lower-root
cancellation and basin-cell geometry, added independent Decimal/root and
rendered-cell regression checks, exported vector PDFs, and aligned the owned
report/notebook and interface/merge handoff. The PDF skill supported visual
checks. Actual commands/outcomes and environment limits are recorded in
`docs/WP03_ANALYSIS.md` and `artifacts/manifests/wp03_review_followup.json`.
This is agent-assisted validation, not human understanding, a new human
approval or permission to merge.

On 31 October 2026, Devam requested a latest-commit recheck of Raghav's two WP01
PRs, WP03 and Ashwath's WP02, correction of our own issues, and a new ownership-
specific review comment. OpenAI ChatGPT/Codex verified remote heads and original
fixes, tested a temporary combined source tree with a proposed WP02-only import
repair, and found that WP03's configurable reference generator also accepted
rtol below SciPy's floor. It fixed that validation in WP03's shared solver and
reference configuration, added eight independent rejection/effective-tolerance
checks, and recorded actual tests/reproduction evidence. Temporary WP02 code is
a proposal, not a change to Ashwath's branch. No change to the mathematical fold
convention, human approval, merge or human understanding is claimed.

## WP05 ZIP submission, 30 October 2026

Rohan's supplied `Rohan_RK45_Completed_Code.zip` reports **Antigravity AI Assistant** use for the PyTorch inverse engine, SciPy baseline, observation/noise/split utilities, tests, experiment runner/configs, report section and notebook. This is a submitted disclosure, not independent verification of the ZIP's completion or human-check claims. The upload preserves its WP05 code and curated outputs; final scientific evidence and owner understanding remain under review.

At Devam's request, OpenAI ChatGPT/Codex imported the WP05 contribution on `wp05/rohan-inverse-validation`, inspected it against the task and existing PRs, prepared an evidence review and opened a PR from Devam's connected account on behalf of Rohan. Existing WP03 records were retained. The assembled notebook was regenerated from the current five fragments rather than replacing WP03's section with the older portable scaffold. Actual checks and limitations are in `docs/WP05_SUBMISSION_REVIEW.md`; no teammate approval or completed group integration is claimed.

31 October 2026: at Devam's explicit request to fix the outstanding PRs and build a separate WP01-WP03 integration PR, OpenAI ChatGPT/Codex applied the WP01 compatibility/review corrections and ran focused tests. 189 WP01 tests passed, including 90-digit independent roots for both reported close-fold examples and rejection of unsupported rtol before any output. Near-fold roots are solved in offsets; simple-root signs/derivatives use the factored cubic. The existing standalone fold-band policy is unchanged pending the separate integration PR. These changes are authored as Devam-assisted fixes, not an approval or statement of the original owner's understanding.

## 2026-10-30 — AshChan07, WP02

OpenAI Codex assisted Model B derivations, equilibrium/history/comparison implementation,
independent deterministic tests, bounded synthetic CPU experiments, PNG/EPS/PDF figures,
report and notebook section 2, the editable three-slide WP02 contribution and speaking script.
The implementation reuses WP01 and the shared solver; no empirical data or model API was used.
An initial near-fold reference test failed because the double-precision polynomial oracle
lost accuracy; a 60-digit expanded-polynomial reference replaced it without loosening the
acceptance tolerance. Notebook sandbox/cache restrictions and a slide PDF-export font
runtime error were recorded during validation; see WP02 handoff for final outcomes.
The AI-assisted Task 1 review was posted on PR #3 separately; no human approval was submitted.
Human reproduction, comprehension, rehearsal and the four scientific approvals remain pending.

Final verification of the existing WP02 work added a logistic near-fold comparison
 guard and regression case. The fresh-kernel notebook execution succeeded after
using temporary config/cache directories and approved local kernel networking.
The report compiled and WP02 pages 7–11 plus all three slide renders were inspected.
The slide PDF companion was generated from the inspected renders after the native
export limitation; the PPTX preserves editable evidence. No human review was claimed.

31 October 2026: at Devam's explicit request to fix the outstanding PRs and build a separate WP01-WP03 integration PR, OpenAI ChatGPT/Codex applied the WP02 compatibility/review corrections and ran focused tests. 40 WP02 tests passed. Removed the deleted WP01 constant import while keeping the conservative comparison exclusion local; reject unsupported tiny rtol before output; exported notebook provenance no longer requires Git. The older restored WP01 dependency is replaced by current WP01 only in the separate integration PR. These changes are authored as Devam-assisted fixes, not an approval or statement of the original owner's understanding.

31 October 2026: at Devam's request, Codex applied the source WP01/WP02 fixes, opened PR #11, integrated current Prem PR #10, and prepared a standalone notebook/data/figure download for PR #5. Real fresh Jupyter kernels checked classical and all-five exports; datasets and EPS inventories are explicit. The source trainer's two reporting findings remain disclosed, not silently fixed or relabelled. The report is maintained separately in Overleaf; no LaTeX assembly, human approval or understanding certification was performed.

31 October 2026, reporting-fix follow-up: at Devam's request, Codex independently reviewed Prem PR #10 head 00393cd, ran its ten reporting regressions and full 301-test suite, audited the refreshed 54-fit exit evidence against the previous tables, and integrated the unchanged engine fixes into PR #5. Added four deterministic checks comparing the inverse trainer's actual physics loss with the forward residual API under time/harvest scaling. Updated the notebook and handoff wording, preserving explicit legacy status semantics. No full historical sweep, human approval or LaTeX assembly was performed.

Observed final follow-up checks: 525 integrated tests passed; refreshed portable notebook ran 27 code cells with zero errors (29.53 s) and its identical ZIP-extracted copy passed a second isolated kernel (28.56 s). These runs demonstrate execution and truthful visible exit/loss reporting, not convergence or universal parameter recovery.
