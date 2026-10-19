# Bootstrap verification — 19 October 2026

This file records checks on the **repository scaffold**. All five scientific tasks remain unclaimed and not started. No trained forward/inverse PINN, final scientific report, final result figures or final presentation is claimed.

## Passed locally, including isolated virtual-environment verification

- Python 3.12.14 used for bootstrap verification; team/CI target remains Python 3.11, which must be verified remotely or by a teammate.
- At the user's request, repeated verification from a fresh `.venv` with system packages excluded and the user-site disabled. Confirmed `git check-ignore .venv/pyvenv.cfg` succeeds and no `.venv` files are tracked. All core, notebook/dev and CPU-PyTorch dependencies were installed there; package imports resolve to that environment.
- Isolated-environment dependency health check: `pip check` reports no broken requirements. The resolved versions are recorded in `artifacts/manifests/bootstrap_environment_py312_linux.txt`; the compact verification record is `artifacts/manifests/bootstrap_venv_verification.json`.
- Editable installation of the package succeeded; core and optional PyTorch modules import.
- `python -m pytest -q`: **41 passed**, including the optional autograd test, with no skips after installing CPU Torch.
- `ruff check .` and `ruff format --check .`: passed.
- Notebook schema validation and deterministic assembly: passed; 12 assembled cells, including 6 code cells.
- All 6 notebook code cells executed in order with one namespace in a fresh Python process. These are starter import/status cells, not completed experiments.
- Solver smoke for A/B: passed. A stops at its event with an exact zero endpoint; B retains its smooth equilibrium semantics. PNG/EPS export succeeded and the PNG was visually inspected.
- Event-time RK45 compared to independent quadrature in the tests; units/scaling, error metrics, data split rejection, B coefficient ambiguity and four-reviewer roster selection were checked.
- LaTeX skeleton compiled with bibliography; PDF pages visually inspected. A final compile has no overfull boxes or undefined references. The temporary PDF is deliberately under ignored `results/report-check/`, not presented as a final report.
- Existing relative Markdown links resolved, and the roster retains five unchosen tasks.
- Submission packaging refused the unfinished scaffold because the final report PDF was absent. Its additional placeholder/roster/EPS gates remain in the script; this check does not certify final scientific completeness.

## Not yet verified / external setup

- Standard clean-kernel Jupyter execution could not start here: this execution environment prohibits local socket binding (`Operation not permitted` for TCP and IPC). Direct fresh-process cell execution passed, but it is **not claimed as full kernel execution**. Run the documented `nbconvert --execute` command locally or in CI before integration acceptance.
- The user supplied `devam2006/mm-allee-harvesting-`; the connected GitHub API verified owner `devam2006`, private visibility and write access on 19 October 2026. Scaffold upload and remote Actions checks are in progress; collaborator invitations and branch protections remain pending. See `docs/REPOSITORY_ADMIN.md` for actual status.
- Browser creation was initially blocked by sign-in. The user subsequently created the private repository and supplied its link, allowing upload through the already-authenticated GitHub plugin. No collaborator invitations have been sent.
- Full task-specific acceptance tests and experiment outputs are still to be implemented by their chosen owners.

The version ranges in `pyproject.toml` are not a frozen final scientific environment. Record the actual resolved environment and final reproduction results when the experiments are complete.

The bootstrap dependency snapshot is specific to Linux/Python 3.12 and includes a CPU Torch wheel. It is evidence of the tested environment, not a universal cross-platform lock. Use `docs/SETUP.md` for ordinary installation and record a fresh environment for final experiments.
