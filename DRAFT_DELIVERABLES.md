# Notebook, dataset and figure handoff (PR #5)

The active deliverable is the small five-package Colab/Jupyter notebook and its companion archive under `deliverables/`; the runtime is hosted publicly and included locally in the archive. The editable LaTeX report is maintained in Overleaf; the old repository report/slide previews are historical and are not rebuilt by this task.

- `notebooks/project_colab.ipynb`: small recommended Colab/Jupyter entry point using a fixed public snapshot.
- `notebooks/project.ipynb`: readable assembled checkout notebook.
- `notebooks/project_standalone.ipynb`: larger legacy embedded export; use the small Colab entry point for browser use.
- `deliverables/mm-allee-notebook-data-figures.zip`: executed portable notebook, readable source, synthetic datasets, tables/provenance and EPS/PNG figures.
- `docs/END_TO_END_INTEGRATION.md`: measured checks and the verified WP05 reporting fixes and remaining review requirements.
- `docs/DRAFT_SOURCES.md`: exact source PR/commit ledger.

Run `python scripts/assemble_notebook.py`, then `python scripts/export_standalone_notebook.py --packages 1 2 3 4 5 --output notebooks/project_standalone.ipynb`. Execute in a fresh kernel from an isolated directory. Build the archive with `python scripts/package_notebook_delivery.py --notebook PATH_TO_EXECUTED_NOTEBOOK`.

The portable notebook executes the demonstrations and reads recorded final-sweep evidence; it does not silently repeat hundreds of historical fits. All data are synthetic. Human reviews/understanding, presentation/rehearsal and final Overleaf report remain separate requirements before submission. No final scientific approval or presentation date is invented.
