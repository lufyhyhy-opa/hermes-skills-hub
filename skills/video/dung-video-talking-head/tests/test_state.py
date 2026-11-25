import json
from pathlib import Path

from thlib import state


def test_lock_roundtrip(tmp_path):
    lock = state.write_lock(tmp_path, "1.1.0")
    assert lock["version"] == "1.1.0" and lock["skill"] == "dung-video-talking-head"
    assert state.read_lock(tmp_path) == lock


def test_append_state_is_append_only(tmp_path):
    f = tmp_path / "a.json"
    f.write_text("{}", encoding="utf-8")
    state.write_lock(tmp_path, "1.1.0")
    r1 = state.append_state(tmp_path, "INTAKE", "t_1", "1", "opa-editor", [f])
    r2 = state.append_state(tmp_path, "PLAN", "t_2", "1", "opa-editor", [f])
    rows = state.read_state(tmp_path)
    assert [r["stage"] for r in rows] == ["INTAKE", "PLAN"]
    assert rows[0]["files"]["a.json"] == state.sha8(f)
    assert r1 != r2


def test_sha8_changes_with_content(tmp_path):
    f = tmp_path / "x"
    f.write_text("1")
    a = state.sha8(f)
    f.write_text("2")
    assert state.sha8(f) != a
