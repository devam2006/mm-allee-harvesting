# WP01–WP03 notebook integration

This branch combines WP01 PR #8 (`b83bba8`), WP02 PR #9 (`879b110`), and
WP03 PR #4 (`16a05ce`). The source PRs include the requested review fixes;
the integrated shared contract is reviewed here. No merge or human approval
is implied by machine checks.

## Shared mathematical contract

`thresholds.critical_a/critical_b` are the common critical-control providers.
WP01's `fold_a` and WP02's `critical_effort` delegate to them. WP01's A records
reuse WP03's positive branch solver. Only equality to the same computed critical
control denotes the fold; adjacent distinct controls remain sub/supercritical.
Floating output that cannot resolve a distinct pair is reported explicitly.
WP02 propagates WP03's initial-state `boundary_unresolved` outcome. Its
conservative comparison input exclusion remains separate from root topology.

This implements Devam's requested integration proposal; affected-owner review
is still required. It does not assert that all five humans agreed or understood
the mathematics. The historical source-branch convention notes remain provenance.

## Notebook and data

- `notebooks/wp01_wp03.ipynb`: readable assembled classical notebook.
- `notebooks/wp01_wp03_standalone.ipynb`: one portable file containing the exact
  source, configs, six clean synthetic reference datasets, tables and figures.
  It restores them to a temporary directory and requires no Git checkout or
  network data download. Standard scientific Python dependencies are required.
- `notebooks/sections/01_*`, `02_*`, `03_*`: editable explanations, equations,
  algorithms, labelled plots and interpretations. Colour callouts distinguish
  questions/methods. The standalone bootstrap is folded for readability.
- All examples are synthetic. No external observed dataset was used or claimed.
  `data/fixtures/wp03_reference/` contains six clean CSVs and provenance; noise
  and inverse observation construction remain WP05 responsibilities.
- Ten curated classical PNGs have EPS partners (three WP01, two WP02, five WP03,
  including the early numerical-reference figure). The Overleaf report is
  maintained separately; this PR does not assemble or compile LaTeX.

## Verification

Windows / Python 3.14.3, existing ignored review environment selected explicitly:

```text
python -m pytest -q                          421 passed, 1 optional Torch skip
ruff check .                                passed
ruff format --check .                       passed
python scripts/sync_team.py --check          passed
git diff --check                            passed
```

The standalone notebook executed in a **real fresh Jupyter kernel**, from a
separate folder: **16 code cells, zero errors, 20.49 seconds**. It emitted ten
PNG figures. The setup restores its embedded snapshot; no installed project
package or repository working directory is required. Representative branch
and basin figures were visually inspected. The kernel used the existing
scientific environment, not a newly downloaded dependency installation.

The course instructions require explanation/equations/algorithms before their
code, labelled outputs and interpretation. The classical fragments supply these;
execution success alone is not treated as proof of scientific completeness.

Rebuild:

```bash
python scripts/assemble_notebook.py --packages 1 2 3 --output notebooks/wp01_wp03.ipynb
python scripts/export_standalone_notebook.py --packages 1 2 3
```

The exporter is an authoring tool and uses the `dev,notebook` extras (including
Ruff for deterministic bootstrap formatting). Notebook execution needs only
NumPy, SciPy, Matplotlib and the usual Jupyter/IPython environment.

## Remaining group work

Update on 31 October: PR #5 integrates Prem's latest PR #10 `00393cd`.
Both reproduced inverse reporting defects have verified fixes. Four direct
forward/inverse physics-loss parity tests now pass in the integration branch.
The older open-finding note below is history; see
`docs/PREM_PR10_FINAL_REVIEW.md` for the current status.

Test this branch with Prem's current WP04/WP05 integration PR #10, then assemble
the five-package portable notebook, datasets and figure handoff in PR #5. Keep
the known inverse validation-loss/optimizer-status review findings visible until
fixed; neither a smoke fit nor old recorded convergence labels establish final
accuracy. Final presentation rehearsal, individual understanding, human review
and the Overleaf report are separate deliverables.
