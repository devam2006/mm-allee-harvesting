# Evolving group deliverables

**Branch:** `integration/final-deliverables-draft`. This is a working draft, not the submission ZIP.

The branch starts from WP03's rechecked and corrected source at `20fbd5b21844a94e81e021d1571fbed0f7b47379` in [PR #4](https://github.com/devam2006/mm-allee-harvesting/pull/4). That PR is still awaiting teammate approvals. Starting a dependent draft does not merge or approve it.

The [WP03 learning guide](https://github.com/devam2006/mm-allee-harvesting/blob/wp03/collapse-analysis/docs/WP03_EXPLAINED.md) lives on the WP03 branch only. The draft branch links to it without copying it.

## Available now

| Material | Entry point | Current content |
|---|---|---|
| Report source | [report/main.tex](report/main.tex) | Shared introduction/objectives, model/scaling summary, implemented WP03 section, labelled gaps for other owners |
| Report preview | [report/draft_report.pdf](report/draft_report.pdf) | Compiled working draft; regenerate after source changes |
| Notebook source | [notebooks/project.ipynb](notebooks/project.ipynb) | Shared overview and all five fragments; WP03 executable, unfinished tasks clearly labelled |
| Notebook overview | [notebooks/frontmatter.md](notebooks/frontmatter.md) | Editable common introduction and completeness map |
| PowerPoint | [presentation/draft_presentation.pptx](presentation/draft_presentation.pptx) | Editable shared setup and WP03 evidence; explicit slots for the remaining analysis |
| Slide preview | [presentation/draft_presentation.pdf](presentation/draft_presentation.pdf) | Matching working draft |
| Slide text/notes | [presentation/draft_slides.md](presentation/draft_slides.md) | What each slide explains and where later contributions belong |
| Source/status ledger | [docs/DRAFT_SOURCES.md](docs/DRAFT_SOURCES.md) | Which results are present and what still needs importing/review |

The deck is partial. It is not a rehearsed 25-minute talk. Use [presentation/outline.md](presentation/outline.md) for the final 25+5 allocation.

## Updating the report and notebook

Each owner continues editing their numbered `.tex` section and notebook fragment in their task PR. The integration branch assembles those sources; do not put a competing implementation into the combined notebook.

After a task PR is reviewed and merged into main:

```bash
git fetch origin
git switch integration/final-deliverables-draft
git merge origin/main
python scripts/assemble_notebook.py
python -m pytest -q
```

Resolve source-section/bibliography conflicts with the relevant owner. Record the imported commit and checks in the source ledger. If an unmerged task is inspected on the draft branch, record its exact commit and pending status instead of claiming it is final.

With the ignored venv active:

```bash
python -m pip install -e ".[dev,notebook]"
python scripts/assemble_notebook.py
jupyter nbconvert --to notebook --execute notebooks/project.ipynb --output project.executed.ipynb --output-dir results
latexmk -pdf -cd report/main.tex
python scripts/build_presentation_data.py
python scripts/check_submission_ready.py --output results/draft-readiness.json
```

Keep the compiled preview current by copying the successfully built `report/main.pdf` to `report/draft_report.pdf`. Keep the matching presentation PDF beside its editable PPTX. The optional `presentation/build_deck.mjs` builder requires the Artifact Tool authoring runtime; it is not a scientific Python dependency. The PPTX itself can be edited directly in PowerPoint or LibreOffice.

The readiness command should still fail while task sections or final metadata are missing. A successfully compiled draft is not ready for submission. Do not bypass the packager or publish a final ZIP from this incomplete branch.

## Before submission

Import the reviewed WP01/WP02/WP04/WP05 sections, reconcile repeated introductions/notation, replace all draft gaps, verify references and actual author names, freeze the combined environment and experiments, rerun the full notebook in a clean kernel, inspect the report/deck, rehearse and record the 25+5 timing. Then run the existing final readiness/package checks and reproduce from the extracted ZIP.

The course PDF requires editable TeX, compiled report PDF, references, original EPS figures and an executable notebook, submitted at least one week before the presentation. It gives 3 marks to the report, 2 to the notebook and 5 to presentation/individual understanding. The group's approved extension slot is 30 minutes including Q&A. The presentation date is still not recorded in `team.json`.
