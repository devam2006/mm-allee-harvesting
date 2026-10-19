"""Render task ownership from team.json; --check detects stale documentation."""

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = {
    "WP01": {
        "title": "Foundations and Model A",
        "brief": "WP01_foundations.md",
        "question": "Find the steady population levels under a fixed catch and check their stability",
        "duty": "Report assembly and EPS audit",
        "talk": "Motivation, assumptions, logistic baseline, scaling and Model A",
    },
    "WP02": {
        "title": "Model B and history",
        "brief": "WP02_model_b.md",
        "question": "Compare catch policies and show why reducing harvest may not undo collapse",
        "duty": "Presentation assembly and timing",
        "talk": "Model B, fair comparisons, harvesting history and restocking",
    },
    "WP03": {
        "title": "Collapse and numerical references",
        "brief": "WP03_collapse.md",
        "question": "Calculate when collapse occurs, which starts survive and extinction time",
        "duty": "Independent reproduction and submission bundle",
        "talk": "Thresholds, finite-time extinction, basins and reference generation",
    },
    "WP04": {
        "title": "Forward PINNs",
        "brief": "WP04_forward_pinn.md",
        "question": "Train a network to solve the known equations and compare it with a solver",
        "duty": "Shared neural engine and forward benchmark",
        "talk": "PINN construction, forward results, errors, runtime and a difficult case",
    },
    "WP05": {
        "title": "Inverse PINNs",
        "brief": "WP05_inverse_pinn.md",
        "question": "Estimate unknown parameters from noisy observations and test what is learnable",
        "duty": "Notebook assembly and acknowledgement audit",
        "talk": "Inverse identifiability, noise, held-out validation, failures and conclusions",
    },
}


def validate_roster(roster):
    """An unassigned task is allowed; duplicate accounts/claims are not."""
    members = roster.get("members", [])
    if len(members) != 5:
        raise ValueError("team.json must contain exactly five members")
    handles, ids, owners = set(), set(), {}
    for member in members:
        handle = member.get("github")
        if not isinstance(handle, str) or not re.fullmatch(
            r"[A-Za-z0-9][A-Za-z0-9-]{0,38}", handle
        ):
            raise ValueError("Each member needs an actual GitHub handle")
        if handle.lower() in handles:
            raise ValueError("Duplicate GitHub handle")
        handles.add(handle.lower())
        member_id = member.get("id")
        if not isinstance(member_id, str) or not member_id or member_id in ids:
            raise ValueError("Each member needs a distinct nonempty id")
        ids.add(member_id)
        task = member.get("work_package")
        if task is None:
            continue
        if not isinstance(task, str) or task not in TASKS:
            raise ValueError(f"Unknown work_package: {task!r}; use WP01 through WP05 or null")
        if task in owners:
            raise ValueError(f"Two members selected {task}")
        owners[task] = handle
    return owners


def owner_label(owners, task):
    return "@" + owners[task] if task in owners else "Unclaimed"


def replace_block(text, name, body):
    start = f"<!-- team-sync:{name}:start -->"
    end = f"<!-- team-sync:{name}:end -->"
    if text.count(start) != 1 or text.count(end) != 1:
        raise ValueError(f"Expected one matching {name} ownership block")
    before, rest = text.split(start, 1)
    _, after = rest.split(end, 1)
    return before + start + "\n" + body.rstrip() + "\n" + end + after


def status_rows(text, owners):
    """Preserve human-written scientific progress and evidence while changing owners."""
    progress = {}
    for line in text.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) >= 4 and cells[0] in TASKS:
            progress[cells[0]] = (cells[2], " | ".join(cells[3:]))
    rows = ["| Package | Owner | State | PR/evidence |", "|---|---|---|---|"]
    for task in TASKS:
        state, evidence = progress.get(task, ("Not started", "Add verified evidence/PR"))
        rows.append(f"| {task} | {owner_label(owners, task)} | {state} | {evidence} |")
    return "\n".join(rows)


def render_updates(root, roster):
    """Validate every target before the caller writes anything."""
    owners = validate_roster(roster)
    readme = root / "README.md"
    board = root / "docs/tasks/README.md"
    status = root / "STATUS.md"
    presentation = root / "presentation/outline.md"
    updates = {}
    people = ", ".join("@" + member["github"] for member in roster["members"])
    rows = [f"**Contributors:** {people}", "", "| Task | Owner |", "|---|---|"]
    for task, info in TASKS.items():
        rows.append(
            f"| [{task}: {info['title']}](docs/tasks/{info['brief']}) | {owner_label(owners, task)} |"
        )
    updates[readme] = replace_block(readme.read_text(), "owners", "\n".join(rows))
    rows = ["| Task | In plain language | Shared duty | Claimed by |", "|---|---|---|---|"]
    for task, info in TASKS.items():
        rows.append(
            f"| [{task}: {info['title']}]({info['brief']}) | {info['question']} | {info['duty']} | {owner_label(owners, task)} |"
        )
    updates[board] = replace_block(board.read_text(), "board", "\n".join(rows))
    updates[status] = replace_block(
        status.read_text(), "status", status_rows(status.read_text(), owners)
    )
    rows = ["| Time | Speaker | Story and evidence |", "|---|---|---|"]
    for index, (task, info) in enumerate(TASKS.items()):
        speaker = owner_label(owners, task)
        rows.append(f"| {5 * index}–{5 * (index + 1)} min | {speaker} ({task}) | {info['talk']} |")
    rows.append("| 25–30 min | All five | Questions and individual understanding |")
    updates[presentation] = replace_block(presentation.read_text(), "presentation", "\n".join(rows))
    for task, info in TASKS.items():
        path = root / "docs/tasks" / info["brief"]
        updates[path] = replace_block(
            path.read_text(),
            "owner",
            f"**Owner:** {owner_label(owners, task)}. See [team.json](../../team.json) for the current choice.",
        )
    return updates


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true", help="Fail if generated ownership text is stale"
    )
    args = parser.parse_args()
    try:
        roster = json.loads((ROOT / "team.json").read_text())
        updates = render_updates(ROOT, roster)
        changed = [path for path, text in updates.items() if path.read_text() != text]
        if args.check and changed:
            parser.exit(
                1,
                "Ownership docs are stale; run python scripts/sync_team.py:\n"
                + "\n".join(str(path.relative_to(ROOT)) for path in changed)
                + "\n",
            )
        if not args.check:
            for path in changed:
                path.write_text(updates[path])
        print(
            f"Ownership docs {'current' if args.check else 'synchronised'} ({len(changed)} changes)"
        )
    except (ValueError, OSError) as exc:
        parser.exit(1, f"Cannot synchronise ownership: {exc}\n")


if __name__ == "__main__":
    main()
