"""validate_edit.py — cổng của stage PLAN: kiểm edit.json theo luật edit/1.1.

Dùng:
    PYTHONIOENCODING=utf-8 python validate_edit.py <project_dir>
    PYTHONIOENCODING=utf-8 python validate_edit.py <project_dir> --legacy <edit.json 1.0.0>

Đọc rules.lock (khoá version luật), words.json, pauses.json và edit.json của
dự án. Chế độ --legacy đổi một edit.json 1.0.0 (có giây) sang schema 1.1 rồi
kiểm bản đã đổi — chỉ số từ của file cũ phải ứng với words.json của dự án.
In từng lỗi theo mã (xem stages/PLAN.md) và thoát mã 1 khi còn lỗi.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path

from thlib import editschema, rules


def _load(path: Path) -> dict | list:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def run(project: Path, legacy: str | None = None) -> tuple[str, list[dict]]:
    """Trả về (tên file đã kiểm, danh sách lỗi)."""
    project = Path(project)
    R = rules.load(project=project)
    words = _load(project / "words.json")
    pauses = _load(project / "pauses.json")

    if legacy:
        name = f"{Path(legacy).name} (đã đổi sang {editschema.SCHEMA_ID})"
        edit = editschema.from_legacy(_load(legacy), words)
    else:
        name = "edit.json"
        edit = _load(project / "edit.json")

    return name, editschema.validate(edit, words, pauses, R)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Kiểm edit.json theo luật edit/1.1")
    ap.add_argument(
        "project", help="Thư mục dự án (rules.lock, words.json, pauses.json, edit.json)"
    )
    ap.add_argument("--legacy", help="Kiểm một edit.json 1.0.0 sau khi đổi sang 1.1")
    args = ap.parse_args(argv)

    name, errors = run(Path(args.project), args.legacy)
    if not errors:
        print(f"ĐẠT: {name} không vi phạm luật nào")
        return 0

    print(f"FAIL: {name} có {len(errors)} lỗi")
    for e in errors:
        print(f"  {e['code']:<21} {e['where']:<14} {e['msg']}")
    counts = Counter(e["code"] for e in errors)
    print("Tổng: " + ", ".join(f"{code} x{n}" for code, n in sorted(counts.items())))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
