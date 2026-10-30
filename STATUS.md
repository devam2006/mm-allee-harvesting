# Project status

PR #11 integrates reviewed WP01–WP03 source fixes and shared numerical conventions. PR #5 combines this with Prem's current WP04–WP05 PR #10 into a portable notebook/data/figure candidate: The previous 511-test handoff and two isolated kernel runs passed; the refreshed source includes Prem PR #10 `00393cd` with verified reporting fixes (301 source tests; 525 integrated tests including four direct residual parity cases). Legacy status denotes training completion; optimizer convergence is reported separately. Human understanding, reviews, the final Overleaf report and presentation remain separate requirements.

<!-- team-sync:status:start -->
| Package | Owner | State | PR/evidence |
|---|---|---|---|
| WP01 | @RaghavSinghal15 | PR review | [PR #8](https://github.com/devam2006/mm-allee-harvesting/pull/8): restores reverted PR #3 with all review fixes; report assembly pending other sections |
| WP02 | @AshChan07 | PR review | PR #9 contains Model B/comparison/history; current consumer fixes integrated in this branch; human reviews pending |
| WP03 | @devam2006 | PR review | Core analysis, references and optional sensitivity/MSY implemented; [PR #4](https://github.com/devam2006/mm-allee-harvesting/pull/4); [results/commands](docs/WP03_ANALYSIS.md), wp03/collapse-analysis; human learning/review and final integration pending |
| WP04 | @Prem-Mehta03 | PR review | [PR #6](https://github.com/devam2006/mm-allee-harvesting/pull/6) (do not merge yet) and the integration [PR #10](https://github.com/devam2006/mm-allee-harvesting/pull/10) (draft): JAX engine, review fixes, one shared forward+inverse setting (tanh, 2x32, lr 1e-3); forward 18/18 on two seed sets; report, notebook and evidence updated; four approvals, another member's reproduction and the PR #4 merge pending |
| WP05 | @rohanagrawal28 | PR review (draft) | [Draft PR #7](https://github.com/devam2006/mm-allee-harvesting/pull/7) and the integration [PR #10](https://github.com/devam2006/mm-allee-harvesting/pull/10): inverse sweep regenerated with the shared setting (clean recovery 10/18, originally 0/18; legacy completed-training label; explicit L-BFGS exits audited in PR #5); report and notebook updated; Rohan to review; findings in `docs/WP05_SUBMISSION_REVIEW.md` and `experiments/integration/README.md` |
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
