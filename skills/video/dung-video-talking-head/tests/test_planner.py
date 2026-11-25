# tests/test_planner.py — kiểm tính chất của bộ xếp tiếng SFX (Task 8, S01–S27).
# Cổng R0a kiểm TÍNH CHẤT chứ không so bảng cue với prototype (spec §13.2);
# sim_v11_auto_standard.json chỉ dùng để tham chiếu bằng mắt.
import copy
import dataclasses
import json
import math

import numpy as np
import pytest

from thlib import editschema, planner

# Phán quyết R4: mọi so sánh với khoảng ngắt dùng dung sai 1e-3 s, vì số thực
# ghi vào sfx_plan.json đã làm tròn 4 số lẻ.
TOL = 1e-3
# Phán quyết R5: sai số mức cho phép giữa mức đo được và (mục tiêu tầng − hụt TP).
LEVEL_TOL_DB = 0.3


def _pause_of(plan_pause, pauses):
    """Khoảng ngắt gốc khớp cặp [t0, t1] đã làm tròn trong sfx_plan (R4)."""
    t0, t1 = plan_pause
    return next((p for p in pauses if abs(p[0] - t0) <= TOL and abs(p[1] - t1) <= TOL), None)


def _replan(words, pauses, edit, manifest, signals, vo, R, preset, overrides=()):
    return planner.plan(words, pauses, edit, list(overrides), manifest, signals, vo, R, preset)[0]


def _cand_of(plan, cid):
    return next(c for c in plan["candidates"] if c["id"] == cid)


def test_every_cue_inside_a_pause(v2plan, fixture_v2_pauses_full, rules_110):
    """S05: thân cue nằm trọn trong một khoảng ngắt thật, chừa g0 đầu / g1 cuối."""
    plan, _ = v2plan
    P = fixture_v2_pauses_full["pauses"]
    g0, g1 = rules_110.get("sfx.g0_s"), rules_110.get("sfx.g1_s")
    pause_min = rules_110.get("sfx.pause_min_s")
    assert plan["cues"], "không đặt được cue nào"
    for c in plan["cues"]:
        p = _pause_of(c["pause"], P)
        assert p is not None, c
        assert c["start_s"] >= p[0] + g0 - TOL, c
        assert c["end_s"] <= p[1] - g1 + TOL, c
        assert p[1] - p[0] >= pause_min[c["tier"]] - TOL, c


def test_one_cue_per_pause(v2plan):
    """S05: tối đa 1 cue mỗi khoảng ngắt."""
    plan, _ = v2plan
    used = [tuple(c["pause"]) for c in plan["cues"]]
    assert len(set(used)) == len(used)


def test_spacing_and_budget(v2plan, fixture_v2_pauses_full, rules_110):
    """S10 (đỉnh–đỉnh, A–A, cùng file) và S11 (cửa sổ 5 s, ngân sách video)."""
    plan, _ = v2plan
    cues = sorted(plan["cues"], key=lambda c: c["peak_s"])
    peaks = [c["peak_s"] for c in cues]
    assert peaks == sorted(peaks)
    assert all(b - a >= rules_110.get("sfx.p2p_s") - TOL for a, b in zip(peaks, peaks[1:]))
    assert all(sum(1 for p in peaks if s <= p < s + 5) <= 2 for s in peaks)
    assert len(peaks) <= math.ceil(2.5 * fixture_v2_pauses_full["duration_s"] / 10)
    assert len(peaks) <= plan["budget"]
    a_peaks = [c["peak_s"] for c in cues if c["tier"] == "A"]
    assert len(a_peaks) <= rules_110.get("sfx.max_a")
    assert all(b - a >= rules_110.get("sfx.aa_s") - TOL for a, b in zip(a_peaks, a_peaks[1:]))
    assert sum(1 for t in a_peaks if t <= rules_110.get("sfx.hook_window_s")) <= 1
    assert sum(1 for c in cues if c["role"] == "cut") <= rules_110.get("sfx.max_cut_c")
    for i, c in enumerate(cues):
        for x in cues[i + 1:]:
            if x["file"] == c["file"]:
                assert x["peak_s"] - c["peak_s"] >= rules_110.get("sfx.same_file_s") - TOL


def test_spacing_holds_for_every_preset(fixture_v2_words_corrected, fixture_v2_pauses_full,
                                        v2_edit_v11, sfx_manifest_110, sfx_signals_110,
                                        v2_vo_mono, rules_110):
    """S10/S11 cố định ở mọi preset; punchy là preset chật nhất nên phải kiểm."""
    for preset in ("calm", "standard", "punchy"):
        out = _replan(fixture_v2_words_corrected, fixture_v2_pauses_full, v2_edit_v11,
                      sfx_manifest_110, sfx_signals_110, v2_vo_mono, rules_110, preset)
        peaks = sorted(c["peak_s"] for c in out["cues"])
        assert all(b - a >= rules_110.get("sfx.p2p_s") - TOL for a, b in zip(peaks, peaks[1:])), preset
        assert len(peaks) <= out["budget"], preset
        for width, cap in ((5, rules_110.preset(preset)["max_5s"]),
                           (10, rules_110.preset(preset)["max_10s"])):
            assert all(sum(1 for p in peaks if s <= p < s + width) <= cap for s in peaks), preset


def test_same_role_never_repeats_file_back_to_back(fixture_v2_words_corrected, fixture_v2_pauses_full,
                                                   v2_edit_v11, sfx_manifest_110, sfx_signals_110,
                                                   v2_vo_mono, rules_110):
    """S10: hai cue liền nhau (theo đỉnh) của cùng một vai không dùng chung file,
    dù cách nhau ≥ same_file_s — ở mọi preset (punchy từng đặt hai stomp b05,
    b10 cùng impact/hit-weak)."""
    for preset in ("calm", "standard", "punchy"):
        out = _replan(fixture_v2_words_corrected, fixture_v2_pauses_full, v2_edit_v11,
                      sfx_manifest_110, sfx_signals_110, v2_vo_mono, rules_110, preset)
        cues = sorted(out["cues"], key=lambda c: c["peak_s"])
        for role in sorted({c["role"] for c in cues}):
            files = [c["file"] for c in cues if c["role"] == role]
            assert all(a != b for a, b in zip(files, files[1:])), (preset, role, files)
        if preset == "punchy":
            # hit-blow trượt S14 ở tầng A −2 dB nên b05 chỉ còn hit-weak = file của
            # stomp liền sau b10: lượt thử đó ghi mã S10, b05 không có tiếng.
            b05 = _cand_of(out, "b05")
            assert b05["decision"] == "CHỈ CHỮ" and b05["cue"] is None
            assert any(t["file"] == "impact/hit-weak" and t["reason"].startswith("S10")
                       for t in b05["tried"]), b05["tried"]


def test_hook_and_cta_placed(v2plan):
    """Hai cue bắt buộc của video 02 phải đặt được (S22, S20)."""
    plan, _ = v2plan
    roles = {c["role"] for c in plan["cues"]}
    assert "hook" in roles and "cta" in roles
    cta = [c for c in plan["cues"] if c["role"] == "cta"][0]
    for c in plan["cues"]:
        if c is not cta:
            assert abs(c["peak_s"] - cta["peak_s"]) >= 1.0 - TOL


def test_peaks_land_on_a_frame(v2plan, rules_110):
    """S08: đỉnh đặt đúng frame đồng bộ của hình."""
    plan, _ = v2plan
    fps = rules_110.get("fps")
    for c in plan["cues"]:
        assert abs(c["peak_s"] - c["frame"] / fps) <= TOL


def test_levels_relative_to_voice(v2plan, rules_110):
    """S14 (phán quyết R5): mức phone-K đo lại = mục tiêu tầng − hụt trần TP."""
    plan, _ = v2plan
    tier_db = rules_110.preset("standard")["tier_db"]
    for c in plan["cues"]:
        assert c["target_db"] == tier_db[c["tier"]]
        assert c["short_db"] <= rules_110.get("sfx.max_short_db")
        assert abs(c["levels"]["phone_k"] - (c["target_db"] - c["short_db"])) <= LEVEL_TOL_DB, c
        assert set(c["levels"]) == {"phone_k", "k", "phone_a"}


def test_cues_audio_matches_plan(v2plan, rules_110):
    """cues_audio (đầu vào của mix.render_stem) khớp từng cue của sfx_plan."""
    plan, audio_cues = v2plan
    assert len(audio_cues) == len(plan["cues"])
    for c, a in zip(plan["cues"], audio_cues):
        assert abs(a["start_s"] - c["start_s"]) <= TOL
        assert isinstance(a["samples"], np.ndarray)
        assert abs(len(a["samples"]) / 48000 - (c["end_s"] - c["start_s"])) <= TOL
        assert np.abs(a["samples"]).max() <= 10 ** (rules_110.get("sfx.tp_cap_dbtp") / 20)


def test_plan_follows_contract(v2plan):
    """S23: mọi ứng viên đều có quyết định, slot đã thử và mã luật."""
    plan, _ = v2plan
    assert set(plan) == {"rules_version", "preset", "vo_ref", "budget", "candidates",
                         "cues", "warnings", "inputs_sha256"}
    assert set(plan["inputs_sha256"]) == {"words", "pauses", "edit", "overrides", "vo",
                                          "manifest", "rules"}
    assert plan["rules_version"] == "1.1.0" and plan["preset"] == "standard"
    ids = [c["id"] for c in plan["candidates"]]
    assert len(set(ids)) == len(ids)
    ok_ids = {c["id"] for c in plan["candidates"] if c["decision"] == "OK"}
    assert ok_ids == {c["id"] for c in plan["cues"]}
    for c in plan["candidates"]:
        assert c["decision"] in ("OK", "GỘP", "CHỈ CHỮ", "BỎ", "XOÁ")
        assert (c["cue"] is None) == (c["decision"] != "OK")
        for t in c["tried"]:
            assert set(t) == {"mode", "pause", "file", "reason"}
        if c["decision"] in ("GỘP", "XOÁ"):
            assert c["rule"]
    assert all(isinstance(w, str) and w.startswith("LOW_DENSITY:") for w in plan["warnings"])


def test_section_candidates_5a_and_5b(fixture_v2_words_corrected, fixture_v2_pauses_full,
                                      v2_edit_v11, rules_110):
    """S02: 5a (ranh giới đoạn văn) và 5b (đầu block sau khoảng ngắt ≥ 400 ms),
    trùng khoảng ngắt thì gộp và ghi nguồn 5a."""
    C = planner.candidates(fixture_v2_words_corrected, fixture_v2_pauses_full, v2_edit_v11, rules_110)
    sec = [c for c in C if c["role"] == "section"]
    assert {c["anchor_word"] for c in sec} == {9, 21, 49, 88, 113, 127, 147}
    src = {c["anchor_word"]: c["source"] for c in sec}
    assert src[21] == "5a" and src[49] == "5a"   # 49: 5a và 5b cùng khoảng ngắt -> 5a
    assert src[9] == "5b" and src[113] == "5b"
    assert {c["role"] for c in C} == {"hook", "stomp", "cta", "card", "section", "cut"}


def test_slots_respect_anchor_and_pause_min(fixture_v2_words_corrected, fixture_v2_pauses_full,
                                            v2_edit_v11, rules_110):
    """S07: slot pre-hit là khoảng ngắt kết thúc đúng onset của từ neo."""
    C = planner.candidates(fixture_v2_words_corrected, fixture_v2_pauses_full, v2_edit_v11, rules_110)
    hook = [c for c in C if c["role"] == "hook"][0]
    got = planner.slots(hook, fixture_v2_pauses_full, fixture_v2_words_corrected, rules_110)
    assert got[0][0] == "pre" and got[0][2] == 7
    assert abs(got[0][1][1] - fixture_v2_words_corrected[7]["on"]) <= 0.02
    card = [c for c in C if c["role"] == "card"][0]
    assert planner.slots(card, fixture_v2_pauses_full, fixture_v2_words_corrected, rules_110) == []


def test_build_cue_rejects_short_pause(sfx_manifest_110, sfx_signals_110, fixture_v2_pauses_full,
                                       rules_110):
    """S05: khoảng ngắt không đủ chỗ cho thân cue thì trả lý do, không trả cue."""
    ctx = planner.Ctx(sfx_manifest_110, sfx_signals_110, fixture_v2_pauses_full["vo_ref"],
                      rules_110, "standard")
    cue, why = planner.build_cue(ctx, "impact/hit-blow", "pre", (10.0, 10.05), "A", "impact")
    assert cue is None and why.startswith("S05")
    cue, why = planner.build_cue(ctx, "impact/hit-blow", "pre", (10.0, 10.4), "A", "impact")
    assert why is None and cue["start_s"] >= 10.0 + rules_110.get("sfx.g0_s") - 1e-9
    assert cue["end_s"] <= 10.4 - rules_110.get("sfx.g1_s") + 1e-9


def test_deterministic(fixture_v2_words_corrected, fixture_v2_pauses_full, v2_edit_v11,
                       sfx_manifest_110, sfx_signals_110, v2_vo_mono, rules_110, v2plan):
    """S21: cùng đầu vào thì sfx_plan byte-identical."""
    again = _replan(fixture_v2_words_corrected, fixture_v2_pauses_full, v2_edit_v11,
                    sfx_manifest_110, sfx_signals_110, v2_vo_mono, rules_110, "standard")
    assert json.dumps(again, sort_keys=True, ensure_ascii=False) == \
        json.dumps(v2plan[0], sort_keys=True, ensure_ascii=False)


def test_calm_has_fewer_or_equal_cues(v2plan, fixture_v2_words_corrected, fixture_v2_pauses_full,
                                      v2_edit_v11, sfx_manifest_110, sfx_signals_110, v2_vo_mono,
                                      rules_110):
    """Preset chỉ đổi ngân sách/mức: calm không được nhiều cue hơn standard."""
    calm = _replan(fixture_v2_words_corrected, fixture_v2_pauses_full, v2_edit_v11,
                   sfx_manifest_110, sfx_signals_110, v2_vo_mono, rules_110, "calm")
    assert len(calm["cues"]) <= len(v2plan[0]["cues"])
    assert calm["budget"] < v2plan[0]["budget"]
    for c in calm["cues"]:
        assert c["target_db"] == rules_110.preset("calm")["tier_db"][c["tier"]]


def test_override_none_removes_candidate(v2plan, fixture_v2_words_corrected,
                                         fixture_v2_pauses_full, v2_edit_v11, sfx_manifest_110,
                                         sfx_signals_110, v2_vo_mono, rules_110):
    """§10.3: override `none` gỡ hẳn ứng viên (BỎ / OVERRIDE)."""
    hook_id = [c["id"] for c in v2plan[0]["cues"] if c["role"] == "hook"][0]
    out = _replan(fixture_v2_words_corrected, fixture_v2_pauses_full, v2_edit_v11,
                  sfx_manifest_110, sfx_signals_110, v2_vo_mono, rules_110, "standard",
                  [{"target": hook_id, "action": "none"}])
    removed = [c for c in out["candidates"] if c["id"] == hook_id][0]
    assert removed["decision"] == "BỎ" and removed["rule"] == "OVERRIDE"
    assert hook_id not in {c["id"] for c in out["cues"]}


def test_override_promote_a(v2plan, fixture_v2_words_corrected, fixture_v2_pauses_full,
                            v2_edit_v11, sfx_manifest_110, sfx_signals_110, v2_vo_mono, rules_110):
    """§10.3: override `promote_A` nâng ứng viên lên tầng A / hạng 2."""
    target = [c["id"] for c in v2plan[0]["candidates"] if c["role"] == "section"][0]
    out = _replan(fixture_v2_words_corrected, fixture_v2_pauses_full, v2_edit_v11,
                  sfx_manifest_110, sfx_signals_110, v2_vo_mono, rules_110, "standard",
                  [{"target": target, "action": "promote_A"}])
    promoted = [c for c in out["candidates"] if c["id"] == target][0]
    assert promoted["tier"] == "A" and promoted["rank"] == 2


def _toy(vo_ref):
    """Hai ứng viên chuyển đoạn cách nhau 0,5 s — chỉ luật đỉnh-đỉnh (S10)
    ngăn được cue thứ hai (ngân sách và cửa sổ 5 s vẫn còn chỗ)."""
    on = [0.2, 0.5, 1.4, 1.6, 2.3, 2.6]
    words = [{"i": i, "w": "w%d" % i, "s": t, "e": t + 0.2, "on": t, "src": "script", "guess": False}
             for i, t in enumerate(on)]
    pauses = {
        "pauses": [[1.0, 1.4], [1.9, 2.3]],
        "designed_breaks": [{"after_word": 1, "kind": "paragraph"},
                            {"after_word": 3, "kind": "paragraph"}],
        "vo_ref": vo_ref, "duration_s": 5.0, "last_word_end": 2.8,
    }
    edit = {"schema": "edit/1.1", "hook": None, "steps": None, "cta": None, "shots": [],
            "blocks": [{"id": "b01", "top": None, "hero": [0, 6], "bottom": None,
                        "style": "script", "color": None, "accent": None,
                        "display": {}, "reveal": False}]}
    return words, pauses, edit


def test_peak_to_peak_blocks_the_second_cue(sfx_manifest_110, sfx_signals_110,
                                            fixture_v2_pauses_full, rules_110):
    """S10: hai khoảng ngắt cách nhau < p2p_s thì chỉ một cái có tiếng."""
    words, pauses, edit = _toy(fixture_v2_pauses_full["vo_ref"])
    out = planner.plan(words, pauses, edit, [], sfx_manifest_110, sfx_signals_110,
                       np.zeros(100), rules_110, "standard")[0]
    assert out["budget"] == 2 and len(out["cues"]) == 1
    loser = [c for c in out["candidates"] if c["decision"] != "OK"]
    assert len(loser) == 1 and loser[0]["decision"] == "BỎ" and loser[0]["rule"] == "S10"
    assert "LOW_DENSITY:events<3" in out["warnings"]
    assert "LOW_DENSITY:no-hook-no-cta" in out["warnings"]


def test_unknown_override_is_an_error(fixture_v2_words_corrected, fixture_v2_pauses_full,
                                      v2_edit_v11, sfx_manifest_110, sfx_signals_110,
                                      v2_vo_mono, rules_110):
    """§10.3: ngoài `none` / `promote_A` đều FAIL, và target lạ cũng vậy."""
    for bad in ({"target": "hook@w7", "action": "louder"}, {"target": "khong-co", "action": "none"}):
        with pytest.raises(ValueError):
            _replan(fixture_v2_words_corrected, fixture_v2_pauses_full, v2_edit_v11,
                    sfx_manifest_110, sfx_signals_110, v2_vo_mono, rules_110, "standard", [bad])


def test_gapfill_takes_over_when_every_candidate_is_removed(
        fixture_v2_words_corrected, fixture_v2_pauses_full, v2_edit_v11, sfx_manifest_110,
        sfx_signals_110, v2_vo_mono, rules_110):
    """S26: gỡ hết ứng viên thì chỉ còn cue lấp khoảng trống, và cảnh báo
    thiếu hook lẫn CTA."""
    C = planner.candidates(fixture_v2_words_corrected, fixture_v2_pauses_full, v2_edit_v11, rules_110)
    out = _replan(fixture_v2_words_corrected, fixture_v2_pauses_full, v2_edit_v11,
                  sfx_manifest_110, sfx_signals_110, v2_vo_mono, rules_110, "standard",
                  [{"target": c["id"], "action": "none"} for c in C])
    assert out["cues"] and {c["role"] for c in out["cues"]} == {"gapfill"}
    assert "LOW_DENSITY:no-hook-no-cta" in out["warnings"]
    peaks = sorted(c["peak_s"] for c in out["cues"])
    pts = [fixture_v2_words_corrected[0]["on"]] + peaks + [fixture_v2_pauses_full["last_word_end"]]
    gaps = [b - a for a, b in zip(pts, pts[1:]) if b - a > rules_110.get("sfx.max_gap_s")]
    assert [w for w in out["warnings"] if w[12:13].isdigit()] or not gaps


# ------------------------------------------------ neo stomp = đầu block (§5.4)


def test_stomp_pre_hit_anchors_at_block_start(v2plan, fixture_v2_words_corrected,
                                              fixture_v2_pauses_full, v2_edit_v11, rules_110):
    """§5.4 / S07: stomp neo ở từ đầu block (dòng trên), và lead đo tới đúng
    từ neo của slot. Video 02: b05 (top [49, 52), hero [52, 55)) phải pre-hit
    trong khoảng ngắt kết thúc ở onset của w49 — không trượt S07 vì đo nhầm
    tới hero[0] rồi rơi xuống post-hit."""
    W = fixture_v2_words_corrected
    b05 = _cand_of(v2plan[0], "b05")
    assert b05["anchor_word"] == 49
    assert b05["decision"] == "OK" and b05["cue"]["mode"] == "pre", b05
    assert abs(b05["cue"]["pause"][1] - W[49]["on"]) <= 0.02 + TOL
    assert 0 <= W[49]["on"] - b05["cue"]["peak_s"] <= rules_110.get("sfx.lead_max_s") + TOL
    assert _cand_of(v2plan[0], "section@w49")["decision"] == "GỘP"   # S05: khoảng ngắt đã có stomp

    C = {c["id"]: c for c in planner.candidates(W, fixture_v2_pauses_full, v2_edit_v11, rules_110)}
    got = planner.slots(C["b05"], fixture_v2_pauses_full, W, rules_110)
    assert got[0][0] == "pre" and got[0][2] == 49
    # b02: đầu block (w5) không có khoảng ngắt nên slot pre-hit đến từ neo phụ hero[0] = w7.
    got = planner.slots(C["b02"], fixture_v2_pauses_full, W, rules_110)
    assert [(m, a) for m, _, a in got if m == "pre"] == [("pre", 7)]
    assert all(a is None for m, _, a in got if m == "post")


# ------------------------------------------------ cảnh tổng hợp cho từng nhánh luật


def _words(ons, texts=None, length=0.25):
    """Từ tổng hợp: `s` = `on` = mốc cho sẵn, `e` = on + length."""
    texts = texts or ["w%d" % i for i in range(len(ons))]
    return [{"i": i, "w": t, "s": on, "e": on + length, "on": on, "src": "script", "guess": False}
            for i, (t, on) in enumerate(zip(texts, ons))]


def _grid(n, step=0.5, t0=0.2):
    """n onset cách đều `step` giây, bắt đầu ở t0."""
    return [round(t0 + step * i, 4) for i in range(n)]


def _block(bid, hero, top=None, bottom=None, style="script", reveal=False, display=None):
    return {"id": bid, "top": top, "hero": hero, "bottom": bottom, "style": style,
            "color": None if style == "script" else "warn", "accent": None,
            "display": display or {}, "reveal": reveal}


def _scene(words, pauses, blocks, duration, hook=None, cta=None, shots=None, breaks=()):
    """(words, pauses.json, edit.json) tổng hợp; vo_ref do fixture `toyplan` điền."""
    pauses_json = {"pauses": [list(p) for p in pauses], "designed_breaks": list(breaks),
                   "vo_ref": None, "duration_s": duration, "last_word_end": words[-1]["e"]}
    edit = {"schema": "edit/1.1", "hook": hook, "blocks": blocks, "steps": None,
            "shots": shots or [{"cut_at_word": 0, "s0": 1.0, "s1": 1.0}], "cta": cta}
    return words, pauses_json, edit


def _patched(R, **sfx):
    """Bản sao bộ luật với vài tham số `sfx.*` đổi giá trị — chỉ để cô lập
    một nhánh luật mà trị số thật che mất."""
    raw = copy.deepcopy(R.raw)
    raw["params"]["sfx"].update(sfx)
    return dataclasses.replace(R, raw=raw)


@pytest.fixture
def toyplan(sfx_manifest_110, sfx_signals_110, fixture_v2_pauses_full, rules_110):
    """Chạy planner (preset standard, 10 file thật) trên một cảnh tổng hợp;
    VO_REF mượn của video 02."""
    def run(scene, overrides=(), R=None):
        words, pauses, edit = scene
        pauses = {**pauses, "vo_ref": fixture_v2_pauses_full["vo_ref"]}
        return planner.plan(words, pauses, edit, list(overrides), sfx_manifest_110,
                            sfx_signals_110, np.zeros(100), R or rules_110, "standard")[0]
    return run


def _cta_scene(hero_texts, keyword, display=None):
    """Block stomp b02 có hero [2, 4) và câu CTA [4, 6) mang `keyword`."""
    words = _words(_grid(6), ["mở", "đầu", *hero_texts, "lưu", "ngay"])
    blocks = [_block("b01", [0, 2]),
              _block("b02", [2, 4], style="stomp", display=display),
              _block("b03", [4, 6])]
    cta = {"range": [4, 6], "label": "Lưu ngay", "keyword": keyword}
    return _scene(words, [], blocks, 4.0, cta=cta)


@pytest.mark.parametrize("hero,display,keyword,repeats", [
    (["hai", "lần"], None, "2 LẦN", True),      # số đọc bằng chữ vẫn là token "2"
    (["20", "lần"], None, "2 LẦN", False),      # "2" nằm trong "20" nhưng không phải token
    (["15", "ngày"], None, "5", False),
    (["50", "ảnh"], None, "5", False),
    (["Lưu", "ngay!"], None, "LƯU", True),
    (["hai", "lần"], {"2": "20"}, "2 LẦN", False),   # so trên chữ HIỂN THỊ (display)
])
def test_s20_matches_validate_edit(hero, display, keyword, repeats, rules_110):
    """S20: planner gỡ stomp (XOÁ / S20) đúng khi và chỉ khi validate_edit báo
    CTA_KEYWORD_IN_STOMP — cùng một phép so tập token."""
    words, pauses, edit = _cta_scene(hero, keyword, display)
    b02 = next(c for c in planner.candidates(words, pauses, edit, rules_110) if c["id"] == "b02")
    codes = [e["code"] for e in editschema.validate(edit, words, pauses, rules_110)]
    assert ("CTA_KEYWORD_IN_STOMP" in codes) is repeats
    assert (b02["decision"], b02["rule"]) == (("XOÁ", "S20") if repeats else (None, None))


def test_s20_removed_stomp_stays_removed(toyplan):
    """S20: stomp bị XOÁ không vào vòng phân bổ và không có tiếng."""
    out = toyplan(_cta_scene(["hai", "lần"], "2 LẦN"))
    b02 = _cand_of(out, "b02")
    assert (b02["decision"], b02["rule"], b02["cue"], b02["tried"]) == ("XOÁ", "S20", None, [])


def test_reveal_falls_back_to_post_hit(toyplan, rules_110):
    """Vai reveal (A/2) neo ở hero[0]; không có khoảng ngắt trước từ neo thì
    post-hit trong khoảng ngắt có t0 ∈ [e − 100 ms, e + 300 ms] của từ hero cuối."""
    words = _words([0.2, 0.5, 0.8, 1.1, 1.4, 1.7, 2.0, 2.75, 3.0])
    blocks = [_block("b01", [0, 2], bottom=[2, 4]),
              _block("b02", [5, 7], top=[4, 5], bottom=[7, 9], reveal=True)]
    scene = _scene(words, [(2.3, 2.75)], blocks, 3.6)
    cand = next(c for c in planner.candidates(*scene, rules_110) if c["id"] == "b02")
    assert (cand["role"], cand["tier"], cand["rank"], cand["anchor_word"]) == ("reveal", "A", 2, 5)
    assert planner.slots(cand, scene[1], words, rules_110) == [("post", (2.3, 2.75), None)]

    b02 = _cand_of(toyplan(scene), "b02")
    assert b02["decision"] == "OK" and b02["cue"]["mode"] == "post"
    assert b02["cue"]["pause"] == [2.3, 2.75]


def test_cta_falls_back_to_post_hit_after_last_word(toyplan, rules_110):
    """S20: không có khoảng ngắt trước `cta.range[0]` thì CTA post-hit trong
    khoảng ngắt sau từ cuối video."""
    words = _words(_grid(6))                      # từ cuối: on 2,7 s, e 2,95 s
    cta = {"range": [3, 6], "label": "Lưu", "keyword": "LƯU"}
    scene = _scene(words, [(3.0, 3.6)], [_block("b01", [0, 3], bottom=[3, 6])], 4.0, cta=cta)
    cand = next(c for c in planner.candidates(*scene, rules_110) if c["role"] == "cta")
    assert cand["anchor_word"] == 3 and cand["last"] == 5
    assert planner.slots(cand, scene[1], words, rules_110) == [("post", (3.0, 3.6), None)]

    cta_out = _cand_of(toyplan(scene), "cta@w3")
    assert cta_out["decision"] == "OK" and cta_out["cue"]["mode"] == "post"
    assert cta_out["cue"]["pause"] == [3.0, 3.6]


def test_cta_without_slot_is_s20(toyplan, rules_110):
    """S20: khoảng ngắt trước từ neo và sau từ cuối đều ngắn hơn PAUSE_MIN tầng B
    ⇒ CTA không có slot nào, không có tiếng — BỎ dưới mã S20, không phải S07."""
    words = _words(_grid(6))                      # neo w3: on 1,7 s; từ cuối: e 2,95 s
    cta = {"range": [3, 6], "label": "Lưu", "keyword": "LƯU"}
    scene = _scene(words, [(1.55, 1.7), (3.0, 3.2)], [_block("b01", [0, 3], bottom=[3, 6])],
                   4.0, cta=cta)
    cand = next(c for c in planner.candidates(*scene, rules_110) if c["role"] == "cta")
    assert planner.slots(cand, scene[1], words, rules_110) == []

    cta_out = _cand_of(toyplan(scene), "cta@w3")
    assert (cta_out["decision"], cta_out["rule"], cta_out["cue"], cta_out["tried"]) == \
        ("BỎ", "S20", None, [])


def _pill_scene():
    """Câu CTA [8, 12) mở đầu block b02 sau khoảng ngắt dài 0,8 s (2,6–3,4 s): sparkle của CTA
    pre-hit ở đó trượt S07 (đuôi dài, chữ đi trước lời > 600 ms), không có khoảng ngắt sau từ
    cuối ⇒ CTA không có tiếng; whoosh chuyển đoạn 5b (đuôi ngắn) thì vừa khoảng ngắt đó."""
    words = _words([0.2, 0.5, 0.8, 1.1, 1.4, 1.7, 2.0, 2.3, 3.4, 3.7, 4.0, 4.3])
    cta = {"range": [8, 12], "label": "Lưu ngay", "keyword": "LƯU"}
    return _scene(words, [(2.6, 3.4)], [_block("b01", [0, 8]), _block("b02", [8, 12])], 5.0, cta=cta)


def test_silent_cta_pill_keeps_its_zone_clear(toyplan, rules_110):
    """A3 / S20 (R23): CTA không pre-hit (ở đây BỎ) thì pill hiện ở on(cta.range[0]) = 3,4 s
    không tiếng — ứng viên hạng dưới CTA không được có đỉnh trong ±cta_clear_s quanh mốc đó.
    Trước đây whoosh của section@w8 kêu ~0,17 s trước khi pill bật."""
    scene = _pill_scene()
    assert next(c for c in planner.candidates(*scene, rules_110) if c["role"] == "section")["id"] == "section@w8"
    out = toyplan(scene)
    cta, sec = _cand_of(out, "cta@w8"), _cand_of(out, "section@w8")
    assert (cta["decision"], cta["rule"]) == ("BỎ", "S07"), cta
    assert (sec["decision"], sec["rule"], sec["cue"]) == ("BỎ", "S20", None), sec
    assert sec["tried"] and all(t["reason"].startswith("S20 vùng im quanh pill CTA") for t in sec["tried"])
    assert all(abs(c["peak_s"] - 3.4) >= rules_110.get("sfx.cta_clear_s") for c in out["cues"])


def _cut_scene(cut_words, still_words, pauses, n_words, duration):
    """Một block duy nhất (không có ứng viên chuyển đoạn/lấp); shot đổi cỡ
    ở `cut_words` (cú cắt zoom) và giữ cỡ ở `still_words` (không phải cú cắt)."""
    shots, scale = [{"cut_at_word": 0, "s0": 1.0, "s1": 1.0}], 1.0
    for k in sorted(cut_words + still_words):
        if k in cut_words:
            scale = 1.2 if scale == 1.0 else 1.0
        shots.append({"cut_at_word": k, "s0": scale, "s1": scale})
    words = _words(_grid(n_words))
    return _scene(words, pauses, [_block("b01", [0, n_words])], duration, shots=shots)


def test_cut_cues_never_on_consecutive_shots(toyplan):
    """S11: hai cú cắt zoom ở hai shot liền nhau thì chỉ một cú có tiếng."""
    scene = _cut_scene([5, 17], [], [(2.3, 2.7), (8.3, 8.7)], 23, 12.0)
    out = toyplan(scene)
    cuts = [c for c in out["candidates"] if c["role"] == "cut"]
    assert [c["id"] for c in cuts] == ["cut@w5", "cut@w17"]
    assert [c["decision"] for c in cuts].count("OK") == 1
    loser = next(c for c in cuts if c["decision"] != "OK")
    assert (loser["decision"], loser["rule"]) == ("BỎ", "S11")
    assert loser["tried"] and all("liên tiếp" in t["reason"] for t in loser["tried"])


def test_cut_cues_capped_at_max_cut_c(toyplan, rules_110):
    """S11: tối đa `max_cut_c` cue cắt zoom mỗi video (cú cắt không liền nhau,
    cách nhau đủ xa để S10 và cửa sổ S11 đều còn chỗ)."""
    scene = _cut_scene([5, 16, 27], [10, 22], [(2.3, 2.7), (7.8, 8.2), (13.3, 13.7)], 35, 18.0)
    out = toyplan(scene)
    cuts = [c for c in out["candidates"] if c["role"] == "cut"]
    assert len(cuts) == 3
    assert [c["decision"] for c in cuts].count("OK") == rules_110.get("sfx.max_cut_c")
    loser = next(c for c in cuts if c["decision"] != "OK")
    assert (loser["decision"], loser["rule"]) == ("BỎ", "S11")
    assert all("cắt zoom tối đa" in t["reason"] for t in loser["tried"])


def _reveal_scene(anchors, n_words, duration, hook_word=None):
    """Block reveal ở mỗi từ neo trong `anchors` (có dòng trên để đầu block
    không trùng neo — tránh sinh ứng viên chuyển đoạn), khoảng ngắt 450 ms kết
    thúc đúng onset của neo; tuỳ chọn thêm hook ở `hook_word`."""
    words = _words(_grid(n_words))
    neo = sorted(anchors + ([hook_word] if hook_word else []))
    pauses = [(words[a]["on"] - 0.45, words[a]["on"]) for a in neo]
    blocks = [_block("b00", [0, min(anchors) - 1])]
    blocks += [_block("r%02d" % a, [a, a + 2], top=[a - 1, a], reveal=True) for a in anchors]
    hook = {"text": "x", "color": "warn", "hit_word": hook_word} if hook_word else None
    return _scene(words, pauses, blocks, duration, hook=hook)


def test_tier_a_capped_at_max_a(toyplan, rules_110):
    """S11: tối đa `max_a` cue tầng A; cue A thứ 5 thành CHỈ CHỮ (S01)."""
    scene = _reveal_scene([8, 21, 34, 47, 60], 66, 33.5)
    out = toyplan(scene)
    reveals = [c for c in out["candidates"] if c["role"] == "reveal"]
    assert len(reveals) == 5
    assert sum(1 for c in out["cues"] if c["tier"] == "A") == rules_110.get("sfx.max_a")
    losers = [c for c in reveals if c["decision"] != "OK"]
    assert len(losers) == 1
    assert (losers[0]["decision"], losers[0]["rule"]) == ("CHỈ CHỮ", "S11")
    assert all("tầng A tối đa" in t["reason"] for t in losers[0]["tried"])


def test_hook_window_allows_one_tier_a(toyplan, rules_110):
    """S22: 0–hook_window_s tối đa 1 cue tầng A; cue A thứ hai thành CHỈ CHỮ.

    Với trị số thật (aa_s 6 s > hook_window_s 3,5 s) luật A–A của S10 chặn
    trước, nên S22 chỉ lộ ra khi nới aa_s và same_file_s."""
    scene = _reveal_scene([6], 12, 6.0, hook_word=3)
    loose = _patched(rules_110, aa_s=1.0, same_file_s=1.0)
    out = toyplan(scene, R=loose)
    assert _cand_of(out, "hook@w3")["decision"] == "OK"
    r06 = _cand_of(out, "r06")
    assert r06["tier"] == "A" and r06["cue"] is None
    assert (r06["decision"], r06["rule"]) == ("CHỈ CHỮ", "S22")
    assert all(t["reason"].startswith("S22") for t in r06["tried"])

    strict = _cand_of(toyplan(scene), "r06")
    assert (strict["decision"], strict["rule"]) == ("CHỈ CHỮ", "S10")


def test_per_video_budget_caps_cue_count(toyplan, rules_110):
    """S11: PER_VIDEO = ceil(k × giây / 10); video 3,6 s ở standard chỉ có 1 cue
    dù cue thứ hai hợp lệ với S10 và cửa sổ 5 s / 10 s."""
    words = _words([0.2, 0.5, 1.4, 1.6, 3.0, 3.2], length=0.2)
    breaks = [{"after_word": 1, "kind": "paragraph"}, {"after_word": 3, "kind": "paragraph"}]
    scene = _scene(words, [(1.0, 1.4), (2.6, 3.0)], [_block("b01", [0, 6])], 3.6, breaks=breaks)
    out = toyplan(scene)
    assert out["budget"] == math.ceil(rules_110.preset("standard")["k_per10"] * 3.6 / 10) == 1
    assert len(out["cues"]) == 1
    loser = next(c for c in out["candidates"] if c["decision"] != "OK")
    assert (loser["decision"], loser["rule"]) == ("BỎ", "S11")
    # File khác cue đã đặt chỉ vướng ngân sách (file trùng thì vướng thêm S10 cùng file).
    other_files = {t["reason"] for t in loser["tried"] if t["file"] != out["cues"][0]["file"]}
    assert other_files == {"S11 hết ngân sách video (1 cue)"}


def _gap_scene():
    """12 s lời, không ứng viên nào; đầu block b02 (w11) có khoảng ngắt 350 ms
    gần giữa video — chỗ duy nhất S26 lấp được."""
    words = _words(_grid(23))
    blocks = [_block("b01", [0, 11]), _block("b02", [11, 23])]
    return _scene(words, [(5.35, 5.7)], blocks, 12.0)


def test_gapfill_accepts_overrides(toyplan, rules_110):
    """§10.3: override trỏ tới ứng viên lấp S26 (id có trong sfx_plan.candidates)
    phải chạy được: `none` gỡ nó (BỎ / OVERRIDE), `promote_A` nâng lên tầng A;
    target không có vẫn là lỗi."""
    base = toyplan(_gap_scene())
    gap = _cand_of(base, "gapfill@w11")
    assert gap["decision"] == "OK" and gap["tier"] == "C"

    removed = toyplan(_gap_scene(), [{"target": "gapfill@w11", "action": "none"}])
    gap = _cand_of(removed, "gapfill@w11")
    assert (gap["decision"], gap["rule"], gap["cue"], gap["tried"]) == ("BỎ", "OVERRIDE", None, [])
    assert removed["cues"] == []
    assert any(w.startswith("LOW_DENSITY:0.20-") for w in removed["warnings"])

    promoted = toyplan(_gap_scene(), [{"target": "gapfill@w11", "action": "promote_A"}])
    gap = _cand_of(promoted, "gapfill@w11")
    assert (gap["decision"], gap["tier"], gap["rank"]) == ("OK", "A", 2)
    assert gap["cue"]["target_db"] == rules_110.preset("standard")["tier_db"]["A"]

    with pytest.raises(ValueError):
        toyplan(_gap_scene(), [{"target": "gapfill@w12", "action": "none"}])


def _snap_scene():
    """Đầu block b02 (w11, on 5,7 s) sau khoảng ngắt 450 ms ⇒ ứng viên chuyển đoạn 5b;
    shot đổi cỡ 0,2 ở w15 (on 7,7 s, khoảng ngắt 350 ms ngay trước) ⇒ ứng viên cắt zoom
    — hai đỉnh cách nhau ~2 s, không có ứng viên nào khác."""
    words = _words(_grid(23))
    blocks = [_block("b01", [0, 11]), _block("b02", [11, 23])]
    shots = [{"cut_at_word": 0, "s0": 1.0, "s1": 1.0}, {"cut_at_word": 15, "s0": 1.2, "s1": 1.2}]
    return _scene(words, [(5.25, 5.7), (7.35, 7.7)], blocks, 12.0, shots=shots)


def test_same_wav_under_two_keys_is_the_same_file(toyplan, sfx_manifest_110, rules_110):
    """A2 / S10: transition-snap đăng ký hai lần (whoosh/ và air/, cùng md5). Luật cùng file
    ≥ same_file_s so theo md5: cue chuyển đoạn lấy whoosh/transition-snap thì cue cắt zoom
    cách ~2 s không được lấy air/transition-snap (S10), phải sang file khác của họ air."""
    files = sfx_manifest_110["files"]
    assert files["whoosh/transition-snap"]["md5"] == files["air/transition-snap"]["md5"]
    R = _patched(rules_110, family_files={**rules_110.get("sfx.family_files"),
                                          "whoosh": ["whoosh/transition-snap"],
                                          "air": ["air/transition-snap", "air/sweep-short"]})
    out = toyplan(_snap_scene(), R=R)
    sec, cut = _cand_of(out, "section@w11"), _cand_of(out, "cut@w15")
    assert sec["decision"] == "OK" and sec["cue"]["file"] == "whoosh/transition-snap"
    assert 1.0 <= cut["cue"]["peak_s"] - sec["cue"]["peak_s"] < rules_110.get("sfx.same_file_s")
    assert cut["decision"] == "OK" and cut["cue"]["file"] == "air/sweep-short", cut
    assert [(t["file"], t["reason"]) for t in cut["tried"]] == [
        ("air/transition-snap", "S10 cùng file < 5 s (section@w11)")]


def test_merged_into_finds_host_cue(v2plan):
    """GỘP: cue OK đang giữ khoảng ngắt mà ứng viên bị gộp vào (slot gộp đầu
    tiên trong `tried`); ứng viên không GỘP thì None."""
    plan, _ = v2plan
    cues = plan["cues"]
    assert planner.merged_into(_cand_of(plan, "b02"), cues)["id"] == "hook@w7"
    assert planner.merged_into(_cand_of(plan, "section@w49"), cues)["id"] == "b05"
    assert planner.merged_into(_cand_of(plan, "b05"), cues) is None
    assert planner.merged_into(_cand_of(plan, "card@w28"), cues) is None
