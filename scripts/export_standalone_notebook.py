"""Embed the exact source/config/data snapshot in a single executable notebook."""

import argparse
import base64
import hashlib
import io
import json
import mimetypes
import re
import subprocess
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import nbformat
from assemble_notebook import ROOT, build_notebook


def export_notebook(packages, target):
    nb = build_notebook(packages)
    sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    dirty = bool(
        subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True).strip()
    )
    selected = set()
    for pattern in ["src/**/*.py", "pyproject.toml", "data/fixtures/**/*", "docs/AI_USAGE.md"]:
        selected.update(
            p for p in ROOT.glob(pattern) if p.is_file() and "__pycache__" not in p.parts
        )
    for index in packages:
        wp = f"wp{index:02d}"
        for pattern in [
            f"configs/{wp}*.json",
            f"experiments/{wp}/*.py",
            f"artifacts/figures/{wp}_*",
            f"artifacts/tables/{wp}_*",
            f"artifacts/manifests/{wp}*",
        ]:
            selected.update(p for p in ROOT.glob(pattern) if p.is_file())
    if 4 in packages or 5 in packages:
        for pattern in [
            "artifacts/tables/shared_*.csv",
            "configs/shared_*.json",
            "experiments/integration/*.py",
        ]:
            selected.update(p for p in ROOT.glob(pattern) if p.is_file())
    snapshot = {
        "source_commit": sha,
        "source_dirty": dirty,
        "work_packages": packages,
        "data": "synthetic",
        "file_sha256": {
            p.relative_to(ROOT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(selected)
        },
    }
    stream = io.BytesIO()
    with ZipFile(stream, "w", ZIP_DEFLATED) as archive:
        for path in sorted(selected):
            archive.writestr(path.relative_to(ROOT).as_posix(), path.read_bytes())
        archive.writestr("SOURCE_SNAPSHOT.json", json.dumps(snapshot, indent=2))
    payload = stream.getvalue()
    digest = hashlib.sha256(payload).hexdigest()
    bootstrap = """# Restore the source and synthetic evidence embedded in this notebook.
import base64
import hashlib
import io
import os
import sys
import tempfile
from pathlib import Path
from zipfile import ZipFile

_payload = base64.b64decode(PAYLOAD)
assert hashlib.sha256(_payload).hexdigest() == DIGEST
ROOT = Path(tempfile.mkdtemp(prefix="mm-allee-notebook-"))
with ZipFile(io.BytesIO(_payload)) as _archive:
    for _entry in _archive.infolist():
        _path = (ROOT / _entry.filename).resolve()
        if not _path.is_relative_to(ROOT.resolve()):
            raise RuntimeError("Invalid embedded file path")
        _path.parent.mkdir(parents=True, exist_ok=True)
        _path.write_bytes(_archive.read(_entry))
sys.path.insert(0, str(ROOT / "src"))
os.environ["PYTHONPATH"] = str(ROOT / "src")
os.chdir(ROOT)
try:
    get_ipython().run_line_magic("matplotlib", "inline")
except NameError:
    import matplotlib
    matplotlib.use("Agg")
print("Restored bundled source and synthetic data:", ROOT)
""".replace("PAYLOAD", repr(base64.b64encode(payload).decode())).replace("DIGEST", repr(digest))
    bootstrap = subprocess.run(
        [sys.executable, "-m", "ruff", "format", "--stdin-filename", "bootstrap.py", "-"],
        input=bootstrap,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.rstrip()
    intro = nbformat.v4.new_markdown_cell(
        "# Harvesting under a strong Allee effect\n\n"
        "<div style='border-left:5px solid #176b87;padding:12px;background:#176b8710'><b>Portable notebook</b><br>"
        "This file contains its Python source, configurations, synthetic datasets and recorded evidence. "
        "Run all cells from the top in a fresh kernel. No repository checkout or data download is needed.</div>\n\n"
        "**Environment:** Python 3.11 or newer; install `numpy scipy matplotlib nbformat ipython`"
        + (" and `jax` (CPU)" if 4 in packages or 5 in packages else "")
        + ". The bootstrap restores the included source into a temporary directory. "
        "The readable source files are also included in the companion download.\n\n"
        "**Scope:** " + ", ".join(f"WP{i:02d}" for i in packages) + ". "
        "All population examples are synthetic. A short demonstrator is distinct from recorded final experiments. "
        "Explanations, equations and algorithms precede the corresponding code; interpretations and limitations follow.\n\n"
        "**Execution budget:** classical experiments are bounded by their saved configs. "
        "PINN demonstrations use the stated notebook settings; the full historical parameter sweeps are read from tables, not silently retrained."
    )
    intro["id"] = "portable-introduction"
    setup = nbformat.v4.new_code_cell(bootstrap)
    setup["id"] = "portable-source-bootstrap"
    setup.metadata["jupyter"] = {"source_hidden": True}
    nb.cells = [intro, setup, *nb.cells[1:]]
    for cell in nb.cells:
        if cell.cell_type != "markdown":
            continue
        for match in list(re.finditer(r"!\[([^]]*)\]\(([^)]+)\)", cell.source)):
            source = (ROOT / "notebooks" / match.group(2)).resolve()
            if not source.is_relative_to(ROOT.resolve()) or not source.is_file():
                continue
            mime = mimetypes.guess_type(source.name)[0]
            if mime not in {"image/png", "image/jpeg", "image/svg+xml"}:
                continue
            key = source.name
            cell.setdefault("attachments", {})[key] = {
                mime: base64.b64encode(source.read_bytes()).decode()
            }
            cell.source = cell.source.replace(
                match.group(0), f"![{match.group(1)}](attachment:{key})"
            )
    nb.metadata["source_snapshot"] = {k: v for k, v in snapshot.items() if k != "file_sha256"}
    nb.metadata["payload_sha256"] = digest
    nbformat.validate(nb)
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    # Hash the same LF bytes Git stores on every platform, including Windows.
    target.write_text(nbformat.writes(nb).rstrip("\n") + "\n", encoding="utf-8", newline="\n")
    manifest = target.with_suffix(".manifest.json")
    manifest.write_text(
        json.dumps(
            {
                **snapshot,
                "payload_sha256": digest,
                "notebook_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Exported {target}: {len(selected)} embedded files, {len(payload)} compressed bytes")
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packages", type=int, nargs="+", choices=range(1, 6), default=[1, 2, 3])
    parser.add_argument(
        "--output", type=Path, default=ROOT / "notebooks/wp01_wp03_standalone.ipynb"
    )
    args = parser.parse_args()
    export_notebook(args.packages, args.output)


if __name__ == "__main__":
    main()
