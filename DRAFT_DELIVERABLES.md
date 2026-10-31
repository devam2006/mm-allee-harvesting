# Notebook, dataset and figure handoff (PR #5)

**Current integration update:** reviewed WP01 notebook text from PR #12 and
WP02 notebook/provenance changes from PR #9 are being incorporated here. See
`docs/CLASSICAL_REFRESH.md`. Subsequent Prem/Rohan updates and the final ZIP
rebuild remain pending. The tracked/public ZIP downloads below are earlier
snapshots and do not yet contain this refresh.

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
