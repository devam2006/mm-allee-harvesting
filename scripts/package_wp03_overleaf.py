"""Package only Devam's editable WP03 section and its three EPS figures."""

import hashlib
import json
import re
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]


def main():
    section = ROOT / "report/sections/03_collapse.tex"
    text = section.read_text(encoding="utf-8")
    names = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", text)
    if set(names) != {"wp03_basins.eps", "wp03_extinction.eps", "wp03_bottleneck_core.eps"}:
        raise ValueError("Unexpected WP03 report figure inventory")
    labels = set(re.findall(r"\\label\{([^}]+)\}", text))
    references = set(re.findall(r"\\(?:eqref|ref)\{([^}]+)\}", text))
    if references - labels or "\t" in text:
        raise ValueError("Unresolved section reference or invalid TeX escape")
    files = {"sections/03_collapse.tex": section.read_bytes()}
    for name in names:
        raw = (ROOT / "artifacts/figures" / name).read_bytes()
        if not raw.startswith(b"%!PS-Adobe") or b"EPSF" not in raw[:100]:
            raise ValueError(f"Invalid EPS: {name}")
        files[f"figures/{name}"] = raw
    files["README.txt"] = (
        "WP03 core-scope Overleaf update - editable draft\n\n"
        "Copy sections/03_collapse.tex and the three files in figures/ into your\n"
        "CURRENT Overleaf project, preserving teammates' other sections.\n"
        "This ZIP is a section update, not a full replacement project.\n\n"
        "Keep your existing main.tex, preamble, metadata and bibliography.\n"
        "The section retains bibliography keys scipy_solve_ivp, scipy_quad and\n"
        "scipy_bounded from the supplied Overleaf project.\n"
        "Compile the existing main.tex in Overleaf and inspect the final layout.\n"
        "No compiled PDF is supplied; the figures here are EPS only.\n\n"
        "Scope: thresholds, basins, extinction, numerical accuracy, qualitative\n"
        "slow decline near critical catch, reference data and limitations.\n"
        "Sensitivity, yield optimisation and asymptotic derivations are omitted.\n"
        "Review and edit the section yourself before finalising it.\n"
    ).encode()
    output = ROOT / "deliverables/wp03-overleaf-update.zip"
    with ZipFile(output, "w", compression=ZIP_DEFLATED) as archive:
        for name, raw in sorted(files.items()):
            entry = ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.compress_type = ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, raw)
    with ZipFile(output) as archive:
        if archive.testzip() is not None or set(archive.namelist()) != set(files):
            raise ValueError("WP03 archive failed integrity check")
    record = {
        "archive": output.name,
        "bytes": output.stat().st_size,
        "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "files": {name: hashlib.sha256(raw).hexdigest() for name, raw in files.items()},
        "scope": "WP03 section only; copy into the current Overleaf project",
        "compiled_pdf_included": False,
    }
    output.with_suffix(".manifest.json").write_text(
        json.dumps(record, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps({key: value for key, value in record.items() if key != "files"}))


if __name__ == "__main__":
    main()
