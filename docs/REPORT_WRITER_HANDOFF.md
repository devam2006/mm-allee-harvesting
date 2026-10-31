# Full report writing handoff for an AI agent

**Latest WP05 evidence:** `docs/WP05_NOTEBOOK_UPDATE.md` records Rohan's clean/noisy
live demonstrations and separate settings. All non-WP05 notebook cells are
unchanged. Distinguish these illustrations from the unchanged frozen 108-fit
benchmark when writing the report. The current minimal release is v3.

**Final notebook update:** Prem/Rohan's supplied notebook has now been reconciled
with the reviewed WP01–WP03 work. Read `docs/FINAL_NOTEBOOK.md` and use the current
PR #5 notebook and source ledger when drafting. The template remains blank in
all report bodies, explicitly including WP03.

## Current request and starting point

Use **PR #5**, branch `integration/final-deliverables-draft`, as the combined
scientific source. The reviewed computational baseline is
`be6126a670a9f49cdf3ec2222e87e4723084bcc7`. Read `AGENTS.md`,
`docs/DRAFT_SOURCES.md` and `docs/CLASSICAL_REFRESH.md` first. Fetch the current
PR head before starting, record the exact head used, and inspect any subsequent
changes against that baseline.

**This handoff provides a blank layout, not a written report.** Devam explicitly
asked to leave every section blank, including WP03. The supplied Overleaf ZIP
was byte-identical to the earlier export (17 files, SHA-256
`26f8ca077601b960b42061705740855121c4205c7ec6d2b7ec85ec0cfc25bf5b`).
`docs/course/overleaf_blank_template.zip` preserves its layout and headings but
has empty bodies for all five packages, abstract, introduction/assumptions,
conclusions and acknowledgements. Its bibliography is empty, and the old WP03
figures have been removed. The source attachment itself is unchanged.

The **next report-writing job**, when invoked, is to write a complete AI-assisted
draft in every section from reviewed evidence. The five members will then edit
their own sections. Do not carry the old WP03 prose into the blank template as
if it were already final. The repository's existing `report/main.tex`, report
sections and old PDF are historical prose sources; they are not the current
complete report or the authoritative Overleaf layout.

Devam has supplied the edited notebook, now reconciled and executed as described
in `docs/FINAL_NOTEBOOK.md`. Use that final WP01–WP05 notebook together with the
saved evidence, and record the actual current PR head used for the report.
The earlier computational baseline above remains provenance. Never invent
missing results or silently describe untested content as verified.

## Layout and editable section split

Start a report-only branch from PR #5. Unpack the blank template into a working
report directory. Preserve this structure in the Overleaf upload ZIP:

```text
main.tex
preamble.tex
abstract.tex
frontmatter.tex
references.bib
sections/
  01_foundations.tex
  02_model_b_history.tex
  03_collapse.tex
  04_forward_pinn.tex
  05_inverse_validation.tex
  conclusions.tex
  acknowledgements.tex
figures/
README.md
```

Keep the supplied **12pt A4 article** style, Latin Modern/T1 fonts, geometry
(22 mm side margins, 24 mm top, 25 mm bottom), mathematics/theorem packages,
booktabs, subcaption, microtype and hyperlinks. Equations, figures and tables
are numbered by section. Keep the main file's input order and `\FloatBarrier`
separators. Use LaTeX's automatic section numbers: WP01 is a package identifier,
not an instruction to force section 1 after the introduction.

| File | Content to write in the future full draft | Human editing owner |
|---|---|---|
| `abstract.tex` | Objective, methods, principal supported results and limitations; write last | Shared, coordinated by Devam |
| `frontmatter.tex` | Motivation, ecological context, objectives, assumptions, models, units and notation | Shared, coordinated by Devam |
| `01_foundations.tex` | Nondimensionalisation, logistic baseline, Model A equilibria, phase signs, fold and root algorithm | Raghav / WP01 |
| `02_model_b_history.tex` | Model B derivation/stability, fair comparison protocols, realised catch, carried harvest history and explicit restocking | Ashwath / WP02 |
| `03_collapse.tex` | Thresholds, basins, extinction quadrature/events, convergence, bottleneck, implemented sensitivity/MSY and limitations | Devam / WP03 |
| `04_forward_pinn.tex` | Forward PINN mathematics, JAX implementation, settings selection, independent solver benchmarks, metrics, seeds and failures | Prem / WP04 |
| `05_inverse_validation.tex` | Identifiability, fixed scaling, noisy observations/splits, ODE baseline, inverse loss/optimisation, recovery and failure analysis | Rohan / WP05; reconcile Prem's shared-engine contribution |
| `conclusions.tex` | A coherent comparison of analytical, numerical, forward and inverse findings; supported limits and future work | Shared, coordinated by Devam |
| `acknowledgements.tex` | Actual contributions, synthetic data/source provenance, AI platforms and their recorded roles | All owners confirm; Devam consolidates |

Use the names/allocations in `team.json`. Keep shared notation and bibliography
in common files, and keep each owner's exposition editable in their own file.
Use unique label prefixes and `\label`, `\ref`, `\eqref` and `\cite`; avoid
hard-coded section/figure numbers. Coordinate shared-file edits after the draft.

## Evidence and writing order

Use the readable `notebooks/project.ipynb` and the five owned fragments under
`notebooks/sections/` for current explanations, and `notebooks/project_colab.ipynb`
for the actual integrated browser entry point. Inspect corresponding `src/`,
`experiments/`, `configs/`, `tests/`, `artifacts/tables/` and
`artifacts/manifests/`. Use the current PR's files, not the older public main
notebook, download ZIP, old compiled report or embedded runtime snapshot as the
latest prose source. Source provenance is in `docs/DRAFT_SOURCES.md`.

Read `docs/SCIENTIFIC_CONTRACT.md`, `docs/INTERFACES.md`,
`docs/CLASSICAL_INTEGRATION.md`, `docs/END_TO_END_INTEGRATION.md`,
`docs/DATA_PROVENANCE.md`, `docs/REFERENCES.md` and `docs/AI_USAGE.md`.
Read the supplied course PDF in `docs/course/` in full. It requires editable TeX,
a compiled PDF, references and EPS figure originals; the report should cover
motivation/objectives, assumptions, mathematical formulation/analysis,
numerical simulations and interpretation. AI use and borrowed material must
be acknowledged. This does not certify human understanding or approvals.

Write each technical section as a connected argument: question and assumptions
-> derivation -> algorithm/numerical procedure -> quantitative evidence ->
interpretation -> limitations. Explain enough that its owner can defend it.
Use readable mathematical reasoning, units and well-captioned figures/tables.
Avoid a repository changelog, raw test logs, unexplained formulas, long source
listings or unsupported claims. The report is a coherent end-to-end account,
not five disconnected notebook summaries. No arbitrary page count is imposed.

For every reported number or performance claim, keep a claim-to-evidence map
in the report branch's README or audit file: source table/row, config, manifest,
commit, method/units and relevant check. Read the CSVs to populate tables;
do not transcribe old rounded prose without verification. Distinguish actual
new runs, recorded historical sweeps and unimplemented proposals. The 531 tests
and fresh 32-cell notebook run support the checks stated in the integration
log; they are not a rerun of every historical PINN training sweep.

## Scientific details that must remain consistent

- Define `N,t,r,K,A,H,h` and `x=N/K, tau=rt, a=A/K, q=H/(rK), e=h/r`.
  H has population/time units; h has inverse-time units. Distinguish the
  logistic, constant-yield A and proportional-effort B equations.
- Use the shared computed thresholds and positive branches. Exact equality to
  the computed critical control denotes the fold; a numerical uncertainty band
  does not create roots above it. Explain semistability from one-sided signs,
  and explicit resolution errors for unrepresentable distinct roots.
- A with positive catch stops at the first zero event. Any absorbing continuation
  means harvest shutdown, not an equilibrium of the original ODE. B from a
  positive start has asymptotic decline, not exact finite extinction. Separate
  a sampled epsilon-crossing from an extinction event. Preserve basin uncertainty.
- Present matched initial catch `H=h*N0` and matched threshold fractions as
  different comparison questions. Use total/mean catch with the full observation
  horizon. Harvest histories carry state; restocking is a declared intervention,
  not spontaneous recovery or a fabricated closed hysteresis loop.
- Keep example parameter sets separate. WP02 uses `r=0.5,K=1000,A=200`;
  the WP03/PINN examples use `r=0.7,K=100,A=20`. Their different dimensional
  thresholds agree after scaling. Do not infer a universal policy-risk ranking.
- In inverse work use fixed external scales, the actual fitted/known parameters
  and split/noise seeds. Explain the proven four-unknown Model B ambiguity;
  distinguish it from poor conditioning with independently known K.
- The final inverse design uses 101 observations over `[0,8]`, split 61/20/20,
  and an independently known exact N0 even in noisy runs. Explain the noise-free
  initial anchor used by both PINN and ODE fitting, and the baseline's declared
  zero padding after candidate extinction.
- The held-out observations are excluded from fitting, but collocation covers
  their time window. Call this physics-supported prediction, not extrapolation
  outside the physics domain. Report RMSE/MAE/relative L2 with near-zero caveats.
- The saved clean PINN table gives A regular 3/3, A near-fold 0/3, A extinction
  1/3, B regular 3/3, B near-fold 3/3, B decline 0/3: 10/18 recover all fitted
  parameters within 5%. B near-fold succeeds despite poor conditioning. Use
  these scoped results and the actual noisy/ODE tables, including failures.
- Legacy `converged` denotes training completion, not numerical optimiser
  convergence. Read `lbfgs_outcome`: all 54 recorded final PINN fits reach the
  iteration limit. Show budgets, failed fits, limited seeds, post-hoc criteria
  and limits. No universal claim that PINNs cannot recover a case is supported.

## Figures, citations and Overleaf output

Copy current EPS originals from `artifacts/figures/` into the report ZIP's
`figures/`; the old template's four WP03 figures have deliberately been removed.
Choose figures that support the argument and explain axes, units, protocols,
seeds and failure cases. Distinguish current figures from explicitly historical
original-settings comparisons. Supply all figure dependencies; use relative
extensionless `\includegraphics{wp...}` paths with `\graphicspath{{figures/}}`.
Preserve original EPS files even when PDF companions are needed for compilation.

Use the supplied `epstopdf` setup for pdfLaTeX. If conversion is unavailable,
provide matching converted PDF companions and verify they match the EPS originals.
Do not claim a successful compile without actually compiling. Do not infer
Overleaf build compatibility merely because notebook figures display.

Populate `references.bib` with verified sources actually cited in the text.
Check bibliographic metadata and method/ecology attribution against primary
papers or authoritative documentation. Cite adapted equations, methods, figures
and data. All present project examples are synthetic, not observations of a
species. Record actual AI platforms and roles from the logs and owner input;
do not invent model identities, citations, empirical validation or human reviews.

When the full draft is written, deliver an **Overleaf-importable source ZIP**
with `main.tex` at its root, all inputs, bibliography and figure dependencies,
plus the actually compiled report PDF. Include a concise README with compiler
settings, exact source commit, figure inventory and owner editing map. Label it
an AI-assisted draft for team editing; do not leave empty technical sections or
`SCAFFOLD_ONLY` filler in that later full draft. Keep the current blank template
clearly separate from the future written draft.

Compile `main.tex` with pdfLaTeX/BibTeX (for example `latexmk -pdf main.tex`),
resolve missing references/citations/figures, and inspect rendered pages for
clipping, table widths, equation breaks, figure quality and float placement.
If using Overleaf, set Main document = `main.tex`, Compiler = pdfLaTeX, then
recompile and inspect/download the PDF. Keep the source ZIP self-contained;
no `../artifacts` paths, private tokens or absolute workstation paths.

Check the report against the final integrated notebook and its evidence. The
notebook/EPS ZIP is described in `docs/FINAL_NOTEBOOK.md`. This handoff does not
write or approve the report, update Overleaf live, or merge any source PR.
