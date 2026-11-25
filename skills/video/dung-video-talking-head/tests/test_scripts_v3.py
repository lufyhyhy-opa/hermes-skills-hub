from pathlib import Path

from thlib import scripts_v3 as S

FIXTURES = Path(__file__).parent / "fixtures" / "scripts"


def test_v3_has_60_sections(v3_sections):
    assert sorted(v3_sections) == list(range(1, 61))
    assert v3_sections[2]["title"].startswith("Một ảnh sản phẩm")
    assert "APPLY" not in v3_sections[2]["script"]


def test_placeholders(v3_sections):
    assert "[CLAIM]" in v3_sections[37]["placeholders"]
    assert v3_sections[2]["placeholders"] == []


def test_paragraphs_video02(v3_sections):
    assert len(v3_sections[2]["paragraphs"]) == 6


def test_eval_rows_expand_ranges(eval_rows):
    nums = [r["row"] for r in eval_rows]
    assert 18 in nums and 43 in nums and 50 in nums


# --- Tự viết thêm test cho load_director / find_v3_file (interface có trong
# brief nhưng Step 1 không cho sẵn test; Task 4 sẽ dùng lại hai hàm này) ----


def test_v3_has_60_eval_rows_total():
    eval_rows = S.load_eval(FIXTURES / "60-kich-ban-heygen-talking-head.md")
    assert sorted(r["row"] for r in eval_rows) == list(range(1, 61))
    row18 = next(r for r in eval_rows if r["row"] == 18)
    assert row18["title"] == "Thoại như brochure"
    row45 = next(r for r in eval_rows if r["row"] == 45)  # thuộc dòng gộp 43–50
    assert row45["title"] == "Cộng đồng"


def test_load_director_has_60_sections():
    director = S.load_director(FIXTURES / "60-kich-ban-video-ngan-ai-vm-dabest.md")
    assert sorted(director) == list(range(1, 61))
    assert director[1]["title"] == "Ảnh AI giả không phải vì công cụ dở"
    assert director[1]["n"] == 1
    assert len(director[1]["body"]) > 0


def test_find_v3_file():
    found = S.find_v3_file(FIXTURES)
    assert found.name.startswith("60 k")
    assert "v3" in found.name
