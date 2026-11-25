# tests/test_verify.py — VERIFY V1-V7 (Task 13).
# Unit test nhanh cho V5 (chuỗi provenance, không cần BUILD thật) + e2e chậm
# trên dự án video 02 (Task 12) cho toàn bộ V1-V7 và hai kịch bản tamper.
import json
import shutil
import subprocess
from pathlib import Path

import pytest

import verify
from test_build_e2e import _intake_core, _scaffold
from thlib import build, manifest, paths, state
from thlib import verify as tverify

FIXTURES = Path(__file__).parent / "fixtures"

V5_FILES = {
    "words.json": [], "pauses.json": {}, "meta.json": {}, "edit.json": {},
    "picture_lock.json": {}, "out/sfx_plan.json": {},
}


def _read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _make_v5_project(tmp_path):
    """Dự án tối giản chỉ để kiểm check_v5: 6 artifact của Data Contracts +
    STATE.md ghi đúng sha8 hiện tại của từng file (mô phỏng INTAKE/PLAN/BUILD —
    stage.py, Task 14, chưa có)."""
    state.write_lock(tmp_path, "1.1.0")
    for rel, content in V5_FILES.items():
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(content), encoding="utf-8")
    state.append_state(tmp_path, "INTAKE", "t", "1", "test",
                        [tmp_path / "words.json", tmp_path / "pauses.json", tmp_path / "meta.json"])
    state.append_state(tmp_path, "PLAN", "t", "1", "test", [tmp_path / "edit.json"])
    state.append_state(tmp_path, "BUILD", "t", "1", "test",
                        [tmp_path / "picture_lock.json", tmp_path / "out" / "sfx_plan.json"])
    return tmp_path


def test_check_v5_passes_when_state_matches_current_files(tmp_path):
    project = _make_v5_project(tmp_path)
    result = tverify.check_v5(project)
    assert result["ok"] is True, result
    assert result["owner_stage"] is None


def test_check_v5_fails_owner_plan_when_edit_json_tampered(tmp_path):
    project = _make_v5_project(tmp_path)
    (project / "edit.json").write_text('{"schema": "edit/1.1", "tampered": true}', encoding="utf-8")
    result = tverify.check_v5(project)
    assert result["ok"] is False
    assert result["owner_stage"] == "PLAN"
    assert "edit.json" in result["msg"]


def test_check_v5_fails_owner_intake_when_words_json_missing(tmp_path):
    project = _make_v5_project(tmp_path)
    (project / "words.json").unlink()
    result = tverify.check_v5(project)
    assert result["ok"] is False
    assert result["owner_stage"] == "INTAKE"


def test_check_v1_passes_without_card_rules(tmp_path, monkeypatch):
    """Không truyền card_rules (CLI mặc định, chưa có stage.py/Task 14) ⇒ V1 bỏ
    qua chấm khớp card, vẫn PASS như trước (fix round 2, finding 2: không phá
    hành vi hiện tại khi không ai cung cấp card)."""
    monkeypatch.setattr(tverify, "SHADOW_ROOT", tmp_path / "no-shadow-here")
    project = tmp_path / "project"
    lock = state.write_lock(project, "1.1.0")
    result = tverify.check_v1(project, tverify._OWN_SKILL_ROOT, lock)
    assert result["ok"] is True, result
    assert "bỏ qua chấm khớp card" in result["msg"]


def test_check_v1_passes_when_card_rules_matches_lock(tmp_path, monkeypatch):
    monkeypatch.setattr(tverify, "SHADOW_ROOT", tmp_path / "no-shadow-here")
    project = tmp_path / "project"
    lock = state.write_lock(project, "1.1.0")
    result = tverify.check_v1(project, tverify._OWN_SKILL_ROOT, lock,
                               card_rules=f"{lock['skill']}@{lock['version']}")
    assert result["ok"] is True, result
    assert "khớp card" in result["msg"]


def test_check_v1_fails_owner_dev_when_card_rules_mismatches_lock(tmp_path, monkeypatch):
    """Spec §11.1 "V1: rules.lock khớp card" — card khai bản khác rules.lock đã
    khoá (vd make_cards.py sinh nhầm card, hoặc project bị khoá version cũ) ⇒
    FAIL, owner_stage "dev" (sự cố hạ tầng/dispatch, không phải lỗi biên tập)."""
    monkeypatch.setattr(tverify, "SHADOW_ROOT", tmp_path / "no-shadow-here")
    project = tmp_path / "project"
    lock = state.write_lock(project, "1.1.0")
    result = tverify.check_v1(project, tverify._OWN_SKILL_ROOT, lock,
                               card_rules="dung-video-talking-head@9.9.9")
    assert result["ok"] is False
    assert result["owner_stage"] == "dev"
    assert "RULES=" in result["msg"]


def test_check_v1_fails_owner_dev_when_release_file_edited_in_place(tmp_path, monkeypatch):
    """C10 (spec §4.3): V1 băm lại từng file của release so với MANIFEST — sửa tại chỗ một
    script sau khi khoá mà không sinh lại MANIFEST ⇒ FAIL owner dev, nêu đúng file (trước đây
    V1 chỉ so sha của chính file MANIFEST nên vẫn PASS)."""
    monkeypatch.setattr(tverify, "SHADOW_ROOT", tmp_path / "no-shadow-here")
    root = tmp_path / "skill"
    rel = root / "releases" / "1.1.0"
    (rel / "scripts").mkdir(parents=True)
    (rel / "rules.json").write_bytes(b'{"version": "1.1.0"}\n')
    (rel / "scripts" / "stage.py").write_bytes(b"print('stage')\n")
    (rel / manifest.MANIFEST_NAME).write_bytes(manifest.build_manifest(rel).encode("utf-8"))
    lock = {"skill": state.SKILL_NAME, "version": "1.1.0",
            "manifest_sha256": manifest.file_sha256(rel / manifest.MANIFEST_NAME)}
    assert tverify.check_v1(tmp_path / "project", root, lock)["ok"] is True

    (rel / "scripts" / "stage.py").write_bytes(b"print('sua tai cho')\n")
    result = tverify.check_v1(tmp_path / "project", root, lock)
    assert result["ok"] is False and result["owner_stage"] == "dev"
    assert (rel / "scripts" / "stage.py").as_posix() in result["msg"]


def _fake_mods(safe_run):
    ns = lambda **kw: type("M", (), {k: staticmethod(v) for k, v in kw.items()})  # noqa: E731
    return {"validate_edit": ns(run=lambda project: ("edit.json", [])),
            "lint_sfx": ns(lint_project=lambda project, post_mux=False: []),
            "check_text_safe": ns(run=safe_run)}


def test_check_v2_routes_text_safe_tool_errors_to_build(tmp_path):
    """B3: check_text_safe hỏng vì công cụ (Remotion/Chrome, node_modules, lock) ⇒ owner BUILD
    (lỗi skill → dev), không phải PLAN; chữ tràn thật (frame FAIL) vẫn owner PLAN."""
    def crash(project):
        raise RuntimeError("remotion still frame 12 lỗi: Chrome crashed")
    got = tverify.check_v2(tmp_path, _fake_mods(crash))
    assert got["ok"] is False and got["owner_stage"] == "BUILD" and "Chrome crashed" in got["msg"]

    def bad_key(project):
        raise KeyError("duration_f")
    assert tverify.check_v2(tmp_path, _fake_mods(bad_key))["owner_stage"] == "BUILD"

    got = tverify.check_v2(tmp_path, _fake_mods(lambda project: [{"frame": 12, "ok": False}]))
    assert got["ok"] is False and got["owner_stage"] == "PLAN"


def test_timeouts_are_not_scored_as_check_failures(tmp_path, monkeypatch):
    """R47: render still của V2 quá hạn (thlib.proc đã giết cả cây) không phải lỗi công cụ của BUILD
    — subprocess.TimeoutExpired đi thẳng qua check_v2 và verify.run để stage.py BLOCK transient."""
    def slow(project):
        raise subprocess.TimeoutExpired(["remotion", "still"], 180)
    with pytest.raises(subprocess.TimeoutExpired):
        tverify.check_v2(tmp_path, _fake_mods(slow))
    project = tmp_path / "project"
    state.write_lock(project, "1.1.0")
    monkeypatch.setattr(tverify, "check_v1", lambda *a: slow(project))
    with pytest.raises(subprocess.TimeoutExpired):
        tverify.run(project, paths.SKILL)


def _verdict_project(tmp_path, verdict="VERIFIED", concerns=()):
    """Dự án đã qua lượt VERIFY tất định: meta.json + out/verify/VERDICT.json (không cần BUILD)."""
    out = tmp_path / "out" / "verify"
    out.mkdir(parents=True)
    (tmp_path / "meta.json").write_text(json.dumps({"video": 2, "guess_count": 0, "script_match": 0.99}),
                                        encoding="utf-8")
    checks = [{"id": f"V{i}", "ok": True, "msg": "ok"} for i in range(1, 8)]
    (out / "VERDICT.json").write_text(json.dumps({"verdict": verdict, "owner_stage": None, "checks": checks,
                                                  "concerns": list(concerns)}), encoding="utf-8")
    return tmp_path


def test_finalize_folds_v7_concern_into_verdict(tmp_path):
    """V7 (§11.1): nhận xét contact sheet của verifier model ở out/verify/v7_concern.txt được
    verify.finalize gộp vào VERDICT.json / VERDICT.md / kpi.json ⇒ DONE_WITH_CONCERNS (bắt buộc
    theo §11.1, và §11.2 đưa video đó cho user). Chạy lại vẫn một concern; không có nhận xét thì
    kết luận giữ nguyên."""
    project = _verdict_project(tmp_path)
    out = project / "out" / "verify"
    assert verify.finalize(project)["verdict"] == "VERIFIED"           # không có file nhận xét
    (out / "v7_concern.txt").write_text("  Khung 7: phụ đề\nche miệng người nói.  \n", encoding="utf-8")
    for _ in range(2):
        got = verify.finalize(project)
    note = verify.V7_PREFIX + "Khung 7: phụ đề che miệng người nói."
    assert got["verdict"] == "DONE_WITH_CONCERNS" and got["concerns"] == [note]
    assert _read(out / "VERDICT.json") == got
    assert note in (out / "VERDICT.md").read_text(encoding="utf-8")
    kpi = _read(out / "kpi.json")
    assert kpi["verdict"] == "DONE_WITH_CONCERNS" and kpi["concerns"] == [note] and kpi["video"] == 2

    (out / "v7_concern.txt").write_text("\n", encoding="utf-8")      # verifier xoá nhận xét
    assert verify.finalize(project)["verdict"] == "VERIFIED"

    other = _verdict_project(tmp_path / "p2", "DONE_WITH_CONCERNS", ["LOW_DENSITY (S26): …"])
    (other / "out" / "verify" / "v7_concern.txt").write_text("Khung 3 tối.", encoding="utf-8")
    assert verify.finalize(other)["concerns"] == ["LOW_DENSITY (S26): …", verify.V7_PREFIX + "Khung 3 tối."]


def test_load_release_modules_rejects_foreign_release_root(tmp_path):
    """release_root khác gốc thlib đang chạy (thlib.verify._OWN_SKILL_ROOT) phải
    FAIL rõ ràng — importlib chưa cách ly được sys.modules['thlib'] khỏi tiến
    trình này, nên âm thầm tiếp tục sẽ chấm nhầm bản (Concern 4, task-13-report.md)."""
    foreign_root = tmp_path / "other-skill-copy"
    foreign_root.mkdir()
    with pytest.raises(RuntimeError, match="khác gốc thlib đang chạy"):
        tverify._load_release_modules(foreign_root, "1.1.0")


def test_load_release_modules_accepts_own_release_root():
    """release_root == gốc thlib đang chạy (mặc định paths.SKILL của CLI) vẫn nạp
    bình thường — chặn foreign root không được phá hành vi single-release hiện tại."""
    mods = tverify._load_release_modules(tverify._OWN_SKILL_ROOT, "1.1.0")
    assert set(mods) == {"validate_edit", "lint_sfx", "check_text_safe", "make_report"}


# ------------------------------------------------------------- e2e (chậm)


@pytest.fixture(scope="module")
def verified_project(tmp_path_factory, rules_110, v3_sections, fixture_v2_words):
    """Dự án video 02 đã BUILD (Task 12) + chuỗi STATE.md provenance mô phỏng
    (stage.py/Task 14 chưa có) cho 6 artifact mà V5 kiểm.

    Cách ly cả `paths.VID_ROOT` (dự án) lẫn `tverify.SHADOW_ROOT` (đường quét
    bản skill che của V1) khỏi máy thật: nếu không, V1 trong 3 e2e test dưới
    đây sẽ quét thẳng vào `C:/Users/Minh PC/AppData/Local/hermes/profiles/**`
    (cây thật, có thể đổi bất cứ lúc nào) thay vì một thư mục tmp trống — dùng
    `yield` thay vì `return` để patch còn hiệu lực suốt vòng đời module-scope
    fixture này (verify.main() gọi lại check_v1, đọc SHADOW_ROOT tại thời điểm
    chạy test, không phải lúc fixture setup)."""
    root = tmp_path_factory.mktemp("vid")
    shadow_root = tmp_path_factory.mktemp("shadow")  # trống — không có bản skill che nào
    with pytest.MonkeyPatch.context() as mp:
        mp.setenv("TH_VID_ROOT", str(root))
        mp.setattr(paths, "VID_ROOT", root)
        mp.setattr(tverify, "SHADOW_ROOT", shadow_root)
        project = paths.project_dir(2, "1.1.0")
        _scaffold(project)
        _intake_core(project, rules_110, v3_sections[2]["script"], fixture_v2_words)
        shutil.copy2(FIXTURES / "v2" / "edit_v11.json", project / "edit.json")
        result = build.run(project, rules_110, "standard")
        assert result["ok"], result
        state.append_state(project, "INTAKE", "t13", "1", "test",
                            [project / "words.json", project / "pauses.json", project / "meta.json"])
        state.append_state(project, "PLAN", "t13", "1", "test", [project / "edit.json"])
        state.append_state(project, "BUILD", "t13", "1", "test",
                            [project / "picture_lock.json", project / "out" / "sfx_plan.json"])
        yield project


@pytest.mark.slow
def test_verify_happy_path_all_checks_pass(verified_project):
    project = verified_project
    rc = verify.main([str(project)])
    verdict = _read(project / "out" / "verify" / "VERDICT.json")
    assert rc == 0, verdict
    assert verdict["owner_stage"] is None
    assert [c["id"] for c in verdict["checks"]] == ["V1", "V2", "V3", "V4", "V5", "V6", "V7"]
    assert all(c["ok"] for c in verdict["checks"]), verdict["checks"]
    # Fix round 2 (finding 1): ghép contact sheet thành công không còn tự bịa
    # CONCERN placeholder, nên một BUILD sạch đạt thẳng VERIFIED (trước đây
    # luôn kẹt ở DONE_WITH_CONCERNS vì V7 luôn nhét một CONCERN giả).
    assert verdict["verdict"] == "VERIFIED", verdict
    assert verdict["concerns"] == []
    assert (project / "out" / "verify" / "contact_sheet.png").is_file()
    assert (project / "out" / "verify" / "VERDICT.md").is_file()
    kpi = _read(project / "out" / "verify" / "kpi.json")
    assert kpi["video"] == 2 and kpi["verdict"] == verdict["verdict"]


@pytest.mark.slow
def test_verify_tampered_edit_json_rejects_owner_plan(verified_project):
    """Task 13 brief: sửa 1 byte vô hại (thêm khoảng trắng, JSON không đổi
    nghĩa) trong edit.json — validate_edit/lint_sfx vẫn PASS, chỉ V5 (sha8 so
    với STATE.md) phát hiện lệch ⇒ REJECTED, owner_stage PLAN."""
    project = verified_project
    edit_path = project / "edit.json"
    original = edit_path.read_bytes()
    try:
        text = original.decode("utf-8")
        assert text.startswith("{")
        tampered = "{ " + text[1:]
        assert json.loads(tampered) == json.loads(text)          # JSON không đổi nghĩa
        edit_path.write_text(tampered, encoding="utf-8")

        rc = verify.main([str(project)])
        verdict = _read(project / "out" / "verify" / "VERDICT.json")
        assert rc == 1
        assert verdict["verdict"] == "REJECTED"
        assert verdict["owner_stage"] == "PLAN"
        by_id = {c["id"]: c for c in verdict["checks"]}
        assert by_id["V5"]["ok"] is False and "edit.json" in by_id["V5"]["msg"]
    finally:
        edit_path.write_bytes(original)


@pytest.mark.slow
def test_verify_missing_final_nobgm_rejects_owner_build(verified_project):
    """delete final-nobgm.mp4 ⇒ V4 (loudness, file thiếu) và L11 trong V2
    (lint_sfx --post-mux) đều FAIL ⇒ REJECTED, owner_stage BUILD."""
    project = verified_project
    nobgm = project / "out" / "final-nobgm.mp4"
    backup = project / "out" / "_final-nobgm.mp4.bak"
    nobgm.rename(backup)
    try:
        rc = verify.main([str(project)])
        verdict = _read(project / "out" / "verify" / "VERDICT.json")
        assert rc == 1
        assert verdict["verdict"] == "REJECTED"
        assert verdict["owner_stage"] == "BUILD"
        by_id = {c["id"]: c for c in verdict["checks"]}
        assert by_id["V4"]["ok"] is False
        assert by_id["V2"]["ok"] is False
    finally:
        backup.rename(nobgm)
