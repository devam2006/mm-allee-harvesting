# Project status

WP03's mathematical/computational analysis, early references and optional sensitivity/MSY are implemented on wp03/collapse-analysis and prepared for review. Other packages remain as recorded in the current main tree; final integration is pending. No trained PINN, empirical finding, final report or final presentation is claimed. Human understanding/review is not certified by code completion.

<!-- team-sync:status:start -->
| Package | Owner | State | PR/evidence |
|---|---|---|---|
| WP01 | @RaghavSinghal15 | PR review | [PR #8](https://github.com/devam2006/mm-allee-harvesting/pull/8): restores reverted PR #3 with all review fixes; report assembly pending other sections |
| WP02 | @AshChan07 | PR review | PR #9 contains Model B/comparison/history; current consumer fixes integrated in this branch; human reviews pending |
| WP03 | @devam2006 | PR review | Core analysis, references and optional sensitivity/MSY implemented; [PR #4](https://github.com/devam2006/mm-allee-harvesting/pull/4); [results/commands](docs/WP03_ANALYSIS.md), wp03/collapse-analysis; human learning/review and final integration pending |
| WP04 | @Prem-Mehta03 | Not started | Fill after assignment |
| WP05 | @rohanagrawal28 | Not started | Fill after assignment |
<!-- team-sync:status:end -->

States: not started -> in progress -> PR review -> integrated -> reproduced. Only use **reproduced** after another member runs the documented commands from a clean environment.

Bootstrap already provides dimensional/dimensionless RHS functions, a zero-event RK45 wrapper, metric helpers, split validation, notebook assembly, five test groups and collaboration tooling. The assigned members must derive, extend, test and interpret these components rather than present them as completed analysis.

30 October 2026: Raghav's [PR #4 review](https://github.com/devam2006/mm-allee-harvesting/pull/4#pullrequestreview-5705535562)
follow-up fixes small-a B root cancellation and basin colour spill above the
fold, adds vector report figures, and documents fold-convention differences,
near-boundary conditioning and merge-order steps. Current validation and limits
are recorded in [WP03 analysis](docs/WP03_ANALYSIS.md). The PR remains unmerged;
remaining human reviews and cross-package integration are pending.

31 October 2026: latest-head recheck adds WP03's unsupported-RK45-tolerance
validation fix and eight regressions. Default numerical results and reference
fixtures are preserved. WP01/WP02 dependency and convention alignment remains
pending; evidence is in the [WP03 analysis follow-up](docs/WP03_ANALYSIS.md).


31 October 2026, WP02 review follow-up: PR #9 incorporates classical integration
#11 (`649e0c1`), replacing the obsolete WP01 restoration with corrected WP01/WP03
and shared exact-fold/basin semantics. Full suite: 421 passed, one optional Torch
skip; all three classical experiments and the combined notebook execute.
[WP02 evidence](docs/tasks/WP02_validation.md) supersedes its old publishing
blocker. Raghav reproduced/approved WP02 at `879b110`; fresh review of the updated
head and the other required approvals remain pending. No main merge, final
presentation rehearsal or certification of human understanding is claimed.

31 October 2026, latest WP02 review follow-up: canonical POSIX dependency-hash
keys fix Windows manifest portability; the focused provenance regression passes
on macOS. Native Windows execution and fresh-head CI remain pending.

WP02 final-notebook follow-up: add dimensional yield/basin and history tables,
with yield derivation and explicit boundary uncertainty. Source fragment and
local assembled notebook updated; final Colab publication remains with Devam.
