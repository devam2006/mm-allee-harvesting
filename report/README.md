# Current project report

**Start:** [compiled report PDF](MM_Project_Report.pdf) · [main.tex](main.tex) · [bibliography](references.bib) · [EPS figures](figures/).

The sources come from the supplied `MM_Project_Report - latest.zip`; the unchanged original export and per-file import hashes are in `source/`. Sections 1, 2, 3 and 5, front matter, abstract, conclusions and acknowledgements preserve the supplied wording. **Prem's rewrite/confirmation of Section 4 remains pending.** Its present text is included verbatim and is not represented as owner-final.

The shared preamble restricts the PostScript-only `breakurl` hooks to an actual latex/dvips build. This fixes compilation with XeTeX without changing author prose. No generated `*-eps-converted-to.pdf` companions are committed. The published EPS files are originals; local builds may generate temporary conversions.

## Build

From this directory, with a TeX distribution, BibTeX and Ghostscript installed:

```bash
latexmk -pdf -shell-escape main.tex
```

Alternatively: pdfLaTeX, BibTeX, pdfLaTeX twice, with EPS conversion enabled. Build products and conversion companions are ignored. Consult the [publication checks](../docs/FINAL_PUBLICATION.md) for the Tectonic/Ghostscript commands actually used in the verification build and their limitations.

The current PDF is a compiled snapshot of this supplied report, **not an assertion that pending owner review is complete**. `draft_report.pdf` is an older development preview. Figure styling in the Overleaf export can differ from curated experiment PNGs; the [evidence map](../docs/REPRODUCIBILITY.md) explains their origins. Reproduce the two supplementary WP05 illustrations with `python report/tools/make_extra_figs.py --output results/report-illustrations` from the repository root after installing the package.
