import pytest

from thlib import align


def ww(*spec):
    """Dựng từ whisper giả: ww(("chữ", s, e), ...)."""
    return [{"w": w, "s": s, "e": e} for w, s, e in spec]


def spans(res):
    return [(w["s"], w["e"]) for w in res["words"]]


def test_align_video02(v3_sections, fixture_v2_words):
    res = align.align(v3_sections[2]["script"], fixture_v2_words)
    assert res["score"] >= 0.95
    texts = [w["w"] for w in res["words"]]
    assert "trước" in texts                 # whisper heard 'cho'; display keeps the script word
    ss = [w["s"] for w in res["words"]]
    assert ss == sorted(ss)


def test_designed_breaks_video02(v3_sections, fixture_v2_words):
    res = align.align(v3_sections[2]["script"], fixture_v2_words)
    br = align.designed_breaks(v3_sections[2]["script"], res["words"])
    assert sum(1 for b in br if b["kind"] == "paragraph") == 5


def test_every_display_word_of_video02_gets_timing(v3_sections, fixture_v2_words):
    script = v3_sections[2]["script"]
    res = align.align(script, fixture_v2_words)
    W = res["words"]
    assert len(W) == len(script.split()) - 1          # chỉ bỏ đúng một token "..."
    assert [w["i"] for w in W] == list(range(len(W)))
    for w in W:
        assert isinstance(w["s"], float) and isinstance(w["e"], float) and w["e"] >= w["s"]
        assert w["src"] == "script" and w["guess"] is False
    assert res["guess_count"] == 0
    # '...' bị bỏ nên từ sau nó lùi một index; dấu câu cuối từ bị cắt.
    assert [W[k]["w"] for k in (7, 8, 9)] == ["20", "lần", "Một"]
    assert (W[7]["s"], W[7]["e"]) == (2.46, 3.08)     # từ khớp giữ nguyên mốc whisper
    assert (W[9]["s"], W[9]["e"]) == (3.8, 4.42)
    assert [W[k]["w"] for k in (154, 155)] == ["TÀI", "SẢN"]   # giữ nguyên chữ script
    tr = next(w for w in W if w["w"] == "trước")      # whisper nghe 'cho' -> nội suy
    assert (tr["s"], tr["e"]) == pytest.approx((38.08, 38.18))


def test_script_number_words_split_whisper_digit_span():
    whisper = ww(("Chụp", 0.0, 0.3), ("lại", 0.3, 0.5), ("20", 0.5, 1.1), ("lần.", 1.1, 1.4))
    res = align.align("Chụp lại hai mươi lần.", whisper)
    assert [w["w"] for w in res["words"]] == ["Chụp", "lại", "hai", "mươi", "lần"]
    assert spans(res) == pytest.approx([(0.0, 0.3), (0.3, 0.5), (0.5, 0.8), (0.8, 1.1), (1.1, 1.4)])
    assert res["score"] == 1.0


def test_whisper_number_words_merge_onto_script_digit():
    whisper = ww(("Chụp", 0.0, 0.3), ("hai", 0.5, 0.8), ("mươi", 0.8, 1.1), ("lần", 1.1, 1.4))
    res = align.align("Chụp 20 lần", whisper)
    assert res["words"][1]["w"] == "20"
    assert spans(res)[1] == (0.5, 1.1)


def test_unmatched_words_interpolated_between_neighbours():
    whisper = ww(("anh", 1.0, 1.2), ("zzz", 1.2, 1.5), ("học", 2.0, 2.4))
    res = align.align("Anh ấy đi học.", whisper)
    assert spans(res) == pytest.approx([(1.0, 1.2), (1.2, 1.6), (1.6, 2.0), (2.0, 2.4)])
    assert all(w["guess"] is False for w in res["words"])


def test_unmatched_edges_use_whisper_extent():
    whisper = ww(("xx", 0.5, 1.0), ("bê", 1.0, 1.5), ("xê", 1.5, 2.0), ("yy", 2.0, 2.6))
    res = align.align("a bê xê d", whisper)
    assert spans(res) == pytest.approx([(0.5, 1.0), (1.0, 1.5), (1.5, 2.0), (2.0, 2.6)])


def test_overlapping_whisper_neighbours_keep_starts_sorted():
    whisper = ww(("cáo", 1.0, 1.6), ("nhưng", 1.5, 2.0))
    res = align.align("cáo đây nhưng", whisper)
    ss = [w["s"] for w in res["words"]]
    assert ss == sorted(ss)


def test_designed_breaks_video02_positions(v3_sections, fixture_v2_words):
    script = v3_sections[2]["script"]
    W = align.align(script, fixture_v2_words)["words"]
    br = align.designed_breaks(script, W)
    assert br[0] == {"after_word": 8, "kind": "ellipsis"}          # "lần. ..."
    after = [W[b["after_word"] + 1]["w"] for b in br if b["kind"] == "paragraph"]
    assert after == ["Từ", "Nhưng", "Tôi", "AI", "Lưu"]             # spec §6.3


def test_designed_breaks_attached_and_unicode_ellipsis():
    script = "Xin chào... bạn\n\nTạm … biệt"
    W = align.align(script, [])["words"]
    assert [w["w"] for w in W] == ["Xin", "chào", "bạn", "Tạm", "biệt"]
    assert align.designed_breaks(script, W) == [
        {"after_word": 1, "kind": "ellipsis"},
        {"after_word": 2, "kind": "paragraph"},
        {"after_word": 3, "kind": "ellipsis"},
    ]


def test_designed_breaks_rejects_words_from_another_script():
    W = align.align("một hai ba", [])["words"]
    with pytest.raises(ValueError):
        align.designed_breaks("một hai", W)
