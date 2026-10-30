# Five-package notebook integration

The integration combines classical PR #11 (`649e0c1`, including current WP01
`b83bba8`, WP02 `879b110`, WP03 `16a05ce`) with Prem's WP04/WP05 PR #10
`00393cd78057e8b16c50698521f0a91ed341fb12`. Source PRs remain open for human review. No PR was merged or approved
by the agent. The report is maintained in Overleaf, not assembled here.

## Reporting-fix review, 31 October 2026

Prem added `7b502cc` (runtime fixes and ten regression tests), followed by
`00393cd` (refreshed 54-fit evidence and scientific wording). All ten reporting
regressions and the full 301-test source suite passed independently; both
GitHub CI jobs passed on `00393cd`. The refreshed integrated source passed
521 tests before adding four further direct forward/inverse parity cases;
all four parity cases also passed. They compare the inverse trainer's actual
logged physics loss with the forward residual API under `tau = r*t` for both
models and nonunit growth rates/population scales, with learning frozen.

Validation loss now measures the returned model when selection is disabled;
changing validation observations leaves the trained state unchanged. Exceptions
return `lbfgs_failed`, `success=False`, a message and the Adam fallback. Separate
L-BFGS outcomes distinguish tolerance, iteration-limit and abnormal exits.
The legacy `status=converged` means training completed, **not** optimizer
convergence; read `optimizer.lbfgs_outcome` and the exported table columns.

The refreshed table has 54 PINN iteration-limit exits, no reported optimizer
errors, and no abnormal exits. All 324 parameter rows and 108 prediction rows
retain their previous numerical results (only runtime and exit columns change).
These are independent audits of Prem's regenerated evidence, not a second
independent execution of his full sweep. Clean recovery remains 10/18.
See [the focused final review](PREM_PR10_FINAL_REVIEW.md).

## Previous handoff verification (before Prem's fixes)

- Full source suite: **511 passed**, including JAX tests.
- The portable notebook ran in a real fresh Jupyter kernel from an isolated
  folder: **27 code cells, zero errors, 28.6 seconds**. It exercised the forward
  and inverse demonstrations; historical final sweeps were read from curated
  evidence rather than retrained. Existing Windows/Python 3.14.3 dependencies
  were used; this was not a new dependency installation.
- The first portability attempt found a missing `experiments/integration`
  helper in the embedded payload. The exporter now includes that helper and
  embeds static Markdown figures as notebook attachments. The subsequent kernel
  run passed. These were packaging fixes, not changes to the scientific engine.
- WP01–WP03 explanations contain coloured question/method callouts, equations,
  numerical algorithms before code, labelled outputs and interpretation. The
  common threshold/basin contract is described consistently in all three.
- The archive builder validates execution counts/errors, EPS companions,
  synthetic-data split audits and all archived SHA-256 checksums.

## Deliverables and reproduction

The previous PR #5 handoff rerun passed all **511 tests in 40.80 seconds**. Its
portable notebook ran **27 code cells with no errors in 26.83 seconds**. The
same notebook was then extracted from the actual delivery ZIP and rerun in a
second isolated fresh kernel: **27 executed cells, no errors** (24.48 seconds
between the first cell starting and the last cell completing). Its bytes are
bound by the archive manifest's `executed_notebook_sha256`.

The ZIP contains **17 PNG/EPS pairs across all five packages** (15 current or
exploratory figures and two explicitly historical WP05 pairs), available PDF
partners, six clean synthetic trajectory CSVs, and **5,454 reconstructed
observation rows in 54 scenarios**. Every file is covered by SHA-256 inventory;
the checksum inventory itself is excluded from its own list. Representative
WP04 forward and WP05 held-out plots were visually inspected. Classical PR #11
also passed both GitHub CI jobs on `649e0c1`.

`notebooks/project.ipynb` is the readable repository notebook;
`notebooks/project_standalone.ipynb` embeds its source/config/data/evidence.
The download archive contains an executed standalone `project.ipynb`, readable
source, configs, clean data, reconstructed noisy observations, current and
historical evidence/figures, environment details and checksums.

```bash
python scripts/assemble_notebook.py
python scripts/export_standalone_notebook.py --packages 1 2 3 4 5 --output notebooks/project_standalone.ipynb
# Execute the standalone notebook in a fresh Jupyter kernel, then:
python scripts/package_notebook_delivery.py --notebook results/project_standalone.executed.ipynb
```

No observed species dataset was used. Six frozen clean CSVs and the current
noise/split generator reconstruct the final-config observation scenarios with
explicit seeds and fixed scales. Reconstructed inputs are labelled accordingly;
they are not claimed byte-identical to an author's unsaved historical arrays.
The clean population column is evaluation truth and must not enter fitting.

## Scientific limitations and owner review

The two reproduced reporting defects have fixes verified above; the previous
open-finding warning is superseded. The notebook shows the separate L-BFGS exit
and returned-model validation loss. It does not interpret the legacy training
status as convergence. A unified status vocabulary and owner review of the
adopted settings/parameter contracts remain group decisions; four direct parity
tests now cover the previously missing computational integration check.

Poor conditioning/failed PINN recovery with tested settings is distinct from
the proven four-unknown Model B structural nonidentifiability. The clean ODE
baseline recovers all six cases; broad claims about every possible PINN setting
are not supported. Small seed samples do not prove statistical equivalence.

The full 54-fit inverse sweep and hundreds of shared-settings fits were not
repeated here. Curated tables retain their source provenance. Human scientific
review of the integrated contracts, presentation/rehearsal, and the
final Overleaf report remain separate requirements before final submission.
