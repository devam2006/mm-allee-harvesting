"""Stage an EPS report for PDF-only engines; never modify authored TeX sources."""

import argparse
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def prepare(output, ghostscript=None):
    output = Path(output).resolve()
    if output == (ROOT / "report").resolve():
        raise ValueError("Build in a separate directory to preserve the original EPS sources")
    engine = ghostscript or shutil.which("gs") or shutil.which("gswin64c")
    if not engine:
        raise RuntimeError("Install Ghostscript, or pass --ghostscript PATH")
    output.mkdir(parents=True, exist_ok=True)
    for pattern in ("*.tex", "*.bib", "sections/*.tex"):
        for source in (ROOT / "report").glob(pattern):
            destination = output / source.relative_to(ROOT / "report")
            destination.parent.mkdir(parents=True, exist_ok=True)
            text = source.read_text(encoding="utf-8")
            text = re.sub(r"(\\includegraphics(?:\[[^\]]*\])?\{[^}]+)\.eps\}", r"\1.pdf}", text)
            destination.write_text(text, encoding="utf-8", newline="\n")
    figures = output / "figures"
    figures.mkdir(exist_ok=True)
    for source in (ROOT / "report/figures").glob("*.eps"):
        subprocess.run(
            [
                engine,
                "-dSAFER",
                "-dBATCH",
                "-dNOPAUSE",
                "-sDEVICE=pdfwrite",
                "-dCompatibilityLevel=1.5",
                "-dEPSCrop",
                f"-sOutputFile={figures / (source.stem + '.pdf')}",
                str(source),
            ],
            check=True,
            capture_output=True,
        )
    print(f"Staged report and temporary PDF figures in {output}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "results/report-build")
    parser.add_argument("--ghostscript")
    args = parser.parse_args()
    prepare(args.output, args.ghostscript)


if __name__ == "__main__":
    main()
