# Team workflow

## One-time setup

Repository owner adds all four other GitHub accounts as collaborators with write access. Each person accepts before working. Fill exactly five distinct handles in `team.json`; let each person choose one of the five unclaimed work packages and record it. Member IDs are placeholders, not GitHub usernames. Set up your own Git credentials; never commit tokens or reuse someone else's login.

## Branch -> pull request -> four reviewers -> merge

```bash
git switch main
git pull --ff-only origin main
git switch -c wp01/model-a-equilibria
# edit, run your tests and update report/notebook/AI log
python -m pytest -q
ruff check .
ruff format --check .
python scripts/assemble_notebook.py
git status --short
git add src tests docs report notebooks configs experiments artifacts
git diff --cached
git commit -m "WP01: derive and verify Model A equilibria"
git push -u origin wp01/model-a-equilibria
python scripts/open_pr.py --title "WP01: Model A equilibria" --body-file pr-body.md
```

Create a local `pr-body.md` from `.github/pull_request_template.md` (it is ignored). `open_pr.py` uses the GitHub CLI (`gh`), validates the complete roster and current author, opens a PR against `main`, assigns the author, and requests all other **four** members as reviewers. Use `--dry-run` to inspect its command. Authenticate `gh` locally if needed.

Without `gh`: GitHub -> Compare & pull request -> base `main`; paste the template, assign yourself in **Assignees**, and add all other four accounts in **Reviewers**. Assignees and reviewers are different fields. Mark a PR as Draft while unfinished; request final reviews when ready. Do not review from the author's account.

Every reviewer checks the equations, interpretation, changed code and tests. At least one reviewer reruns the documented command; all four use GitHub's **Approve** after they are satisfied. An AI review can assist but does not replace a person's review. Authors answer comments and obtain fresh approval after substantive changes.

**Merge policy:** all four non-author members approve the latest changes, required CI passes, conversations are resolved, and the branch contains current main. A non-author human performs squash merge and deletes the branch. Agents never merge their own PR. Do not bypass failed checks or count a comment as approval. For a five-person roster this means four distinct approvals; a new extra collaborator does not replace a missing teammate's approval.

The initial bootstrap commit may seed an empty repository. After that, use PRs for every change, including documentation and integration. Record actual branch-protection configuration in `docs/REPOSITORY_ADMIN.md`; files alone do not enable it. If private-repository protections are unavailable on the account's plan, the **same manual four-review policy still applies** and the owner merges only after checking it.

## Avoiding conflicts

- One branch per small deliverable, named `wpNN/short-purpose`, `fix/short-purpose` or `integration/short-purpose`.
- Edit only your owned report section and notebook fragment. The named assembler edits `report/main.tex`, `notebooks/project.ipynb` or shared slides in a separate integration PR.
- All packages depend on a small shared API. Agree interface changes before implementation and update `docs/INTERFACES.md` plus consumers in one reviewed PR.
- Merge dependencies first. For dependent work either wait for main or declare a stacked PR and retarget after the dependency merges. Do not silently copy unmerged code.
- Update your branch with `git fetch origin` then `git merge origin/main`; resolve conflicts and rerun tests. Avoid rewriting a branch already under review.
- Never commit `.venv`, generated bulk data, model weights, local credentials or executed notebook noise. Curated results need manifests and small reviewed files.

## Definition of done for each package

- Core acceptance items implemented and tested; still-pending extras named explicitly.
- Reproduction command and config produce the promised figures/table on a CPU, or document the measured hardware requirement honestly.
- Every figure has axis labels, units, model, parameters, legend and interpretation; report exports include EPS.
- Report and notebook explain equations and algorithms **before** code/results. No fabricated outcomes or unresolved template placeholders in the submission.
- AI-use/provenance/reference records updated; human owner can explain the method and its limitations.
- Four reviews and passing checks; another member reproduces the evidence and updates STATUS.md.
