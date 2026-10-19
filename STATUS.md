# Project status

Repository scaffold is prepared. WP03's clean RK45 reference milestone is implemented on its task branch; the rest of WP03 and the other scientific packages remain pending. No trained PINN, empirical finding, final report or final presentation is claimed. Human understanding/review is not certified by code completion.

<!-- team-sync:status:start -->
| Package | Owner | State | PR/evidence |
|---|---|---|---|
| WP01 | @RaghavSinghal15 | Not started | Fill after assignment |
| WP02 | @AshChan07 | Not started | Fill after assignment |
| WP03 | @devam2006 | In progress | RK45 clean A/B milestone; [handoff](docs/WP03_RK45_HANDOFF.md), branch wp03/rk45-reference-data; other analysis and human review pending |
| WP04 | @Prem-Mehta03 | Not started | Fill after assignment |
| WP05 | @rohanagrawal28 | Not started | Fill after assignment |
<!-- team-sync:status:end -->

States: not started -> in progress -> PR review -> integrated -> reproduced. Only use **reproduced** after another member runs the documented commands from a clean environment.

Bootstrap already provides dimensional/dimensionless RHS functions, a zero-event RK45 wrapper, metric helpers, split validation, notebook assembly, five test groups and collaboration tooling. The assigned members must derive, extend, test and interpret these components rather than present them as completed analysis.
