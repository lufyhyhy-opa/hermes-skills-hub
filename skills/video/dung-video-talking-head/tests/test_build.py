# tests/test_build.py — stage BUILD (Task 12): render_video.py, mux.py, make_report.py và
# thứ tự cổng của thlib.build.run. Hai bước cần Remotion (text-safe, render hình) được
# thay bằng bản giả ở đây; bản render thật nằm ở test_build_e2e.py (chậm).
import json
import subprocess
from pathlib import Path

import numpy as np
import pytest
from scipy.signal import butter, sosfilt

import make_report
import mux
import render_video
from thlib import audio as A, build, lint, loud, mix, state, voice

PRE_CODES = ["L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8", "L9", "L10", "L12", "L13", "L14"]
FINALS = ("final.mp4", "final-nobgm.mp4", "final-social.mp4")


def _write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def _read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _black_video(path, frames, fps=30):
    """Hình đen 64×64 dài đúng `frames` frame — thay bản render Remotion."""
    path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=black:s=64x64:r={fps}",
                    "-frames:v", str(frames), "-c:v", "libx264", "-pix_fmt", "yuv420p", str(path)],
                   check=True, capture_output=True)


def _sample_rate(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
                          "stream=sample_rate", "-of", "default=nw=1:nk=1", str(path)],
                         capture_output=True, text=True, check=True).stdout
    return int(out.split()[0])


def _video_packets(path):
    """Số packet (frame) của luồng hình."""
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets",
                          "-show_entries", "stream=nb_read_packets", "-of", "default=nw=1:nk=1", str(path)],
                         capture_output=True, text=True, check=True).stdout
    return int(out.split()[0])


# ------------------------------------------------ render_video.py


def _fake_remotion(project, calls, code=0, write=True):
    remotion = project / "node_modules" / ".bin" / render_video.bin_name("remotion")
    remotion.parent.mkdir(parents=True, exist_ok=True)
    remotion.write_text("")

    def fake_run(args, **kw):
        calls.append((args, kw))
        if write:
            (project / "out" / "_video.mp4").write_bytes(b"hinh")
        return subprocess.CompletedProcess(args, code)
    return remotion, fake_run


def test_render_video_renders_picture_only(tmp_path, monkeypatch, capsys):
    """Đường render duy nhất: `remotion render src/index.ts Main out/_video.mp4 --muted
    --concurrency=4 --crf=18` trong thư mục dự án (tiếng ghép sau bằng ffmpeg — S25)."""
    calls = []
    remotion, fake_run = _fake_remotion(tmp_path, calls)
    monkeypatch.setattr(render_video.proc, "run", fake_run)
    assert render_video.main([str(tmp_path)]) == 0
    (args, kw), = calls
    assert args == [str(remotion), "render", "src/index.ts", "Main", "out/_video.mp4",
                    "--muted", "--concurrency=4", "--crf=18"]
    assert kw["cwd"] == tmp_path and kw["timeout"] == 1200      # R47: render hình tối đa 1200 s
    assert capsys.readouterr().out.splitlines()[-1].startswith("KẾT QUẢ: PASS")


def test_render_video_timeout_exits_timeout_code(tmp_path, monkeypatch, capsys):
    """R47: Remotion render quá hạn (cả cây đã bị giết) ⇒ mã proc.TIMEOUT_EXIT, không để hình dở."""
    _fake_remotion(tmp_path, [])

    def slow(args, **kw):
        (tmp_path / "out" / "_video.mp4").write_bytes(b"do dang")
        raise subprocess.TimeoutExpired(args, kw["timeout"])
    monkeypatch.setattr(render_video.proc, "run", slow)
    assert render_video.main([str(tmp_path)]) == render_video.proc.TIMEOUT_EXIT
    assert "1200" in capsys.readouterr().out and not (tmp_path / "out" / "_video.mp4").exists()


def test_render_video_failures(tmp_path, monkeypatch, capsys):
    """Chưa npm install ⇒ mã 1 kèm lời nhắc; Remotion lỗi ⇒ mã 1 và không để lại
    out/_video.mp4 cũ cho mux ghép nhầm."""
    assert render_video.main([str(tmp_path)]) == 1
    assert "npm install" in capsys.readouterr().out

    calls = []
    _, fake_run = _fake_remotion(tmp_path, calls, code=1, write=False)
    stale = tmp_path / "out" / "_video.mp4"
    stale.parent.mkdir(parents=True)
    stale.write_bytes(b"ban cu")
    monkeypatch.setattr(render_video.proc, "run", fake_run)
    assert render_video.main([str(tmp_path)]) == 1
    assert not stale.exists() and "FAIL" in capsys.readouterr().out


# ------------------------------------------------ mux.py


def _band(n, amp, seed):
    """Nhiễu dải 100 Hz–4 kHz (như giọng: AAC không cắt mất năng lượng cao tần)."""
    sos = butter(4, (100, 4000), btype="bandpass", fs=A.SR, output="sos")
    return amp * sosfilt(sos, np.random.default_rng(seed).standard_normal(n))


MIX_LOOPS = {"mix.wav": {"attempts": 2, "ceiling_dbtp": -2.4},          # bản ghi vòng R35 của cổng mix
             "mix-nobgm.wav": {"attempts": 1, "ceiling_dbtp": -2.0}}


def _mux_project(root, R, late_f=0):
    """Dự án 8 s tổng hợp, sẵn sàng mux: giọng 0,2–3,5 s và 4,2–7,0 s, một cue chuyển
    đoạn plan xếp ở 3,6 s (sfx_stem.wav đúng chỗ đó); mix / mix-nobgm đã loudnorm −16
    nhưng trộn cue trễ `late_f` frame, out/mix_loudness.json = MIX_LOOPS (cổng mix ghi);
    out/_video.mp4 đen dài duration_f frame."""
    dur, fps = 8.0, R.get("fps")
    vo = np.zeros(int(dur * A.SR))
    for k, (a, b) in enumerate(((0.2, 3.5), (4.2, 7.0))):
        vo[int(a * A.SR): int(b * A.SR)] = _band(int(b * A.SR) - int(a * A.SR), 0.2, k)
    n = int(0.3 * A.SR)
    cue = _band(n, 0.1, 9) * np.linspace(1, 0, n) ** 2
    found = voice.find_pauses(vo, R)
    t_end = min(voice.last_word_end([{"e": 7.0}], found, dur) + R.get("end.pad_s"), dur)
    state.write_lock(root, "1.1.0")
    (root / "public").mkdir()
    A.write_wav(root / "public" / "sfx_stem.wav",
                mix.render_stem([{"start_s": 3.6, "samples": cue}], len(vo)))
    late = mix.render_stem([{"start_s": 3.6 + late_f / fps, "samples": cue}], len(vo))
    A.write_wav(root / "raw.wav", mix.mixdown(np.stack([vo, vo], axis=1), late, None, t_end, R))
    for wav in ("mix.wav", "mix-nobgm.wav"):
        mix.loudnorm_file(root / "raw.wav", root / "public" / wav, -16.0, -1.5)
    _write_json(root / "out" / "mix_loudness.json", MIX_LOOPS)
    peak = 3.6 + int(np.argmax(np.abs(cue))) / A.SR
    _write_json(root / "out" / "sfx_plan.json", {"cues": [
        {"id": "section@w3", "role": "section", "tier": "B", "mode": "pre", "frame": round(peak * fps),
         "peak_s": round(peak, 4), "start_s": 3.6, "end_s": round(3.6 + n / A.SR, 4)}]})
    _black_video(root / "out" / "_video.mp4", round(t_end * fps), fps)
    return t_end


def test_mux_writes_three_outputs_and_qa(tmp_path, rules_110, capsys):
    """final / final-nobgm ghép mix đã chuẩn hoá, social loudnorm mix.wav về −14;
    QA.json: xcorr(mix, final), lệch từng cue, loudness + TP + độ dài ba bản xuất và bản ghi
    vòng R35 của từng bản (số lần, trần limiter cuối — final/nobgm lấy từ cổng mix)."""
    t_end = _mux_project(tmp_path, rules_110)
    assert mux.main([str(tmp_path)]) == 0
    out = tmp_path / "out"
    qa = _read(out / "QA.json")
    assert abs(qa["xcorr_ms"]) <= 2.0
    (cue,) = qa["cues"]
    assert cue["id"] == "section@w3" and abs(cue["offset_f"]) <= 0.1
    frames = _video_packets(out / "_video.mp4")
    for name, target in zip(FINALS, (-16.0, -16.0, -14.0)):
        x, got = A.decode(out / name), qa["outputs"][name]
        assert abs(got["lufs"] - target) <= 0.5 and got["tp_dbtp"] <= -1.5, (name, got)
        assert abs(got["lufs"] - A.integrated_lufs(x)) <= 0.01, name        # đo đúng file đã ghi
        assert abs(got["duration_s"] - t_end) <= 1 / 30, name
        assert _sample_rate(out / name) == A.SR
        assert _video_packets(out / name) == frames, name                   # hình giữ đủ mọi frame
    for name, wav in (("final.mp4", "mix.wav"), ("final-nobgm.mp4", "mix-nobgm.wav")):
        got = qa["outputs"][name]
        assert {k: got[k] for k in ("attempts", "ceiling_dbtp")} == MIX_LOOPS[wav], name
    social = qa["outputs"]["final-social.mp4"]
    assert 1 <= social["attempts"] <= loud.TP_TRIES and social["ceiling_dbtp"] <= -2.0   # ≤ TP đích − 0,5
    assert "social_margin_db" not in qa                                      # thay bằng bản ghi mỗi bản xuất
    assert not (out / "_social.wav").exists()                                # file tạm đã dọn
    assert capsys.readouterr().out.splitlines()[-1].startswith("KẾT QUẢ:")


def test_mux_qa_measures_cue_offset_on_final(tmp_path, rules_110):
    """Lệch cue đo trên tiếng final so với chỗ plan xếp (đoạn mẫu lấy từ sfx_stem.wav),
    không so với mix: mix trộn cue trễ 2 f ⇒ xcorr(mix, final) vẫn ≈ 0, cue lệch +2 f."""
    _mux_project(tmp_path, rules_110, late_f=2)
    assert mux.main([str(tmp_path)]) == 0
    qa = _read(tmp_path / "out" / "QA.json")
    assert abs(qa["xcorr_ms"]) <= 2.0
    assert abs(qa["cues"][0]["offset_f"] - 2) <= 0.1


def test_mux_social_from_lossless_mix_with_encode_loop(tmp_path, rules_110, monkeypatch):
    """R35: social làm từ public/mix.wav (lossless — không phải tiếng AAC của final.mp4) qua vòng dùng
    chung mix.loudnorm_encoded: loudnorm −14 với limiter true-peak 4× ở trần TP đích − 0,5, ghép
    đúng lệnh của final (-shortest), TP đo trên final-social.mp4 đã mã hoá; còn vượt thì hạ trần
    phần vượt + 0,1 dB rồi làm lại. QA.json ghi số lần + trần cuối. Hết TP_TRIES lần vẫn vượt: mux
    vẫn ghi QA với bản cuối — cổng hỏng là L11 như trước."""
    _mux_project(tmp_path, rules_110)
    out = tmp_path / "out"
    loops, stages, cmds, measured_on = [], [], [], []
    real_loop, real_loudnorm, real_ffmpeg = mix.loudnorm_encoded, mix.loudnorm_file, mux.ffmpeg

    def spy_loop(src, wav, target, tp, encode):
        loops.append((Path(src).relative_to(tmp_path).as_posix(), Path(wav).name, target, tp))
        return real_loop(src, wav, target, tp, encode)

    def spy_loudnorm(src, dst, target, tp, margin_db, oversample):
        stages.append((Path(src).name, round(margin_db, 6), oversample))
        return real_loudnorm(src, dst, target, tp, margin_db, oversample)

    def spy_tp(path):
        measured_on.append(Path(path).name)
        return next(measured)
    measured = iter([-1.2, -1.9])
    monkeypatch.setattr(mix, "loudnorm_encoded", spy_loop)
    monkeypatch.setattr(mix, "loudnorm_file", spy_loudnorm)
    monkeypatch.setattr(mix, "encoded_tp", spy_tp)
    monkeypatch.setattr(mux, "ffmpeg", lambda args: cmds.append(args) or real_ffmpeg(args))
    assert mux.main([str(tmp_path)]) == 0
    assert loops == [("public/mix.wav", "_social.wav", -14.0, -1.5)]        # một vòng dùng chung
    assert stages == [("mix.wav", 0.5, 4), ("mix.wav", 0.9, 4)]
    assert measured_on == ["final-social.mp4"] * 2                           # đo bản đã mã hoá
    social_cmds = [c for c in cmds if c[-1] == str(out / "final-social.mp4")]
    assert social_cmds == 2 * [["-y", "-i", str(out / "_video.mp4"), "-i", str(out / "_social.wav"),
                                "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a",
                                "192k", "-ar", "48000", "-shortest", str(out / "final-social.mp4")]]
    social = _read(out / "QA.json")["outputs"]["final-social.mp4"]
    assert social["attempts"] == 2 and social["ceiling_dbtp"] == -2.4

    stages.clear()
    measured = iter([-1.0, -1.1, -1.2])                      # không đạt: dừng sau TP_TRIES lần
    assert mux.main([str(tmp_path)]) == 0                    # mux chỉ đo; L11 sẽ FAIL
    assert [s[1] for s in stages] == [0.5, 1.1, 1.6] and len(stages) == loud.TP_TRIES
    social = _read(out / "QA.json")["outputs"]["final-social.mp4"]
    assert social["attempts"] == 3 and social["ceiling_dbtp"] == -3.1
    assert (out / "final-social.mp4").is_file() and not (out / "_social.wav").exists()


def test_mux_missing_video(tmp_path, capsys):
    state.write_lock(tmp_path, "1.1.0")
    assert mux.main([str(tmp_path)]) == 1
    assert "_video.mp4" in capsys.readouterr().out


def test_mux_needs_mix_loop_record(tmp_path, rules_110, capsys):
    """final / nobgm không tự làm vòng R35 (cổng mix đã làm): thiếu bản ghi của cổng mix ⇒ mã 1."""
    _mux_project(tmp_path, rules_110)
    (tmp_path / "out" / "mix_loudness.json").unlink()
    assert mux.main([str(tmp_path)]) == 1
    assert "mix_loudness.json" in capsys.readouterr().out


# ------------------------------------------------ make_report.py


def _report_project(root):
    """Dự án đủ đầu vào của make_report (số liệu giả, đúng dạng contract)."""
    state.write_lock(root, "1.1.0")
    _write_json(root / "meta.json", {"video": 2, "preset": "standard", "script_match": 0.8765,
                                     "guess_count": 1, "broll_class": "light", "claim_gate": True})
    _write_json(root / "words.json", [
        {"i": 0, "w": "Hôm", "s": 0.27, "e": 0.41, "on": 0.27, "src": "script", "guess": False},
        {"i": 1, "w": "nayy", "s": 0.41, "e": 0.62, "on": 0.43, "src": "asr", "guess": True}])
    _write_json(root / "picture_lock.json", {
        "fps": 30, "duration_f": 60, "t_end": 2.0, "warnings": ["LAST_WORD_TIGHT:b01"],
        "blocks": [{"id": "b01", "top": [], "bottom": [],
                    "hero": [{"t": "Hôm", "show": 0.22},
                             {"t": "nayy", "show": 0.5, "display_shift_s": 0.12}]}]})
    ok_cue = {"file": "impact/hit-blow", "mode": "pre", "pause": [0.62, 1.0], "frame": 25, "peak_s": 0.8333,
              "start_s": 0.7, "end_s": 0.95, "gain_db": -3.1, "fade_loss_db": 0.2, "short_db": 0.0,
              "target_db": -4.0, "levels": {"phone_k": -4.0305, "k": -3.3891, "phone_a": -5.8441}}
    _write_json(root / "out" / "sfx_plan.json", {
        "rules_version": "1.1.0", "preset": "standard", "budget": 3,
        "candidates": [
            {"id": "hook@w1", "role": "hook", "tier": "A", "rank": 1, "source": "hook", "anchor_word": 1,
             "decision": "OK", "rule": None, "tried": [], "cue": ok_cue},
            {"id": "card@w9", "role": "card", "tier": "B", "rank": 3, "source": "steps", "anchor_word": 9,
             "decision": "BỎ", "rule": "S07", "tried": [], "cue": None}],
        "cues": [{"id": "hook@w1", "role": "hook", "tier": "A", **ok_cue}],
        "warnings": ["LOW_DENSITY:10.00-16.00"]})
    _write_json(root / "out" / "sfx_lint.json", [
        {"code": "L4", "ok": True, "frame": None, "msg": "ngân sách 1/3 | WARN LOW_DENSITY:10.00-16.00"},
        {"code": "L11", "ok": False, "frame": 25, "msg": "hook@w1: trên final lệch +3.00 f"}])
    _write_json(root / "out" / "QA.json", {
        "xcorr_ms": -0.021, "cues": [{"id": "hook@w1", "role": "hook", "frame": 25, "offset_f": 0.0}],
        "outputs": {"final.mp4": {"lufs": -16.02, "tp_dbtp": -1.93, "duration_s": 2.0, "attempts": 1,
                                  "ceiling_dbtp": -2.0},
                    "final-nobgm.mp4": {"lufs": -16.01, "tp_dbtp": -1.95, "duration_s": 2.0, "attempts": 1,
                                        "ceiling_dbtp": -2.0},
                    "final-social.mp4": {"lufs": -14.03, "tp_dbtp": -1.71, "duration_s": 2.0, "attempts": 2,
                                         "ceiling_dbtp": -3.23}}})


def test_make_report_writes_every_section(tmp_path):
    """EDITOR-REPORT: đường dẫn, loudness ba bản, đồng bộ, mọi ứng viên sfx_plan (id, vai,
    tầng, quyết định, luật, đỉnh, file, mức 3 miền), lint, độ khớp + mọi từ guess, cảnh báo
    SFX cạnh cảnh báo khoá hình (LAST_WORD_TIGHT, display_shift_s — R31), claim gate, B-roll."""
    _report_project(tmp_path)
    assert make_report.main([str(tmp_path)]) == 0
    text = (tmp_path / "out" / "EDITOR-REPORT.md").read_text(encoding="utf-8")
    heads = [ln for ln in text.splitlines() if ln.startswith("## ")]
    assert heads == list(make_report.SECTIONS)
    for piece in ("final-social.mp4", "-16.02", "-1.93", "-14.03",            # loudness
                  "| 1 | -2.00 |", "| 2 | -3.23 |",                            # số lần + trần mỗi bản (R35)
                  "-0.021", "hook@w1",                                         # đồng bộ
                  "card@w9", "BỎ", "S07", "impact/hit-blow", "0.8333", "-4.03", "-3.39", "-5.84",
                  "L11", "FAIL", "lệch +3.00 f",                               # lint
                  "0.8765", "nayy",                                            # lời chuẩn
                  "LOW_DENSITY:10.00-16.00", "LAST_WORD_TIGHT:b01", "+0.120",  # cảnh báo
                  "light"):
        assert piece in text, piece
    assert "1/3 \\| WARN" in text                      # '|' trong msg lint không vỡ bảng
    claim = text.split("## Claim gate", 1)[1].split("## ", 1)[0]
    assert "**có**" in claim


def test_make_report_needs_inputs(tmp_path, capsys):
    _report_project(tmp_path)
    (tmp_path / "out" / "QA.json").unlink()
    assert make_report.main([str(tmp_path)]) == 1
    assert "QA.json" in capsys.readouterr().out


# ------------------------------------------------ build.run (Remotion giả)


def _v2_project(root, vo, words, pauses, edit):
    """Dự án video 02 đã xong INTAKE + PLAN: rules.lock, public/vo-clean.wav (stereo),
    words/pauses/edit/meta.json, src/data/ (script.ts do BUILD sinh)."""
    proj = root / "2" / "edit-r1.1.0"
    state.write_lock(proj, "1.1.0")
    (proj / "public").mkdir()
    (proj / "src" / "data").mkdir(parents=True)
    A.write_wav(proj / "public" / "vo-clean.wav", np.stack([vo, vo], axis=1))
    for name, obj in (("words.json", words), ("pauses.json", pauses), ("edit.json", edit),
                      ("meta.json", {"video": 2, "preset": "standard", "script_match": 0.99, "guess_count": 0,
                                     "broll_class": "none", "claim_gate": False})):
        _write_json(proj / name, obj)
    return proj


def _fake_scripts(real, calls, fail=None):
    """Thay hai script cần Remotion: text-safe đạt (ghi text_safe.json), render = hình đen dài
    duration_f; mux.py và make_report.py chạy thật. `fail` = script giả vờ hỏng."""
    def fake(project, name):
        calls.append(name)
        if name == fail:
            raise build.BuildError("%s (giả) thoát mã 1" % name)
        if name == "check_text_safe.py":
            _write_json(project / "out" / "safe" / "text_safe.json", [])
            return "KẾT QUẢ: PASS (giả)"
        if name == "render_video.py":
            _black_video(project / "out" / "_video.mp4", _read(project / "picture_lock.json")["duration_f"])
            return "KẾT QUẢ: PASS (giả)"
        return real(project, name)
    return fake


def _names(artifacts, proj):
    return [Path(a).relative_to(proj).as_posix() for a in artifacts]


def test_build_stops_at_first_failed_gate(tmp_path, monkeypatch, v2_vo_mono, fixture_v2_words_corrected,
                                          fixture_v2_pauses_full, v2_edit_v11, rules_110):
    """Cổng hỏng đầu tiên dừng BUILD: text-safe FAIL ⇒ failed_gate text_safe, chỉ còn các file
    đã ghi trước đó; stem chưa được ghi. sfx_plan.json ghi đúng chuỗi JSON chuẩn mà
    lint.plan_sha256 băm (sha file = sha plan — S21)."""
    proj = _v2_project(tmp_path, v2_vo_mono, fixture_v2_words_corrected, fixture_v2_pauses_full, v2_edit_v11)
    calls = []
    monkeypatch.setattr(build, "_script", _fake_scripts(build._script, calls, fail="check_text_safe.py"))
    got = build.run(proj, rules_110, "standard")
    assert got["ok"] is False and got["failed_gate"] == "text_safe"
    assert _names(got["artifacts"], proj) == ["out/sfx_plan.json", "picture_lock.json", "src/data/script.ts"]
    assert calls == ["check_text_safe.py"]
    assert not (proj / "public" / "sfx_stem.wav").exists()
    plan_file = proj / "out" / "sfx_plan.json"
    assert state.sha256_file(plan_file) == lint.plan_sha256(_read(plan_file))


def test_script_exit_2_is_a_tool_error(tmp_path, monkeypatch):
    """B3: script của release thoát mã 2 = lỗi công cụ (ToolError, dev); mã 1 = cổng không
    đạt (BuildError thường — với text_safe là chữ tràn, owner PLAN/template)."""
    for code, tool in ((2, True), (1, False)):
        monkeypatch.setattr(build.proc, "run",
                            lambda *a, code=code, **kw: subprocess.CompletedProcess(a[0], code, "log", ""))
        with pytest.raises(build.BuildError) as got:
            build._script(tmp_path, "check_text_safe.py")
        assert isinstance(got.value, build.ToolError) is tool, code


def test_script_timeouts_surface_as_timeout_expired(tmp_path, monkeypatch, rules_110):
    """R47: script render_video.py có trần 1200 s ở build.py; script quá hạn (thlib.proc giết cả
    cây) hoặc thoát mã proc.TIMEOUT_EXIT ⇒ subprocess.TimeoutExpired đi thẳng qua build.run (không
    thành cổng hỏng) để stage.py BLOCK transient."""
    seen = {}

    def fake(args, **kw):
        seen[Path(args[1]).name] = kw["timeout"]
        return subprocess.CompletedProcess(args, build.proc.TIMEOUT_EXIT, "quá hạn", "")
    monkeypatch.setattr(build.proc, "run", fake)
    for name in ("render_video.py", "check_text_safe.py"):
        with pytest.raises(subprocess.TimeoutExpired):
            build._script(tmp_path, name)
    assert seen == {"render_video.py": 1200, "check_text_safe.py": None}   # text-safe: mỗi still tự có trần

    def outer(args, **kw):
        raise subprocess.TimeoutExpired(args, kw["timeout"])
    monkeypatch.setattr(build.proc, "run", outer)
    with pytest.raises(subprocess.TimeoutExpired):
        build._script(tmp_path, "render_video.py")

    def slow(s):
        raise subprocess.TimeoutExpired(["render_video.py"], 1200)
    monkeypatch.setattr(build, "_STEPS", (("render", slow),))
    with pytest.raises(subprocess.TimeoutExpired):
        build.run(tmp_path, rules_110, "standard")


def test_build_flags_text_safe_tool_error(tmp_path, monkeypatch, v2_vo_mono, fixture_v2_words_corrected,
                                          fixture_v2_pauses_full, v2_edit_v11, rules_110):
    """B3: build.run báo tool_error — True khi cổng hỏng vì công cụ (ToolError, lỗi chương
    trình), False khi cổng không đạt thật — để stage.py chuyển đúng owner."""
    proj = _v2_project(tmp_path, v2_vo_mono, fixture_v2_words_corrected, fixture_v2_pauses_full, v2_edit_v11)

    def tool_fail(project, name):
        raise build.ToolError("check_text_safe.py thoát mã 2: LỖI CÔNG CỤ (giả)")
    monkeypatch.setattr(build, "_script", tool_fail)
    got = build.run(proj, rules_110, "standard")
    assert (got["failed_gate"], got["tool_error"]) == ("text_safe", True)

    monkeypatch.setattr(build, "_script", _fake_scripts(build._script, [], fail="check_text_safe.py"))
    got = build.run(proj, rules_110, "standard")
    assert (got["failed_gate"], got["tool_error"]) == ("text_safe", False)

    def crash(project, name):
        raise OSError("không chạy được python con")
    monkeypatch.setattr(build, "_script", crash)
    got = build.run(proj, rules_110, "standard")
    assert (got["failed_gate"], got["tool_error"]) == ("text_safe", True)


def test_build_runs_every_gate_with_bed(tmp_path, monkeypatch, v2_vo_mono, fixture_v2_words_corrected,
                                        fixture_v2_pauses_full, v2_edit_v11, rules_110):
    """Đủ cổng theo thứ tự R27 khi đã chọn nhạc nền: stem + bed → lint trước mux (13 mã, L10
    so với sha planner — không BỎ QUA) → mix / mix-nobgm → render (giả) → mux → L11 → report;
    sfx_lint.json cuối có đủ 14 mã, bed đạt L12, mix có bed khác mix-nobgm. Bản AAC thử đầu của
    mix.wav bị ép vượt TP ⇒ vòng R35 làm lại mix.wav với trần hạ, bản ghi (số lần, trần) đi tới
    QA.json của final.mp4; social làm từ mix.wav (có bed)."""
    proj = _v2_project(tmp_path, v2_vo_mono, fixture_v2_words_corrected, fixture_v2_pauses_full, v2_edit_v11)
    monkeypatch.setattr(build.mix, "select_bgm", lambda ver, n: "g-eazy-nba-type")
    calls = []
    monkeypatch.setattr(build, "_script", _fake_scripts(build._script, calls))
    real_tp, forced = mix.encoded_tp, [-1.2]

    def first_trial_over(path):                  # chỉ ép lần thử đầu (của mix.wav); sau đó đo thật
        return forced.pop() if forced else real_tp(path)
    monkeypatch.setattr(mix, "encoded_tp", first_trial_over)
    got = build.run(proj, rules_110, "standard")
    assert got["ok"] is True and got["failed_gate"] is None, got
    assert build.GATES == ("planner", "picture_lock", "text_safe", "stem_bed", "lint_pre_mux", "mix",
                           "render", "mux", "lint_post_mux", "report")
    assert calls == ["check_text_safe.py", "render_video.py", "mux.py", "make_report.py"]
    assert _names(got["artifacts"], proj) == [
        "out/sfx_plan.json", "picture_lock.json", "src/data/script.ts", "out/safe/text_safe.json",
        "public/sfx_stem.wav", "public/bgm_bed.wav", "out/sfx_lint.json", "public/mix.wav",
        "public/mix-nobgm.wav", "out/mix_loudness.json", "out/_video.mp4", "out/final.mp4",
        "out/final-nobgm.mp4", "out/final-social.mp4", "out/QA.json", "out/EDITOR-REPORT.md"]
    results = _read(proj / "out" / "sfx_lint.json")
    assert [r["code"] for r in results] == PRE_CODES + ["L11"]
    assert all(r["ok"] for r in results), [r for r in results if not r["ok"]]
    by = {r["code"]: r for r in results}
    assert "BỎ QUA" not in by["L10"]["msg"] and "không có nhạc nền" not in by["L12"]["msg"]
    pub = proj / "public"
    assert (pub / "mix.wav").read_bytes() != (pub / "mix-nobgm.wav").read_bytes()
    qa, loops = _read(proj / "out" / "QA.json")["outputs"], _read(proj / "out" / "mix_loudness.json")
    assert not forced and loops["mix.wav"]["attempts"] >= 2                    # lần thử bị ép vượt ⇒ làm lại
    assert loops["mix.wav"]["ceiling_dbtp"] <= -1.5 - (0.5 + 0.3 + 0.1) + 1e-9  # trần hạ phần vượt + 0,1
    for name, mp4 in (("mix.wav", "final.mp4"), ("mix-nobgm.wav", "final-nobgm.mp4")):
        y = A.decode(pub / name)
        assert abs(A.integrated_lufs(y) + 16.0) <= 0.5
        assert max(A.true_peak_db(y[:, ch]) for ch in range(2)) <= -1.5, name   # S18: TP ≤ −1,5
        assert {k: qa[mp4][k] for k in ("attempts", "ceiling_dbtp")} == loops[name], mp4
        # bản AAC thử của cổng mix đoán đúng TP bản xuất mux ghép từ mix đó (cùng bộ mã)
        trial = build._aac_trial(pub / name, tmp_path / "_t.m4a")
        assert abs(mix.encoded_tp(trial) - qa[mp4]["tp_dbtp"]) <= 0.01, name
    assert 1 <= qa["final-social.mp4"]["attempts"] <= loud.TP_TRIES
    assert qa["final-social.mp4"]["ceiling_dbtp"] <= -2.0 + 1e-9
    assert not list((proj / "out").glob("_raw-*"))                    # mix thô tạm đã dọn
    assert not list((proj / "out").glob("*.m4a"))                     # bản AAC thử đã dọn


def test_build_mix_gate_holds_loudness(tmp_path, monkeypatch, rules_110):
    """Cổng 'loudness mix' (S18, R35): mix / mix-nobgm đi qua đúng vòng dùng chung của social
    (mix.loudnorm_encoded — limiter true-peak 4×, mã hoá AAC thử như mux.py, TP bản thử còn vượt
    thì hạ trần phần vượt + 0,1 dB, tối đa TP_TRIES lần); bản ghi vòng (số lần, trần cuối) ghi
    ở out/mix_loudness.json cho QA.json. File ghi ra có I lệch quá tol_lu, TP > tp_dbtp, hay bản
    AAC thử vẫn vượt sau TP_TRIES lần ⇒ BuildError (BUILD dừng ở mix, trước render)."""
    (tmp_path / "public").mkdir()
    (tmp_path / "out").mkdir()
    vo = _band(2 * A.SR, 0.2, 0)
    A.write_wav(tmp_path / "public" / "vo-clean.wav", np.stack([vo, vo], axis=1))
    A.write_wav(tmp_path / "public" / "sfx_stem.wav", np.zeros(len(vo)))
    s = {"project": tmp_path, "R": rules_110, "lock": {"t_end": 2.0}}
    calls, loops, got, aac = [], [], {"lufs": -16.02, "tp_dbtp": -1.99}, iter([-1.2, -1.6, -1.7])
    real_loop = mix.loudnorm_encoded

    def fake(src, dst, target, tp, margin_db=loud.LIMIT_MARGIN_DB, oversample=1):
        calls.append((Path(dst).name, target, tp, round(margin_db, 6), oversample))
        return dict(got)

    def fake_trial(wav, trial):                  # bản AAC thử giả (mix giả không ghi WAV thật)
        trial.write_bytes(b"aac")
        return trial

    def spy_loop(src, wav, target, tp, encode):
        loops.append(Path(wav).name)
        return real_loop(src, wav, target, tp, encode)
    monkeypatch.setattr(mix, "loudnorm_file", fake)
    monkeypatch.setattr(mix, "loudnorm_encoded", spy_loop)
    monkeypatch.setattr(mix, "encoded_tp", lambda path: next(aac))
    monkeypatch.setattr(build, "_aac_trial", fake_trial)
    _, files, note = build._mix(s)
    assert loops == ["mix.wav", "mix-nobgm.wav"]                     # final/nobgm dùng chung vòng R35
    assert [f.name for f in files] == ["mix.wav", "mix-nobgm.wav", "mix_loudness.json"]
    assert calls == [("mix.wav", -16.0, -1.5, 0.5, 4), ("mix.wav", -16.0, -1.5, 0.9, 4),
                     ("mix-nobgm.wav", -16.0, -1.5, 0.5, 4)]
    assert "AAC thử TP -1.60" in note and "AAC thử TP -1.70" in note
    assert _read(tmp_path / "out" / "mix_loudness.json") == {
        "mix.wav": {"attempts": 2, "ceiling_dbtp": -2.4},
        "mix-nobgm.wav": {"attempts": 1, "ceiling_dbtp": -2.0}}

    for bad, tps in (({"lufs": -16.0, "tp_dbtp": -1.4}, [-2.0]),        # WAV vượt TP
                     ({"lufs": -16.6, "tp_dbtp": -2.0}, [-2.0]),        # I lệch quá tol_lu
                     ({"lufs": -16.0, "tp_dbtp": -2.0}, [-1.0, -1.1, -1.2])):   # AAC thử vẫn vượt
        calls.clear()
        got, aac = bad, iter(tps)
        with pytest.raises(build.BuildError, match="mix.wav"):
            build._mix(s)
        assert len(calls) == len(tps)
    assert [c[3] for c in calls] == [0.5, 1.1, 1.6] and len(calls) == loud.TP_TRIES
    assert not list((tmp_path / "out").glob("_raw-*"))               # mix thô + bản thử tạm vẫn được dọn


def test_build_without_bgm_drops_stale_bed(tmp_path, monkeypatch, v2_vo_mono, fixture_v2_words_corrected,
                                           fixture_v2_pauses_full, v2_edit_v11, rules_110):
    """Chưa chọn nhạc nền (trước gate 9): bgm_bed.wav của lần BUILD trước bị xoá để lint và
    mix không dùng nhầm; L12 báo không có nhạc nền; mix.wav = mix-nobgm.wav."""
    proj = _v2_project(tmp_path, v2_vo_mono, fixture_v2_words_corrected, fixture_v2_pauses_full, v2_edit_v11)
    A.write_wav(proj / "public" / "bgm_bed.wav", np.full((1000, 2), 0.5))
    monkeypatch.setattr(build.mix, "select_bgm", lambda ver, n: None)
    calls = []
    monkeypatch.setattr(build, "_script", _fake_scripts(build._script, calls, fail="render_video.py"))
    got = build.run(proj, rules_110, "standard")
    assert got["failed_gate"] == "render"
    assert not (proj / "public" / "bgm_bed.wav").exists()
    l12 = next(r for r in _read(proj / "out" / "sfx_lint.json") if r["code"] == "L12")
    assert l12["ok"] and "không có nhạc nền" in l12["msg"]
    pub = proj / "public"
    assert (pub / "mix.wav").read_bytes() == (pub / "mix-nobgm.wav").read_bytes()
