import json

import pytest

import lint_rules
from thlib import manifest, paths, rules, state


def test_load_and_get():
    R = rules.load("1.1.0")
    assert R.version == "1.1.0"
    assert R.get("sfx.p2p_s") == 1.0
    assert R.preset("standard")["tier_db"]["A"] == -3.0


def test_every_leaf_has_source():
    R = rules.load("1.1.0")
    missing = rules.leaves_without_source(R.raw)
    assert missing == []


def test_schema_valid():
    R = rules.load("1.1.0")
    rules.validate(R.raw)  # raises on error


def test_load_from_project_lock(tmp_path):
    state.write_lock(tmp_path, "1.1.0")
    assert rules.load(project=tmp_path).version == "1.1.0"


def test_per_video_budget_formula():
    R = rules.load("1.1.0")
    assert rules.per_video_budget(R, "standard", 43.12) == 11  # ceil(2.5*4.312)


def test_get_missing_key_raises_with_path():
    R = rules.load("1.1.0")
    with pytest.raises(KeyError, match="sfx.khong_ton_tai"):
        R.get("sfx.khong_ton_tai")


def test_load_requires_ver_or_project():
    with pytest.raises(ValueError):
        rules.load()


# --- lint_rules.py --------------------------------------------------------


def _fake_release(tmp_path, monkeypatch):
    """Trỏ paths.release_dir sang thư mục tạm chép từ release 1.1.0 thật (kèm
    MANIFEST.sha256 sinh cho đúng bản tạm), để test lint mà không đụng vào
    rules.json/schema thật."""
    rel = tmp_path / "rel"
    rel.mkdir()
    real_rel = paths.release_dir("1.1.0")
    (rel / "rules.json").write_text(
        (real_rel / "rules.json").read_text(encoding="utf-8"), encoding="utf-8"
    )
    (rel / "rules.schema.json").write_text(
        (real_rel / "rules.schema.json").read_text(encoding="utf-8"), encoding="utf-8"
    )
    (rel / manifest.MANIFEST_NAME).write_text(manifest.build_manifest(rel), encoding="utf-8")
    monkeypatch.setattr(paths, "release_dir", lambda ver: rel)
    return rel


def test_lint_pass(tmp_path, monkeypatch):
    _fake_release(tmp_path, monkeypatch)
    project = tmp_path / "proj"
    state.write_lock(project, "1.1.0")
    assert lint_rules.lint(project) == []


def test_lint_missing_lock_version(tmp_path):
    project = tmp_path / "proj"
    project.mkdir()
    (project / state.LOCK_FILENAME).write_text(
        json.dumps({"skill": "dung-video-talking-head"}), encoding="utf-8"
    )
    errors = lint_rules.lint(project)
    assert any("version" in e for e in errors)


def test_lint_sha_mismatch(tmp_path, monkeypatch):
    rel = _fake_release(tmp_path, monkeypatch)
    project = tmp_path / "proj"
    state.write_lock(project, "1.1.0")  # chưa có MANIFEST.sha256 -> khoá "dev"
    (rel / "MANIFEST.sha256").write_text("gia-lap-doi-sau-khi-khoa", encoding="utf-8")

    errors = lint_rules.lint(project)
    assert any("lệch" in e for e in errors)


def test_lint_fails_when_release_file_edited_after_fresh_lock(tmp_path, monkeypatch):
    """C10: lock vừa ghi (như scaffold của INTAKE) không làm lint thành phép lặp — sửa tại chỗ
    rules.json (JSON vẫn hợp lệ, schema/sources vẫn đạt) mà không sinh lại MANIFEST là FAIL,
    lỗi nêu đúng file."""
    rel = _fake_release(tmp_path, monkeypatch)
    project = tmp_path / "proj"
    state.write_lock(project, "1.1.0")
    raw = json.loads((rel / "rules.json").read_text(encoding="utf-8"))
    raw["params"]["sfx"]["p2p_s"] = 0.5
    (rel / "rules.json").write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")

    errors = lint_rules.lint(project)
    assert len(errors) == 1, errors
    assert (rel / "rules.json").as_posix() in errors[0]


def test_lint_fails_without_manifest(tmp_path, monkeypatch):
    """Không có MANIFEST.sha256 thì không kiểm được file release nào ⇒ FAIL (hết chế độ "dev")."""
    rel = _fake_release(tmp_path, monkeypatch)
    (rel / manifest.MANIFEST_NAME).unlink()
    project = tmp_path / "proj"
    state.write_lock(project, "1.1.0")

    errors = lint_rules.lint(project)
    assert any(manifest.MANIFEST_NAME in e for e in errors), errors


def test_lint_missing_source(tmp_path, monkeypatch):
    rel = _fake_release(tmp_path, monkeypatch)
    raw = json.loads((rel / "rules.json").read_text(encoding="utf-8"))
    del raw["sources"]["sfx.p2p_s"]
    (rel / "rules.json").write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")

    project = tmp_path / "proj"
    state.write_lock(project, "1.1.0")

    errors = lint_rules.lint(project)
    assert any("sources" in e for e in errors)


def test_lint_schema_invalid(tmp_path, monkeypatch):
    rel = _fake_release(tmp_path, monkeypatch)
    raw = json.loads((rel / "rules.json").read_text(encoding="utf-8"))
    del raw["params"]["fps"]
    (rel / "rules.json").write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")

    project = tmp_path / "proj"
    state.write_lock(project, "1.1.0")

    errors = lint_rules.lint(project)
    assert any("schema" in e for e in errors)


def test_lint_cli_exit_code(tmp_path, monkeypatch, capsys):
    _fake_release(tmp_path, monkeypatch)
    project = tmp_path / "proj"
    state.write_lock(project, "1.1.0")
    monkeypatch.setattr("sys.argv", ["lint_rules.py", str(project)])
    assert lint_rules.main() == 0

    bad_project = tmp_path / "bad"
    bad_project.mkdir()
    monkeypatch.setattr("sys.argv", ["lint_rules.py", str(bad_project)])
    assert lint_rules.main() == 1
