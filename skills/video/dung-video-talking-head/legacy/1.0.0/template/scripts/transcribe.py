# -*- coding: utf-8 -*-
"""Bóc lời tiếng Việt kèm mốc thời gian từng từ (faster-whisper large-v3).

Đọc "source" trong edit.json, ghi:
    scripts/transcript.json   theo câu (để đọc)
    scripts/words.json        danh sách phẳng từng từ — edit.json trỏ vào đây bằng index
và in bảng index để chia block.

Chạy từ thư mục project:
    python scripts/transcribe.py                 # large-v3, tiếng Việt
    python scripts/transcribe.py --from 37.5     # nghe lại một đoạn nghi sai (chỉ in, không ghi)
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="large-v3")
    ap.add_argument("--lang", default="vi")
    ap.add_argument("--from", dest="start", type=float, help="chỉ nghe lại từ giây này (chế độ soát)")
    ap.add_argument("--to", dest="end", type=float)
    ap.add_argument("--prompt", help="gợi ý ngữ cảnh/từ khoá cho chế độ soát")
    args = ap.parse_args()

    from faster_whisper import WhisperModel

    src = json.loads((ROOT / "edit.json").read_text(encoding="utf-8"))["source"]
    wav = Path(tempfile.gettempdir()) / "vtt_audio.wav"
    cut = []
    if args.start is not None:
        cut += ["-ss", str(args.start)]
    if args.end is not None:
        cut += ["-to", str(args.end)]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, *cut, "-vn", "-ac", "1",
                    "-ar", "16000", "-acodec", "pcm_s16le", str(wav)], check=True)

    model = WhisperModel(args.model, device="cpu", compute_type="int8")
    review = args.start is not None
    segs, _ = model.transcribe(
        str(wav), language=args.lang, word_timestamps=not review, vad_filter=not review,
        beam_size=10 if review else 5, condition_on_previous_text=False,
        initial_prompt=args.prompt,
    )

    offset = args.start or 0.0
    if review:
        for s in segs:
            print(f"[{s.start + offset:6.2f}-{s.end + offset:6.2f}] {s.text.strip()}")
        return

    sentences, flat = [], []
    for s in segs:
        ws = [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)}
              for w in (s.words or []) if w.word.strip()]
        sentences.append({"start": round(s.start, 3), "end": round(s.end, 3),
                          "text": s.text.strip(), "words": ws})
        flat += ws

    out = ROOT / "scripts"
    (out / "transcript.json").write_text(json.dumps(sentences, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "words.json").write_text(json.dumps(flat, ensure_ascii=False), encoding="utf-8")

    for s in sentences:
        print(f"\n[{s['start']:6.2f}-{s['end']:6.2f}] {s['text']}")
    print("\n--- index từng từ (dùng trong edit.json) ---")
    for i, w in enumerate(flat):
        print(f"{i:4d} {w['s']:7.2f} {w['e']:7.2f}  {w['w']}")


if __name__ == "__main__":
    main()
