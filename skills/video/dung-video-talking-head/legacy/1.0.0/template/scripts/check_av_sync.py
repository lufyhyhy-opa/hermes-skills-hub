# -*- coding: utf-8 -*-
"""Đo SFX có rơi đúng frame thiết kế trong bản render không.

Với mỗi cue sắc (impact / pop), tương quan chéo mẫu SFX gốc với track tiếng
của file render trong cửa sổ ±12f quanh chỗ đã đặt, suy ra frame đỉnh thực tế.
    residual = frame đỉnh đo được − frame đích (cue.target)
Đạt khi |residual| ≤ 0.5f ở mọi probe. Lệch đều cùng một lượng → chỉnh
OUTPUT_AUDIO_OFFSET_F trong build.py đúng lượng đó rồi build + render lại.

Chạy từ thư mục project:
    python scripts/check_av_sync.py out/final.mp4
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
FPS, SR = 30, 48000
WINDOW_F = 12
PROBE_DIRS = ("sfx/impact/", "sfx/ui/")


def pcm(path):
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-vn", "-ac", "1", "-ar", str(SR),
         "-f", "s16le", "-"],
        capture_output=True, check=True,
    ).stdout
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768


def peak_sample(x):
    env = np.convolve(np.abs(x), np.ones(240) / 240, mode="same")
    return int(np.argmax(env))


def load_cues():
    ts = (ROOT / "src" / "data" / "script.ts").read_text(encoding="utf-8")
    body = ts.split("export const SFX: Cue[] = ", 1)[1].rstrip().rstrip(";")
    return json.loads(body)


def main():
    render = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "out" / "final.mp4")
    mix = pcm(render)
    probes = [c for c in load_cues() if c["src"].startswith(PROBE_DIRS)]
    if not probes:
        sys.exit("Không có cue impact/ui nào để làm probe.")

    worst = 0.0
    print(f"{'cue':34s} {'đích':>8s} {'đo':>8s} {'lệch':>7s}  độ tin")
    for c in probes:
        tpl = pcm(ROOT / "public" / c["src"])
        pk = peak_sample(tpl)
        # đoạn quanh đỉnh là phần đặc trưng nhất, ít bị giọng nói lấn
        a, b = max(0, pk - SR // 50), min(len(tpl), pk + SR // 8)
        seg_tpl = tpl[a:b]

        expect = int(c["from"] / FPS * SR) + a
        lo = max(0, expect - WINDOW_F * SR // FPS)
        hi = min(len(mix), expect + WINDOW_F * SR // FPS + len(seg_tpl))
        seg = mix[lo:hi]
        if len(seg) <= len(seg_tpl):
            continue

        corr = np.correlate(seg, seg_tpl, mode="valid")
        energy = np.sqrt(np.convolve(seg ** 2, np.ones(len(seg_tpl)), mode="valid"))
        ncc = corr / (energy * np.linalg.norm(seg_tpl) + 1e-9)
        k = int(np.argmax(ncc))

        measured_f = (lo + k + (pk - a)) / SR * FPS
        resid = measured_f - c["target"]
        worst = max(worst, abs(resid))
        print(f"{c['note'][:34]:34s} {c['target']:8.2f} {measured_f:8.2f} {resid:+7.2f}  {ncc[k]:.2f}")

    verdict = "ĐẠT" if worst <= 0.5 else "CHƯA ĐẠT"
    print(f"\nLệch lớn nhất {worst:.2f}f → {verdict} (ngưỡng 0.5f)")
    sys.exit(0 if worst <= 0.5 else 1)


if __name__ == "__main__":
    main()
