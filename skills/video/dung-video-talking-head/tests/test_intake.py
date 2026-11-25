# tests/test_intake.py — intake.py (P0) nhanh, chế độ cache: VID_ROOT tạm với mp4 giả, lời
# whisper lấy từ bản quét tests/fixtures/scan/video_v3_mapping.csv (không chạy whisper).
# C5: --all cần --allow-all, luôn loại batch.exclude_videos (D11), lô ≤ batch.max_videos.
# C6: lô đã có thì phải --update; --update chỉ đổi video được nêu, không đụng "## Lời duyệt".
import csv
import json
from pathlib import Path

import pytest

import intake
from thlib import paths

FIXTURES = Path(__file__).parent / "fixtures"
SCAN = FIXTURES / "scan" / "video_v3_mapping.csv"
VIDEOS = (1, 2, *range(3, 15), 16, 21, 27, 31)


@pytest.fixture
def vid_root(tmp_path, monkeypatch):
    root = tmp_path / "vid"
    for n in VIDEOS:
        (root / str(n)).mkdir(parents=True)
        (root / str(n) / f"{n}.mp4").write_bytes(b"x")
    monkeypatch.setattr(paths, "VID_ROOT", root)
    monkeypatch.setattr(paths, "DOCS_ROOT", FIXTURES / "scripts")
    return root


def _run(*args, cache=SCAN):
    return intake.main(["--batch", "b01", *args, "--transcriber", f"cache:{cache}"])


def _batch():
    return paths.batch_dir("b01")


def _manifest():
    return json.loads((_batch() / "batch_manifest.json").read_text(encoding="utf-8"))


def test_rules_exclude_delivered_videos(rules_110):
    """D11: video 1–2 đã giao, không dựng lại — nằm trong rules, có nguồn."""
    assert rules_110.get("batch.exclude_videos") == [1, 2]
    assert "D11" in rules_110.raw["sources"]["batch.exclude_videos"]["label"]


def test_all_needs_allow_all(vid_root, capsys):
    assert _run("--all") == 1
    assert "--allow-all" in capsys.readouterr().err
    assert not _batch().exists()


def test_allow_all_scans_everything_but_excluded(vid_root, capsys):
    """--all --allow-all (Gate 8 / dev): bỏ giới hạn số video nhưng vẫn loại video 1–2."""
    assert _run("--all", "--allow-all") == 0
    got = [v["n"] for v in _manifest()["videos"]]
    assert got == [n for n in VIDEOS if n not in (1, 2)] and len(got) > 10
    assert "1, 2" in capsys.readouterr().out


def test_excluded_videos_are_dropped_from_a_selection(vid_root, capsys):
    assert _run("--videos", "1,16,2,21") == 0
    assert [v["n"] for v in _manifest()["videos"]] == [16, 21]
    assert "batch.exclude_videos" in capsys.readouterr().out
    assert _run("--videos", "1,2", "--out", str(vid_root / "x")) == 1         # không còn video nào


def test_batch_size_is_capped_by_max_videos(vid_root, capsys, rules_110):
    cap = rules_110.get("batch.max_videos")
    too_many = ",".join(str(n) for n in range(3, 3 + cap + 1))
    assert _run("--videos", too_many) == 1
    assert f"batch.max_videos = {cap}" in capsys.readouterr().err
    assert not _batch().exists()
    assert _run("--videos", ",".join(str(n) for n in range(3, 3 + cap))) == 0
    assert len(_manifest()["videos"]) == cap


def _mapping_rows():
    with open(_batch() / "mapping.csv", encoding="utf-8-sig", newline="") as fh:
        return {int(r["video"].split()[0]): r for r in csv.DictReader(fh)}


def test_rerun_on_existing_batch_needs_update(vid_root, capsys):
    """C6: chạy lại intake trên lô đã có mà không --update ⇒ exit 1, không ghi đè gì."""
    assert _run("--videos", "16,21,31") == 0
    before = {p.name: p.read_bytes() for p in _batch().iterdir() if p.is_file()}
    capsys.readouterr()
    assert _run("--videos", "16") == 1
    assert "--update" in capsys.readouterr().err
    assert {p.name: p.read_bytes() for p in _batch().iterdir() if p.is_file()} == before


def test_update_changes_only_named_videos_and_keeps_approvals(vid_root, tmp_path):
    """C6: --update --videos 31 (video render lại) chỉ đổi mục 31 trong manifest, mapping.csv,
    vo_script; mục 16, 21 giữ nguyên; phần "## Lời duyệt" của APPROVALS.md giữ nguyên từng byte."""
    assert _run("--videos", "16,21,31") == 0
    approvals = _batch() / "APPROVALS.md"
    verbatim = "\n- 2026-09-12 PREP-1: \"ok hết, riêng video 31 để render lại\" (user)\n"
    approvals.write_text(approvals.read_text(encoding="utf-8") + verbatim, encoding="utf-8")
    tail = approvals.read_text(encoding="utf-8").split("## Lời duyệt", 1)[1]
    old = {v["n"]: v for v in _manifest()["videos"]}
    old_rows = _mapping_rows()

    rerendered = tmp_path / "rerendered.csv"                 # lời mới của video 31 sau khi render lại
    heard = "Tính năng ghi âm cuộc họp đang được chia sẻ khắp nơi. Nhưng SME có thật sự cần nó ngay không?"
    with open(rerendered, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["video", "heard"])
        w.writeheader()
        w.writerow({"video": "31", "heard": heard})
    assert _run("--update", "--videos", "31", cache=rerendered) == 0

    new = {v["n"]: v for v in _manifest()["videos"]}
    assert sorted(new) == [16, 21, 31]
    assert new[16] == old[16] and new[21] == old[21]
    assert new[31]["score"] != old[31]["score"]
    rows = _mapping_rows()
    assert rows[16] == old_rows[16] and rows[21] == old_rows[21] and rows[31]["heard"] == heard
    text = approvals.read_text(encoding="utf-8")
    assert text.split("## Lời duyệt", 1)[1] == tail and verbatim in text


def test_update_needs_existing_batch_and_named_videos(vid_root, capsys):
    assert _run("--update", "--videos", "16") == 1                            # chưa có lô
    assert not _batch().exists()
    assert _run("--videos", "16,21") == 0
    assert _run("--update", "--all", "--allow-all") == 1                      # --update chỉ với --videos


def test_update_never_adds_a_video_to_the_batch(vid_root, capsys):
    """C6: --update chỉ ghép lại video đã có trong lô — thêm video sẽ dời nhóm PREP-<k> của lô đã
    duyệt; video mới vào một lô sau."""
    assert _run("--videos", "16,21") == 0
    before = (_batch() / "batch_manifest.json").read_bytes()
    capsys.readouterr()
    assert _run("--update", "--videos", "21,27") == 1
    assert "27" in capsys.readouterr().err
    assert (_batch() / "batch_manifest.json").read_bytes() == before
