# Instructions for AI agents

Read README.md, your assigned docs/tasks/WP*.md, docs/SCIENTIFIC_CONTRACT.md, docs/INTERFACES.md, docs/TESTING.md and CONTRIBUTING.md before editing.

## Scope and ownership

- Work only on the assigned package and its report/notebook/test files. Shared-interface changes need a focused PR and review from affected owners. Record interface decisions in docs/DECISIONS.md.
- Reuse `mm_allee.models` and `mm_allee.solver`; do not copy model equations into notebooks or experiment scripts. Torch equations belong in `mm_allee.pinn` and require parity tests against NumPy functions.
- The scaffold is not the final solution. Do not mark a work package complete because starter tests pass. Implement every core acceptance item, and list deferred extras explicitly.
- Use small task branches and PRs. The human member is PR author/assignee, and all other four humans review. Never self-approve, impersonate reviewers, auto-merge, force-push main or push directly to main after bootstrap.
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
- Write plots to PNG + EPS with opaque fills. Commit only small curated outputs with provenance; ignore environments, bulk runs and weights.
- Update your report section, notebook fragment, AI-use log, package checklist and STATUS.md with the same PR. Record actual commands and outcomes in the PR body.
- Explain the equations and algorithms in language the assigned human can defend. Ask that human to verify understanding before marking their work ready.
- Run `python -m pytest -q`, `ruff check .`, `ruff format --check .`, notebook assembly and relevant package tests. Report unavailable checks honestly.

## Agent handoff template

State completed core subtasks, files changed, exact reproduction commands, outputs and seeds, tests and results, scientific limitations, unfinished items, shared API changes and requested human review. Finish by opening a PR and requesting all other members once the roster is complete. Do not merge it yourself.
