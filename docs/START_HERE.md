# Start with your agent, or work through a task yourself

We are studying a population that struggles to survive when its numbers get too low. We compare a fixed catch with harvesting a fraction of the population, find when collapse happens, and test neural networks on solving the equations and estimating unknown parameters.

You do not need to read the engineering documents before starting. Give your coding agent the repository and the message below. It should read your task, explain it and guide the implementation. If you prefer doing the work yourself, the same task briefs contain the steps and completion checklists.

## A message you can paste

```text
Repository: https://github.com/devam2006/mm-allee-harvesting
Read AGENTS.md and follow its workflow. Help me choose one of the five tasks
if I have not already chosen. Explain my task in simple terms with a small
example, then help me implement it in stages while explaining the maths,
code, tests and results. Keep to my task and prepare a pull request for review.
```

If you already chose a task, add **“I chose Task 3 (WP03)”**, changing the number as needed. If you only want an explanation, say **“Explain first; do not implement yet.”** If you want to write the code yourself, say **“Guide me with hints and review my work.”**

The repository is private: your agent needs an authorised repository connection or an accessible local checkout. A link alone does not grant access. Open the cloned project folder in your coding tool, or use its supported private-repository connection.

## Which task would I like?

| Task | Your main question | What you will show |
|---|---|---|
| [1: Foundations and Model A](tasks/WP01_foundations.md) | At a fixed catch, where can the population settle, and is that steady state stable? | Derivations and population/harvest plots; assemble the report. |
| [2: Model B and history](tasks/WP02_model_b.md) | What changes when we catch a fraction instead? Does lowering harvest undo a collapse? | Comparisons, harvesting ramps and explicit restocking; assemble the slides. |
| [3: Collapse and references](tasks/WP03_collapse.md) | How much harvesting is too much, which initial populations survive, and how long does extinction take? | Thresholds, extinction/basin plots and trusted numerical data; check the final submission bundle. |
| [4: Forward PINNs](tasks/WP04_forward_pinn.md) | Can a neural network solve a known population equation as well as a standard solver? | A shared neural engine and prediction/error comparisons for both models. |
| [5: Inverse PINNs](tasks/WP05_inverse_pinn.md) | Can noisy observations tell us the unknown model parameters, and where does that fail? | Parameter/noise studies and held-out validation; assemble the notebook and acknowledgements. |

Check [team.json](../team.json) and the [task board](tasks/README.md) for current owners and open choices. Agree choices with the group; do not assume roster position chooses your task.

## When someone chooses

Send Devam each choice, for example “WP01 → username”; choices can be recorded individually or together. The member rows are already in `team.json`. An agent can update the chosen member's `work_package`, leave undecided members as `null`, and run:

```bash
python scripts/sync_team.py
python scripts/sync_team.py --check
```

This updates the owner shown in the root README, task board, five briefs, status table and presentation outline without copying names around by hand. It does not change scientific progress or grant GitHub access. The JSON and generated docs are reviewed together; ownership appears on `main` after merge. CI fails if a JSON edit leaves the displayed ownership stale.

## What should the first session look like?

Your agent should explain your task's main question, introduce the few terms you need, and walk through a small example. It should then point out the existing starter code and the outputs you still need to produce. A passing starter test is useful, but your full task is not implemented yet.

For example, before calculating equilibrium stability, it can explain that a steady population has zero net growth and compare what happens just above and below that level. Then it can connect that picture to the derivative, the Python function, a test and the plotted result.

When implementation is requested, work in small pieces: **understand an idea -> build it -> check it -> interpret it**. Explanations should accompany meaningful steps, not interrupt every edit for permission. If the pace is wrong, tell the agent to slow down, give another example or keep its updates shorter.

## What do I need to deliver?

Each task has its own detailed checklist. In general you contribute working code, meaningful tests, reproducible figures/tables, an explained report section, an explained notebook section and about five speaking minutes. Your task also has the integration duty shown above. The group uses a **25-minute talk plus 5-minute Q&A**.

AI can do much of the implementation, but each person must be able to explain the submitted equations, methods, code and results. Ask your agent to show how these pieces connect and what the result does **not** establish. Brief understanding checks can help; they are not a compulsory quiz.

## How do the pieces fit together?

Tasks 1–3 establish the equations and conventional numerical references. Task 4 provides the neural engine; Task 5 reuses it and Task 3's data. You can start independent derivations, tests and explanations while a dependency is being developed. Do not create five separate copies of the same model.

Use the [integration plan](INTEGRATION.md) when combining the report, notebook, slides and submission bundle. The final scientific work is still to be done; this repository currently provides the verified scaffold and task plan.

## How do I share my work?

Work on a branch and open a pull request. Request the other four members as reviewers once their actual GitHub handles are recorded. All four approve before a non-author human merges; an AI review does not replace their approval. Missing names should not block useful local implementation, but reviewer requests remain pending until the roster is complete.

Your agent handles the detailed [setup](SETUP.md), [interfaces](INTERFACES.md), [tests](TESTING.md) and [Git workflow](../CONTRIBUTING.md). If you work manually, these are the relevant guides.

## Entry files for coding tools

| Tool | Repository entry point |
|---|---|
| Codex | Root [AGENTS.md](../AGENTS.md). Open the project checkout/workspace so its repository guidance can be read. |
| Claude Code | Root [CLAUDE.md](../CLAUDE.md), which imports the same `AGENTS.md`. |
| Other agents or ordinary chat tools | Explicitly ask the tool to read `AGENTS.md` after it has repository access. Automatic discovery depends on the tool. |

These files guide behaviour; they do not install an agent, grant GitHub access or enforce server-side merge rules. Entry-file conventions were checked against [OpenAI's AGENTS.md guidance](https://learn.chatgpt.com/docs/agent-configuration/agents-md) and [Claude Code's memory/import guidance](https://code.claude.com/docs/en/memory). Keep `AGENTS.md` as the shared playbook and `CLAUDE.md` as its thin entry point.
