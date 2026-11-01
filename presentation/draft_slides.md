# Working slide draft

This is the text/notes map for the editable PPTX and matching PDF. It contains available WP03 evidence and labelled places for incoming work. It is not the final talk or a rehearsal record.

| Slide | Content | What still changes |
|---|---|---|
| 1 | Project title and five GitHub handles | Confirm actual author names and presentation date |
| 2 | A/B equations, scaling and assumptions | Reconcile with WP01's introduction |
| 3 | Foundations/comparison/history slots | Replace with reviewed WP01/WP02 diagrams and interpretation |
| 4 | WP03 threshold table with units | Keep tied to source config/table |
| 5 | Editable A/B positive branches and basin interpretation | Keep fold semistability and zero-boundary caveats in explanation |
| 6 | Extinction integral, RK45 event policy and six independent event checks | Keep data tied to the event-validation table |
| 7 | Forward/inverse evidence slots | Replace with measured WP04/WP05 graphs, metrics and failures |
| 8 | Supported classical conclusions and current limits | Extend after PINN/policy evidence arrives |
| 9 | Q&A | Keep five minutes free in the final slot |

The native chart/table data come from `presentation/data/draft_results.json`, regenerated with `python scripts/build_presentation_data.py`. Speaker notes identify exact source tables, definitions and limitations. The report's original PNG/EPS figures remain versioned under `artifacts/figures/`.

The native chart workbooks use 12 significant digits for Excel portability. The scientific JSON and original tables retain their full precision. Rendering the two event-time series as overlapping bars does not display their tiny disagreement; the event table retains the quantitative errors.

The partial deck's slide count does not set the final count. Split the combined pending slots into the members' 2–3 slide contributions as work arrives. Preserve the five equal speaking blocks in `presentation/outline.md`; WP03's populated contribution should fit its five-minute allocation. Move optional sensitivity/MSY/bottleneck detail to backup slides if needed.

You can edit the PPTX directly. `build_deck.mjs` is an optional source for agents with the Artifact Tool authoring runtime and requires its module/font/validation setup. It is not part of the project's Python installation. Updating slide source/data and rebuilding the PPTX/PDF is preferable to changing a reported number manually.
