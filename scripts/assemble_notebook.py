"""Deterministically assemble the five independently owned notebook fragments."""

import argparse
from copy import deepcopy
from pathlib import Path

import nbformat

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = [
    "01_foundations.ipynb",
    "02_model_b_history.ipynb",
    "03_collapse.ipynb",
    "04_forward_pinn.ipynb",
    "05_inverse_validation.ipynb",
]


def build_notebook(packages=None):
    packages = list(range(1, 6)) if packages is None else list(packages)
    nb = nbformat.v4.new_notebook()
    nb.metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    nb.cells = [
        nbformat.v4.new_markdown_cell(
            "# Strong Allee effect and harvesting\n\n"
            "Assembled from five task fragments. Read the scope/status in each section. "
            "Synthetic examples are not empirical observations. The final submission requires "
            "completed derivations, algorithms, results, interpretation and AI/data acknowledgements."
        ),
        nbformat.v4.new_code_cell(
            "import os\nfrom pathlib import Path\n\nimport mm_allee\n\n"
            "ROOT = next(\n"
            "    (\n"
            "        path\n"
            "        for path in [Path.cwd(), *Path.cwd().parents]\n"
            '        if (path / "pyproject.toml").exists() and (path / "src/mm_allee").exists()\n'
            "    ),\n"
            "    None,\n"
            ")\n"
            'if ROOT is None:\n    raise RuntimeError("Run this notebook inside the project checkout")\n'
            'os.chdir(ROOT)\nprint("Package:", mm_allee.__version__)'
        ),
    ]
    nb.cells[0]["id"] = "project-introduction"
    nb.cells[1]["id"] = "project-setup"
    overview = ROOT / "notebooks/frontmatter.md"
    if overview.is_file():
        nb.cells[0].source = overview.read_text(encoding="utf-8")
    for index, name in enumerate(EXPECTED, 1):
        if index not in packages:
            continue
        fragment = nbformat.read(ROOT / "notebooks/sections" / name, as_version=4)
        nbformat.validate(fragment)
        for j, original in enumerate(fragment.cells):
            cell = deepcopy(original)
            cell["id"] = f"wp{index:02d}-cell-{j:03d}"
            if cell.cell_type == "code":
                cell.outputs = []
                cell.execution_count = None
            nb.cells.append(cell)
    nbformat.validate(nb)
    nb.metadata["work_packages"] = [f"WP{index:02d}" for index in packages]
    return nb


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packages", nargs="+", type=int, choices=range(1, 6))
    parser.add_argument("--output", type=Path, default=ROOT / "notebooks/project.ipynb")
    args = parser.parse_args()
    nb = build_notebook(args.packages)
    target = args.output
    target.parent.mkdir(parents=True, exist_ok=True)
    nbformat.write(nb, target)
    print(f"Assembled {len(nb.cells)} cells into {target}")


if __name__ == "__main__":
    main()
