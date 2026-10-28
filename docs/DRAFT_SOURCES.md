# Sources and gaps in the working draft

| Package | Source used here | Status and next action |
|---|---|---|
| WP01, Raghav | Main's labelled scaffold | PR #3 was merged then reverted. Its default numerical results reproduce, but review comment [6470288214](https://github.com/devam2006/mm-allee-harvesting/pull/3#issuecomment-6470288214) records open correctness issues. Import the corrected/restored version after review. |
| WP02, Ash | Main's labelled scaffold | Model B branches, fair comparisons, harvest history/restocking and report/notebook contribution still await an implementation handoff. |
| WP03, Devam | PR #4 source at `20fbd5b21844a94e81e021d1571fbed0f7b47379` | Implemented numerical/classical analysis, including recheck fixes; teammate approvals and human learning remain pending. |
| WP04, Prem | Main's labelled scaffold | Need actual forward-PINN engine/runs, error/runtime tables, difficult cases, report and notebook fragment. |
| WP05, Rohan | Main's labelled scaffold | Clean WP03 references exist. Need actual inverse design, noisy observations/splits, PINN and ODE-fit evidence, held-out/noise studies, report/notebook and disclosures. |

This records what has been imported, not what teammates may have completed locally. Do not infer that absent pushed work means no work has been done.

The shared introduction and draft slide text summarise the approved equations and implemented WP03 results. Every numerical slide cites its source table in speaker notes. No PINN score, empirical dataset result, successful recovery claim, personal review or rehearsal is invented.

The WP03 guide is deliberately not copied here. Read it on [the WP03 branch](https://github.com/devam2006/mm-allee-harvesting/blob/wp03/collapse-analysis/docs/WP03_EXPLAINED.md).

When refreshing this draft, record the exact incoming commit, imported files, actual validation commands/outcomes and any remaining conflicts. Keep the task owner's source fragment as the place to make scientific changes.
