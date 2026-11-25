"""thlib.editschema — schema `edit/1.1` (chỉ nhãn, không có giây), bộ kiểm
luật dựng (`validate`), đổi edit.json 1.0.0 sang 1.1 (`from_legacy`) và khung
đề xuất cho stage PLAN (`propose`).

Mọi chỉ số từ là nửa mở `[a, b)` vào words.json. Mọi ngưỡng đọc từ rules.json:
`text.*` (độ dài block, số từ hero, nhãn đập, khoảng cách shot, scale) và
`sfx.*` (`stomp_s`, `hook_window_s`, `cut_near_s`).

Quy ước đo (ghi rõ trong stages/PLAN.md):
- độ dài block = `e` của từ cuối − `s` của từ đầu (khoảng lời của block);
- mốc một sự kiện (nhãn đập, cú cắt) = `on` — onset thật S04 của từ;
- shot đầu là khung mở, không phải cú cắt, nên không xét CUT_SNAP.
"""

from __future__ import annotations

from typing import Any, Iterator

import jsonschema

from . import textnorm
from .rules import Rules

SCHEMA_ID = "edit/1.1"

# Biên so sánh số thực: mốc từ trong JSON làm tròn 4 chữ số (Ruling R4).
_TOL = 1e-6
_ONSET_TOL = 1e-3

# Trọng số của bộ cắt block trong `propose` (giây; chỉ ảnh hưởng khung đề xuất).
_BAD_CHUNK = 10.0      # đoạn ra ngoài 1,5–3 s
_OFF_PHRASE = 1.0      # đoạn không mở đầu ở một cụm lời
_CROSS_BREAK = 2.0     # đoạn nuốt một nhịp ngắt có chủ đích
_MAX_OVER_S = 2.0      # không xét đoạn dài quá block_max_s + 2 s

_COLORS = ["warn", "gold", "ink"]
_STOMP_LIKE = ("stomp", "quote")
_PARTS = ("top", "hero", "bottom")

_RANGE = {
    "type": "array",
    "items": {"type": "integer", "minimum": 0},
    "minItems": 2,
    "maxItems": 2,
}
_RANGE_OR_NULL = {"oneOf": [_RANGE, {"type": "null"}]}
_SCALE = {"type": "number", "minimum": 1.0}
_SHIFT = {"type": "number", "minimum": -0.25, "maximum": 0.25}

SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "edit/1.1 — nhãn dựng video talking-head",
    "type": "object",
    "required": ["schema", "hook", "blocks", "steps", "shots", "cta"],
    "additionalProperties": False,
    "properties": {
        "schema": {"const": SCHEMA_ID},
        "hook": {
            "oneOf": [
                {
                    "type": "object",
                    "required": ["text", "color", "hit_word"],
                    "additionalProperties": False,
                    "properties": {
                        "text": {"type": "string", "minLength": 1},
                        "color": {"enum": _COLORS},
                        "hit_word": {"type": ["integer", "null"], "minimum": 0},
                    },
                },
                {"type": "null"},
            ]
        },
        "blocks": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": [
                    "id", "top", "hero", "bottom", "style", "color", "accent",
                    "display", "reveal",
                ],
                "additionalProperties": False,
                "properties": {
                    "id": {"type": "string", "minLength": 1},
                    "top": _RANGE_OR_NULL,
                    "hero": _RANGE,
                    "bottom": _RANGE_OR_NULL,
                    "style": {"enum": ["script", "stomp", "quote"]},
                    "color": {"enum": [*_COLORS, None]},
                    "accent": {"type": ["integer", "null"], "minimum": 0},
                    "display": {
                        "type": "object",
                        "propertyNames": {"pattern": "^[0-9]+$"},
                        "additionalProperties": {"type": "string"},
                    },
                    "reveal": {"type": "boolean"},
                },
            },
        },
        "steps": {
            "oneOf": [
                {
                    "type": "object",
                    "required": ["title", "items"],
                    "additionalProperties": False,
                    "properties": {
                        "title": {"type": "string", "minLength": 1},
                        "items": {
                            "type": "array",
                            "minItems": 3,
                            "maxItems": 5,
                            "items": {
                                "type": "object",
                                "required": ["range", "label"],
                                "additionalProperties": False,
                                "properties": {
                                    "range": _RANGE,
                                    "label": {"type": "string", "minLength": 1},
                                },
                            },
                        },
                    },
                },
                {"type": "null"},
            ]
        },
        "shots": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["cut_at_word", "s0", "s1"],
                "additionalProperties": False,
                "properties": {
                    "cut_at_word": {"type": "integer", "minimum": 0},
                    "s0": _SCALE,
                    "s1": _SCALE,
                    "x": _SHIFT,
                    "y": _SHIFT,
                },
            },
        },
        "cta": {
            "oneOf": [
                {
                    "type": "object",
                    "required": ["label", "keyword"],
                    "additionalProperties": False,
                    "properties": {
                        "range": _RANGE_OR_NULL,
                        "label": {"type": "string", "minLength": 1},
                        "keyword": {"type": "string", "minLength": 1},
                    },
                },
                {"type": "null"},
            ]
        },
    },
}


# --- tiện ích chung -------------------------------------------------------


def _err(code: str, msg: str, where: str) -> dict:
    return {"code": code, "msg": msg, "where": where}


def _parts(block: dict) -> Iterator[tuple[str, list[int]]]:
    """(tên tầng, range) của các tầng có mặt trong block, theo thứ tự đọc."""
    for name in _PARTS:
        rng = block.get(name)
        if rng:
            yield name, rng


def _block_span(block: dict) -> tuple[int, int]:
    """Chỉ số từ đầu và từ cuối (nửa mở) của cả block."""
    ranges = [rng for _, rng in _parts(block)]
    return min(r[0] for r in ranges), max(r[1] for r in ranges)


def _text(words: list[dict], a: int, b: int) -> str:
    return " ".join(str(w["w"]) for w in words[a:b])


def _dur(words: list[dict], a: int, b: int) -> float:
    """Độ dài lời của đoạn [a, b): e của từ cuối − s của từ đầu."""
    return float(words[b - 1]["e"]) - float(words[a]["s"])


def _pause_dist(t: float, pause_list: list) -> float:
    """Khoảng cách từ thời điểm t tới khoảng ngắt gần nhất (0 nếu nằm trong)."""
    return min(
        (max(float(t0) - t, t - float(t1), 0.0) for t0, t1 in pause_list),
        default=float("inf"),
    )


def _hook_words(edit: dict, words: list[dict], R: Rules) -> set[int]:
    """Các từ do hook hiển thị (được phép vắng mặt trong block): từ trong cửa
    sổ hook có chữ trùng một token của hook.text, cộng chính `hit_word`."""
    hook = edit.get("hook")
    if not hook:
        return set()
    tokens = set(textnorm.norm(hook["text"]))
    window = R.get("sfx.hook_window_s")
    out = set()
    for k, w in enumerate(words):
        shown = set(textnorm.norm(str(w["w"])))
        if shown and shown <= tokens and float(w["on"]) <= window + _TOL:
            out.add(k)
    if hook.get("hit_word") is not None:
        out.add(hook["hit_word"])
    return out


# --- kiểm schema và biên chỉ số ------------------------------------------


def _schema_errors(edit: dict) -> list[dict]:
    validator = jsonschema.Draft202012Validator(SCHEMA)
    errors = []
    for exc in sorted(validator.iter_errors(edit), key=lambda e: list(e.absolute_path)):
        where = "/".join(str(p) for p in exc.absolute_path) or "edit"
        errors.append(_err("SCHEMA", f"sai schema {SCHEMA_ID}: {exc.message}", where))
    return errors


def _bounds_errors(edit: dict, words: list[dict]) -> list[dict]:
    """Chỉ số từ phải nằm trong words.json và range phải không rỗng."""
    n = len(words)
    errors: list[dict] = []

    def check_range(rng, label: str, where: str) -> bool:
        a, b = rng
        if not (0 <= a < b <= n):
            errors.append(_err("SCHEMA", f"{label} [{a}, {b}) ngoài khoảng từ 0–{n}", where))
            return False
        return True

    def check_index(value, label: str, where: str) -> None:
        if not 0 <= value < n:
            errors.append(_err("SCHEMA", f"{label} {value} ngoài khoảng từ 0–{n - 1}", where))

    for block in edit["blocks"]:
        where = block["id"]
        checked = [
            check_range(rng, f"{name} của block {where}", where) for name, rng in _parts(block)
        ]
        if not all(checked):
            continue
        hero = block["hero"]
        if block["accent"] is not None and not 0 <= block["accent"] < hero[1] - hero[0]:
            errors.append(
                _err("SCHEMA", f"accent {block['accent']} của block {where} ngoài hero "
                     f"({hero[1] - hero[0]} từ)", where)
            )
        covered = {i for _, rng in _parts(block) for i in range(*rng)}
        for key in block["display"]:
            if int(key) not in covered:
                errors.append(
                    _err("SCHEMA", f"display có từ {key} không thuộc block {where}", where)
                )

    steps = edit.get("steps")
    if steps:
        for k, item in enumerate(steps["items"]):
            check_range(item["range"], f"range của mục {k + 1}", f"steps.items[{k}]")

    hook = edit.get("hook")
    if hook and hook.get("hit_word") is not None:
        check_index(hook["hit_word"], "hit_word", "hook")

    cta = edit.get("cta")
    if cta and cta.get("range"):
        check_range(cta["range"], "cta.range", "cta")

    for k, shot in enumerate(edit["shots"]):
        check_index(shot["cut_at_word"], "cut_at_word", f"shots[{k}]")

    return errors


# --- các luật dựng --------------------------------------------------------


def _check_blocks(edit: dict, words: list[dict], R: Rules) -> list[dict]:
    """BLOCK_LEN (độ dài lời), HERO_WORDS (số từ hero), REVEAL_STYLE."""
    lo, hi = R.get("text.block_min_s"), R.get("text.block_max_s")
    hero_lo, hero_hi = R.get("text.hero_words_min"), R.get("text.hero_words_max")
    errors: list[dict] = []

    for block in edit["blocks"]:
        where = block["id"]
        a, b = _block_span(block)
        dur = _dur(words, a, b)
        if not lo - _TOL <= dur <= hi + _TOL:
            errors.append(
                _err("BLOCK_LEN", f"block {where} dài {dur:.2f} s — ngoài {lo:.1f}–{hi:.1f} s "
                     f"(tách đôi hoặc gộp với block kề)", where)
            )
        hero_n = block["hero"][1] - block["hero"][0]
        if not hero_lo <= hero_n <= hero_hi:
            errors.append(
                _err("HERO_WORDS", f"hero của block {where} có {hero_n} từ — phải "
                     f"{hero_lo}–{hero_hi} từ", where)
            )
        if block["reveal"] and block["style"] != "script":
            errors.append(
                _err("REVEAL_STYLE", f"block {where} bật reveal nhưng style là "
                     f"'{block['style']}' — reveal chỉ dành cho block script", where)
            )
    return errors


def _check_coverage(edit: dict, words: list[dict], R: Rules) -> list[dict]:
    """OVERLAP_OR_GAP: range nối tiếp, không chồng, không bỏ từ (trừ đoạn
    nhường cho steps hoặc hook)."""
    errors: list[dict] = []
    owner: list[str | None] = [None] * len(words)

    def claim(rng, name: str) -> None:
        conflicts: dict[str, int] = {}
        for i in range(*rng):
            if owner[i] is not None:
                conflicts.setdefault(owner[i], i)
            else:
                owner[i] = name
        for other, i in conflicts.items():
            errors.append(
                _err("OVERLAP_OR_GAP", f"từ {i} («{words[i]['w']}») nằm trong cả {other} và "
                     f"{name} — các range không được chồng nhau", name)
            )

    previous_end = -1
    for block in edit["blocks"]:
        where = block["id"]
        parts = list(_parts(block))
        for (name_a, rng_a), (name_b, rng_b) in zip(parts, parts[1:]):
            if rng_a[1] > rng_b[0]:
                errors.append(
                    _err("OVERLAP_OR_GAP", f"trong block {where}, {name_a} và {name_b} không "
                         f"nối tiếp theo thứ tự top → hero → bottom", where)
                )
        start, end = _block_span(block)
        if start < previous_end:
            errors.append(
                _err("OVERLAP_OR_GAP", f"block {where} bắt đầu ở từ {start}, trước block liền "
                     f"trước — các block phải xếp theo thứ tự lời", where)
            )
        previous_end = max(previous_end, end)
        for _, rng in parts:
            claim(rng, where)

    steps = edit.get("steps")
    if steps:
        for k, item in enumerate(steps["items"]):
            claim(item["range"], f"steps.items[{k}]")

    free = _hook_words(edit, words, R)
    missing = [i for i in range(len(words)) if owner[i] is None and i not in free]
    for a, b in _runs(missing):
        errors.append(
            _err("OVERLAP_OR_GAP", f"bỏ từ {a}–{b - 1} («{_text(words, a, b)}») — mọi từ phải "
                 f"thuộc một block, một mục steps hoặc hook", f"words[{a}]")
        )
    return errors


def _check_steps(edit: dict) -> list[dict]:
    """STEPS: các mục của bảng liền nhau, và không block nào bắt đầu trong khoảng bảng
    [từ đầu mục 1, hết mục cuối) — block chen giữa làm thẻ ra trước block đó (R34) nên
    các mục sau không bao giờ hiện."""
    steps = edit.get("steps")
    if not steps:
        return []
    items, errors = steps["items"], []
    for k in range(1, len(items)):
        end, start = items[k - 1]["range"][1], items[k]["range"][0]
        if start != end:
            errors.append(_err("STEPS", f"mục {k} hết ở từ {end} nhưng mục {k + 1} bắt đầu ở từ "
                               f"{start} — các mục phải liền nhau", f"steps.items[{k}]"))
    lo, hi = items[0]["range"][0], items[-1]["range"][1]
    for block in edit["blocks"]:
        start = _block_span(block)[0]
        if lo <= start < hi:
            errors.append(_err("STEPS", f"block {block['id']} bắt đầu ở từ {start}, trong khoảng bảng "
                               f"liệt kê (từ {lo}–{hi - 1}) — không đặt block trong khoảng thời gian "
                               f"của bảng", block["id"]))
    return errors


def _runs(indices: list[int]) -> list[tuple[int, int]]:
    """Gom các chỉ số liên tiếp thành các đoạn nửa mở [a, b)."""
    runs: list[tuple[int, int]] = []
    for i in indices:
        if runs and runs[-1][1] == i:
            runs[-1] = (runs[-1][0], i + 1)
        else:
            runs.append((i, i + 1))
    return runs


def hero_has_cta_keyword(block: dict, words: list[dict], keyword: str) -> bool:
    """S20: hero HIỂN THỊ của block (tính cả `display`) chứa đủ mọi token của
    keyword CTA, so theo tập token `textnorm.norm` (không so chuỗi con: «20
    lần» không chứa «2 LẦN»). Một định nghĩa duy nhất cho validate_edit
    (CTA_KEYWORD_IN_STOMP) và planner (ứng viên stomp XOÁ / S20)."""
    wanted = set(textnorm.norm(keyword))
    shown = " ".join(
        block["display"].get(str(i), str(words[i]["w"])) for i in range(*block["hero"])
    )
    return bool(wanted) and wanted <= set(textnorm.norm(shown))


def _check_stomps(edit: dict, words: list[dict], R: Rules) -> list[dict]:
    """STOMP_SPACING, STOMP_LIKE_MAX, CTA_KEYWORD_IN_STOMP."""
    errors: list[dict] = []
    gap_min = R.get("sfx.stomp_s")
    max_like = R.get("text.max_stomp_like")

    stomp_like = [b for b in edit["blocks"] if b["style"] in _STOMP_LIKE]
    previous = None
    for block in stomp_like:
        onset = float(words[_block_span(block)[0]]["on"])
        if previous is not None and onset - previous[1] < gap_min - _TOL:
            errors.append(
                _err("STOMP_SPACING", f"block {block['id']} cách nhãn đập trước "
                     f"({previous[0]}) {onset - previous[1]:.2f} s — phải ≥ {gap_min:.0f} s",
                     block["id"])
            )
        previous = (block["id"], onset)

    like_count = len(stomp_like) + sum(1 for b in edit["blocks"] if b["reveal"])
    if like_count > max_like:
        errors.append(
            _err("STOMP_LIKE_MAX", f"video có {like_count} nhãn đập (stomp/quote/reveal) — "
                 f"tối đa {max_like}", "blocks")
        )

    cta = edit.get("cta")
    if cta:
        for block in stomp_like:
            if hero_has_cta_keyword(block, words, cta["keyword"]):
                errors.append(
                    _err("CTA_KEYWORD_IN_STOMP", f"hero của block {block['id']} chứa từ khoá "
                         f"CTA «{cta['keyword']}» — đổi block sang script hoặc chọn hero khác "
                         f"(tránh đập hai lần ở CTA)", block["id"])
                )
    return errors


def _check_hook_cta(edit: dict, words: list[dict], R: Rules) -> list[dict]:
    """HIT_WORD (hook), CTA_RANGE, CTA_TEXT (độ dài nhãn/từ khoá pill CTA — B2)."""
    errors: list[dict] = []
    hook = edit.get("hook")
    if hook and hook.get("hit_word") is not None:
        hit = hook["hit_word"]
        in_stomp = any(
            b["style"] == "stomp" and b["hero"][0] <= hit < b["hero"][1] for b in edit["blocks"]
        )
        if not in_stomp:
            errors.append(
                _err("HIT_WORD", f"hit_word {hit} («{words[hit]['w']}») không nằm trong hero "
                     f"của block stomp nào", "hook")
            )
        window = R.get("sfx.hook_window_s")
        onset = float(words[hit]["on"])
        if onset > window + _TOL:
            errors.append(
                _err("HIT_WORD", f"hit_word {hit} («{words[hit]['w']}») nói ở giây {onset:.2f} "
                     f"— hook chỉ đặt trong {window:.1f} s đầu", "hook")
            )

    cta = edit.get("cta")
    if cta is not None and not cta.get("range"):
        errors.append(
            _err("CTA_RANGE", "có cta nhưng thiếu cta.range — phải chỉ ra câu CTA bằng chỉ số "
                 "từ (lời không nói CTA thì bỏ hẳn cta và báo user)", "cta")
        )
    for key in ("label", "keyword") if cta else ():
        limit = R.get(f"text.cta_{key}_max_chars")
        if len(cta[key]) > limit:
            errors.append(_err("CTA_TEXT", f"cta.{key} «{cta[key]}» dài {len(cta[key])} ký tự — tối đa "
                               f"{limit} (pill CTA phải vừa hộp chữ)", f"cta.{key}"))
    return errors


def _t_end(pauses: dict, R: Rules) -> float:
    """S27, cùng định nghĩa với picture._t_end: đầu khoảng ngắt sau từ cuối + end.pad_s,
    không quá độ dài nguồn."""
    lwe = float(pauses["last_word_end"])
    p0 = next((float(p[0]) for p in pauses["pauses"] if float(p[0]) >= lwe - _ONSET_TOL), lwe)
    return min(p0 + R.get("end.pad_s"), float(pauses["duration_s"]))


def _check_tail(edit: dict, words: list[dict], pauses: dict, R: Rules) -> list[dict]:
    """SHOT_GAP ở mép cuối: từ lúc shot cuối bắt đầu (0 s nếu chỉ có shot đầu — R24) tới
    t_end ≤ shot_gap_max_s, trừ shot đẩy vào CTA (cắt ở/sau từ đầu câu CTA)."""
    shots, gap_hi = edit["shots"], R.get("text.shot_gap_max_s")
    last = len(shots) - 1
    start = float(words[shots[last]["cut_at_word"]]["on"]) if last > 0 else 0.0
    cta = edit.get("cta") or {}
    if last > 0 and cta.get("range") and shots[last]["cut_at_word"] >= cta["range"][0]:
        return []
    tail = _t_end(pauses, R) - start
    if tail <= gap_hi + _TOL:
        return []
    return [_err("SHOT_GAP", f"shot cuối (shot {last}) giữ {tail:.2f} s tới hết video — phải ≤ "
                 f"{gap_hi:.1f} s: thêm cú cắt, hoặc cắt shot cuối ở từ đầu câu CTA", f"shots[{last}]")]


def _check_shots(edit: dict, words: list[dict], pauses: dict, R: Rules) -> list[dict]:
    """SCALE, SHOT_GAP (cả hai mép video: cú cắt đầu đo từ 0 s — R24 — và _check_tail),
    CUT_SNAP."""
    errors: list[dict] = []
    scale_max, scale_hi = R.get("text.scale_max"), R.get("text.scale_hi")
    hi_left = R.get("text.scale_hi_max_shots")
    gap_lo, gap_hi = R.get("text.shot_gap_min_s"), R.get("text.shot_gap_max_s")
    near = R.get("sfx.cut_near_s")
    pause_list = pauses["pauses"]

    for k, shot in enumerate(edit["shots"]):
        where = f"shots[{k}]"
        scale = max(shot["s0"], shot["s1"])
        if scale > scale_hi + _TOL:
            errors.append(
                _err("SCALE", f"shot {k} phóng tới {scale:.2f} — trần tuyệt đối "
                     f"{scale_hi:.2f}", where)
            )
        elif scale > scale_max + _TOL:
            if hi_left > 0:
                hi_left -= 1
            else:
                errors.append(
                    _err("SCALE", f"shot {k} phóng tới {scale:.2f} — quá {scale_max:.2f} và đã "
                         f"dùng hết {R.get('text.scale_hi_max_shots')} shot được vượt", where)
                )

        word = shot["cut_at_word"]
        onset = float(words[word]["on"])
        if k > 0:
            previous = edit["shots"][k - 1]["cut_at_word"]
            if word <= previous:
                errors.append(
                    _err("SHOT_GAP", f"shot {k} cắt ở từ {word}, không sau cú cắt trước "
                         f"({previous}) — shots phải xếp tăng dần", where)
                )
            else:
                # R24: shot đầu chạy từ t = 0 nên cú cắt thật đầu tiên đo từ 0 s.
                gap = onset - (float(words[previous]["on"]) if k > 1 else 0.0)
                if not gap_lo - _TOL <= gap <= gap_hi + _TOL:
                    errors.append(
                        _err("SHOT_GAP", f"cú cắt {k} cách {'cú trước' if k > 1 else 'đầu video'} "
                             f"{gap:.2f} s — phải {gap_lo:.1f}–{gap_hi:.1f} s", where)
                    )
            distance = _pause_dist(onset, pause_list)
            if distance > near + _TOL:
                errors.append(
                    _err("CUT_SNAP", f"cú cắt {k} ở từ {word} («{words[word]['w']}») cách "
                         f"khoảng ngắt gần nhất {distance:.2f} s — phải ≤ {near:.1f} s", where)
                )
    return errors + _check_tail(edit, words, pauses, R)


def validate(edit: dict, words: list[dict], pauses: dict, R: Rules) -> list[dict]:
    """Kiểm một edit.json 1.1 theo bộ luật; trả về danh sách
    `{"code", "msg", "where"}` (rỗng = ĐẠT). Sai schema hoặc chỉ số vượt số từ
    thì trả về ngay các lỗi đó — các luật sau cần cấu trúc đúng mới đo được."""
    errors = _schema_errors(edit)
    if errors:
        return errors
    errors = _bounds_errors(edit, words)
    if errors:
        return errors

    return (
        _check_blocks(edit, words, R)
        + _check_coverage(edit, words, R)
        + _check_steps(edit)
        + _check_stomps(edit, words, R)
        + _check_hook_cta(edit, words, R)
        + _check_shots(edit, words, pauses, R)
    )


# --- đổi edit.json 1.0.0 sang 1.1 ----------------------------------------


def _word_at(words: list[dict], t: float) -> int:
    """Từ đầu tiên có `s` ≥ t (hết lời thì lấy từ cuối)."""
    return next((k for k, w in enumerate(words) if float(w["s"]) >= t), len(words) - 1)


def from_legacy(legacy: dict, words: list[dict]) -> dict:
    """Đổi edit.json 1.0.0 (có giây) sang schema edit/1.1 (chỉ nhãn): `shots.t`
    và `cta.start` thành chỉ số từ, `fix` thành `display` của block chứa từ đó;
    mọi nhãn khác giữ nguyên. `words` phải là bảng từ mà edit cũ tham chiếu."""
    def copy_range(rng):
        return list(rng) if rng else None

    blocks = []
    for block in legacy["blocks"]:
        blocks.append({
            "id": block["id"],
            "top": copy_range(block.get("top")),
            "hero": list(block["hero"]),
            "bottom": copy_range(block.get("bottom")),
            "style": block.get("style", "script"),
            "color": block.get("color"),
            "accent": block.get("accent"),
            "display": {},
            "reveal": False,
        })

    for key, shown in (legacy.get("fix") or {}).items():
        index = int(key)
        for block in blocks:
            if any(rng[0] <= index < rng[1] for _, rng in _parts(block)):
                block["display"][str(index)] = shown
                break

    hook = legacy.get("hook")
    cta = legacy.get("cta")
    steps = legacy.get("steps")
    return {
        "schema": SCHEMA_ID,
        "hook": (
            {"text": hook["text"], "color": hook.get("color", "gold"), "hit_word": None}
            if hook else None
        ),
        "blocks": blocks,
        "steps": (
            {
                "title": steps["title"],
                "items": [
                    {"range": list(item["range"]), "label": item["label"]}
                    for item in steps["items"]
                ],
            }
            if steps else None
        ),
        "shots": [
            {
                "cut_at_word": _word_at(words, float(shot["t"])),
                "s0": shot["s0"],
                "s1": shot["s1"],
                **({"x": shot["x"]} if "x" in shot else {}),
                **({"y": shot["y"]} if "y" in shot else {}),
            }
            for shot in legacy["shots"]
        ],
        "cta": (
            {
                "range": [_word_at(words, float(cta["start"])), len(words)],
                "label": cta["label"],
                "keyword": cta["keyword"],
            }
            if cta else None
        ),
    }


# --- khung đề xuất cho PLAN ----------------------------------------------


def _phrase_starts(words: list[dict], pause_list: list) -> list[int]:
    """Từ mở đầu một cụm lời: từ đầu bài và mọi từ có onset đúng bằng mốc kết
    thúc của một khoảng ngắt (S04 gán onset = t1)."""
    ends = [float(t1) for _, t1 in pause_list]
    return [
        k for k, w in enumerate(words)
        if k == 0 or any(abs(float(w["on"]) - t1) <= _ONSET_TOL for t1 in ends)
    ]


def _split(
    words: list[dict], starts: set[int], breaks: set[int], R: Rules
) -> list[tuple[int, int]]:
    """Cắt lời thành các đoạn dài `block_min_s`–`block_max_s`, bằng quy hoạch
    động: mỗi đoạn tốn |độ dài − độ dài lý tưởng|, cộng phạt nếu không mở đầu
    ở một cụm lời, nếu nuốt một nhịp ngắt có chủ đích, hoặc nếu ra ngoài
    khoảng cho phép (phạt nặng, chỉ nhận khi không còn cách khác)."""
    lo, hi = R.get("text.block_min_s"), R.get("text.block_max_s")
    ideal = (lo + hi) / 2
    n = len(words)
    cost = [float("inf")] * (n + 1)
    back = [0] * (n + 1)
    cost[0] = 0.0
    for i in range(1, n + 1):
        for j in range(i - 1, -1, -1):
            length = _dur(words, j, i)
            if length > hi + _MAX_OVER_S and j < i - 1:
                break
            here = abs(length - ideal)
            if not lo - _TOL <= length <= hi + _TOL:
                here += _BAD_CHUNK
            if j not in starts:
                here += _OFF_PHRASE
            if any(j < b < i for b in breaks):
                here += _CROSS_BREAK
            if cost[j] + here < cost[i]:
                cost[i], back[i] = cost[j] + here, j

    chunks: list[tuple[int, int]] = []
    i = n
    while i > 0:
        chunks.append((back[i], i))
        i = back[i]
    return list(reversed(chunks))


def _pick_cuts(candidates: list[int], words: list[dict], R: Rules) -> list[int]:
    """Chọn các từ để cắt máy: mỗi lần lấy ứng viên có khoảng cách gần giữa
    khoảng cho phép nhất (2–4 s -> đích 3 s). Không còn ứng viên nào trong
    khoảng thì lấy ứng viên gần nhất phía sau — validate sẽ báo SHOT_GAP."""
    gap_lo, gap_hi = R.get("text.shot_gap_min_s"), R.get("text.shot_gap_max_s")
    ideal = (gap_lo + gap_hi) / 2
    on = [float(w["on"]) for w in words]
    cuts = [candidates[0]]
    pool = [c for c in candidates[1:]]
    while pool:
        last = on[cuts[-1]] if len(cuts) > 1 else 0.0   # R24: shot đầu chạy từ 0 s
        fits = [c for c in pool if gap_lo - _TOL <= on[c] - last <= gap_hi + _TOL]
        if fits:
            pick = min(fits, key=lambda c: (abs(on[c] - last - ideal), c))
        else:
            beyond = [c for c in pool if on[c] - last > gap_hi]
            if not beyond:
                break
            pick = beyond[0]
        cuts.append(pick)
        pool = [c for c in pool if c > pick]
    return cuts


def propose(words: list[dict], pauses: dict, designed_breaks: list[dict], R: Rules) -> dict:
    """Khung edit.json 1.1 do code sinh cho stage PLAN: mỗi block là một cụm
    lời 1,5–3 s cắt ở khoảng ngắt, hero là 2–4 từ cuối cụm, style script; cú
    cắt máy cách nhau 2–4 s ngay tại đầu block, xen toàn/cận. Hook, steps và
    CTA để trống — đó là phần phán đoán của agent (stages/PLAN.md)."""
    pause_list = pauses["pauses"]
    starts = set(_phrase_starts(words, pause_list))
    breaks = {b["after_word"] + 1 for b in designed_breaks if 0 < b["after_word"] + 1 < len(words)}
    chunks = _split(words, starts, breaks, R)

    blocks = []
    for k, (a, b) in enumerate(chunks):
        hero_n = min(4, max(2, b - a - 2))
        hero_a = max(a, b - hero_n)
        blocks.append({
            "id": f"b{k + 1:02d}",
            "top": [a, hero_a] if hero_a > a else None,
            "hero": [hero_a, b],
            "bottom": None,
            "style": "script",
            "color": None,
            "accent": None,
            "display": {},
            "reveal": False,
        })

    # Cắt máy ở đầu block; khi hai đầu block cách nhau quá 4 s thì thêm đầu cụm
    # lời ở giữa — mọi ứng viên đều phải snap được vào một khoảng ngắt.
    near = R.get("sfx.cut_near_s")
    candidates = [
        a for a in sorted(starts | {a for a, _ in chunks})
        if a == chunks[0][0] or _pause_dist(float(words[a]["on"]), pause_list) <= near + _TOL
    ]
    shots = [
        {
            "cut_at_word": word,
            "s0": 1.00 if k % 2 == 0 else 1.16,
            "s1": 1.04 if k % 2 == 0 else 1.20,
            "x": 0.0,
            "y": 0.0,
        }
        for k, word in enumerate(_pick_cuts(candidates, words, R))
    ]

    return {
        "schema": SCHEMA_ID,
        "hook": None,
        "blocks": blocks,
        "steps": None,
        "shots": shots,
        "cta": None,
    }
