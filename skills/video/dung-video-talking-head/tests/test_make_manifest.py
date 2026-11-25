# tests/test_make_manifest.py — Task 16: make_manifest.py sinh MANIFEST.sha256
# của một bản release (spec §4.3): sha256 từng file thật thuộc release, sắp
# theo đường dẫn, bỏ MANIFEST.sha256 cũ và sản phẩm build (__pycache__,
# node_modules, .pytest_cache, *.pyc) — nguồn duy nhất lint_rules.py /
# verify.py (V1) dùng để khoá release qua rules.lock.
import hashlib

import make_manifest


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def test_build_manifest_lists_files_sorted_by_path(tmp_path):
    rules_path = tmp_path / "rules.json"
    rules_path.write_text("{}", encoding="utf-8")
    (tmp_path / "scripts").mkdir()
    stage_path = tmp_path / "scripts" / "stage.py"
    stage_path.write_bytes(bytes([112, 97, 115, 115, 10]))  # b"pass\n", tránh escape lệch trong nguồn

    manifest = make_manifest.build_manifest(tmp_path)

    assert manifest.splitlines() == [
        f"{_sha(rules_path.read_bytes())}  rules.json",
        f"{_sha(stage_path.read_bytes())}  scripts/stage.py",
    ]
    assert manifest.endswith("\n")


def test_build_manifest_excludes_own_file_and_build_artifacts(tmp_path):
    (tmp_path / "a.txt").write_bytes(b"a")
    (tmp_path / "MANIFEST.sha256").write_text("stale\n", encoding="utf-8")
    pycache = tmp_path / "scripts" / "thlib" / "__pycache__"
    pycache.mkdir(parents=True)
    (pycache / "paths.cpython-312.pyc").write_bytes(b"\x00\x01")
    (tmp_path / "scripts" / "loose.pyc").write_bytes(b"\x00")
    node_modules = tmp_path / "template" / "node_modules" / "react"
    node_modules.mkdir(parents=True)
    (node_modules / "index.js").write_text("module.exports = {}", encoding="utf-8")

    manifest = make_manifest.build_manifest(tmp_path)

    assert manifest == f"{_sha(b'a')}  a.txt\n"


def test_build_manifest_deterministic_across_calls(tmp_path):
    (tmp_path / "b.txt").write_text("hai", encoding="utf-8")
    (tmp_path / "a.txt").write_text("một", encoding="utf-8")

    first = make_manifest.build_manifest(tmp_path)
    second = make_manifest.build_manifest(tmp_path)

    assert first == second
    assert [line.split("  ", 1)[1] for line in first.splitlines()] == ["a.txt", "b.txt"]


def test_main_writes_manifest_and_prints_pass(tmp_path, capsys):
    release = tmp_path / "rel"
    release.mkdir()
    (release / "rules.json").write_text("{}", encoding="utf-8")

    code = make_manifest.main(["--release-dir", str(release)])

    out = capsys.readouterr().out
    assert code == 0
    assert "PASS" in out
    written = (release / "MANIFEST.sha256").read_text(encoding="utf-8")
    assert written == f"{_sha(b'{}')}  rules.json\n"


def test_main_missing_release_dir_fails(tmp_path, capsys):
    code = make_manifest.main(["--release-dir", str(tmp_path / "missing")])

    assert code == 1
    assert "Không tìm thấy" in capsys.readouterr().out
