# Downloadable notebook, data and figures

Download and extract [mm-allee-notebook-data-figures.zip](mm-allee-notebook-data-figures.zip).
Open its root `project.ipynb` in Jupyter and run all cells. This executed notebook
embeds the source/config/data/evidence it needs; no checkout or data download is
required. Install the scientific Python dependencies listed in its first cell.

The ZIP includes 17 PNG/EPS figure pairs, available vector PDFs, six clean
synthetic CSVs, 54 reconstructed observation scenarios, readable source and
experiment scripts, recorded tables, provenance, environment versions and file
checksums. Historical figures and reconstructed inputs are labelled explicitly.
The report is maintained separately in Overleaf.

[Verification and limits](../docs/END_TO_END_INTEGRATION.md) distinguish successful
execution from the verified inverse reporting fixes, legacy status semantics and recorded
research sweeps that were not independently rerun. This is an integration candidate awaiting
human reviews, not the group's completed final submission.

Rebuild after executing the portable notebook:

```bash
python scripts/package_notebook_delivery.py --notebook PATH_TO_EXECUTED_NOTEBOOK
```

The companion `.manifest.json` records the source revision, notebook and ZIP
hashes. `SHA256SUMS.json` inside the ZIP covers every other archived file.
