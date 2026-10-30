# Five-package notebook integration

The integration combines classical PR #11 (`649e0c1`, including current WP01
`b83bba8`, WP02 `879b110`, WP03 `16a05ce`) with Prem's WP04/WP05 PR #10
`c84a0bf`. Source PRs remain open for human review. No PR was merged or approved
by the agent. The report is maintained in Overleaf, not assembled here.

## Observed verification

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

## Scientific limitations still requiring the owners

Prem's latest reviewed Python engine still has the two PR #10 reporting
findings: selection-off validation-loss histories can be undefined, and an
L-BFGS exception/iteration exit can be labelled converged. This work does not
silently rewrite the trainer or relabel its historical fits. The notebook now
discloses those limitations. Passing execution and finite prediction metrics
do not establish that optimizer convergence labels are trustworthy.

Poor conditioning/failed PINN recovery with tested settings is distinct from
the proven four-unknown Model B structural nonidentifiability. The clean ODE
baseline recovers all six cases; broad claims about every possible PINN setting
are not supported. Small seed samples do not prove statistical equivalence.

The full 54-fit inverse sweep and hundreds of shared-settings fits were not
repeated here. Curated tables retain their source provenance. Human scientific
review, resolution of the reporting findings, presentation/rehearsal, and the
final Overleaf report remain separate requirements before final submission.
