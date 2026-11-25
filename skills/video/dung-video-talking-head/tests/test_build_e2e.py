# tests/test_build_e2e.py — BUILD thật của video 02 (Task 12; chậm: text-safe + render ≈ vài phút).
# Dự án tạm dưới tmp (TH_VID_ROOT → tmp, không đụng Vid Heygen): scaffold của stage.py (template
# 1.1.0 + font 1.0.0 R17 + npm install, master 1620×2880 từ 2.mp4 thật, chỉ đọc), INTAKE lõi của
# stage.py (vo_clear, align lời v3 với từ whisper large-v3 đã lưu của video 02, khoảng ngắt /
# onset / VO_REF / nhịp ngắt), edit_v11.json làm output PLAN, rồi build.run.
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

import make_report
import stage
from thlib import audio as A, build, lint, loud, mix, paths, state

FIXTURES = Path(__file__).parent / "fixtures"
SOURCE = Path("D:/MMO/Van Minh AI/Vid Heygen/2/2.mp4")      # nguồn thật, chỉ đọc
PRE_CODES = ["L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8", "L9", "L10", "L12", "L13", "L14"]
TARGETS = (("final.mp4", "final_lufs"), ("final-nobgm.mp4", "final_lufs"),
           ("final-social.mp4", "social_lufs"))


def _read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _scaffold(project):
    """Scaffold production của INTAKE (stage.scaffold, Task 14): template 1.1.0, bộ font 1.0.0,
    rules.lock, master 1620×2880, npm install."""
    stage.scaffold(project, SOURCE, "1.1.0")


def _intake_core(project, R, script, whisper_words):
    """INTAKE lõi của stage.py trên nguồn thật, nhưng dùng từ whisper large-v3 đã lưu thay vì chạy
    whisper: vo-clean.wav, words.json (lời v3 + mốc whisper + on), pauses.json, vo_script.txt,
    meta.json đúng Data Contracts."""
    stage.intake_core(project, SOURCE, R, 2, "standard", script, lambda _wav: whisper_words,
                      {"broll_class": "none", "claim_gate": False})


@pytest.fixture(scope="module")
def v2_build(tmp_path_factory, rules_110, v3_sections, fixture_v2_words):
    """(dự án, kết quả build.run) của video 02, dựng một lần cho cả module."""
    root = tmp_path_factory.mktemp("vid")
    with pytest.MonkeyPatch.context() as mp:
        mp.setenv("TH_VID_ROOT", str(root))
        mp.setattr(paths, "VID_ROOT", root)
        project = paths.project_dir(2, "1.1.0")
        _scaffold(project)
        _intake_core(project, rules_110, v3_sections[2]["script"], fixture_v2_words)
        shutil.copy2(FIXTURES / "v2" / "edit_v11.json", project / "edit.json")
        result = build.run(project, rules_110, "standard")
    return project, result


def _video_packets(path):
    """Số packet (frame) của luồng hình."""
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets",
                          "-show_entries", "stream=nb_read_packets", "-of", "default=nw=1:nk=1", str(path)],
                         capture_output=True, text=True, check=True).stdout
    return int(out.split()[0])


@pytest.mark.slow
def test_build_video2_end_to_end(v2_build, rules_110):
    """build.run ok; ba bản xuất dài duration_f/30 ± 1 f; QA.json xcorr ≤ 2 ms, mọi cue lệch
    −1/+2 f; final / nobgm −16 ± 0,5, social −14 ± 0,5, TP ≤ −1,5 (đo lại ở đây); lint đủ 14 mã
    PASS; EDITOR-REPORT đủ mục. Gate 9 đã chọn 4 bài ⇒ video 02 có bed của bài select_bgm(2),
    L12 chấm mức bed (không phải "không có nhạc nền") và mix.wav khác mix-nobgm.wav."""
    project, result = v2_build
    assert result["ok"] is True and result["failed_gate"] is None, result
    out, fps = project / "out", rules_110.get("fps")
    lock = _read(project / "picture_lock.json")
    want_s = lock["duration_f"] / fps
    L = rules_110.get("loudness")
    for name, key in TARGETS:
        x = A.decode(out / name)
        assert abs(len(x) / A.SR - want_s) <= 1 / fps, name
        assert abs(_video_packets(out / name) - lock["duration_f"]) <= 1, name
        assert abs(A.integrated_lufs(x) - L[key]) <= L["tol_lu"], name
        assert max(A.true_peak_db(x[:, ch]) for ch in range(x.shape[1])) <= L["tp_dbtp"], name

    qa, plan = _read(out / "QA.json"), _read(out / "sfx_plan.json")
    for name, _ in TARGETS:                  # R35: vòng mã hoá–đo–hạ trần, trần đầu TP đích − 0,5 dB
        got = qa["outputs"][name]
        print("QA %-17s %6.2f LUFS  TP %6.2f dBTP  lần %d  trần %.2f dBTP"
              % (name, got["lufs"], got["tp_dbtp"], got["attempts"], got["ceiling_dbtp"]))
        assert 1 <= got["attempts"] <= loud.TP_TRIES, name
        assert got["ceiling_dbtp"] <= L["tp_dbtp"] - loud.LIMIT_MARGIN_DB + 1e-9, name
    assert abs(qa["xcorr_ms"]) <= rules_110.get("xcorr_max_ms")
    assert plan["cues"] and [c["id"] for c in qa["cues"]] == [c["id"] for c in plan["cues"]]
    assert all(-1 <= c["offset_f"] <= 2 for c in qa["cues"]), qa["cues"]

    results = _read(out / "sfx_lint.json")
    assert [r["code"] for r in results] == PRE_CODES + ["L11"]
    assert all(r["ok"] for r in results), [r for r in results if not r["ok"]]
    report = (out / "EDITOR-REPORT.md").read_text(encoding="utf-8")
    assert [ln for ln in report.splitlines() if ln.startswith("## ")] == list(make_report.SECTIONS)
    pub = project / "public"
    assert mix.select_bgm("1.1.0", 2) is not None
    assert (pub / "bgm_bed.wav").exists()
    l12 = next(r for r in results if r["code"] == "L12")
    assert l12["msg"].startswith("bed "), l12
    print("L12", l12["msg"])
    assert (pub / "mix.wav").read_bytes() != (pub / "mix-nobgm.wav").read_bytes()
    assert "- Nhạc nền: có" in report


@pytest.mark.slow
def test_lint_sfx_in_separate_process_reproduces_plan(v2_build):
    """S21 giữa hai process: lint_sfx.py --post-mux chạy planner lại ở một process Python
    khác trên dự án vừa dựng ⇒ L10 PASS với đúng sha của sfx_plan.json BUILD ghi (file ghi
    đúng chuỗi JSON chuẩn nên sha file = sha plan), và sfx_lint.json ra y từng byte."""
    project, result = v2_build
    assert result["ok"] is True, result
    plan_file, lint_file = project / "out" / "sfx_plan.json", project / "out" / "sfx_lint.json"
    sha = lint.plan_sha256(_read(plan_file))
    assert state.sha256_file(plan_file) == sha
    built = lint_file.read_bytes()
    run = subprocess.run([sys.executable, str(paths.release_dir("1.1.0") / "scripts" / "lint_sfx.py"),
                          str(project), "--post-mux"], capture_output=True, text=True, encoding="utf-8",
                         errors="replace", env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    assert run.returncode == 0, run.stdout + run.stderr
    l10 = next(r for r in _read(lint_file) if r["code"] == "L10")
    assert l10["ok"] and sha[:12] in l10["msg"], l10
    assert lint_file.read_bytes() == built
