"""Aggregate final-submission blockers without claiming human/scientific approval."""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def audit(root):
    root = Path(root)
    blockers = []
    required = [
        "report/main.tex",
        "report/main.pdf",
        "report/references.bib",
        "notebooks/project.ipynb",
        "artifacts/manifests/final_environment.txt",
        "artifacts/manifests/final_reproduction.json",
    ]
    for name in required:
        if not (root / name).is_file():
            blockers.append({"kind": "missing_file", "path": name})
    pdf = root / "report/main.pdf"
    if pdf.is_file() and not pdf.read_bytes().startswith(b"%PDF-"):
        blockers.append({"kind": "invalid_pdf", "path": "report/main.pdf"})
    for folder in ("report", "notebooks", "presentation"):
        for path in sorted((root / folder).rglob("*")):
            if path.suffix not in {".tex", ".ipynb", ".md"}:
                continue
            text = path.read_text(encoding="utf-8").replace("\\_", "_")
            if any(word in text for word in ("SCAFFOLD_ONLY", "TODO", "TBD")):
                blockers.append({"kind": "unfinished_content", "path": str(path.relative_to(root))})
    eps = list((root / "artifacts/figures").glob("*.eps"))
    if not eps:
        blockers.append({"kind": "missing_eps", "path": "artifacts/figures"})
    for path in sorted((root / "artifacts/figures").glob("*.png")):
        if not path.with_suffix(".eps").is_file():
            blockers.append({"kind": "missing_eps_partner", "path": str(path.relative_to(root))})
    try:
        roster = json.loads((root / "team.json").read_text())
    except (OSError, json.JSONDecodeError):
        blockers.append({"kind": "invalid_roster", "path": "team.json"})
    else:
        members = roster.get("members", [])
        if len(members) != 5 or {m.get("work_package") for m in members} != {
            f"WP0{i}" for i in range(1, 6)
        }:
            blockers.append({"kind": "incomplete_allocations", "path": "team.json"})
        if any(not m.get("name") or not m.get("github") for m in members):
            blockers.append({"kind": "missing_author_names", "path": "team.json"})
        if not roster.get("presentation_datetime_ist"):
            blockers.append({"kind": "missing_presentation_datetime", "path": "team.json"})
    return {
        "automated_ready": not blockers,
        "blockers": blockers,
        "human_verification_required": [
            "all five scientific sections and disclosures checked",
            "four current human approvals",
            "independent non-author reproduction",
            "all members understand the work",
            "presentation rehearsed and submission timing checked",
        ],
        "scope": "File/readiness audit only; cannot certify scientific correctness or human approval",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit(ROOT)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(
        json.dumps(
            {"automated_ready": result["automated_ready"], "blockers": len(result["blockers"])}
        )
    )
    raise SystemExit(0 if result["automated_ready"] else 1)


if __name__ == "__main__":
    main()
