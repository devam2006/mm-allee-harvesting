# Rohan's WP05 submission: intake and review

[**Draft PR #7**](https://github.com/devam2006/mm-allee-harvesting/pull/7). Owner/assignee: **@rohanagrawal28**. Uploaded by **@devam2006** at his request, from `Rohan_RK45_Completed_Code.zip`. This is a contribution submitted for review, not a completed or approved WP05 package.

## Scope and dependencies

- Branch: `wp05/rohan-inverse-validation`.
- Base: `wp03/collapse-analysis` at `6ba15550b0c72447c2652870e71ed7166ab5b6d9`, the open WP03 PR #4. Main still lacks the required reference fixtures after the earlier reverts. Merge/reconcile WP03 first, then retarget this PR to main.
- WP05 source, tests, configs, curated tables/figures, report section and notebook fragment were copied byte-for-byte. `artifacts/manifests/wp05_submission.json` records the archive and imported-file hashes.
- Existing WP03 source/fixtures/sections and project disclosures were retained from the base. The ZIP's duplicate `results/` files, older assembled notebook, stale portable metadata and unchanged scaffold are excluded. The combined notebook is regenerated from the current fragments.
- Supplied claims about completed experiments and human checks remain unverified. The original `wp05_manifest.json` is preserved as submitted, including its `completed` label; project status does not adopt that claim.

## Initial review findings

### [P1] Reconcile the PINN engine with WP04 before combining the branches

The WP05 submission creates independent **PyTorch** `pinn/network.py` and `pinn/residual.py` implementations and changes `pinn/__init__.py` and `autodiff.py`. Prem's open WP04 PR #6 uses **JAX** at those same paths with different network, residual and training APIs. Combining either version by overwriting the other breaks its consumer. WP04/WP05 owners need a reviewed shared-engine decision or explicit coexistence, followed by both packages' tests. No framework conversion is performed during intake.

### [P1] Reproduce and reconcile the claimed final sweep

`configs/wp05_final.json` specifies 6 cases x 3 noise levels x 3 seeds x 2 methods = **108 prediction records** (324 parameter records for the declared three fitted parameters). The submitted prediction CSV has **33 records**, leaving **75 configured combinations missing**. For example, clean regular cases include seed 11 only and most difficult-case combinations are absent. The submitted manifest nevertheless declares completion for all cases/noises/seeds.

There is also a code/output mismatch: `fit_ode_least_squares` emits `converged` or `failed: ...`, whereas the submitted prediction table includes ODE statuses `near_fold_instability` and `finite_extinction_truncation` that the runner does not generate. This does not establish how the supplied values were produced. Supply the actual generating revision/config/environment and run logs, retain all failed seeds, regenerate outputs, and update report claims from that evidence.

Visual inspection also finds that `wp05_heldout_failure.png` labels the regular paths as 45 -> 72 (A) and 45 -> 70 (B), whereas the referenced clean CSVs end at **96.09247** and **91.62271** respectively at t=8. The PNG lacks numeric axis scales, axis labels/units and observed samples. Its companion EPS identifies a different vector-graphics creator from the Matplotlib plotting function. Label any schematic explicitly and regenerate evidence figures from recorded observations/predictions; the supplied figure does not validate the claimed held-out fits.

### [P2] Seed the model before constructing its weights

`experiments/wp05/run.py` constructs `PINN(...)` before calling `trainer.fit(..., seed=seed)`. `torch.manual_seed(seed)` is called only inside `fit`, after network initialization. Consequently the configured seed does not control the starting weights and results can depend on process history or run order. Move seeding ahead of network construction and verify same-seed repetitions in separate fresh processes.

Observed probe: two three-epoch runs with `fit(seed=11)` and different RNG states before network construction produced predictions differing by up to **49.24057 population units**. These linear-data fault probes are not a parameter-recovery benchmark; see `artifacts/manifests/wp05_intake_probes.json`.

### [P2] Record failed or unconverged PINN fits honestly

`src/mm_allee/pinn/inverse.py` returns `success=True` and `status="converged"` unconditionally after the epoch loop and final metric evaluation. There is no convergence criterion. An observed three-epoch budget-exhausted run returned success/converged; a nonfinite-weight fault instead raised `ValueError: Metric inputs must be finite`, returning no failed-run record. The runner does not catch that error per seed or save partial tables before the whole sweep ends. Define statuses for nonfinite loss, exhausted budget and validation stopping, preserve failed-run records, and test these through the actual trainer. A short smoke execution does not establish parameter recovery.

## Validation and remaining acceptance

Local checks used Windows, Python 3.14.3 and Torch 2.15.0+cpu. Reproduction entry point:

```bash
python -m pip install -e ".[dev,notebook,pinn]"
python -m pytest tests/wp05 -q
python -m pytest -q
ruff check .
ruff format --check .
python scripts/sync_team.py --check
python scripts/assemble_notebook.py
python experiments/wp05/run.py --config configs/wp05_smoke.json --output results/wp05-intake-smoke
```

| Check | Observed result |
|---|---|
| WP05 tests | **27 passed** in 43.34 s on the first run |
| Full suite | **207 passed** in 11.89 s |
| Ownership sync | Passed, no changes |
| Notebook assembly | Passed, 30 cells; current WP03 fragment retained |
| Ruff lint after assembly | **35 errors** (including copied notebook-cell findings); fails |
| Ruff format | **10 files** would be reformatted; fails |
| PR whitespace check | Three existing submitted LaTeX lines contain trailing spaces; not edited during intake |
| Actual smoke run | Exit 0, **7.84 s**, 8 prediction / 24 parameter records, both A/B and methods |
| Notebook execution | All **13 code cells passed** in one fresh Python process (20.30 s). Full Jupyter launch stalled before output and was stopped; clean-kernel verification remains pending |

The first full-suite attempt had 205 passes and two inherited WP03 manifest-hash failures caused solely by Git's Windows CRLF checkout conversion. For each affected inherited output, the original Git blob was independently checked against the manifest hash and restored locally with canonical LF bytes; the rerun passed all 207 tests. No source, index content or inherited scientific result was changed to resolve this checkout issue. Set `PYTHONUTF8=1` when running the commands on Windows; the local temporary/cache directory was inside the workspace.

Smoke outputs are stored separately as `artifacts/tables/wp05_intake_smoke_{prediction,parameter}.csv` and summarized in `artifacts/manifests/wp05_intake_validation.json`. They do **not** replace the ZIP's claimed final results. In this short 50-epoch smoke, PINN test RMSE was about 1.96/7.17 for A and 4.54/4.72 for B (clean/1% noise), while ODE test RMSE was about 5e-8/1.09 for both models. This budget differs from the final configuration and does not validate or refute its claimed final metrics. Random initialization remains uncontrolled as described above. EPS export warned that transparent fills are rendered opaque.

Do not use the submitted full-sweep values as independently reproduced results. Final-sweep reproduction, report compilation, independent member reproduction, shared JAX/PyTorch integration, acceptance-evidence mapping and all human approvals remain pending. The task's acceptance boxes stay open. Test-tail predictions use collocation through the full horizon and must be labelled physics-supported prediction rather than extrapolation outside the physics domain.

The current CI workflow filters PRs to base `main`. A PR stacked on the WP03 branch will not automatically run those checks; absence of CI is not a pass. Recheck CI after retargeting, or deliberately run the workflow on this branch.

## Review ownership

Rohan remains the code owner and assignee. Devam is the technical GitHub PR author because the upload uses his connected account; this exception is explicit and does not impersonate Rohan. Review requests are verified for Prem (`Prem-Mehta03`), Ash (`AshChan07`) and Raghav (`RaghavSinghal15`). Devam's assisted review is recorded here; GitHub cannot count his approval on his own PR. Resolve how to record the four non-owner human reviews before merge. Rohan should verify the upload and answer the findings. No approval, merge or final readiness is asserted.
