"""propose_edit.py — sinh `propose_edit.json`: khung edit.json 1.1 do code cắt
sẵn cho stage PLAN (agent chép sang edit.json rồi sửa theo stages/PLAN.md).

Dùng:
    PYTHONIOENCODING=utf-8 python propose_edit.py <project_dir>

Khung gồm block 1,5–3 s cắt ở khoảng ngắt (hero là 2–4 từ cuối, style script)
và cú cắt máy 2–4 s xen toàn/cận. Hook, steps và CTA để trống — đó là phần
phán đoán của agent.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from thlib import editschema, rules

FILENAME = "propose_edit.json"


def run(project: Path) -> Path:
    """Ghi `propose_edit.json` vào thư mục dự án; trả về đường dẫn đã ghi."""
    project = Path(project)
    R = rules.load(project=project)
    words = json.loads((project / "words.json").read_text(encoding="utf-8"))
    pauses = json.loads((project / "pauses.json").read_text(encoding="utf-8"))

    proposal = editschema.propose(words, pauses, pauses["designed_breaks"], R)
    out = project / FILENAME
    out.write_text(json.dumps(proposal, ensure_ascii=False, indent=2), encoding="utf-8")
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Sinh khung edit.json 1.1 cho stage PLAN")
    ap.add_argument("project", help="Thư mục dự án (rules.lock, words.json, pauses.json)")
    args = ap.parse_args(argv)

    out = run(Path(args.project))
    proposal = json.loads(out.read_text(encoding="utf-8"))
    print(f"Đã ghi {out}")
    print(
        f"Khung có {len(proposal['blocks'])} block và {len(proposal['shots'])} cú cắt; "
        "hook/steps/cta để trống."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
