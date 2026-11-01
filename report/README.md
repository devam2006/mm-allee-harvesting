# Current project report

**Start:** [compiled report PDF](MM_Project_Report.pdf) · [main.tex](main.tex) · [bibliography](references.bib) · [EPS figures](figures/).

The sources come from the supplied `MM_Project_Report - latest.zip`; the unchanged original export and per-file import hashes are in `source/`. Sections 1, 2, 3 and 5, front matter, abstract, conclusions and acknowledgements preserve the supplied wording. **Section 4 has been confirmed by its owner, Mehta Prem (1 November 2026).** This is the owner's own statement, given in conversation with the assistant that prepared the branch; it is not a GitHub review or approval.

The shared preamble restricts the PostScript-only `breakurl` hooks to an actual latex/dvips build. This fixes compilation with XeTeX without changing author prose. No generated `*-eps-converted-to.pdf` companions are committed. The published EPS files are originals; local builds may generate temporary conversions.

## Build

From this directory, with a TeX distribution, BibTeX and Ghostscript installed:

```bash
latexmk -pdf -shell-escape main.tex
```

Alternatively: pdfLaTeX, BibTeX, pdfLaTeX twice, with EPS conversion enabled. Build products and conversion companions are ignored. Consult the [publication checks](../docs/FINAL_PUBLICATION.md) for the Tectonic/Ghostscript commands actually used in the verification build and their limitations.

The current PDF is a compiled snapshot of this supplied report, **not an assertion that every owner review is complete**. `draft_report.pdf` is an older development preview. Figure styling in the Overleaf export can differ from curated experiment PNGs; the [evidence map](../docs/REPRODUCIBILITY.md) explains their origins. Reproduce the two supplementary WP05 illustrations with `python report/tools/make_extra_figs.py --output results/report-illustrations` from the repository root after installing the package.

## Update of 1 November 2026 (branch `report/submission`)
The sources were synchronised with the newer Overleaf export (`MM_Project_Report`, 1 Nov 2026 10:26; supplied hashes in [`source/import_manifest_2026-11-01.json`](source/import_manifest_2026-11-01.json), its README in `source/overleaf-export-2026-11-01-README.txt`). The earlier export remains unchanged in `source/overleaf-latest.zip`. Only four files differ in wording from the previous import: `02_model_b_history.tex` (two sentences), `04_forward_pinn.tex` (the "Choosing the setting" subsection was shortened to a trial-and-error description with confirmation on seeds 11, 22, 33; the sentence "always in scientific notation" was dropped), `05_inverse_validation.tex` (four small edits) and `acknowledgements.tex` (author name order). The shared preamble fix, trailing-space normalisation and LF line endings are kept. Figures and `references.bib` are unchanged in content.

Points noted when synchronising: Section 5.5 no longer contains the selection table or the 64-wide-network rule; "The PINN uses seeds 10,11" in Section 6 was a typing slip and is corrected to "seed 1011", as in the notebook (fit seed 1011, noise seed 11). The author name is written "Mehta Prem" throughout the report (title page and acknowledgements), at the owner's instruction; `team.json` and some repository documents still write "Prem Mehta".

The PDF was rebuilt with pdfLaTeX and BibTeX (MiKTeX 25.12; 32 pages, no unresolved references or overfull boxes), not with Tectonic as before.
