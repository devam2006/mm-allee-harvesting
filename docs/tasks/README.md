# Task board and owners

Find your GitHub handle in the table below. Ask your agent to read your task brief, explain it and guide implementation. The [first-session guide](../START_HERE.md) has a message you can paste; agents start at [AGENTS.md](../../AGENTS.md).

All five allocations were finalised by Devam on 19 October 2026 and are recorded in [team.json](../../team.json). Each task has one human owner; AI agents assist that owner. For an agreed reassignment, update `work_package`, run `python scripts/sync_team.py` from the root and publish the JSON/generated docs together under the administration workflow. Roster order does not select a task.

<!-- team-sync:board:start -->
| Task | In plain language | Shared duty | Claimed by |
|---|---|---|---|
| [WP01: Foundations and Model A](WP01_foundations.md) | Find the steady population levels under a fixed catch and check their stability | Report assembly and EPS audit | @RaghavSinghal15 |
| [WP02: Model B and history](WP02_model_b.md) | Compare catch policies and show why reducing harvest may not undo collapse | Presentation assembly and timing | @AshChan07 |
| [WP03: Collapse and numerical references](WP03_collapse.md) | Calculate when collapse occurs, which starts survive and extinction time | Independent reproduction and submission bundle | @devam2006 |
| [WP04: Forward PINNs](WP04_forward_pinn.md) | Train a network to solve the known equations and compare it with a solver | Shared neural engine and forward benchmark | @Prem-Mehta03 |
| [WP05: Inverse PINNs](WP05_inverse_pinn.md) | Estimate unknown parameters from noisy observations and test what is learnable | Notebook assembly and acknowledgement audit | @rohanagrawal28 |
<!-- team-sync:board:end -->

Every chosen owner writes their report/notebook section, tests, figure interpretation, references and AI-use entry; prepares about five minutes of the confirmed 25+5-minute presentation; and reviews the other four owners' PRs. Integration duties belong to the task and move with the choice.

The 18–22-hour budgets in the briefs are planning targets. Reassess after the first smoke runs. The inverse task reuses Task 4's engine and Task 3's data; it should not build those stacks again. Optional analyses and larger joint fits can be deferred so the workload stays manageable.
