"""thlib.picture — khoá hình (picture_lock.json) và src/data/script.ts cho
template 1.1 (§5.7 bước 7; S08, S20, S22, S24, S27, B14).

Khoá hình ghi mốc hiển thị (giây, trục vo-clean) của mọi thứ template vẽ: chữ
từng từ, lúc block tắt, thẻ liệt kê, pill CTA, tít hook, cú cắt. Remotion chỉ
đọc script.ts sinh từ khoá này, không tự suy thời gian từ lời.

Luật hiển thị (`show` = lúc animation của phần tử bắt đầu):
- mỗi từ hiện ở `on − text.lead_s` (onset thật S04);
- block có cue stomp/reveal OK — hoặc (Ruling R22) ứng viên stomp/reveal của
  nó bị GỘP vào một cue OK khác cùng khoảng ngắt — thì top + hero hiện cùng lúc
  ở display_s = đỉnh − sync_frame.block/fps (S08); bottom vẫn theo lời;
- thẻ: cue thẻ OK ⇒ vào ở đỉnh − sync_frame.card/fps; không thì mục 1 − 0,29 s
  nhưng không trước khi từ cuối của block trước thẻ đọc xong và block đó chuyển
  nhanh xong (R32); mục hiện ở on + 2 f − lead; thẻ ra ở min(từ cuối của mục cuối
  + 0,15 s; block đầu tiên sau thẻ hiện − 8 f thoát của thẻ) — thẻ ra xong trước
  khi block đó hiện (R34);
- pill CTA: cue CTA pre-hit ⇒ đỉnh − sync_frame.cta_pill/fps; post-hit hay
  không có tiếng ⇒ on(cta.range[0]), tại đó không có tiếng (R23, S20);
- block tắt (R30) — thẻ và phụ đề chung đáy hộp chữ: thoát thường 6 f ở
  min(e từ cuối + 0,22 s; lúc phải tắt xong − 0,22 s), lúc phải tắt xong là lúc
  block sau hiện, hoặc lúc thẻ vào với block cuối trước thẻ; thoát thường cắt mất
  từ cuối (chưa đậm ≥ 90 % đủ 3 frame) thì chuyển nhanh 2 f (`exit_f`), tắt xong
  đúng lúc phải tắt xong;
- vẫn không đủ thì dời mốc hiện (R31): block sau không đồng bộ ⇒ các từ đầu của nó
  hiện muộn lại vừa đủ; thứ hiện sau khoá theo cue (block đồng bộ, thẻ có tiếng)
  ⇒ đuôi block này (nếu không đồng bộ) hiện sớm lại vừa đủ. Mỗi từ dời ≤ 0,15 s,
  từ bị lùi hiện ≤ 0,10 s sau onset, độ dời ghi ở `display_shift_s` của từ; sự
  kiện có tiếng không dời (S08). Hết cách thì giữ mốc tốt nhất có thể và ghi
  `LAST_WORD_TIGHT:<id>` vào `warnings` của khoá (CONCERN, không làm hỏng BUILD);
- t_end = đầu khoảng ngắt sau từ cuối + end.pad_s (≤ độ dài), duration_f =
  round(t_end × fps) (S27) — cùng định nghĩa với L11;
- shot đầu là khung mở (t = 0, không phải cú cắt — Ruling R24); cú cắt ở
  on(cut_at_word), có cue cắt hoặc chuyển đoạn OK neo đúng từ cắt thì snap vào
  frame đỉnh k/fps.
Mọi số thực làm tròn 4 số lẻ (tất định, như sfx_plan).
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from . import planner
from .rules import Rules

# Mốc tít hook (giây) — khớp Hook.tsx: vào trong [0, land] (outCubic), đẩy nhẹ
# tới out, thoát tới end. land × fps = 10,2 f ⇒ đạt 90 % ở frame 6 =
# sfx.sync_frame.hook_title (test so); tít còn trên hình tới end = 1,5 s (S22).
HOOK_TIMING = {"land": 0.34, "out": 1.08, "end": 1.5}
_HOLD_S = 0.22         # block giữ sau từ cuối (HOLD của Subtitle 1.0.0)
_YIELD_S = 0.22        # block tắt trước lúc phải tắt xong (block sau hiện, thẻ vào)
_EXIT_F = 6            # frame thoát thường của block (Subtitle.tsx đọc exit_f)
_QUICK_EXIT_F = 2      # R30: chuyển nhanh khi thoát thường cắt mất từ cuối
_READ_F = 3            # R30: từ cuối đậm ≥ 90 % trong ≥ 3 frame liền
_MAX_SHIFT_S = 0.15    # R31: mỗi từ dời mốc hiện tối đa
_MAX_LATE_S = 0.10     # R31: từ bị lùi hiện tối đa sau onset của nó
_CARD_EXIT_F = 8       # R34: frame thoát của thẻ (OUT của StepList.tsx)
_STEPS_LEAD_S = 0.29   # thẻ vào trước mục 1 khi thẻ không có tiếng (1.0.0)
_STEPS_HOLD_S = 0.15   # thẻ giữ sau từ cuối của mục cuối (1.0.0)
_ITEM_DELAY_F = 2      # mục liệt kê hiện sau onset 2 frame
_TOL = 1e-3            # R4: số trong pauses.json / sfx_plan làm tròn 4 số lẻ
_SYNC_AT = 0.9         # S24: tiến độ animation coi là "đã tới"
_BLOCK_ROLES = ("stomp", "reveal")

TS_HEAD = ("// TỰ SINH bởi thlib.picture.write_script_ts từ picture_lock.json — "
           "đừng sửa tay, BUILD sinh lại.\n")
# Kiểu dữ liệu của script.ts — bản giữ chỗ trong template khai đúng khối này.
TS_TYPES = """export type Word = { t: string; show: number; display_shift_s?: number };
export type Block = {
  id: string;
  style: "script" | "stomp" | "quote";
  color: "warn" | "gold" | "ink" | null;
  accent: number | null;
  synced: boolean;
  out: number;
  exit_f: number;
  top: Word[]; hero: Word[]; bottom: Word[];
};
export type Steps = { title: string; in: number; out: number; items: { label: string; show: number }[] };
export type Shot = { t: number; s0: number; s1: number; x?: number; y?: number };
export type Hook = { text: string; color: "warn" | "gold" | "ink"; land: number; out: number; end: number };
export type Cta = { label: string; keyword: string; show: number };
export type Safe = {
  text_x_min: number; text_x_max: number; text_y_min: number; text_y_max: number;
  sub_bottom_px: number; sub_max_w: number; subject_y_min: number; subject_y_max: number;
};
"""


def SYNC_PROGRESS(frames: float, ease) -> int:
    """S24: frame đầu tiên mà animation dài `frames` frame, easing `ease`, đạt
    ≥ 90 % tiến độ — phải bằng sfx.sync_frame.* của rules.json."""
    return next(f for f in range(math.ceil(frames) + 1) if ease(min(1.0, f / frames)) >= _SYNC_AT)


def _r(x: float) -> float:
    return round(float(x), 4)


def _block_sync(plan: dict) -> dict:
    """id block → frame đỉnh mà top + hero của block đồng bộ theo (S08): cue
    stomp/reveal OK của chính block, hoặc (R22) cue OK đã GỘP ứng viên
    stomp/reveal của block vì chung khoảng ngắt."""
    out = {}
    for c in plan["candidates"]:
        if c["role"] in _BLOCK_ROLES:
            host = c["cue"] if c["decision"] == "OK" else planner.merged_into(c, plan["cues"])
            if host is not None:
                out[c["id"]] = host["frame"]
    return out


def _line(words: list[dict], rng, display: dict, lead: float, show: float | None) -> list[dict]:
    """Chữ của một dòng: text hiển thị (`display` của block đè chữ lời) và mốc hiện."""
    if rng is None:
        return []
    return [{"t": display.get(str(k), words[k]["w"]),
             "show": _r(words[k]["on"] - lead if show is None else show)} for k in range(*rng)]


def _indices(spec: dict) -> list[int]:
    """Chỉ số từ (words.json) của một block edit, theo thứ tự top + hero + bottom."""
    return [k for rng in (spec["top"], spec["hero"], spec["bottom"]) if rng for k in range(*rng)]


def _block_words(block: dict) -> list[dict]:
    return block["top"] + block["hero"] + block["bottom"]


def _first(block: dict) -> float:
    return min(w["show"] for w in _block_words(block))


def _last(block: dict) -> float:
    return max(w["show"] for w in _block_words(block))


def _block_lines(words: list[dict], edit: dict, plan: dict, R: Rules) -> list[dict]:
    """Block của khoá với chữ ở mốc hiện gốc (S08); out/exit_f điền sau ở _blocks."""
    fps, lead, sync = R.get("fps"), R.get("text.lead_s"), R.get("sfx.sync_frame.block")
    synced = _block_sync(plan)
    out = []
    for spec in edit["blocks"]:
        frame = synced.get(spec["id"])
        show = None if frame is None else (frame - sync) / fps
        display = spec.get("display") or {}
        out.append({"id": spec["id"], "style": spec["style"], "color": spec["color"],
                    "accent": spec["accent"], "synced": frame is not None, "out": None, "exit_f": None,
                    "top": _line(words, spec["top"], display, lead, show),
                    "hero": _line(words, spec["hero"], display, lead, show),
                    "bottom": _line(words, spec["bottom"], display, lead, None)})
    return out


def _progress(f: int, show: float, R: Rules) -> float:
    """Tiến độ hiện ở frame f của từ hiện ở `show` — wordP của Subtitle.tsx: outCubic
    qua text.reveal_f frame."""
    t = min(1.0, max(0.0, (f - show * R.get("fps")) / R.get("text.reveal_f")))
    return 1 - (1 - t) ** 3


def _f90(show: float, R: Rules) -> int:
    """Frame đầu tiên từ hiện ở `show` đạt ≥ 90 % tiến độ (S24)."""
    f = math.floor(show * R.get("fps"))
    while _progress(f, show, R) < _SYNC_AT:
        f += 1
    return f


def _readable(block: dict, R: Rules) -> bool:
    """R30: từ hiện sau cùng của block đậm ≥ 90 % trên hình trong ≥ 3 frame liền. Độ đậm
    = tiến độ hiện × (1 − tiến độ thoát tuyến tính qua exit_f frame từ out), như
    Subtitle.tsx; block chỉ được vẽ tới out·fps + exit_f."""
    fps, last, out, ex = R.get("fps"), _last(block), block["out"], block["exit_f"]
    run = 0
    for f in range(math.floor(last * fps), math.floor(out * fps + ex) + 1):
        q = min(1.0, max(0.0, (f - out * fps) / ex))
        run = run + 1 if _progress(f, last, R) * (1 - q) >= _SYNC_AT else 0
        if run >= _READ_F:
            return True
    return False


def _clear_at(block: dict, R: Rules) -> float:
    """Lúc sớm nhất thứ hiện sau (block sau, thẻ) được lên hình mà từ cuối của block vẫn
    đọc được: đậm ≥ 90 % từ frame f90 trong 3 frame rồi chuyển nhanh 2 f (R31, R32)."""
    return (_f90(_last(block), R) + _READ_F - 1 + _QUICK_EXIT_F) / R.get("fps")


def _with_exit(block: dict, out: float, exit_f: int) -> dict:
    return {**block, "out": _r(out), "exit_f": exit_f}


def _quick(block: dict, gate: float, R: Rules) -> dict:
    """R30: chuyển nhanh 2 f, tắt xong đúng ở `gate`."""
    return _with_exit(block, gate - _QUICK_EXIT_F / R.get("fps"), _QUICK_EXIT_F)


def _exit(block: dict, e_last: float, gate: float | None, R: Rules) -> dict:
    """R30: thoát thường 6 f ở min(e từ cuối + 0,22; gate − 0,22) khi từ cuối đọc được,
    không thì chuyển nhanh. `gate` = lúc phải tắt xong (None: block cuối video)."""
    if gate is None:
        return _with_exit(block, e_last + _HOLD_S, _EXIT_F)
    normal = _with_exit(block, min(e_last + _HOLD_S, gate - _YIELD_S), _EXIT_F)
    return normal if _readable(normal, R) else _quick(block, gate, R)


def _reshow(w: dict, new: float) -> dict:
    """Bản sao từ `w` hiện ở `new`; display_shift_s = độ dời so với mốc gốc (R31)."""
    orig = w["show"] - w.get("display_shift_s", 0.0)
    return {**w, "show": _r(new), "display_shift_s": _r(new - orig)}


def _map_words(block: dict, fn) -> dict:
    """Bản sao block, mỗi từ thay bằng fn(j, từ) — j là thứ tự trong top + hero + bottom."""
    out, j = dict(block), 0
    for line in ("top", "hero", "bottom"):
        out[line] = [fn(j + n, w) for n, w in enumerate(block[line])]
        j += len(block[line])
    return out


def _delay(block: dict, ons: list[float], t: float) -> dict:
    """R31: các từ của block sau (không đồng bộ) hiện trước `t` hiện muộn lại tới `t` —
    mỗi từ dời ≤ 0,15 s và hiện ≤ 0,10 s sau onset `ons[j]` của nó."""
    def later(j: int, w: dict) -> dict:
        orig = w["show"] - w.get("display_shift_s", 0.0)
        new = min(t, orig + _MAX_SHIFT_S, ons[j] + _MAX_LATE_S)
        return _reshow(w, new) if new > w["show"] else w
    return _map_words(block, later)


def _advance(block: dict, gate: float, R: Rules) -> dict:
    """R31: thứ hiện sau khoá theo cue ⇒ block (không đồng bộ) chuyển nhanh ở `gate` và các
    từ cuối hiện sớm lại tới mốc muộn nhất mà từ cuối vẫn đọc được — mỗi từ dời ≤ 0,15 s,
    không sớm hơn từ đầu của block (block trước đã tính lúc tắt theo mốc đó)."""
    fps, quick, head = R.get("fps"), _quick(block, gate, R), _first(block)
    # f90 phải ≤ frame cuối còn hiện đủ − 2; outCubic đạt 90 % sau reveal·(1 − 0,1^⅓) frame.
    k90 = R.get("text.reveal_f") * (1 - (1 - _SYNC_AT) ** (1 / 3))
    f_read = math.floor(quick["out"] * fps + 1e-6) - (_READ_F - 1)
    t = math.floor((f_read - k90) / fps * 1e4) / 1e4      # làm tròn xuống lưới 4 số lẻ của khoá

    def earlier(_j: int, w: dict) -> dict:
        orig = w["show"] - w.get("display_shift_s", 0.0)
        new = max(t, orig - _MAX_SHIFT_S, head)
        return _reshow(w, new) if new < w["show"] else w
    return _map_words(quick, earlier)


def _blocks(words: list[dict], edit: dict, plan: dict, steps: dict | None,
            R: Rules) -> tuple[list[dict], dict | None, list[str]]:
    """Mốc tắt, kiểu thoát và mốc hiện cuối của mọi block, lần lượt từ đầu video: thẻ
    không tiếng nhường block trước thẻ (R32), chọn thoát (R30), rồi dời mốc hiện khi từ
    cuối vẫn không đọc kịp (R31). Trả (blocks, steps, warnings)."""
    blocks = _block_lines(words, edit, plan, R)
    ons = [[words[k]["on"] for k in _indices(spec)] for spec in edit["blocks"]]
    card_synced = any(c["role"] == "card" for c in plan["cues"])
    warnings = []
    for i, spec in enumerate(edit["blocks"]):
        nxt = blocks[i + 1] if i + 1 < len(blocks) else None
        to_card = steps is not None and _first(blocks[i]) < steps["in"] and (
            nxt is None or _first(nxt) >= steps["in"])
        if to_card and not card_synced:
            steps = {**steps, "in": _r(max(steps["in"], _clear_at(blocks[i], R)))}
        gate = steps["in"] if to_card else None if nxt is None else _first(nxt)
        blk = _exit(blocks[i], words[max(_indices(spec))]["e"], gate, R)
        if gate is not None and not _readable(blk, R):
            if not to_card and not nxt["synced"]:
                blocks[i + 1] = _delay(nxt, ons[i + 1], _clear_at(blk, R))
                blk = _quick(blk, _first(blocks[i + 1]), R)
            elif not blk["synced"]:          # thứ hiện sau khoá theo cue: block đồng bộ, thẻ có tiếng
                blk = _advance(blk, gate, R)
        if not _readable(blk, R):
            warnings.append("LAST_WORD_TIGHT:" + blk["id"])
        blocks[i] = blk
    return blocks, steps, warnings


def _steps(words: list[dict], edit: dict, plan: dict, R: Rules) -> dict | None:
    steps = edit.get("steps")
    if not steps:
        return None
    fps, lead = R.get("fps"), R.get("text.lead_s")
    items = [{"label": it["label"], "show": _r(words[it["range"][0]]["on"] + _ITEM_DELAY_F / fps - lead)}
             for it in steps["items"]]
    card = next((c for c in plan["cues"] if c["role"] == "card"), None)
    t_in = ((card["frame"] - R.get("sfx.sync_frame.card")) / fps if card
            else items[0]["show"] - _STEPS_LEAD_S)
    last = steps["items"][-1]["range"][1] - 1
    return {"title": steps["title"], "in": _r(t_in), "out": _r(words[last]["e"] + _STEPS_HOLD_S),
            "items": items}


def _card_out_before_next_block(steps: dict, blocks: list[dict], R: Rules) -> dict:
    """R34: thẻ ra xong (8 f thoát của StepList) trước khi block đầu tiên sau thẻ hiện
    (bản sao của `steps`, out đã kẹp). Không còn block nào sau thẻ thì giữ nguyên."""
    later = [t for t in map(_first, blocks) if t >= steps["in"]]
    if not later:
        return steps
    return {**steps, "out": _r(min(steps["out"], min(later) - _CARD_EXIT_F / R.get("fps")))}


def _cta(words: list[dict], edit: dict, plan: dict, R: Rules) -> dict | None:
    cta = edit.get("cta")
    if not cta:
        return None
    cue = next((c for c in plan["cues"] if c["role"] == "cta"), None)
    if cue is not None and cue["mode"] == "pre":
        show = (cue["frame"] - R.get("sfx.sync_frame.cta_pill")) / R.get("fps")
    else:
        show = words[cta["range"][0]]["on"]
    return {"label": cta["label"], "keyword": cta["keyword"], "show": _r(show)}


def _shots(words: list[dict], edit: dict, plan: dict, R: Rules) -> list[dict]:
    fps, sync = R.get("fps"), R.get("sfx.sync_frame.cut")
    ok = [c for c in plan["candidates"] if c["decision"] == "OK" and c["role"] in ("cut", "section")]
    # Cue cắt ghi sau nên thắng cue chuyển đoạn khi cả hai neo cùng một từ cắt:
    # tiếng air là tiếng của chính cú cắt.
    snap = {c["anchor_word"]: c["cue"]["frame"] for c in sorted(ok, key=lambda c: c["role"] == "cut")}
    out = []
    for i, shot in enumerate(edit["shots"]):
        k = shot["cut_at_word"]
        # R24: shot 0 là khung mở, không phải cú cắt ⇒ t = 0 (on(từ 0) sẽ bắn kick giả).
        t = 0.0 if i == 0 else (snap[k] - sync) / fps if k in snap else words[k]["on"]
        out.append({"t": _r(t), "s0": shot["s0"], "s1": shot["s1"],
                    "x": shot.get("x", 0.0), "y": shot.get("y", 0.0)})
    return out


def _t_end(pauses: dict, R: Rules) -> float:
    """S27: đầu khoảng ngắt sau từ cuối + end.pad_s, không quá độ dài nguồn."""
    lwe = pauses["last_word_end"]
    p0 = next((p[0] for p in pauses["pauses"] if p[0] >= lwe - _TOL), lwe)
    return min(p0 + R.get("end.pad_s"), pauses["duration_s"])


def build_lock(words: list[dict], edit: dict, plan: dict, pauses: dict, R: Rules) -> dict:
    """Khoá hình theo Data Contracts (`safe` = safe_zone của Rules đã dựng khoá —
    Ruling R25 — để script.ts xuất SAFE; `warnings` = LAST_WORD_TIGHT:<id> của R31).
    `words` là words.json có `on`, `edit` là edit.json 1.1, `plan` là sfx_plan,
    `pauses` là pauses.json. Không sửa đầu vào."""
    fps = R.get("fps")
    t_end = _r(_t_end(pauses, R))
    hook = edit.get("hook")
    blocks, steps, warnings = _blocks(words, edit, plan, _steps(words, edit, plan, R), R)
    return {
        "fps": fps,
        "duration_f": int(round(t_end * fps)),
        "t_end": t_end,
        "hook": {"text": hook["text"], "color": hook["color"], **HOOK_TIMING} if hook else None,
        "blocks": blocks,
        "steps": _card_out_before_next_block(steps, blocks, R) if steps else None,
        "cta": _cta(words, edit, plan, R),
        "shots": _shots(words, edit, plan, R),
        "safe": dict(R.get("safe_zone")),
        "warnings": warnings,
    }


def write_script_ts(lock: dict, path) -> None:
    """Ghi src/data/script.ts từ khoá hình: FPS, DURATION_F, DURATION_S (= t_end),
    HOOK, BLOCKS, STEPS, SHOTS, CTA, SAFE. Không có bảng SFX — tiếng trộn bằng
    ffmpeg (S25). Cùng khoá ⇒ cùng từng byte."""
    def j(v):
        return json.dumps(v, ensure_ascii=False, indent=1)

    text = TS_HEAD + TS_TYPES + (
        "\n"
        f"export const FPS = {lock['fps']};\n"
        f"export const DURATION_F = {lock['duration_f']};\n"
        f"export const DURATION_S = {j(lock['t_end'])};\n"
        f"export const HOOK: Hook | null = {j(lock['hook'])};\n"
        f"export const BLOCKS: Block[] = {j(lock['blocks'])};\n"
        f"export const STEPS: Steps | null = {j(lock['steps'])};\n"
        f"export const SHOTS: Shot[] = {j(lock['shots'])};\n"
        f"export const CTA: Cta | null = {j(lock['cta'])};\n"
        f"export const SAFE: Safe = {j(lock['safe'])};\n"
    )
    Path(path).write_bytes(text.encode("utf-8"))
