# Repository administration

Requested owner/repository: `devam2006/mm-allee-harvesting`; visibility **private**. Account identity was checked through the connected GitHub account. Creation and server-side settings are separate from this scaffold; do not claim they are active until verified.

## Bootstrap

After an authenticated private repository is created, push this scaffold as its initial commit. For a locally unpacked copy with no Git metadata:

```bash
git init -b main
git add .
git commit -m "Bootstrap five-member Allee harvesting project"
git remote add origin https://github.com/devam2006/mm-allee-harvesting.git
git push -u origin main
```

If a README was created on GitHub already, clone that repo and copy the scaffold into it; preserve history. Do not force-push over an existing branch. If using GitHub CLI to create from this directory, `gh repo create devam2006/mm-allee-harvesting --private --source . --remote origin --push` is an alternative **after** initialising and committing locally; do not run both flows or create a duplicate repository.

## Four-person review policy

1. Invite the other four verified handles, grant write access, and wait for acceptance. Fill all names/handles in `team.json` without making guesses.
2. In repository Settings -> Branches/rules, protect `main` where the account's private-repository plan supports it. Require a PR, **4 approving reviews**, stale-approval dismissal, resolved conversations, current branches, and the unique `core` and `pinn` checks after they have appeared once. Disable force pushes and deletions; apply protections to administrators where supported. Do not add a bypass for agents.
3. Disable automatic merging for this project workflow; use squash merges and delete merged branches. Never treat a completed CI run as a human approval.
4. All four other group members are requested on each PR by `scripts/open_pr.py`. A numeric four-approval rule alone can count other collaborators; keep the roster exact and manually verify that the required four people approved.
5. If the account cannot enforce private branch protection, record that limitation below and follow the same **manual** four-approval policy. Keep the repo private; changing visibility is not a workaround.

GitHub documents private protected branches on eligible paid plans; this does not prove which plan this account has. See [official branch protection documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches).

`CODEOWNERS` is intentionally not populated with fake handles. It can be added after the roster is known; listing multiple owners does not itself require every owner to approve, so it cannot replace the four-member review rule.

## Actual configuration record

- Private repository created/verified: **verified private** via the connected GitHub API on 19 October 2026: `devam2006/mm-allee-harvesting`. The user created the repository and supplied its exact URL.
- Initial scaffold uploaded/verified: **complete**. Commit `04332ecd913a808929fcb08fa9b2567aeb3e89b3`; all 86 source files match local Git tree `576787bad8bd55fa7f84141728c479d18c6346a3`. Subsequent bootstrap documentation records this verification.
- Roster supplied: `devam2006`, `Prem-Mehta03`, `rohanagrawal28`, `AshChan07`, `RaghavSinghal15`. Devam selected **WP03** on 19 October 2026; the other four choices remain open. See `team.json` for current assignments.
- Collaborator invitations: **sent by the owner**, reported by Devam on 19 October 2026; the group was also notified on WhatsApp. A subsequent connected GitHub API check verified `Prem-Mehta03` and `rohanagrawal28` have **write** access; `AshChan07` and `RaghavSinghal15` still report `none`, so their active access remains pending. The owner `devam2006` has admin access. The plugin exposes no collaborator-invitation action.
- CI completed remotely: **passed**, both `core` and `pinn` on Python 3.11, including full notebook kernel execution. [Verified run](https://github.com/devam2006/mm-allee-harvesting/actions/runs/39220681098).
- Branch protections/rules enabled: **not configured**; GitHub reports `main` as unprotected. The four-person review policy is documented and assisted by the PR helper, not yet enforced server-side.
- Current review gate: **manual four-member approval policy** until the repository owner configures available protections. The actual handles are now recorded; reviewer requests require the other four to have collaborator access.

Only update these with observed evidence/links or clearly attributed owner reports. Remaining task assignments await the group's choices; recording a handle does not give that account repository access.

The user supplied the created repository URL; the connected GitHub API verified its owner and private visibility. Browser sign-in is no longer required. The repository was subsequently renamed to `devam2006/mm-allee-harvesting` (without the trailing hyphen); the stable repository ID is `1425301318`, and all active URLs/configuration now use its canonical name.

## Grant the supplied teammates access

The owner has reported sending invitations to the four non-owner handles listed in `team.json`. Each person needs to accept their invitation; verify write access in GitHub Settings -> Collaborators. This is separate from adding roster metadata and separate from being listed as a Git commit contributor. No collaborator invitations were sent by the agent. After access is active, `scripts/open_pr.py` can request all four other roster members as reviewers even before task selection.
