"""Publish selected runtime artifacts and a small, version-pinned Colab notebook."""

import argparse
import hashlib
import io
import json
import re
import shutil
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

import nbformat
from assemble_notebook import ROOT, build_notebook

PUBLIC_REPOSITORY = "devam2006/mm-allee-notebook-runtime"
MANIFEST = ROOT / "artifacts/notebook_runtime/manifest.json"
IMAGE_PATTERN = re.compile(r"!\[([^]]*)\]\(([^)]+)\)")


def markdown_images(notebook):
    images = set()
    for cell in notebook.cells:
        if cell.cell_type == "markdown":
            for match in IMAGE_PATTERN.finditer(cell.source):
                path = (ROOT / "notebooks" / match[2]).resolve()
                if path.is_relative_to(ROOT.resolve()) and path.is_file():
                    images.add(path)
    return images


def build_assets(public_dir):
    """Export selected public artifacts; never copy Git history/private review notes."""
    public_dir = Path(public_dir)
    public_dir.mkdir(parents=True, exist_ok=True)
    selected = set()
    for pattern in [
        "src/**/*.py",
        "pyproject.toml",
        "data/fixtures/**/*",
        "configs/wp*.json",
        "configs/shared_*.json",
        "experiments/wp*/*.py",
        "experiments/integration/*.py",
        "artifacts/tables/wp*",
        "artifacts/tables/shared_*.csv",
        "artifacts/manifests/wp*",
    ]:
        selected.update(
            path
            for path in ROOT.glob(pattern)
            if path.is_file() and "__pycache__" not in path.parts
        )
    images = markdown_images(build_notebook())
    selected.update(images)
    files = {path.relative_to(ROOT).as_posix(): path.read_bytes() for path in sorted(selected)}
    snapshot = {
        "source_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        "source_dirty": bool(
            subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True).strip()
        ),
        "work_packages": [f"WP{i:02d}" for i in range(1, 6)],
        "data": "synthetic",
        "file_sha256": {name: hashlib.sha256(data).hexdigest() for name, data in files.items()},
        "scope": "Selected runtime source, configs, synthetic fixtures, tables and five display figures",
    }
    files["SOURCE_SNAPSHOT.json"] = (json.dumps(snapshot, indent=2) + "\n").encode()
    stream = io.BytesIO()
    with ZipFile(stream, "w", compression=ZIP_DEFLATED) as archive:
        for name, data in sorted(files.items()):
            entry = ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.compress_type = ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, data)
    payload = stream.getvalue()
    digest = hashlib.sha256(payload).hexdigest()
    relative = f"runtime/wp01-wp05-{digest[:16]}.zip"
    target = public_dir / relative
    target.parent.mkdir(exist_ok=True)
    target.write_bytes(payload)
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(target, MANIFEST.parent / target.name)
    manifest = {
        **snapshot,
        "path": relative,
        "sha256": digest,
        "bytes": len(payload),
        "files": len(files),
        "static_figures": len(images),
        "public_repository": PUBLIC_REPOSITORY,
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (public_dir / "runtime/manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    # Readable scientific resources plus all report figures; no private discussion/history.
    for path in selected:
        destination = public_dir / path.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, destination)
    for path in (ROOT / "artifacts/figures").glob("*"):
        if path.suffix in {".png", ".eps", ".pdf"}:
            destination = public_dir / path.relative_to(ROOT)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, destination)
    from package_notebook_delivery import observation_csv

    observations, rows = observation_csv(json.loads((ROOT / "configs/wp05_final.json").read_text()))
    (public_dir / "datasets").mkdir(exist_ok=True)
    (public_dir / "datasets/wp05_observations.csv").write_bytes(observations)
    (public_dir / "datasets/README.md").write_text(
        "# Synthetic observations\n\nThe clean trajectories are in data/fixtures/wp03_reference/. "
        f"wp05_observations.csv contains {rows} reconstructed rows in 54 scenarios using the "
        "versioned noise/split generator and final config. These are synthetic, not field data. "
        "Use (dataset_id, observation_id) as the unique key. population is evaluation truth; "
        "fit only observed_population on train rows. These reconstructed inputs are not claimed "
        "byte-identical to an author's unsaved historical arrays.\n",
        encoding="utf-8",
    )
    shutil.copyfile(ROOT / ".gitattributes", public_dir / ".gitattributes")
    for name in ["REFERENCES.md", "DATA_PROVENANCE.md", "SCIENTIFIC_CONTRACT.md"]:
        (public_dir / "docs").mkdir(exist_ok=True)
        shutil.copyfile(ROOT / "docs" / name, public_dir / "docs" / name)
    (public_dir / "README.md").write_text(
        "# Strong-Allee harvesting: notebook, code and synthetic data\n\n"
        f"[**Open in Google Colab**](https://colab.research.google.com/github/{PUBLIC_REPOSITORY}/blob/main/project.ipynb)\n\n"
        "Connect a CPU runtime and choose **Runtime → Run all**. The small notebook downloads "
        "a fixed, checksum-verified snapshot of its code/data on the first run. No Drive mount, "
        "private repository permission or API key is required. Figures appear as the cells run.\n\n"
        "The notebook covers WP01–WP05: classical equilibria/history/collapse, forward PINNs, "
        "inverse estimation and held-out validation. All population data are synthetic. "
        "Recorded long sweeps are loaded from tables, not retrained by the demonstration.\n\n"
        "## Files\n\n"
        "- `project.ipynb`: small Colab/Jupyter entry point.\n"
        "- `runtime/`: fixed executable snapshot and its manifest.\n"
        "- `src/`, `experiments/`, `configs/`: readable scientific code and settings.\n"
        "- `data/fixtures/wp03_reference/`: six frozen clean trajectories and provenance.\n"
        "- `datasets/`: reconstructed noisy observations with explicit split/noise labels.\n"
        "- `artifacts/figures/`: PNG/EPS figure pairs and available PDFs for the report.\n"
        "- `artifacts/tables/`, `artifacts/manifests/`: recorded experiment evidence.\n\n"
        "Python 3.11+ is required. The setup cell installs only missing standard scientific "
        "dependencies (NumPy, SciPy, Matplotlib, IPython, JAX). Internet is needed on first use; "
        "a downloaded repository copy also includes the local runtime ZIP for offline Jupyter use.\n\n"
        "## Interpretation and attribution\n\n"
        "The inverse trainer's legacy `converged` label denotes completed training; read the "
        "separate L-BFGS outcome. The recorded final sweep has 54 iteration-limit exits; clean "
        "parameter recovery is 10/18. Good trajectory fits do not prove accurate parameters. "
        "This is a computational integration candidate; human review and the final Overleaf "
        "report/presentation remain separate. See NOTICE.md and docs/REFERENCES.md for attribution. "
        "AI tools assisted implementation and review under the members' direction. "
        "The private development history and discussions are not included here.\n",
        encoding="utf-8",
    )
    print(json.dumps({"runtime_bytes": len(payload), "files": len(files), "path": relative}))
    return manifest


def setup_source(manifest, asset_ref):
    if not re.fullmatch(r"[0-9a-f]{40}", asset_ref):
        raise ValueError("Pin an immutable 40-character public asset commit")
    url = f"https://raw.githubusercontent.com/{PUBLIC_REPOSITORY}/{asset_ref}/{manifest['path']}"
    source = """# @title Load the project data and code
import hashlib
import importlib.util
import io
import os
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path
from zipfile import ZipFile

_url = RUNTIME_URL
_expected = EXPECTED_SHA256
_name = BUNDLE_NAME
_cache = Path(tempfile.gettempdir()) / "mm-allee-runtime" / _name
_local_candidates = [Path.cwd() / "runtime" / _name, Path.cwd() / _name, _cache]
for _candidate in _local_candidates:
    if _candidate.is_file():
        _payload = _candidate.read_bytes()
        print("Using downloaded/packaged project data.")
        break
else:
    print("Downloading the fixed public data/code snapshot...")
    with urllib.request.urlopen(_url, timeout=60) as _response:
        _payload = _response.read(10 * 1024 * 1024 + 1)
if len(_payload) > 10 * 1024 * 1024 or hashlib.sha256(_payload).hexdigest() != _expected:
    raise RuntimeError("Project data checksum mismatch. Use a fresh notebook/download package.")
_cache.parent.mkdir(parents=True, exist_ok=True)
_cache.write_bytes(_payload)
ROOT = Path(tempfile.mkdtemp(prefix="mm-allee-notebook-"))
with ZipFile(io.BytesIO(_payload)) as _archive:
    for _entry in _archive.infolist():
        _path = (ROOT / _entry.filename).resolve()
        if not _path.is_relative_to(ROOT.resolve()):
            raise RuntimeError("Invalid project data path")
        _path.parent.mkdir(parents=True, exist_ok=True)
        _path.write_bytes(_archive.read(_entry))
sys.path.insert(0, str(ROOT / "src"))
os.environ["PYTHONPATH"] = str(ROOT / "src")
os.chdir(ROOT)
_missing = [name for name in ["numpy", "scipy", "matplotlib", "IPython", "jax"]
            if importlib.util.find_spec(name) is None]
if _missing:
    print("Installing missing scientific packages:", ", ".join(_missing))
    subprocess.check_call([sys.executable, "-m", "pip", "-q", "install", *_missing])
try:
    get_ipython().run_line_magic("matplotlib", "inline")
except NameError:
    import matplotlib
    matplotlib.use("Agg")
print("Project ready. Run the remaining cells from the top.")
"""
    source = (
        source.replace("RUNTIME_URL", repr(url))
        .replace("EXPECTED_SHA256", repr(manifest["sha256"]))
        .replace("BUNDLE_NAME", repr(Path(manifest["path"]).name))
    )
    return subprocess.run(
        [sys.executable, "-m", "ruff", "format", "--stdin-filename", "setup.py", "-"],
        input=source,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.rstrip()


def export_notebook(manifest, asset_ref, target):
    notebook = build_notebook()
    introduction = nbformat.v4.new_markdown_cell(
        "# Harvesting under a Strong Allee Effect\n\n"
        "**Colab:** connect a CPU runtime, then choose **Runtime → Run all**. "
        "The first cell downloads the required code and synthetic data from a fixed public "
        f"GitHub version ({manifest['bytes'] / 1_000_000:.2f} MB), verifies its checksum and prepares the project. "
        "No Google Drive mount, private-repository access or API key is required.\n\n"
        "The notebook opens without large encoded code cells. Figures and demonstration results "
        "appear when their cells run. Most scientific packages are already available in Colab; "
        "only missing dependencies are installed. **Internet is needed on the first run**, unless "
        "the companion download's runtime ZIP is beside this notebook under `runtime/`.\n\n"
        "**Scope:** WP01–WP05. All examples are synthetic. Equations and algorithms precede code; "
        "interpretations and limitations follow. Historical sweeps are loaded from recorded tables, "
        "not silently retrained. The report is maintained separately in Overleaf.\n\n"
        "**Reproduction:** the public snapshot is pinned to a commit and SHA-256. Keep those values "
        "unchanged to reproduce this version. Python 3.11+ and NumPy/SciPy/Matplotlib/IPython/JAX are required."
    )
    custom_introduction = ROOT / "notebooks/colab_introduction.md"
    if custom_introduction.is_file():
        introduction.source = custom_introduction.read_text(encoding="utf-8")
    introduction.id = "colab-introduction"
    setup = nbformat.v4.new_code_cell(setup_source(manifest, asset_ref))
    setup.id = "colab-project-setup"
    setup.metadata["cellView"] = "form"
    setup.metadata["jupyter"] = {"source_hidden": True}
    cells = [introduction, setup]
    heading = ROOT / "notebooks/colab_setup_heading.md"
    if heading.is_file():
        cell = nbformat.v4.new_markdown_cell(heading.read_text(encoding="utf-8"))
        cell.id = "OHbQMxz-wPYl"
        cells.append(cell)
    for original in notebook.cells[1:]:
        cell = deepcopy(original)
        figures = []
        if cell.cell_type == "markdown":
            for match in list(IMAGE_PATTERN.finditer(cell.source)):
                path = (ROOT / "notebooks" / match[2]).resolve()
                if path.is_relative_to(ROOT.resolve()) and path.is_file():
                    cell.source = cell.source.replace(
                        match[0], f"**Figure:** {match[1]} (run the next cell)."
                    )
                    figures.append(path.relative_to(ROOT).as_posix())
        cells.append(cell)
        for index, figure in enumerate(figures):
            code = "import IPython.display as _figures\n\n" + (
                f"_figures.display(_figures.Image(filename=str(ROOT / {figure!r})))"
            )
            image_cell = nbformat.v4.new_code_cell(code)
            image_cell.id = f"{cell.id}-figure-{index}"
            cells.append(image_cell)
    notebook.cells = cells
    acknowledgements = nbformat.v4.new_markdown_cell(
        "## Reproduction, sources and acknowledgements\n\n"
        "The short demonstrations are executed when this notebook runs; long-study tables "
        "are recorded evidence. The setup fixes the code/data version and checks its integrity.\n\n"
        "**Contributions:** Raghav Singhal (WP01), Ashwath Chandramouli (WP02), "
        "Devam Jatin Bhavsar (WP03), Prem Mehta (WP04), Rohan Agrawal (WP05). "
        "Codex and Claude Code assisted derivation, implementation, experiments, review and "
        "integration under the members' direction. Humans remain responsible for the work; "
        "execution checks do not certify their understanding or approval.\n\n"
        "All examples are synthetic. Data-generation details and references are supplied "
        "with the reproducibility resources linked at the start. The report is maintained separately."
    )
    acknowledgements.id = "colab-reproduction-acknowledgements"
    custom_acknowledgements = ROOT / "notebooks/colab_acknowledgements.md"
    if custom_acknowledgements.is_file():
        acknowledgements.source = custom_acknowledgements.read_text(encoding="utf-8")
    notebook.cells.append(acknowledgements)
    notebook.metadata["runtime_bundle"] = {
        "url": f"https://raw.githubusercontent.com/{PUBLIC_REPOSITORY}/{asset_ref}/{manifest['path']}",
        "path": manifest["path"],
        "sha256": manifest["sha256"],
        "asset_commit": asset_ref,
        "bytes": manifest["bytes"],
        "source_commit": manifest["source_commit"],
    }
    notebook.metadata["colab"] = {"provenance": [], "toc_visible": True}
    nbformat.validate(notebook)
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(notebook, target)
    subprocess.run(
        [sys.executable, "-m", "ruff", "format", str(target)],
        capture_output=True,
        text=True,
        check=True,
    )
    notebook = nbformat.read(target, as_version=4)
    print(
        json.dumps(
            {
                "notebook": str(target),
                "bytes": target.stat().st_size,
                "largest_code_cell": max(len(c.source) for c in cells if c.cell_type == "code"),
            }
        )
    )
    return notebook


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    assets = commands.add_parser("assets")
    assets.add_argument("--public-dir", required=True, type=Path)
    notebook = commands.add_parser("notebook")
    notebook.add_argument("--asset-ref", required=True)
    notebook.add_argument("--output", type=Path, default=ROOT / "notebooks/project_colab.ipynb")
    args = parser.parse_args()
    if args.command == "assets":
        build_assets(args.public_dir)
    else:
        export_notebook(
            json.loads(MANIFEST.read_text(encoding="utf-8")), args.asset_ref, args.output
        )


if __name__ == "__main__":
    main()
