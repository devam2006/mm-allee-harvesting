"""Bundle final hand-in artifacts; deliberately refuses the unfinished scaffold."""

import hashlib
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]


def main():
    required = [
        "report/main.tex",
        "report/main.pdf",
        "report/references.bib",
        "notebooks/project.ipynb",
    ]
    missing = [name for name in required if not (ROOT / name).is_file()]
    if missing:
        raise SystemExit("Not ready: missing " + ", ".join(missing))
    if not (ROOT / "report/main.pdf").read_bytes().startswith(b"%PDF-"):
        raise SystemExit("Not ready: report/main.pdf is not a PDF")
    figures = list((ROOT / "artifacts/figures").glob("*.eps"))
    if not figures:
        raise SystemExit("Not ready: final EPS figures are required")
    for png in (ROOT / "artifacts/figures").glob("*.png"):
        if not png.with_suffix(".eps").exists():
            raise SystemExit(f"Missing EPS partner: {png.name}")
    for directory in (ROOT / "report", ROOT / "notebooks", ROOT / "presentation"):
        for path in directory.rglob("*"):
            if path.suffix in {".tex", ".ipynb", ".md"}:
                text = path.read_text().replace("\\_", "_")
                if any(marker in text for marker in ("SCAFFOLD_ONLY", "TODO", "TBD")):
                    raise SystemExit(
                        f"Not ready: unresolved scaffold marker in {path.relative_to(ROOT)}"
                    )
    roster = json.loads((ROOT / "team.json").read_text())
    members = roster.get("members", [])
    choices = {m.get("work_package") for m in members}
    if len(members) != 5 or choices != {f"WP0{i}" for i in range(1, 6)}:
        raise SystemExit("Fill exactly one chosen task per member in team.json before submission")
    if any(not m.get("name") or not m.get("github") for m in members):
        raise SystemExit("Fill the actual member names and handles before submission")
    if not roster.get("presentation_datetime_ist"):
        raise SystemExit("Record the agreed presentation date/time before submission")
    roots = [
        "src",
        "scripts",
        "configs",
        "experiments",
        "tests",
        "docs",
        "report",
        "notebooks",
        "artifacts",
        "presentation",
        "data/fixtures",
    ]
    files = {
        ROOT / name
        for name in [
            "README.md",
            "STATUS.md",
            "CONTRIBUTING.md",
            "AGENTS.md",
            "team.json",
            "pyproject.toml",
            "requirements.txt",
            "requirements-dev.txt",
            "requirements-pinn.txt",
        ]
    }
    allowed = {
        ".py",
        ".json",
        ".csv",
        ".md",
        ".tex",
        ".bib",
        ".pdf",
        ".eps",
        ".png",
        ".ipynb",
        ".txt",
        ".toml",
    }
    for name in roots:
        for path in (ROOT / name).rglob("*"):
            if (
                path.is_file()
                and path.suffix in allowed
                and not any(part in {"__pycache__", ".ipynb_checkpoints"} for part in path.parts)
            ):
                files.add(path)
    target = ROOT / "submission/mm-allee-submission.zip"
    target.parent.mkdir(exist_ok=True)
    checksums = {}
    with ZipFile(target, "w", ZIP_DEFLATED) as archive:
        for path in sorted(files):
            relative = str(path.relative_to(ROOT))
            archive.write(path, relative)
            checksums[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
        archive.writestr("SHA256SUMS.json", json.dumps(checksums, indent=2) + "\n")
    print(f"Bundled {len(files)} files: {target}")
    print(
        "Inspect and reproduce extracted contents; this check does not certify scientific completeness."
    )


if __name__ == "__main__":
    main()
