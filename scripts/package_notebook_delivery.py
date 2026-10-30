"""Build the notebook/data/figure handoff; the report is managed in Overleaf."""

import argparse
import csv
import hashlib
import importlib.metadata
import io
import json
import platform
import subprocess
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

import nbformat
import numpy as np

from mm_allee.data import generate_noisy_observations
from mm_allee.validation import audit_splits_and_leakage

ROOT = Path(__file__).resolve().parents[1]


def observation_csv(config):
    stream = io.StringIO(newline="")
    columns = [
        "dataset_id",
        "observation_id",
        "trajectory_id",
        "model",
        "time",
        "population",
        "observed_population",
        "split",
        "noise_sigma",
        "noise_seed",
        "is_synthetic",
    ]
    writer = csv.DictWriter(stream, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    total = 0
    for case in config["cases"]:
        with (ROOT / case["reference_csv"]).open(encoding="utf-8") as handle:
            clean = list(csv.DictReader(handle))
        times = np.array([float(row["time"]) for row in clean])
        populations = np.array([float(row["population"]) for row in clean])
        for sigma in config["noise_sigmas"]:
            for seed in config["seeds"]:
                obs = generate_noisy_observations(
                    times,
                    populations,
                    trajectory_id=case["case_id"],
                    model=case["model"],
                    noise_sigma=sigma,
                    noise_seed=seed,
                    n_ref=config["fixed_reference_scales"]["population"],
                )
                audit_splits_and_leakage(obs)
                dataset = f"{case['case_id']}:sigma={sigma}:seed={seed}"
                for i, time in enumerate(times):
                    writer.writerow(
                        dict(
                            dataset_id=dataset,
                            observation_id=obs["observation_id"][i],
                            trajectory_id=case["case_id"],
                            model=case["model"],
                            time=time,
                            population=populations[i],
                            observed_population=obs["observed_population"][i],
                            split=obs["split"][i],
                            noise_sigma=sigma,
                            noise_seed=seed,
                            is_synthetic=True,
                        )
                    )
                    total += 1
    return stream.getvalue().encode(), total


def package_delivery(executed_notebook, target):
    nb = nbformat.read(executed_notebook, as_version=4)
    nbformat.validate(nb)
    if nb.metadata.get("work_packages") != [f"WP{i:02d}" for i in range(1, 6)]:
        raise ValueError("Expected the five-package notebook")
    cells = [cell for cell in nb.cells if cell.cell_type == "code"]
    if any(cell.execution_count is None for cell in cells):
        raise ValueError("Execute every notebook code cell before packaging")
    if any(out.output_type == "error" for cell in cells for out in cell.outputs):
        raise ValueError("Notebook contains an execution error")
    files = {"project.ipynb": Path(executed_notebook).read_bytes()}
    for directory, prefix in [
        ("src", "source/src"),
        ("scripts", "source/scripts"),
        ("configs", "configs"),
        ("artifacts/tables", "tables"),
        ("artifacts/manifests", "provenance"),
    ]:
        for path in (ROOT / directory).rglob("*"):
            if (
                path.is_file()
                and path.suffix in {".py", ".json", ".csv", ".txt", ".md"}
                and "__pycache__" not in path.parts
            ):
                files[f"{prefix}/{path.relative_to(ROOT / directory).as_posix()}"] = (
                    path.read_bytes()
                )
    for path in (ROOT / "data/fixtures/wp03_reference").glob("*"):
        if path.is_file():
            files[f"datasets/clean/{path.name}"] = path.read_bytes()
    inventory = []
    for image in sorted((ROOT / "artifacts/figures").glob("*.png")):
        eps = image.with_suffix(".eps")
        if not eps.is_file() or not eps.read_bytes().startswith(b"%!PS"):
            raise ValueError(f"Missing/invalid EPS partner: {image.name}")
        for path in [image, eps, image.with_suffix(".pdf")]:
            if path.is_file():
                files[f"figures/{path.name}"] = path.read_bytes()
        inventory.append(
            dict(
                stem=image.stem,
                package=image.stem[:4].upper(),
                png=True,
                eps=True,
                historical=any(word in image.stem for word in ["original_settings", "swish_lr"]),
            )
        )
    config = json.loads((ROOT / "configs/wp05_final.json").read_text())
    files["datasets/wp05_observations.csv"], observation_count = observation_csv(config)
    files["datasets/README.md"] = (
        "# Synthetic datasets\n\nNo external field dataset was used or downloaded. The six clean trajectories are the frozen WP03 fixtures. "
        "wp05_observations.csv reconstructs all scenarios in configs/wp05_final.json using the current versioned noise/split generator: 6 cases, 3 noise levels, 3 seeds. "
        "These are deterministic reconstructed inputs, not a new fit or an assertion of byte identity with an author's unsaved historical observation arrays. "
        "Use (dataset_id, observation_id) as the unique key. population is clean evaluation truth; train only on observed_population rows labelled train. "
        "Validation/test windows remain separate. Noise is never clipped. Units and fixed scales are in the config.\n"
    ).encode()
    for name in [
        "docs/AI_USAGE.md",
        "docs/REFERENCES.md",
        "docs/SCIENTIFIC_CONTRACT.md",
        "docs/INTERFACES.md",
        "docs/CLASSICAL_INTEGRATION.md",
        "pyproject.toml",
    ]:
        files[f"source/{name}"] = (ROOT / name).read_bytes()
    environment = {
        "python": platform.python_version(),
        **{
            name: importlib.metadata.version(name)
            for name in ["numpy", "scipy", "matplotlib", "jax", "nbformat", "nbclient"]
        },
    }
    files["environment.json"] = json.dumps(environment, indent=2).encode()
    files["figures/INVENTORY.json"] = json.dumps(inventory, indent=2).encode()
    snapshot = dict(
        source_commit=subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip(),
        source_dirty=bool(
            subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True).strip()
        ),
        executed_code_cells=len(cells),
        synthetic_observation_rows=observation_count,
        figure_pairs=len(inventory),
        work_packages=[f"WP{i:02d}" for i in range(1, 6)],
        report="Maintained separately in Overleaf",
        known_limits=[
            "WP05 validation-selection-off loss histories and optimizer status reporting remain under review in PR #10",
            "Recorded final-sweep tables are not fresh reruns of all fits",
            "Human review, presentation and final Overleaf report remain separate",
        ],
    )
    files["SOURCE_SNAPSHOT.json"] = json.dumps(snapshot, indent=2).encode()
    files["README.md"] = (
        "# Notebook, data and figure handoff\n\nOpen project.ipynb in Jupyter and Restart Kernel / Run All. It contains its source/config/data/evidence snapshot and restores it automatically; no repository checkout or dataset download is needed. "
        "Install the scientific dependencies listed in the first Markdown cell. The tested environment is in environment.json. "
        "The saved notebook includes the actual successful kernel outputs; its ordinary demonstrations are not reruns of all recorded research sweeps.\n\n"
        "figures/ includes PNG/EPS pairs and available PDFs; use EPS files in the separately maintained Overleaf report. Historical alternatives are labelled in INVENTORY.json. "
        "datasets/ includes clean synthetic fixtures and reconstructed noisy training/validation/test inputs. tables/ and provenance/ preserve recorded evidence and its limitations. "
        "source/ contains readable implementation, authoring scripts and disclosures.\n\n"
        "This is a technically verified integration candidate, not certification of the unresolved WP05 reporting labels, human approvals, presentation readiness or final Overleaf report.\n"
    ).encode()
    files["SHA256SUMS.json"] = json.dumps(
        {name: hashlib.sha256(data).hexdigest() for name, data in files.items()}, indent=2
    ).encode()
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(target, "w", ZIP_DEFLATED) as archive:
        for name, data in sorted(files.items()):
            archive.writestr(name, data)
    with ZipFile(target) as archive:
        expected = json.loads(archive.read("SHA256SUMS.json"))
        assert all(
            hashlib.sha256(archive.read(name)).hexdigest() == digest
            for name, digest in expected.items()
        )
    target.with_suffix(".manifest.json").write_text(
        json.dumps(
            {
                **snapshot,
                "zip_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
                "zip_bytes": target.stat().st_size,
                "files": len(files),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"archive": str(target), **snapshot, "files": len(files)}))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--notebook", type=Path, required=True)
    parser.add_argument(
        "--output", type=Path, default=ROOT / "deliverables/mm-allee-notebook-data-figures.zip"
    )
    args = parser.parse_args()
    package_delivery(args.notebook, args.output)


if __name__ == "__main__":
    main()
