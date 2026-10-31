# Notebook, dataset and figure handoff (PR #5)

**Latest WP05-only update:** the additional Rohan notebook changes are now integrated only into WP05; all other cells are identical. The v3 ZIP includes the two new WP05 EPS plots (19 EPS total). See `docs/WP05_NOTEBOOK_UPDATE.md`.

**Earlier final notebook update:** Prem/Rohan's supplied layout is integrated with the reviewed WP01–WP03 work. All 29 code cells executed without errors. The refreshed notebook/EPS-only ZIP is described in `docs/FINAL_NOTEBOOK.md`; the older draft-refresh notes and full support archive remain provenance. The report template remains blank in every body, including WP03.

The requested final download is `deliverables/mm-allee-final-notebook-eps.zip`: one finalized notebook and 17 EPS figures only. It has no report, PDF or PNG exports. The notebook downloads its fixed public runtime on first use. The older full support archive is retained separately. The editable LaTeX report is maintained in Overleaf; the old repository report/slide previews are historical and are not rebuilt by this task.

- `notebooks/project_colab.ipynb`: small recommended Colab/Jupyter entry point using a fixed public snapshot.
- `notebooks/project.ipynb`: readable assembled checkout notebook.
- `notebooks/project_standalone.ipynb`: larger legacy embedded export; use the small Colab entry point for browser use.
- `deliverables/mm-allee-final-notebook-eps.zip`: requested final notebook + EPS-only export, publicly downloadable.
- `deliverables/mm-allee-notebook-data-figures.zip`: separate earlier full support archive, with source/data/runtime and display variants.
- `docs/END_TO_END_INTEGRATION.md`: measured checks and the verified WP05 reporting fixes and remaining review requirements.
- `docs/DRAFT_SOURCES.md`: exact source PR/commit ledger.

Run `python scripts/assemble_notebook.py`, then `python scripts/export_standalone_notebook.py --packages 1 2 3 4 5 --output notebooks/project_standalone.ipynb`. Execute in a fresh kernel from an isolated directory. Build the archive with `python scripts/package_notebook_delivery.py --notebook PATH_TO_EXECUTED_NOTEBOOK`.

The portable notebook executes the demonstrations and reads recorded final-sweep evidence; it does not silently repeat hundreds of historical fits. All data are synthetic. Human reviews/understanding, presentation/rehearsal and final Overleaf report remain separate requirements before submission. No final scientific approval or presentation date is invented.
