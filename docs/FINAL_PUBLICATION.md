# Final public repository verification

Publication preparation: **1 November 2026**. This records checks performed for PR #5, not a claim of new scientific experiments or formal teammate approval. The merged commit and final CI results are recorded in the PR timeline. The [publication manifest](publication_manifest.json) records input/output hashes and sizes.

## Final inputs and preserved scope

- Primary source: PR #5, `integration/final-deliverables-draft`, inspected at `4bfcdfc529c02097920a2ec8b4afb9ac706fb5a9` before this publication update.
- Devam supplied `MM_Project_Notebook-Latest.ipynb`. All 63 final cell sources are adopted exactly; all 27 code cells match the inspected PR #5 code. Source fragments and the Colab exporter reproduce those cell sources. Cleared outputs keep the public notebook small.
- The supplied `MM_Project_Report - latest.zip` is archived unchanged at [`report/source/overleaf-latest.zip`](../report/source/overleaf-latest.zip). The [import manifest](../report/source/import_manifest.json) records the original exported file hashes, before compatibility/formatting changes.
- Authored report wording is preserved, including Sections 1–5, front matter, abstract, conclusions and acknowledgements. Two trailing spaces were removed. Shared preamble changes restrict `breakurl` to a DVI/PostScript build and reduce table padding to fit the supplied wide table. The supplementary figure helper now accepts a usable output directory; its illustrative calculations are unchanged.
- **Prem's Section 4 rewrite/confirmation remains pending.** Its source is imported verbatim. In particular, its optimizer discussion must be reconciled by its owner with the recorded outcomes; budget exhaustion is not tolerance convergence. Successful compilation does not certify owner approval.
- Reduced WP03 scope is retained: critical harvesting controls, basins and critical cases, extinction integrals/times, numerical validation, qualitative bottleneck trajectories and six reference trajectories. Historical optional sensitivity/MSY/asymptotic artifacts remain clearly separated.
- PR #10 was inspected at `a0cbbc974f7ea0c6694ef504ef2bcdec6f77cd56`. Its PINN implementation, experiment configurations and recorded data are already incorporated in PR #5. No separate restoration of its older notebook is needed.

## Executed checks

| Check | Observed result |
|---|---|
| Complete Python test suite, `python -m pytest -q` | **533 passed**, 122.58 seconds |
| Final Colab notebook, fresh isolated kernel and actual pinned runtime download | **27 code cells, zero errors**, 93.09 seconds |
| Notebook figures | **16 PNG outputs**, all decoded and verified as images |
| Ruff lint and formatting | Passed |
| Generated ownership records, `python scripts/sync_team.py --check` | Passed |
| Clean inverse benchmark, independently grouped by method/run | **10/18 PINN**, **18/18 ODE least squares**, all fitted parameters within 5%; recorded total remains **108 fits** |
| Forward final and confirmation tables | **18/18 each** below 5% relative L2 error; observed maxima 0.004069712 and 0.002303257 respectively |
| Report build | **33 pages**, bibliography and internal references resolved; all 16 figure inclusions resolved |
| Report visual inspection | All 33 pages rendered and inspected; figures present, wide numeric table fits; no unresolved-reference markers or overfull boxes |
| Notebook/EPS download | ZIP integrity, notebook identity, 18 EPS figures and separate checksum inventory verified |
| Overleaf download | ZIP integrity, editable source/bibliography and EPS originals verified; no generated PDF figure companions |
| Secrets scan, Gitleaks 8.30.1 with redacted reporting | No findings in all fetched Git refs/history (101 commits, 116 MB) or working directory (65 MB), including archives to depth 2 |

The local test and notebook environment used Python 3.14.3; CI targets Python 3.11. Experiment environments are separately recorded in the existing manifests. These are measured local checks; CI must additionally pass on the exact PR head before merge. No expensive forward/inverse sweep was rerun for publication. The separate notebook demonstrations do not replace or enlarge the recorded benchmark.

## Report compilation

The verification build used **Tectonic 0.17.0** and **Ghostscript 10.07.0**. The original EPS files stay in Git. The staging helper copies sources to an ignored build directory, converts EPS into temporary same-stem PDFs, and changes only the staged graphic extensions:

```bash
python scripts/prepare_report_build.py
tectonic -X compile results/report-build/main.tex --keep-logs
```

Set `--ghostscript /path/to/gs` if Ghostscript is not on PATH. Copy `results/report-build/main.pdf` to `report/MM_Project_Report.pdf` after a successful build. The bundled LaTeX compiler also accepted the staged sources. No system pdfLaTeX/latexmk was available locally, so that alternative command is documented rather than claimed as tested. Remaining underfull-box messages concern spacing, not missing content.

Rebuild the uploadable source archive with `python scripts/package_report.py`. It excludes all PDFs, including generated EPS conversion companions. The original input export remains available separately for provenance.

## Runtime, evidence and publication policy

The public companion repository is unchanged. The loading cell remains pinned to runtime commit `6ff183adae6093c26e663dfac254d2c071ea06a0`, asset `runtime/wp01-wp05-def74213164d849f.zip`, SHA-256 `def74213164d849f511f28c1ff8f581e87fef01ba67bb6b33c77934ff72ef64c`. The [reproduction map](REPRODUCIBILITY.md) links the notebook's results to source, configurations, tables, figures and commands. All population data are synthetic; no external personal dataset or credentials are required.

Devam explicitly authorized this final integration merge and public publication, subject to actual GitHub protections. Inspection found no enforced main-branch protection or ruleset. No rule was disabled, no review impersonated, no force push performed and no historical branch/PR deleted. Formal GitHub review submissions were absent at inspection; the owner's reported completed reviews are distinct from formal approvals and from the still-pending Section 4 report confirmation. The normal PR workflow and green exact-head CI are used for the merge.

The [AI-use log](AI_USAGE.md) and report acknowledgements disclose collective assistance from ChatGPT, OpenAI Codex, Claude Code and Antigravity AI Assistant. Human authors remain responsible for the mathematics, interpretation and final report approval.
