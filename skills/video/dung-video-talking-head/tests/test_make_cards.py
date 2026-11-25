# tests/test_make_cards.py — vỏ Hermes CLI (thlib.kanban) và make_cards.py (Task 14).
# Không test nào tạo card thật: create() đi đường dry_run, hoặc runner subprocess bị thay
# bằng hàm giả (_FakeCli) ghi lại argv và trả JSON có kèm dòng banner "⚠ … gateway".
import json
from collections import Counter
from pathlib import Path

import pytest

import make_cards
from thlib import kanban, paths

_REAL_RUN = kanban._run                                  # runner thật (fixture autouse thay nó trong mọi test)

BANNER = ("⚠ A previous `hermes update` pulled new code but did not restart running gateways.\n"
          "  Gateways may still be serving pre-update modules (mixed sys.modules).\n"
          "  Run `hermes update` or `hermes gateway restart`.\n")


class _Proc:
    def __init__(self, stdout, returncode=0, stderr=""):
        self.stdout, self.returncode, self.stderr = stdout, returncode, stderr


class _FakeCli:
    """Thay kanban._run: ghi argv; `boards list` trả self.boards, `create` trả id tăng dần,
    `show` trả self.shows[id]."""

    def __init__(self):
        self.calls, self.shows, self.n = [], {}, 0
        self.boards = ["default", "vm-heygen-b01"]

    def __call__(self, argv):
        self.calls.append(argv)
        if argv[2:4] == ["boards", "list"]:
            return _Proc(BANNER + json.dumps([{"slug": s, "archived": False} for s in self.boards], indent=2))
        if "create" in argv:
            self.n += 1
            return _Proc(BANNER + json.dumps({"id": f"t_{self.n:04d}", "status": "todo"}, indent=2))
        if "show" in argv:
            return _Proc(BANNER + json.dumps(self.shows[argv[argv.index("show") + 1]], indent=2))
        return _Proc("", 2, "lệnh lạ")

    def creates(self):
        return [a for a in self.calls if "create" in a]


def _flag(argv, name):
    return [argv[i + 1] for i, a in enumerate(argv) if a == name]


@pytest.fixture(autouse=True)
def _no_real_cli(monkeypatch):
    """Mặc định cấm gọi Hermes CLI thật; test nào cần thì tự thay kanban._run bằng _FakeCli."""
    def no_cli(argv):
        raise AssertionError("test không được gọi Hermes CLI thật")
    monkeypatch.setattr(kanban, "_run", no_cli)


# ------------------------------------------------------------------ thlib.kanban


def test_show_strips_gateway_banner_before_json(monkeypatch):
    fake = _FakeCli()
    fake.shows["t_1"] = {"task": {"id": "t_1", "body": "VIDEO: 7"}, "parents": [], "children": []}
    monkeypatch.setattr(kanban, "_run", fake)
    got = kanban.show("t_1", "vm-heygen-b01")
    assert got["task"]["body"] == "VIDEO: 7"
    assert fake.calls[0][:3] == [kanban.HB, "kanban", "--board"]
    assert fake.calls[0][-3:] == ["show", "t_1", "--json"]


def test_cli_error_raises(monkeypatch):
    monkeypatch.setattr(kanban, "_run", lambda argv: _Proc(BANNER, 1, "no such task: t_x"))
    with pytest.raises(kanban.KanbanError, match="no such task"):
        kanban.show("t_x", None)


def test_cli_error_drops_banner_from_stderr(monkeypatch):
    """hermes-semantics-2: Hermes in banner "⚠ … hermes update" ở stderr ngay trước lỗi — lỗi (rồi lý do
    block của stage.py) chỉ giữ dòng lỗi thật."""
    monkeypatch.setattr(kanban, "_run", lambda argv: _Proc("", 1, BANNER + "no such task: t_x\n"))
    with pytest.raises(kanban.KanbanError) as err:
        kanban.show("t_x", None)
    assert "no such task: t_x" in str(err.value)
    assert "hermes update" not in str(err.value) and "⚠" not in str(err.value)


def test_create_dry_run_never_calls_cli(monkeypatch):
    def boom(argv):
        raise AssertionError("dry_run không được gọi CLI")
    monkeypatch.setattr(kanban, "_run", boom)
    got = kanban.create("vm-heygen-b01", "[vmh-07] PLAN", "body", "opa-editor", ["t_a"],
                        "dir:X:/vid/7", "vmh-7-plan-a1", ["dung-video-talking-head"], "20m", 2, 2,
                        dry_run=True)
    assert got["id"] == "<vmh-7-plan-a1>"
    argv = got["argv"]
    assert argv[:5] == [kanban.HB, "kanban", "--board", "vm-heygen-b01", "create"]
    assert _flag(argv, "--parent") == ["t_a"] and _flag(argv, "--goal-max-turns") == ["2"]
    assert "--goal" in argv and argv[-1] == "--json"


@pytest.mark.parametrize("stage", ["PREP", "INTAKE", "PLAN", "BUILD", "VERIFY"])
def test_max_retries_is_rules_retries_plus_one(rules_110, stage):
    """C2: rules budgets.<stage>.retries = số lần thử lại SAU lần đầu; Hermes `--max-retries N`
    ngắt ở lần hỏng thứ N ⇒ truyền retries + 1 (INTAKE/BUILD/VERIFY 1 → 2, PREP/PLAN 2 → 3)."""
    b = rules_110.get(f"budgets.{stage}")
    got = kanban.create("b", "t", "body", "opa-editor", [], None, "k", [], b["runtime"], b["retries"],
                        b["goal_turns"], dry_run=True)
    assert _flag(got["argv"], "--max-retries") == [str(b["retries"] + 1)]
    no_retry = kanban.create("b", "t", "body", "opa-editor", [], None, "k", [], None, 0, 0, dry_run=True)
    assert _flag(no_retry["argv"], "--max-retries") == ["1"]              # 0 lần thử lại ⇒ ngắt ở lần hỏng đầu


def test_create_returns_id_parsed_after_banner(monkeypatch):
    fake = _FakeCli()
    monkeypatch.setattr(kanban, "_run", fake)
    tid = kanban.create("b", "[vmh-b01] APPROVE-CANARY", "chờ user", "user", ["t_v"], None,
                        "vmh-b01-approve-canary-a1", [], None, None, 0)
    assert tid == "t_0001"
    argv = fake.calls[0]
    for absent in ("--workspace", "--skill", "--max-runtime", "--max-retries", "--goal",
                   "--model", "--initial-status"):
        assert absent not in argv, absent
    assert _flag(argv, "--assignee") == ["user"]


# ------------------------------------------------------------------ make_cards


def _video(n, status, canary=False):
    return {"n": n, "source": f"X:/vid/{n}/{n}.mp4", "v3": n, "v3_title": f"Mục {n}",
            "score": 0.9, "second_score": 0.2, "status": status,
            "reasons": [] if status == "ok" else ["placeholder"], "director_row": None,
            "eval_row": None, "eval_type": None, "vo_script": f"vo_script/{n}.txt",
            "vo_script_sha256": "0" * 64, "canary": canary, "sample": False}


FAKE_MANIFEST = {"batch": "b01", "rules_version": "1.1.0", "preset": "standard",
                 "videos": [_video(3, "ok", canary=True), _video(4, "ok"), _video(5, "ok"),
                            _video(6, "needs_rerender")]}


@pytest.fixture
def vid_root(tmp_path, monkeypatch):
    """VID_ROOT tạm với lô b01 = FAKE_MANIFEST (3 ok + 1 needs_rerender)."""
    monkeypatch.setattr(paths, "VID_ROOT", tmp_path)
    monkeypatch.delenv("TH_VID_ROOT", raising=False)       # FS-9: chạy thật từ chối TH_VID_ROOT
    batch = paths.batch_dir("b01")
    batch.mkdir(parents=True)
    (batch / "batch_manifest.json").write_text(json.dumps(FAKE_MANIFEST, ensure_ascii=False),
                                               encoding="utf-8")
    return tmp_path


def _by_key(cards):
    return {c["key"]: c for c in cards}


def _prep_entry(n, status):
    return {"n": n, "status": status, "reasons": [] if status == "ok" else ["user chưa quyết"],
            "broll_class": "none", "assets": [], "claim_gate": False, "claim_reasons": []}


def _approved(statuses):
    """Phiếu PREP-1 đã duyệt của lô b01 (nhóm duy nhất: video 3, 4, 5, 6)."""
    return {1: {"batch": "b01", "videos": [_prep_entry(n, s) for n, s in sorted(statuses.items())]}}


PREPS_OK = _approved({3: "ok", 4: "ok", 5: "ok", 6: "needs_rerender"})
PREP_KEYS = ["vmh-b01-prep-1-a1", "vmh-b01-approve-prep-1-a1"]


def _write_prep(statuses):
    path = paths.batch_dir("b01") / "prep" / "prep-1.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(_approved(statuses)[1], ensure_ascii=False), encoding="utf-8")


def _registry():
    return json.loads((paths.batch_dir("b01") / make_cards.REGISTRY).read_text(encoding="utf-8"))


def _approve_all(fake):
    """APPROVE-PREP-<k> đã complete trên board giả (operator complete sau lời duyệt của user)."""
    for e in _registry()["cards"].values():
        if e["kind"] == "APPROVE-PREP":
            fake.shows[e["id"]] = {"task": {"id": e["id"], "status": "done", "body": ""}}


def test_phase_prep_plans_only_prep_and_approval(rules_110):
    """C1: P0 chỉ tạo PREP-<k> và APPROVE-PREP-<k>; chưa có canary hay chuỗi video nào."""
    cards = make_cards.plan_cards(FAKE_MANIFEST, {}, rules_110, "prep")
    assert [c["key"] for c in cards] == PREP_KEYS
    assert cards[1]["parents"] == ["vmh-b01-prep-1-a1"] and cards[0]["parents"] == []
    assert make_cards.check_plan(cards, FAKE_MANIFEST, {}, rules_110, "prep", {"cards": {}}) == []


def test_phase_videos_plans_canary_then_other_chains(rules_110):
    cards = make_cards.plan_cards(FAKE_MANIFEST, PREPS_OK, rules_110, "videos")
    kinds = Counter(c["kind"] for c in cards)
    assert kinds == {"APPROVE-CANARY": 1, "INTAKE": 3, "PLAN": 3, "BUILD": 3, "VERIFY": 3}
    assert Counter(c["video"] for c in cards if c["video"] is not None) == {3: 4, 4: 4, 5: 4}
    keys = [c["key"] for c in cards]
    for c in cards:                                         # cha trong phase này luôn đứng trước con
        assert all(keys.index(p) < keys.index(c["key"]) for p in c["parents"] if p in keys), c["key"]
    k = _by_key(cards)
    assert k["vmh-3-intake-a1"]["parents"] == ["vmh-b01-approve-prep-1-a1"]
    assert k["vmh-3-verify-a1"]["parents"] == ["vmh-3-build-a1"]
    assert k["vmh-b01-approve-canary-a1"]["parents"] == ["vmh-3-verify-a1"]
    for n in (4, 5):
        assert k[f"vmh-{n}-intake-a1"]["parents"] == ["vmh-b01-approve-prep-1-a1", "vmh-b01-approve-canary-a1"]
        assert k[f"vmh-{n}-verify-a1"]["parents"] == [f"vmh-{n}-build-a1"]
    registered = {"cards": {key: {"parents": []} for key in PREP_KEYS}}
    assert make_cards.check_plan(cards, FAKE_MANIFEST, PREPS_OK, rules_110, "videos", registered) == []
    errors = make_cards.check_plan(cards, FAKE_MANIFEST, PREPS_OK, rules_110, "videos", {"cards": {}})
    assert any("vmh-b01-approve-prep-1-a1" in e for e in errors)          # phase prep chưa chạy


def test_phase_videos_picks_next_ok_canary_when_prep_flips_it(rules_110):
    """C1 (hồi quy): PREP đổi video canary của intake.py (3) sang needs_* ⇒ phase 2 chọn video
    ok kế tiếp (4) làm canary; video 3 và 6 không có card nào."""
    preps = _approved({3: "needs_input", 4: "ok", 5: "ok", 6: "needs_rerender"})
    k = _by_key(make_cards.plan_cards(FAKE_MANIFEST, preps, rules_110, "videos"))
    assert k["vmh-4-intake-a1"]["parents"] == ["vmh-b01-approve-prep-1-a1"]
    assert k["vmh-b01-approve-canary-a1"]["parents"] == ["vmh-4-verify-a1"]
    assert k["vmh-5-intake-a1"]["parents"] == ["vmh-b01-approve-prep-1-a1", "vmh-b01-approve-canary-a1"]
    assert not any(c["video"] in (3, 6) for c in k.values())


def test_card_flags_follow_rules_budgets(rules_110):
    k = _by_key(make_cards.plan_cards(FAKE_MANIFEST, {}, rules_110, "prep")
                + make_cards.plan_cards(FAKE_MANIFEST, PREPS_OK, rules_110, "videos"))
    plan, verify, prep = k["vmh-4-plan-a1"], k["vmh-4-verify-a1"], k["vmh-b01-prep-1-a1"]
    assert plan["assignee"] == "opa-editor" and verify["assignee"] == "opa-verifier"
    assert plan["workspace"] == f"dir:{(paths.VID_ROOT / '4').as_posix()}"
    assert plan["skills"] == ["dung-video-talking-head"]
    b = rules_110.get("budgets.PLAN")
    assert (plan["runtime"], plan["retries"], plan["goal_turns"]) == (b["runtime"], b["retries"],
                                                                     b["goal_turns"])
    assert plan["model"] is None                            # a1 chạy model mặc định của profile
    assert kanban.parse_body(plan["body"]) == {
        "videos": [4], "stage": "PLAN", "prep_k": None, "ver": "1.1.0", "preset": "standard",
        "attempt": 1, "batch": "b01"}
    assert kanban.parse_body(prep["body"])["videos"] == [3, 4, 5, 6]
    assert kanban.parse_body(prep["body"])["prep_k"] == 1
    for key in ("vmh-b01-approve-prep-1-a1", "vmh-b01-approve-canary-a1"):   # R28
        a = k[key]
        assert a["assignee"] == "user" and a["initial_status"] is None
        assert a["runtime"] is None and a["retries"] is None and a["goal_turns"] == 0


def test_approved_prep_state_overrides_manifest_status(rules_110):
    preps = _approved({3: "ok", 4: "needs_input", 5: "ok", 6: "needs_rerender"})
    cards = make_cards.plan_cards(FAKE_MANIFEST, preps, rules_110, "videos")
    assert Counter(c["video"] for c in cards if c["video"] is not None) == {3: 4, 5: 4}


def test_dry_run_cli_prints_plan_and_creates_nothing(vid_root, monkeypatch, capsys):
    def boom(argv):
        raise AssertionError("dry-run không được gọi CLI")
    monkeypatch.setattr(kanban, "_run", boom)
    assert make_cards.main(["--batch", "b01", "--board", "vm-heygen-b01", "--dry-run"]) == 0
    out = capsys.readouterr().out
    assert out.count(kanban.HB) == 2                         # phase prep: PREP-1 + APPROVE-PREP-1
    assert not (paths.batch_dir("b01") / make_cards.REGISTRY).exists()
    assert make_cards.main(["--batch", "b01", "--board", "vm-heygen-b01", "--check"]) == 0
    assert "PASS" in capsys.readouterr().out


def test_check_fails_on_manifest_of_other_release(vid_root, capsys):
    bad = {**FAKE_MANIFEST, "rules_version": "9.9.9"}
    (paths.batch_dir("b01") / "batch_manifest.json").write_text(json.dumps(bad), encoding="utf-8")
    assert make_cards.main(["--batch", "b01", "--board", "vm-heygen-b01", "--check"]) == 1
    assert "9.9.9" in capsys.readouterr().out


def test_two_phase_real_run_then_registry(vid_root, monkeypatch, capsys, rules_110):
    """C1: phase prep tạo 2 card; phase videos (sau khi APPROVE-PREP complete) tạo 13 card theo
    phiếu đã duyệt; chạy lại không tạo thêm; sổ card ghi cha của từng card."""
    fake = _FakeCli()
    monkeypatch.setattr(kanban, "_run", fake)
    assert make_cards.main(["--batch", "b01", "--board", "vm-heygen-b01"]) == 0
    assert [_flag(a, "--idempotency-key")[0] for a in fake.creates()] == PREP_KEYS
    _write_prep({3: "ok", 4: "ok", 5: "ok", 6: "needs_rerender"})
    _approve_all(fake)
    assert make_cards.main(["--batch", "b01", "--board", "vm-heygen-b01", "--phase", "videos"]) == 0
    assert "canary: video 3" in capsys.readouterr().out
    creates = fake.creates()
    assert len(creates) == 15
    ids = {_flag(a, "--idempotency-key")[0]: f"t_{i:04d}" for i, a in enumerate(creates, 1)}
    intake4 = next(a for a in creates if _flag(a, "--idempotency-key") == ["vmh-4-intake-a1"])
    assert _flag(intake4, "--parent") == [ids["vmh-b01-approve-prep-1-a1"], ids["vmh-b01-approve-canary-a1"]]
    reg = _registry()
    assert reg["board"] == "vm-heygen-b01" and len(reg["cards"]) == 15
    assert reg["cards"]["vmh-b01-approve-canary-a1"]["parents"] == ["vmh-3-verify-a1"]
    for argv in creates:                                    # C2: --max-retries = retries + 1
        kind = reg["cards"][_flag(argv, "--idempotency-key")[0]]["kind"]
        want = [] if kind.startswith("APPROVE") else [str(rules_110.get(f"budgets.{kind}.retries") + 1)]
        assert _flag(argv, "--max-retries") == want, kind

    for phase in ("prep", "videos"):                        # chạy lại: không tạo thêm card nào
        assert make_cards.main(["--batch", "b01", "--board", "vm-heygen-b01", "--phase", phase]) == 0
        assert make_cards.main(["--batch", "b01", "--board", "vm-heygen-b01", "--phase", phase, "--check"]) == 0
    assert len(fake.creates()) == 15
    assert make_cards.main(["--batch", "b01", "--board", "vm-heygen-other"]) == 1


def test_phase_videos_real_run_uses_flipped_canary(vid_root, monkeypatch, capsys):
    """C1 (hồi quy qua CLI): phiếu duyệt đổi video 3 sang needs_input ⇒ canary là video 4."""
    fake = _FakeCli()
    monkeypatch.setattr(kanban, "_run", fake)
    assert make_cards.main(["--batch", "b01", "--board", "vm-heygen-b01"]) == 0
    _write_prep({3: "needs_input", 4: "ok", 5: "ok", 6: "needs_rerender"})
    _approve_all(fake)
    assert make_cards.main(["--batch", "b01", "--board", "vm-heygen-b01", "--phase", "videos"]) == 0
    assert "canary: video 4" in capsys.readouterr().out
    reg = _registry()
    assert reg["cards"]["vmh-b01-approve-canary-a1"]["parents"] == ["vmh-4-verify-a1"]
    assert not any(e["video"] in (3, 6) for e in reg["cards"].values())
    assert len(fake.creates()) == 2 + 9


def test_video_joining_after_phase_videos_keeps_registered_canary(vid_root, monkeypatch, capsys):
    """C1: video 3 (canary của intake.py) bị PREP đổi needs_rerender ⇒ canary 4; user render lại,
    phiếu duyệt đổi 3 về ok ⇒ chạy lại phase videos chỉ thêm chuỗi của 3 sau APPROVE-CANARY."""
    fake = _FakeCli()
    monkeypatch.setattr(kanban, "_run", fake)
    videos = ["--batch", "b01", "--board", "vm-heygen-b01", "--phase", "videos"]
    assert make_cards.main(["--batch", "b01", "--board", "vm-heygen-b01"]) == 0
    _write_prep({3: "needs_rerender", 4: "ok", 5: "ok", 6: "needs_rerender"})
    _approve_all(fake)
    assert make_cards.main(videos) == 0
    _write_prep({3: "ok", 4: "ok", 5: "ok", 6: "needs_rerender"})
    capsys.readouterr()
    assert make_cards.main(videos + ["--check"]) == 0 and "canary: video 4" in capsys.readouterr().out
    assert make_cards.main(videos) == 0
    reg = _registry()
    assert reg["cards"]["vmh-3-intake-a1"]["parents"] == ["vmh-b01-approve-prep-1-a1", "vmh-b01-approve-canary-a1"]
    assert len(fake.creates()) == 2 + 9 + 4


def test_phase_videos_needs_approved_prep_of_every_group(vid_root, monkeypatch, capsys):
    """C1: phase videos FAIL (không tạo card) khi chưa có phase prep, thiếu phiếu PREP đạt khuôn,
    hoặc APPROVE-PREP chưa complete trên board."""
    fake = _FakeCli()
    monkeypatch.setattr(kanban, "_run", fake)
    videos = ["--batch", "b01", "--board", "vm-heygen-b01", "--phase", "videos"]
    _write_prep({3: "ok", 4: "ok", 5: "ok", 6: "needs_rerender"})
    assert make_cards.main(videos) == 1                     # phase prep chưa chạy
    assert "approve-prep-1" in capsys.readouterr().out
    (paths.batch_dir("b01") / "prep" / "prep-1.json").unlink()
    assert make_cards.main(["--batch", "b01", "--board", "vm-heygen-b01"]) == 0
    capsys.readouterr()
    assert make_cards.main(videos) == 1                     # chưa có phiếu PREP-1
    assert "prep-1.json" in capsys.readouterr().out
    _write_prep({3: "ok", 4: "ok", 5: "ok"})                # phiếu thiếu video 6 của nhóm
    assert make_cards.main(videos + ["--check"]) == 1
    assert "[3, 4, 5, 6]" in capsys.readouterr().out
    _write_prep({3: "ok", 4: "ok", 5: "ok", 6: "needs_rerender"})
    todo = _registry()["cards"]["vmh-b01-approve-prep-1-a1"]["id"]
    fake.shows[todo] = {"task": {"id": todo, "status": "todo", "body": ""}}
    assert make_cards.main(videos) == 1                     # user chưa duyệt
    assert "APPROVE-PREP-1" in capsys.readouterr().out
    assert len(fake.creates()) == 2


def test_check_fails_when_registered_parents_differ(vid_root, monkeypatch, capsys):
    """C1: sau phase videos, phiếu duyệt đổi canary ⇒ --check FAIL vì cha đã tạo khác kế hoạch
    (thay vì PASS rồi deadlock lô như trước)."""
    fake = _FakeCli()
    monkeypatch.setattr(kanban, "_run", fake)
    assert make_cards.main(["--batch", "b01", "--board", "vm-heygen-b01"]) == 0
    _write_prep({3: "ok", 4: "ok", 5: "ok", 6: "needs_rerender"})
    _approve_all(fake)
    assert make_cards.main(["--batch", "b01", "--board", "vm-heygen-b01", "--phase", "videos"]) == 0
    _write_prep({3: "needs_input", 4: "ok", 5: "ok", 6: "needs_rerender"})
    capsys.readouterr()
    assert make_cards.main(["--batch", "b01", "--board", "vm-heygen-b01", "--phase", "videos", "--check"]) == 1
    out = capsys.readouterr().out
    assert "vmh-b01-approve-canary-a1" in out and "vmh-3-verify-a1" in out


def test_retry_plan_creates_a2_chain_with_strong_model(vid_root, monkeypatch, capsys, rules_110):
    fake = _FakeCli()
    monkeypatch.setattr(kanban, "_run", fake)
    assert make_cards.main(["--batch", "b01", "--board", "vm-heygen-b01"]) == 0
    _write_prep({3: "ok", 4: "ok", 5: "ok", 6: "needs_rerender"})
    _approve_all(fake)
    assert make_cards.main(["--batch", "b01", "--board", "vm-heygen-b01", "--phase", "videos"]) == 0
    old = {key: e["id"] for key, e in _registry()["cards"].items()}
    capsys.readouterr()

    assert make_cards.main(["--batch", "b01", "--board", "vm-heygen-b01", "--retry", "3:PLAN"]) == 0
    new = fake.creates()[15:]
    keys = [_flag(a, "--idempotency-key")[0] for a in new]
    assert keys == ["vmh-3-plan-a2", "vmh-3-build-a2", "vmh-3-verify-a2"]
    assert _flag(new[0], "--model") == [rules_110.get("models.plan_a2")]
    assert _flag(new[1], "--model") == []
    assert _flag(new[0], "--parent") == [old["vmh-3-intake-a1"]]
    assert _flag(new[1], "--parent") == ["t_0016"] and _flag(new[2], "--parent") == ["t_0017"]
    assert kanban.parse_body(_flag(new[0], "--body")[0])["attempt"] == 2
    out = capsys.readouterr().out
    for key in ("vmh-3-plan-a1", "vmh-3-build-a1", "vmh-3-verify-a1"):   # việc của operator
        assert old[key] in out
    assert f"link t_0018 {old['vmh-b01-approve-canary-a1']}" in out    # canary: nối lại card duyệt
    assert _registry()["cards"]["vmh-3-plan-a2"]["parents"] == ["vmh-3-intake-a1"]
    for argv in fake.creates():                             # R43: không card nào ở goal mode (prep, videos, retry)
        assert "--goal" not in argv and "--goal-max-turns" not in argv, _flag(argv, "--idempotency-key")


# ------------------------------------------------------------------ R44: board có sẵn, in VID_ROOT


def test_real_run_fails_with_create_command_when_board_missing(vid_root, monkeypatch, capsys):
    """R44 (MF-3): chạy thật hỏi `hermes kanban boards list --json` trước tiên; board chưa có ⇒
    FAIL in đúng lệnh tạo board, không tạo card, không ghi sổ."""
    fake = _FakeCli()
    fake.boards = ["default", "vm-heygen-1"]
    monkeypatch.setattr(kanban, "_run", fake)
    assert make_cards.main(["--batch", "b01", "--board", "vm-heygen-b01"]) == 1
    out = capsys.readouterr().out
    assert 'hermes kanban boards create vm-heygen-b01 --name "Van Minh AI · HeyGen b01"' in out
    assert fake.calls == [[kanban.HB, "kanban", "boards", "list", "--json"]]
    assert not (paths.batch_dir("b01") / make_cards.REGISTRY).exists()


def test_real_run_prints_vid_root_and_checks_board_first(vid_root, monkeypatch, capsys):
    """R44 (FS-9): chạy thật in `VID_ROOT: <paths.VID_ROOT>`; lệnh Hermes đầu tiên là boards list."""
    fake = _FakeCli()
    monkeypatch.setattr(kanban, "_run", fake)
    assert make_cards.main(["--batch", "b01", "--board", "vm-heygen-b01"]) == 0
    assert f"VID_ROOT: {vid_root.as_posix()}" in capsys.readouterr().out
    assert fake.calls[0][2:] == ["boards", "list", "--json"] and len(fake.creates()) == 2


def test_check_and_dry_run_never_ask_hermes_for_boards(vid_root, capsys):
    """--check / --dry-run vẫn không gọi Hermes (fixture autouse cấm CLI) và không in VID_ROOT."""
    assert make_cards.main(["--batch", "b01", "--board", "vm-heygen-b01", "--check"]) == 0
    assert make_cards.main(["--batch", "b01", "--board", "vm-heygen-b01", "--dry-run"]) == 0
    assert "VID_ROOT:" not in capsys.readouterr().out



# ------------------------------------------------------------------ R48 FS-11: thứ tự việc của --retry


def _operator_steps(out: str) -> list[str]:
    return [ln.strip()[2:] for ln in out.splitlines() if ln.startswith("  - ")]


def _videos_ready(fake):
    assert make_cards.main(["--batch", "b01", "--board", "vm-heygen-b01"]) == 0
    _write_prep({3: "ok", 4: "ok", 5: "ok", 6: "needs_rerender"})
    _approve_all(fake)
    assert make_cards.main(["--batch", "b01", "--board", "vm-heygen-b01", "--phase", "videos"]) == 0
    return {key: e["id"] for key, e in _registry()["cards"].items()}


def test_retry_relinks_approval_before_archiving_in_reverse_order(vid_root, monkeypatch, capsys):
    """FS-11: card duyệt luôn có cha chưa xong — link card mới → unlink card cũ → archive card cũ từ
    cuối chuỗi về đầu (archive trước sẽ thả APPROVE-CANARY / card con cũ sang ready)."""
    fake = _FakeCli()
    monkeypatch.setattr(kanban, "_run", fake)
    old = _videos_ready(fake)
    capsys.readouterr()
    assert make_cards.main(["--batch", "b01", "--board", "vm-heygen-b01", "--retry", "3:INTAKE"]) == 0
    steps = _operator_steps(capsys.readouterr().out)
    hb, approve = "hermes kanban --board vm-heygen-b01", old["vmh-b01-approve-canary-a1"]
    new_verify = _registry()["cards"]["vmh-3-verify-a2"]["id"]
    chain = [old[f"vmh-3-{s}-a1"] for s in ("intake", "plan", "build", "verify")]
    assert len(steps) == 3
    assert steps[0].endswith(f"{hb} link {new_verify} {approve}")
    assert steps[1].endswith(f"{hb} unlink {chain[-1]} {approve}")
    assert steps[2].endswith(f"{hb} archive {' '.join(reversed(chain))}")


def test_retry_without_approval_card_only_archives_in_reverse(vid_root, monkeypatch, capsys):
    fake = _FakeCli()
    monkeypatch.setattr(kanban, "_run", fake)
    old = _videos_ready(fake)
    capsys.readouterr()
    assert make_cards.main(["--batch", "b01", "--board", "vm-heygen-b01", "--retry", "4:PLAN"]) == 0
    steps = _operator_steps(capsys.readouterr().out)
    chain = [old[f"vmh-4-{s}-a1"] for s in ("plan", "build", "verify")]
    assert steps == [f"archive card cũ (từ cuối chuỗi về đầu): hermes kanban --board vm-heygen-b01 archive "
                     f"{' '.join(reversed(chain))}"]


# ------------------------------------------------------------------ R48 FS-9: biến môi trường lái lệch


def test_run_drops_pinned_kanban_db_when_board_is_given(monkeypatch):
    """FS-9: HERMES_KANBAN_DB (dispatcher gắn cho worker) đè --board trong Hermes ⇒ lệnh có --board
    chạy với env không có HERMES_KANBAN_DB / HERMES_KANBAN_WORKSPACES_ROOT; lệnh không --board giữ nguyên."""
    seen = []
    monkeypatch.setattr(kanban.subprocess, "run", lambda argv, **kw: seen.append(kw["env"]) or _Proc("{}"))
    monkeypatch.setenv("HERMES_KANBAN_DB", "X:/worker-board/kanban.db")
    monkeypatch.setenv("HERMES_KANBAN_WORKSPACES_ROOT", "X:/worker-board/workspaces")
    monkeypatch.setenv("HERMES_KANBAN_BOARD", "vm-heygen-b01")
    _REAL_RUN([kanban.HB, "kanban", "--board", "vm-heygen-b01", "show", "t_1", "--json"])
    _REAL_RUN([kanban.HB, "kanban", "boards", "list", "--json"])
    with_board, without_board = seen
    assert "HERMES_KANBAN_DB" not in with_board and "HERMES_KANBAN_WORKSPACES_ROOT" not in with_board
    assert with_board["HERMES_KANBAN_BOARD"] == "vm-heygen-b01" and with_board["PYTHONIOENCODING"] == "utf-8"
    assert without_board["HERMES_KANBAN_DB"] == "X:/worker-board/kanban.db"


def test_real_run_refuses_th_vid_root_unless_allowed(vid_root, monkeypatch, capsys):
    """FS-9: TH_VID_ROOT còn sót trong shell ⇒ card thật trỏ workspace/sổ card vào bản nháp; chạy thật
    FAIL (không gọi Hermes) trừ khi có --allow-th-vid-root. --check không bị ảnh hưởng."""
    fake = _FakeCli()
    monkeypatch.setattr(kanban, "_run", fake)
    monkeypatch.setenv("TH_VID_ROOT", str(vid_root))
    base = ["--batch", "b01", "--board", "vm-heygen-b01"]
    assert make_cards.main(base) == 1
    out = capsys.readouterr().out
    assert "TH_VID_ROOT" in out and "--allow-th-vid-root" in out and fake.calls == []
    assert make_cards.main(base + ["--check"]) == 0
    assert make_cards.main(base + ["--allow-th-vid-root"]) == 0
    assert len(fake.creates()) == 2
