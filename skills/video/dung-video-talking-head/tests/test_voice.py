import hashlib
from pathlib import Path

import numpy as np
import pytest
from scipy.io import wavfile

from thlib import audio as A, voice, rules

# Oracle: prototype/sim_v11_auto_standard.json — planner_v11.py chạy trên đúng
# file tests/fixtures/v2/vo-clean.m4a (md5 dcd0c6ef…), làm tròn 4 chữ số.
PROTO_PAUSES = [
    (0.0, 0.2691), (0.5794, 0.7742), (1.3804, 1.7185), (2.6598, 3.0433), (3.6101, 4.3311),
    (5.3519, 5.5426), (7.2344, 7.7265), (11.3619, 11.5205), (14.6565, 15.0603),
    (15.3077, 15.6457), (16.4104, 16.6903), (18.671, 19.0516), (22.1531, 22.3538),
    (24.7878, 25.2122), (26.1641, 26.593), (27.5105, 27.829), (28.7381, 29.0525),
    (30.7789, 31.2059), (33.4676, 33.9574), (34.4661, 34.7695), (35.7273, 36.1042),
    (38.6698, 39.032), (39.7267, 39.9835), (41.051, 41.3179), (42.8454, 43.136),
]
# phone_a: sim JSON ghi -20.9300 vì phone() mặc định của prototype dùng HPF
# 350 Hz (+ LPF 12 kHz); tính lại đúng công thức prototype với HPF 300 Hz của
# spec §5.1 được -20.8063 — đó là giá trị đối chiếu.
PROTO_VO_REF = {"k": -18.8234, "phone_k": -19.1960, "phone_a": -20.8063}

SOURCE_V2 = Path("D:/MMO/Van Minh AI/Vid Heygen/2/2.mp4")   # nguồn thật, chỉ đọc


def burst(sec_on, sec_off, n=4):
    x = []
    rng = np.random.default_rng(1)
    for _ in range(n):
        x.append(0.1 * rng.standard_normal(int(sec_on * A.SR)))
        x.append(np.zeros(int(sec_off * A.SR)))
    return np.concatenate(x)


def test_find_pauses_on_synthetic():
    R = rules.load("1.1.0")
    P = voice.find_pauses(burst(0.8, 0.3), R)
    assert len(P) == 4 and all(abs((b - a) - 0.3) < 0.03 for a, b in P)


def test_onset_earliest_word_rule():
    R = rules.load("1.1.0")
    words = [{"s": 2.46, "e": 3.30}, {"s": 3.30, "e": 3.60}]   # '20', 'lần' from video 2
    on = voice.correct_onsets(words, [(2.66, 3.043)], R)
    assert abs(on[0] - 3.043) < 1e-9 and on[1] >= on[0] + 0.02


def test_onset_each_pause_goes_to_one_word_only(rules_110):
    # t1 = 1.0 lọt cửa sổ của cả hai từ -> chỉ từ SỚM NHẤT nhận; từ sau giữ s
    # whisper rồi bị kẹp ≥ onset trước + 20 ms.
    words = [{"s": 0.95, "e": 0.98}, {"s": 0.99, "e": 1.20}, {"s": 1.50, "e": 1.80}]
    on = voice.correct_onsets(words, [(0.5, 1.0)], rules_110)
    assert on[0] == 1.0
    assert abs(on[1] - 1.02) < 1e-9
    assert on[2] == 1.50


def test_two_pauses_never_collapse_into_one_word(rules_110):
    # one long word spanning both pauses, then a short word after each
    words = [{"s": 1.00, "e": 2.60}, {"s": 2.70, "e": 3.00}, {"s": 3.40, "e": 3.80}]
    pauses = [(2.00, 2.20), (3.05, 3.35)]
    on = voice.correct_onsets(words, pauses, rules_110)
    # pause 1 (t1=2.20) belongs to word 0; pause 2 (t1=3.35) must NOT overwrite it
    assert abs(on[0] - 2.20) < 1e-9
    assert on[1] >= on[0] + rules_110.get("audio.onset_mono_gap_s")
    assert on[2] >= on[1]
    assert sorted(on) == on


def test_two_pauses_inside_same_word_window_only_earliest_wins(rules_110):
    # rules.json 1.1.0: onset_post_s = 0.05 s, nên với words/pauses gốc của
    # test_two_pauses_never_collapse_into_one_word, t1=3.35 KHÔNG còn lọt cửa
    # sổ của từ 0 (e + post = 2.65 < 3.35) -> pause 2 tự nhiên rơi vào từ 2,
    # không đụng độ. Test này nới "e" của từ 0 tới 3.35 để cả hai t1 (2.20 và
    # 3.35) cùng lọt cửa sổ đúng MỘT từ, tái hiện đúng lỗi ghi đè ở S04: nếu
    # không theo dõi từ đã nhận, t1 sau (3.35) sẽ ghi đè on[0] thay vì bị bỏ
    # qua (từ 1 và từ 2 không lọt cửa sổ của 3.35 nên không có từ nào khác để
    # gán, đúng nhánh "không còn từ nào -> giữ không có onset").
    words = [{"s": 1.00, "e": 3.35}, {"s": 3.55, "e": 3.70}, {"s": 3.90, "e": 4.20}]
    pauses = [(2.00, 2.20), (3.05, 3.35)]
    on = voice.correct_onsets(words, pauses, rules_110)
    assert abs(on[0] - 2.20) < 1e-9        # từ 0 giữ pause SỚM NHẤT của nó
    assert on[1] == 3.55                    # pause 2 không có từ nào khác -> giữ s whisper
    assert on[2] == 3.90
    assert sorted(on) == on


def test_find_pauses_matches_prototype_on_video2(v2_vo_mono, rules_110):
    P = voice.find_pauses(v2_vo_mono, rules_110)
    assert len(P) == len(PROTO_PAUSES)
    for (a, b), (pa, pb) in zip(P, PROTO_PAUSES):
        assert abs(a - pa) < 1e-4 and abs(b - pb) < 1e-4


def test_vo_ref_matches_prototype_on_video2(v2_vo_mono, rules_110):
    ref = voice.vo_ref(v2_vo_mono, rules_110)
    assert set(ref) == {"phone_k", "k", "phone_a"}
    assert abs(ref["k"] - PROTO_VO_REF["k"]) < 0.01
    assert abs(ref["phone_k"] - PROTO_VO_REF["phone_k"]) < 0.01
    assert abs(ref["phone_a"] - PROTO_VO_REF["phone_a"]) < 0.01


def test_onsets_on_video2_fixtures(fixture_v2_whisper_words_on, fixture_v2_words_corrected):
    for W in (fixture_v2_whisper_words_on, fixture_v2_words_corrected):
        on = [w["on"] for w in W]
        assert all(b >= a + 0.02 - 1e-9 for a, b in zip(on, on[1:]))
    # whisper đặt '20' ở 2.46 s nhưng giọng im tới hết khoảng ngắt 2.6598–3.0433.
    w20 = fixture_v2_whisper_words_on[7]
    assert w20["w"] == "20" and w20["i"] == 7 and abs(w20["on"] - 3.0433) < 1e-3


def test_last_word_end_uses_final_silence_start():
    words = [{"s": 0.0, "e": 1.0}, {"s": 1.0, "e": 2.0}]
    assert voice.last_word_end(words, [(0.5, 0.6), (1.8, 3.0)], 3.0) == 1.8
    assert voice.last_word_end(words, [(0.5, 0.6), (1.8, 2.9)], 3.0) == 2.0
    assert voice.last_word_end(words, [], 3.0) == 2.0


def test_pauses_full_fixture_video2(fixture_v2_pauses_full):
    P = fixture_v2_pauses_full
    assert set(P) == {"pauses", "designed_breaks", "vo_ref", "duration_s", "last_word_end"}
    assert abs(P["duration_s"] - 43.136) < 1e-3
    assert abs(P["last_word_end"] - 42.8454) < 1e-3   # khoảng ngắt cuối chạm hết file
    assert all(isinstance(p, list) and len(p) == 2 for p in P["pauses"])


def test_clear_chain_is_s28_verbatim(rules_110):
    assert voice.clear_chain(rules_110) == (
        "highpass=f=110,lowpass=f=10000,equalizer=f=220:t=q:w=1.1:g=-6,"
        "equalizer=f=3500:t=q:w=1.3:g=3.5,"
        "acompressor=threshold=-18dB:ratio=2.2:attack=10:release=90:makeup=2"
    )


def test_loudnorm_apply_pass_is_linear_and_reports(rules_110):
    # Lượt áp giữ nguyên chuỗi của brief và in JSON để đọc normalization_type.
    m = {"input_i": "-16.04", "input_tp": "-2.50", "input_lra": "3.50",
         "input_thresh": "-26.30", "target_offset": "0.02"}
    assert voice._loudnorm(rules_110, m) == (
        "loudnorm=I=-16:TP=-2:LRA=11:measured_I=-16.04:measured_TP=-2.50"
        ":measured_LRA=3.50:measured_thresh=-26.30:offset=0.02:linear=true"
        ":print_format=json"
    )


def test_require_linear_rejects_dynamic_fallback():
    # ffmpeg lặng lẽ rơi về 'dynamic' khi không đạt I và TP đích cùng lúc.
    stats = {"input_i": "-17.04", "input_tp": "-1.72", "input_lra": "3.50",
             "normalization_type": "dynamic"}
    with pytest.raises(RuntimeError, match="dynamic"):
        voice._require_linear(stats)
    voice._require_linear({**stats, "normalization_type": "linear"})


def test_peak_stage_leaves_linear_headroom(rules_110):
    # Về I đích (-17.04 -> +1.04 dB), rồi limiter trần TP đích - 0,5 dB
    # (-2.5 dBFS = 0.749894); latency=true bù trễ lookahead, level=false giữ mức.
    assert voice._peak_stage(rules_110, -17.04) == (
        "volume=1.04dB,alimiter=limit=0.749894:level=false:latency=true"
    )


def _peaky_stereo(sec=8.0, seed=5):
    """Nhiễu hai mức xen kẽ 0,4 s (LRA > 0) + click 2 ms mỗi 2 s. Sau chuỗi
    S28 PLR ≈ 20 dB, quá 14 dB (TP đích − I đích) mà loudnorm tuyến tính
    chịu được — bản không có khâu đỉnh rơi về 'dynamic'."""
    rng = np.random.default_rng(seed)
    n = int(sec * A.SR)
    seg = int(0.4 * A.SR)
    x = rng.standard_normal(n) * np.where((np.arange(n) // seg) % 2 == 0, 0.05, 0.025)
    for k in range(int(0.25 * A.SR), n, int(2.0 * A.SR)):
        x[k:k + int(0.002 * A.SR)] += 0.5
    return np.stack([x, x], axis=1)


def test_vo_clear_stays_linear_on_peaky_voice(tmp_path, rules_110):
    # vo_clear ném RuntimeError nếu lượt 2 không tuyến tính -> chạy qua = tuyến tính.
    src = tmp_path / "peaky.wav"
    wavfile.write(src, A.SR, (np.clip(_peaky_stereo(), -1, 1) * 32767).astype(np.int16))
    # Tiền đề: chỉ có chuỗi S28 thì TP − I vượt TP đích − I đích.
    ch = voice._measure(src, rules_110, voice.clear_chain(rules_110))
    assert float(ch["input_tp"]) - float(ch["input_i"]) > (
        rules_110.get("voice.tp_dbtp") - rules_110.get("voice.target_lufs"))
    qa = voice.vo_clear(src, tmp_path / "out.wav", rules_110)
    assert abs(qa["lufs"] - rules_110.get("voice.target_lufs")) <= rules_110.get("voice.tol_lu")
    assert qa["tp_dbtp"] <= rules_110.get("voice.tp_dbtp")
    assert abs(qa["xcorr_ms"]) <= rules_110.get("voice.xcorr_max_ms")


def test_vo_clear_output_unchanged_by_r35(tmp_path, rules_110):
    # R35 chỉ đổi bản xuất (limiter true-peak + vòng mã hoá–đo–hạ trần); chuỗi giọng vẫn R9 (limiter
    # theo mẫu): mẫu PCM vo_clear ra trên tín hiệu peaky phải y hệt BASE 75e31d6 (sha256 dưới đây).
    src = tmp_path / "peaky.wav"
    wavfile.write(src, A.SR, (np.clip(_peaky_stereo(), -1, 1) * 32767).astype(np.int16))
    voice.vo_clear(src, tmp_path / "out.wav", rules_110)
    sr, data = wavfile.read(tmp_path / "out.wav")
    assert sr == A.SR and data.dtype == np.int16 and data.shape == (len(_peaky_stereo()), 2)
    assert hashlib.sha256(data.tobytes()).hexdigest() == (
        "a3abaa924e7504b3d9965494d099e0826aa286c4c6cd8c5395e10c627ea9dd59")


def test_vo_clear_refuses_dynamic_fallback(tmp_path, rules_110, monkeypatch):
    # Bỏ khâu đỉnh (= bản trước sửa): lượt 2 rơi về 'dynamic' -> vo_clear phải
    # ném lỗi và không để lại file ra, thay vì trả QA như thường.
    monkeypatch.setattr(voice, "_peak_stage", lambda R, measured_i: "anull")
    src = tmp_path / "peaky.wav"
    wavfile.write(src, A.SR, (np.clip(_peaky_stereo(), -1, 1) * 32767).astype(np.int16))
    out = tmp_path / "out.wav"
    with pytest.raises(RuntimeError, match="dynamic"):
        voice.vo_clear(src, out, rules_110)
    assert not out.exists()


@pytest.mark.slow
def test_vo_clear_qa_on_video2(tmp_path, rules_110):
    # Nguồn thật: PLR sau chuỗi S28 ≈ 15,3 dB. vo_clear ném lỗi nếu loudnorm
    # lượt 2 rơi về 'dynamic', nên test qua nghĩa là đã chạy tuyến tính.
    out = tmp_path / "vo-clean.wav"
    qa = voice.vo_clear(SOURCE_V2, out, rules_110)
    assert set(qa) == {"lufs", "tp_dbtp", "tilt_db", "low_db", "voice_hf_ratio", "xcorr_ms"}
    assert abs(qa["lufs"] + 16) <= 0.5
    assert qa["tp_dbtp"] <= -2.0 + 0.1
    assert abs(qa["xcorr_ms"]) <= 2.0
    assert qa["tilt_db"] >= rules_110.get("voice.tilt_min_db")
    assert qa["low_db"] <= rules_110.get("voice.low_max_db")
    assert 0.0 <= qa["voice_hf_ratio"] <= 1.0
    sr, data = wavfile.read(out)
    assert sr == 48000 and data.ndim == 2 and data.shape[1] == 2 and data.dtype == np.int16
