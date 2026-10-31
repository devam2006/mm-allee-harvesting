# Five-package notebook, data and figure handoff

The current PR #5 source combines reviewed WP01–WP03 with Prem/Rohan's final
notebook layout and approved factual corrections. See
[FINAL_NOTEBOOK.md](docs/FINAL_NOTEBOOK.md) for the 29-cell execution and archive
checks. The Overleaf template remains blank, including WP03.

[**Download the final notebook + EPS figures ZIP**](https://github.com/devam2006/mm-allee-notebook-runtime/releases/download/notebook-eps-v2/mm-allee-final-notebook-eps.zip). It contains your finalized notebook and 17 EPS figures only. [Open the notebook directly in Colab](https://colab.research.google.com/github/devam2006/mm-allee-notebook-runtime/blob/main/project.ipynb), connect a CPU runtime and Run all. It downloads the fixed public code/data snapshot; no Drive mount or private repo access is needed. The Overleaf report is maintained separately. See `docs/COLAB_QUICKSTART.md` for reproduction details.

# MM project: harvesting under a strong Allee effect

**This is the five-package integration candidate.** [DRAFT_DELIVERABLES.md](DRAFT_DELIVERABLES.md) lists the current notebook/data/figure handoff and remaining human reviews. Older repository report/slide previews are historical; collaborators maintain the report directly in Overleaf.

**Approved title:** Harvesting under a Strong Allee Effect: Collapse Thresholds, Hysteresis and Comparison of Constant-Yield vs Proportional-Effort Harvesting, with Physics-Informed Neural Network (PINN) Forward and Inverse Analysis

Private, five-person Mathematical Modelling project. Humans own and explain the work; AI agents assist with implementation, checking and writing. This repository starts as a **tested scaffold and work plan**, not a completed scientific project. See [STATUS.md](STATUS.md).

## Start here — with your coding agent or on your own

**Using Codex, Claude Code or another coding agent?** Give it this repo and paste:

```text
Read AGENTS.md. Help me choose a task if I have not chosen one.
Explain my task with a small example, then help me implement it in stages
while explaining the maths, code, tests and results. Prepare a PR for review.
```

If you already chose a task, add **“I chose Task 3 (WP03)”**, changing the number. Your agent should read the task brief itself and explain the relevant parts to you. It should help you learn as it builds. You can also ask for explanation only, hints while you code, or shorter implementation updates.

**[New to the project? Start here](docs/START_HERE.md)** · **[Choose a task](docs/tasks/README.md)** · **[Set up Python](docs/SETUP.md)**

| Coding tool | Entry file |
|---|---|
| Codex | [AGENTS.md](AGENTS.md): the shared task, teaching and implementation playbook |
| Claude Code | [CLAUDE.md](CLAUDE.md): imports the same playbook |
| Other agents/chat tools | Ask them to open `AGENTS.md` explicitly after obtaining repository access |

The repo is private: the agent needs an authorised connection or your local checkout; the link alone does not grant access.

**WP03 numerical handoff:** [verified clean RK45 references for A/B](docs/WP03_RK45_HANDOFF.md), with generator, small CSVs and numerical evidence. WP05 owns noisy observations, splits and inverse fitting. Task 3's analysis is implemented on this branch; Devam's understanding review remains pending.

**Working manually?** Choose a task below, read its plain-language introduction and checklist, then use the setup guide. Read the [scientific conventions](docs/SCIENTIFIC_CONTRACT.md) for common equations and the [interfaces](docs/INTERFACES.md) when connecting your code to another task.

Whichever way you work, choose tasks with the group and record the choices in [team.json](team.json); the five GitHub handles are already listed there. For project work, make changes on a branch, request **all other four members as PR reviewers**, and merge only after four approvals and passing checks: [workflow](CONTRIBUTING.md). Owner-authorised repository setup and task-assignment administration do not need four approvals. Your task includes code, tests, figures, a report section, a notebook section and a contribution to the final [integration](docs/INTEGRATION.md).

**Task 3 results and reproduction:** [thresholds, extinction, basins and optional sensitivity/MSY](docs/WP03_ANALYSIS.md). The early [clean RK45 data handoff](docs/WP03_RK45_HANDOFF.md) remains available for Tasks 4/5.

**Understand Task 3:** [start with the plain-language WP03 guide](https://github.com/devam2006/mm-allee-harvesting/blob/wp03/collapse-analysis/docs/WP03_EXPLAINED.md), covering the basics, all implemented analyses, numerical methods, actual outputs and presentation questions.

## Five work packages

The original split overloaded the forward-PINN owner. Hysteresis moves to WP02; sensitivity and sustainable yield move to WP03. Each person owns one substantial analysis/computation package plus one integration responsibility. Suggested effort is roughly 18–22 focused hours each; revise after the first smoke run. These are estimates, not course requirements.

| Task | Package and original items | Main deliverables | Integration responsibility |
|---|---|---|---|
| Task 1 | [WP01: foundations and Model A](docs/tasks/WP01_foundations.md), items 1, 2(A), 6(A), logistic recap | Nondimensionalisation, Model A equilibria/stability and branch plot, shared math interfaces | LaTeX report assembly and EPS audit |
| Task 2 | [WP02: Model B and harvesting history](docs/tasks/WP02_model_b.md), items 2(B), 6(B), 7, 10; item 8 optional | B equilibria, fair comparisons, ramp/restocking experiment; slowing down if time permits | Slide assembly and rehearsal timing |
| Task 3 | [WP03: collapse and numerical reference](docs/tasks/WP03_collapse.md), items 3, 4, 5; 9, 11 optional | Threshold derivations, extinction quadrature/event checks, basins, synthetic reference generator | Final reproduction run and submission packaging |
| Task 4 | [WP04: forward PINNs](docs/tasks/WP04_forward_pinn.md), item 12 | Shared JAX PINN engine, both models, RK45 comparisons and error/runtime tables | Forward notebook section and shared PINN handoff |
| Task 5 | [WP05: inverse PINNs and validation](docs/tasks/WP05_inverse_pinn.md), items 13, 14 | Identifiable inverse designs, noise study, held-out tests, collapse failure cases | Notebook assembly, data provenance and AI acknowledgements |

Choose tasks with the group; record one distinct `work_package` (WP01–WP05) per person in `team.json`. Use `null` until a person chooses. The ownership display below is generated from that file; no task is preassigned by roster order. All five contribute references, AI-use records, report text, notebook explanations and their own presentation content.

## Team and task owners

<!-- team-sync:owners:start -->
**Contributors:** @devam2006, @Prem-Mehta03, @rohanagrawal28, @AshChan07, @RaghavSinghal15

| Task | Owner |
|---|---|
| [WP01: Foundations and Model A](docs/tasks/WP01_foundations.md) | @RaghavSinghal15 |
| [WP02: Model B and history](docs/tasks/WP02_model_b.md) | @AshChan07 |
| [WP03: Collapse and numerical references](docs/tasks/WP03_collapse.md) | @devam2006 |
| [WP04: Forward PINNs](docs/tasks/WP04_forward_pinn.md) | @Prem-Mehta03 |
| [WP05: Inverse PINNs](docs/tasks/WP05_inverse_pinn.md) | @rohanagrawal28 |
<!-- team-sync:owners:end -->

**When someone chooses:** update `team.json`, run `python scripts/sync_team.py`, and commit the updated JSON and docs together. This refreshes the README, task board, all five task briefs, status owners and presentation speakers. CI checks that they agree. Ownership appears on `main` after the owner applies or merges the administration update; no four-member review is needed for this setup step. Repository access is managed separately in GitHub Settings.

## Model and scope

Class baseline: `dN/dt = r N (1-N/K) - H`.

Model A: `dN/dt = r N (1-N/K)(N/A-1) - H`.

Model B: `dN/dt = r N (1-N/K)(N/A-1) - h N`, with `r>0`, `K>0`, `0<A<K`, `H,h>=0`.

Use `x=N/K`, `tau=r*t`, `a=A/K`, `q=H/(r*K)`, `e=h/r`. The shared functions use these dimensionless variables. Dimensional inverse inference must use **fixed, recorded reference scales**, never unknown true parameters hidden in preprocessing.

**Core:** foundations, stability, collapse thresholds, finite-time extinction, basins, branch diagrams, a correctly interpreted harvesting-history experiment, forward PINNs for A/B, inverse PINNs for A/B, noise and held-out validation. **Extras:** recovery slowing, threshold sensitivity and sustainable-yield safety margins. Extras must not delay core integration.

Important scientific rules:

- For `H>0`, zero is not an equilibrium of A. Stop the ODE at its first zero crossing; any subsequent zero segment explicitly means harvest shutdown and an absorbing extinction convention. For `H=0`, decline below A approaches zero asymptotically.
- B approaches zero asymptotically from positive initial states. A small-population cutoff is not an exact finite extinction time.
- A nonnegative harvest ramp up and down generally shows irreversible collapse/history dependence, **not a spontaneous closed recovery loop**. Show restocking as an explicit intervention.
- Under B with a single fixed effort, all four of `r,A,K,h` are structurally nonidentifiable from `N(t)` alone. Fix an independently known parameter for the main inverse study. Explain this limitation, rather than claiming unique four-parameter recovery.
- Synthetic trajectories must be labelled synthetic. No empirical species-specific conclusion is implied. PINNs are an evaluated advanced component, not presumed better than RK45.

Derivations and boundary cases: [SCIENTIFIC_CONTRACT.md](docs/SCIENTIFIC_CONTRACT.md).

## Repository layout

| Path | Purpose |
|---|---|
| `src/mm_allee/` | Shared installable Python package; numerical and PINN modules stay separate |
| `configs/` | Small versioned experiment configurations |
| `experiments/wp01/` … `wp05/` | Reproducible command-line entry points owned by each member |
| `tests/wp01/` … `wp05/` | Working scaffold checks, extended with each package's acceptance tests |
| `docs/tasks/` | Five detailed assignments and handoff checklists |
| `docs/` | Requirements, scientific/API/data contracts, testing and integration instructions |
| `notebooks/sections/` | Five independently editable notebook fragments |
| `notebooks/project.ipynb` | Single assembled executable submission notebook |
| `report/sections/` | Five independently editable LaTeX sections |
| `report/main.tex`, `references.bib` | Report entry point and bibliography |
| `presentation/` | Shared timed outline and eventual editable slides |
| `artifacts/figures/`, `tables/`, `manifests/` | Small curated, reviewed evidence committed deliberately |
| `data/` | Provenance instructions; generated bulk data ignored |
| `results/` | Local runs, checkpoints and logs; ignored |
| `scripts/` | Smoke run, notebook assembly, roster-aware PR creation, submission packaging |
| `.github/` | CI, issue and PR templates |

## Quick start

Python **3.11** is the team target. See [SETUP.md](docs/SETUP.md) for Windows PowerShell and Linux/macOS commands.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev,notebook]"
python -m pytest -q
python scripts/smoke.py
python scripts/assemble_notebook.py
```

WP04/WP05 additionally install `python -m pip install -e ".[pinn]"` (JAX, CPU, float64; the PINN engine is JAX-based). Nothing needs an API key. Run `ruff check .` and `ruff format --check .` before a PR. The [testing guide](docs/TESTING.md) distinguishes existing scaffold checks from still-required scientific validation.

## Actual course deliverables

The group has confirmed an **extension slot of 30 minutes including Q&A** (user confirmation, 19 October 2026), superseding the PDF's usual 10+5-minute slot for this project. Plan **25 minutes of presentation + 5 minutes Q&A**, about 5 speaking minutes per member. All five members must understand and explain the submission.

- Editable LaTeX source, compiled PDF, bibliography and **EPS figure files**: 3 marks.
- One executable Jupyter notebook, with detailed Markdown/equations/algorithms before code, labelled plots and interpretations: 2 marks.
- Presentation and individual understanding: 5 marks.
- Advanced methods such as PINNs may earn up to 5 bonus marks when mathematically explained and credibly validated; no automatic bonus.
- Submit the report source, figures, PDF and notebook **at least one week before** the presentation. Presentations must finish **before 14 November 2026**. Topic/date/time approval is due **19 October 2026**; topic approval is already reported by the group, date/time are unrecorded here.

[Submission checklist, ownership, integration order and relative deadlines](docs/INTEGRATION.md). [Course source PDF](docs/course/Mathematical_Modeling_project_instructions.pdf).

## First team actions

1. Confirm presentation date/time and record it in `docs/INTEGRATION.md`.
2. Choose the five packages, update `team.json` and run `python scripts/sync_team.py`; the repo owner grants the other four accounts write access.
3. Enable the available branch protections and review gates described in [REPOSITORY_ADMIN.md](docs/REPOSITORY_ADMIN.md). They are **not enabled by these files**.
4. WP01/WP03 settle model/solver/data interfaces first; WP04 starts the shared PINN engine; WP05 develops its inverse design and data checks in parallel.
5. Use the package-level checklists; a green scaffold CI is not a completed project.
