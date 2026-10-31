# Source ledger for the notebook/data/figure handoff

The final notebook also incorporates Devam's supplied Prem/Rohan Markdown
attachment, preserving its WP04/WP05 layout with approved factual corrections.
See `FINAL_NOTEBOOK.md` for its exact SHA-256, preserved classical cells and final
execution/archive evidence. The source PR ledger below remains valid.

| Package | Exact source | Scope |
|---|---|---|
| WP01 | PR #8 b83bba8c7f3c7d094d4439cf9b6d281a325ae4d0; notebook PR #12 6deae943d56ce0481a80d2321ce590dbfa567180 | Reviewed numerical fixes and clearer notebook derivation/algorithm; checksum-only follow-up 58ff57a9cb183d6df868014a9e789778761232ea |
| WP02 | PR #9 cba9051dec77b82f7cf0aafb2ce3d82f1e14d832 | Reviewed comparison/history, dimensional notebook tables, dependency hashes and Windows POSIX-path fix |
| WP03 | PR #4 16a05ce2f2c8eabfca7a95bcecf78dd7b5e190c8 | Reviewed collapse/reference analysis plus effective-tolerance fix |
| WP01–WP03 integration | PR #11 649e0c1bd545d73f2ea153e09a4a214c6fd2324e | Shared thresholds/branches/exact fold, notebook structure and standalone export |
| WP04–WP05 | Prem PR #10 a0cbbc974f7ea0c6694ef504ef2bcdec6f77cd56 | Existing validated trainer fixes and 54-fit evidence, plus scoped clean-recovery and held-out-domain notebook wording |

The latest WP01–WP03 refresh and exact reproduction evidence are recorded in
`CLASSICAL_REFRESH.md`. Rohan's later independent updates remain for the next integration
pass. Existing ZIPs/public notebook releases are earlier snapshots until the
final packaging pass; they are not rebuilt as part of this refresh.

The refreshed combined source passed 525 tests; its portable notebook executed 27 code cells without errors (29.53 seconds). Detailed checks are in `END_TO_END_INTEGRATION.md`. Its portable notebook ran in a real fresh Jupyter kernel (27 code cells, no errors). Notebook-only integration changes embed missing helpers/static figures and qualify current review limitations. Prem's latest trainer fixes and refreshed tables are included without modifying his implementation. Legacy status semantics remain explicit. All source PRs remain reviewable and unmerged.

Overleaf source ZIP and the supplied course PDF were inspected. Only existing EPS figures were present in the report snapshot, and other sections there were still scaffolds; collaborators maintain the report directly. This branch does not claim to refresh Overleaf or assemble a new report. Roster names were filled from that supplied report's acknowledgements; the existing more complete Devam name was preserved.

The current browser entry point is `notebooks/project_colab.ipynb`, publicly hosted at `devam2006/mm-allee-notebook-runtime` (notebook 0d2680c, assets 774d3d2). The browser export adds no scientific changes: 531 tests and a 32-code-cell anonymous-download kernel run passed. See `COLAB_QUICKSTART.md`; earlier embedded-export counts/timings above remain historical.

Devam's final Colab math-Markdown attachment is adopted verbatim in `project_colab.ipynb` and mapped back to the WP03 source fragment. All 32 code cells and the runtime pin are unchanged; the updated exporter rebuild matches the attachment exactly.
