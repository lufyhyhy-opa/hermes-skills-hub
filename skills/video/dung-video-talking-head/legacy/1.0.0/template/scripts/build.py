# -*- coding: utf-8 -*-
"""edit.json + scripts/words.json + public/sfx/  →  src/data/script.ts

Mọi thứ riêng của một video nằm trong edit.json. File này chỉ biến nó thành
dữ liệu cho Remotion, kể cả bảng SFX (tự suy ra từ block/step/shot, không
viết frame tay).

Chạy từ thư mục project:
    python scripts/build.py
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
FPS = 30

# Phải khớp với Subtitle.tsx (LEAD) và Hook.tsx (HOOK_TIMING).
LEAD = 0.05
ARRIVE_F = 3                 # chữ đọc ra "tới nơi" ~3f sau khi bắt đầu hiện
HOOK_TIMING = {"land": 0.34, "out": 1.08, "end": 1.5}

# Remotion 4.x + AAC 48kHz mp4: encoder priming làm cả track tiếng trễ ~1.28f.
# Đổi phiên bản Remotion / codec / sample rate / container → đo lại bằng check_av_sync.py.
OUTPUT_AUDIO_OFFSET_F = 1.28

# Từ vựng SFX cho video người nói: whoosh / impact / pop / sparkle.
# Không dùng tiếng UI tổng hợp (tone, bleep, notify) — nghe như game.
SFX = {
    "hook": ("impact/bass-hit-short.mp3", 0.55),
    "stomp": (("impact/hit-blow.mp3", "impact/bass-hit-short.mp3"), 0.42),
    "hero": (("transition/swoosh-quick.mp3", "transition/sweep-short.mp3"), 0.2),
    "card": ("transition/swoosh-quick.mp3", 0.26),
    "item": ("ui/pop-electric.mp3", 0.4),   # ui/pop.mp3 không rõ nguồn → không dùng thương mại
    "cta": ("light/sparkle-touch.mp3", 0.3),
    "cut": ("transition/air-woosh-quick.mp3", 0.14),
}
CUT_MIN_JUMP = 0.12          # chỉ whoosh những cú cắt đổi cỡ cảnh rõ rệt
CUT_CLEAR_F = 10             # bỏ whoosh cắt nếu đã có cue khác trong ±10f

# SFX rơi vào lúc đang nói phải thấp hơn giọng ít nhất DUCK_DB (so RMS 100ms),
# không thì impact/bass đè mất chữ. Trong khoảng lặng thì giữ âm lượng thiết kế.
DUCK_DB = 3.0
VO_ACTIVE_DB = -35.0
SR = 48000


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def duration_s(src):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", src],
        capture_output=True, text=True, check=True,
    ).stdout
    return float(out.strip())


def pcm(path):
    raw = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-vn", "-ac", "1", "-ar", str(SR),
         "-f", "s16le", "-"],
        capture_output=True, check=True,
    ).stdout
    return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768


def rms_env(x, win_s=0.1):
    w = int(SR * win_s)
    return np.sqrt(np.convolve(x ** 2, np.ones(w) / w, mode="same"))


def peak_lag_f(x):
    """Số frame từ đầu file tới đỉnh năng lượng — căn theo đỉnh, không theo đầu file."""
    env = np.convolve(np.abs(x), np.ones(240) / 240, mode="same")  # đường bao 5ms
    return float(np.argmax(env)) / SR * FPS


def build_words(words, fix):
    fix = {int(k): v for k, v in fix.items()}

    def clean(i):
        return re.sub(r"[,.!?]$", "", fix.get(i, words[i]["w"]))

    def rng(r):
        if not r:
            return []
        a, b = r
        return [{"t": clean(i), "s": words[i]["s"], "e": words[i]["e"]} for i in range(a, b)]

    return rng


def build_blocks(spec, rng):
    out = []
    for b in spec["blocks"]:
        top, hero, bottom = rng(b.get("top")), rng(b["hero"]), rng(b.get("bottom"))
        allw = top + hero + bottom
        out.append({
            "id": b["id"],
            "start": round(min(w["s"] for w in allw), 3),
            "end": round(max(w["e"] for w in allw), 3),
            "style": b.get("style", "script"),
            "color": b.get("color"),
            "accent": b.get("accent"),
            "top": top, "hero": hero, "bottom": bottom,
        })
    return out


def build_steps(spec, rng):
    st = spec.get("steps")
    if not st:
        return None
    items = []
    for it in st["items"]:
        ws = rng(it["range"])
        items.append({"label": it["label"], "start": ws[0]["s"], "end": ws[-1]["e"]})
    return {
        "title": st["title"],
        "items": items,
        "in": round(items[0]["start"] - 0.29, 3),
        "out": round(items[-1]["end"] + 0.15, 3),
    }


def build_sfx(blocks, steps, shots, hook, cta, sfx_dir, vo):
    info = {}   # src -> (peak_lag_f, rms_max)
    vo_env = rms_env(vo)

    def meta(src):
        if src not in info:
            f = sfx_dir / src
            if not f.exists():
                sys.exit(f"Thiếu file SFX: {f}")
            x = pcm(f)
            info[src] = (peak_lag_f(x), float(rms_env(x).max()))
        return info[src]

    def duck(vol, src, target_f):
        a = max(0, int((target_f / FPS - 0.1) * SR))
        b = int((target_f / FPS + 0.3) * SR)
        local = float(vo_env[a:b].max()) if b > a else 0.0
        if 20 * np.log10(local + 1e-9) < VO_ACTIVE_DB:
            return vol
        return min(vol, local * 10 ** (-DUCK_DB / 20) / meta(src)[1])

    cues = []

    def add(target_f, kind, note, n=0, vol_scale=1.0):
        srcs, vol = SFX[kind]
        src = srcs[n % len(srcs)] if isinstance(srcs, tuple) else srcs
        lag, _ = meta(src)
        want = vol * vol_scale
        got = duck(want, src, target_f)
        cues.append({
            "from": max(0, round(target_f - lag - OUTPUT_AUDIO_OFFSET_F)),
            "target": round(target_f, 2),   # giữ phần lẻ: đích thật, không phải đích đã làm tròn
            "src": f"sfx/{src}",
            "volume": round(got, 3),
            "note": note + (f"  [hạ {want:.2f}→{got:.2f} tránh lấn giọng]" if got < want - 0.005 else ""),
        })

    if hook:
        add(HOOK_TIMING["land"] * FPS - 2, "hook", f"hook '{hook['text']}' đập xuống")

    n_hero = n_stomp = 0
    for b in blocks:
        t = (b["hero"][0]["s"] - LEAD) * FPS + ARRIVE_F
        label = " ".join(w["t"] for w in b["hero"])
        if b["style"] in ("stomp", "quote"):
            add(t, "stomp", f"{b['id']} chữ đập: {label}", n_stomp)
            n_stomp += 1
        else:
            # hai mẫu xen kẽ + nhịp âm lượng lệch nhẹ: chống cảm giác "súng máy"
            add(t, "hero", f"{b['id']} hero: {label}", n_hero, 1.0 if n_hero % 2 == 0 else 0.85)
            n_hero += 1

    if steps:
        add(steps["in"] * FPS + 4, "card", "bảng liệt kê trượt vào")
        for i, it in enumerate(steps["items"]):
            # thang âm lượng giảm dần = cảm giác xa dần, không lặp máy móc
            add(it["start"] * FPS + 2, "item", f"mục {i + 1}: {it['label']}", vol_scale=1 - 0.1 * i)

    if cta:
        add(cta["start"] * FPS + 6, "cta", "CTA hiện")

    taken = [c["target"] for c in cues]
    for prev, cur in zip(shots, shots[1:]):
        if abs(cur["s0"] - prev["s1"]) < CUT_MIN_JUMP:
            continue
        f = cur["t"] * FPS
        if any(abs(f - t) <= CUT_CLEAR_F for t in taken):
            continue
        add(f, "cut", f"cắt cỡ cảnh {prev['s1']:.2f}→{cur['s0']:.2f}")

    return sorted(cues, key=lambda c: c["from"]), {k: v[0] for k, v in info.items()}


TS_HEAD = """// TỰ SINH bởi scripts/build.py từ edit.json — đừng sửa tay, sửa edit.json rồi chạy lại.
export type Word = { t: string; s: number; e: number };
export type Block = {
  id: string; start: number; end: number;
  style: "script" | "stomp" | "quote";
  color: "warn" | "gold" | "ink" | null;
  accent: number | null;
  top: Word[]; hero: Word[]; bottom: Word[];
};
export type Steps = { title: string; in: number; out: number; items: { label: string; start: number; end: number }[] };
export type Shot = { t: number; s0: number; s1: number; x?: number; y?: number };
export type Hook = { text: string; color: "warn" | "gold" | "ink"; land: number; out: number; end: number };
export type Cta = { label: string; keyword: string; start: number };
export type Cue = { from: number; target: number; src: string; volume: number; note: string };
"""


def main():
    spec = load(ROOT / "edit.json")
    words = load(ROOT / "scripts" / "words.json")
    rng = build_words(words, spec.get("fix", {}))

    dur = duration_s(spec["source"])
    blocks = build_blocks(spec, rng)
    steps = build_steps(spec, rng)
    shots = spec["shots"]
    hook = {**spec["hook"], **HOOK_TIMING} if spec.get("hook") else None
    cta = spec.get("cta")
    cues, peak = build_sfx(blocks, steps, shots, hook, cta, ROOT / "public" / "sfx", pcm(spec["source"]))

    j = lambda v: json.dumps(v, ensure_ascii=False, indent=1)
    ts = TS_HEAD + f"""
export const DURATION_S = {dur};
export const DURATION_F = {round(dur * FPS)};
export const HOOK: Hook | null = {j(hook)};
export const BLOCKS: Block[] = {j(blocks)};
export const STEPS: Steps | null = {j(steps)};
export const SHOTS: Shot[] = {j(shots)};
export const CTA: Cta | null = {j(cta)};
export const SFX: Cue[] = {j(cues)};
"""
    out = ROOT / "src" / "data" / "script.ts"
    out.write_text(ts, encoding="utf-8")

    print(f"→ {out.relative_to(ROOT)}  | {dur:.2f}s = {round(dur * FPS)}f | "
          f"{len(blocks)} block | {len(steps['items']) if steps else 0} mục | "
          f"{len(shots)} shot | {len(cues)} SFX")
    for src, lag_f in sorted(peak.items()):
        print(f"   peak {lag_f:5.2f}f  {src}")
    for c in cues:
        if "[hạ" in c["note"]:
            print(f"   f{c['from']:5d}  {c['note']}")


if __name__ == "__main__":
    main()
