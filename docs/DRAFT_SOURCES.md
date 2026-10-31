# Source ledger for the notebook/data/figure handoff

| Package | Exact source | Scope |
|---|---|---|
| WP01 | PR #8 b83bba8c7f3c7d094d4439cf9b6d281a325ae4d0 | Original fixes plus both close-root/tolerance follow-up corrections |
| WP02 | PR #9 879b110b0b5bfac52840b6e2db5b6cf00cbec050 | Comparison/history plus consumer/provenance fixes |
| WP03 | PR #4 16a05ce2f2c8eabfca7a95bcecf78dd7b5e190c8 | Reviewed collapse/reference analysis plus effective-tolerance fix |
| WP01–WP03 integration | PR #11 649e0c1bd545d73f2ea153e09a4a214c6fd2324e | Shared thresholds/branches/exact fold, notebook structure and standalone export |
| WP04–WP05 | Prem PR #10 00393cd78057e8b16c50698521f0a91ed341fb12 | JAX shared setting, validated reporting fixes and refreshed 54-fit exit evidence |

The refreshed combined source passed 525 tests; its portable notebook executed 27 code cells without errors (29.53 seconds). Detailed checks are in `END_TO_END_INTEGRATION.md`. Its portable notebook ran in a real fresh Jupyter kernel (27 code cells, no errors). Notebook-only integration changes embed missing helpers/static figures and qualify current review limitations. Prem's latest trainer fixes and refreshed tables are included without modifying his implementation. Legacy status semantics remain explicit. All source PRs remain reviewable and unmerged.

Overleaf source ZIP and the supplied course PDF were inspected. Only existing EPS figures were present in the report snapshot, and other sections there were still scaffolds; collaborators maintain the report directly. This branch does not claim to refresh Overleaf or assemble a new report. Roster names were filled from that supplied report's acknowledgements; the existing more complete Devam name was preserved.

The current browser entry point is `notebooks/project_colab.ipynb`, publicly hosted at `devam2006/mm-allee-notebook-runtime` (notebook c4abf90, assets 774d3d2). The browser export adds no scientific changes: 531 tests and a 32-code-cell anonymous-download kernel run passed. See `COLAB_QUICKSTART.md`; earlier embedded-export counts/timings above remain historical.
