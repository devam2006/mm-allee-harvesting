"""Create an Overleaf-ready source ZIP with EPS originals and no converted PDFs."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]


def main():
    report = ROOT / "report"
    selected = set()
    for pattern in ("*.tex", "*.bib", "README.md", "sections/*.tex", "figures/*.eps", "tools/*.py"):
        selected.update(path for path in report.glob(pattern) if path.is_file())
    target = ROOT / "deliverables/MM_Project_Report.zip"
    with ZipFile(target, "w", compression=ZIP_DEFLATED) as archive:
        for path in sorted(selected):
            info = ZipInfo(path.relative_to(report).as_posix(), date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes())
    with ZipFile(target) as archive:
        assert "main.tex" in archive.namelist() and archive.testzip() is None
        assert not any(name.endswith(".pdf") for name in archive.namelist())
    print(f"Packaged {len(selected)} source/EPS files: {target}")


if __name__ == "__main__":
    main()
