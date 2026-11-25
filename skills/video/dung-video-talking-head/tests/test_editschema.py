import json
from pathlib import Path

import pytest

import propose_edit
import validate_edit
from thlib import editschema, rules, state

FIXTURES = Path(__file__).parent / "fixtures"
EDIT_LEGACY = FIXTURES / "v2" / "edit_legacy.json"
EDIT_V11 = FIXTURES / "v2" / "edit_v11.json"


def _load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _codes(errors):
    return [e["code"] for e in errors]


# --- ba test của kế hoạch (Task 7 bước 1) ---------------------------------


def test_legacy_video2_violations(fixture_v2_whisper_words_on, fixture_v2_pauses_full):
    R = rules.load("1.1.0")
    legacy = _load(EDIT_LEGACY)
    W = fixture_v2_whisper_words_on          # chỉ số của edit cũ theo từ whisper
    errs = editschema.validate(editschema.from_legacy(legacy, W), W, fixture_v2_pauses_full, R)
    codes = _codes(errs)
    assert codes.count("STOMP_SPACING") >= 2
    assert codes.count("BLOCK_LEN") >= 7
    assert codes.count("HERO_WORDS") >= 2
    assert codes.count("SHOT_GAP") >= 3


def test_fixed_video2_edit_passes(fixture_v2_words_corrected, fixture_v2_pauses_full):
    R = rules.load("1.1.0")
    edit = _load(EDIT_V11)                   # chỉ số theo từ đã căn với lời chuẩn
    assert editschema.validate(edit, fixture_v2_words_corrected, fixture_v2_pauses_full, R) == []


def test_propose_is_valid(fixture_v2_words_corrected, fixture_v2_pauses_full):
    R = rules.load("1.1.0")
    W, P = fixture_v2_words_corrected, fixture_v2_pauses_full
    p = editschema.propose(W, P, P["designed_breaks"], R)
    skip = ("HIT_WORD", "CTA_RANGE")
    bad = [e for e in editschema.validate(p, W, P, R) if e["code"] not in skip]
    assert bad == []


# --- mỗi mã lỗi bắt được đúng lỗi của nó ----------------------------------


def _set_style(edit, block_id, style):
    next(b for b in edit["blocks"] if b["id"] == block_id)["style"] = style


MUTATIONS = [
    # (tên, cách phá bản edit_v11 hợp lệ, mã lỗi phải bắt được)
    ("thiếu hero", lambda e: e["blocks"][0].pop("hero"), "SCHEMA"),
    ("chỉ số vượt số từ", lambda e: e["blocks"][0].update(hero=[0, 9999]), "SCHEMA"),
    ("block quá ngắn", lambda e: (e["blocks"][0].update(bottom=None),
                                  e["blocks"][1].update(top=[3, 7])), "BLOCK_LEN"),
    ("hero 1 từ", lambda e: e["blocks"][0].update(hero=[0, 1], bottom=[1, 5]), "HERO_WORDS"),
    ("bỏ từ", lambda e: e["blocks"][0].update(bottom=None), "OVERLAP_OR_GAP"),
    ("hai stomp sát nhau", lambda e: _set_style(e, "b06", "stomp"), "STOMP_SPACING"),
    ("quá nhiều nhãn đập", lambda e: (_set_style(e, "b13", "stomp"),
                                      _set_style(e, "b15", "stomp")), "STOMP_LIKE_MAX"),
    ("reveal trên stomp", lambda e: e["blocks"][1].update(reveal=True), "REVEAL_STYLE"),
    ("hit_word ngoài hero stomp", lambda e: e["hook"].update(hit_word=20), "HIT_WORD"),
    ("cta thiếu range", lambda e: e["cta"].pop("range"), "CTA_RANGE"),
    ("stomp nuốt từ khoá CTA", lambda e: _set_style(e, "b17", "stomp"), "CTA_KEYWORD_IN_STOMP"),
    ("scale quá lớn", lambda e: e["shots"][0].update(s1=1.30), "SCALE"),
    ("thiếu một cú cắt", lambda e: e["shots"].pop(1), "SHOT_GAP"),
    ("cắt giữa câu", lambda e: e["shots"][1].update(cut_at_word=30), "CUT_SNAP"),
]


@pytest.mark.parametrize("name,mutate,code", MUTATIONS, ids=[m[0] for m in MUTATIONS])
def test_validate_catches(name, mutate, code, fixture_v2_words_corrected, fixture_v2_pauses_full):
    R = rules.load("1.1.0")
    edit = _load(EDIT_V11)
    mutate(edit)
    errs = editschema.validate(edit, fixture_v2_words_corrected, fixture_v2_pauses_full, R)
    assert code in _codes(errs)
    assert all(e["msg"] and e["where"] for e in errs)


def _block_between_items(e):
    """Mục 3 của bảng (từ 36–39) thành block bx chen giữa mục 2 và mục 4."""
    e["steps"]["items"].pop(2)
    bx = dict(e["blocks"][3], id="bx", top=None, hero=[36, 40], bottom=None)
    e["blocks"].insert(4, bx)


def test_steps_items_contiguous_and_no_block_inside(fixture_v2_words_corrected, fixture_v2_pauses_full):
    """B5: bảng liệt kê là 3–5 mục LIỀN NHAU và không block nào bắt đầu trong khoảng bảng
    [từ đầu mục 1, hết mục cuối) — block chen giữa làm thẻ ra sớm (R34), các mục sau không
    bao giờ hiện. Luật 1.0.0: "Trong khoảng thời gian của bảng không đặt block"."""
    R = rules.load("1.1.0")
    W, P = fixture_v2_words_corrected, fixture_v2_pauses_full

    def check(mutate):
        edit = _load(EDIT_V11)
        mutate(edit)
        return editschema.validate(edit, W, P, R)

    errs = check(_block_between_items)
    steps = [e for e in errs if e["code"] == "STEPS"]
    assert {e["where"] for e in steps} == {"steps.items[2]", "bx"}, errs

    def gap(e):                                          # mục 2 bỏ từ 32: mục không liền nhau
        e["steps"]["items"][1]["range"] = [33, 36]
    assert "steps.items[1]" in {e["where"] for e in check(gap) if e["code"] == "STEPS"}

    for n in (2, 6):                                     # schema: 3–5 mục
        def resize(e, n=n):
            items = e["steps"]["items"]
            e["steps"]["items"] = items[:n] if n < len(items) else items + [dict(items[-1])]
        assert _codes(check(resize)) and set(_codes(check(resize))) == {"SCHEMA"}, n


def test_cta_label_and_keyword_length(fixture_v2_words_corrected, fixture_v2_pauses_full):
    """B2: nhãn và từ khoá của pill CTA có trần độ dài (rules text.cta_*_max_chars) để pill
    vừa hộp chữ mà chữ không co quá nhỏ; video 02 ("Bình luận" / "5 TÀI SẢN") đạt, và từ khoá
    dài nhất trong 60 kịch bản kênh ("BRIEF TRƯỚC TOOL", 16 ký tự) cũng đạt."""
    R = rules.load("1.1.0")
    W, P = fixture_v2_words_corrected, fixture_v2_pauses_full
    lab, key = R.get("text.cta_label_max_chars"), R.get("text.cta_keyword_max_chars")
    assert (lab, key) == (14, 16)

    def errs(**cta):
        edit = _load(EDIT_V11)
        edit["cta"].update(cta)
        return [e for e in editschema.validate(edit, W, P, R) if e["code"] == "CTA_TEXT"]
    assert errs() == [] and errs(keyword="BRIEF TRƯỚC TOOL", label="x" * lab) == []
    assert [e["where"] for e in errs(label="x" * (lab + 1))] == ["cta.label"]
    assert [e["where"] for e in errs(keyword="Y" * (key + 1))] == ["cta.keyword"]


def _shot_gaps(errs):
    return {e["where"]: e["msg"] for e in errs if e["code"] == "SHOT_GAP"}


def test_shot_gap_covers_both_video_edges(fixture_v2_words_corrected, fixture_v2_pauses_full):
    """B4 / §9.1 SHOT_GAP 2–4 s ở cả hai mép video: shot đầu chạy từ t = 0 (R24) nên cú cắt
    thật đầu tiên đo từ 0 s, không từ on(từ 0); từ cú cắt cuối tới t_end (S27) ≤ 4 s, trừ khi
    shot cuối cắt ở/sau từ đầu câu CTA (shot đẩy vào CTA). Một shot tĩnh 43 s phải FAIL."""
    R = rules.load("1.1.0")
    W, P = fixture_v2_words_corrected, fixture_v2_pauses_full
    base = _load(EDIT_V11)
    assert editschema.validate(base, W, P, R) == []    # shot cuối (w147 = cta.range[0]) dài 4,1 s: miễn

    single = dict(base, shots=base["shots"][:1])
    assert "shots[0]" in _shot_gaps(editschema.validate(single, W, P, R))

    no_push = dict(base, shots=base["shots"][:-1])     # shot cuối ở w133 (36,1 s): 7 s tới t_end
    assert "shots[12]" in _shot_gaps(editschema.validate(no_push, W, P, R))
    no_cta = dict(base, cta=None)                      # hết miễn trừ CTA: 4,1 s > 4 s
    assert "shots[13]" in _shot_gaps(editschema.validate(no_cta, W, P, R))

    words = [dict(w) for w in W]
    words[9]["on"] = 4.2                               # 4,2 s từ t = 0 nhưng 3,93 s từ on(từ 0)
    late = json.loads(json.dumps(base))
    late["shots"][1]["cut_at_word"] = 9
    assert "shots[1]" in _shot_gaps(editschema.validate(late, words, P, R))


# --- from_legacy: giây -> chỉ số từ ---------------------------------------


def _fake_words(n):
    return [
        {"i": k, "w": f"t{k}", "s": k * 1.0, "e": k * 1.0 + 0.5, "on": k * 1.0}
        for k in range(n)
    ]


def test_from_legacy_converts_seconds_and_fix():
    words = _fake_words(10)
    legacy = {
        "source": "D:/x/1.mp4",
        "fix": {"5": "Ánh sáng"},
        "hook": {"text": "20", "color": "warn"},
        "blocks": [
            {"id": "b01", "top": [0, 2], "hero": [2, 4], "style": "script"},
            {"id": "b02", "hero": [4, 7], "bottom": [7, 10], "style": "stomp", "color": "gold",
             "accent": 1},
        ],
        "steps": None,
        "shots": [{"t": 0.0, "s0": 1.0, "s1": 1.04},
                  {"t": 3.2, "s0": 1.16, "s1": 1.20, "y": -0.06}],
        "cta": {"label": "Bình luận", "keyword": "PROMPT", "start": 6.5},
    }
    edit = editschema.from_legacy(legacy, words)

    assert edit["schema"] == "edit/1.1"
    assert [s["cut_at_word"] for s in edit["shots"]] == [0, 4]      # từ đầu có s >= t
    assert edit["shots"][1]["y"] == -0.06
    assert edit["cta"]["range"] == [7, 10]                          # từ "Bình luận" tới hết lời
    assert edit["hook"] == {"text": "20", "color": "warn", "hit_word": None}
    assert edit["blocks"][1]["display"] == {"5": "Ánh sáng"}        # fix -> display của block
    assert edit["blocks"][0]["bottom"] is None and edit["blocks"][0]["reveal"] is False
    assert "source" not in edit and "fix" not in edit


# --- CLI ------------------------------------------------------------------


@pytest.fixture
def v2_project(tmp_path, fixture_v2_words_corrected, fixture_v2_pauses_full):
    """Dự án tạm của video 2: rules.lock + words.json + pauses.json + edit.json."""
    state.write_lock(tmp_path, "1.1.0")
    (tmp_path / "words.json").write_text(
        json.dumps(fixture_v2_words_corrected, ensure_ascii=False), encoding="utf-8"
    )
    (tmp_path / "pauses.json").write_text(
        json.dumps(fixture_v2_pauses_full, ensure_ascii=False), encoding="utf-8"
    )
    (tmp_path / "edit.json").write_text(EDIT_V11.read_text(encoding="utf-8"), encoding="utf-8")
    return tmp_path


def test_validate_edit_cli_pass_and_fail(v2_project, capsys):
    assert validate_edit.main([str(v2_project)]) == 0
    assert "ĐẠT" in capsys.readouterr().out

    edit = _load(v2_project / "edit.json")
    edit["shots"].pop(1)
    (v2_project / "edit.json").write_text(json.dumps(edit, ensure_ascii=False), encoding="utf-8")
    assert validate_edit.main([str(v2_project)]) == 1
    assert "SHOT_GAP" in capsys.readouterr().out


def test_validate_edit_cli_legacy_mode(v2_project, capsys):
    code = validate_edit.main([str(v2_project), "--legacy", str(EDIT_LEGACY)])
    out = capsys.readouterr().out
    assert code == 1
    assert out.count("STOMP_SPACING") >= 2 and out.count("BLOCK_LEN") >= 7


def test_propose_edit_cli_writes_valid_skeleton(v2_project, capsys):
    assert propose_edit.main([str(v2_project)]) == 0
    out = capsys.readouterr().out
    proposal = _load(v2_project / "propose_edit.json")
    assert "propose_edit.json" in out
    assert proposal["schema"] == "edit/1.1"
    assert proposal["hook"] is None and proposal["cta"] is None
    assert len(proposal["blocks"]) >= 10
