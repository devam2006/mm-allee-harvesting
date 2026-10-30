# Project status

WP03's mathematical/computational analysis, early references and optional sensitivity/MSY are implemented on wp03/collapse-analysis and prepared for review. Other packages remain as recorded in the current main tree; final integration is pending. No trained PINN, empirical finding, final report or final presentation is claimed. Human understanding/review is not certified by code completion.

<!-- team-sync:status:start -->
| Package | Owner | State | PR/evidence |
|---|---|---|---|
| WP01 | @RaghavSinghal15 | Not started | Fill after assignment |
| WP02 | @AshChan07 | Not started | Fill after assignment |
| WP03 | @devam2006 | PR review | Core analysis, references and optional sensitivity/MSY implemented; [PR #4](https://github.com/devam2006/mm-allee-harvesting/pull/4); [results/commands](docs/WP03_ANALYSIS.md), wp03/collapse-analysis; human learning/review and final integration pending |
| WP04 | @Prem-Mehta03 | Not started | Fill after assignment |
| WP05 | @rohanagrawal28 | PR review (draft) | [Draft PR #7](https://github.com/devam2006/mm-allee-harvesting/pull/7), `wp05/rohan-inverse-validation`, stacked on WP03 PR #4; submitted results unverified; WP04 API reconciliation and findings in `docs/WP05_SUBMISSION_REVIEW.md` |
<!-- team-sync:status:end -->

States: not started -> in progress -> PR review -> integrated -> reproduced. Only use **reproduced** after another member runs the documented commands from a clean environment.

Bootstrap already provides dimensional/dimensionless RHS functions, a zero-event RK45 wrapper, metric helpers, split validation, notebook assembly, five test groups and collaboration tooling. The assigned members must derive, extend, test and interpret these components rather than present them as completed analysis.
