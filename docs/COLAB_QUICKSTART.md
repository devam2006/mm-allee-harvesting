# Open and run the project

## Current draft integration candidate

PR #5 now includes the reviewed WP01/WP02 notebook updates and Prem PR #10
`a0cbbc9` wording. Use `notebooks/project_colab.ipynb` from this branch for that
candidate. It is 86,677 bytes and pins public runtime commit
`b0c6f278a5bff74dda2341cea3b0823c018c21de`, SHA-256
`1aa5283ac899d954ec3dc1115fd533e6d3824cec01518c45df210752d5472e17`.
The new public-download path passed 32 code cells without errors in 47.45 s.
Markdown math and table syntax were checked; the finalized WP03 cells are
unchanged. See [refresh evidence](CLASSICAL_REFRESH.md).

The public main notebook and release links below are **earlier published
snapshots**. They will be refreshed with the final ZIP after the remaining
owner updates; the new immutable runtime is already public for this candidate.

## Earlier published download

[Download the final notebook + EPS-only ZIP](https://github.com/devam2006/mm-allee-notebook-runtime/releases/download/notebook-eps-v1/mm-allee-final-notebook-eps.zip). This minimal download contains one notebook and 17 EPS figures only; the notebook fetches its public runtime on first run. The earlier full support archive described below remains separate.

[**Open the small notebook in Google Colab**](https://colab.research.google.com/github/devam2006/mm-allee-notebook-runtime/blob/main/project.ipynb).

Connect a CPU runtime and choose **Runtime → Run all**. No Drive mount, private
GitHub repository permission or API key is required. The first cell fetches a
fixed public snapshot (1.55 MB) and checks its SHA-256 before restoring it.
The scientific code and synthetic datasets are also readable in the
[public companion repository](https://github.com/devam2006/mm-allee-notebook-runtime).

The notebook is approximately **82 KB**, with a largest code cell of **2,634
characters**. The previous embedded export had a **5,250,542-character** setup
cell and a roughly 7 MB unexecuted file. It was executable in a kernel, but that
check missed the cost of opening/highlighting it in Colab's browser editor.
The small notebook has no encoded code payload or embedded image attachments.
All 15 figures appear as outputs when their cells run.

## Version and checks

- Public notebook commit: `0d2680ca1ed0164144b818c7fe5a5ee75148efc3`.
- Public asset commit: `774d3d2773e219e21a9859aa4d621a4988b7552d`.
- Runtime: `runtime/wp01-wp05-aa68d518ae054ca6.zip`; its full SHA-256 and
  source-file inventory are in `artifacts/notebook_runtime/manifest.json`.
- Anonymous notebook/runtime download returned HTTP 200 and the expected hash.
  The published notebook matches the tested notebook content.
- The actual public-download path ran in a fresh Jupyter kernel: **32 code
  cells, zero errors, 26.62 seconds**, including 15 PNG figure outputs.
- Full source suite: **531 passed in 55.60 seconds**, including six regressions
  for notebook/cell size, immutable refs, offline restoration, checksum
  rejection and archive path confinement.
- The extracted delivery notebook passed a second fresh kernel with external
  HTTP disabled: **32 code cells, zero errors, 29.37 seconds**, using only its
  packaged runtime ZIP.
- No live Firefox/Colab UI benchmark or browser RAM measurement is claimed.
  The Windows browser automation environment stopped UI control; the size
  budgets, anonymous retrieval and fresh-kernel execution were checked directly.

The public companion contains selected code, data, figures and provenance. It
does not contain private Git history, review discussions, credentials, trained
weights, the Overleaf report or historical presentation drafts. All data remain
synthetic. Existing PINN accuracy/identifiability limitations still apply.

## Download or reproduce

`notebooks/project_colab.ipynb` is the small entry point. The earlier full support
ZIP includes this notebook, an executed `project.ipynb`, all figure files,
datasets, readable source and its exact `runtime/` ZIP. With that directory next
to the notebook, a Jupyter kernel can restore locally without downloading the
runtime. Scientific dependencies must already be installed for offline use.

`notebooks/project_standalone.ipynb` remains the legacy embedded export; the
small public notebook is the recommended browser entry point.

To publish an updated scientific snapshot, first run:

```bash
python scripts/export_colab_notebook.py assets --public-dir PATH_TO_PUBLIC_CHECKOUT
```

Review and publish those selected public files, obtain that public commit SHA,
then generate the notebook pinned to that commit:

```bash
python scripts/export_colab_notebook.py notebook --asset-ref FULL_PUBLIC_ASSET_COMMIT
```

Execute the notebook in a fresh kernel, then build the handoff:

```bash
python scripts/package_notebook_delivery.py --notebook PATH_TO_EXECUTED_COLAB_NOTEBOOK
```

Public availability and machine checks do not replace the four human reviews,
owner agreement on shared contracts, final Overleaf work or presentation.

## Final Markdown from Devam

The attached `project_colab_markdown_fixed.ipynb` is the final notebook text.
Six WP03 Markdown cells use `$...$` / `$$...$$` in place of `\(...\)` /
`\[...\]`. The 32 code-cell sources, cell order/IDs and pinned runtime are
identical. Every changed Markdown string is exactly the delimiter conversion
of its prior text, so the equations and interpretation are unchanged.
The WP03 source fragment was updated and regenerates the attached notebook
exactly. Existing real outputs are retained from the identical tested code;
training was not repeated for this documentation-only update.
