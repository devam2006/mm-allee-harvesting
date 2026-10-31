# Final WP01–WP05 notebook

Devam supplied `project_colab_markdown_fixed _1_.ipynb` as Prem and Rohan's
edited notebook. Its SHA-256 is
`7ee09306a9eb66d056e57f8d23f1252c416c8940d29cbb2e8674bb5b8b689e75`.
This integration keeps the reviewed WP01–WP03 cells from PR #5 unchanged and
imports the supplied WP04/WP05 layout, including removal of exploratory sections.
Their source, tables and EPS figures remain available in the companion.

## Markdown and code reconciliation

The supplied introduction and contribution table are preserved exactly in
`notebooks/colab_introduction.md` and the final small notebook. Eleven of the
fourteen supplied WP04/WP05 Markdown cells retain identical content. The other
three have only the approved factual/reference corrections:

- The removed diagnostic is referenced as a companion study, rather than a
  nonexistent section further down the notebook.
- The held-out window is physics-supported prediction inside the collocation
  domain, rather than extrapolation outside that domain.
- Clean recovery matches the saved table: B near-fold 3/3, A near-fold 0/3,
  B decline 0/3, A extinction 1/3; overall clean PINN recovery is still 10/18.
  The exact independently known N0 and baseline extinction-padding disclosure
  are retained.

Devam explicitly authorized minimal factual corrections while keeping the
supplied formatting. WP04 cell IDs are renumbered on assembly because removed
cells are absent. Code adds an independent csv import and retains the supplied
`%matplotlib inline` reset, removing its unused matplotlib import. No model,
trainer, config, dataset or saved numerical result changes. The inline reset
allows plots to display after WP02's figure-saving backend.

The existing immutable runtime stays pinned to public asset commit
`b0c6f278a5bff74dda2341cea3b0823c018c21de`, SHA-256
`1aa5283ac899d954ec3dc1115fd533e6d3824cec01518c45df210752d5472e17`.
It already contains the reviewed classical fixes and shared PINN implementation.
The older runtime from the attachment is not restored.

## Verification and delivery

The small notebook has **68 cells / 29 code cells**, is **78,854 bytes** and has
a largest code cell of 2,634 characters. It opens without saved image outputs
or an encoded bootstrap payload. A genuine fresh-kernel run passed **29 code
cells with zero errors in 36.12 seconds**, emitted **16 PNG outputs** and ran
the WP02 comparison/history tables. Executed evidence is retained under ignored
`results/project_colab.executed.ipynb`; figures appear in the small notebook
when its cells run.

The first source-suite run had 530 passes and one outdated assertion expecting
the removed diagnostic display figure. The expected count was updated from
five static display figures to the four retained WP04/WP05 images; all six
Colab-export regressions then passed. The final full source suite subsequently
passed **531 tests in 108.49 seconds**. Lint, formatting and ownership checks
pass. Markdown syntax, unchanged classical cells and
the exact supplied introduction are audited separately. No live browser-memory
benchmark is claimed.

Final minimal archive: `deliverables/mm-allee-final-notebook-eps.zip` —
**483,322 bytes / 18 files**: `project.ipynb` and all **17 EPS figures**.
SHA-256: `421696d55a9feed67cf7723f6eb90d30111eb659d34abb8e0cfd07df4ceee48d`.
The external manifest covers every archived file. The earlier full support
archive remains historical. The public `notebook-eps-v2` release is the refreshed
minimal download; version 1 remains an earlier reproducible snapshot.

All examples are synthetic. Curated long sweeps are recorded evidence, not
silently retrained. Human scientific approvals remain separate. The Overleaf
template is still blank in every report body, including WP03; this integration
does not write or compile a report.
