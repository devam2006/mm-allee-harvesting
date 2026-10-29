# Project status

Initial state: repository scaffold prepared; scientific work packages are **not started**. Existing tests exercise shared infrastructure only. No trained PINN, empirical finding, final report or final presentation is claimed.

<!-- team-sync:status:start -->
| Package | Owner | State | PR/evidence |
|---|---|---|---|
| WP01 | @RaghavSinghal15 | Not started | Fill after assignment |
| WP02 | @AshChan07 | Not started | Fill after assignment |
| WP03 | @devam2006 | Not started | Fill after assignment |
| WP04 | @Prem-Mehta03 | In progress | Branch `wp04/forward-pinn-engine` pushed, PR to be opened: JAX engine, 42 tests, final sweep (swish, 300 points, seeds 0/1/42: 17/18 accurate), diagnostic and activation selection done; PR, four reviews, WP05 hook check and reproduction pending |
| WP05 | @rohanagrawal28 | Not started | Fill after assignment |
<!-- team-sync:status:end -->

States: not started -> in progress -> PR review -> integrated -> reproduced. Only use **reproduced** after another member runs the documented commands from a clean environment.

Bootstrap already provides dimensional/dimensionless RHS functions, a zero-event RK45 wrapper, metric helpers, split validation, notebook assembly, five test groups and collaboration tooling. The assigned members must derive, extend, test and interpret these components rather than present them as completed analysis.
