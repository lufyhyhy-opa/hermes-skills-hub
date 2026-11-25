import json
from pathlib import Path

import pytest

import intake
from thlib import mapping, paths, scripts_v3

FIXTURES = Path(__file__).parent / "fixtures"


def test_list_videos_includes_loose(tmp_path):
    (tmp_path / "7").mkdir(); (tmp_path / "7" / "7.mp4").write_bytes(b"x")
    (tmp_path / "55.mp4").write_bytes(b"x")
    vids = mapping.list_videos(tmp_path)
    assert [(v["n"], v["loose"]) for v in vids] == [(7, False), (55, True)]


def test_list_videos_ignores_non_numeric_entries(tmp_path):
    # Layout thật (context task): A_Minh_*, B1..B19, Video_avatar* không phải
    # video theo số mục v3 — list_videos phải bỏ qua.
    (tmp_path / "A_Minh_demo").mkdir()
    (tmp_path / "B1").mkdir()
    (tmp_path / "Video_avatar_wolfgang.mp4").write_bytes(b"x")
    (tmp_path / "3").mkdir(); (tmp_path / "3" / "3.mp4").write_bytes(b"x")
    vids = mapping.list_videos(tmp_path)
    assert [v["n"] for v in vids] == [3]


def test_list_videos_folder_without_matching_mp4_is_skipped(tmp_path):
    (tmp_path / "9").mkdir()  # folder rỗng, chưa có 9.mp4
    vids = mapping.list_videos(tmp_path)
    assert vids == []


def test_match_and_classify_against_verified_scan(v3_sections, scan_rows, rules_110):
    for row in scan_rows:                       # audit/video_v3_mapping.csv (copied to fixtures)
        m = mapping.match_clip(row["heard"], v3_sections)
        n = int(row["video"].split()[0])
        c = mapping.classify({"n": n}, m, v3_sections, rules_110)
        if n in (31, 33, 37):
            assert c["status"] == "needs_rerender"
        elif n == 38:
            assert c["status"] == "needs_rerender"
        elif n == 34:
            assert c["status"] == "needs_input" and "35" in c["reasons"][0]
        elif n not in (32,):
            assert c["status"] == "ok", (n, c)


def test_classify_placeholder_requires_heard_word_too(v3_sections, rules_110):
    # Spec §6.1 điểm 3: "mục v3 có placeholder [IN HOA] VÀ whisper nghe thấy
    # chính từ đó" — cả hai vế, không chỉ cấu trúc. Mục 32 chỉ có 1
    # placeholder ("[CÔNG CỤ]") nên dễ tách hai ca: whisper đọc đúng chữ
    # placeholder (needs_rerender) so với whisper đọc thành lời tự nhiên
    # khác, không nhắc tới "công cụ" (không rơi vào nhánh placeholder).
    base_match = {"v3": 32, "score": 0.9, "second": 25, "second_score": 0.1, "motion_score": 0.0}

    literal = mapping.classify(
        {"n": 32}, {**base_match, "heard": "đừng tải công cụ chỉ vì thấy video viral"},
        v3_sections, rules_110,
    )
    assert literal == {"status": "needs_rerender", "reasons": ["placeholder"]}

    natural = mapping.classify(
        {"n": 32}, {**base_match, "heard": "đừng tải app chỉ vì thấy video viral"},
        v3_sections, rules_110,
    )
    assert natural == {"status": "ok", "reasons": []}


# --- Tự viết thêm test cho match_director / match_eval (interface có trong
# brief nhưng Step 1 không cho sẵn test, giống cách Task 3 đã làm với
# load_director/find_v3_file). Dùng 3 ví dụ ghép tiêu đề đúng trong spec §6.1
# điểm 2: phân loại/đạo diễn #18 ↔ v3 #16; #25 ↔ v3 #21; #31 ↔ v3 #27. ------


def test_match_director_by_title(v3_sections):
    director = scripts_v3.load_director(FIXTURES / "scripts" / "60-kich-ban-video-ngan-ai-vm-dabest.md")
    assert mapping.match_director(v3_sections[16], director) == 18
    assert mapping.match_director(v3_sections[21], director) == 25
    assert mapping.match_director(v3_sections[27], director) == 31


def test_match_eval_uses_director_row_as_key(v3_sections, eval_rows):
    director = scripts_v3.load_director(FIXTURES / "scripts" / "60-kich-ban-video-ngan-ai-vm-dabest.md")
    for v3_n, expected_row in ((16, 18), (21, 25), (27, 31)):
        director_row = mapping.match_director(v3_sections[v3_n], director)
        assert director_row == expected_row
        assert mapping.match_eval(v3_sections[v3_n], director_row, eval_rows) == expected_row


def test_match_eval_none_when_director_row_missing(v3_sections, eval_rows):
    assert mapping.match_eval(v3_sections[16], None, eval_rows) is None


# --- intake.py end-to-end trên video thật (đọc, không sửa) — chậm vì chạy
# whisper large-v3, đánh dấu slow (chạy với -m slow). Video 3/34/38 là 3 ca
# đại diện đã được audit/video_v3_mapping.csv xác nhận: ok / SỐ LỆCH /
# không khớp mục nào; video 2 (đã giao, D11) phải bị loại (C5). -----------


@pytest.mark.slow
def test_intake_real_three_videos(tmp_path, monkeypatch):
    monkeypatch.setattr(paths, "VID_ROOT", Path("D:/MMO/Van Minh AI/Vid Heygen"))
    rc = intake.main(["--batch", "_t", "--videos", "2,3,34,38", "--transcriber", "whisper",
                       "--out", str(tmp_path)])
    assert rc == 0

    manifest = json.loads((tmp_path / "batch_manifest.json").read_text(encoding="utf-8"))
    status_by_n = {v["n"]: v["status"] for v in manifest["videos"]}
    assert 2 not in status_by_n
    assert status_by_n[3] == "ok"
    assert status_by_n[34] == "needs_input"
    assert status_by_n[38] == "needs_rerender"

    # intake.py không được tạo folder cho video lẻ (34.mp4 không có folder
    # 34/) — mọi thứ chỉ ghi vào batch dir (--out).
    assert not Path("D:/MMO/Van Minh AI/Vid Heygen/34").exists()
