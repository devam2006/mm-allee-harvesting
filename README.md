# Mathematical Modelling of Population Harvesting under a Strong Allee Effect

**Equilibria, stability, extinction and PINN analysis** — a five-member Mathematical Modelling project at BITS Pilani, K K Birla Goa Campus.

A strong Allee effect means that a population below a critical size declines even without harvesting. We compare two harvesting policies, derive their survival thresholds, calculate extinction times, and assess physics-informed neural networks (PINNs) for solving the population equation and estimating its parameters. All examples and observations are **synthetic**.

## Start here

- **[Run the final notebook in Google Colab](https://colab.research.google.com/github/devam2006/mm-allee-harvesting/blob/main/notebooks/project_colab.ipynb)** — connect a CPU runtime and choose **Runtime → Run all**.
- **[Read/download the notebook](notebooks/project_colab.ipynb)** — this adopts the authors' final supplied notebook; its code matches the reviewed integration.
- **[Read the report PDF](report/MM_Project_Report.pdf)** · **[Overleaf source ZIP](deliverables/MM_Project_Report.zip)** · **[Editable LaTeX source](report/main.tex)** · **[Report figures](report/figures/)** · **[Bibliography](report/references.bib)**.
- **[Find a result and reproduce it](docs/REPRODUCIBILITY.md)** · **[Browse the synthetic data](data/README.md)** · **[Documentation index](docs/README.md)**.

**Report review status:** the supplied Overleaf text is preserved. The owner of the forward-PINN report section (`report/sections/04_forward_pinn.tex`), Mehta Prem, confirmed it on 1 November 2026 (the owner's own statement, not a GitHub review). A successful build and numerical checks are not an approval. Sections 1, 2, 3 and 5, the introduction, conclusions and acknowledgements are the supplied owner-edited text.

The notebook's first loading cell uses the existing **[public code/data companion](https://github.com/devam2006/mm-allee-notebook-runtime)**. Its immutable runtime commit and SHA-256 are unchanged. No private-repository login, Drive mount or API key is required; internet is needed for the first download. The companion and its historical releases are retained as they are.

## Models and mathematical results

Let $N(t)$ be population, $r>0$ a growth-rate parameter, $K>A>0$ the carrying capacity and Allee threshold. Natural growth is

$$g(N)=rN\left(1-\frac NK\right)\left(\frac NA-1\right).$$

| Policy | Equation | Harvest units |
|---|---|---|
| **Model A: constant catch** | $dN/dt=g(N)-H$ | $H$: population/time |
| **Model B: proportional effort** | $dN/dt=g(N)-hN$ | $h$: inverse time |

Use $x=N/K$, $\tau=rt$, $a=A/K$, $q=H/(rK)$ and $e=h/r$. For A the critical catch is the maximum of total growth; for B the critical effort is the maximum of per-capita growth:

$$x_* = \frac{1+a+\sqrt{1-a+a^2}}3,\qquad H_c=rKx_*(1-x_*)(x_*/a-1),\qquad h_c=\frac{r(K-A)^2}{4AK}.$$

Below the positive critical control, an unstable lower equilibrium separates decline from persistence. At the fold the positive roots merge into a semistable equilibrium, attracting only from above. Above the critical control, collapse follows. Under positive constant catch A can reach zero in finite time; B approaches zero asymptotically. A simulations stop at the zero event. Returning harvesting to zero need not restore a population below the Allee threshold; restocking is a separate intervention.

For the illustrative values $r=0.7$, $K=100$, $A=20$, we obtain $N_*=70.5505$, $H_c=36.7597$ and $h_c=0.56$. The logistic constant-catch reference is $rK/4=17.5$; equal $r,K$ do not imply equal production curves or a universal risk ranking.

## Numerical and PINN findings

- **Classical calculations:** threshold formulas are checked by independent numerical maximisation. Extinction quadrature is compared with two RK45 tolerances and an independently expanded-polynomial DOP853 solution. The recorded six-case maximum discrepancy is about $4.56\times10^{-8}$ in dimensionless time, not a universal error bound.
- **Forward PINNs:** the recorded final and held-out seed sets each have 18/18 runs within the predeclared relative-$L^2$ threshold $5\times10^{-2}$ (36/36 combined). Recorded failures in earlier settings are retained. This result concerns the tested synthetic cases, not arbitrary parameters.
- **Inverse benchmark:** at zero noise, every fitted parameter is within 5% in **10/18 PINN fits versus 18/18 ODE least-squares fits**. The full recorded benchmark has **108 fits** (54 per method), including three noise levels and three seeds. Good trajectory prediction does not guarantee parameter recovery.
- **Identifiability:** a single fixed-effort B trajectory identifies at most three polynomial coefficient combinations, not all four unknown parameters. Main inverse runs fix independently known $K$ and disclose exact known initial population. Held-out observations inside the physics collocation interval are physics-supported prediction, not unseen-domain extrapolation.

The notebook runs short demonstrations and reads the larger benchmark tables. The newer clean/1%-noise inverse demonstrations use their stated settings and are **not** replacements for the recorded 108-fit benchmark. Optimizer iteration-limit completion is distinct from tolerance convergence. See the [evidence map](docs/REPRODUCIBILITY.md).

## Contributors

| Contributor | Responsibility |
|---|---|
| Raghav Singhal | WP01: scaling, Model A equilibria, stability and root methods |
| Ashwath Chandramouli | WP02: Model B, fair policy comparisons and harvesting history |
| Devam Jatin Bhavsar | WP03: critical controls, basins, extinction, independent numerical checks and clean reference data |
| Prem Mehta | WP04: forward PINNs and shared neural-network setting |
| Rohan Agrawal | WP05: inverse PINNs, identifiability and validation |

WP03's current presentation retains the core analysis and a qualitative bottleneck, with no sensitivity/MSY or bottleneck-asymptotic exposition. The notebook, report and integration are collective work.

## Install and run locally

Python **3.11+** is required. From the repository root:

```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell instead:
# .\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev,notebook,pinn]"
jupyter lab notebooks/project_colab.ipynb
```

For classical experiments only, `python -m pip install -e .` installs NumPy, SciPy and Matplotlib; add `.[pinn]` for JAX and `.[notebook]` for notebook tools. The self-loading Colab notebook prepares its own pinned runtime, while `notebooks/project.ipynb` runs the current local package. These two paths are intentionally distinct.

```bash
python -m pytest -q
ruff check .
ruff format --check .
python scripts/assemble_notebook.py
python experiments/wp03/run.py --config configs/wp03.json --output results/wp03-core --core-only
```

The [reproduction guide](docs/REPRODUCIBILITY.md) gives WP01–WP05 commands and identifies the longer CPU training runs. Recorded environment versions are in [artifacts/manifests](artifacts/manifests/); timings and learned weights can vary across platforms.

## Repository map

| Location | What to find |
|---|---|
| [`notebooks/`](notebooks/) | Final Colab notebook, local assembled notebook and owned source sections |
| [`report/`](report/) | Current report sources, bibliography, original EPS figures, compiled PDF and review status |
| [`src/mm_allee/`](src/mm_allee/) | Shared models, thresholds, ODE solvers, inference and PINN implementation |
| [`experiments/`](experiments/) | Reproduction/plotting entry points for every work package |
| [`configs/`](configs/) | Recorded parameters, solver tolerances, seeds and training budgets |
| [`data/fixtures/wp03_reference/`](data/fixtures/wp03_reference/) | Six clean synthetic reference CSVs and provenance |
| [`artifacts/tables/`](artifacts/tables/) | Recorded comparison, accuracy, parameter and prediction tables |
| [`artifacts/figures/`](artifacts/figures/) | Curated PNG/EPS plots; historical optional figures are labelled in the guide |
| [`artifacts/manifests/`](artifacts/manifests/) | Configurations, environment information and checksums for saved results |
| [`tests/`](tests/) | Mathematical, numerical, interface and notebook regression tests |
| [`docs/`](docs/) | Scientific conventions, reproduction, references, validation and historical development records |
| [`deliverables/`](deliverables/) | Notebook/EPS packages; version information is in the adjacent manifests |

## Data, limitations, references and AI assistance

No field population dataset is used. Six clean trajectories are generated from the models; noisy observations, fixed splits and seeds are described in the [data guide](data/README.md). Evaluation truth is separate from fitting inputs. The models assume deterministic, well-mixed populations and constant parameters, without demographic/environmental randomness, age structure or delays. The calculations are not species-specific harvesting recommendations.

The report's [bibliography](report/references.bib) and [source notes](docs/REFERENCES.md) identify ecological, mathematical and software sources. The authors collectively acknowledge **ChatGPT, OpenAI Codex, Claude Code and Antigravity AI Assistant** for explanation, implementation, experiments, checking, integration and writing support; see the [report disclosure](report/sections/acknowledgements.tex) and [AI-use log](docs/AI_USAGE.md). The authors remain responsible for the results and explanations.

<details>
<summary>Contributor handles and detailed work-package notes</summary>

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

</details>
