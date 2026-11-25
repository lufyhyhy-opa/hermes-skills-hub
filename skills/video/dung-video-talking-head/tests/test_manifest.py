# tests/test_manifest.py — C10: thlib.manifest (spec §4.3 "lint_rules.py so lock với release; lệch
# là FAIL"). lint_rules.py và V1 băm lại TỪNG file của release so với từng dòng MANIFEST, không chỉ
# sha của chính file MANIFEST — sửa tại chỗ rules.json hay một script mà không sinh lại MANIFEST
# phải FAIL. Release giả dựng trong tmp_path; test cuối kiểm release thật trong repo.
import hashlib
from pathlib import Path

from thlib import manifest, paths


def _release(root: Path) -> Path:
    rel = root / "releases" / "1.1.0"
    (rel / "scripts").mkdir(parents=True)
    (rel / "sfx").mkdir()
    (rel / "rules.json").write_bytes(b'{"version": "1.1.0"}\n')
    (rel / "scripts" / "stage.py").write_bytes(b"print('stage')\n")
    (rel / "sfx" / "hit.wav").write_bytes(b"RIFF\x00\x00\r\n\x00WAVE")
    (rel / manifest.MANIFEST_NAME).write_text(manifest.build_manifest(rel), encoding="utf-8")
    return rel


def _locked(rel: Path) -> str:
    """sha MANIFEST mà rules.lock ghi (state.write_lock)."""
    return manifest.file_sha256(rel / manifest.MANIFEST_NAME)


def test_fresh_release_matches_its_manifest(tmp_path):
    rel = _release(tmp_path)
    assert manifest.release_errors(rel, _locked(rel)) == []


def test_in_place_edit_without_new_manifest_names_the_file(tmp_path):
    rel = _release(tmp_path)
    locked = _locked(rel)
    (rel / "rules.json").write_bytes(b'{"version": "1.1.0", "sua_tai_cho": true}\n')
    errors = manifest.release_errors(rel, locked)
    assert len(errors) == 1, errors
    assert (rel / "rules.json").as_posix() in errors[0]


def test_missing_and_unlisted_release_files_are_named(tmp_path):
    rel = _release(tmp_path)
    locked = _locked(rel)
    (rel / "scripts" / "stage.py").unlink()
    (rel / "scripts" / "them_moi.py").write_bytes(b"x = 1\n")
    text = " ".join(manifest.release_errors(rel, locked))
    assert (rel / "scripts" / "stage.py").as_posix() in text
    assert (rel / "scripts" / "them_moi.py").as_posix() in text


def test_build_artifacts_are_not_release_files(tmp_path):
    rel = _release(tmp_path)
    locked = _locked(rel)
    (rel / "scripts" / "__pycache__").mkdir()
    (rel / "scripts" / "__pycache__" / "stage.cpython-312.pyc").write_bytes(b"\x00\x01")
    (rel / "template" / "node_modules" / "react").mkdir(parents=True)
    (rel / "template" / "node_modules" / "react" / "index.js").write_bytes(b"module.exports = {}\n")
    assert manifest.release_errors(rel, locked) == []


def test_manifest_missing_or_not_the_locked_one_fails(tmp_path):
    rel = _release(tmp_path)
    locked = _locked(rel)
    errors = manifest.release_errors(rel, "0" * 64)
    assert len(errors) == 1 and "lệch" in errors[0] and "rules.lock" in errors[0]
    (rel / manifest.MANIFEST_NAME).unlink()
    errors = manifest.release_errors(rel, locked)
    assert len(errors) == 1 and (rel / manifest.MANIFEST_NAME).as_posix() in errors[0]


def test_line_endings_do_not_change_text_hashes(tmp_path):
    """git core.autocrlf=true checkout thư mục skill thật bằng CRLF; worktree dev có file LF lẫn
    CRLF — sha văn bản (cả MANIFEST mà rules.lock khoá) không phụ thuộc kiểu xuống dòng; file
    nhị phân băm nguyên byte."""
    lf, crlf = tmp_path / "lf.py", tmp_path / "crlf.py"
    lf.write_bytes(b"a = 1\nb = 2\n")
    crlf.write_bytes(b"a = 1\r\nb = 2\r\n")
    assert manifest.file_sha256(lf) == manifest.file_sha256(crlf) == hashlib.sha256(lf.read_bytes()).hexdigest()
    wav = tmp_path / "x.wav"
    wav.write_bytes(b"RIFF\x00\r\n")
    assert manifest.file_sha256(wav) == hashlib.sha256(b"RIFF\x00\r\n").hexdigest()

    rel = _release(tmp_path / "checkout")
    locked = _locked(rel)
    for path in (rel / "scripts" / "stage.py", rel / manifest.MANIFEST_NAME):
        data = path.read_bytes().replace(b"\r\n", b"\n")
        path.write_bytes(data.replace(b"\n", b"\r\n") if path.suffix == ".py" else data)
    assert manifest.release_errors(rel, locked) == []


def test_shipped_release_matches_its_manifest():
    """releases/1.1.0/MANIFEST.sha256 trong repo được sinh lại sau mọi lần sửa release
    (PYTHONIOENCODING=utf-8 python tools/make_manifest.py)."""
    rel = paths.release_dir("1.1.0")
    assert manifest.release_errors(rel, _locked(rel)) == []
