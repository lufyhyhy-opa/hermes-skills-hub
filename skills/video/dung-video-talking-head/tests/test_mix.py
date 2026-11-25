# tests/test_mix.py — stem SFX, nhạc nền S29, trộn, loudnorm 2 lượt tuyến tính
# và import_bgm.py (Task 9). Mức tuyệt đối đo theo BS.1770 nhiều kênh (R10).
import hashlib
import json
import re

import numpy as np
import pytest
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

import import_bgm
from thlib import loud, mix, audio as A, paths, rules


def noise(sec, amp=0.1, seed=0):
    return amp * np.random.default_rng(seed).standard_normal(int(sec * A.SR))


def band_db(x, lo, hi):
    f, P = A.spectrum(x)
    return 10 * np.log10(A.band_frac(f, P, lo, hi) / (hi - lo))


def test_render_stem_places_samples():
    s = mix.render_stem([{"start_s": 1.0, "samples": np.ones(10)}], A.SR * 2)
    assert s[A.SR - 1] == 0 and s[A.SR] == 1 and s[A.SR + 9] == 1 and s[A.SR + 10] == 0


def test_render_stem_sums_overlaps_and_clips_to_length():
    cues = [{"start_s": -2 / A.SR, "samples": np.ones(4)},
            {"start_s": 1 / A.SR, "samples": np.ones(3)},
            {"start_s": 8 / A.SR, "samples": np.ones(5)}]
    assert mix.render_stem(cues, 10).tolist() == [1, 2, 1, 1, 0, 0, 0, 0, 1, 1]


def test_bgm_bed_level_and_fades():
    R = rules.load("1.1.0")
    vo = noise(20, 0.05); track = noise(8, 0.3, seed=2)
    bed = mix.bgm_bed(track, vo, 19.0, R)
    assert abs((A.integrated_lufs(bed[: int(18 * A.SR)]) - A.integrated_lufs(vo)) - (-15.0)) <= 1.0
    assert np.abs(bed[:100]).max() < 1e-3 and np.abs(bed[int(19.0 * A.SR):]).max() == 0


def test_bgm_bed_stereo_track_loops_without_dip_at_voice_minus_15():
    R = rules.load("1.1.0")
    vo = noise(20, 0.05)
    track = np.stack([noise(6, 0.3, 3), noise(6, 0.3, 4)], axis=1)
    bed = mix.bgm_bed(track, vo, 19.0, R)
    assert bed.shape == (len(vo), 2)
    # R10: bed stereo so với giọng phát ra hai kênh (dual-mono), cùng một định nghĩa.
    vo_played = A.integrated_lufs(np.stack([vo, vo], axis=1)[: int(19 * A.SR)])
    assert abs(A.integrated_lufs(bed) - (vo_played + R.get("bgm.rel_lu"))) <= 0.1
    # Bài 6 s lặp 3 lần (mối nối 5,5 / 11 / 16,5 s): crossfade đẳng công suất không hụt mức.
    env = A.db(A.rms_env(bed[:, 0], 0.1))[int(1.5 * A.SR): int(17 * A.SR)]
    assert env.min() > np.median(env) - 1.5


def test_bgm_bed_applies_hpf_and_presence_cut():
    R = rules.load("1.1.0")
    bed = mix.bgm_bed(noise(12, 0.3, 7), noise(12, 0.05), 12.0, R)[A.SR: 10 * A.SR]
    assert band_db(bed, 30, 60) - band_db(bed, 400, 600) < -8        # HPF 100 Hz
    assert -3.5 < band_db(bed, 1900, 2100) - band_db(bed, 300, 500) < -2.0   # −3 dB @ 2 kHz


def test_mixdown_sums_trims_and_fades():
    R = rules.load("1.1.0")
    n = 3 * A.SR
    vo = np.full((n, 2), 0.1); stem = np.full(n, 0.2); bed = np.full((n, 2), 0.05)
    out = mix.mixdown(vo, stem, bed, 2.0, R)
    fade = round(R.get("end.fade_s") * A.SR)
    assert out.shape == (2 * A.SR, 2)
    assert np.allclose(out[: -fade], 0.35)
    assert np.all(np.diff(out[-fade:, 0]) < 0) and np.all(out[-1] == 0)
    assert np.allclose(mix.mixdown(vo, stem, None, 2.0, R)[A.SR], 0.3)
    # Lớp ngắn hơn t_end được đệm 0 (giọng hết ở 1 s, stem vẫn còn).
    assert np.allclose(mix.mixdown(vo[: A.SR], stem, None, 2.0, R)[int(1.5 * A.SR)], 0.2)


def test_loudnorm_file_hits_target(tmp_path):
    x = np.stack([noise(10, 0.02), noise(10, 0.02, 1)], axis=1)
    A.write_wav(tmp_path / "in.wav", x)
    r = mix.loudnorm_file(tmp_path / "in.wav", tmp_path / "out.wav", -16.0, -1.5)
    # R10: đo BS.1770 nhiều kênh trên [n, 2], không hạ mono (mono đọc thấp hơn ~6 dB).
    y = A.decode(tmp_path / "out.wav")
    assert abs(A.integrated_lufs(y) + 16.0) <= 0.5
    assert abs(r["lufs"] + 16.0) <= 0.5 and r["tp_dbtp"] <= -1.5
    assert abs(r["input_lufs"] - A.integrated_lufs(x)) <= 0.2   # thlib khớp ffmpeg
    assert wavfile.read(tmp_path / "out.wav")[0] == A.SR


def test_loudnorm_file_refuses_non_linear(tmp_path):
    x = noise(10, 0.001)
    x[A.SR] = 0.9   # đỉnh nhọn: nâng lên −16 LUFS thì TP vượt trần ⇒ ffmpeg sẽ chạy động
    # (R19: đỉnh mang phần lớn I đo được; limiter cắt nó thì I hụt ~3,8 LU, gain bù vẫn vượt trần)
    A.write_wav(tmp_path / "in.wav", np.stack([x, x], axis=1))
    with pytest.raises(RuntimeError, match="tuyến tính"):
        mix.loudnorm_file(tmp_path / "in.wav", tmp_path / "out.wav", -16.0, -1.5)
    assert not (tmp_path / "out.wav").exists()


@pytest.mark.parametrize("target", [-16.0, -14.0])
def test_loudnorm_file_handles_peaky_mix(tmp_path, v2_vo_mono, rules_110, target):
    # R19: giọng video 2 (20 s đầu) + bed tonight-hiphop ở giọng − 15 LU. Mix đo
    # I −15,37 / TP −1,37 dBTP: gain tuyến tính tới −14 (social) đẩy TP lên 0 dBTP
    # ⇒ không có khâu đỉnh thì ffmpeg rơi về 'dynamic' và loudnorm_file ném lỗi.
    vo = v2_vo_mono[: 20 * A.SR]
    track = A.decode(paths.release_dir("1.1.0") / "bgm" / "tonight-hiphop.wav")
    bed = mix.bgm_bed(track, vo, 20.0, rules_110)
    raw = mix.mixdown(np.stack([vo, vo], axis=1), np.zeros(len(vo)), bed, 20.0, rules_110)
    A.write_wav(tmp_path / "in.wav", raw)
    r = mix.loudnorm_file(tmp_path / "in.wav", tmp_path / "out.wav", target, -1.5)
    y = A.decode(tmp_path / "out.wav")
    assert abs(A.integrated_lufs(y) - target) <= 0.5      # BS.1770 hai kênh (R10)
    assert max(A.true_peak_db(y[:, ch]) for ch in range(2)) <= -1.5
    assert abs(r["lufs"] - target) <= 0.5 and r["tp_dbtp"] <= -1.5


def test_peak_stage_options_compose_filter():
    """Mặc định giữ đúng khâu đỉnh R19 (limiter theo mẫu, trần TP đích − 0,5 dB); margin_db đổi
    trần; oversample > 1 chạy limiter ở SR × oversample rồi hạ về SR (limiter true-peak)."""
    assert loud.peak_stage(-14.0, -1.5, -16.0) == (
        "volume=2dB,alimiter=limit=0.794328:level=false:latency=true")
    assert loud.peak_stage(-14.0, -1.5, -16.0, 1.0, 4) == (
        "aresample=192000,volume=2dB,alimiter=limit=0.749894:level=false:latency=true,aresample=48000")


def test_loudnorm_file_true_peak_limiter(tmp_path):
    """oversample=4 chặn đỉnh giữa hai mẫu (bản social, mux.py): nhiễu kiểu giọng ≈ −14 LUFS
    + ba cú sin fs/4 lệch pha 45° — mẫu chỉ thấy 0,707 biên độ nên sample peak −3,5 dBFS mà
    true peak ≈ −0,3 dBTP. Ra −14 ±0,5 LUFS, TP ≤ −1,5; margin_db 1,0 hạ TP thêm."""
    sos = butter(4, (100, 4000), btype="bandpass", fs=A.SR, output="sos")
    x = sosfilt(sos, noise(8, 1.0))
    x *= 10 ** ((-14.3 - A.integrated_lufs(np.stack([x, x], axis=1))) / 20)
    t = np.arange(int(0.01 * A.SR)) / A.SR
    for k in range(3):
        a = int((1.5 + 2 * k) * A.SR)
        x[a:a + len(t)] = 0.95 * np.sin(2 * np.pi * (A.SR / 4) * t + np.pi / 4)
    assert A.db(np.abs(x).max()) < -3.0 and A.true_peak_db(x) > -0.5
    A.write_wav(tmp_path / "in.wav", np.stack([x, x], axis=1))
    tp = {}
    for margin in (0.5, 1.0):
        mix.loudnorm_file(tmp_path / "in.wav", tmp_path / "out.wav", -14.0, -1.5, margin, 4)
        y = A.decode(tmp_path / "out.wav")
        tp[margin] = max(A.true_peak_db(y[:, ch]) for ch in range(2))
        assert abs(A.integrated_lufs(y) + 14.0) <= 0.5 and tp[margin] <= -1.5, (margin, tp)
    assert tp[1.0] <= tp[0.5] - 0.3


def _aac(wav):
    """encode của vòng R35 trong test: mã hoá AAC `wav` như ba bản xuất -> <wav>.m4a."""
    m4a = wav.with_suffix(".m4a")
    loud.ffmpeg(["-y", "-i", str(wav), *loud.AAC_ARGS, str(m4a)])
    return m4a


def test_loudnorm_encoded_retries_once_on_peaky_mix(tmp_path, monkeypatch):
    """R35: mix kiểu giọng ≈ −14 LUFS + ba cú click chữ nhật 0,75 ms. Lần 1 (limiter true-peak 4×,
    trần TP đích − 0,5 = −2,0 dBTP) WAV đạt nhưng bộ mã AAC vọt TP bản mã hoá quá −1,5 ⇒ đúng một
    lần làm lại với trần hạ (phần vượt + 0,1 dB), lần 2 đạt; bản ghi: số lần, trần cuối, TP mã hoá."""
    sos = butter(4, (100, 4000), btype="bandpass", fs=A.SR, output="sos")
    x = sosfilt(sos, noise(8, 1.0))
    x *= 10 ** ((-14.3 - A.integrated_lufs(np.stack([x, x], axis=1))) / 20)
    for k in range(3):
        a = int((1.5 + 2 * k) * A.SR)
        x[a:a + int(0.00075 * A.SR)] += 0.9
    A.write_wav(tmp_path / "mix.wav", np.stack([x, x], axis=1))
    stages, tps = [], []
    real_loudnorm, real_tp = mix.loudnorm_file, mix.encoded_tp

    def spy_loudnorm(src, dst, target, tp, margin_db, oversample):
        stages.append((margin_db, oversample))
        return real_loudnorm(src, dst, target, tp, margin_db, oversample)

    def spy_tp(path):
        tps.append(real_tp(path))
        return tps[-1]
    monkeypatch.setattr(mix, "loudnorm_file", spy_loudnorm)
    monkeypatch.setattr(mix, "encoded_tp", spy_tp)
    rec = mix.loudnorm_encoded(tmp_path / "mix.wav", tmp_path / "social.wav", -14.0, -1.5, _aac)
    assert len(tps) == 2 and tps[0] > -1.5 >= tps[1], tps            # lần 1 vượt, lần 2 đạt
    assert stages == [(loud.LIMIT_MARGIN_DB, loud.TP_OVERSAMPLE),
                      (pytest.approx(0.5 + (tps[0] + 1.5) + loud.TP_STEP_DB), loud.TP_OVERSAMPLE)]
    assert rec["attempts"] == 2 and rec["encoded_tp_dbtp"] == tps[1]
    assert rec["ceiling_dbtp"] == round(-1.5 - stages[1][0], 3)
    y = A.decode(tmp_path / "social.m4a")
    assert abs(A.integrated_lufs(y) + 14.0) <= 0.5
    assert max(A.true_peak_db(y[:, ch]) for ch in range(2)) <= -1.5


def test_loudnorm_encoded_raises_after_tp_tries(tmp_path, monkeypatch):
    """R35: bản mã hoá vẫn vượt TP sau TP_TRIES lần hạ trần (vượt + 0,1 dB mỗi lần) ⇒ TruePeakError
    kèm bản ghi lần cuối (file lần cuối để lại cho cổng chấm)."""
    margins = []

    def fake(src, dst, target, tp, margin_db, oversample):
        margins.append(round(margin_db, 6))
        return {"lufs": target, "tp_dbtp": -2.0}
    tps = iter([-1.0, -1.1, -1.2])
    monkeypatch.setattr(mix, "loudnorm_file", fake)
    monkeypatch.setattr(mix, "encoded_tp", lambda path: next(tps))
    with pytest.raises(mix.TruePeakError, match="3 lần") as info:
        mix.loudnorm_encoded(tmp_path / "mix.wav", tmp_path / "out.wav", -16.0, -1.5, lambda wav: wav)
    assert margins == [0.5, 1.1, 1.6] and len(margins) == loud.TP_TRIES
    assert info.value.record == {"lufs": -16.0, "tp_dbtp": -2.0, "attempts": 3, "ceiling_dbtp": -3.1,
                                 "encoded_tp_dbtp": -1.2}


def _write_manifest(rel, tracks):
    (rel / "bgm_manifest.json").write_text(json.dumps({"tracks": tracks}), encoding="utf-8")


def test_select_bgm_rotates_selected_by_order(tmp_path, monkeypatch):
    monkeypatch.setattr(paths, "release_dir", lambda ver: tmp_path)
    _write_manifest(tmp_path, {
        "a": {"selected": True, "order": 2, "content_id_risk": "none"},
        "b": {"selected": True, "order": 1, "content_id_risk": "none"},
        "c": {"selected": True, "order": 0, "content_id_risk": "unknown"},
        "d": {"selected": False, "order": None, "content_id_risk": "none"},
    })
    assert [mix.select_bgm("x", n) for n in range(4)] == ["b", "a", "b", "a"]


def test_select_bgm_none_when_nothing_selected(tmp_path, monkeypatch):
    monkeypatch.setattr(paths, "release_dir", lambda ver: tmp_path)
    _write_manifest(tmp_path, {"a": {"selected": False, "order": None, "content_id_risk": "none"}})
    assert mix.select_bgm("x", 2) is None


def _song(path, seed):
    """Bài stereo 6 s + đuôi im 2 s; trả phần có nhạc."""
    body = np.stack([noise(6, 0.2, seed), noise(6, 0.2, seed + 1)], axis=1)
    A.write_wav(path, np.concatenate([body, np.zeros((2 * A.SR, 2))]))
    return body


def test_import_bgm_manifest_and_content_id_gate(tmp_path, monkeypatch):
    rel = tmp_path / "rel"
    rel.mkdir()
    _song(tmp_path / "a.wav", 5)
    body = _song(tmp_path / "b.wav", 7)
    url = "https://example.com/song.mp3"
    a = import_bgm.add_track(rel, tmp_path / "a.wav", "a", url, "Test License", False, True, 0)
    b = import_bgm.add_track(rel, tmp_path / "b.wav", "b", url + "?2", "Test License", True, True, 1)
    assert a["content_id_risk"] == "unknown" and b["content_id_risk"] == "none"
    assert b["selected"] is True and b["order"] == 1
    assert abs(b["loop_s"] - 6.0) < 0.3     # điểm loop bỏ đuôi im
    sr, pcm = wavfile.read(rel / b["path"])
    assert sr == A.SR and pcm.shape[1] == 2
    assert abs(len(pcm) - b["loop_s"] * A.SR) <= 3     # loop_s làm tròn 4 chữ số (±2,4 mẫu)
    assert b["md5"] == hashlib.md5((rel / b["path"]).read_bytes()).hexdigest()
    assert abs(b["lufs"] - A.integrated_lufs(body)) < 0.3
    with pytest.raises(SystemExit, match="md5"):     # nhập lại "a" bằng đúng bài của "b"
        import_bgm.add_track(rel, tmp_path / "b.wav", "a", url, "Test License", True, False, None)
    assert sorted(p.name for p in (rel / "bgm").iterdir()) == ["a.wav", "b.wav"]
    assert hashlib.md5((rel / "bgm" / "a.wav").read_bytes()).hexdigest() == a["md5"]
    manifest = json.loads((rel / "bgm_manifest.json").read_text(encoding="utf-8"))
    assert manifest["tracks"] == {"a": a, "b": b}
    monkeypatch.setattr(paths, "release_dir", lambda ver: rel)
    assert mix.select_bgm("x", 0) == "b"    # "a" chọn nhưng content_id_risk unknown ⇒ bỏ qua


@pytest.mark.parametrize("url, select, order", [
    ("Mixkit, re-check before commercial use", False, None),   # không phải URL nguồn
    ("https://example.com/x.mp3", True, None),                 # --select thiếu --order
])
def test_import_bgm_refuses_bad_input(tmp_path, url, select, order):
    src = tmp_path / "song.wav"
    A.write_wav(src, np.stack([noise(2, 0.2), noise(2, 0.2, 1)], axis=1))
    with pytest.raises(SystemExit):
        import_bgm.add_track(tmp_path, src, "x", url, "Test License", True, select, order)
    assert not (tmp_path / "bgm_manifest.json").exists()


def test_release_bgm_candidates_are_licensed_and_measured():
    rel = paths.release_dir("1.1.0")
    tracks = json.loads((rel / "bgm_manifest.json").read_text(encoding="utf-8"))["tracks"]
    assert len(tracks) >= 4
    for key, t in tracks.items():
        wav = rel / t["path"]
        assert t["md5"] == hashlib.md5(wav.read_bytes()).hexdigest(), key
        assert t["source_url"].startswith("https://") and t["license"], key
        assert t["content_id_risk"] == "none", key
        sr, pcm = wavfile.read(wav)
        assert sr == A.SR and pcm.ndim == 2 and pcm.shape[1] == 2, key
        assert abs(t["loop_s"] - len(pcm) / sr) < 1e-3, key
        assert -40 < t["lufs"] < 0, key


def test_release_bgm_accounts_for_all_local_candidates():
    """Brief bước 3: 5 bài SFX_LIB/bgm. Bài có URL trong mục bgm/ của
    ATTRIBUTION.md phải nằm trong manifest với đúng URL đó. Bài không có URL
    (bgm-tech-house: 'Mixkit，商用前复核') không được nhập — license unknown bị
    loại tự động (S13, §14); chỉ nhập khi user đưa URL thật ở cổng 9."""
    tracks = json.loads(
        (paths.release_dir("1.1.0") / "bgm_manifest.json").read_text(encoding="utf-8"))["tracks"]
    rows = (paths.SFX_LIB / "ATTRIBUTION.md").read_text(encoding="utf-8").split("## bgm/", 1)[1]
    candidates = sorted((paths.SFX_LIB / "bgm").glob("*.mp3"))
    unsourced = []
    for mp3 in candidates:
        row = next(r for r in rows.splitlines() if f"`{mp3.name}`" in r)
        url = re.search(r"https://\S+?\.mp3", row)
        if url:
            assert tracks[mp3.stem]["source_url"] == url.group(0), mp3.name
        else:
            unsourced.append(mp3.name)
    assert len(candidates) == 5 and unsourced == ["bgm-tech-house.mp3"]
