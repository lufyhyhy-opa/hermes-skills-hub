# tests/test_stage.py — stage.py (lối vào của mỗi card), check_prep.py, thân card (Task 14).
# VID_ROOT luôn trỏ vào tmp (fixture autouse); không test nào gọi Hermes CLI thật — runner của
# thlib.kanban bị thay bằng hàm giả. Test chậm cuối file chạy stage.py thật (process con) qua
# INTAKE → PLAN → PLAN --check → BUILD → VERIFY trên video 02 (whisper + render thật).
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pytest

import check_prep
import stage
from thlib import kanban, manifest, mapping, paths, scripts_v3, state

FIXTURES = Path(__file__).parent / "fixtures"
STAGE_PY = paths.release_dir("1.1.0") / "scripts" / "stage.py"
SOURCE_V2 = Path("D:/MMO/Van Minh AI/Vid Heygen/2/2.mp4")      # nguồn thật, chỉ đọc
CTA_V2 = {"range": [147, 162], "label": "Bình luận", "keyword": "5 TÀI SẢN"}


@pytest.fixture(autouse=True)
def _sandbox(tmp_path, monkeypatch):
    """VID_ROOT tạm, DOCS_ROOT = bản sao 3 file kịch bản, không có card Hermes nào."""
    monkeypatch.setattr(paths, "VID_ROOT", tmp_path / "vid")
    monkeypatch.setattr(paths, "DOCS_ROOT", FIXTURES / "scripts")
    for var in ("HERMES_KANBAN_TASK", "HERMES_KANBAN_BOARD", "HERMES_KANBAN_RUN_ID",
                "HERMES_PROFILE", "HERMES_DELEGATED_CHILD_CONTEXT"):
        monkeypatch.delenv(var, raising=False)

    def no_cli(argv):
        raise AssertionError("test không được gọi Hermes CLI thật")
    monkeypatch.setattr(kanban, "_run", no_cli)


def _body(stage_name="PLAN", video="2", ver="1.1.0", preset="standard", attempt=1, batch="b99"):
    return (f"VIDEO: {video}   STAGE: {stage_name}   RULES: dung-video-talking-head@{ver}\n"
            f"PRESET: {preset}   ATTEMPT: a{attempt}\nBATCH: {batch}")


def _card(tmp_path, text, name="card.txt"):
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return str(path)


def _protocol(out):
    """4 dòng cuối stdout → dict; kiểm đúng khuôn giao thức."""
    lines = out.rstrip("\n").splitlines()[-4:]
    keys = ["RESULT", "NEXT", "SUMMARY", "METADATA"]
    assert [ln.split(":", 1)[0] for ln in lines] == keys, lines
    got = {k: ln.split(": ", 1)[1] for k, ln in zip(keys, lines)}
    assert got["RESULT"] in ("PASS", "FAIL", "BLOCK")
    assert got["NEXT"].strip() and got["SUMMARY"].strip()
    assert not re.search(r"\d", got["SUMMARY"]), got["SUMMARY"]       # SUMMARY không có số
    got["METADATA"] = json.loads(got["METADATA"])
    return got


# ------------------------------------------------------------------ thân card


def test_parse_body_video_and_prep_cards():
    assert kanban.parse_body(_body("BUILD", "7")) == {
        "videos": [7], "stage": "BUILD", "prep_k": None, "ver": "1.1.0", "preset": "standard",
        "attempt": 1, "batch": "b99"}
    got = kanban.parse_body(_body("PREP-2", "16,21,27", attempt=3) + "\n")
    assert (got["videos"], got["stage"], got["prep_k"], got["attempt"]) == ([16, 21, 27], "PREP", 2, 3)
    body = kanban.format_body([16, 21], "PREP-1", "1.1.0", "calm", 2, "b01")
    assert kanban.parse_body(body)["preset"] == "calm"
    assert kanban.parse_body(body.replace("\n", "\r\n"))["videos"] == [16, 21]


@pytest.mark.parametrize("text", [
    "",
    _body().replace("\nBATCH: b99", ""),                                   # thiếu dòng
    _body() + "\nGHI CHÚ: làm nhanh",                                      # thừa dòng
    _body().replace("dung-video-talking-head", "dung-video-khac"),         # sai skill
    _body("RENDER"),                                                       # stage lạ
    _body("PLAN", "7,8"),                                                  # nhiều video ngoài PREP
    _body(attempt=0),
    _body(ver="1.1"),
    "VIDEO: 7 STAGE: PLAN\nPRESET: standard ATTEMPT: a1\nBATCH: b99",
])
def test_parse_body_rejects_off_template(text):
    with pytest.raises(kanban.CardError):
        kanban.parse_body(text)


# ------------------------------------------------------------------ khoá + giao thức


def test_second_lock_acquire_fails_fast(tmp_path):
    lock = tmp_path / "7" / ".stage.lock"
    with stage.file_lock(lock):
        t0 = time.monotonic()
        with pytest.raises(stage.LockBusy):
            with stage.file_lock(lock):
                pass
        assert time.monotonic() - t0 < 1.0
    with stage.file_lock(lock):                             # nhả rồi thì lấy lại được
        pass


@pytest.mark.parametrize("stage_name, kind", [("PLAN", "transient"), ("BUILD", "transient")])
def test_stage_blocks_when_video_is_locked(tmp_path, capsys, stage_name, kind):
    """Khoá video bận ⇒ BLOCK transient ngay, mọi stage như nhau (R43: không còn card goal)."""
    card = _card(tmp_path, _body(stage_name, "2"))
    with stage.file_lock(paths.VID_ROOT / "2" / ".stage.lock"):
        t0 = time.monotonic()
        rc = stage.main([stage_name, "--card-file", card])
        assert time.monotonic() - t0 < 5.0
    got = _protocol(capsys.readouterr().out)
    assert rc == 2 and got["RESULT"] == "BLOCK"
    assert got["METADATA"]["block"] == kind and got["METADATA"]["cause"] == "transient"
    assert got["METADATA"]["video"] == 2 and f'kind="{kind}"' in got["NEXT"]


def test_off_template_card_blocks_with_protocol(tmp_path, capsys):
    rc = stage.main(["PLAN", "--card-file", _card(tmp_path, "làm video 2 giúp mình")])
    got = _protocol(capsys.readouterr().out)
    assert rc == 2 and got["RESULT"] == "BLOCK" and got["METADATA"]["block"] == "needs_input"
    assert "card ngoài mẫu" in got["NEXT"] and 'kind="needs_input"' in got["NEXT"]


def test_card_for_other_release_blocks(tmp_path, capsys):
    assert stage.main(["PLAN", "--card-file", _card(tmp_path, _body("PLAN", "2", ver="1.1.1"))]) == 2
    assert _protocol(capsys.readouterr().out)["METADATA"]["block"] == "needs_input"


def test_wrong_stage_argument_fails_with_the_cards_own_command(tmp_path, capsys):
    """Gõ sai tên stage là lỗi của lệnh, không phải của card ⇒ FAIL (không BLOCK dính), NEXT in đúng lệnh
    của stage ghi trên card, giữ cách nhận card (--card-file/--task)."""
    card = _card(tmp_path, _body("BUILD", "2"))
    assert stage.main(["PLAN", "--card-file", card]) == 1
    got = _protocol(capsys.readouterr().out)
    assert got["RESULT"] == "FAIL" and "Không complete card." in got["NEXT"]
    assert 'stage.py" BUILD --card-file' in got["NEXT"] and "STAGE BUILD" in got["NEXT"]


def test_prep_k_and_lowercase_stage_names_are_accepted(capsys):
    """Card `STAGE: PREP-1` ⇒ stage PREP: worker gõ `PREP-1` hay `prep` không thành lỗi cú pháp."""
    for word in ("PREP-1", "prep"):
        assert stage.main([word, "--task", "t_bad"]) == 1
        got = _protocol(capsys.readouterr().out)
        assert "sai cú pháp" not in got["NEXT"] and 'stage.py" PREP ' in got["NEXT"], got["NEXT"]


def test_syntax_error_keeps_the_given_task_id(capsys):
    assert stage.main(["PREPARE", "--task", "t_0000abcd"]) == 1
    got = _protocol(capsys.readouterr().out)
    assert got["RESULT"] == "FAIL" and "--task t_0000abcd" in got["NEXT"]
    assert 'stage.py" STAGE --task t_0000abcd' in got["NEXT"] and "PREP-1" in got["NEXT"]


HERMES_BLOCK_KINDS = {"dependency", "needs_input", "capability", "transient"}   # kanban_db.VALID_BLOCK_KINDS


def test_no_goal_mode_stages(rules_110):
    """R43 (MF-4): không stage nào chạy goal mode — budgets goal_turns = 0 mọi stage (make_cards
    không thêm --goal) và GOAL_STAGES rỗng (C3 giữ khung đổi kind nếu sau này bật lại)."""
    goal = {s for s in stage.STAGE_NAMES if rules_110.get(f"budgets.{s}.goal_turns") > 0}
    assert set(stage.GOAL_STAGES) == goal == set()


@pytest.mark.parametrize("stage_name", ["PREP", "INTAKE", "PLAN", "BUILD", "VERIFY"])
@pytest.mark.parametrize("cause", ["transient", "needs_input", "capability"])
def test_block_kind_is_hermes_valid(stage_name, cause):
    """C3 + R43: kind in ra luôn là loại Hermes nhận và giữ nguyên nguyên nhân ở mọi stage."""
    kind = stage.hermes_kind(stage_name, cause)
    assert kind in HERMES_BLOCK_KINDS and kind == cause


def test_plan_program_error_blocks_capability(tmp_path, v2_intaken, monkeypatch, capsys):
    """R43: traceback trong PLAN ⇒ kind capability (dev), như mọi stage."""
    def crash(project):
        raise RuntimeError("propose_edit hỏng")
    monkeypatch.setattr(stage.propose_edit, "run", crash)
    assert stage.main(["PLAN", "--card-file", _card(tmp_path, _body("PLAN", "2"))]) == 2
    got = _protocol(capsys.readouterr().out)
    assert got["METADATA"]["block"] == "capability" and got["METADATA"]["cause"] == "capability"
    assert 'kind="capability"' in got["NEXT"] and 'reason="capability:' in got["NEXT"]


def test_next_gates_kanban_complete_on_result(tmp_path, v2_intaken, monkeypatch, capsys):
    """R43/FS-5: chỉ NEXT của PASS cuối stage dặn kanban_complete — summary = dòng SUMMARY (PREP/PLAN:
    dòng "ĐẠT: …" + "RESULT: PASS"), metadata = JSON dòng METADATA; PASS giữa chừng dặn chưa complete;
    FAIL/BLOCK dặn không complete."""
    card = _card(tmp_path, _body("PLAN", "2"))

    def run(*argv):
        stage.main(list(argv))
        return _protocol(capsys.readouterr().out)

    got = run("PLAN", "--card-file", card)                                  # PASS giữa chừng
    assert got["RESULT"] == "PASS" and "kanban_complete" not in got["NEXT"] and "Chưa complete card." in got["NEXT"]
    got = run("PLAN", "--check", "--card-file", card)                       # FAIL: chưa có edit.json
    assert got["RESULT"] == "FAIL" and "Không complete card." in got["NEXT"] and "kanban_complete" not in got["NEXT"]
    shutil.copy2(FIXTURES / "v2" / "edit_v11.json", v2_intaken / "edit.json")
    got = run("PLAN", "--check", "--card-file", card)                       # PASS cuối stage
    assert got["RESULT"] == "PASS"
    for needle in ("tool kanban_complete", 'dòng "ĐẠT: …"', 'dòng "RESULT: PASS"', "metadata = JSON của dòng METADATA"):
        assert needle in got["NEXT"], needle

    monkeypatch.setattr(stage.build, "run", lambda project, R, preset: {
        "ok": True, "failed_gate": None, "artifacts": []})
    build = _card(tmp_path, _body("BUILD", "2"), "build.txt")
    got = run("BUILD", "--card-file", build)
    assert got["RESULT"] == "PASS"
    for needle in ("tool kanban_complete", "summary = dòng SUMMARY", "metadata = JSON của dòng METADATA"):
        assert needle in got["NEXT"], needle
    with stage.file_lock(paths.VID_ROOT / "2" / ".stage.lock"):
        got = run("BUILD", "--card-file", build)                            # BLOCK
    assert got["RESULT"] == "BLOCK" and "Không complete card." in got["NEXT"] and "kanban_complete" not in got["NEXT"]


@pytest.mark.parametrize("argv, env_task", [(["PLAN", "--task", "t_00000009"], None), (["PLAN"], "t_00000009")])
def test_card_body_read_from_kanban_show(tmp_path, monkeypatch, capsys, argv, env_task):
    """R42: id card lấy từ --task (worker) hoặc $HERMES_KANBAN_TASK (test/chạy tay)."""
    calls = []

    def fake(argv):
        calls.append(argv)
        task = {"task": {"id": "t_00000009", "body": "không phải card con trỏ"}, "parents": []}
        return type("P", (), {"returncode": 0, "stderr": "",
                              "stdout": "⚠ gateway banner\n  Run `hermes gateway restart`.\n"
                                        + json.dumps(task)})()
    monkeypatch.setattr(kanban, "_run", fake)
    if env_task:
        monkeypatch.setenv("HERMES_KANBAN_TASK", env_task)
    monkeypatch.setenv("HERMES_KANBAN_BOARD", "vm-heygen-b99")
    assert stage.main(argv) == 2
    assert calls[0][2:] == ["--board", "vm-heygen-b99", "show", "t_00000009", "--json"]
    assert _protocol(capsys.readouterr().out)["METADATA"]["block"] == "needs_input"


BANNER = ("⚠ A previous `hermes update` pulled new code but did not restart running gateways.\n"
          "  Gateways may still be serving pre-update modules (mixed sys.modules).\n"
          "  Run `hermes update` or `hermes gateway restart`.\n")


def _fake_show(shows):
    """kanban._run giả: `show <id>` trả shows[id]; id không có ⇒ đúng lỗi Hermes thật (rc 1, banner +
    "no such task: <id>" ở stderr — _cmd_show)."""
    def fake(argv):
        tid = argv[argv.index("show") + 1]
        if tid not in shows:
            return type("P", (), {"returncode": 1, "stdout": "", "stderr": BANNER + f"no such task: {tid}\n"})()
        return type("P", (), {"returncode": 0, "stderr": "", "stdout": json.dumps(shows[tid])})()
    return fake


def _wrong_task_failed(out, stage_args):
    """Id sai ⇒ FAIL (không BLOCK, không kanban_block — tool đó luôn chặn card thật của worker) kèm
    đúng lệnh chạy lại như khi thiếu id."""
    got = _protocol(out)
    assert got["RESULT"] == "FAIL" and "kanban_block" not in got["NEXT"], got
    assert (f'chạy lại: python "{STAGE_PY.as_posix()}" {stage_args} --task <id trong câu "work kanban task'
            in got["NEXT"]), got["NEXT"]
    return got


@pytest.mark.parametrize("bad", ["t_9", "t_DEADBEEF", "t_deadbeef0", "APPROVE-PREP-1", "<id>"])
def test_malformed_task_id_fails_without_calling_hermes(capsys, bad):
    """hermes-semantics-2: id không đúng khuôn Hermes (t_ + 8 chữ hex thường) ⇒ FAIL, không hỏi CLI
    (_sandbox cấm gọi CLI thật)."""
    assert stage.main(["BUILD", "--task", bad]) == 1
    _wrong_task_failed(capsys.readouterr().out, "BUILD")


def test_unknown_task_id_fails_instead_of_blocking(monkeypatch, capsys):
    """hermes-semantics-2 / consistency-6: `show` báo "no such task" (gõ nhầm một ký tự) ⇒ FAIL kèm
    lệnh chạy lại; banner "⚠ … hermes update" của CLI không lọt vào output."""
    monkeypatch.setattr(kanban, "_run", _fake_show({}))
    assert stage.main(["PLAN", "--check", "--task", "t_deadbeef"]) == 1
    out = capsys.readouterr().out
    got = _wrong_task_failed(out, "PLAN --check")
    assert "t_deadbeef" in got["NEXT"] and "hermes update" not in out


@pytest.mark.parametrize("runs, rc", [
    ([{"id": 5, "profile": "opa-editor", "ended_at": 1757500000}], 1),     # card cha đã xong: không run mở
    ([], 1),                                                                # card chưa ai nhận
    ([{"id": 6, "profile": "opa-verifier", "ended_at": None}], 1),          # run mở của profile khác
    ([{"id": 7, "profile": "opa-editor", "ended_at": None}], 0),            # đúng card của worker này
])
def test_task_id_without_this_workers_open_run_fails(v2_intaken, monkeypatch, capsys, runs, rc):
    """hermes-semantics-2: trong lệnh terminal của worker (HERMES_DELEGATED_CHILD_CONTEXT=1) card phải
    có run đang mở của đúng $HERMES_PROFILE — id của card cha (in trong ngữ cảnh worker) hay card khác
    ⇒ FAIL, không đi tiếp tới BLOCK "card ngoài mẫu" và không ghi STATE.md với run "0"."""
    shows = {"t_0a0a0a0a": {"task": {"id": "t_0a0a0a0a", "status": "running", "body": _body("PLAN", "2")},
                            "parents": [], "runs": runs}}
    monkeypatch.setattr(kanban, "_run", _fake_show(shows))
    monkeypatch.setenv("HERMES_DELEGATED_CHILD_CONTEXT", "1")
    monkeypatch.setenv("HERMES_PROFILE", "opa-editor")
    rows = len(state.read_state(v2_intaken))
    assert stage.main(["PLAN", "--task", "t_0a0a0a0a"]) == rc
    out = capsys.readouterr().out
    if rc:
        _wrong_task_failed(out, "PLAN")
        assert len(state.read_state(v2_intaken)) == rows
    else:
        assert state.read_state(v2_intaken)[-1]["run"] == "7"


@pytest.mark.parametrize("argv, rerun", [(["BUILD"], "BUILD"), (["PLAN", "--check"], "PLAN --check")])
def test_no_task_id_fails_with_rerun_command(capsys, argv, rerun):
    """R42: không --task, không $HERMES_KANBAN_TASK, không --card-file ⇒ FAIL (không BLOCK), NEXT là
    lệnh chạy lại kèm --task lấy từ câu "work kanban task …"; không hỏi Hermes (không `kanban list`)."""
    assert stage.main(argv) == 1
    got = _protocol(capsys.readouterr().out)
    assert got["RESULT"] == "FAIL"
    assert f'chạy lại: python "{STAGE_PY.as_posix()}" {rerun} --task <id trong câu "work kanban task' in got["NEXT"]


_CHILD_RUNNER = """
import json, runpy, sys
sys.path.insert(0, {scripts!r})
from thlib import kanban
shows = json.load(open({shows!r}, encoding="utf-8"))
def fake(argv):
    with open({log!r}, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(argv[1:]) + "\\n")
    if "show" not in argv:
        return type("P", (), {{"returncode": 1, "stdout": "", "stderr": "delegate_task child contexts cannot mutate"}})()
    return type("P", (), {{"returncode": 0, "stderr": "", "stdout": json.dumps(shows[argv[argv.index("show") + 1]])}})()
kanban._run = fake
sys.argv = [{stage_py!r}, *sys.argv[1:]]
runpy.run_path({stage_py!r}, run_name="__main__")
"""


def _child_env(root):
    """Env của lệnh terminal trong worker Hermes (delegation_context.scrub_kanban_env): mất TASK,
    RUN_ID, CLAIM_LOCK, GOAL_*; có HERMES_DELEGATED_CHILD_CONTEXT=1; board/workspace/profile giữ."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("HERMES_KANBAN_")}
    env.update(HERMES_DELEGATED_CHILD_CONTEXT="1", HERMES_KANBAN_BOARD="vm-heygen-b99",
               HERMES_KANBAN_WORKSPACE=str(root / "2"), HERMES_PROFILE="opa-editor",
               TH_VID_ROOT=str(root), PYTHONIOENCODING="utf-8")
    return env


def test_worker_child_env_uses_task_flag_and_keys_plan_rounds_by_task(tmp_path, v2_intaken):
    """R42 (MF-1): lệnh terminal của worker không có $HERMES_KANBAN_TASK/RUN_ID ⇒ stage.py đọc card
    bằng --task (kanban show), run = run chưa kết thúc trong show, NEXT chép lại --task; vòng FAIL
    của PLAN tính theo id card nên card a2 không thừa hưởng vòng của a1."""
    shows = {"t_a2a2a2a2": {"task": {"id": "t_a2a2a2a2", "body": _body("PLAN", "2", attempt=2)}, "parents": [],
                      "runs": [{"id": 11, "profile": "opa-editor", "ended_at": 1757500000},
                               {"id": 12, "profile": "opa-editor", "ended_at": None}]}}
    (tmp_path / "shows.json").write_text(json.dumps(shows), encoding="utf-8")
    log = tmp_path / "calls.log"
    runner = tmp_path / "child.py"
    runner.write_text(_CHILD_RUNNER.format(scripts=str(stage.SCRIPTS), shows=str(tmp_path / "shows.json"),
                                           log=str(log), stage_py=str(STAGE_PY)), encoding="utf-8")
    (v2_intaken / stage.PLAN_CHECKS).write_text(json.dumps({"t_a1a1a1a1": stage.PLAN_MAX_ROUNDS}), encoding="utf-8")
    bad = json.loads((FIXTURES / "v2" / "edit_v11.json").read_text(encoding="utf-8"))
    bad["shots"].pop(1)                                                    # SHOT_GAP
    (v2_intaken / "edit.json").write_text(json.dumps(bad, ensure_ascii=False), encoding="utf-8")

    def run(*args):
        proc = subprocess.run([sys.executable, str(runner), *args], capture_output=True, text=True,
                              encoding="utf-8", errors="replace", env=_child_env(paths.VID_ROOT))
        return proc.returncode, _protocol(proc.stdout)

    rc, got = run("PLAN", "--check", "--task", "t_a2a2a2a2")
    assert (rc, got["RESULT"]) == (1, "FAIL"), got                         # vòng 1 của a2, không BLOCK
    assert got["METADATA"]["round"] == 1
    assert f'python "{STAGE_PY.as_posix()}" PLAN --check --task t_a2a2a2a2' in got["NEXT"]
    assert json.loads((v2_intaken / stage.PLAN_CHECKS).read_text(encoding="utf-8")) == {
        "t_a1a1a1a1": stage.PLAN_MAX_ROUNDS, "t_a2a2a2a2": 1}
    calls = [json.loads(ln) for ln in log.read_text(encoding="utf-8").splitlines()]
    assert calls == [["kanban", "--board", "vm-heygen-b99", "show", "t_a2a2a2a2", "--json"]]

    shutil.copy2(FIXTURES / "v2" / "edit_v11.json", v2_intaken / "edit.json")
    rc, got = run("PLAN", "--check", "--task", "t_a2a2a2a2")
    assert (rc, got["RESULT"]) == (0, "PASS"), got
    row = state.read_state(v2_intaken)[-1]
    assert (row["stage"], row["task"], row["run"], row["profile"]) == ("PLAN", "t_a2a2a2a2", "12", "opa-editor")

    rc, got = run("PLAN", "--check")                                        # quên --task
    assert (rc, got["RESULT"]) == (1, "FAIL") and "--task <id trong câu" in got["NEXT"]
    assert all("list" not in c for c in
               (json.loads(ln) for ln in log.read_text(encoding="utf-8").splitlines()))


@pytest.mark.parametrize("runs, env_run, want", [
    ([{"id": 3, "ended_at": 10, "profile": "p"}], "77", "77"),              # mọi run đã kết thúc ⇒ env
    ([], None, "0"),
])
def test_run_id_falls_back_to_env_then_zero(tmp_path, v2_intaken, monkeypatch, capsys, runs, env_run, want):
    """R42: run = run chưa kết thúc trong `kanban show` (ended_at rỗng), không có thì
    $HERMES_KANBAN_RUN_ID, không có nữa thì "0"."""
    shown = {"task": {"id": "t_0000000f", "body": _body("PLAN", "2")}, "parents": [], "runs": runs}
    monkeypatch.setattr(kanban, "_run", lambda argv: type("P", (), {"returncode": 0, "stderr": "",
                                                                     "stdout": json.dumps(shown)})())
    if env_run:
        monkeypatch.setenv("HERMES_KANBAN_RUN_ID", env_run)
    assert stage.main(["PLAN", "--task", "t_0000000f"]) == 0
    assert "--task t_0000000f" in _protocol(capsys.readouterr().out)["NEXT"]
    row = state.read_state(v2_intaken)[-1]
    assert (row["stage"], row["task"], row["run"]) == ("PLAN", "t_0000000f", want)


def test_cli_prints_utf8_protocol_without_pythonioencoding(tmp_path):
    """Worker Hermes không đặt PYTHONIOENCODING: stage.py vẫn in tiếng Việt UTF-8, đủ 4 dòng."""
    env = {k: v for k, v in os.environ.items()
           if k not in ("PYTHONIOENCODING", "PYTHONUTF8", "HERMES_KANBAN_TASK", "HERMES_KANBAN_BOARD")}
    env["TH_VID_ROOT"] = str(tmp_path / "vid")
    run = subprocess.run([sys.executable, str(STAGE_PY), "PLAN", "--card-file",
                          _card(tmp_path, "không phải card con trỏ")], capture_output=True, env=env)
    got = _protocol(run.stdout.decode("utf-8"))
    assert run.returncode == 2 and "card ngoài mẫu" in got["NEXT"]


# ------------------------------------------------------------------ PLAN


@pytest.fixture
def v2_intaken(fixture_v2_words_corrected, fixture_v2_pauses_full):
    """Dự án video 02 như INTAKE để lại: rules.lock, words/pauses/meta.json, dòng STATE INTAKE."""
    project = paths.project_dir(2, "1.1.0")
    state.write_lock(project, "1.1.0")
    meta = {"video": 2, "source": SOURCE_V2.as_posix(), "duration_s": 43.2, "rules_version": "1.1.0",
            "preset": "standard", "vo_script_sha256": None, "script_match": 0.98, "guess_count": 0,
            "voice_hf_ratio": 0.01, "vo_qa": {"tilt_db": -5, "low_db": -15, "lufs": -16, "tp_dbtp": -2.5},
            "xcorr_ms": 0.0, "broll_class": "none", "claim_gate": False}
    for name, obj in (("words.json", fixture_v2_words_corrected),
                      ("pauses.json", fixture_v2_pauses_full), ("meta.json", meta)):
        (project / name).write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
    state.append_state(project, "INTAKE", "t_i", "1", "test",
                       [project / "words.json", project / "pauses.json", project / "meta.json"])
    return project


def test_plan_proposes_then_check_passes_and_records_state(tmp_path, v2_intaken, capsys):
    card = _card(tmp_path, _body("PLAN", "2"))
    assert stage.main(["PLAN", "--card-file", card]) == 0
    got = _protocol(capsys.readouterr().out)
    assert got["RESULT"] == "PASS"
    assert f'python "{STAGE_PY.as_posix()}" PLAN --check' in got["NEXT"]      # đường dẫn có dấu cách
    assert (v2_intaken / "propose_edit.json").is_file()

    shutil.copy2(FIXTURES / "v2" / "edit_v11.json", v2_intaken / "edit.json")
    assert stage.main(["PLAN", "--check", "--card-file", card]) == 0
    assert _protocol(capsys.readouterr().out)["RESULT"] == "PASS"
    rows = state.read_state(v2_intaken)
    assert rows[-1]["stage"] == "PLAN"
    assert rows[-1]["files"]["edit.json"] == state.sha8(v2_intaken / "edit.json")


def test_plan_check_fails_then_blocks_after_three_rounds(tmp_path, v2_intaken, capsys):
    card = _card(tmp_path, _body("PLAN", "2"))
    edit = json.loads((FIXTURES / "v2" / "edit_v11.json").read_text(encoding="utf-8"))
    edit["shots"].pop(1)                                     # SHOT_GAP
    (v2_intaken / "edit.json").write_text(json.dumps(edit, ensure_ascii=False), encoding="utf-8")
    results = []
    for _ in range(stage.PLAN_MAX_ROUNDS):
        rc = stage.main(["PLAN", "--check", "--card-file", card])
        out = capsys.readouterr().out
        results.append((rc, _protocol(out)["RESULT"]))
        assert "SHOT_GAP" in out
    assert results[:-1] == [(1, "FAIL")] * (stage.PLAN_MAX_ROUNDS - 1)
    assert results[-1] == (2, "BLOCK")
    assert all(r["stage"] != "PLAN" for r in state.read_state(v2_intaken))


@pytest.mark.parametrize("tool_error, kind", [(False, "needs_input"), (True, "capability")])
def test_build_text_safe_owner_depends_on_tool_error(tmp_path, v2_intaken, monkeypatch, capsys,
                                                     tool_error, kind):
    """B3: text_safe FAIL vì chữ tràn ⇒ block needs_input (owner PLAN hoặc template); vì lỗi
    công cụ (check_text_safe thoát 2, lỗi chương trình) ⇒ block capability (dev)."""
    shutil.copy2(FIXTURES / "v2" / "edit_v11.json", v2_intaken / "edit.json")
    state.append_state(v2_intaken, "PLAN", "t_p", "1", "test", [v2_intaken / "edit.json"])
    monkeypatch.setattr(stage.build, "run", lambda project, R, preset: {
        "ok": False, "failed_gate": "text_safe", "tool_error": tool_error, "artifacts": []})
    assert stage.main(["BUILD", "--card-file", _card(tmp_path, _body("BUILD", "2"))]) == 2
    got = _protocol(capsys.readouterr().out)
    assert got["METADATA"]["block"] == kind and got["METADATA"]["failed_gate"] == "text_safe"
    assert ("text_safe.json" in got["NEXT"]) is (not tool_error)


def _drift_release(tmp_path, monkeypatch, project):
    """C10: bản release giả (rules.json/schema thật + một script) có MANIFEST, paths.release_dir trỏ
    vào đó; `project` (nếu có) khoá lại vào bản giả; rồi một file bị sửa tại chỗ mà không sinh lại
    MANIFEST. Trả file bị sửa."""
    rel = tmp_path / "rel"
    (rel / "scripts").mkdir(parents=True)
    for name in ("rules.json", "rules.schema.json"):
        shutil.copy2(stage.REL / name, rel / name)
    edited = rel / "scripts" / "stage.py"
    edited.write_bytes(b"# ban gia\n")
    (rel / manifest.MANIFEST_NAME).write_text(manifest.build_manifest(rel), encoding="utf-8")
    monkeypatch.setattr(paths, "release_dir", lambda ver: rel)
    if project is not None:
        state.write_lock(project, "1.1.0")
    edited.write_bytes(b"# sua tai cho\n")
    return edited


@pytest.mark.parametrize("stage_name, kind", [("PLAN", "capability"), ("BUILD", "capability")])
def test_plan_and_build_block_when_release_drifts(tmp_path, v2_intaken, monkeypatch, capsys, stage_name, kind):
    """C10 + spec §4.3: PLAN và BUILD chạy lint_rules trước khi làm gì — một file release sửa tại
    chỗ sau khi khoá ⇒ BLOCK capability (dev), nêu file."""
    shutil.copy2(FIXTURES / "v2" / "edit_v11.json", v2_intaken / "edit.json")
    state.append_state(v2_intaken, "PLAN", "t_p", "1", "test", [v2_intaken / "edit.json"])
    edited = _drift_release(tmp_path, monkeypatch, v2_intaken)
    monkeypatch.setattr(stage.propose_edit, "run", lambda *a: pytest.fail("PLAN chạy với release lệch"))
    monkeypatch.setattr(stage.build, "run", lambda *a: pytest.fail("BUILD chạy với release lệch"))
    assert stage.main([stage_name, "--card-file", _card(tmp_path, _body(stage_name, "2"))]) == 2
    got = _protocol(capsys.readouterr().out)
    assert got["METADATA"]["block"] == kind and got["METADATA"]["cause"] == "capability"
    assert "lint_rules FAIL" in got["NEXT"] and edited.as_posix() in got["NEXT"]


def _fake_verify_pass(project, verdict="VERIFIED"):
    """verify.main giả: ghi out/verify/ như lượt chấm tất định thật (VERDICT, kpi, contact sheet)."""
    def fake(argv):
        out = project / "out" / "verify"
        out.mkdir(parents=True, exist_ok=True)
        checks = [{"id": f"V{i}", "ok": True, "msg": "ok"} for i in range(1, 8)]
        (out / "VERDICT.json").write_text(json.dumps({"verdict": verdict, "owner_stage": None, "checks": checks,
                                                      "concerns": []}), encoding="utf-8")
        for name in ("VERDICT.md", "kpi.json", "contact_sheet.png"):
            (out / name).write_text("{}", encoding="utf-8")
        return 0
    return fake


def test_verify_two_steps_fold_v7_concern(tmp_path, v2_intaken, monkeypatch, capsys):
    """V7: lượt VERIFY đầu chấm tất định, xoá nhận xét cũ và NEXT chỉ đúng hai đường dẫn tuyệt đối
    (contact sheet, out/verify/v7_concern.txt) cùng lệnh --finalize; verifier chỉ ghi vào file đó
    (vùng được ghi §10.1) rồi chạy VERIFY --finalize ⇒ VERDICT DONE_WITH_CONCERNS, dòng STATE."""
    card = _card(tmp_path, _body("VERIFY", "2"))
    out = v2_intaken / "out" / "verify"
    out.mkdir(parents=True)
    concern = out / "v7_concern.txt"
    concern.write_text("nhận xét của lần VERIFY trước", encoding="utf-8")
    monkeypatch.setattr(stage.verify, "main", _fake_verify_pass(v2_intaken))

    assert stage.main(["VERIFY", "--card-file", card]) == 0
    got = _protocol(capsys.readouterr().out)
    assert got["RESULT"] == "PASS" and not concern.exists()
    for needle in ((out / "contact_sheet.png").as_posix(), concern.as_posix(), "VERIFY --finalize"):
        assert needle in got["NEXT"], needle
    assert "kanban_complete" not in got["NEXT"]                               # R43: chưa complete

    concern.write_text("Khung 9: pill CTA đè lên mắt người nói.", encoding="utf-8")
    assert stage.main(["VERIFY", "--finalize", "--card-file", card]) == 0
    got = _protocol(capsys.readouterr().out)
    verdict = json.loads((out / "VERDICT.json").read_text(encoding="utf-8"))
    assert got["RESULT"] == "PASS" and got["METADATA"]["verdict"] == verdict["verdict"] == "DONE_WITH_CONCERNS"
    assert "tool kanban_complete" in got["NEXT"] and "summary = dòng SUMMARY" in got["NEXT"]   # R43/FS-5
    assert any("pill CTA đè lên mắt" in c for c in verdict["concerns"])
    rows = state.read_state(v2_intaken)
    assert rows[-1]["stage"] == "VERIFY" and rows[-1]["files"]["VERDICT.json"] == state.sha8(out / "VERDICT.json")


def test_verify_cannot_pass_silently_when_image_unseen(tmp_path, v2_intaken, monkeypatch, capsys):
    """R45 (MF-5): NEXT của lượt VERIFY đầu dặn — tool ảnh lỗi hoặc không xem được ảnh thì ghi
    `không xem được contact sheet: <lỗi>` vào out/verify/v7_concern.txt rồi --finalize; dòng đó
    đưa VERDICT về DONE_WITH_CONCERNS, không VERIFIED."""
    card = _card(tmp_path, _body("VERIFY", "2"))
    monkeypatch.setattr(stage.verify, "main", _fake_verify_pass(v2_intaken))
    assert stage.main(["VERIFY", "--card-file", card]) == 0
    got = _protocol(capsys.readouterr().out)
    concern = v2_intaken / "out" / "verify" / "v7_concern.txt"
    assert "không xem được contact sheet: <lỗi>" in got["NEXT"] and concern.as_posix() in got["NEXT"]
    assert got["NEXT"].index("không xem được contact sheet") < got["NEXT"].index("VERIFY --finalize")

    concern.write_text("không xem được contact sheet: vision 401 Invalid API Key", encoding="utf-8")
    assert stage.main(["VERIFY", "--finalize", "--card-file", card]) == 0
    got = _protocol(capsys.readouterr().out)
    assert got["METADATA"]["verdict"] == "DONE_WITH_CONCERNS" and got["METADATA"]["v7_concern"] is True


def test_verify_holds_machine_heavy_lock(tmp_path, v2_intaken, monkeypatch, capsys):
    """Spec §10.6 (ledger): VERIFY chạy verify.py (render stills của check_text_safe) trong khoá máy
    VID_ROOT/_batches/.heavy.lock; khoá bận quá HEAVY_WAIT_S ⇒ BLOCK transient, verify.py không chạy."""
    heavy = paths.VID_ROOT / "_batches" / ".heavy.lock"
    card = _card(tmp_path, _body("VERIFY", "2"))
    held, fake = [], _fake_verify_pass(v2_intaken)

    def verify_main(argv):
        try:
            with stage.file_lock(heavy):
                held.append(False)
        except stage.LockBusy:
            held.append(True)
        return fake(argv)
    monkeypatch.setattr(stage.verify, "main", verify_main)
    assert stage.main(["VERIFY", "--card-file", card]) == 0
    assert _protocol(capsys.readouterr().out)["RESULT"] == "PASS" and held == [True]

    monkeypatch.setattr(stage, "HEAVY_WAIT_S", 0.1)
    with stage.file_lock(heavy):
        assert stage.main(["VERIFY", "--card-file", card]) == 2
    got = _protocol(capsys.readouterr().out)
    assert got["METADATA"]["block"] == "transient" and heavy.as_posix() in got["NEXT"]
    assert held == [True]                                   # lượt bị chặn không chạy verify.py


def test_verify_finalize_needs_first_pass_and_only_verify(tmp_path, v2_intaken, capsys):
    """--finalize chỉ dành cho VERIFY, và cần lượt VERIFY đầu đã ghi VERDICT.json."""
    assert stage.main(["VERIFY", "--finalize", "--card-file", _card(tmp_path, _body("VERIFY", "2"))]) == 2
    assert _protocol(capsys.readouterr().out)["METADATA"]["block"] == "needs_input"
    assert stage.main(["PLAN", "--finalize", "--card-file", _card(tmp_path, _body("PLAN", "2"))]) == 1
    assert _protocol(capsys.readouterr().out)["RESULT"] == "FAIL"


def test_plan_without_intake_state_blocks(tmp_path, capsys):
    assert stage.main(["PLAN", "--card-file", _card(tmp_path, _body("PLAN", "2"))]) == 2
    assert _protocol(capsys.readouterr().out)["METADATA"]["block"] == "needs_input"


_FILE_TOKEN = re.compile(r"\S+?\.(?:json|md|txt|png|mp4|wav|lock|py)(?!\w)")


def _relative_paths(next_line: str, tmp_path) -> list[str]:
    """Đường dẫn file trong NEXT không nằm dưới một gốc tuyệt đối (tmp hoặc gốc skill) — C7."""
    text = next_line
    for root in (Path(tmp_path).as_posix(), stage.REL.parent.parent.as_posix()):
        text = text.replace(root, "ABS")
    tokens = [t.lstrip("\"'(") for t in _FILE_TOKEN.findall(text)]
    return [t for t in tokens if not t.startswith("ABS/")]


def test_next_lines_name_only_absolute_paths(tmp_path, v2_intaken, monkeypatch, capsys):
    """C7: cwd của worker Hermes là Vid Heygen/<n> (trên edit-r<ver> một cấp) — mọi đường dẫn
    trong NEXT phải tuyệt đối, nhất là edit.json / propose_edit.json của PLAN; file edit.json
    ghi lạc ra thư mục cha được chỉ ra."""
    card, edit = _card(tmp_path, _body("PLAN", "2")), v2_intaken / "edit.json"
    nexts = []

    def run(*argv):
        stage.main(list(argv))
        got = _protocol(capsys.readouterr().out)
        nexts.append(got["NEXT"])
        return got

    got = run("PLAN", "--card-file", card)                                     # PASS: chép khung
    assert edit.as_posix() in got["NEXT"] and (v2_intaken / "propose_edit.json").as_posix() in got["NEXT"]
    got = run("PLAN", "--check", "--card-file", card)                          # FAIL: chưa có edit.json
    assert got["RESULT"] == "FAIL" and edit.as_posix() in got["NEXT"]
    stray = v2_intaken.parent / "edit.json"                                    # ghi nhầm theo cwd
    stray.write_text("{}", encoding="utf-8")
    got = run("PLAN", "--check", "--card-file", card)
    assert stray.as_posix() in got["NEXT"] and edit.as_posix() in got["NEXT"]
    stray.unlink()
    bad = json.loads((FIXTURES / "v2" / "edit_v11.json").read_text(encoding="utf-8"))
    bad["shots"].pop(1)
    edit.write_text(json.dumps(bad, ensure_ascii=False), encoding="utf-8")
    got = run("PLAN", "--check", "--card-file", card)                          # FAIL: mã lỗi
    assert got["RESULT"] == "FAIL" and edit.as_posix() in got["NEXT"]

    shutil.copy2(FIXTURES / "v2" / "edit_v11.json", edit)
    state.append_state(v2_intaken, "PLAN", "t_p", "1", "test", [edit])
    monkeypatch.setattr(stage.build, "run", lambda project, R, preset: {
        "ok": False, "failed_gate": "text_safe", "tool_error": False, "artifacts": []})
    got = run("BUILD", "--card-file", _card(tmp_path, _body("BUILD", "2"), "build.txt"))   # BLOCK text_safe
    assert (v2_intaken / "out" / "safe" / "text_safe.json").as_posix() in got["NEXT"]
    (v2_intaken / state.STATE_FILENAME).unlink()
    got = run("PLAN", "--card-file", card)                                     # BLOCK: chưa qua INTAKE
    assert got["RESULT"] == "BLOCK" and (v2_intaken / "words.json").as_posix() in got["NEXT"]
    for line in nexts:
        assert _relative_paths(line, tmp_path) == [], line


# ------------------------------------------------------------------ PREP + check_prep


def _prep_video(n, status="ok", broll="none", assets=(), claim=False):
    return {"n": n, "status": status, "reasons": [] if status == "ok" else ["placeholder"],
            "broll_class": broll, "assets": list(assets), "claim_gate": claim,
            "claim_reasons": ["cần test thật"] if claim else []}


HEAVY_ASSET = {"desc": "Quay màn hình ChatGPT tạo 5 ảnh", "anchor_quote": "5 tài sản từ 1 ảnh",
               "kind": "screen_rec", "owner": "user", "due": "2026-09-20"}


@pytest.fixture
def batch_b99(v3_sections):
    """Lô b99: video 16 (ok) và 31 (needs_rerender), đúng khuôn intake.py (P0)."""
    batch = paths.batch_dir("b99")
    (batch / "vo_script").mkdir(parents=True)
    videos = []
    for n, status in ((16, "ok"), (31, "needs_rerender")):
        text = v3_sections[n]["script"]
        (batch / "vo_script" / f"{n}.txt").write_text(text, encoding="utf-8")
        videos.append({"n": n, "source": f"X:/vid/{n}/{n}.mp4", "v3": n,
                       "v3_title": v3_sections[n]["title"], "score": 0.91, "second_score": 0.2,
                       "status": status, "reasons": [] if status == "ok" else ["placeholder"],
                       "director_row": 18 if n == 16 else None, "eval_row": 18 if n == 16 else None,
                       "eval_type": None, "vo_script": f"vo_script/{n}.txt",
                       "vo_script_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
                       "canary": n == 16, "sample": False})
    manifest = {"batch": "b99", "rules_version": "1.1.0", "preset": "standard", "videos": videos}
    (batch / "batch_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    with (batch / "mapping.csv").open("w", encoding="utf-8-sig", newline="") as fh:     # khuôn intake.py
        w = csv.DictWriter(fh, fieldnames=["video", "best_v3", "score", "second_v3", "second_score",
                                           "motion_score", "v3_title", "flags", "heard"])
        w.writeheader()
        for n, flags in ((16, ""), (31, "placeholder")):
            w.writerow({"video": str(n), "best_v3": f"{n:02d}", "score": "0.91", "second_v3": "04",
                        "second_score": "0.20", "motion_score": "0.12", "v3_title": v3_sections[n]["title"],
                        "flags": flags, "heard": HEARD[n]})
    return batch


HEARD = {16: "lời thoại AI nghe như quảng cáo", 31: "tính năng tin mới mô tả nền G ngang hàng USC Case"}


def test_prep_prints_inputs_then_check_renders_sheet(tmp_path, batch_b99, v3_sections, capsys):
    card = _card(tmp_path, _body("PREP-1", "16,31"))
    assert stage.main(["PREP", "--card-file", card]) == 0
    out = capsys.readouterr().out
    got = _protocol(out)
    assert got["RESULT"] == "PASS" and "PREP --check" in got["NEXT"]
    assert str((batch_b99 / "vo_script" / "16.txt").as_posix()) in out.replace("\\", "/")
    assert "stages/PREP.md" in out.replace("\\", "/")
    assert v3_sections[16]["title"] in out and "đạo diễn #18" in out    # R14: tiêu đề + điểm gợi ý
    assert HEARD[31] in out and "motion 0.12" in out                     # dòng mapping.csv của video

    assert stage.main(["PREP", "--check", "--card-file", card]) == 1       # chưa có phiếu
    assert _protocol(capsys.readouterr().out)["RESULT"] == "FAIL"

    prep = {"batch": "b99", "videos": [_prep_video(16, broll="heavy", assets=[HEAVY_ASSET], claim=True),
                                       _prep_video(31, status="needs_rerender")]}
    (batch_b99 / "prep").mkdir()
    (batch_b99 / "prep" / "prep-1.json").write_text(json.dumps(prep, ensure_ascii=False), encoding="utf-8")
    assert stage.main(["PREP", "--check", "--card-file", card]) == 0
    got = _protocol(capsys.readouterr().out)
    assert got["RESULT"] == "PASS"
    assert "tool kanban_complete" in got["NEXT"] and 'dòng "ĐẠT: …"' in got["NEXT"]      # R43/FS-5
    sheet = (batch_b99 / "PREP-SHEET.md").read_text(encoding="utf-8")
    assert v3_sections[16]["title"] in sheet and HEAVY_ASSET["anchor_quote"] in sheet
    assert re.search(r"đạo diễn #18 \".+\" — tiêu đề \d\.\d\d, lời \d\.\d\d", sheet)
    assert re.search(r"phân loại #18 \".+\" — tiêu đề \d\.\d\d", sheet)
    assert "Video 31" in sheet and "needs_rerender" in sheet


APPROVALS = """# APPROVALS — batch b99

- Canary: video 16
- Mẫu (1/5): video 16

## Lời duyệt
(operator chép nguyên văn lời duyệt của user vào đây)
- 2026-09-12 PREP-1 (user muốn sửa): "video 16 không cần quay màn hình,
  dùng ảnh AI là đủ"
- 2026-09-12 PREP-10: "ok"
- 2026-09-13 APPROVE-PREP-2: "duyệt"
"""


@pytest.mark.parametrize("attempt", [1, 2])
def test_prep_prints_user_notes_and_retry_revises_per_them(tmp_path, batch_b99, capsys, attempt):
    """FS-3: PREP in các mục "## Lời duyệt" của APPROVALS.md nhắc PREP-<k> (đủ dòng nối tiếp, không
    lẫn PREP-10 hay PREP khác); lần thử a2 trở đi NEXT dặn sửa phiếu theo đúng lời đó."""
    (batch_b99 / "APPROVALS.md").write_text(APPROVALS, encoding="utf-8")
    card = _card(tmp_path, _body("PREP-1", "16,31", attempt=attempt))
    assert stage.main(["PREP", "--card-file", card]) == 0
    out = capsys.readouterr().out
    got = _protocol(out)
    assert 'PREP-1 (user muốn sửa): "video 16 không cần quay màn hình,' in out
    assert "dùng ảnh AI là đủ" in out and "PREP-10" not in out and "APPROVE-PREP-2" not in out
    revise = "sửa phiếu theo lời user về PREP-1 in ở trên"
    assert (revise in got["NEXT"]) is (attempt > 1)
    assert "PREP --check" in got["NEXT"] and "kanban_complete" not in got["NEXT"]


def test_approval_notes_keep_bulleted_verbatim_reply(tmp_path):
    """consistency-2: lời user dán nguyên văn có dòng bắt đầu "- " vẫn thuộc mục của nó — mục mới chỉ
    bắt đầu ở dòng đầu mục "- … <YYYY-MM-DD> …" (tên card + ngày, OPERATOR.md §3)."""
    reply = ['- APPROVE-PREP-1 — 2026-09-20 — sửa phiếu: "Sửa mấy chỗ:',
             "- video 16 để needs_input, chờ tôi quay màn hình",
             '- video 21 ghép mục v3 số 12"']
    (tmp_path / "APPROVALS.md").write_text(
        "# APPROVALS — batch b01\n\n- Canary: video 16\n\n## Lời duyệt\n(operator chép nguyên văn lời duyệt của user "
        "vào đây)\n- APPROVE-PREP-2 — 2026-09-19: duyệt\n" + "\n".join(reply)
        + "\n- APPROVE-PREP-10 — 2026-09-21: duyệt\n", encoding="utf-8")
    assert stage.prep.approval_notes(tmp_path, 1) == ["\n".join(reply)]
    assert stage.prep.approval_notes(tmp_path, 2) == ["- APPROVE-PREP-2 — 2026-09-19: duyệt"]


def test_prep_retry_without_notes_does_not_claim_user_notes(tmp_path, batch_b99, capsys):
    """consistency-2: lần thử a2 (vd. sau timed_out) mà APPROVALS.md chưa có mục nào về PREP-<k> ⇒ NEXT
    không bảo "sửa theo lời user in ở trên" (chỉ in "(chưa có)"), mà nói rõ là làm lại theo PREP.md."""
    card = _card(tmp_path, _body("PREP-1", "16,31", attempt=2))
    assert stage.main(["PREP", "--card-file", card]) == 0
    out = capsys.readouterr().out
    got = _protocol(out)
    assert "(chưa có)" in out and "sửa phiếu theo lời user" not in got["NEXT"]
    assert "APPROVALS.md chưa có mục nào về PREP-1; làm lại phiếu theo PREP.md" in got["NEXT"]


def test_prep_and_card_errors_name_absolute_paths(tmp_path, batch_b99, capsys):
    """C7: PREP --check chưa có phiếu (hướng dẫn stages/PREP.md) và card ghi preset lạ (rules.json)
    cũng chỉ in đường dẫn tuyệt đối."""
    assert stage.main(["PREP", "--check", "--card-file", _card(tmp_path, _body("PREP-1", "16,31"))]) == 1
    got = _protocol(capsys.readouterr().out)
    assert (stage.REL / "stages" / "PREP.md").as_posix() in got["NEXT"]
    assert _relative_paths(got["NEXT"], tmp_path) == []
    assert stage.main(["PLAN", "--card-file", _card(tmp_path, _body("PLAN", "2", preset="zzz"), "p.txt")]) == 2
    got = _protocol(capsys.readouterr().out)
    assert (stage.REL / "rules.json").as_posix() in got["NEXT"]
    assert _relative_paths(got["NEXT"], tmp_path) == []


def test_hint_scores_are_the_numbers_the_matcher_used(v3_sections):
    """R14: điểm in trên PREP-SHEET đúng là số match_director / match_eval dùng để chọn."""
    director = scripts_v3.load_director(FIXTURES / "scripts" / scripts_v3.DIRECTOR_FILENAME)
    eval_rows = scripts_v3.load_eval(FIXTURES / "scripts" / scripts_v3.EVAL_FILENAME)
    for v3_n in (16, 21, 27):                               # ba ca ghép tiêu đề đã kiểm tay (spec §6.1)
        section = v3_sections[v3_n]
        best = mapping.match_director(section, director)
        scores = {n: mapping.hint_scores(section, d, None) for n, d in director.items()}
        gated = {n: s["director_text"] for n, s in scores.items() if s["director_title"] >= 0.5}
        assert max(gated, key=gated.get) == best            # dòng được chọn = lời khớp nhất trong số qua ngưỡng
        assert len({round(s["director_text"], 6) for s in scores.values()}) > 10      # điểm thật, không hằng số
        e = next(r for r in eval_rows if r["row"] == mapping.match_eval(section, best, eval_rows))
        assert mapping.hint_scores(section, None, e)["eval_title"] >= 0.5
    assert mapping.hint_scores(v3_sections[16], None, None) == {"director_title": None, "director_text": None,
                                                                "eval_title": None}


def test_prep_check_rejects_video_set_other_than_card(tmp_path, batch_b99, capsys):
    (batch_b99 / "prep").mkdir()
    prep = {"batch": "b99", "videos": [_prep_video(16)]}
    (batch_b99 / "prep" / "prep-1.json").write_text(json.dumps(prep), encoding="utf-8")
    card = _card(tmp_path, _body("PREP-1", "16,31"))
    assert stage.main(["PREP", "--check", "--card-file", card]) == 1
    assert "31" in capsys.readouterr().out


@pytest.mark.parametrize("mutate, needle", [
    (lambda v: v.pop("broll_class"), "broll_class"),
    (lambda v: v.pop("status"), "status"),
    (lambda v: v["assets"][0].update(anchor_quote=""), "anchor_quote"),
    (lambda v: v["assets"][0].pop("desc"), "desc"),
    (lambda v: v.update(assets=[]), "heavy"),
    (lambda v: v.update(claim_reasons=[]), "claim"),
    (lambda v: v["assets"][0].update(kind="meme"), "kind"),
])
def test_check_prep_rejects(tmp_path, capsys, mutate, needle):
    video = _prep_video(16, broll="heavy", assets=[dict(HEAVY_ASSET)], claim=True)
    mutate(video)
    path = tmp_path / "prep-1.json"
    path.write_text(json.dumps({"batch": "b99", "videos": [video]}, ensure_ascii=False), encoding="utf-8")
    assert check_prep.main([str(path)]) == 1
    assert needle in capsys.readouterr().out


def test_check_prep_passes_valid_sheet(tmp_path, capsys):
    prep = {"batch": "b99", "videos": [
        _prep_video(16, broll="heavy", assets=[HEAVY_ASSET], claim=True),
        _prep_video(21, broll="light", assets=[{**HEAVY_ASSET, "desc": "", "owner": "agent",
                                                 "kind": "ai_image", "due": None}]),
        {**_prep_video(31, status="needs_rerender"), "note": "HeyGen đọc nguyên placeholder"}]}
    path = tmp_path / "prep-1.json"
    path.write_text(json.dumps(prep, ensure_ascii=False), encoding="utf-8")
    assert check_prep.main([str(path)]) == 0
    assert "PASS" in capsys.readouterr().out


# ------------------------------------------------------------------ INTAKE (nhánh nhanh)


def test_intake_blocks_without_approved_prep(tmp_path, batch_b99, capsys):
    card = _card(tmp_path, _body("INTAKE", "16"))
    assert stage.main(["INTAKE", "--card-file", card]) == 2
    got = _protocol(capsys.readouterr().out)
    assert got["METADATA"]["block"] == "needs_input" and "PREP" in got["NEXT"]
    assert not paths.project_dir(16, "1.1.0").exists()                  # chưa scaffold gì


def test_intake_blocks_when_vo_script_was_edited(tmp_path, batch_b99, capsys):
    (batch_b99 / "prep").mkdir()
    prep = {"batch": "b99", "videos": [_prep_video(16), _prep_video(31, status="needs_rerender")]}
    (batch_b99 / "prep" / "prep-1.json").write_text(json.dumps(prep), encoding="utf-8")
    (batch_b99 / "vo_script" / "16.txt").write_text("lời đã bị sửa tay", encoding="utf-8")
    assert stage.main(["INTAKE", "--card-file", _card(tmp_path, _body("INTAKE", "16"))]) == 2
    got = _protocol(capsys.readouterr().out)
    assert got["METADATA"]["block"] == "needs_input" and "vo_script" in got["NEXT"]
    # C6: lệnh an toàn đúng từng chữ — intake --update chỉ video này, lời nghe lấy từ mapping.csv của lô
    intake_py = (stage.SCRIPTS / "intake.py").as_posix()
    assert (f'python "{intake_py}" --batch b99 --update --videos 16 '
            f'--transcriber "cache:{(batch_b99 / "mapping.csv").as_posix()}" --preset standard --rules 1.1.0'
            ) in got["NEXT"]
    assert "--retry 16:INTAKE" in got["NEXT"]


def test_intake_lint_after_scaffold_rehashes_release_files(tmp_path, batch_b99, monkeypatch, capsys):
    """C10: scaffold vừa ghi rules.lock mới, nên lint_rules sau đó không được là phép lặp lock ==
    MANIFEST — nó băm lại file release: bản release sửa tại chỗ ⇒ INTAKE BLOCK capability, nêu file,
    không chạy tiếp INTAKE lõi."""
    (batch_b99 / "prep").mkdir()
    prep = {"batch": "b99", "videos": [_prep_video(16), _prep_video(31, status="needs_rerender")]}
    (batch_b99 / "prep" / "prep-1.json").write_text(json.dumps(prep), encoding="utf-8")
    source = tmp_path / "16.mp4"
    source.write_bytes(b"\x00")
    manifest_path = batch_b99 / "batch_manifest.json"
    batch = json.loads(manifest_path.read_text(encoding="utf-8"))
    batch["videos"] = [{**v, "source": source.as_posix()} if v["n"] == 16 else v for v in batch["videos"]]
    manifest_path.write_text(json.dumps(batch, ensure_ascii=False), encoding="utf-8")
    edited = _drift_release(tmp_path, monkeypatch, None)
    monkeypatch.setattr(stage, "scaffold", lambda project, src, ver: state.write_lock(project, ver))
    monkeypatch.setattr(stage, "intake_core", lambda *a: pytest.fail("INTAKE chạy tiếp với release lệch"))
    assert stage.main(["INTAKE", "--card-file", _card(tmp_path, _body("INTAKE", "16"))]) == 2
    got = _protocol(capsys.readouterr().out)
    assert got["METADATA"]["block"] == "capability" and "lint_rules FAIL" in got["NEXT"]
    assert edited.as_posix() in got["NEXT"]


def _intake_ready(tmp_path, batch, monkeypatch):
    """Lô b99 sẵn cho INTAKE video 16: phiếu PREP ok, video nguồn có thật, font pack giả."""
    (batch / "prep").mkdir()
    prep = {"batch": "b99", "videos": [_prep_video(16), _prep_video(31, status="needs_rerender")]}
    (batch / "prep" / "prep-1.json").write_text(json.dumps(prep), encoding="utf-8")
    source = tmp_path / "16.mp4"
    source.write_bytes(b"\x00")
    manifest_path = batch / "batch_manifest.json"
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    data["videos"] = [{**v, "source": source.as_posix()} if v["n"] == 16 else v for v in data["videos"]]
    manifest_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    pack = tmp_path / "fonts"
    for rel in stage.FONTS.values():
        (pack / rel).parent.mkdir(parents=True, exist_ok=True)
        (pack / rel).write_bytes(b"font")
    monkeypatch.setattr(stage, "FONT_PACK", pack)


def _fake_heavy(calls, slow=None):
    """proc.run giả: ghi (lệnh, timeout); lệnh chứa `slow` thì quá hạn; ffmpeg ghi file đích."""
    def run(args, *, timeout, **kw):
        text = args if isinstance(args, str) else " ".join(map(str, args))
        calls.append((text, timeout))
        if slow and slow in text:
            raise subprocess.TimeoutExpired(args, timeout, output="đang chạy dở")
        if not isinstance(args, str) and Path(str(args[0])).name == "ffmpeg":
            Path(args[-1]).write_bytes(b"mp4")
        return subprocess.CompletedProcess(args, 0, "", "")
    return run


@pytest.mark.parametrize("slow, limit", [("ffmpeg", 600), ("npm install", 900), ("browser ensure", 900)])
def test_scaffold_timeout_blocks_transient(tmp_path, batch_b99, monkeypatch, capsys, slow, limit):
    """R47 (FS-2): mã hoá master (600 s), npm install (900 s), tải trình duyệt Remotion (900 s) có
    trần thời gian; quá hạn ⇒ cả cây process bị giết (thlib.proc) và card BLOCK transient."""
    _intake_ready(tmp_path, batch_b99, monkeypatch)
    calls = []
    monkeypatch.setattr(stage.proc, "run", _fake_heavy(calls, slow))
    monkeypatch.setattr(stage, "intake_core", lambda *a: pytest.fail("INTAKE chạy tiếp sau khi quá hạn"))
    assert stage.main(["INTAKE", "--card-file", _card(tmp_path, _body("INTAKE", "16"))]) == 2
    got = _protocol(capsys.readouterr().out)
    assert got["METADATA"]["block"] == "transient" and f"{limit} s" in got["NEXT"]
    assert calls[-1][1] == limit and slow in calls[-1][0]


def test_build_and_verify_timeouts_block_transient(tmp_path, v2_intaken, monkeypatch, capsys):
    """R47: process con quá hạn trong BUILD (render 1200 s) hay VERIFY (V2 render still 180 s) ⇒
    BLOCK transient nêu trần thời gian, khoá video/máy được nhả."""
    shutil.copy2(FIXTURES / "v2" / "edit_v11.json", v2_intaken / "edit.json")
    state.append_state(v2_intaken, "PLAN", "t_p", "1", "test", [v2_intaken / "edit.json"])

    def raiser(cmd, limit):
        def slow(*a, **kw):
            raise subprocess.TimeoutExpired(cmd, limit)
        return slow
    monkeypatch.setattr(stage.build, "run", raiser(["remotion", "render"], 1200))
    assert stage.main(["BUILD", "--card-file", _card(tmp_path, _body("BUILD", "2"), "b.txt")]) == 2
    got = _protocol(capsys.readouterr().out)
    assert got["METADATA"]["block"] == "transient" and "1200 s" in got["NEXT"]
    monkeypatch.setattr(stage.verify, "main", raiser(["remotion", "still"], 180))
    assert stage.main(["VERIFY", "--card-file", _card(tmp_path, _body("VERIFY", "2"), "v.txt")]) == 2
    got = _protocol(capsys.readouterr().out)
    assert got["METADATA"]["block"] == "transient" and "180 s" in got["NEXT"]
    for lock in (paths.VID_ROOT / "2" / ".stage.lock", paths.VID_ROOT / "_batches" / ".heavy.lock"):
        with stage.file_lock(lock):                                         # đã nhả
            pass


def test_scaffold_ensures_remotion_browser_after_npm_install(tmp_path, batch_b99, monkeypatch, capsys):
    """R47 (FS-13): scaffold tải trình duyệt của Remotion ngay sau npm install (INTAKE, ngoài khoá
    máy) — BUILD không bao giờ tải trong lúc giữ .heavy.lock."""
    _intake_ready(tmp_path, batch_b99, monkeypatch)
    calls = []
    monkeypatch.setattr(stage.proc, "run", _fake_heavy(calls))
    monkeypatch.setattr(stage, "intake_core", lambda *a: (_ for _ in ()).throw(stage.Block("needs_input", "dừng")))
    assert stage.main(["INTAKE", "--card-file", _card(tmp_path, _body("INTAKE", "16"))]) == 2
    remotion = paths.project_dir(16, "1.1.0") / "node_modules" / ".bin" / stage.bin_name("remotion")
    assert [t for _, t in calls] == [600, 900, 900]
    assert calls[0][0].startswith("ffmpeg ") and calls[1][0] == "npm install --no-audit --no-fund"
    assert calls[2][0] == f"{remotion} browser ensure"


# ------------------------------------------------------------------ e2e chậm (video 02 thật)


def _run_stage(root, *args):
    run = subprocess.run([sys.executable, str(paths.release_dir("1.1.0") / "scripts" / "stage.py"), *args],
                         capture_output=True, text=True, encoding="utf-8", errors="replace",
                         env={**os.environ, "PYTHONIOENCODING": "utf-8", "TH_VID_ROOT": str(root),
                              "HERMES_KANBAN_TASK": "", "HERMES_KANBAN_BOARD": ""})
    print(run.stdout[-3000:], run.stderr[-2000:])
    return run.returncode, _protocol(run.stdout)


@pytest.mark.slow
def test_stage_end_to_end_video2(tmp_path, v3_sections, monkeypatch):
    """INTAKE (scaffold + whisper large-v3 thật) → PLAN → PLAN --check → BUILD → VERIFY qua
    stage.py ở process con, TH_VID_ROOT = tmp; agent PLAN được mô phỏng: khung propose_edit.json
    + câu CTA của video 02."""
    root = tmp_path / "vid"
    monkeypatch.setattr(paths, "VID_ROOT", root)
    batch = paths.batch_dir("b99")
    (batch / "vo_script").mkdir(parents=True)
    (batch / "prep").mkdir()
    text = v3_sections[2]["script"]
    (batch / "vo_script" / "2.txt").write_text(text, encoding="utf-8")
    manifest = {"batch": "b99", "rules_version": "1.1.0", "preset": "standard", "videos": [
        {"n": 2, "source": SOURCE_V2.as_posix(), "v3": 2, "v3_title": v3_sections[2]["title"],
         "score": 0.95, "second_score": 0.2, "status": "ok", "reasons": [], "director_row": None,
         "eval_row": None, "eval_type": None, "vo_script": "vo_script/2.txt",
         "vo_script_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
         "canary": True, "sample": False}]}
    (batch / "batch_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    (batch / "prep" / "prep-1.json").write_text(json.dumps({"batch": "b99", "videos": [_prep_video(2)]}),
                                                encoding="utf-8")
    cards = {s: _card(tmp_path, _body(s, "2"), f"{s}.txt") for s in ("INTAKE", "PLAN", "BUILD", "VERIFY")}
    project = paths.project_dir(2, "1.1.0")

    rc, got = _run_stage(root, "INTAKE", "--card-file", cards["INTAKE"])
    assert (rc, got["RESULT"]) == (0, "PASS"), got
    assert "tool kanban_complete" in got["NEXT"] and "summary = dòng SUMMARY" in got["NEXT"]   # R43/FS-5
    meta = json.loads((project / "meta.json").read_text(encoding="utf-8"))
    assert meta["script_match"] >= 0.9 and meta["broll_class"] == "none"
    assert meta["vo_script_sha256"] == manifest["videos"][0]["vo_script_sha256"]
    words = json.loads((project / "words.json").read_text(encoding="utf-8"))
    assert all(b["on"] >= a["on"] + 0.02 - 1e-9 for a, b in zip(words, words[1:]))
    assert (project / "ASR_REPORT.md").is_file() and (project / "node_modules").is_dir()

    rc, got = _run_stage(root, "PLAN", "--card-file", cards["PLAN"])
    assert (rc, got["RESULT"]) == (0, "PASS"), got
    edit = json.loads((project / "propose_edit.json").read_text(encoding="utf-8"))
    (project / "edit.json").write_text(json.dumps({**edit, "cta": CTA_V2}, ensure_ascii=False), encoding="utf-8")
    rc, got = _run_stage(root, "PLAN", "--check", "--card-file", cards["PLAN"])
    assert (rc, got["RESULT"]) == (0, "PASS"), got

    rc, got = _run_stage(root, "BUILD", "--card-file", cards["BUILD"])
    assert (rc, got["RESULT"]) == (0, "PASS"), got
    assert (project / "out" / "final.mp4").is_file()

    rc, got = _run_stage(root, "VERIFY", "--card-file", cards["VERIFY"])
    assert (rc, got["RESULT"]) == (0, "PASS"), got
    verdict = json.loads((project / "out" / "verify" / "VERDICT.json").read_text(encoding="utf-8"))
    assert verdict["verdict"] in ("VERIFIED", "DONE_WITH_CONCERNS"), verdict
    assert [r["stage"] for r in state.read_state(project)] == ["INTAKE", "PLAN", "PLAN", "BUILD", "VERIFY"]
