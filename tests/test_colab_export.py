"""Regressions for browser-sized notebooks and verified runtime restoration."""

import hashlib
import importlib.util
import io
import os
import sys
from pathlib import Path
from types import SimpleNamespace
from zipfile import ZipFile

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
REF = "a" * 40


@pytest.fixture(scope="module")
def exporter():
    # The PINN-only CI selection does not install notebook authoring dependencies.
    # Load them when these core tests run, not while pytest collects all modules.
    sys.path.insert(0, str(SCRIPTS))
    spec = importlib.util.spec_from_file_location(
        "colab_export", SCRIPTS / "export_colab_notebook.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def manifest(payload=b"snapshot"):
    return {
        "bytes": len(payload),
        "path": "runtime/example.zip",
        "sha256": hashlib.sha256(payload).hexdigest(),
        "source_commit": REF,
    }


def test_colab_notebook_opens_without_large_encoded_cells_or_attachments(tmp_path, exporter):
    notebook = exporter.export_notebook(manifest(), REF, tmp_path / "project.ipynb")
    assert (tmp_path / "project.ipynb").stat().st_size < 150_000
    assert max(len(cell.source) for cell in notebook.cells if cell.cell_type == "code") < 10_000
    assert not any("base64" in cell.source or cell.get("attachments") for cell in notebook.cells)
    # The finalized layout has two WP04 and two WP05 display figures;
    # the exploratory diagnostic remains in the downloadable figure assets.
    assert len([cell for cell in notebook.cells if "_figures.display" in cell.source]) == 4
    bundle = notebook.metadata.runtime_bundle
    assert f"/{REF}/runtime/" in bundle.url and bundle.sha256 == manifest()["sha256"]


@pytest.mark.parametrize("ref", ["main", "not-a-commit"])
def test_hosted_assets_require_an_immutable_commit(ref, exporter):
    with pytest.raises(ValueError, match="immutable"):
        exporter.setup_source(manifest(), ref)


def run_setup(monkeypatch, tmp_path, payload, exporter, expected_payload=None):
    runtime = tmp_path / "runtime"
    runtime.mkdir()
    (runtime / "example.zip").write_bytes(payload)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("PYTHONPATH", os.environ.get("PYTHONPATH", ""))
    monkeypatch.setattr(sys, "path", list(sys.path))
    monkeypatch.setattr("tempfile.gettempdir", lambda: str(tmp_path))
    monkeypatch.setattr("urllib.request.urlopen", lambda *a, **k: pytest.fail("Unexpected network"))
    monkeypatch.setattr("subprocess.check_call", lambda *a, **k: None)
    namespace = {"get_ipython": lambda: SimpleNamespace(run_line_magic=lambda *args: None)}
    exec(exporter.setup_source(manifest(expected_payload or payload), REF), namespace)
    return namespace


def test_packaged_runtime_restores_offline_and_preserves_source_bytes(
    monkeypatch, tmp_path, exporter
):
    stream = io.BytesIO()
    expected = b"answer = 42\n"
    with ZipFile(stream, "w") as archive:
        archive.writestr("src/example.py", expected)
        archive.writestr("pyproject.toml", "[project]\nname='example'\n")
    namespace = run_setup(monkeypatch, tmp_path, stream.getvalue(), exporter)
    root = namespace["ROOT"]
    assert (root / "src/example.py").read_bytes() == expected
    assert str(root / "src") == sys.path[0] == os.environ["PYTHONPATH"]


def test_tampered_runtime_is_rejected_before_extraction(monkeypatch, tmp_path, exporter):
    with pytest.raises(RuntimeError, match="checksum mismatch"):
        run_setup(monkeypatch, tmp_path, b"tampered", exporter, expected_payload=b"expected")


def test_runtime_archive_cannot_escape_the_restored_folder(monkeypatch, tmp_path, exporter):
    stream = io.BytesIO()
    with ZipFile(stream, "w") as archive:
        archive.writestr("../escape.txt", "invalid")
    with pytest.raises(RuntimeError, match="Invalid project data path"):
        run_setup(monkeypatch, tmp_path, stream.getvalue(), exporter)
    assert not (tmp_path / "escape.txt").exists()
