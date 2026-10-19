# Course requirements and project decisions

Source: [provided Mathematical Modelling instructions, pages 1–2](course/Mathematical_Modeling_project_instructions.pdf). This checklist transcribes the requirements; the PDF remains authoritative.

| Requirement | Evidence/owner |
|---|---|
| Group of five; distinct approved topic | `team.json`; approved topic supplied by the group |
| Editable `.tex`, compiled PDF, references, EPS figures (3 marks) | `report/main.tex`, `report/sections/`, `report/references.bib`, curated `artifacts/figures/*.eps`; WP01 owner assembles |
| Introduction, motivation, objectives, assumptions, formulation, diagrams, analysis, numerical simulations, graphs and interpretation | Five report sections plus WP01 owner's introduction/conclusion |
| Executable `.ipynb` with detailed colourful Markdown, equations and algorithms before each code section, labelled plots and interpretations (2 marks) | `notebooks/project.ipynb`; WP05 owner assembles, everyone writes one fragment |
| Present motivation, model, reasoning, implementation, results, limitations; each member answers on own contribution (5 marks) | `presentation/outline.md`; WP02 owner assembles, all five rehearse |
| PDF usual slot 10 min talk + 5 min questions | **Project exception confirmed by the user, 19 Oct 2026:** extensions receive 30 minutes including Q&A; plan 25+5, 5 speaking minutes per member |
| AI allowed; students explain every submitted equation/method/algorithm/code component | Human review and explanation checklist in each work package |
| Acknowledge AI platforms and roles; cite data/results/figures/adapted material | `docs/AI_USAGE.md`, `docs/DATA_PROVENANCE.md`, bibliography; each member contributes |
| Dishonest resource or AI acknowledgment can incur a 10-mark penalty | Record actual use contemporaneously; no invented disclosures |
| Advanced component up to 5 bonus marks | WP04/WP05 methods, independent RK45 reference, held-out tests, quantitative errors, comparison graphs and limitations |
| Topic, date and time finalized with professor on/before 19 October 2026 | Topic approved per user; slot still must be recorded by team |
| All presentations before 14 November 2026 | Use the agreed course slot; do not assume 14 November itself is allowed |
| Submit source, figures, PDF and notebook at least one week before scheduled presentation | WP03 owner checks timestamp and complete bundle |

The course prioritises understanding over cosmetic complexity. The approved group plan keeps PINNs in scope, but never sacrifice the classical analysis or the submission requirements for a larger neural network.

No external data are required for this synthetic benchmark design. If observational data are added later, get a focused scope decision, cite provenance/licensing and explain units/calibration separately.
