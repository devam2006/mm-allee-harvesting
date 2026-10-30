# Source ledger for the notebook/data/figure handoff

| Package | Exact source | Scope |
|---|---|---|
| WP01 | PR #8 b83bba8c7f3c7d094d4439cf9b6d281a325ae4d0 | Original fixes plus both close-root/tolerance follow-up corrections |
| WP02 | PR #9 879b110b0b5bfac52840b6e2db5b6cf00cbec050 | Comparison/history plus consumer/provenance fixes |
| WP03 | PR #4 16a05ce2f2c8eabfca7a95bcecf78dd7b5e190c8 | Reviewed collapse/reference analysis plus effective-tolerance fix |
| WP01–WP03 integration | PR #11 649e0c1bd545d73f2ea153e09a4a214c6fd2324e | Shared thresholds/branches/exact fold, notebook structure and standalone export |
| WP04–WP05 | Prem PR #10 c84a0bf7c52c29661018d9bfa0df8b0fa69c93fa | Current JAX shared setting and updated report/notebook prose; two reporting findings remain open |

The combined source candidate passed 511 tests. Its portable notebook ran in a real fresh Jupyter kernel (27 code cells, no errors). Notebook-only integration changes embed missing helpers/static figures and qualify current review limitations. They do not change Prem's trainer or relabel its historical statuses. All source PRs remain reviewable and unmerged.

Overleaf source ZIP and the supplied course PDF were inspected. Only existing EPS figures were present in the report snapshot, and other sections there were still scaffolds; collaborators maintain the report directly. This branch does not claim to refresh Overleaf or assemble a new report. Roster names were filled from that supplied report's acknowledgements; the existing more complete Devam name was preserved.
