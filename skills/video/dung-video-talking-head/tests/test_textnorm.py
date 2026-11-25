from thlib.textnorm import norm, norm_tokens, similarity


def test_numbers():
    assert norm("hai mươi lăm người") == ["25", "người"]
    assert norm("một trăm hai mươi") == ["120"]
    assert norm("mười lăm phút") == ["15", "phút"]
    assert norm("năm loại content") == ["5", "loại", "content"]
    assert norm("90 % ảnh") == ["90%", "ảnh"]
    assert norm("chín mươi phần trăm") == ["90%"]


def test_indices_track_source_words():
    toks = norm_tokens("Chụp lại hai mươi lần.")
    assert toks == [("chụp", [0]), ("lại", [1]), ("20", [2, 3]), ("lần", [4])]


def test_similarity_video02_script_vs_whisper(fixture_v2_words, v3_sections):
    whisper = " ".join(w["w"] for w in fixture_v2_words)
    assert similarity(norm(v3_sections[2]["script"]), norm(whisper)) >= 0.97


def test_number_homonyms_stay_literal_words():
    # "tư"/"lẻ" cũng là từ tiếng Việt thường (đầu tư, tư duy, riêng lẻ) —
    # đứng một mình (không nối tiếp một từ số khác) thì KHÔNG phải là số.
    assert norm("Tôi đầu tư vào bản đó") == ["tôi", "đầu", "tư", "vào", "bản", "đó"]
    assert norm("Tư duy tiết kiệm") == ["tư", "duy", "tiết", "kiệm"]
    assert norm("công cụ riêng lẻ") == ["công", "cụ", "riêng", "lẻ"]


def test_number_homonyms_still_parse_inside_a_real_number():
    # Nhưng khi nối tiếp một từ số khác đã mở đoạn thì vẫn là số bình thường.
    assert norm("hai mươi tư người") == ["24", "người"]
    assert norm("một trăm linh năm") == ["105"]


def test_number_run_does_not_swallow_next_sentence_enumerator():
    # Lỗi thật trên §41: câu hỏi kết bằng "không" (phủ định) đứng ngay trước
    # enumerator số của câu kế, sau khi dấu câu bị bỏ — "không? Một," từng bị
    # gộp thành một token "0" duy nhất, nuốt mất chỉ số của "Một".
    toks = norm_tokens(
        "Có đúng brief không? Một, có nhất quán không? Hai, "
        "có dùng được không? Ba, có lặp lại không? Bốn, xong."
    )
    digit_tokens = [(t, idx) for t, idx in toks if t.isdigit()]
    assert [t for t, _ in digit_tokens] == ["0", "1", "0", "2", "0", "3", "0", "4"]
    # mỗi token số chỉ gộp đúng MỘT chỉ số nguồn — không nuốt từ của câu khác.
    assert all(len(idx) == 1 for _, idx in digit_tokens)
