# MM project: harvesting under a strong Allee effect

**Approved title:** Harvesting under a Strong Allee Effect: Collapse Thresholds, Hysteresis and Comparison of Constant-Yield vs Proportional-Effort Harvesting, with Physics-Informed Neural Network (PINN) Forward and Inverse Analysis

Private, five-person Mathematical Modelling project. Humans own and explain the work; AI agents assist with implementation, checking and writing. This repository starts as a **tested scaffold and work plan**, not a completed scientific project. See [STATUS.md](STATUS.md).

## Start here

1. Read [course requirements](docs/COURSE_REQUIREMENTS.md) and [scientific conventions](docs/SCIENTIFIC_CONTRACT.md).
2. Choose tasks, then fill the five names and GitHub handles in [team.json](team.json), then follow [SETUP.md](docs/SETUP.md).
3. Choose one unclaimed task in the [task board](docs/tasks/README.md) or the table below. Give your AI agent [AGENTS.md](AGENTS.md), that package, and [interfaces](docs/INTERFACES.md).
4. Make a branch and PR; request **all other four members as reviewers**. Merge only after all four approve the current changes and checks pass. See [CONTRIBUTING.md](CONTRIBUTING.md).
5. Deliver your code, tests, reproducible experiment outputs, report section and notebook section together. Finish with the [integration plan](docs/INTEGRATION.md).

## Five work packages

The original split overloaded the forward-PINN owner. Hysteresis moves to WP02; sensitivity and sustainable yield move to WP03. Each person owns one substantial analysis/computation package plus one integration responsibility. Suggested effort is roughly 18–22 focused hours each; revise after the first smoke run. These are estimates, not course requirements.

| Task (unclaimed) | Package and original items | Main deliverables | Integration responsibility |
|---|---|---|---|
| Task 1 | [WP01: foundations and Model A](docs/tasks/WP01_foundations.md), items 1, 2(A), 6(A), logistic recap | Nondimensionalisation, Model A equilibria/stability and branch plot, shared math interfaces | LaTeX report assembly and EPS audit |
| Task 2 | [WP02: Model B and harvesting history](docs/tasks/WP02_model_b.md), items 2(B), 6(B), 7, 10; item 8 optional | B equilibria, fair comparisons, ramp/restocking experiment; slowing down if time permits | Slide assembly and rehearsal timing |
| Task 3 | [WP03: collapse and numerical reference](docs/tasks/WP03_collapse.md), items 3, 4, 5; 9, 11 optional | Threshold derivations, extinction quadrature/event checks, basins, synthetic reference generator | Final reproduction run and submission packaging |
| Task 4 | [WP04: forward PINNs](docs/tasks/WP04_forward_pinn.md), item 12 | Shared PyTorch PINN engine, both models, RK45 comparisons and error/runtime tables | Forward notebook section and shared PINN handoff |
| Task 5 | [WP05: inverse PINNs and validation](docs/tasks/WP05_inverse_pinn.md), items 13, 14 | Identifiable inverse designs, noise study, held-out tests, collapse failure cases | Notebook assembly, data provenance and AI acknowledgements |

All five tasks are **unclaimed**. You and your teammates choose freely; then fill `work_package` in `team.json` with one distinct WP01–WP05 per person. No task is preassigned to Devam or anyone else. All five contribute references, AI-use records, report text, notebook explanations and their own presentation content.

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

WP04/WP05 additionally install `python -m pip install -e ".[pinn]"`. Nothing needs an API key. Run `ruff check .` and `ruff format --check .` before a PR. The [testing guide](docs/TESTING.md) distinguishes existing scaffold checks from still-required scientific validation.

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
2. Assign the five packages and fill `team.json`; owner adds the four collaborators with write access.
3. Enable the available branch protections and review gates described in [REPOSITORY_ADMIN.md](docs/REPOSITORY_ADMIN.md). They are **not enabled by these files**.
4. WP01/WP03 settle model/solver/data interfaces first; WP04 starts the shared PINN engine; WP05 develops its inverse design and data checks in parallel.
5. Use the package-level checklists; a green scaffold CI is not a completed project.
