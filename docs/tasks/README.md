# Task board — choose an open task

You can ask your agent to read this page, explain the choices, and guide the task you choose. The [first-session guide](../START_HERE.md) has a message you can paste; agents start at [AGENTS.md](../../AGENTS.md).

The five contributors are recorded in [team.json](../../team.json); tasks stay open until each person chooses. Agree choices together, update their `work_package`, then run `python scripts/sync_team.py` from the root. The generated table below and each brief will show the owners. Each task has one human owner; AI agents assist that owner. Roster order does not select a task.

<!-- team-sync:board:start -->
| Task | In plain language | Shared duty | Claimed by |
|---|---|---|---|
| [WP01: Foundations and Model A](WP01_foundations.md) | Find the steady population levels under a fixed catch and check their stability | Report assembly and EPS audit | Unclaimed |
| [WP02: Model B and history](WP02_model_b.md) | Compare catch policies and show why reducing harvest may not undo collapse | Presentation assembly and timing | Unclaimed |
| [WP03: Collapse and numerical references](WP03_collapse.md) | Calculate when collapse occurs, which starts survive and extinction time | Independent reproduction and submission bundle | @devam2006 |
| [WP04: Forward PINNs](WP04_forward_pinn.md) | Train a network to solve the known equations and compare it with a solver | Shared neural engine and forward benchmark | @Prem-Mehta03 |
| [WP05: Inverse PINNs](WP05_inverse_pinn.md) | Estimate unknown parameters from noisy observations and test what is learnable | Notebook assembly and acknowledgement audit | @rohanagrawal28 |
<!-- team-sync:board:end -->

Every chosen owner writes their report/notebook section, tests, figure interpretation, references and AI-use entry; prepares about five minutes of the confirmed 25+5-minute presentation; and reviews the other four owners' PRs. Integration duties belong to the task and move with the choice.

The 18–22-hour budgets in the briefs are planning targets. Reassess after the first smoke runs. The inverse task reuses Task 4's engine and Task 3's data; it should not build those stacks again. Optional analyses and larger joint fits can be deferred so the workload stays manageable.
