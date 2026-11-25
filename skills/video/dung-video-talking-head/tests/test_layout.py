# tests/test_layout.py — C9 (Ruling R36): gốc skill không lộ tài liệu 1.0.0 cho worker Hermes.
# Hermes liệt kê "supporting files" của skill trong prompt mọi worker từ đúng bốn thư mục ở gốc
# skill: references/ (*.md), templates/ (đệ quy), assets/ (đệ quy), scripts/ (*.py, *.sh, …) —
# hermes-agent tools/skills_tool.py _LINKED_FILE_SPECS, và agent/skill_commands.py
# _supporting_files đi đĩa đúng bốn tên đó khi danh sách rỗng. Đồng thời agent/skill_utils.py
# iter_skill_index_files quét mọi thư mục con tìm SKILL.md (mỗi file là một skill riêng).
# Kiểm trên file git theo dõi (bố cục thật sự được ship), không phụ thuộc rác build trên đĩa.
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HERMES_LISTED_DIRS = ("references", "templates", "assets", "scripts")
LEGACY = "legacy/1.0.0"


def _tracked() -> list[str]:
    out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, text=True,
                         encoding="utf-8", check=True).stdout
    return [p for p in out.split("\0") if p]


def test_no_tracked_file_under_a_hermes_listed_root_dir():
    exposed = [p for p in _tracked() if p.split("/", 1)[0] in HERMES_LISTED_DIRS]
    assert exposed == [], exposed


def test_1_0_0_material_lives_under_legacy():
    tracked = set(_tracked())
    for rel in ("references/edit-json.md", "references/style.md", "scripts/new_project.py",
                "assets/ATTRIBUTION.md", "assets/sfx/impact/hit-blow.mp3", "template/package.json",
                "template/src/Root.tsx", "examples/edit.json"):
        assert f"{LEGACY}/{rel}" in tracked, rel
    assert not any(p.split("/", 1)[0] in ("template", "examples") for p in tracked)


def test_dev_tools_live_in_a_dir_hermes_does_not_list():
    tracked = set(_tracked())
    assert {"tools/check_drift.py", "tools/make_manifest.py"} <= tracked


def test_the_root_skill_md_is_the_only_skill_md():
    assert [p for p in _tracked() if p.rsplit("/", 1)[-1] == "SKILL.md"] == ["SKILL.md"]


def test_import_sfx_pack_sources_resolve_under_legacy():
    """import_sfx.py đọc pack 1.0.0 ở legacy/1.0.0/assets: đủ file nguồn và dòng source_url."""
    import import_sfx
    pack = ROOT / LEGACY / "assets"
    for key, (origin, orig) in import_sfx.MAPPING.items():
        if origin == "pack":
            assert (pack / "sfx" / orig).is_file(), key
            assert import_sfx._find_source_url(pack / "ATTRIBUTION.md", Path(orig).name), key
