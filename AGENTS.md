# Start here, coding agent

You are helping one member of a five-person mathematical modelling project. They may arrive with only the repository link and may not have read any task document. **Read the relevant task yourself, explain it in ordinary language, then help them do the work and understand the result.** Do not send them away to read a stack of files before you can help.

This is the shared playbook for Codex, Claude Code and other coding agents. `CLAUDE.md` imports this file; keep the actual instructions here. Use the files in the current checkout as evidence, not an earlier chat's assumptions.

## First session or a new task

1. Establish access. If you only received a private URL, use the available authenticated repository connection or the user's local checkout. If access fails, explain the exact blocker and request access/a checkout; do not invent file contents or ask for tokens in chat.
2. Read [README.md](README.md), [STATUS.md](STATUS.md), [team.json](team.json) and the [task board](docs/tasks/README.md). These tell you what exists, what is unfinished and what the member has chosen. GitHub handles are already recorded; task choices may still be null. `WP01` means Task 1, and similarly through `WP05`.
3. If the user names a task, open its brief from the table below. If no task is selected and the roster does not resolve it, explain the five choices in one sentence each and ask which they want. Do not assign a task to Devam or anyone else by default. You can explain the project and inspect setup while a choice is pending.
4. Before implementation, read the chosen brief, [scientific conventions](docs/SCIENTIFIC_CONTRACT.md), [shared interfaces](docs/INTERFACES.md), [testing guide](docs/TESTING.md) and [PR workflow](CONTRIBUTING.md). Inspect the existing files/tests before planning new ones. Explain which deliverables already exist as scaffold and which must still be built.
5. Start with a short orientation: the question this task answers, a small numerical/visual example, the files and outputs it owns, its dependencies, and the first useful implementation step. If implementation is already requested, proceed in small stages; do not ask for permission after each routine edit or test.

For a resumed session, inspect the chosen task's checklist, current diff/branch and latest handoff before continuing. For a small unrelated fix, read only the guidance that applies; do not restart the whole onboarding lecture.

## Task routing

| Choice | Read this brief | Explain its purpose as |
|---|---|---|
| Task 1 / WP01 | [Foundations](docs/tasks/WP01_foundations.md) | Find the population levels that can remain steady under a fixed catch, and whether small disturbances return to them. |
| Task 2 / WP02 | [Model B and history](docs/tasks/WP02_model_b.md) | Compare catching a fixed amount with catching a fraction, and show what happens when harvesting rises and falls. |
| Task 3 / WP03 | [Collapse](docs/tasks/WP03_collapse.md) | Find the harvesting and initial-population boundaries between persistence and collapse, and calculate extinction time. |
| Task 4 / WP04 | [Forward PINNs](docs/tasks/WP04_forward_pinn.md) | Give a neural network the known population equation and test how well it predicts the population over time. |
| Task 5 / WP05 | [Inverse PINNs](docs/tasks/WP05_inverse_pinn.md) | Start with noisy population observations, estimate unknown parameters, and test what can actually be learned. |

Each brief also names its report/notebook section, tests, figures and shared integration duty. Do not take over the other four tasks. Task 4's neural engine and Task 3's numerical data are reused by Task 5, not rebuilt independently.

## Teach while building

- Default to **explain, implement one meaningful piece, test it, interpret it**. A meaningful piece is a derivation, solver feature, experiment or figure—not every line or file.
- Introduce one idea at a time. Explain a term before using it: an equilibrium is a steady population; stability asks what happens after a small disturbance; a basin is the set of starting populations with the same long-term outcome. Use a small example before a general formula.
- Connect mathematics -> algorithm -> code -> result. Say what a test checks and why its result supports the conclusion; do not just paste terminal output or finished code.
- At a useful milestone, give a short progress note and offer one brief understanding check. These are learning opportunities, not approval gates or a compulsory quiz. Respect the member's pace; continue authorised work without repetitive confirmations and never claim they demonstrated understanding if they have not.
- If the user asks only to understand, explain without implementing. If they want to code it themselves, give the next manageable step, hints and feedback rather than taking over. If they want direct implementation, keep explanations concise and leave clear mathematical/code documentation.
- Before handoff, explain the main result, its limitation and a question they may be asked in the presentation. Each person has about five speaking minutes in the confirmed 25-minute talk + 5-minute Q&A.

Human-facing onboarding and a copyable first message are in [START_HERE.md](docs/START_HERE.md). The member does not have to read that page for you to follow this playbook.

## Where to look next

| Need | File or location |
|---|---|
| Install/run locally | [SETUP.md](docs/SETUP.md); `pyproject.toml` owns dependencies |
| Equations, units, boundary cases and inverse limitations | [SCIENTIFIC_CONTRACT.md](docs/SCIENTIFIC_CONTRACT.md) |
| Existing vs planned Python APIs; data/output schemas | [INTERFACES.md](docs/INTERFACES.md) |
| Fast checks vs full scientific acceptance | [TESTING.md](docs/TESTING.md), then `tests/wpNN/` |
| Join the five pieces into the submission | [INTEGRATION.md](docs/INTEGRATION.md) |
| Branches, four human reviewers and merge policy | [CONTRIBUTING.md](CONTRIBUTING.md) |
| Record actual AI use, sources and synthetic data | [AI_USAGE.md](docs/AI_USAGE.md), [DATA_PROVENANCE.md](docs/DATA_PROVENANCE.md), [REFERENCES.md](docs/REFERENCES.md) |

## Environment and verification

- Use the Git-ignored `.venv`; see setup for Linux/macOS and Windows commands. Install `.[dev,notebook]`, plus `.[pinn]` for Tasks 4/5. No model API key is required by this project.
- Run commands from the repository root with that environment's Python. Start with `python -m pytest tests/wpNN -q`. Before a substantive PR run `python -m pytest -q`, `ruff check .`, `ruff format --check .` and `python scripts/assemble_notebook.py`, plus the relevant experiments. For documentation-only edits check links and `git diff --check`; do not launch training.
- Long sweeps need explicit, recorded runtime budgets. Start with a real CPU smoke run and report failures. If a dependency is not merged, do independent derivation/tests or another unblocked subtask; do not fabricate its outputs or mark dependent work complete.

## Scope and ownership

- `team.json` owns membership and task assignments. After any roster/choice edit run `python scripts/sync_team.py`; commit all generated ownership updates together. Do not hand-edit the `team-sync` blocks. Use `--check` to check for drift. The script does not publish changes; apply or merge them under the workflow below.

- **Owner-authorised setup exception:** Devam clarified on 19 October 2026 that repository setup and task-assignment administration do not need four teammate approvals. The owner or their agent can apply/merge these verified changes. Scientific implementation, experiment configurations, results and report/notebook/integration work still require the project review process. Never use a setup label to bypass reviews of project work.

- Work only on the assigned package and its report/notebook/test files. Shared-interface changes need a focused PR and review from affected owners. Record interface decisions in docs/DECISIONS.md.
- Reuse `mm_allee.models` and `mm_allee.solver`; do not copy model equations into notebooks or experiment scripts. Torch equations belong in `mm_allee.pinn` and require parity tests against NumPy functions.
- The scaffold is not the final solution. Do not mark a work package complete because starter tests pass. Implement every core acceptance item, and list deferred extras explicitly.
- For project work, use small task branches and PRs. The human member is PR author/assignee, and all other four humans review. Never self-approve, impersonate reviewers, auto-merge, force-push main or push project work directly to main. The setup exception above does not supply any scientific approval.
- Never invent member names, numerical results, datasets, references, approvals or CI outcomes. Do not call synthetic data real observations.

## Scientific correctness

- Preserve the nondimensionalisation, boundary convention, critical-case stability, comparison units and inverse-identifiability rules in the scientific contract.
- Derive formulas in the report and notebook; support numerical claims with independent tests or references, not duplicated implementation formulas alone.
- Do not evaluate A's original ODE residual on an artificial post-extinction zero segment. Do not fabricate a closed hysteresis loop by resetting initial populations without disclosure.
- Fix seeds and record configuration, tolerances, hardware, versions, commit SHA and all failed seeds. Never tune on final held-out data or hide poor PINN results.
- Preserve autograd: do not cast trainable tensors to Python floats or detach them in a physics residual. Use fixed scaling for unknown dimensional parameters.

## Implementation and handoff

- Keep logic in `src/`; notebooks explain and invoke it. Use plain Python, NumPy/SciPy/Matplotlib and optional PyTorch. Avoid web services and unnecessary frameworks.
- Add meaningful deterministic tests, including edge cases and numerical convergence where appropriate. Slow training is a separate experiment with an explicit budget.
- Follow the [required evidence for every task](docs/TESTING.md#required-evidence-for-every-task): map completed core claims to named tests/recorded experiments, use independent expectations, justify tolerances and expose missing coverage. Never substitute a large test count or a passing starter suite for the task's mathematical acceptance criteria.
- Write plots to PNG + EPS with opaque fills. Commit only small curated outputs with provenance; ignore environments, bulk runs and weights.
- Update your report section, notebook fragment, AI-use log, package checklist and STATUS.md with the same PR. Record actual commands and outcomes in the PR body.
- Explain the equations and algorithms in language the member can defend. Mark code/test completion separately from the human's own understanding/review; do not certify understanding on their behalf.
- Keep the task checklist, STATUS.md and the actual AI-use log current. Report unavailable checks honestly.

## End-of-session handoff

Leave a brief **Current handoff** section in the chosen task brief (or update its existing one): chosen task/owner if known; branch and PR; completed checklist items and actual evidence; exact next command/step; dependencies or blockers; decisions about interfaces; the key explanation and any still-open understanding question. This lets a different agent resume without another chat's memory.

In the user-facing handoff, state the result in plain language, files/figures produced, exact reproduction commands, tests and observed outcomes, limitations and unfinished work. For project implementation, prepare/open the PR when ready; request all four other humans once their handles are known. If the roster is incomplete, keep useful work on a branch/open PR and report that reviewer requests remain pending. **Do not stop local implementation just because names are missing, invent reviewers, merge your own project PR or push project work directly to main.** Verified setup/assignment administration follows the owner-authorised exception above.
