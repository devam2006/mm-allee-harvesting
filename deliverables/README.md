# Downloadable notebook, data and figures

Download and extract [mm-allee-notebook-data-figures.zip](mm-allee-notebook-data-figures.zip).
Open the small `project_colab.ipynb` in Colab, or the executed `project.ipynb` in
Jupyter. The runtime ZIP beside it provides local code/data; a notebook opened
alone downloads the identical fixed snapshot from public GitHub. No private
repository access or Google Drive mount is needed. Install the scientific Python
dependencies listed in the first cell if they are missing.

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

[Open directly in Colab](https://colab.research.google.com/github/devam2006/mm-allee-notebook-runtime/blob/main/project.ipynb). This is the small browser entry point; the older encoded export is retained separately.
