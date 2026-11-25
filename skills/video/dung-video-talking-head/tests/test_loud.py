# tests/test_loud.py — phần dùng chung của loudnorm qua ffmpeg (thlib.loud):
# đọc JSON loudnorm, khâu đỉnh R9 (giọng) / R19 (final, nobgm, social).
import pytest

from thlib import loud


def test_loudnorm_json_read_from_ffmpeg_stderr():
    stderr = (
        "Input #0, mov,mp4 from 'x{y}.mp4':\n"
        "[Parsed_loudnorm_5 @ 000001d403dbf480] \n"
        '{\n\t"input_i" : "-17.04",\n\t"input_tp" : "-1.72",\n\t"input_lra" : "3.50",\n'
        '\t"input_thresh" : "-27.30",\n\t"normalization_type" : "dynamic",\n'
        '\t"target_offset" : "0.02"\n}\n'
        "[out#0/null @ 000001d4017309c0] video:0KiB audio:32352KiB\n"
    )
    st = loud.loudnorm_json(stderr)
    assert st["input_i"] == "-17.04" and st["target_offset"] == "0.02"
    with pytest.raises(RuntimeError):
        loud.loudnorm_json("Error opening input file")


def test_peak_stage_social_target():
    # R19, social −14 / TP −1,5: gain −15,37 -> −14 (+1,37 dB), trần limiter
    # TP đích − 0,5 dB = −2 dBFS = 0,794328.
    assert loud.peak_stage(-14.0, -1.5, -15.37) == (
        "volume=1.37dB,alimiter=limit=0.794328:level=false:latency=true"
    )
