"""Open a PR with all four non-author teammates requested as reviewers."""

import argparse
import json
import re
import shlex
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def reviewers_for(roster, author):
    members = roster.get("members", [])
    if len(members) != 5:
        raise ValueError("Exactly five members required in team.json")
    handles = [m.get("github") for m in members]
    if any(
        not isinstance(h, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}", h)
        for h in handles
    ):
        raise ValueError("Fill all five actual GitHub handles in team.json first")
    normalised = [h.lower() for h in handles]
    if len(set(normalised)) != 5:
        raise ValueError("Five distinct GitHub accounts required")
    if author.lower() not in normalised:
        raise ValueError("Authenticated author is not in the five-person roster")
    return [h for h in handles if h.lower() != author.lower()]


def capture(args):
    return subprocess.check_output(args, cwd=ROOT, text=True).strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", required=True)
    parser.add_argument("--body-file", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if not args.body_file.is_file():
        parser.error("--body-file must exist; copy and fill the PR template first")
    roster = json.loads((ROOT / "team.json").read_text())
    try:
        # Validate the roster before opening any authenticated GitHub operation.
        first = roster.get("members", [{}])[0].get("github") or ""
        reviewers_for(roster, first)
        author = capture(["gh", "api", "user", "--jq", ".login"])
        reviewers = reviewers_for(roster, author)
        branch = capture(["git", "branch", "--show-current"])
        if not branch or branch == "main":
            raise ValueError(
                "Create and push a task branch first; never open work directly on main"
            )
        repo = roster["repository"]
        info = json.loads(
            capture(["gh", "repo", "view", repo, "--json", "nameWithOwner,isPrivate"])
        )
        if not info["isPrivate"] or info["nameWithOwner"].lower() != repo.lower():
            raise ValueError("Target repository must match team.json and be private")
        command = [
            "gh",
            "pr",
            "create",
            "--repo",
            repo,
            "--base",
            "main",
            "--head",
            branch,
            "--title",
            args.title,
            "--body-file",
            str(args.body_file.resolve()),
            "--assignee",
            author,
            "--reviewer",
            ",".join(reviewers),
        ]
        if args.dry_run:
            print(shlex.join(command))
            return
        subprocess.run(command, cwd=ROOT, check=True)
        print("PR opened; wait for all four human approvals and CI. Do not auto-merge.")
    except (ValueError, FileNotFoundError, subprocess.CalledProcessError) as exc:
        parser.exit(
            1,
            f"PR not completed: {exc}. If GitHub partially created it, inspect before retrying.\n",
        )


if __name__ == "__main__":
    main()
