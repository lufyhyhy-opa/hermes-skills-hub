import numpy as np
from thlib import audio as A


def sine(f, amp=1.0, dur=3.0):
    t = np.arange(int(A.SR * dur)) / A.SR
    return amp * np.sin(2 * np.pi * f * t)


def test_momentary_1k_fullscale_is_minus3():
    m = A.momentary(sine(997.0))
    assert abs(np.median(m[A.SR:]) - (-3.01)) < 0.15


def test_integrated_matches_momentary_for_steady_tone():
    assert abs(A.integrated_lufs(sine(997.0, 0.1)) - (-23.01)) < 0.2


def test_phone_filter_kills_100hz_keeps_1k():
    lo = A.db(np.sqrt(np.mean(A.phone(sine(100.0))[A.SR:] ** 2)))
    hi = A.db(np.sqrt(np.mean(A.phone(sine(1000.0))[A.SR:] ** 2)))
    assert hi - lo > 30


def test_runs():
    assert A.runs(np.array([0, 1, 1, 0, 1])) == [(1, 3), (4, 5)]


def test_true_peak_not_below_sample_peak():
    x = sine(11025.0, 0.5, 0.5)
    assert A.true_peak_db(x) >= A.db(np.abs(x).max()) - 1e-6


def test_xcorr_detects_delay():
    rng = np.random.default_rng(0); a = rng.standard_normal(A.SR)
    b = np.concatenate([np.zeros(2048), a])[: len(a)]
    assert abs(A.xcorr_lag_ms(a, b) - 2048 / 48) < 0.1


def test_integrated_lufs_silence_does_not_crash():
    # Every 400 ms block fails the -70 LUFS absolute gate: regression test for
    # the TypeError previously raised by the fallback branch on numpy 2.x.
    val = A.integrated_lufs(np.zeros(A.SR))
    assert np.isfinite(val)
    assert val < -70.0


def test_integrated_lufs_stereo_sums_channel_powers():
    # Ruling R10: [n, 2] đo theo BS.1770 nhiều kênh = cộng công suất hai kênh
    # (G = 1,0 cho L/R), không hạ mono. Hai kênh giống nhau đọc cao hơn 3,01 dB.
    x = sine(997.0, 0.1)
    assert abs(A.integrated_lufs(np.stack([x, x], axis=1)) - (A.integrated_lufs(x) + 3.0103)) < 0.01
    left, right = 0.05 * np.random.default_rng(0).standard_normal((2, 10 * A.SR))
    power_sum = 10 * np.log10(10 ** (A.integrated_lufs(left) / 10) + 10 ** (A.integrated_lufs(right) / 10))
    assert abs(A.integrated_lufs(np.stack([left, right], axis=1)) - power_sum) < 0.05


def test_decode_mono_keeps_level_of_mono_file(tmp_path):
    x = 0.5 * np.sin(2 * np.pi * 1000 * np.arange(A.SR) / A.SR)
    A.write_wav(tmp_path / "m.wav", x)
    y = A.decode_mono(tmp_path / "m.wav")
    assert abs(np.abs(y).max() - 0.5) < 0.01


def test_decode_mono_averages_stereo(tmp_path):
    l = 0.5 * np.ones(A.SR); r = np.zeros(A.SR)
    A.write_wav(tmp_path / "s.wav", np.stack([l, r], axis=1))
    y = A.decode_mono(tmp_path / "s.wav")
    assert abs(np.median(y) - 0.25) < 0.01


def test_integrated_lufs_relative_gate_excludes_quiet_tail():
    loud = sine(997.0, 1.0, 2.0)
    quiet = sine(997.0, 0.01, 1.0)  # ~-40 dBFS, still above the absolute gate
    mix = np.concatenate([loud, quiet])
    # The relative gate (-10 LU below the absolute-gated mean) should drop the
    # quiet tail's blocks, keeping the result close to the loud-only value
    # instead of being dragged toward the quiet segment's loudness (~-43 LUFS).
    assert abs(A.integrated_lufs(mix) - A.integrated_lufs(loud)) < 1.0
    assert A.integrated_lufs(mix) > -10.0
