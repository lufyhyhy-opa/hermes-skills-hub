# tests/test_skill_md.py — Task 16: SKILL.md trở thành router ≤ 40 dòng cho
# 1.1.0; frontmatter name/description/triggers giữ nguyên so với 1.0.0 (tag
# `v1.0.0`), chỉ metadata.version đổi (spec §4.3, plan Task 16).
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_MD = ROOT / "SKILL.md"


def _frontmatter(text: str) -> str:
    return text.split("---", 2)[1]


def test_skill_md_is_at_most_40_lines():
    lines = SKILL_MD.read_text(encoding="utf-8").splitlines()
    assert len(lines) <= 40, f"SKILL.md dài {len(lines)} dòng, vượt 40"


def test_frontmatter_unchanged_from_1_0_0_except_version_bump():
    old = subprocess.run(
        ["git", "show", "v1.0.0:SKILL.md"], cwd=ROOT,
        capture_output=True, text=True, encoding="utf-8", check=True,
    ).stdout
    old_fm = _frontmatter(old)
    new_fm = _frontmatter(SKILL_MD.read_text(encoding="utf-8"))
    assert "version: 1.0.0" in old_fm
    assert new_fm == old_fm.replace("version: 1.0.0", "version: 1.1.0")


STAGE_CMD = 'python "${HERMES_SKILL_DIR}/releases/1.1.0/scripts/stage.py" STAGE --task ID'
EXAMPLE = 'python "${HERMES_SKILL_DIR}/releases/1.1.0/scripts/stage.py" PREP --task t_1a2b3c4d'
GUIDES = [ROOT / "releases" / "1.1.0" / "stages" / f"{g}.md" for g in ("PREP", "PLAN")]


def test_router_rule1_is_the_quoted_stage_command_with_task():
    """R48 FS-4 (R42): Hermes xoá $HERMES_KANBAN_TASK khỏi lệnh terminal của worker ⇒ lệnh đầu mang --task
    lấy từ câu "work kanban task <id>"; đường dẫn skill có dấu cách ⇒ trong ngoặc kép, qua
    ${HERMES_SKILL_DIR} (Hermes chỉ thay biến này trong SKILL.md); card PREP-<k> ⇒ stage PREP."""
    text = SKILL_MD.read_text(encoding="utf-8")
    rule1 = next(ln for ln in text.splitlines() if ln.startswith("1. "))
    assert STAGE_CMD in rule1 and EXAMPLE in rule1 and "`STAGE: PREP-1` ⇒ `PREP`" in rule1 and "`NEXT`" in rule1
    commands = [span for span in rule1.split("`")[1::2] if span.startswith("python ")]
    assert commands and not any(c in span for span in commands for c in "<>"), commands   # bash: < > là chuyển hướng
    assert '"--task"' in (ROOT / "releases" / "1.1.0" / "scripts" / "stage.py").read_text(encoding="utf-8")


def test_router_names_kanban_tools_guides_and_forbids_cli():
    text = SKILL_MD.read_text(encoding="utf-8")
    for need in ("`kanban_comment`", "`kanban_block`", "`kanban_complete`", "không dùng lệnh `hermes kanban`",
                 "`releases/<ver>/stages/PREP.md`", "`releases/<ver>/stages/PLAN.md`", "legacy/1.0.0"):
        assert need in text, need
    assert "git show" not in text and "<skill>" not in text


def test_stage_guides_point_at_next_not_a_path():
    """R48 FS-4: PREP.md/PLAN.md đọc bằng read_file (không thay ${HERMES_SKILL_DIR}) ⇒ không tự viết đường
    dẫn stage.py; dặn chạy đúng lệnh ở dòng NEXT và complete đúng như NEXT (FS-5)."""
    for guide in GUIDES:
        text = guide.read_text(encoding="utf-8")
        assert "<skill>" not in text and "HERMES_SKILL_DIR" not in text, guide.name
        assert "chạy đúng lệnh ở dòng NEXT" in text and "`kanban_complete`" in text, guide.name
