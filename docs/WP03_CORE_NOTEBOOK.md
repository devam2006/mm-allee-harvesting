# WP03 core notebook and editable report

Devam authorized a smaller WP03 contribution on top of PR #5 baseline
`2ab0cac2729c20ec77d80b307f7f789755fe0835`. That baseline already contains
Raghav's finalized WP01 and Rohan's finalized WP05 updates. Ashwath's next
WP02 notebook changes are not imported in this pass.

## Retained contribution

1. **3.1 Critical harvesting rates:** differentiate total growth for A and
   per-capita growth for B; show one dimensional example and independent maxima.
2. **3.2 Basins:** explain signs, the lower boundary, exact equilibria,
   zero-harvest cases and one-sided stability at the fold.
3. **3.3 Extinction time:** derive the separated integral and state its valid
   domain; distinguish finite extinction from asymptotic decline.
4. **3.4 Numerical checks:** adaptive RK45, its zero event, two tolerances,
   independent DOP853 and the measured comparison, with limitations.
5. **3.5 Slow decline:** show trajectories just above critical catch without
   asymptotic formulas or an inverse-square-root overlay.
6. **3.6 Reference data and limitations:** retain the six clean trajectories
   and their 606 sampled points, ownership boundaries and synthetic-data caveats.

This supports a four-to-five-minute story: harvesting limit, initial-state
boundary, extinction time, independent check, brief reference-data handoff.
Computational validation does not certify personal understanding or approval.

## Execution and compatibility

```bash
python experiments/wp03/run.py --config configs/wp03.json --output results/wp03-core --core-only
python experiments/wp03/generate_reference.py --config configs/wp03_reference.json --output results/wp03-reference
python scripts/assemble_notebook.py
python -m pytest -q
```

The notebook uses `--core-only`. It actually skips sensitivity derivatives,
elasticities, yield optimisation, policy margins and bottleneck asymptotic
tables. Its four tables retain the same numerical results as the historical
study: six threshold rows, 427 extinction rows, 34 basin cases and six event
checks. The new tests verify that optional routines are not called and that
core results/trajectories match the historical mode exactly.

The historical command without `--core-only` keeps the full study. Shared
models, threshold/root helpers, robust extinction evaluations, solver and
reference generator are unchanged. WP04/WP05 trainers, configurations,
datasets, frozen tables and owner-finalized notebook content are preserved.
The portable runtime pin must be refreshed to include the new WP03 runner;
that setup change does not change another work package's notebook section.

## Figures and report editing

The current WP03 report uses `wp03_basins.eps`, `wp03_extinction.eps` and the
new `wp03_bottleneck_core.eps`. The first two figures are unchanged. The
historical two-panel bottleneck and optional sensitivity/yield figure remain
development evidence, outside the reduced final package.

`report/sections/03_collapse.tex` is now an editable core-scope draft, following
Devam's explicit request. It is based on his supplied revised WP03 attachment,
with the bottleneck derivation replaced by a qualitative explanation and the
new trajectories-only figure. No teammate's report section is edited. The
separate blank Overleaf template ZIP remains unchanged.

The WP03-only Overleaf update ZIP contains this section, its three EPS files
and copying instructions. Copy these owned files into the current Overleaf
project; do not replace teammates' newer sections. The existing bibliography
keys `scipy_solve_ivp`, `scipy_quad` and `scipy_bounded` are retained. The
editable source is supplied for Devam's own review and final Overleaf layout.

The minimal group notebook/EPS ZIP is rebuilt with:

```bash
python scripts/package_notebook_eps.py --wp03-core
```

It excludes the two archived WP03 figures and includes the new core figure.
The final execution, scope checks and download hashes are recorded in the
delivery manifest and the PR #5 status update.

## Source verification

The complete source suite passed **533 tests in 58.58 seconds** (including
160 WP03 checks and the new core-mode regressions). Ruff lint/format (163
files), ownership synchronization and whitespace checks passed. The actual
core study completed in 3.01 seconds; its four numerical tables match the
historical records exactly. The new trajectories-only plot was inspected.
Final portable execution and download hashes follow in the delivery record.

## Final portable delivery

[Notebook](https://github.com/devam2006/mm-allee-notebook-runtime/releases/download/notebook-eps-v5/project.ipynb) · [Notebook/EPS ZIP](https://github.com/devam2006/mm-allee-notebook-runtime/releases/download/notebook-eps-v5/mm-allee-final-notebook-eps.zip) · [WP03 Overleaf update](https://github.com/devam2006/mm-allee-notebook-runtime/releases/download/notebook-eps-v5/wp03-overleaf-update.zip) · [Editable WP03 TeX](https://github.com/devam2006/mm-allee-notebook-runtime/releases/download/notebook-eps-v5/03_collapse.tex)

The actual new public runtime passed all **27 code cells with zero errors in
33.34 seconds**, producing **16 PNG outputs**. All other package sections,
front matter and acknowledgements are identical to baseline 2ab0cac in all
assembled/portable variants. Runtime bootstrap/pin changes carry only the new
WP03 runner; shared models/solvers, PINN code/configs and fixtures remain exact.
All embedded payload-file hashes and outer checksums were verified.

Notebook SHA-256: `0d1c8d95cf803d7360b21f2c9a3d45e521825a2cd118a7d31e613be0202322eb`.
ZIP SHA-256: `2a5a2199b67fbe2b30bc99698896d5f1d4ed75115c51c0e37a803a59075acd7a`; 510,803 bytes / 19 files.
WP03 report update SHA-256: `e08a324ac37ed86a033e40d10b104a58bc3ee29e5a297f2f80fe5ae311d10c94`; 166,855 bytes / five files.

The report update is editable LaTeX/EPS source; no compiled report PDF is
included or layout certification claimed. Compile the existing main.tex on
Overleaf after copying the owned files and make your final edits there.
