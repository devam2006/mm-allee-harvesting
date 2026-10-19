# Integration and final submission

## Schedule

Presentation slot: **30 minutes including Q&A confirmed by the user on 19 October 2026**. Plan 25 min talk + 5 min Q&A, about 5 min speaking per member. Date/time: **not supplied**; record it in `team.json` and here. Course PDF deadlines remain unchanged: submission at least one week before the chosen slot; all presentations before 14 November 2026.

Let D be the actual presentation date/time (IST). These are internal targets, not invented course deadlines:

| Target | Work |
|---|---|
| Immediately | Assign members, confirm D with professor, accept collaborator invitations, freeze conventions |
| D-14 days or earlier | WP01/WP03 foundation APIs and first numerical fixture; WP04 first shared engine; WP05 split/baseline design |
| D-11 | Core analysis/experiments and each report/notebook section in review |
| D-10 | Scientific/configuration freeze; all core PRs merged after four reviews |
| D-9 | Assemble report/notebook/slides; independent reproduction |
| D-8 | Fix integration issues, compile/inspect, rehearse, package and audit |
| **D-7 or earlier** | **Submit required source/figures/PDF/notebook to professor** |
| After submission to D | Rehearse understanding and Q&A; do not silently change reported results |

If the selected slot makes these targets impossible, compress internal milestones together and drop extras first; the one-week course submission rule still applies. Do not invent a booked slot from the date range.

## Dependency and merge order

1. **WP01 + WP03 foundation PRs:** common units/RHS/root records, solver boundary policy, threshold conventions and reference-data schema. Small verified pieces merge first.
2. **WP02/WP03 analysis PRs:** B branches, history, collapse/quadrature/basins, early synthetic fixtures. Classical analysis is a useful standalone milestone.
3. **WP04 engine PR:** differentiable shared residual/network and short A/B runs; WP05 reviews extension hooks. WP05 can already build identifiability checks, observation splits and conventional fit in parallel.
4. **WP04/WP05 evidence PRs:** frozen configs, seed-level metrics, failure cases and curated PNG/EPS figures. Both use WP03's references and one data schema.
5. **Integration PRs:** WP01 owner assembles LaTeX; WP05 owner assembles the notebook; WP02 owner assembles slides. Each integration PR still needs all other four reviews. WP03 owner reruns and packages only after these integrate.

Different members can open independent PRs simultaneously. Avoid one giant last-day PR that combines five incompatible APIs. Each PR includes its report/notebook updates so explanations do not fall behind code.

## Shared handoff from every member

Provide a module/test list; exact command/config; small curated figures **PNG and EPS**; raw numerical tables behind the figures; manifests; one `.tex` section; one notebook fragment; 2–3 slide contributions plus a five-minute speaker script; verified references and an AI-use entry; unfinished extras/limitations. A teammate reproduces the command and checks the conclusion.

## One coherent notebook

Fragments live at `notebooks/sections/01_...ipynb` through `05_...ipynb`; avoid editing the assembled notebook independently. Run:

```bash
python scripts/assemble_notebook.py
jupyter nbconvert --to notebook --execute notebooks/project.ipynb --output project.executed.ipynb --output-dir results
```

WP05 owner checks section order, equations/algorithm Markdown before code, accessible colours, labelled axes, interpretations and a final limitations/disclosure cell. Code calls shared modules and reproducible configs. Choose a short but genuine A/B forward and inverse smoke budget for notebook execution; provide commands/manifests for longer sweeps. If loading curated final outputs, explain and supply their regeneration command—do not imply the notebook retrained them.

## One coherent report

WP01 owner assembles `report/main.tex` and all sections with one bibliography and consistent notation. Include objective/assumption/model summary; classical derivations and signs; numerical algorithms and convergence; PINN forward/inverse math and honest evidence; conclusions/limitations; contribution/data/AI acknowledgements. Every result must trace to a curated table/figure/config. Keep EPS originals and use PDF/PNG or deliberate conversion for PDFLaTeX.

```bash
latexmk -pdf -cd report/main.tex
```

Visually inspect the final compiled PDF, equations, captions, references and page layout. No claim that starter LaTeX compilation means the scientific report is complete.

## Final submission checklist (WP03 owner audits)

- [ ] All five core work packages reproduced; optional work labelled complete or omitted.
- [ ] Editable `report/main.tex` plus every included `.tex` section and `.bib` reference file.
- [ ] Compiled final `report/main.pdf`, visually checked, no missing references/figures.
- [ ] Original `.eps` for every generated reported figure, plus PNG/PDF display variants as needed.
- [ ] Single final executable `.ipynb`, clean-kernel execution log and environment instructions.
- [ ] All imported Python modules, experiment scripts/configs, curated tables/figures/manifests and any small required fixtures.
- [ ] Actual dependency snapshot and reproduction commands; no personal absolute paths/secrets/bulk weights.
- [ ] Explicit synthetic labels, split/noise protocol, inverse identifiability caveat and failure disclosure.
- [ ] Complete real AI/platform roles and source/data/figure citations; five named contribution statements.
- [ ] Presentation editable source, PDF, timed 25+5 outline and rehearsed Q&A; include alongside mandatory files for convenience.
- [ ] Four-person reviews/checks complete; final commit recorded; no `TODO`, `TBD` or `SCAFFOLD_ONLY` placeholders in report/notebook/slides.
- [ ] Submission sent at least one week before D; team records actual submission time/receipt themselves.

After final files exist:

```bash
python scripts/package_submission.py
```

The script creates a self-contained zip under ignored `submission/`, requires the mandatory report/notebook/EPS artifacts, and rejects obvious unfinished content. It cannot decide whether your scientific reasoning or bibliography is correct. Inspect the zip and rerun the included instructions from its extracted contents before submission.
