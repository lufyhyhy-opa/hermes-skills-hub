# tests/test_collect_kpi.py — collect_kpi.py (C8): operator gom out/verify/kpi.json của một lô vào
# _batches/<b>/kpi.jsonl (spec §10.4), in danh sách video phải gửi user duyệt (D5, §11.2) và, ở
# cuối lô, xoá node_modules của video đã VERIFIED / DONE_WITH_CONCERNS (§13.4). VID_ROOT tạm.
import json

import pytest

import collect_kpi
from thlib import paths


def _video(n, status="ok", canary=False, sample=False):
    return {"n": n, "status": status, "canary": canary, "sample": sample}


MANIFEST = {"batch": "b01", "rules_version": "1.1.0", "preset": "standard",
            "videos": [_video(3, canary=True), _video(4, sample=True), _video(5), _video(6, "needs_rerender"),
                       _video(7)]}
VERDICTS = {3: ("VERIFIED", False), 4: ("VERIFIED", False), 5: ("DONE_WITH_CONCERNS", True), 7: ("REJECTED", False)}


@pytest.fixture
def batch(tmp_path, monkeypatch):
    """Lô b01: canary 4 (PREP đổi 3 ⇒ chuỗi canary là của 4 trong cards.json), mẫu 4, video 5
    DONE_WITH_CONCERNS + claim_gate, 6 needs_rerender (không dựng), 7 REJECTED."""
    monkeypatch.setattr(paths, "VID_ROOT", tmp_path / "vid")
    b = paths.batch_dir("b01")
    b.mkdir(parents=True)
    (b / "batch_manifest.json").write_text(json.dumps(MANIFEST), encoding="utf-8")
    cards = {"vmh-4-verify-a1": {"id": "t_9", "kind": "VERIFY", "video": 4, "attempt": 1, "parents": []},
             "vmh-b01-approve-canary-a1": {"id": "t_10", "kind": "APPROVE-CANARY", "video": None, "attempt": 1,
                                           "parents": ["vmh-4-verify-a1"]}}
    (b / "cards.json").write_text(json.dumps({"board": "vm-heygen-b01", "cards": cards}), encoding="utf-8")
    for n, (verdict, claim) in VERDICTS.items():
        project = paths.project_dir(n, "1.1.0")
        (project / "out" / "verify").mkdir(parents=True)
        (project / "node_modules" / "remotion").mkdir(parents=True)
        (project / "meta.json").write_text(json.dumps({"video": n, "claim_gate": claim}), encoding="utf-8")
        kpi = {"video": n, "verdict": verdict, "owner_stage": "PLAN" if verdict == "REJECTED" else None,
               "checks_ok": 7, "checks_total": 7, "fail_ids": [], "concerns": [], "guess_count": 0,
               "script_match": 0.97}
        (project / "out" / "verify" / "kpi.json").write_text(json.dumps(kpi), encoding="utf-8")
    return b


def _lines(b):
    return [json.loads(ln) for ln in (b / "kpi.jsonl").read_text(encoding="utf-8").splitlines()]


def test_collects_kpi_lines_with_review_flags(batch, capsys):
    assert collect_kpi.main(["--batch", "b01"]) == 0
    lines = _lines(batch)
    assert [ln["video"] for ln in lines] == [3, 4, 5, 7]
    by = {ln["video"]: ln for ln in lines}
    assert by[4]["canary"] and by[4]["sample"] and not by[3]["canary"]    # canary = chuỗi trong cards.json
    assert by[5]["claim_gate"] and by[5]["verdict"] == "DONE_WITH_CONCERNS"
    assert all(ln["batch"] == "b01" for ln in lines)
    out = capsys.readouterr().out
    review = [ln for ln in out.splitlines() if ln.startswith("GỬI USER")]
    assert [ln.split()[3] for ln in review] == ["4", "5"]                  # "GỬI USER: video <n> …"
    final5 = (paths.project_dir(5, "1.1.0") / "out" / "final.mp4").as_posix()
    assert any(final5 in ln and "claim_gate" in ln and "DONE_WITH_CONCERNS" in ln for ln in review)
    assert "video 6" in out and "video 7" in out                            # chưa VERIFY / REJECTED

    assert collect_kpi.main(["--batch", "b01"]) == 0                        # chạy lại: ghi đè, không nhân đôi
    assert len(_lines(batch)) == 4


def test_prune_node_modules_only_for_finished_videos(batch):
    assert collect_kpi.main(["--batch", "b01", "--prune-node-modules"]) == 0
    for n in (3, 4, 5):
        assert not (paths.project_dir(n, "1.1.0") / "node_modules").exists()
        assert (paths.project_dir(n, "1.1.0") / "out" / "verify" / "kpi.json").is_file()
    assert (paths.project_dir(7, "1.1.0") / "node_modules").is_dir()         # REJECTED còn dựng lại


def test_missing_manifest_fails(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(paths, "VID_ROOT", tmp_path)
    assert collect_kpi.main(["--batch", "b09"]) == 1
    assert "batch_manifest.json" in capsys.readouterr().out
