"""Bundle only the finalized small notebook and every EPS figure."""

import argparse
import hashlib
import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

import nbformat

ROOT = Path(__file__).resolve().parents[1]


def package_notebook_eps(notebook, output, *, wp03_core=False):
    notebook, output = Path(notebook), Path(output)
    nb = nbformat.read(notebook, as_version=4)
    nbformat.validate(nb)
    if nb.metadata.get("work_packages") != [f"WP{i:02d}" for i in range(1, 6)]:
        raise ValueError("Expected the final WP01-WP05 notebook")
    if not nb.metadata.get("runtime_bundle", {}).get("sha256"):
        raise ValueError("Expected the small notebook with its verified public runtime")
    files = {"project.ipynb": notebook.read_bytes()}
    figures = sorted((ROOT / "artifacts/figures").glob("*.eps"))
    if wp03_core:
        figures = [
            figure
            for figure in figures
            if figure.stem not in {"wp03_sensitivity_yield", "wp03_bottleneck"}
        ]
        if not any(figure.stem == "wp03_bottleneck_core" for figure in figures):
            raise ValueError("Core WP03 delivery requires its trajectories-only bottleneck figure")
    if {path.name[:4] for path in figures} != {f"wp{i:02d}" for i in range(1, 6)}:
        raise ValueError("EPS figures must cover all five work packages")
    for figure in figures:
        data = figure.read_bytes()
        if not data.startswith(b"%!PS-Adobe") or b"EPSF" not in data[:100]:
            raise ValueError(f"Not an EPS file: {figure.name}")
        files[f"figures/{figure.name}"] = data
    hashes = {name: hashlib.sha256(data).hexdigest() for name, data in files.items()}
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for name, data in sorted(files.items()):
            entry = ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.compress_type = ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, data)
    with ZipFile(output) as archive:
        if set(archive.namelist()) != set(files) or archive.testzip() is not None:
            raise ValueError("ZIP inventory/integrity check failed")
        if not all(
            hashlib.sha256(archive.read(name)).hexdigest() == h for name, h in hashes.items()
        ):
            raise ValueError("ZIP content differs from the selected notebook/figures")
    # The manifest stays outside the requested notebook-and-EPS-only archive.
    record = {
        "archive": output.name,
        "zip_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "zip_bytes": output.stat().st_size,
        "files": len(files),
        "notebooks": 1,
        "eps_figures": len(figures),
        "wp03_core": wp03_core,
        "public_runtime": dict(nb.metadata.runtime_bundle),
        "file_sha256": hashes,
    }
    output.with_suffix(".manifest.json").write_text(
        json.dumps(record, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps({k: v for k, v in record.items() if k not in {"file_sha256", "public_runtime"}})
    )
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--notebook", type=Path, default=ROOT / "notebooks/project_colab.ipynb")
    parser.add_argument(
        "--output", type=Path, default=ROOT / "deliverables/mm-allee-final-notebook-eps.zip"
    )
    parser.add_argument(
        "--wp03-core", action="store_true", help="Omit WP03's archived optional figure"
    )
    args = parser.parse_args()
    package_notebook_eps(args.notebook, args.output, wp03_core=args.wp03_core)


if __name__ == "__main__":
    main()
