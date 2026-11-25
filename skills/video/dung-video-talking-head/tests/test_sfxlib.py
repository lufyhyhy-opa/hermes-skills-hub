# tests/test_sfxlib.py — nhập/đo/kiểm 11 file SFX đã cấp phép (Task 6).
# Xem sfx_manifest.json contract & ràng buộc family trong contracts-and-fixtures.md.
import json

from thlib import rules, sfxlib


def test_manifest_has_10_licensed_files():
    m = sfxlib.load_manifest("1.1.0")["files"]
    assert len(m) == 11  # 10 âm khác nhau; transition-snap có mặt ở cả whoosh và air
    for k, v in m.items():
        assert v["source_url"].startswith("https://") and v["license"]


def test_every_listed_file_passes_its_family():
    R = rules.load("1.1.0")
    m = sfxlib.load_manifest("1.1.0")["files"]
    for fam, keys in R.get("sfx.family_files").items():
        for k in keys:
            ok, why = sfxlib.role_ok(m[k], fam, R)
            assert ok, (k, why)


def test_excluded_files_fail():
    # Đường dẫn worktree (không phải shared-skills sống) theo phán quyết controller.
    R = rules.load("1.1.0")
    bass = sfxlib.measure(sfxlib.prepare("legacy/1.0.0/assets/sfx/impact/bass-hit-short.mp3"))
    assert not sfxlib.role_ok(bass, "impact", R)[0]
    pop = sfxlib.measure(sfxlib.prepare("legacy/1.0.0/assets/sfx/ui/pop-electric.mp3"))
    assert not sfxlib.role_ok(pop, "impact", R)[0]


def test_measurements_match_prototype():
    proto = json.load(open(
        r"D:/MMO/Van Minh AI/docs/specs/2026-09-11-rulebook-evidence/prototype/files_v11.json",
        encoding="utf-8",
    ))
    m = sfxlib.load_manifest("1.1.0")["files"]
    assert abs(m["impact/hit-blow"]["attack20_ms"] - proto["pack:impact/hit-blow.mp3"]["attack20_ms"]) <= 2
