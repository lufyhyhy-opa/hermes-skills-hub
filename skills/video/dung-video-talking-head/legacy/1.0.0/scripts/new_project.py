# -*- coding: utf-8 -*-
"""Tạo project dựng video mới từ template của skill.

    python new_project.py --source "D:/.../1.mp4" --out "D:/.../1/edit"

Làm: copy template → --out, copy font (chỉ những file đã kiểm đủ dấu tiếng Việt)
và SFX vào public/, tạo master 1620×2880 (dư 1.5× để phóng không vỡ), ghi
edit.json khung, npm install. Không ghi đè project đã có.
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
DEFAULT_FONTS = "D:/MMO/Font/Cinematic fonts pack"

# tên đích (fonts.tsx đọc đúng tên này) ← đường dẫn trong font pack
FONTS = {
    "BeVietnamPro-Medium.ttf": "Font Việt hóa cinematic/Be_Vietnam_Pro/Be_Vietnam_Pro/BeVietnamPro-Medium.ttf",
    "BeVietnamPro-Bold.ttf": "Font Việt hóa cinematic/Be_Vietnam_Pro/Be_Vietnam_Pro/BeVietnamPro-Bold.ttf",
    "BeVietnamPro-Black.ttf": "Font Việt hóa cinematic/Be_Vietnam_Pro/Be_Vietnam_Pro/BeVietnamPro-Black.ttf",
    "BeVietnamPro-BlackItalic.ttf": "Font Việt hóa cinematic/Be_Vietnam_Pro/Be_Vietnam_Pro/BeVietnamPro-BlackItalic.ttf",
    "DTPhudu-Bold.otf": "DT-Phudu/Fonts Files/DTPhudu-Bold.otf",
    "DTPhudu-Black.otf": "DT-Phudu/Fonts Files/DTPhudu-Black.otf",
    "BebasNeue.otf": "Font Việt hóa cinematic/PS-Bebas-Neue-Regular-V1.1.otf",
    "Merolat.ttf": "Font Việt hóa cinematic/TF-Merolat-bs2kh4.ttf",
    "HeyMonday.ttf": "Font Việt hóa cinematic/TF-Hey-Monday-i0dzoo.ttf",
}


def run(cmd, **kw):
    print("  $", " ".join(str(c) for c in cmd))
    subprocess.run(cmd, check=True, **kw)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, help="video gốc (dọc 9:16)")
    ap.add_argument("--out", required=True, help="thư mục project mới")
    ap.add_argument("--fonts", default=DEFAULT_FONTS, help="thư mục font pack")
    ap.add_argument("--no-install", action="store_true")
    args = ap.parse_args()

    src, out, pack = Path(args.source), Path(args.out), Path(args.fonts)
    if not src.exists():
        sys.exit(f"Không thấy video: {src}")
    if (out / "package.json").exists():
        sys.exit(f"Đã có project ở {out} — không ghi đè. Chọn --out khác.")

    print("1/5 copy template")
    shutil.copytree(SKILL / "template", out, dirs_exist_ok=True)

    print("2/5 font")
    (out / "public" / "fonts").mkdir(parents=True, exist_ok=True)
    missing = []
    for dst, rel in FONTS.items():
        f = pack / rel
        if f.exists():
            shutil.copy2(f, out / "public" / "fonts" / dst)
        else:
            missing.append(rel)
    if missing:
        sys.exit("Thiếu font trong pack:\n  " + "\n  ".join(missing))

    print("3/5 SFX")
    shutil.copytree(SKILL / "assets" / "sfx", out / "public" / "sfx", dirs_exist_ok=True)

    print("4/5 master 1620x2880")
    probe = json.loads(subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height", "-of", "json", str(src)],
        capture_output=True, text=True, check=True).stdout)["streams"][0]
    if probe["width"] / probe["height"] > 0.6:
        print(f"  CẢNH BÁO: nguồn {probe['width']}x{probe['height']} không phải dọc 9:16 — sẽ bị crop giữa.")
    run(["ffmpeg", "-v", "error", "-stats", "-y", "-i", str(src),
         "-vf", "scale=1620:2880:force_original_aspect_ratio=increase:flags=lanczos,crop=1620:2880",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
         "-g", "30", "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
         str(out / "public" / "master.mp4")])

    spec = out / "edit.json"
    spec.write_text(json.dumps({
        "source": str(src).replace("\\", "/"),
        "fix": {},
        "hook": None,
        "blocks": [],
        "steps": None,
        "shots": [{"t": 0.0, "s0": 1.0, "s1": 1.04}],
        "cta": None,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    if not args.no_install:
        print("5/5 npm install")
        run(["npm", "install", "--no-audit", "--no-fund"], cwd=out, shell=(sys.platform == "win32"))

    print(f"\nXong: {out}\nTiếp: cd vào đó → python scripts/transcribe.py")


if __name__ == "__main__":
    main()
