# tests/test_picture.py — khoá hình (picture_lock), script.ts và cổng text-safe
# (Task 11, 11f, 11g, 11h; S08, S20, S22, S24, S27, B14; phán quyết R22–R26, R29–R34).
import copy
import json
import math
import re
import shutil
import subprocess

import numpy as np
import pytest

import check_text_safe
from thlib import paths, picture, state

TEMPLATE = paths.release_dir("1.1.0") / "template"
# Hai easing của template (src/anim.ts), chép sang Python để so frame đồng bộ.
OUT_CUBIC_TS = "outCubic: (t: number) => 1 - Math.pow(1 - t, 3)"
OUT_BACK_TS = "outBack: (t: number) => 1 + 2.2 * Math.pow(t - 1, 3) + 1.4 * Math.pow(t - 1, 2)"


def out_cubic(t):
    return 1 - (1 - t) ** 3


def out_back(t):
    return 1 + 2.2 * (t - 1) ** 3 + 1.4 * (t - 1) ** 2


def _src(rel):
    return (TEMPLATE / "src" / rel).read_text(encoding="utf-8")


def _const(src, name):
    return int(re.search(r"const %s = (\d+)" % name, src).group(1))


def _block(lock, bid):
    return next(b for b in lock["blocks"] if b["id"] == bid)


def _cand(plan, cid):
    return next(c for c in plan["candidates"] if c["id"] == cid)


def _words(block):
    return block["top"] + block["hero"] + block["bottom"]


def _first_show(block):
    return min(w["show"] for w in _words(block))


def _last_show(block):
    return max(w["show"] for w in _words(block))


def _reveal():
    """REVEAL của Subtitle.tsx: số frame một từ hiện xong."""
    return _const(_src("comp/Subtitle.tsx"), "REVEAL")


def _progress(f, show, reveal, fps=30):
    """Tiến độ hiện (outCubic) ở frame f của từ hiện ở `show` — wordP của Subtitle.tsx."""
    return out_cubic(min(1, max(0, (f - show * fps) / reveal)))


def _f90(show, reveal, fps=30):
    """Frame đầu tiên từ hiện ở `show` đạt ≥ 90 % tiến độ."""
    f = math.floor(show * fps)
    while _progress(f, show, reveal, fps) < 0.9:
        f += 1
    return f


def _last_word_run(block, reveal, fps=30):
    """Số frame liên tiếp dài nhất mà từ hiện sau cùng của block đậm ≥ 90 % trên hình:
    tiến độ hiện × (1 − tiến độ thoát tuyến tính qua exit_f frame từ out), chỉ trong cửa
    sổ Subtitle.tsx vẽ block [show đầu·fps − 2, out·fps + exit_f]."""
    last, out, ex = _last_show(block), block["out"], block["exit_f"]
    best = run = 0
    for f in range(math.ceil(_first_show(block) * fps - 2), math.floor(out * fps + ex) + 1):
        q = min(1, max(0, (f - out * fps) / ex))
        run = run + 1 if _progress(f, last, reveal, fps) * (1 - q) >= 0.9 else 0
        best = max(best, run)
    return best


def _gate(lock, i):
    """Lúc block i phải tắt xong: steps.in với block cuối trước thẻ liệt kê, không thì
    show đầu của block sau (None với block cuối video)."""
    blocks, steps = lock["blocks"], lock["steps"]
    nxt = blocks[i + 1] if i + 1 < len(blocks) else None
    if steps and _first_show(blocks[i]) < steps["in"] and (nxt is None or _first_show(nxt) >= steps["in"]):
        return steps["in"]
    return None if nxt is None else _first_show(nxt)


def _card_cue_plan(plan):
    """Bản sao sfx_plan có cue thẻ OK ở frame 255 (đỉnh 8,5 s) — thẻ vào ở 8,30 s."""
    plan = copy.deepcopy(plan)
    card = _cand(plan, "card@w28")
    cue = dict(plan["cues"][0], id=card["id"], role="card", tier="B", frame=255, peak_s=8.5)
    card.update(decision="OK", rule=None, cue={k: v for k, v in cue.items() if k not in ("id", "role", "tier")})
    plan["cues"] = sorted(plan["cues"] + [cue], key=lambda c: c["peak_s"])
    return plan


# ------------------------------------------------ S24: frame đồng bộ khớp code template


def test_sync_frames_match_template_easing():
    src = open("releases/1.1.0/template/src/comp/Subtitle.tsx", encoding="utf-8").read()
    reveal = int(re.search(r"const REVEAL = (\d+)", src).group(1))
    out_cubic = lambda t: 1 - (1 - t) ** 3
    first90 = next(f for f in range(reveal + 1) if out_cubic(f / reveal) >= 0.9)
    assert first90 == 5          # rules sfx.sync_frame.block


def test_every_sync_frame_matches_template_code(rules_110):
    """S24: frame đồng bộ trong rules.json = frame đầu tiên animation tương ứng
    trong template đạt ≥ 90 % tiến độ (chữ block, thẻ, mục, pill CTA, tít hook)."""
    anim = _src("anim.ts")
    assert OUT_CUBIC_TS in anim and OUT_BACK_TS in anim
    sync, fps = rules_110.get("sfx.sync_frame"), rules_110.get("fps")
    steps, cta = _src("comp/StepList.tsx"), _src("comp/Cta.tsx")
    assert picture.SYNC_PROGRESS(_const(_src("comp/Subtitle.tsx"), "REVEAL"), out_cubic) == sync["block"]
    assert picture.SYNC_PROGRESS(_const(steps, "ENTER"), out_cubic) == sync["card"]
    assert picture.SYNC_PROGRESS(_const(steps, "ITEM"), out_cubic) == sync["item"]
    assert picture.SYNC_PROGRESS(_const(cta, "POP"), out_back) == sync["cta_pill"]
    assert picture.SYNC_PROGRESS(picture.HOOK_TIMING["land"] * fps, out_cubic) == sync["hook_title"]
    # S22: tít hook chạm đích trước frame 9 và còn trên hình tới ≥ 1,5 s.
    assert sync["hook_title"] < 9 and picture.HOOK_TIMING["end"] >= 1.5


# ------------------------------------------------ S08: chữ của sự kiện có tiếng


def test_synced_block_shows_top_and_hero_together(v2_lock):
    b = next(b for b in v2_lock["blocks"] if b["synced"])
    shows = {w["show"] for w in b["top"] + b["hero"]}
    assert len(shows) == 1


def test_unsynced_words_show_at_onset_minus_lead(v2_lock, fixture_v2_words_corrected, rules_110):
    """Mặc định mỗi chữ hiện ở on − text.lead_s (block b01 không có tiếng)."""
    words, lead = fixture_v2_words_corrected, rules_110.get("text.lead_s")
    b01 = _block(v2_lock, "b01")
    assert not b01["synced"] and b01["top"] == []
    assert [w["show"] for w in b01["hero"] + b01["bottom"]] == [
        round(words[k]["on"] - lead, 4) for k in range(0, 5)]
    assert [w["t"] for w in b01["hero"]] == [words[k]["w"] for k in range(0, 3)]


def test_own_stomp_cue_syncs_top_and_hero_bottom_follows_speech(
        v2_lock, v2plan, fixture_v2_words_corrected, rules_110):
    """S08: block stomp có cue OK của chính nó — top + hero hiện ở
    đỉnh − sync_frame.block/fps; bottom vẫn theo lời."""
    plan, fps = v2plan[0], rules_110.get("fps")
    sync, lead = rules_110.get("sfx.sync_frame.block"), rules_110.get("text.lead_s")
    for bid in ("b05", "b10"):
        cue = _cand(plan, bid)["cue"]
        assert _cand(plan, bid)["decision"] == "OK"
        blk = _block(v2_lock, bid)
        assert blk["synced"]
        assert {w["show"] for w in blk["top"] + blk["hero"]} == {round((cue["frame"] - sync) / fps, 4)}
    b10 = _block(v2_lock, "b10")
    assert [w["show"] for w in b10["bottom"]] == [
        round(fixture_v2_words_corrected[k]["on"] - lead, 4) for k in (93, 94)]


def test_merged_stomp_block_syncs_to_host_cue(v2_lock, v2plan, rules_110):
    """R22: ứng viên stomp của b02 bị GỘP vào cue hook OK cùng khoảng ngắt ⇒
    top + hero của b02 hiện theo đỉnh cue hook."""
    plan, fps = v2plan[0], rules_110.get("fps")
    assert _cand(plan, "b02")["decision"] == "GỘP"
    hook = _cand(plan, "hook@w7")
    assert hook["decision"] == "OK" and hook["cue"]["pause"] == _cand(plan, "b02")["tried"][0]["pause"]
    b02 = _block(v2_lock, "b02")
    want = round((hook["cue"]["frame"] - rules_110.get("sfx.sync_frame.block")) / fps, 4)
    assert b02["synced"] and {w["show"] for w in b02["top"] + b02["hero"]} == {want}
    # các block script không có tiếng thì không đồng bộ
    assert [b["id"] for b in v2_lock["blocks"] if b["synced"]] == ["b02", "b05", "b10"]


def test_block_out_holds_then_yields_to_next_block(v2_lock, fixture_v2_words_corrected, v2_edit_v11):
    """R30: thoát thường 6 f ở out = min(e từ cuối + 0,22; lúc phải tắt xong − 0,22) —
    lúc phải tắt xong là show đầu của block sau, hoặc steps.in với block cuối trước thẻ;
    block cuối video chỉ giữ 0,22 s. Thoát thường mà cắt mất từ cuối (chưa đủ 3 frame
    ≥ 90 %) thì chuyển nhanh 2 f, tắt xong đúng lúc phải tắt (video 02: 7 block)."""
    words, reveal = fixture_v2_words_corrected, _reveal()
    quick = []
    for i, (spec, blk) in enumerate(zip(v2_edit_v11["blocks"], v2_lock["blocks"])):
        e, gate = words[(spec["bottom"] or spec["hero"])[1] - 1]["e"], _gate(v2_lock, i)
        normal = dict(blk, out=round(e + 0.22 if gate is None else min(e + 0.22, gate - 0.22), 4), exit_f=6)
        if blk["exit_f"] == 6:
            assert blk["out"] == normal["out"], blk["id"]
        else:
            assert (blk["exit_f"], blk["out"]) == (2, round(gate - 2 / 30, 4)), blk["id"]
            assert _last_word_run(normal, reveal) < 3, blk["id"]
            quick.append(blk["id"])
    assert quick == ["b03", "b04", "b07", "b08", "b09", "b10", "b16"]


def test_no_block_on_screen_after_steps_in(v2_lock):
    """Thẻ liệt kê vào ở steps.in thì không block nào còn trên hình: block hiện trước thẻ
    tắt xong (out + exit_f/fps) chậm nhất ở steps.in — b04 chuyển nhanh 2 f tắt xong đúng
    lúc thẻ vào (R30, R32; b04 từng giữ tới ≈ 9,2 s, chồng lên thẻ ở đáy hộp chữ)."""
    t_in = v2_lock["steps"]["in"]
    before = [b for b in v2_lock["blocks"] if _first_show(b) < t_in]
    assert [b["id"] for b in before] == ["b01", "b02", "b03", "b04"]
    assert all(b["out"] + b["exit_f"] / 30 <= t_in + 1e-4 for b in before)
    b04 = _block(v2_lock, "b04")
    assert (b04["exit_f"], b04["out"]) == (2, round(t_in - 2 / 30, 4))


def test_every_block_last_word_readable(v2_lock, rules_110):
    """R30: từ hiện sau cùng của mọi block đậm ≥ 90 % trên hình và giữ ≥ 3 frame trước khi
    block thoát kéo xuống — tính độc lập bằng công thức của Subtitle.tsx (từ hiện outCubic
    qua REVEAL frame; block thoát tuyến tính qua exit_f frame từ out; cửa sổ vẽ
    [show đầu − 2 f, out + exit_f]). Block không đạt phải mang cảnh báo LAST_WORD_TIGHT;
    video 02 đạt cả 17 (trước R30–R31: 7 block cắt mất từ cuối)."""
    src = _src("comp/Subtitle.tsx")
    for expr in ("frame < inAt * FPS - 2", "frame > outAt * FPS + b.exit_f", "(frame - outAt * FPS) / b.exit_f"):
        assert expr in src, expr
    reveal = _reveal()
    assert reveal == rules_110.get("text.reveal_f") == 9      # picture.py tính theo text.reveal_f
    short = [b["id"] for b in v2_lock["blocks"] if _last_word_run(b, reveal) < 3]
    assert short == [w.removeprefix("LAST_WORD_TIGHT:") for w in v2_lock["warnings"]] == []


def test_display_shifts_are_bounded(v2_lock, fixture_v2_words_corrected, v2_edit_v11, rules_110):
    """R31: từ cuối không đọc kịp thì dời mốc hiện — block sau không đồng bộ ⇒ các từ đầu
    của nó hiện muộn lại; block sau đồng bộ ⇒ đuôi block này hiện sớm hơn. Mỗi từ dời
    ≤ 0,15 s, từ bị lùi hiện ≤ 0,10 s sau onset; sự kiện có tiếng không dời (block đồng bộ
    giữ top + hero ở đỉnh cue, bottom theo lời — S08). Mọi độ dời ghi ở display_shift_s
    của từ: show − display_shift_s = on − lead (mốc gốc)."""
    words, lead = fixture_v2_words_corrected, rules_110.get("text.lead_s")
    shifted = []
    for spec, blk in zip(v2_edit_v11["blocks"], v2_lock["blocks"]):
        ks = [k for r in (spec["top"], spec["hero"], spec["bottom"]) if r for k in range(*r)]
        for k, w in zip(ks, _words(blk)):
            d = w.get("display_shift_s", 0)
            assert abs(d) <= 0.15 + 1e-4, (blk["id"], w["t"])
            if d:
                assert not blk["synced"], blk["id"]
                assert abs(w["show"] - d - (words[k]["on"] - lead)) <= 1e-3, (blk["id"], w["t"])
                assert d < 0 or w["show"] - words[k]["on"] <= 0.10 + 1e-4, (blk["id"], w["t"])
                shifted.append((blk["id"], w["t"], "+" if d > 0 else "-"))
    assert shifted == [("b04", "năm", "+"), ("b09", "nhận", "+"), ("b09", "hiệu", "-"),
                       ("b11", "phải", "+"), ("b11", "giữ", "+"), ("b17", "5", "+")]


def test_display_shifts_are_just_enough(v2_lock):
    """R31: block sau bị lùi thì từ đầu của nó hiện đúng lúc từ cuối block trước vừa đọc
    xong và chuyển nhanh xong: (f90 + 3 frame đọc − 1 + 2 f thoát)/fps, f90 là frame đầu
    từ cuối đạt 90 %. Đuôi bị kéo sớm thì từ cuối hiện muộn nhất có thể mà vẫn đọc được
    (hiện muộn thêm 0,0001 s là không đọc kịp)."""
    blocks, reveal = v2_lock["blocks"], _reveal()
    delayed, advanced = [], []
    for prev, blk in zip(blocks, blocks[1:]):
        if any(w.get("display_shift_s", 0) > 0 for w in _words(blk)):
            assert _first_show(blk) == round((_f90(_last_show(prev), reveal) + 4) / 30, 4), blk["id"]
            assert prev["exit_f"] == 2 and round(prev["out"] + 2 / 30, 4) == _first_show(blk), prev["id"]
            delayed.append(blk["id"])
    for blk in blocks:
        if any(w.get("display_shift_s", 0) < 0 for w in _words(blk)):
            late = dict(blk, bottom=blk["bottom"] + [{"t": "x", "show": _last_show(blk) + 1e-4}])
            assert _last_word_run(blk, reveal) >= 3 > _last_word_run(late, reveal), blk["id"]
            advanced.append(blk["id"])
    assert (delayed, advanced) == (["b04", "b09", "b11", "b17"], ["b09"])


def test_capped_delay_keeps_best_timing_then_warns(fixture_v2_words_corrected, v2_edit_v11, v2plan,
                                                   fixture_v2_pauses_full, rules_110):
    """R31: block sau cần lùi quá giới hạn — cho "năm" (từ 18, đầu b04) nói ngay sau "ra"
    (từ 17, cuối b03): "năm" chỉ lùi được tới 0,10 s sau onset (= dời 0,15 s), b03 chuyển
    nhanh tới đó mà "ra" vẫn không đọc kịp ⇒ giữ mốc tốt nhất, cảnh báo LAST_WORD_TIGHT:b03,
    không làm hỏng BUILD."""
    words = copy.deepcopy(fixture_v2_words_corrected)
    words[18]["on"] = words[17]["on"] + 0.02
    lock = picture.build_lock(words, v2_edit_v11, v2plan[0], fixture_v2_pauses_full, rules_110)
    assert lock["warnings"] == ["LAST_WORD_TIGHT:b03"]
    nam = _block(lock, "b04")["hero"][0]
    assert (nam["t"], nam["display_shift_s"], nam["show"]) == ("năm", 0.15, round(words[18]["on"] + 0.10, 4))
    b03 = _block(lock, "b03")
    assert (b03["exit_f"], b03["out"]) == (2, round(nam["show"] - 2 / 30, 4))
    assert _last_word_run(b03, _reveal()) < 3


def test_display_override_replaces_word_text(fixture_v2_words_corrected, v2_edit_v11, v2plan,
                                             fixture_v2_pauses_full, rules_110):
    """PLAN chỉ đổi cách hiện chữ qua `display` của block (năm → 5)."""
    edit = copy.deepcopy(v2_edit_v11)
    edit["blocks"][2]["display"] = {"12": "5"}
    lock = picture.build_lock(fixture_v2_words_corrected, edit, v2plan[0], fixture_v2_pauses_full, rules_110)
    assert [w["t"] for w in _block(lock, "b03")["hero"]][2] == "5"


# ------------------------------------------------ thẻ liệt kê, CTA, hook


def test_steps_without_card_cue(v2_lock, v2plan, fixture_v2_words_corrected, v2_edit_v11, rules_110):
    """Cue thẻ BỎ ⇒ thẻ vào ở mục 1 hiện − 0,29 s, nhưng không trước khi từ cuối của block
    trước thẻ đọc xong và block đó chuyển nhanh xong: steps.in ≥ (f90 + 4)/fps, f90 là
    frame đầu từ đó đạt 90 % (R32; video 02: 8,5067 → 8,80 s — "tạo" của b04 từng chỉ đạt
    93 % trong 1 frame). Mục hiện ở on + 2 f − lead; thẻ ra ở min(0,15 s sau từ cuối của
    mục cuối; block đầu sau thẻ hiện − OUT 8 f thoát của StepList) (R34)."""
    words, fps, lead = fixture_v2_words_corrected, rules_110.get("fps"), rules_110.get("text.lead_s")
    assert _cand(v2plan[0], "card@w28")["decision"] == "BỎ"
    items = v2_edit_v11["steps"]["items"]
    steps = v2_lock["steps"]
    assert steps["title"] == v2_edit_v11["steps"]["title"]
    assert [it["label"] for it in steps["items"]] == [it["label"] for it in items]
    assert [it["show"] for it in steps["items"]] == [
        round(words[it["range"][0]]["on"] + 2 / fps - lead, 4) for it in items]
    f90 = _f90(_last_show(_block(v2_lock, "b04")), _reveal())
    assert steps["in"] == round(max(steps["items"][0]["show"] - 0.29, (f90 + 4) / fps), 4) == 8.8
    nxt = min(_first_show(b) for b in v2_lock["blocks"] if _first_show(b) >= steps["in"])
    card_exit = _const(_src("comp/StepList.tsx"), "OUT")
    assert steps["out"] == round(min(words[items[-1]["range"][1] - 1]["e"] + 0.15, nxt - card_exit / fps), 4)


def test_card_gone_before_next_block(v2_lock, fixture_v2_words_corrected, v2_edit_v11, v2plan,
                                     fixture_v2_pauses_full, rules_110):
    """R34: thẻ ra xong (steps.out + OUT 8 f thoát của StepList) trước khi block đầu tiên
    sau thẻ hiện — video 02: b05 (stomp) hiện ở 14,5333 s; công thức R29 (− 0,10 s) để thẻ
    còn mờ dần dưới b05 thêm 5 frame. Không còn block nào sau thẻ thì thẻ giữ 0,15 s sau từ
    cuối."""
    steps, fps = v2_lock["steps"], v2_lock["fps"]
    card_exit = _const(_src("comp/StepList.tsx"), "OUT")
    after = [b for b in v2_lock["blocks"] if _first_show(b) >= steps["in"]]
    assert after[0]["id"] == "b05" and card_exit == 8
    assert steps["out"] == round(_first_show(after[0]) - card_exit / fps, 4) == 14.2666
    assert all(steps["out"] + card_exit / fps <= _first_show(b) + 1e-4 for b in after)
    edit = dict(v2_edit_v11, blocks=v2_edit_v11["blocks"][:4])     # b01–b04: không block nào sau thẻ
    lock = picture.build_lock(fixture_v2_words_corrected, edit, v2plan[0], fixture_v2_pauses_full, rules_110)
    last = v2_edit_v11["steps"]["items"][-1]["range"][1] - 1
    assert lock["steps"]["out"] == round(fixture_v2_words_corrected[last]["e"] + 0.15, 4)


def test_steps_with_card_cue_syncs_card(fixture_v2_words_corrected, v2_edit_v11, v2plan,
                                        fixture_v2_pauses_full, rules_110):
    """Cue thẻ OK ⇒ steps.in = đỉnh − sync_frame.card/fps."""
    plan = _card_cue_plan(v2plan[0])
    lock = picture.build_lock(fixture_v2_words_corrected, v2_edit_v11, plan, fixture_v2_pauses_full, rules_110)
    assert lock["steps"]["in"] == round((255 - rules_110.get("sfx.sync_frame.card")) / 30, 4)


def test_synced_card_advances_tail_then_warns(fixture_v2_words_corrected, v2_edit_v11, v2plan,
                                              fixture_v2_pauses_full, rules_110):
    """R32 + R31: thẻ có tiếng giữ steps.in ở đỉnh cue (8,30 s, S08) — không nhường. Block
    trước thẻ (b04, không đồng bộ) kéo sớm đuôi, mỗi từ ≤ 0,15 s, nhưng "tạo" (8,49 s, sau
    cả lúc thẻ vào) vẫn không đọc kịp ⇒ giữ mốc tốt nhất có thể (dời đủ 0,15 s), cảnh báo
    LAST_WORD_TIGHT:b04 trong khoá, không làm hỏng BUILD; b04 vẫn tắt xong trước thẻ."""
    lock = picture.build_lock(fixture_v2_words_corrected, v2_edit_v11, _card_cue_plan(v2plan[0]),
                              fixture_v2_pauses_full, rules_110)
    assert lock["steps"]["in"] == 8.3
    assert lock["warnings"] == ["LAST_WORD_TIGHT:b04"]
    b04 = _block(lock, "b04")
    assert b04["out"] + b04["exit_f"] / 30 <= 8.3 + 1e-4
    assert {w["t"]: w["display_shift_s"] for w in _words(b04)
            if w.get("display_shift_s", 0) < 0} == {"gốc": -0.15, "tôi": -0.15, "tạo": -0.15}
    assert _last_word_run(b04, _reveal()) < 3


def test_cta_pill_syncs_only_for_pre_hit(v2_lock, v2plan, fixture_v2_words_corrected, v2_edit_v11,
                                         fixture_v2_pauses_full, rules_110):
    """R23 / S20: CTA pre-hit ⇒ pill chạm đích ở frame đỉnh; CTA post-hit ⇒
    pill hiện ở on(cta.range[0]), tại đó không có tiếng."""
    plan, fps = v2plan[0], rules_110.get("fps")
    cue = _cand(plan, "cta@w147")["cue"]
    assert cue["mode"] == "pre"
    assert v2_lock["cta"] == {"label": "Bình luận", "keyword": "5 TÀI SẢN",
                              "show": round((cue["frame"] - rules_110.get("sfx.sync_frame.cta_pill")) / fps, 4)}
    post = copy.deepcopy(plan)
    _cand(post, "cta@w147")["cue"]["mode"] = "post"
    next(c for c in post["cues"] if c["id"] == "cta@w147")["mode"] = "post"
    lock = picture.build_lock(fixture_v2_words_corrected, v2_edit_v11, post, fixture_v2_pauses_full, rules_110)
    assert lock["cta"]["show"] == round(fixture_v2_words_corrected[147]["on"], 4)


def test_hook_title_timing(v2_lock, fixture_v2_words_corrected, v2_edit_v11, v2plan,
                           fixture_v2_pauses_full, rules_110):
    """S22: tít hook không tiếng, mốc cố định của template (land/out/end)."""
    assert v2_lock["hook"] == {"text": "20", "color": "warn", **picture.HOOK_TIMING}
    edit = dict(v2_edit_v11, hook=None)
    lock = picture.build_lock(fixture_v2_words_corrected, edit, v2plan[0], fixture_v2_pauses_full, rules_110)
    assert lock["hook"] is None


# ------------------------------------------------ shot, phần kết, dạng file


def test_shots_snap_to_cut_and_section_cues(v2_lock, v2plan, fixture_v2_words_corrected, v2_edit_v11):
    """Ruling R24: shot đầu là khung mở, t = 0 (không phải cú cắt — on(từ 0) ≈ 0,27 s
    sẽ bắn một cú kick cắt giả). Các shot sau: cú cắt có cue cắt/chuyển đoạn OK neo
    đúng từ cắt thì snap vào frame đỉnh k/fps; cú cắt khác ở on(cut_at_word)."""
    plan, words = v2plan[0], fixture_v2_words_corrected
    snap = {c["anchor_word"]: c["cue"]["frame"] for c in plan["candidates"]
            if c["decision"] == "OK" and c["role"] in ("cut", "section")}
    assert {21, 64, 113, 127} <= set(snap)
    shots = v2_lock["shots"]
    assert shots[0]["t"] == 0.0
    for spec, shot in zip(v2_edit_v11["shots"][1:], shots[1:]):
        k = spec["cut_at_word"]
        want = snap[k] / 30 if k in snap else words[k]["on"]
        assert shot["t"] == round(want, 4), k
        assert (shot["s0"], shot["s1"], shot["x"], shot["y"]) == (spec["s0"], spec["s1"], spec["x"], spec["y"])
    assert [s["t"] for s in shots] == sorted(s["t"] for s in shots)


def test_t_end_after_last_word(v2_lock, fixture_v2_words_corrected):
    assert v2_lock["t_end"] > fixture_v2_words_corrected[-1]["e"]


def test_t_end_is_pause_after_last_word_plus_pad(v2_lock, fixture_v2_pauses_full, rules_110):
    """S27: t_end = đầu khoảng ngắt sau từ cuối + end.pad_s (≤ độ dài nguồn);
    duration_f = round(t_end × fps)."""
    p = fixture_v2_pauses_full
    p0 = next(q[0] for q in p["pauses"] if q[0] >= p["last_word_end"] - 1e-3)
    assert v2_lock["t_end"] == round(min(p0 + rules_110.get("end.pad_s"), p["duration_s"]), 4)
    assert v2_lock["duration_f"] == round(v2_lock["t_end"] * 30) and v2_lock["fps"] == 30


def test_lock_is_plain_json(v2_lock, rules_110):
    assert json.loads(json.dumps(v2_lock, ensure_ascii=False)) == v2_lock
    assert list(v2_lock) == ["fps", "duration_f", "t_end", "hook", "blocks", "steps", "cta", "shots", "safe",
                             "warnings"]
    assert list(v2_lock["blocks"][0]) == ["id", "style", "color", "accent", "synced", "out", "exit_f",
                                          "top", "hero", "bottom"]
    assert v2_lock["safe"] == rules_110.get("safe_zone")
    assert v2_lock["warnings"] == []


def _ts_value(text, name):
    m = re.search(r"^export const %s(?:: [^=]+)? = (.*?);$" % name, text, re.M | re.S)
    return json.loads(m.group(1))


def test_write_script_ts_exports_lock(tmp_path, v2_lock):
    out = tmp_path / "script.ts"
    picture.write_script_ts(v2_lock, out)
    text = out.read_text(encoding="utf-8")
    assert re.findall(r"^export const (\w+)", text, re.M) == [
        "FPS", "DURATION_F", "DURATION_S", "HOOK", "BLOCKS", "STEPS", "SHOTS", "CTA", "SAFE"]
    assert "SFX" not in text
    assert _ts_value(text, "FPS") == 30 and _ts_value(text, "DURATION_F") == v2_lock["duration_f"]
    assert _ts_value(text, "DURATION_S") == v2_lock["t_end"]
    for name, key in (("HOOK", "hook"), ("BLOCKS", "blocks"), ("STEPS", "steps"), ("SHOTS", "shots"),
                      ("CTA", "cta"), ("SAFE", "safe")):
        assert _ts_value(text, name) == v2_lock[key], name
    again = tmp_path / "again.ts"
    picture.write_script_ts(v2_lock, again)
    assert again.read_bytes() == out.read_bytes()


def test_template_placeholder_uses_generated_types():
    """Bản giữ chỗ trong template khai đúng các kiểu mà write_script_ts sinh."""
    placeholder = _src("data/script.ts")
    assert picture.TS_TYPES in placeholder
    assert re.findall(r"^export const (\w+)", placeholder, re.M) == [
        "FPS", "DURATION_F", "DURATION_S", "HOOK", "BLOCKS", "STEPS", "SHOTS", "CTA", "SAFE"]


def test_template_is_picture_only():
    """Remotion chỉ render hình (S25): không còn Sfx.tsx, build.py cũ; Footage tắt tiếng."""
    for gone in ("src/comp/Sfx.tsx", "scripts/build.py", "scripts/check_av_sync.py", "scripts/transcribe.py"):
        assert not (TEMPLATE / gone).exists(), gone
    assert re.search(r"<OffthreadVideo[^>]*\bmuted\b", _src("comp/Footage.tsx"), re.S)
    root = _src("Root.tsx")
    assert 'id="Main"' in root and 'id="TextOnly"' in root


def test_template_has_no_npm_render_script():
    """Fix B: bản dựng thật chỉ đi qua scripts/render_video.py (--muted + ffmpeg ghép
    tiếng) — không còn `npm run render` ghi đè out/final.mp4 bằng bản có tiếng."""
    scripts = json.loads((TEMPLATE / "package.json").read_text(encoding="utf-8"))["scripts"]
    assert "render" not in scripts
    assert set(scripts) == {"dev", "still"}


# ------------------------------------------------ check_text_safe (phần không cần Remotion)


def test_probe_frames(v2_lock):
    """Mỗi block: min(show cuối + 12 f, ⌊out·fps⌋) — frame cuối block còn hiện đủ, không
    rơi vào lúc thẻ vào hay block sau hiện (R33); giữa thẻ; CTA show + 20 f; hook land —
    xếp tăng, không trùng, kẹp trong video."""
    fps, blocks, steps = v2_lock["fps"], v2_lock["blocks"], v2_lock["steps"]
    want = {_probe_frame(v2_lock, b["id"]) for b in blocks}
    want |= {round((steps["in"] + steps["out"]) / 2 * fps),
             round(v2_lock["cta"]["show"] * fps) + 20, round(v2_lock["hook"]["land"] * fps),
             math.floor(v2_lock["hook"]["out"] * fps)}     # B1: tít ở đỉnh đẩy ×1,05 (frame out)
    frames = check_text_safe.probe_frames(v2_lock)
    assert frames == sorted(want) and len(frames) == 21
    assert all(0 <= f < v2_lock["duration_f"] for f in frames)
    # b04 chuyển nhanh tới lúc thẻ vào: show cuối + 12 f (f267) từng rơi vào lúc thẻ trượt vào
    assert _probe_frame(v2_lock, "b04") == 261 < steps["in"] * fps
    for blk, nxt in zip(blocks, blocks[1:]):
        assert _probe_frame(v2_lock, blk["id"]) < _first_show(nxt) * fps, blk["id"]
    late = dict(v2_lock, cta=dict(v2_lock["cta"], show=v2_lock["t_end"]))
    assert check_text_safe.probe_frames(late)[-1] == v2_lock["duration_f"] - 1


def test_outside_pixels_are_counted(rules_110):
    safe = rules_110.get("safe_zone")
    alpha = np.zeros((1920, 1080), dtype=np.uint8)
    alpha[safe["text_y_min"]:safe["text_y_max"], safe["text_x_min"]:safe["text_x_max"]] = 255
    assert check_text_safe.outside(alpha, safe) == {"count": 0, "box": None}
    alpha[safe["text_y_max"], 500] = 1                 # 1 điểm ngay dưới hộp
    alpha[400, safe["text_x_min"] - 3] = 7             # 1 điểm lệch trái
    got = check_text_safe.outside(alpha, safe)
    assert got["count"] == 2
    assert got["box"] == [safe["text_x_min"] - 3, 400, 500, safe["text_y_max"]]


def test_read_alpha_from_png(tmp_path):
    """alpha đọc qua ffmpeg alphaextract, đúng từng điểm ảnh."""
    rgba = np.zeros((1920, 1080, 4), dtype=np.uint8)
    rgba[100, 50] = (255, 255, 255, 200)
    png = tmp_path / "f.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", "1080x1920",
                    "-i", "-", "-frames:v", "1", str(png)], input=rgba.tobytes(), check=True)
    alpha = check_text_safe.read_alpha(png)
    assert alpha.shape == (1920, 1080) and alpha[100, 50] == 200 and int(alpha.sum()) == 200


def test_render_still_passes_probe_prop(tmp_path, monkeypatch):
    """R26: cổng render TextOnly với prop probe (bỏ trang trí) qua --props JSON."""
    calls = []

    def fake_run(args, **kw):
        calls.append((args, kw))
        return subprocess.CompletedProcess(args, 0, "", "")

    monkeypatch.setattr(check_text_safe.proc, "run", fake_run)
    assert check_text_safe.render_still(tmp_path, 42) == tmp_path / "out" / "safe" / "f42.png"
    (args, kw), = calls
    assert args[1:5] == ["still", "src/index.ts", "TextOnly", "out/safe/f42.png"]
    assert "--frame=42" in args and kw["cwd"] == tmp_path
    assert kw["timeout"] == 180                                   # R47: mỗi still tối đa 180 s
    props = [a.removeprefix("--props=") for a in args if a.startswith("--props=")]
    assert len(props) == 1 and json.loads(props[0]) == {"probe": True}


def test_cli_timeout_exits_timeout_code(tmp_path, monkeypatch, capsys):
    """R47: render still quá hạn (thlib.proc đã giết cả cây) ⇒ thoát mã proc.TIMEOUT_EXIT — build.py
    đổi thành quá thời gian (BLOCK transient), không phải lỗi công cụ mã 2."""
    def slow(project):
        raise subprocess.TimeoutExpired(["remotion", "still"], 180)
    monkeypatch.setattr(check_text_safe, "run", slow)
    assert check_text_safe.main([str(tmp_path)]) == check_text_safe.proc.TIMEOUT_EXIT
    assert "180" in capsys.readouterr().out


def test_cli_tool_errors_exit_2_and_drop_stale_report(tmp_path, capsys, v2_lock):
    """B3: lỗi công cụ (picture_lock thiếu/hỏng, chưa npm install, thiếu font của template,
    Remotion lỗi) thoát mã 2 — khác mã 1 của chữ tràn thật (owner PLAN/template) — và
    out/safe/text_safe.json của lần trước bị xoá ngay đầu lần chạy (không trỏ nhầm file cũ)."""
    state.write_lock(tmp_path, "1.1.0")
    stale = tmp_path / "out" / "safe" / "text_safe.json"
    stale.parent.mkdir(parents=True)
    stale.write_text("[]", encoding="utf-8")
    assert check_text_safe.main([str(tmp_path)]) == 2
    assert "picture_lock.json" in capsys.readouterr().out and not stale.exists()

    (tmp_path / "picture_lock.json").write_text("{hỏng", encoding="utf-8")
    assert check_text_safe.main([str(tmp_path)]) == 2
    capsys.readouterr()

    (tmp_path / "picture_lock.json").write_text(json.dumps(v2_lock), encoding="utf-8")
    assert check_text_safe.main([str(tmp_path)]) == 2
    assert "npm install" in capsys.readouterr().out

    remotion = tmp_path / "node_modules" / ".bin" / check_text_safe.bin_name("remotion")
    remotion.parent.mkdir(parents=True)
    remotion.write_text("")
    (tmp_path / "src").mkdir()
    shutil.copy2(TEMPLATE / "src" / "fonts.tsx", tmp_path / "src" / "fonts.tsx")
    assert check_text_safe.main([str(tmp_path)]) == 2
    assert "BebasNeue.otf" in capsys.readouterr().out         # public/fonts trống: thiếu font

    for dst in FONTS:
        (tmp_path / "public" / "fonts").mkdir(parents=True, exist_ok=True)
        (tmp_path / "public" / "fonts" / dst).write_bytes(b"font")
    assert check_text_safe.main([str(tmp_path)]) == 2          # file .cmd rỗng: Remotion không ra PNG
    assert "LỖI CÔNG CỤ" in capsys.readouterr().out and not stale.exists()


# ------------------------------------------------ render thật (chậm)


FONT_PACK = "D:/MMO/Font/Cinematic fonts pack"
FONTS = {   # tên đích (fonts.tsx) ← đường dẫn trong font pack (bộ font 1.0.0, R17)
    "BeVietnamPro-Medium.ttf": "Font Việt hóa cinematic/Be_Vietnam_Pro/Be_Vietnam_Pro/BeVietnamPro-Medium.ttf",
    "BeVietnamPro-Bold.ttf": "Font Việt hóa cinematic/Be_Vietnam_Pro/Be_Vietnam_Pro/BeVietnamPro-Bold.ttf",
    "BeVietnamPro-Black.ttf": "Font Việt hóa cinematic/Be_Vietnam_Pro/Be_Vietnam_Pro/BeVietnamPro-Black.ttf",
    "BeVietnamPro-BlackItalic.ttf":
        "Font Việt hóa cinematic/Be_Vietnam_Pro/Be_Vietnam_Pro/BeVietnamPro-BlackItalic.ttf",
    "DTPhudu-Bold.otf": "DT-Phudu/Fonts Files/DTPhudu-Bold.otf",
    "DTPhudu-Black.otf": "DT-Phudu/Fonts Files/DTPhudu-Black.otf",
    "BebasNeue.otf": "Font Việt hóa cinematic/PS-Bebas-Neue-Regular-V1.1.otf",
    "Merolat.ttf": "Font Việt hóa cinematic/TF-Merolat-bs2kh4.ttf",
    "HeyMonday.ttf": "Font Việt hóa cinematic/TF-Hey-Monday-i0dzoo.ttf",
}


@pytest.fixture(scope="session")
def v2_remotion_project(v2_lock):
    """Dự án Remotion của video 02 dựng từ template 1.1.0 dưới tests/_out (git bỏ
    qua): script.ts sinh từ khoá hình, font 1.0.0, npm install."""
    proj = paths.SKILL / "tests" / "_out" / "text_safe_v2"
    if proj.exists():
        shutil.rmtree(proj / "src", ignore_errors=True)
    shutil.copytree(TEMPLATE, proj, dirs_exist_ok=True)
    (proj / "public" / "fonts").mkdir(parents=True, exist_ok=True)
    for dst, rel in FONTS.items():
        shutil.copy2(f"{FONT_PACK}/{rel}", proj / "public" / "fonts" / dst)
    if not (proj / "rules.lock").exists():
        state.write_lock(proj, "1.1.0")
    (proj / "picture_lock.json").write_text(json.dumps(v2_lock, ensure_ascii=False, indent=1),
                                            encoding="utf-8")
    picture.write_script_ts(v2_lock, proj / "src" / "data" / "script.ts")
    subprocess.run("npm install --no-audit --no-fund", cwd=proj, shell=True, check=True,
                   capture_output=True)
    return proj


@pytest.mark.slow
def test_template_typechecks(v2_remotion_project):
    tsc = v2_remotion_project / "node_modules" / ".bin" / check_text_safe.bin_name("tsc")
    run = subprocess.run([str(tsc), "--noEmit"], cwd=v2_remotion_project, capture_output=True, text=True)
    assert run.returncode == 0, run.stdout + run.stderr


@pytest.mark.slow
def test_video2_text_stays_in_safe_zone(v2_remotion_project, v2_lock, capsys):
    """B14: nét chữ và nền/viền thẻ, pill của video 02 — đo đúng như lúc hiện trên
    hình, kể cả blur và opacity chuyển động (R29); quầng, bóng đổ/bóng chữ, box-shadow,
    backdrop-filter không đo (probe, R26) — nằm trong hộp safe zone ở mọi frame dò;
    CLI ghi out/safe/text_safe.json và thoát 0."""
    assert check_text_safe.main([str(v2_remotion_project)]) == 0
    report = json.loads((v2_remotion_project / "out" / "safe" / "text_safe.json").read_text(encoding="utf-8"))
    assert [r["frame"] for r in report] == check_text_safe.probe_frames(v2_lock)
    assert all(r["ok"] and r["count"] == 0 for r in report)
    assert capsys.readouterr().out.splitlines()[-1].startswith("KẾT QUẢ: PASS")


@pytest.mark.slow
def test_overflowing_word_fails_text_safe(v2_remotion_project, v2_lock):
    """Cổng bắt được chữ tràn: một từ hero không xuống dòng được, toàn chữ rộng hơn trần em/ký tự
    đã hiệu chỉnh (W của DTPhudu Black 0,752 em > 0,66 — B2 co cỡ theo trần đó) thì vẫn tràn
    khỏi hộp ⇒ có điểm ảnh ngoài hộp. (Từ dài bình thường như "KHÔNGXUỐNGDÒNGĐƯỢC" giờ tự co.)"""
    script = v2_remotion_project / "src" / "data" / "script.ts"
    bad = copy.deepcopy(v2_lock)
    b05 = _block(bad, "b05")
    b05["hero"][0]["t"] = "W" * 21
    frame = round(max(w["show"] for w in b05["top"] + b05["hero"]) * 30) + 12
    try:
        picture.write_script_ts(bad, script)
        alpha = check_text_safe.read_alpha(check_text_safe.render_still(v2_remotion_project, frame))
        got = check_text_safe.outside(alpha, v2_lock["safe"])
    finally:
        picture.write_script_ts(v2_lock, script)
    assert got["count"] > 0 and (got["box"][0] < 140 or got["box"][2] >= 940)


def _outside_with(project, lock, changes):
    """{tên ca: (frame, số điểm ảnh ngoài hộp)} khi render các bản sửa `lock` (script.ts ghi
    lại bản gốc sau cùng). `changes` = [(tên, hàm sửa bản sao lock, [frame])]."""
    script, got = project / "src" / "data" / "script.ts", {}
    try:
        for name, mutate, frames in changes:
            bad = copy.deepcopy(lock)
            mutate(bad)
            picture.write_script_ts(bad, script)
            for f in frames:
                alpha = check_text_safe.read_alpha(check_text_safe.render_still(project, f))
                got["%s f%d" % (name, f)] = check_text_safe.outside(alpha, lock["safe"])["count"]
    finally:
        picture.write_script_ts(lock, script)
    return got


@pytest.mark.slow
def test_hook_title_fits_at_push_peak(v2_remotion_project, v2_lock):
    """B1: tít hook co theo bề rộng (anim.bebasEm) nên cả lúc land lẫn đỉnh đẩy ×1,05 (frame
    ⌊out·fps⌋, check_text_safe dò frame đó) chữ vẫn nằm trong hộp — kể cả tít hai từ PLAN.md nêu
    ("SAI RỒI", trước đây tràn 31 802 điểm ảnh ở cỡ 460) và tít dài hơn luật 8 ký tự."""
    fps, hook = v2_lock["fps"], v2_lock["hook"]
    frames = [round(hook["land"] * fps), math.floor(hook["out"] * fps)]
    assert frames[1] in check_text_safe.probe_frames(v2_lock)

    def text(t):
        return lambda lk: lk["hook"].update(text=t)
    got = _outside_with(v2_remotion_project, v2_lock,
                        [(t, text(t), frames) for t in ("SAI RỒI", "20 LẦN", "NGỪNG NGAY", "MMMM%%%%")])
    assert got and all(n == 0 for n in got.values()), got


@pytest.mark.slow
def test_long_words_and_cta_fit(v2_remotion_project, v2_lock):
    """B2: cỡ hero và dòng nhỏ còn bị chặn bởi từ dài nhất — từ có em/ký tự lớn nhất trong 60 kịch
    bản kênh ("HOMEWORK", "WORKFLOW" viết hoa trong block script; "MOODBOARD" stomp; "làm moodboard"
    từng tràn 5 760 điểm ảnh) nằm trong hộp; pill CTA với từ khoá dài nhất của kênh ("BRIEF TRƯỚC
    TOOL") vừa hộp cả lúc bật (đỉnh outBack, show + 7 f) lẫn lúc đứng (show + 20 f)."""
    def hero(bid, *texts, line="hero"):
        def mutate(lk):
            for w, t in zip(_block(lk, bid)[line], texts):
                w["t"] = t
        return mutate
    cta_show = round(v2_lock["cta"]["show"] * v2_lock["fps"])
    got = _outside_with(v2_remotion_project, v2_lock, [
        ("b05 stomp MOODBOARD", hero("b05", "MOODBOARD"), [_probe_frame(v2_lock, "b05")]),
        ("b01 script HOMEWORK", hero("b01", "HOMEWORK", "WORKFLOW"), [_probe_frame(v2_lock, "b01")]),
        ("b03 script làm moodboard", hero("b03", "làm", "moodboard"), [_probe_frame(v2_lock, "b03")]),
        ("b01 dòng nhỏ", hero("b01", "communicationscommunications", line="bottom"),
         [_probe_frame(v2_lock, "b01")]),
        ("cta", lambda lk: lk["cta"].update(label="Bình luận ngay", keyword="BRIEF TRƯỚC TOOL"),
         [cta_show + 7, cta_show + 20]),
    ])
    assert got and all(n == 0 for n in got.values()), got


@pytest.mark.slow
def test_width_constants_cover_channel_words(v3_sections):
    """B1/B2: trần em của template phủ đủ font thật — advance đo bằng fontTools: mọi ký tự Bebas
    (chữ hoa, số, dấu tiếng Việt, dấu câu) ≤ nhóm của anim.bebasEm; em/ký tự của mọi từ trong 60
    kịch bản kênh ≤ WORD_EM của Subtitle.tsx theo từng font (stomp in hoa). Đổi font là test này báo."""
    import unicodedata
    from fontTools.ttLib import TTFont

    def advances(rel):
        """advance (em) của ký tự; ký tự font không có (vd “ …) thì 0 — trình duyệt vẽ bằng font khác."""
        font = TTFont(f"{FONT_PACK}/{FONTS[rel]}")
        upm, cmap, hmtx = font["head"].unitsPerEm, font.getBestCmap(), font["hmtx"]

        def adv(ch):
            glyph = cmap.get(ord(ch)) or cmap.get(ord(unicodedata.normalize("NFD", ch)[0]))
            return hmtx[glyph][0] / upm if glyph else 0.0
        return adv

    bebas = advances("BebasNeue.otf")
    group = [(" ", 0.16), ("Ii.,:;!'", 0.21), ("MWmw%@", 0.59)]
    for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789ĂÂĐÊÔƠƯÁÀẢÃẠẦẤẬỒỐỘỜỚỢỪỨỰÉỀẾỆÍÓÚÝ%!?.,:-&":
        cap = next((em for chars, em in group if ch in chars), 0.43)
        assert bebas(ch) <= cap + 1e-9, (ch, bebas(ch), cap)

    em = {k: float(v) for k, v in re.findall(r"(small|script|stomp): ([\d.]+)", _src("comp/Subtitle.tsx"))}
    fonts = {"small": advances("BeVietnamPro-Medium.ttf"), "script": advances("BeVietnamPro-BlackItalic.ttf"),
             "stomp": advances("DTPhudu-Black.otf")}
    words = {w for sec in v3_sections.values() for w in sec["script"].split()}
    for face, adv in fonts.items():
        worst = max(words, key=lambda w: sum(map(adv, w.upper() if face == "stomp" else w)) / len(w))
        t = worst.upper() if face == "stomp" else worst
        assert sum(map(adv, t)) / len(t) <= em[face], (face, worst)


def _still(project, frame, probe):
    """Alpha [H, W] của frame `frame` composition TextOnly, prop probe bật/tắt."""
    rel = "out/safe/cmp_%s_f%d.png" % ("probe" if probe else "full", frame)
    remotion = project / "node_modules" / ".bin" / check_text_safe.bin_name("remotion")
    subprocess.run([str(remotion), "still", "src/index.ts", "TextOnly", rel, "--frame=%d" % frame,
                    "--image-format=png", "--props=" + json.dumps({"probe": probe}, separators=(",", ":"))],
                   cwd=project, check=True, capture_output=True)
    return check_text_safe.read_alpha(project / rel)


def _probe_frame(lock, bid):
    """Frame dò của một block, như check_text_safe.probe_frames: min(show cuối + 12 f,
    ⌊out·fps⌋) (R33; out làm tròn 4 số lẻ nên cộng 1e-6 trước khi lấy phần nguyên)."""
    b, fps = _block(lock, bid), lock["fps"]
    return min(round(_last_show(b) * fps) + 12, math.floor(b["out"] * fps + 1e-6))


@pytest.mark.slow
def test_probe_prop_strips_decoration(v2_remotion_project, v2_lock):
    """R26: TextOnly với probe=true bỏ trang trí của mọi lớp chữ (quầng,
    drop/text-shadow, box-shadow, backdrop-filter), giữ nét chữ và nền/viền thẻ, pill.
    Bản thường mang bóng 1.0.0 nên tràn khỏi hộp; bản dò thì không."""
    safe, fps = v2_lock["safe"], v2_lock["fps"]
    frames = {"hook": round(v2_lock["hook"]["land"] * fps),
              "hero b05": _probe_frame(v2_lock, "b05"),
              "thẻ": round((v2_lock["steps"]["in"] + v2_lock["steps"]["out"]) / 2 * fps),
              "cta": round(v2_lock["cta"]["show"] * fps) + 20}
    for name, frame in frames.items():
        full, probe = _still(v2_remotion_project, frame, False), _still(v2_remotion_project, frame, True)
        assert (probe > 0).sum() < (full > 0).sum(), name
        assert check_text_safe.outside(probe, safe)["count"] == 0, name
        if name in ("hero b05", "thẻ"):
            assert check_text_safe.outside(full, safe)["count"] > 0, name


@pytest.mark.slow
def test_probe_keeps_transition_blur(v2_remotion_project, v2_lock):
    """R29: probe chỉ bỏ bốn loại trang trí của R26 — blur chuyển động vẫn đo. Giữa
    lúc thẻ ra (q = 0,5, blur 4 px) mép trái thẻ nhoè ra ngoài x 140; thẻ sắc nét
    có mép trái đúng ở x 140 (test_steps_card_fits_sub_max_w). Dải y 900–1100 chỉ có
    thân thẻ (chữ block nằm sát đáy hộp)."""
    frame = round(v2_lock["steps"]["out"] * v2_lock["fps"]) + 4
    _, xs = np.nonzero(_still(v2_remotion_project, frame, True)[900:1100])
    assert len(xs) and xs.min() < v2_lock["safe"]["text_x_min"]


@pytest.mark.slow
def test_subtitle_glyphs_sit_on_sub_bottom(v2_remotion_project, v2_lock):
    """R26: phụ đề không còn lề hiệu ứng — đáy nét chữ ở SAFE.sub_bottom_px tính từ
    đáy khung (y 1920 − 484 = 1436, ±6 px), dòng rộng ≤ sub_max_w, giữa ở x 540.
    Frame dò của b13 (dòng dưới "cho từng vị trí" có nét g và dấu nặng)."""
    safe = v2_lock["safe"]
    ys, xs = np.nonzero(_still(v2_remotion_project, _probe_frame(v2_lock, "b13"), True))
    assert abs(int(ys.max()) - (1920 - safe["sub_bottom_px"])) <= 6
    assert xs.max() - xs.min() + 1 <= safe["sub_max_w"]
    assert abs((xs.min() + xs.max() + 1) / 2 - 540) <= 6


@pytest.mark.slow
def test_steps_card_fits_sub_max_w(v2_remotion_project, v2_lock):
    """R26: thẻ liệt kê (tính cả viền) rộng ≤ SAFE.sub_max_w, giữa khung, đáy thẻ
    ở đáy hộp chữ (không còn lề bóng đổ) — giữa khoảng thẻ chỉ có thẻ trên hình."""
    safe, fps = v2_lock["safe"], v2_lock["fps"]
    frame = round((v2_lock["steps"]["in"] + v2_lock["steps"]["out"]) / 2 * fps)
    ys, xs = np.nonzero(_still(v2_remotion_project, frame, True))
    assert xs.max() - xs.min() + 1 <= safe["sub_max_w"]
    assert abs((xs.min() + xs.max() + 1) / 2 - 540) <= 1
    assert abs(int(ys.max()) - (safe["text_y_max"] - 1)) <= 1
