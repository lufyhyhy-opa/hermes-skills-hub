# tests/test_lint.py — lint SFX độc lập L1–L14 (Task 10, spec §5.8).
# Lint không tin số trong sfx_plan: các test dưới đây sửa STEM (plan giữ nguyên)
# để chứng minh lint đo lại từ tín hiệu, và sửa plan / picture_lock để chứng
# minh lint đối chiếu lời tự nhận của plan với số đo.
import copy
import json
import subprocess

import numpy as np
import pytest
from scipy.signal import butter, sosfilt

import lint_sfx
from thlib import audio as A, lint, mix, paths, picture, planner, sfxlib, state, voice

PRE_CODES = ["L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8", "L9", "L10", "L12", "L13", "L14"]


def _run(scene, pauses, R, plan=None, stem=None, lock=None, bed=None, **kw):
    """run_pre_mux trên cảnh video 02, thay từng thành phần khi cần."""
    p, s, vo, lk, man = scene
    return lint.run_pre_mux(p if plan is None else plan, s if stem is None else stem, vo, bed,
                            pauses, lk if lock is None else lock, man, R, "standard", **kw)


def _failed(res):
    return {r["code"] for r in res if not r["ok"]}


def _by_code(res):
    return {r["code"]: r for r in res}


def _cue(plan, cid):
    return next(c for c in plan["cues"] if c["id"] == cid)


def _edit_cue(plan, cid, **fields):
    """Bản sao plan với cue `cid` sửa `fields` ở cả danh sách cues lẫn ứng viên
    (hai chỗ luôn khớp nhau, để chỉ luật đang kiểm lên tiếng)."""
    out = copy.deepcopy(plan)
    _cue(out, cid).update(fields)
    cand = next(c for c in out["candidates"] if c["id"] == cid)
    cand["cue"].update({k: v for k, v in fields.items() if k in cand["cue"]})
    cand.update({k: v for k, v in fields.items() if k in ("role", "tier")})
    return out


def _span(cue):
    """Mẫu quanh thân cue (plan dùng để định vị trong test, lint thì không)."""
    return int((cue["start_s"] - 0.01) * A.SR), int((cue["end_s"] + 0.01) * A.SR)


# ------------------------------------------------ hai cổng bắt buộc (Step 1)


def test_planner_output_passes_lint(v2plan_and_stem, fixture_v2_pauses_full, rules_110):
    plan, stem, vo, lock, man = v2plan_and_stem
    res = lint.run_pre_mux(plan, stem, vo, None, fixture_v2_pauses_full, lock, man, rules_110, "standard")
    assert [r for r in res if not r["ok"]] == []


def test_old_25_cues_fail_expected_codes(old_cues_plan_and_stem, fixture_v2_pauses_full, rules_110):
    plan, stem, vo, lock, man = old_cues_plan_and_stem
    failed = {r["code"] for r in lint.run_pre_mux(plan, stem, vo, None, fixture_v2_pauses_full, lock, man, rules_110, "standard") if not r["ok"]}
    assert {"L1", "L2", "L3", "L4", "L7"} <= failed


# ------------------------------------------------ hình dạng kết quả


def test_every_pre_mux_code_reported_once(v2plan_and_stem, fixture_v2_pauses_full, rules_110):
    res = _run(v2plan_and_stem, fixture_v2_pauses_full, rules_110)
    assert [r["code"] for r in res] == PRE_CODES
    for r in res:
        assert set(r) == {"code", "ok", "msg", "frame"}
        assert isinstance(r["ok"], bool) and isinstance(r["msg"], str) and r["msg"]
        assert r["frame"] is None or isinstance(r["frame"], int)


def test_failure_carries_frame_evidence(old_cues_plan_and_stem, fixture_v2_pauses_full, rules_110):
    """S23: sfx_lint ghi FAIL kèm frame làm bằng chứng."""
    res = _by_code(_run(old_cues_plan_and_stem, fixture_v2_pauses_full, rules_110))
    for code in ("L1", "L2", "L3", "L7"):
        assert isinstance(res[code]["frame"], int) and res[code]["frame"] >= 0, res[code]


# ------------------------------------------------ đo lại trên stem, không tin plan


def test_l1_measures_the_stem_not_the_plan(v2plan_and_stem, fixture_v2_pauses_full, rules_110):
    """S05: dời thân b05 0,4 s sang lời trên STEM, plan giữ nguyên ⇒ L1 (và L13
    cue đè lời) FAIL."""
    plan, stem, *_ = v2plan_and_stem
    a, b = _span(_cue(plan, "b05"))
    moved = stem.copy()
    moved[a:b] = 0
    k = int(0.4 * A.SR)
    moved[a + k: b + k] += stem[a:b]
    res = _by_code(_run(v2plan_and_stem, fixture_v2_pauses_full, rules_110, stem=moved))
    assert not res["L1"]["ok"] and "b05" in res["L1"]["msg"]
    assert not res["L13"]["ok"]


def test_l5_level_is_measured_on_stem(v2plan_and_stem, fixture_v2_pauses_full, rules_110):
    """S14 (R5): cue b05 to hơn 2 dB trên stem ⇒ chỉ L5 FAIL."""
    plan, stem, *_ = v2plan_and_stem
    a, b = _span(_cue(plan, "b05"))
    louder = stem.copy()
    louder[a:b] *= 10 ** (2 / 20)
    res = _run(v2plan_and_stem, fixture_v2_pauses_full, rules_110, stem=louder)
    assert _failed(res) == {"L5"}
    assert "b05" in _by_code(res)["L5"]["msg"]


def test_l9_display_must_match_peak(v2plan_and_stem, fixture_v2_pauses_full, rules_110):
    """S08: chữ của block có tiếng hiện ở đỉnh − SYNC_FRAME/fps; block không có
    cue thì không được đánh dấu synced."""
    lock = v2plan_and_stem[3]
    late = copy.deepcopy(lock)
    b05 = next(b for b in late["blocks"] if b["id"] == "b05")
    for w in b05["top"] + b05["hero"]:
        w["show"] += 2 / 30
    assert _failed(_run(v2plan_and_stem, fixture_v2_pauses_full, rules_110, lock=late)) == {"L9"}

    fake = copy.deepcopy(lock)
    next(b for b in fake["blocks"] if not b["synced"])["synced"] = True
    assert _failed(_run(v2plan_and_stem, fixture_v2_pauses_full, rules_110, lock=fake)) == {"L9"}


def test_l9_merged_block_follows_host_cue(v2plan_and_stem, fixture_v2_pauses_full, rules_110):
    """R22: b02 (stomp GỘP vào cue hook cùng khoảng ngắt) phải hiện theo đỉnh cue
    hook — lệch 2 f hoặc bỏ cờ synced ⇒ L9 FAIL nêu b02."""
    lock = v2plan_and_stem[3]
    for mutate in ("late", "unsynced"):
        bad = copy.deepcopy(lock)
        b02 = next(b for b in bad["blocks"] if b["id"] == "b02")
        if mutate == "late":
            for w in b02["top"] + b02["hero"]:
                w["show"] += 2 / 30
        else:
            b02["synced"] = False
        res = _run(v2plan_and_stem, fixture_v2_pauses_full, rules_110, lock=bad)
        assert _failed(res) == {"L9"}, mutate
        assert "b02" in _by_code(res)["L9"]["msg"], mutate


def test_l9_peak_frame_is_measured_on_stem(v2plan_and_stem, fixture_v2_pauses_full, rules_110):
    """S08/S24: plan khai frame đỉnh trễ 2 f (lock khớp lời khai) nhưng đỉnh đo
    trên stem vẫn ở chỗ cũ ⇒ L9 FAIL (dung sai sớm 1 f)."""
    plan, _, _, lock, _ = v2plan_and_stem
    b05 = _cue(plan, "b05")
    shifted = _edit_cue(plan, "b05", frame=b05["frame"] + 2, peak_s=round(b05["peak_s"] + 2 / 30, 4))
    lock2 = copy.deepcopy(lock)
    blk = next(b for b in lock2["blocks"] if b["id"] == "b05")
    for w in blk["top"] + blk["hero"]:
        w["show"] += 2 / 30
    res = _run(v2plan_and_stem, fixture_v2_pauses_full, rules_110, plan=shifted, lock=lock2)
    assert _failed(res) == {"L9"}


# ------------------------------------------------ đối chiếu plan với luật


def test_l10_compares_plan_hash(v2plan_and_stem, fixture_v2_pauses_full, rules_110):
    """S21: sha256 của sfx_plan phải bằng sha của output planner chạy lại."""
    plan = v2plan_and_stem[0]
    sha = lint.plan_sha256(plan)
    good = _by_code(_run(v2plan_and_stem, fixture_v2_pauses_full, rules_110, expected_sha=sha))
    assert good["L10"]["ok"]
    bad = _by_code(_run(v2plan_and_stem, fixture_v2_pauses_full, rules_110, expected_sha="0" * 64))
    assert not bad["L10"]["ok"]
    skipped = _by_code(_run(v2plan_and_stem, fixture_v2_pauses_full, rules_110))["L10"]
    assert skipped["ok"] and "expected_sha" in skipped["msg"]
    assert lint.plan_sha256(json.loads(json.dumps(plan))) == sha   # qua file JSON vẫn cùng sha


def test_l3_flags_back_to_back_same_file(v2plan, v2plan_and_stem, fixture_v2_pauses_full,
                                         sfx_signals_110, rules_110):
    """S10: cue chuyển đoạn thứ hai đổi sang đúng file của cue chuyển đoạn thứ
    nhất (vẫn cách ≥ same_file_s; cue dựng lại bằng planner.build_cue, stem dựng
    lại) ⇒ chỉ L3 FAIL, msg nêu S10 và hai cue."""
    plan, cues_audio = v2plan
    vo, man = v2plan_and_stem[2], v2plan_and_stem[4]
    first, second = [c for c in plan["cues"] if c["role"] == "section"][:2]
    assert first["file"] != second["file"]
    assert second["peak_s"] - first["peak_s"] >= rules_110.get("sfx.same_file_s")

    ctx = planner.Ctx(man, sfx_signals_110, fixture_v2_pauses_full["vo_ref"], rules_110, "standard")
    pause = next(tuple(p) for p in fixture_v2_pauses_full["pauses"]
                 if all(abs(a - b) <= lint.TOL for a, b in zip(p, second["pause"])))
    cue, why = planner.build_cue(ctx, first["file"], second["mode"], pause, second["tier"],
                                 rules_110.get("sfx.role_family")["section"])
    assert why is None, why
    fields = {k: round(float(cue[k]), 4)
              for k in ("peak_s", "start_s", "end_s", "gain_db", "fade_loss_db", "short_db")}
    bad = _edit_cue(plan, second["id"], file=first["file"], frame=cue["frame"], **fields)
    i = plan["cues"].index(second)
    stem = mix.render_stem([*cues_audio[:i], {"start_s": cue["start_s"], "samples": cue["samples"]},
                            *cues_audio[i + 1:]], len(vo))

    res = _run(v2plan_and_stem, fixture_v2_pauses_full, rules_110, plan=bad, stem=stem)
    assert _failed(res) == {"L3"}
    msg = _by_code(res)["L3"]["msg"]
    assert "S10" in msg and first["id"] in msg and second["id"] in msg


def test_l3_same_wav_under_two_keys(v2plan_and_stem, fixture_v2_pauses_full, rules_110):
    """A2 / S10: whoosh/transition-snap và air/transition-snap là CÙNG một WAV (cùng md5).
    Cue section@w127 dùng whoosh/transition-snap; cue cắt zoom khai air/transition-snap cách
    2,7 s (< same_file_s) ⇒ L3 FAIL 'cùng file' nêu cả hai cue — so md5, không so khoá."""
    plan, man = v2plan_and_stem[0], v2plan_and_stem[4]
    assert man["files"]["whoosh/transition-snap"]["md5"] == man["files"]["air/transition-snap"]["md5"]
    snap = _cue(plan, "section@w127")
    assert snap["file"] == "whoosh/transition-snap"
    assert 2.0 <= snap["peak_s"] - _cue(plan, "section@w113")["peak_s"] < rules_110.get("sfx.same_file_s")
    bad = _edit_cue(plan, "section@w113", role="cut", tier="C", file="air/transition-snap")
    l3 = _by_code(_run(v2plan_and_stem, fixture_v2_pauses_full, rules_110, plan=bad))["L3"]
    assert not l3["ok"] and "cùng file section@w113–section@w127" in l3["msg"], l3


def test_l7_silent_pill_zone(v2plan, v2plan_and_stem, fixture_v2_words_corrected, fixture_v2_pauses_full,
                             v2_edit_v11, sfx_signals_110, rules_110):
    """A3 / S20 (R23): CTA không có tiếng (cue CTA BỎ) ⇒ pill hiện ở on(w147) không tiếng; plan
    đặt whoosh chuyển đoạn section@w147 trong chính khoảng ngắt trước câu CTA (cue dựng lại bằng
    planner.build_cue, stem và picture_lock dựng lại) ⇒ chỉ L7 FAIL, msg nêu section@w147."""
    plan, cues_audio = v2plan
    vo, man = v2plan_and_stem[2], v2plan_and_stem[4]
    cta = _cue(plan, "cta@w147")
    pause = next(tuple(p) for p in fixture_v2_pauses_full["pauses"]
                 if all(abs(a - b) <= lint.TOL for a, b in zip(p, cta["pause"])))
    ctx = planner.Ctx(man, sfx_signals_110, fixture_v2_pauses_full["vo_ref"], rules_110, "standard")
    cue, why = planner.build_cue(ctx, "whoosh/transition-soft", "pre", pause, "B", "whoosh")
    assert why is None, why
    show = fixture_v2_words_corrected[147]["on"]
    assert abs(cue["peak_s"] - show) < rules_110.get("sfx.cta_clear_s")
    fields = {k: round(float(cue[k]), 4) for k in ("peak_s", "start_s", "end_s", "gain_db", "fade_loss_db",
                                                    "short_db", "target_db")}
    fields.update(file=cue["file"], mode="pre", pause=list(cta["pause"]), frame=cue["frame"],
                  levels=dict(cta["levels"]))
    bad = copy.deepcopy(plan)
    for cand in bad["candidates"]:
        if cand["id"] == "cta@w147":
            cand.update(decision="BỎ", rule="S07", cue=None)
        elif cand["id"] == "section@w147":
            cand.update(decision="OK", rule=None, cue={k: fields[k] for k in lint._CUE_KEYS})
    bad["cues"] = [c for c in bad["cues"] if c["id"] != "cta@w147"] + [
        {"id": "section@w147", "role": "section", "tier": "B", **{k: fields[k] for k in lint._CUE_KEYS}}]
    i = plan["cues"].index(cta)
    stem = mix.render_stem([*cues_audio[:i], {"start_s": cue["start_s"], "samples": cue["samples"]},
                            *cues_audio[i + 1:]], len(vo))
    lock = picture.build_lock(fixture_v2_words_corrected, v2_edit_v11, bad, fixture_v2_pauses_full, rules_110)
    assert lock["cta"]["show"] == round(show, 4)

    res = _run(v2plan_and_stem, fixture_v2_pauses_full, rules_110, plan=bad, stem=stem, lock=lock)
    assert _failed(res) == {"L7"}, [r for r in res if not r["ok"]]
    assert "section@w147" in _by_code(res)["L7"]["msg"]


def test_l13_never_sound_role(v2plan_and_stem, fixture_v2_pauses_full, rules_110):
    """S19: cue gắn sự kiện thuộc NEVER_SOUND (hero script) ⇒ L13 FAIL."""
    plan = _edit_cue(v2plan_and_stem[0], "section@w21", role="hero_script")
    assert "L13" in _failed(_run(v2plan_and_stem, fixture_v2_pauses_full, rules_110, plan=plan))


def test_l14_plan_must_be_complete(v2plan_and_stem, fixture_v2_pauses_full, rules_110):
    """S23: thiếu slot đã thử, thiếu mức 3 miền, hay cues lệch ứng viên OK ⇒ L14 FAIL."""
    plan = v2plan_and_stem[0]
    no_tried = copy.deepcopy(plan)
    del no_tried["candidates"][0]["tried"]
    no_levels = copy.deepcopy(plan)
    del no_levels["cues"][0]["levels"]
    dropped = copy.deepcopy(plan)
    dropped["cues"] = dropped["cues"][1:]
    for bad in (no_tried, no_levels, dropped):
        assert "L14" in _failed(_run(v2plan_and_stem, fixture_v2_pauses_full, rules_110, plan=bad))


def test_l6_file_must_fit_role(v2plan_and_stem, fixture_v2_pauses_full, rules_110):
    """S03/S13: stomp dùng file của họ air, hoặc file không có trong manifest ⇒ L6 FAIL."""
    plan = v2plan_and_stem[0]
    for key in ("air/sweep-short", "impact/bass-hit-short"):
        bad = _edit_cue(plan, "b05", file=key)
        res = _by_code(_run(v2plan_and_stem, fixture_v2_pauses_full, rules_110, plan=bad))
        assert not res["L6"]["ok"] and key in res["L6"]["msg"]


def test_l6_detects_swapped_asset(v2plan_and_stem, fixture_v2_pauses_full, rules_110):
    """S13: md5 trong manifest phải khớp file WAV trên đĩa của release."""
    man = copy.deepcopy(v2plan_and_stem[4])
    man["files"]["impact/hit-weak"]["md5"] = "0" * 32
    scene = (*v2plan_and_stem[:4], man)
    res = _by_code(_run(scene, fixture_v2_pauses_full, rules_110))
    assert not res["L6"]["ok"] and "md5" in res["L6"]["msg"]


def test_l8_hook_must_be_tier_a(v2plan_and_stem, fixture_v2_pauses_full, rules_110):
    """S22: cue hook là impact tầng A."""
    plan = _edit_cue(v2plan_and_stem[0], "hook@w7", tier="B")
    assert "L8" in _failed(_run(v2plan_and_stem, fixture_v2_pauses_full, rules_110, plan=plan))


def test_low_density_warns_without_failing(v2plan, v2plan_and_stem, fixture_v2_pauses_full, rules_110):
    """S26: chỉ còn hook + CTA ⇒ L4 vẫn ok nhưng msg có WARN LOW_DENSITY."""
    plan, cues_audio = v2plan
    keep = [i for i, c in enumerate(plan["cues"]) if c["role"] in ("hook", "cta")]
    thin = copy.deepcopy(plan)
    thin["cues"] = [thin["cues"][i] for i in keep]
    kept = {c["id"] for c in thin["cues"]}
    for cand in thin["candidates"]:
        if cand["decision"] == "OK" and cand["id"] not in kept:
            cand.update(decision="BỎ", rule="OVERRIDE", cue=None)
    stem = mix.render_stem([cues_audio[i] for i in keep], len(v2plan_and_stem[2]))
    res = _by_code(_run(v2plan_and_stem, fixture_v2_pauses_full, rules_110, plan=thin, stem=stem))
    assert res["L4"]["ok"] and "LOW_DENSITY" in res["L4"]["msg"]


def test_l12_bed_level_and_short_term_max(v2plan_and_stem, fixture_v2_pauses_full, rules_110):
    """S29: bed = giọng − 15 LU (±1 LU, BS.1770 hai kênh — R10); S-max ≤ I + 6 LU."""
    vo = v2plan_and_stem[2]
    track = 0.2 * np.random.default_rng(0).standard_normal((8 * A.SR, 2))
    bed = mix.bgm_bed(track, vo, 42.0, rules_110)
    assert _by_code(_run(v2plan_and_stem, fixture_v2_pauses_full, rules_110, bed=bed))["L12"]["ok"]
    loud = _by_code(_run(v2plan_and_stem, fixture_v2_pauses_full, rules_110, bed=bed * 2))["L12"]
    assert not loud["ok"]

    burst = bed.copy()
    burst[10 * A.SR: 13 * A.SR] *= 10          # +20 dB trong 3 s
    burst *= 10 ** ((A.integrated_lufs(bed) - A.integrated_lufs(burst)) / 20)   # giữ I đúng đích
    spiky = _by_code(_run(v2plan_and_stem, fixture_v2_pauses_full, rules_110, bed=burst))["L12"]
    assert not spiky["ok"] and "S-max" in spiky["msg"]


def test_l12_passes_without_bed(v2plan_and_stem, fixture_v2_pauses_full, rules_110):
    assert _by_code(_run(v2plan_and_stem, fixture_v2_pauses_full, rules_110))["L12"]["ok"]


# ------------------------------------------------ bộ đổi 25 cue cũ


OLD_ROLES = (["hook", "stomp", "cut", "stomp", "hero_script", "card"] + ["list_item"] * 5
             + ["cut", "hero_script", "hero_script", "cut", "stomp", "stomp", "hero_script",
                "hero_script", "cut", "hero_script", "hero_script", "hero_script", "cta", "stomp"])


def test_old_cues_to_plan_maps_roles_and_peaks(old_cues_plan_and_stem, fixture_v2_pauses_full):
    """Vai lấy từ ghi chú (hook | chữ đập | hero | bảng | mục | CTA | cắt);
    đỉnh = from/30 + lag của file pack 1.0.0."""
    plan = old_cues_plan_and_stem[0]
    peaks = [c["peak_s"] for c in plan["cues"]]
    assert len(peaks) == 25 and peaks == sorted(peaks)
    by_id = {c["id"]: c for c in plan["candidates"]}
    assert [by_id["old%02d" % (i + 1)]["role"] for i in range(25)] == OLD_ROLES
    pack = paths.SKILL / "legacy" / "1.0.0" / "assets" / "sfx"
    lag = sfxlib.measure(A.decode_mono(pack / "impact" / "hit-blow.mp3"))["lag_ms"]
    assert abs(by_id["old02"]["cue"]["peak_s"] - (32 / 30 + lag / 1000)) <= 1e-3
    assert by_id["old02"]["cue"]["file"] == "impact/hit-blow.mp3"
    with pytest.raises(ValueError):
        lint.old_cues_to_plan([{"from": 0, "src": "sfx/x.mp3", "volume": 1.0, "note": "không rõ"}],
                              fixture_v2_pauses_full, {"x.mp3": {"lag_ms": 10}})


# ------------------------------------------------ L11 sau mux


def _write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")


def _mux(video_s, wav, mp4):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i",
                    f"color=c=black:s=64x64:r=30:d={video_s}", "-i", str(wav),
                    "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", str(mp4)],
                   check=True, capture_output=True)


def _band(n, amp, seed):
    """Nhiễu dải 100 Hz–4 kHz (như giọng: AAC không cắt mất năng lượng cao tần)."""
    sos = butter(4, (100, 4000), btype="bandpass", fs=A.SR, output="sos")
    return amp * sosfilt(sos, np.random.default_rng(seed).standard_normal(n))


def _post_project(root, R):
    """Dự án tổng hợp 8 s đã mux: giọng 0,2–3,5 s và 4,2–7,0 s, một cue chuyển
    đoạn trong khoảng ngắt giữa; t_end = đầu khoảng ngắt cuối + end.pad_s."""
    dur = 8.0
    vo = np.zeros(int(dur * A.SR))
    for k, (a, b) in enumerate(((0.2, 3.5), (4.2, 7.0))):
        vo[int(a * A.SR): int(b * A.SR)] = _band(int(b * A.SR) - int(a * A.SR), 0.2, k)
    n = int(0.3 * A.SR)
    cue = _band(n, 0.1, 9) * np.linspace(1, 0, n) ** 2
    stem = mix.render_stem([{"start_s": 3.6, "samples": cue}], len(vo))
    found = voice.find_pauses(vo, R)
    pauses = {"pauses": [list(p) for p in found], "designed_breaks": [], "vo_ref": None,
              "duration_s": dur, "last_word_end": voice.last_word_end([{"e": 7.0}], found, dur)}
    t_end = min(pauses["last_word_end"] + R.get("end.pad_s"), dur)
    (root / "public").mkdir(parents=True)
    A.write_wav(root / "public" / "vo-clean.wav", np.stack([vo, vo], axis=1))
    A.write_wav(root / "public" / "sfx_stem.wav", stem)
    raw = mix.mixdown(np.stack([vo, vo], axis=1), stem, None, t_end, R)
    A.write_wav(root / "raw.wav", raw)
    (root / "out").mkdir()
    for wav, target in (("mix.wav", -16.0), ("mix-nobgm.wav", -16.0), ("social.wav", -14.0)):
        mix.loudnorm_file(root / "raw.wav", root / "public" / wav, target, -1.5)
    for wav, mp4 in (("mix.wav", "final.mp4"), ("mix-nobgm.wav", "final-nobgm.mp4"),
                     ("social.wav", "final-social.mp4")):
        _mux(t_end, root / "public" / wav, root / "out" / mp4)
    peak = 3.6 + int(np.argmax(np.abs(cue))) / A.SR
    _write_json(root / "out" / "sfx_plan.json", {"cues": [
        {"id": "section@w3", "role": "section", "tier": "B", "mode": "pre",
         "frame": int(peak * 30), "peak_s": round(peak, 4)}]})
    _write_json(root / "pauses.json", pauses)
    _write_json(root / "picture_lock.json", {"fps": 30, "t_end": t_end,
                                             "duration_f": round(t_end * 30)})


def test_run_post_mux_checks_exports(tmp_path, rules_110):
    """L11 (S25/S18/S27): đủ 3 bản xuất, xcorr, cue −1/+2 f, loudness, phần kết."""
    _post_project(tmp_path, rules_110)
    res = lint.run_post_mux(tmp_path, rules_110)
    assert [r["code"] for r in res] == ["L11"]
    assert res[0]["ok"], res[0]["msg"]

    (tmp_path / "out" / "final-nobgm.mp4").unlink()
    res = lint.run_post_mux(tmp_path, rules_110)
    assert not res[0]["ok"] and "final-nobgm.mp4" in res[0]["msg"]

    (tmp_path / "public" / "mix.wav").unlink()      # mux chưa chạy xong: vẫn là L11 FAIL, không vỡ
    res = lint.run_post_mux(tmp_path, rules_110)
    assert not res[0]["ok"] and "public/mix.wav" in res[0]["msg"]


# ------------------------------------------------ CLI lint_sfx.py


def _cli_project(root, scene, words, pauses, edit, signals, R):
    """Dự án video 02 trên đĩa, chưa mux (vo-clean, stem của planner, JSON
    đầu vào, out/sfx_plan.json). Trả (thư mục dự án, plan)."""
    _, _, vo, lock, man = scene
    proj = root / "2" / "edit-r1.1.0"
    state.write_lock(proj, "1.1.0")
    (proj / "public").mkdir()
    A.write_wav(proj / "public" / "vo-clean.wav", np.stack([vo, vo], axis=1))
    vo_wav = A.decode_mono(proj / "public" / "vo-clean.wav")
    plan, cues_audio = planner.plan(words, pauses, edit, [], man, signals, vo_wav, R, "standard")
    A.write_wav(proj / "public" / "sfx_stem.wav", mix.render_stem(cues_audio, len(vo_wav)))
    for name, obj in (("words.json", words), ("pauses.json", pauses), ("edit.json", edit),
                      ("picture_lock.json", lock), ("meta.json", {"preset": "standard"}),
                      ("out/sfx_plan.json", plan)):
        _write_json(proj / name, obj)
    return proj, plan


def test_lint_sfx_cli(tmp_path, capsys, v2plan_and_stem, fixture_v2_words_corrected,
                      fixture_v2_pauses_full, v2_edit_v11, sfx_signals_110, rules_110):
    """lint_sfx.py đọc lại mọi thứ từ đĩa, chạy lại planner cho L10, ghi
    out/sfx_lint.json, in một dòng mỗi mã; plan bị đặt tay ⇒ exit 1."""
    proj, plan = _cli_project(tmp_path, v2plan_and_stem, fixture_v2_words_corrected,
                              fixture_v2_pauses_full, v2_edit_v11, sfx_signals_110, rules_110)

    assert lint_sfx.main([str(proj)]) == 0
    report = json.loads((proj / "out" / "sfx_lint.json").read_text(encoding="utf-8"))
    assert [r["code"] for r in report] == PRE_CODES and all(r["ok"] for r in report)
    lines = capsys.readouterr().out.splitlines()
    assert [ln.split()[0] for ln in lines if ln.split() and ln.split()[0] in PRE_CODES] == PRE_CODES

    plan["cues"][0]["gain_db"] += 1.0      # đặt tay ⇒ lệch output planner (S21)
    _write_json(proj / "out" / "sfx_plan.json", plan)
    assert lint_sfx.main([str(proj)]) == 1
    report = json.loads((proj / "out" / "sfx_lint.json").read_text(encoding="utf-8"))
    assert not _by_code(report)["L10"]["ok"]

    (proj / "picture_lock.json").unlink()
    assert lint_sfx.main([str(proj)]) == 1
    assert "picture_lock.json" in capsys.readouterr().out


def test_lint_sfx_cli_mux_mode_is_explicit(tmp_path, capsys, v2plan_and_stem, fixture_v2_words_corrected,
                                           fixture_v2_pauses_full, v2_edit_v11, sfx_signals_110,
                                           rules_110):
    """Chế độ do cờ --post-mux quyết định, không do out/final.mp4 có hay không:
    trước mux (BUILD) không đụng tới out/*.mp4 dù còn bản xuất cũ của lần trước;
    --post-mux (BUILD sau mux, VERIFY) luôn chấm L11 và thiếu final.mp4 là L11 FAIL."""
    proj, _ = _cli_project(tmp_path, v2plan_and_stem, fixture_v2_words_corrected,
                           fixture_v2_pauses_full, v2_edit_v11, sfx_signals_110, rules_110)
    stale = proj / "out" / "final.mp4"
    stale.write_bytes(b"ban xuat cu, hong")         # đọc tới là ffmpeg vỡ
    assert lint_sfx.main([str(proj)]) == 0
    report = json.loads((proj / "out" / "sfx_lint.json").read_text(encoding="utf-8"))
    assert [r["code"] for r in report] == PRE_CODES

    stale.unlink()
    pauses, fps = fixture_v2_pauses_full, rules_110.get("fps")
    t_end = min(pauses["last_word_end"] + rules_110.get("end.pad_s"), pauses["duration_s"])
    _write_json(proj / "picture_lock.json",
                {**v2plan_and_stem[3], "t_end": t_end, "duration_f": round(t_end * fps)})
    capsys.readouterr()
    assert lint_sfx.main([str(proj), "--post-mux"]) == 1
    report = json.loads((proj / "out" / "sfx_lint.json").read_text(encoding="utf-8"))
    assert [r["code"] for r in report] == PRE_CODES + ["L11"]
    assert all(r["ok"] for r in report[:-1])
    assert not report[-1]["ok"] and "out/final.mp4" in report[-1]["msg"]
    assert any(ln.startswith("L11  FAIL") for ln in capsys.readouterr().out.splitlines())
