# Local setup

Use Python 3.11 for team runs and CI. The scaffold also supports Python 3.12; keep final runs on one recorded version. CPU is sufficient for classical analysis and small PINN experiments; GPU use is optional and must be reported.

## Clone and create an environment

After the private repository exists and your invitation is accepted:

```bash
git clone https://github.com/devam2006/mm-allee-harvesting.git mm-allee-harvesting
cd mm-allee-harvesting
```

Linux/macOS/WSL:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev,notebook]"
```

Windows PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev,notebook]"
```

If PowerShell blocks activation, directly call `.\.venv\Scripts\python.exe -m pip install -e ".[dev,notebook]"` and use that Python path for all commands; no machine-wide execution-policy change is needed. In VS Code/Jupyter select this environment, not a different global interpreter.

WP04/WP05:

```bash
python -m pip install -e ".[pinn]"
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
```

For a specifically CPU-only PyTorch wheel use the official install selector linked in `docs/REFERENCES.md`; do not install arbitrary CUDA packages. The PINN extra is separate so the three classical-analysis owners do not need Torch. No cloud inference keys or `.env` file are required.

## Verify

```bash
python scripts/sync_team.py --check
python -m pytest -q
ruff check .
ruff format --check .
python scripts/smoke.py
python scripts/assemble_notebook.py
jupyter nbconvert --to notebook --execute notebooks/project.ipynb --output project.executed.ipynb --output-dir results
```

The starter notebook is explicitly labelled incomplete. Its successful execution validates imports and assembly, not completion of any work package. A/B PINN training scripts are to be implemented by WP04/WP05, not silently simulated by the smoke script.

## Dependency and environment records

`pyproject.toml` is the single source for dependency ranges. `requirements*.txt` are convenience wrappers around its extras, not separately maintained lists. Use a clean virtual environment and capture actual resolved versions for every reported run:

```bash
python -m pip freeze > results/environment.txt
python -m pip check
```

Commit an inspected environment snapshot to `artifacts/manifests/` with the final run, not your entire unrelated global environment. These ranges are not a fully locked environment; WP03 owner freezes the successful final environment before clean reproduction. A changed dependency needs its own PR and tests.

## LaTeX and EPS

Install a LaTeX distribution with `latexmk` and `epstopdf` (for example TeX Live or MiKTeX). The skeleton report includes no result figures yet. From the repo root:

```bash
latexmk -pdf -cd report/main.tex
```

Use PNG for notebook display and export **EPS** alongside it with `mm_allee.plotting.save_figure`. For the PDF report use PDF/PNG graphics or a controlled EPS-to-PDF conversion; always include original EPS files in the submission bundle. Use opaque colors because EPS cannot preserve normal alpha transparency. Verify both the PDF and figure files visually before release.

## What gets committed

Commit source, configs, tests, unexecuted notebook fragments, report sources, cited references, small curated PNG/EPS figures and tables, and manifests. `.gitignore` excludes environments, caches, local runs, generated/raw bulk data, weights, secrets, editor settings, LaTeX temporary output and local submission zips. The final PDF is built for the hand-in bundle; do not ignore all `.pdf` or `.eps` files globally. The provided course PDF is versioned under `docs/course/`.

For large retained results attach a versioned release artifact or use an agreed external location and record its checksum; do not place multi-GB training outputs in Git. Nothing scientific should require an undocumented notebook cell or a private absolute path.
