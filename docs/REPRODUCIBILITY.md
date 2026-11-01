# Reproduce a result or figure

Run commands from the repository root after `python -m pip install -e ".[dev,notebook,pinn]"`. Outputs go to ignored `results/` directories unless an explicit curation flag is used. Reproduction should not overwrite the recorded artifacts by default. The report's owner-edited EPS originals are under `report/figures/`; experiment outputs are under `artifacts/`. They may differ in styling or EPS creation dates without implying new numerical experiments.

## Quick path and recorded evidence

The [final Colab notebook](../notebooks/project_colab.ipynb) runs classical studies and short PINN demonstrations, and loads saved long-study tables/figures. Its code is identical to the reviewed integration. The first cell restores the immutable runtime at public companion commit `6ff183adae6093c26e663dfac254d2c071ea06a0`, SHA-256 `def74213164d849f511f28c1ff8f581e87fef01ba67bb6b33c77934ff72ef64c`. The companion is unchanged by publication of the main project.

`notebooks/project.ipynb` uses the locally installed package instead. Rebuild it with `python scripts/assemble_notebook.py`. Owned explanations/code are in `notebooks/sections/`; custom final introduction, setup heading and acknowledgements are adjacent Markdown files. The canonical notebook contains no saved bulk outputs; executing it produces all figures. Executed validation copies are ignored under `results/`.

## Classical experiments: quick CPU commands

```bash
python experiments/wp01/run.py --config configs/wp01.json --output results/wp01
python experiments/wp02/run.py --config configs/wp02.json --output results/wp02
python experiments/wp03/run.py --config configs/wp03.json --output results/wp03-core --core-only
python experiments/wp03/generate_reference.py --config configs/wp03_reference.json --output results/wp03-reference
```

| Result / plot | Implementation and config | Recorded evidence | Notebook role |
|---|---|---|---|
| Logistic/Allee production curves and phase lines (`wp01_logistic_vs_allee`) | `src/mm_allee/equilibria_plots.py`, `equilibria.py`; WP01 command above | `artifacts/figures/wp01_logistic_vs_allee.*` | Generated live |
| Model A equilibrium branches/fold (`wp01_model_a_branches`) | Same; `configs/wp01.json` | `artifacts/tables/wp01_equilibria.csv`, `wp01_thresholds.json`; `artifacts/manifests/wp01_run.json` | Generated live |
| Perturbations near stable/unstable equilibria (`wp01_model_a_perturbations`) | `equilibria_plots.py`, shared `solver.py` | Paired figures under `artifacts/figures/` | Generated live |
| Model B roots/branches (`wp02_b_branches`) | `model_b.py`, `wp02_experiment.py`; `configs/wp02.json` | `wp02_b_equilibria.csv` and figure | Generated live |
| Fair initial-catch/threshold-fraction comparisons | `comparison.py`, `wp02_experiment.py` | `artifacts/tables/wp02_comparison.csv` | Generated live; selected rows displayed |
| Harvesting history/restocking (`wp02_history`) | `history.py`, `wp02_experiment.py`; WP02 config | `wp02_history_samples.csv`, `wp02_history_summary.csv` and manifest | Generated live; no state reset at reversal |
| Critical controls, basin map (`wp03_basins`) | `thresholds.py`, `collapse.py`, `collapse_study.py`, `experiments/wp03/run.py`; WP03 config | `wp03_thresholds.csv`, `wp03_basins.csv`, `wp03_core_analysis.json` | Generated live |
| Extinction curves and independent RK45/DOP853 checks (`wp03_extinction`) | Same plus shared `solver.py` | `wp03_extinction.csv` (427 rows), `wp03_event_validation.csv` (six cases) | Generated live; no integration through an equilibrium |
| Qualitative slow decline (`wp03_bottleneck_core`) | Core WP03 command; `trajectory_fractions_above_fold` config | `artifacts/figures/wp03_bottleneck_core.*` | Generated live; trajectories only, no asymptotic overlay |
| Six reference trajectories (`wp03_rk45_reference`) | `datasets.py`, `generate_reference.py`; `configs/wp03_reference.json` | Six CSVs in `data/fixtures/wp03_reference/`; `wp03_reference_validation.csv`, `wp03_reference.json` | Regenerated live; reference plot displayed |

All table names in this guide without directory prefixes resolve under `artifacts/tables/`; manifest names resolve under `artifacts/manifests/`. Exact settings and source/file checksums are in the corresponding manifests. The four core WP03 numerical tables match the historical study exactly. Its optional `wp03_sensitivity_yield` and old two-panel `wp03_bottleneck` figures are retained historical evidence, outside the final core presentation; running the WP03 command without `--core-only` reproduces that historical extension.

## PINN experiments: recorded runs and explicit reruns

The following commands train models and can take substantially longer than the notebook. They are **not required to read or run the final notebook**. Keep the recorded budgets, seeds and settings when comparing results.

```bash
# Short smoke checks, not a rerun of the final benchmarks:
python experiments/wp04/run.py --config configs/wp04_smoke.json --output results/wp04-smoke
python experiments/wp05/run.py --config configs/wp05_smoke_shared.json --output results/wp05-smoke

# Recorded final designs (training reruns; use deliberately):
python experiments/wp04/run.py --config configs/wp04_final.json --output results/wp04-final
python experiments/wp04/run.py --config configs/wp04_confirm.json --output results/wp04-confirm
python experiments/wp05/run.py --config configs/wp05_final.json --output results/wp05-final
```

| Result / plot | Source and setting | Recorded outputs and scope |
|---|---|---|
| Forward predictions (`wp04_forward`) and error/loss (`wp04_error_loss`) | `src/mm_allee/pinn/` and `experiments/wp04/run.py`; `wp04_final.json` | `wp04_forward_metrics.csv`, `wp04_forward.json`; 18 PINN runs plus numerical baselines. Notebook loads the curated figures/tables and runs a separate short demo. |
| Forward confirmation seeds | Same runner, `wp04_confirm.json` | `wp04_confirmation_metrics.csv` and manifest; 18 additional PINN runs. Both recorded sets pass the stated 5% relative-$L^2$ criterion. |
| Exploratory activation/conditioning diagnostics | `experiments/wp04/select_activation.py`, `diagnose.py`; `wp04_act_*.json`, `wp04_diagnose.json` | Earlier diagnostic tables/figures; informative historical studies, not the final selected setting. |
| Inverse parameter recovery (`wp05_recovery_noise`) and held-out predictions (`wp05_heldout_failure`) | `pinn/inverse.py`, `inference.py`, `validation.py`, `experiments/wp05/run.py`; `wp05_final.json` | `wp05_parameter_metrics.csv`, `wp05_prediction_metrics.csv`, `wp05_inverse.json`; 108 fits total, including 54 PINN fits. The notebook loads these recorded tables. |
| Clean inverse demo parameter trajectory (`wp05_demo_clean_parameter_trajectory`) | Final notebook WP05 clean-demo cell; its explicit budgets/settings are the authoritative demo config | `wp05_demo_clean_parameter_trajectory.csv`, `wp05_notebook_demo.json` and figure; also generated live. It differs from the frozen final sweep. |
| Identical 1% noisy observations: ODE/PINN (`wp05_demo_observations_1pct`) | Final notebook WP05 noisy-demo cell and shared inverse/ODE APIs | Demo manifest and plot; generated live, not part of the 108-fit count. |
| Report split and structural-counterexample illustrations (`wp05_splits`, `wp05_counterexample`) | `python report/tools/make_extra_figs.py --output results/report-illustrations` | Supplied EPSs under `report/figures/`; illustrative computations only, no training. |
| Shared-setting selection and confirmation | `experiments/integration/shared_settings.py --config configs/shared_stage1.json --output results/shared-stage1` (and corresponding stage2/confirm configs) | `artifacts/tables/shared_*.csv`, related manifests; [study details](../experiments/integration/README.md). Development-era commentary is historical; current claims are checked against the recorded numerical tables. |

The Overleaf export contains its own styling variants of several WP05 plots. These are preserved as supplied, rather than silently replacing them with a different experiment. `report/source/overleaf-latest.zip` and its import manifest identify exact inputs. No expensive sweep was rerun for repository publication.

## Read the numbers correctly

Clean inverse recovery means **every fitted parameter** in a run has relative error at most 0.05. Group the three parameter rows by method and run ID at `noise_sigma == 0`: PINN recovers 10/18, ODE least squares 18/18. B near-fold is 3/3 PINN recovery under the frozen setting; A near-fold and B decline are 0/3, A extinction 1/3, and both regular regimes 3/3. Do not count parameter rows as fits or mix a demo with a benchmark.

The forward setting/confirmation tables contain 18 PINN rows each and meet the stated relative-error threshold. Earlier activation results and the shared-selection studies answer different questions. Legacy inverse `status=converged` denotes completed training; consult the explicit L-BFGS outcome. Known exact N0, known K and fixed external scales are part of the inverse design. The held-out observation window remains inside physics training support.

## Checks and report build

```bash
python -m pytest -q
ruff check .
ruff format --check .
python scripts/sync_team.py --check
python scripts/assemble_notebook.py
```

See [the report build instructions](../report/README.md). For a PDF-only engine such as Tectonic, first run `python scripts/prepare_report_build.py`; it converts EPS originals into temporary same-stem PDFs under ignored `results/report-build/` and adjusts only the staged graphic file extensions. Then run `tectonic -X compile results/report-build/main.tex --keep-logs`. No converted figure companions belong in Git. Scientific author text is preserved. Pending Section 4 review remains a content approval task even when a build succeeds.
