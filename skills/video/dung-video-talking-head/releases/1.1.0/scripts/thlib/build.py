"""thlib.build — stage BUILD (§5.7 bước 7–9; S18, S25, S29): từ words/pauses/edit (INTAKE +
PLAN đã xong) tới ba bản xuất, out/QA.json và out/EDITOR-REPORT.md.

Thứ tự cổng (Ruling R27), dừng ở cổng hỏng đầu tiên:
  planner → picture_lock (+ src/data/script.ts) → text_safe → stem_bed → lint_pre_mux
  (L1–L10, L12–L14) → mix → render (hình, --muted) → mux → lint_post_mux (L11) → report.

- planner chạy đúng như lint_sfx.py (JSON đọc lại từ đĩa, overrides.json không có = [],
  vo = audio.decode_mono(public/vo-clean.wav)) để lint ở process khác ra cùng sha (S21,
  L10); out/sfx_plan.json ghi đúng chuỗi lint.plan_json mà plan_sha256 băm.
- lint chấm đúng những gì đã nằm trên đĩa (sfx_plan.json, sfx_stem.wav, bgm_bed.wav,
  picture_lock.json) với expected_sha = sha output planner (L10 không bao giờ BỎ QUA); mix
  trộn đúng các file đó. out/sfx_lint.json cùng dạng lint_sfx.py ghi (sau mux thêm L11).
- chưa chọn nhạc nền (mix.select_bgm → None, trước gate 9): không có bed, bgm_bed.wav của
  lần trước bị xoá; mix.wav và mix-nobgm.wav cùng tiếng, cả hai vẫn được ghi.
- mix.wav / mix-nobgm.wav: vòng R35 dùng chung với social (mix.loudnorm_encoded) — loudnorm 2
  lượt tuyến tính về loudness.final_lufs (limiter true-peak, trần đầu TP đích − 0,5 dB), mã hoá
  AAC thử đúng như mux.py (out/_raw-*.m4a, xoá sau), TP bản thử còn vượt loudness.tp_dbtp thì hạ
  trần rồi làm lại, tối đa loud.TP_TRIES lần; mix thô ghi float (không cắt đỉnh) ở out/_raw-*.wav
  rồi xoá. Bản ghi vòng (số lần, trần cuối) ghi ở out/mix_loudness.json — mux.py chép vào QA.json
  của final / final-nobgm. Cổng 'loudness mix' (S18): I lệch quá tol_lu, TP của WAV vượt đích hay
  bản AAC thử vẫn vượt sau lần cuối ⇒ cổng mix FAIL, trước khi render.
- cảnh báo của khoá hình (LAST_WORD_TIGHT, R31) không dừng BUILD — make_report ghi ra.
- text_safe, render, mux, report là script của release, chạy ở process con. Script thoát mã 2
  (check_text_safe: thiếu node_modules/font, lock hỏng, Remotion lỗi) hay lỗi chương trình ⇒
  kết quả mang tool_error = True (owner dev); mã 1 của text_safe là chữ tràn thật (B3).
- quá thời gian (R47): render_video.py có trần proc.RENDER_TIMEOUT_S ở đây (thlib.proc giết cả
  cây); script thoát mã proc.TIMEOUT_EXIT (still/render bên trong quá hạn) cũng vậy ⇒
  subprocess.TimeoutExpired đi thẳng qua `run` (không phải cổng hỏng) để stage.py BLOCK transient.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import traceback
from functools import partial
from pathlib import Path

import numpy as np
from scipy.io import wavfile

from . import audio as A
from . import lint, loud, mix, paths, picture, planner, proc, sfxlib
from .rules import Rules

SCRIPTS = Path(__file__).resolve().parents[1]    # releases/<ver>/scripts
_LOG_TAIL = 20                                   # số dòng cuối của log script con in ra khi hỏng
_TOOL_EXIT = 2                                   # script của release thoát mã 2 = lỗi công cụ (B3)
SCRIPT_TIMEOUT_S = {"render_video.py": proc.RENDER_TIMEOUT_S}   # R47; text-safe: từng still tự có trần


class BuildError(Exception):
    """Một cổng BUILD không đạt (lint FAIL, script của release thoát mã ≠ 0)."""


class ToolError(BuildError):
    """Cổng hỏng vì công cụ, không vì nội dung: script của release thoát mã 2 (vd
    check_text_safe thiếu node_modules/font, Remotion lỗi) — lỗi skill/máy, owner dev (B3)."""


def _read(path: Path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _write_json(path: Path, obj) -> Path:
    """JSON thụt lề 2 như lint_sfx.py ghi sfx_lint.json (cùng nội dung ⇒ cùng byte)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def _script(project: Path, name: str) -> str:
    """Chạy script `name` của release với đối số <project> ở process con; trả log. Mã thoát
    ≠ 0 ⇒ BuildError kèm các dòng cuối của log (mã 2 ⇒ ToolError); quá SCRIPT_TIMEOUT_S hoặc mã
    proc.TIMEOUT_EXIT ⇒ subprocess.TimeoutExpired (R47)."""
    run = proc.run([sys.executable, str(SCRIPTS / name), str(project)], capture_output=True,
                   text=True, encoding="utf-8", errors="replace",
                   env={**os.environ, "PYTHONIOENCODING": "utf-8"}, timeout=SCRIPT_TIMEOUT_S.get(name))
    log = (run.stdout + run.stderr).strip()
    if run.returncode != 0:
        tail = "\n".join(log.splitlines()[-_LOG_TAIL:])
        if run.returncode == proc.TIMEOUT_EXIT:
            raise subprocess.TimeoutExpired([name], None, output=tail)
        err = ToolError if run.returncode == _TOOL_EXIT else BuildError
        raise err("%s thoát mã %d:\n%s" % (name, run.returncode, tail))
    return log


def _last_line(log: str) -> str:
    return log.splitlines()[-1] if log else ""


def _require_ok(results: list[dict]) -> None:
    """Có mã lint FAIL ⇒ BuildError liệt kê từng mã (kèm frame vi phạm đầu tiên)."""
    bad = ["%s FAIL%s: %s" % (r["code"], "" if r["frame"] is None else " f%d" % r["frame"], r["msg"])
           for r in results if not r["ok"]]
    if bad:
        raise BuildError("; ".join(bad))


def planner_inputs(project: Path, R: Rules) -> dict:
    """Đầu vào planner, đọc đúng như lint_sfx.py: words/pauses/edit.json, overrides.json
    (không có = []), manifest + tín hiệu SFX của release, vo = decode_mono(vo-clean.wav)."""
    overrides = project / "overrides.json"
    manifest = sfxlib.load_manifest(R.version)
    return {
        "words": _read(project / "words.json"),
        "pauses": _read(project / "pauses.json"),
        "edit": _read(project / "edit.json"),
        "overrides": _read(overrides) if overrides.exists() else [],
        "manifest": manifest,
        "signals": {k: sfxlib.load_signal(R.version, k) for k in manifest["files"]},
        "vo": A.decode_mono(project / "public" / "vo-clean.wav"),
    }


def _layers(project: Path):
    """(stem mono, bed [n, 2] | None) đọc lại từ đĩa — lint và mix dùng đúng file đã ghi."""
    bed = project / "public" / "bgm_bed.wav"
    return A.decode_mono(project / "public" / "sfx_stem.wav"), (A.decode(bed) if bed.exists() else None)


# ------------------------------------------------ các cổng
# Mỗi cổng nhận trạng thái s (dict), trả (khoá mới cho s, file đã ghi, ghi chú in ra).


def _planner(s: dict):
    inp = planner_inputs(s["project"], s["R"])
    plan, cues_audio = planner.plan(inp["words"], inp["pauses"], inp["edit"], inp["overrides"],
                                    inp["manifest"], inp["signals"], inp["vo"], s["R"], s["preset"])
    path = s["project"] / "out" / "sfx_plan.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(lint.plan_json(plan).encode("utf-8"))
    note = "%d cue OK / %d ứng viên, ngân sách %d" % (len(plan["cues"]), len(plan["candidates"]),
                                                      plan["budget"])
    return {**inp, "plan": plan, "cues_audio": cues_audio, "sha": lint.plan_sha256(plan)}, [path], note


def _picture_lock(s: dict):
    lock = picture.build_lock(s["words"], s["edit"], s["plan"], s["pauses"], s["R"])
    ts = s["project"] / "src" / "data" / "script.ts"
    files = [_write_json(s["project"] / "picture_lock.json", lock), ts]
    picture.write_script_ts(lock, ts)
    note = "%d f, %d block; cảnh báo: %s" % (lock["duration_f"], len(lock["blocks"]),
                                             ", ".join(lock["warnings"]) or "không có")
    return {"lock": lock}, files, note


def _text_safe(s: dict):
    log = _script(s["project"], "check_text_safe.py")
    return {}, [s["project"] / "out" / "safe" / "text_safe.json"], _last_line(log)


def _stem_bed(s: dict):
    project, R, vo = s["project"], s["R"], s["vo"]
    stem, bed = project / "public" / "sfx_stem.wav", project / "public" / "bgm_bed.wav"
    A.write_wav(stem, mix.render_stem(s["cues_audio"], len(vo)))
    key = mix.select_bgm(R.version, _read(project / "meta.json")["video"])
    if key is None:
        bed.unlink(missing_ok=True)
        return {}, [stem], "không có nhạc nền (chưa chọn bài)"
    rel = paths.release_dir(R.version)
    track = A.decode(rel / _read(rel / "bgm_manifest.json")["tracks"][key]["path"])
    A.write_wav(bed, mix.bgm_bed(track, vo, s["lock"]["t_end"], R))
    return {}, [stem, bed], "nhạc nền " + key


def _lint_pre_mux(s: dict):
    project = s["project"]
    stem, bed = _layers(project)
    results = lint.run_pre_mux(_read(project / "out" / "sfx_plan.json"), stem, s["vo"], bed, s["pauses"],
                               _read(project / "picture_lock.json"), s["manifest"], s["R"], s["preset"],
                               expected_sha=s["sha"])
    path = _write_json(project / "out" / "sfx_lint.json", results)
    _require_ok(results)
    warns = [r["msg"].split("| WARN ", 1)[1] for r in results if "| WARN " in r["msg"]]
    note = "%d mã PASS" % len(results) + (" — WARN " + "; ".join(warns) if warns else "")
    return {"pre": results}, [path], note


def _aac_trial(wav: Path, trial: Path) -> Path:
    """encode của vòng R35 ở cổng mix: mã hoá AAC `wav` đúng như mux.py (loud.AAC_ARGS) ra bản
    thử `trial` — TP bản thử = TP bản xuất mux ghép từ `wav`."""
    loud.ffmpeg(["-y", "-i", str(wav), *loud.AAC_ARGS, str(trial)])
    return trial


def _mix(s: dict):
    project, R = s["project"], s["R"]
    L = R.get("loudness")
    vo = A.decode(project / "public" / "vo-clean.wav")
    stem, bed = _layers(project)
    files, notes, loops = [], [], {}
    for name, layer in (("mix.wav", bed), ("mix-nobgm.wav", None)):
        raw, dst = project / "out" / ("_raw-" + name), project / "public" / name
        trial = raw.with_suffix(".m4a")
        wavfile.write(str(raw), A.SR, mix.mixdown(vo, stem, layer, s["lock"]["t_end"], R).astype(np.float32))
        try:
            got = mix.loudnorm_encoded(raw, dst, L["final_lufs"], L["tp_dbtp"],
                                       partial(_aac_trial, trial=trial))
        except mix.TruePeakError as exc:           # bản AAC thử vẫn vượt sau lần cuối
            got = exc.record
        finally:
            raw.unlink(missing_ok=True)
            trial.unlink(missing_ok=True)
        note = "%s %.2f LUFS / TP %.2f, AAC thử TP %.2f (trần %.2f dBTP, lần %d)" % (
            name, got["lufs"], got["tp_dbtp"], got["encoded_tp_dbtp"], got["ceiling_dbtp"], got["attempts"])
        if (abs(got["lufs"] - L["final_lufs"]) > L["tol_lu"]
                or max(got["tp_dbtp"], got["encoded_tp_dbtp"]) > L["tp_dbtp"]):
            raise BuildError("%s — cần %g ±%g LUFS, TP ≤ %g (S18)" % (note, L["final_lufs"], L["tol_lu"],
                                                                      L["tp_dbtp"]))
        files.append(dst)
        notes.append(note)
        loops[name] = {"attempts": got["attempts"], "ceiling_dbtp": got["ceiling_dbtp"]}
    files.append(_write_json(project / "out" / "mix_loudness.json", loops))
    return {}, files, "; ".join(notes)


def _render(s: dict):
    log = _script(s["project"], "render_video.py")
    return {}, [s["project"] / "out" / "_video.mp4"], _last_line(log)


def _mux(s: dict):
    log = _script(s["project"], "mux.py")
    out = s["project"] / "out"
    return {}, [out / "final.mp4", out / "final-nobgm.mp4", out / "final-social.mp4", out / "QA.json"], \
        _last_line(log)


def _lint_post_mux(s: dict):
    post = lint.run_post_mux(s["project"], s["R"])
    path = _write_json(s["project"] / "out" / "sfx_lint.json", s["pre"] + post)
    _require_ok(post)
    return {}, [path], post[0]["msg"]


def _report(s: dict):
    log = _script(s["project"], "make_report.py")
    return {}, [s["project"] / "out" / "EDITOR-REPORT.md"], _last_line(log)


_STEPS = (("planner", _planner), ("picture_lock", _picture_lock), ("text_safe", _text_safe),
          ("stem_bed", _stem_bed), ("lint_pre_mux", _lint_pre_mux), ("mix", _mix), ("render", _render),
          ("mux", _mux), ("lint_post_mux", _lint_post_mux), ("report", _report))
GATES = tuple(gate for gate, _ in _STEPS)


def _result(failed_gate: str | None, written: list[Path], tool_error: bool = False) -> dict:
    return {"ok": failed_gate is None, "failed_gate": failed_gate, "tool_error": tool_error,
            "artifacts": [p.as_posix() for p in dict.fromkeys(written)]}


def run(project: Path, R: Rules, preset: str) -> dict:
    """BUILD dự án `project` với bộ luật R và preset. In một dòng mỗi cổng; dừng ở cổng hỏng
    đầu tiên. Trả {"ok", "failed_gate": tên cổng | None, "tool_error": cổng hỏng vì công cụ
    (ToolError hay lỗi chương trình — owner dev, B3) chứ không vì nội dung, "artifacts": file
    các cổng đã đạt ghi ra, theo thứ tự ghi (đường dẫn POSIX)}."""
    s = {"project": Path(project), "R": R, "preset": preset}
    written: list[Path] = []
    for gate, step in _STEPS:
        try:
            new, files, note = step(s)
        except subprocess.TimeoutExpired:            # R47: treo, không phải cổng hỏng — stage.py BLOCK transient
            print("BUILD %-13s QUÁ THỜI GIAN" % gate)
            raise
        except BuildError as exc:
            print("BUILD %-13s FAIL — %s" % (gate, exc))
            return _result(gate, written, isinstance(exc, ToolError))
        except Exception:      # lỗi chương trình (ffmpeg, đầu vào hỏng…): in đủ traceback cho dev
            print("BUILD %-13s LỖI — %s" % (gate, traceback.format_exc().rstrip()))
            return _result(gate, written, True)
        s = {**s, **new}
        written += files
        print("BUILD %-13s PASS — %s" % (gate, note))
    return _result(None, written)
