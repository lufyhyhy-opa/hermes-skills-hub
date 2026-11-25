"""Trích bảng cue SFX cũ của video 2 từ script.ts sang JSON tĩnh, làm fixture kiểm
thử (đối chiếu với planner mới ở các task sau). Chỉ đọc script.ts (read-only),
không sửa gì trong Vid Heygen/2/edit. Chạy một lần, kết quả old_cues.json được commit.
"""

from __future__ import annotations

import json
from pathlib import Path

SRC = Path("D:/MMO/Van Minh AI/Vid Heygen/2/edit/src/data/script.ts")
OUT = Path(__file__).parent / "old_cues.json"
MARK = "export const SFX: Cue[] = "


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    start = text.index(MARK) + len(MARK)
    end = text.rindex(";")
    cues = json.loads(text[start:end])
    OUT.write_text(json.dumps(cues, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Đã ghi {len(cues)} cue cũ vào {OUT}")


if __name__ == "__main__":
    main()
