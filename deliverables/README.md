# Current downloads

- [Final notebook and EPS figures](mm-allee-final-notebook-eps.zip): one `project.ipynb` and 18 EPS figures, 19 files total. The notebook matches the final supplied copy and downloads its unchanged pinned public runtime. First use requires internet. The [separate inventory](mm-allee-final-notebook-eps.manifest.json) gives SHA-256 checksums. Rebuild with `python scripts/package_notebook_eps.py --wp03-core`.
- [Overleaf source ZIP](MM_Project_Report.zip): editable LaTeX, bibliography and original EPS figures, with `main.tex` at the archive root. No PDFs or generated conversion companions are included. Rebuild with `python scripts/package_report.py`. **Prem's Section 4 rewrite/confirmation is pending**; the current source preserves the supplied text.
- [Compiled report PDF](../report/MM_Project_Report.pdf) and [canonical Colab notebook](../notebooks/project_colab.ipynb) are also available separately.

## Retained earlier packages

The larger `mm-allee-notebook-data-figures.zip` is retained for source/data/offline-runtime provenance. It is separate from the current minimal download. Old section-only report updates and report-writing templates are historical; use the complete current Overleaf ZIP above.

The public companion's [v6 release](https://github.com/devam2006/mm-allee-notebook-runtime/releases/tag/notebook-eps-v6) remains unchanged. Its notebook predates the final supplied Markdown adopted here; its runtime remains the verified code/data source used by the current notebook. Use the current repository downloads above for the final presentation copy.
