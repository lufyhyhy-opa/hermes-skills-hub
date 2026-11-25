# tests/test_check_drift.py — Task 15: check_drift.py (M0, spec §13.1), chỉ đọc.
# Cây Hermes giả dựng trong tmp_path (không đụng cây Hermes thật); một cây PASS
# cả 9 mục và một cây FAIL cả 9 mục, cộng vài lát cắt riêng cho các trường hợp
# biên (loại trừ _superseded/, glob "**" khớp cả cấp 0, và đọc YAML khi thiếu
# PyYAML). C11: mục 7 (con trỏ SOUL.md, §13.1 mục 2) và mục 8 (card t_81a309b2 +
# board vm-heygen-1 đã archive, §13.1 mục 4) — Hermes CLI luôn là bản giả
# (fixture autouse), không test nào gọi hermes.exe thật.
import json
from pathlib import Path
from textwrap import dedent

import pytest

import check_drift

CODES = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
BANNER = ("⚠ A previous `hermes update` was interrupted mid-install — gateways may be stale.\n"
          "   Run `hermes update` again to finish.\n")
SKILL_DIR = "C:/Users/Minh PC/AppData/Local/hermes/shared-skills/video/dung-video-talking-head"
# R46: đúng hai dòng controller sẽ thêm vào SOUL.md (bản gốc có phiên bản ở OPERATOR.md §M0).
SOUL_LINE_WORKER = (
    'dung-video-talking-head@1.1 — card có dòng "RULES: dung-video-talking-head@<ver>": chỉ làm theo '
    f"{SKILL_DIR}/SKILL.md và dòng NEXT của stage.py; các quy trình riêng trong SOUL này KHÔNG áp dụng "
    "cho card đó (không tự render, không tự chấm thêm, summary/metadata đúng như dòng NEXT của stage.py dặn, REJECTED thì "
    "kanban_block đúng như NEXT).")
SOUL_LINE_OPERATOR = (
    f"dung-video-talking-head@1.1 — lô vm-heygen-*: chỉ làm theo {SKILL_DIR}/releases/1.1.0/stages/OPERATOR.md; "
    "task packet và quy trình riêng trong SOUL này KHÔNG áp dụng cho các lô đó.")
SOUL_OK = {
    "opa-operator": f"## Video talking-head\n{SOUL_LINE_OPERATOR}\n",
    "opa-editor": f"## Card video\n{SOUL_LINE_WORKER}\n",
    "opa-verifier": f"## Card VERIFY\n{SOUL_LINE_WORKER}\n",
}


class FakeHermes:
    """`hermes kanban …` giả: board vm-heygen-1 ('gone' = đã `boards rm`, 'flag' = board.json
    archived, 'active') và trạng thái card t_81a309b2; ghi lại mọi lệnh đã gọi."""

    def __init__(self, board="gone", card="archived", banner=True):
        self.board, self.card, self.banner, self.calls = board, card, banner, []

    def __call__(self, root, args):
        self.calls.append(list(args))
        head = BANNER if self.banner else ""
        if args[:2] == ["boards", "list"]:
            boards = [{"slug": "default", "archived": False}, {"slug": "vm-heygen-b01", "archived": False}]
            if self.board != "gone":
                boards.append({"slug": "vm-heygen-1", "archived": self.board == "flag"})
            return 0, head + json.dumps(boards, indent=2)
        if args[:3] == ["--board", "vm-heygen-1", "show"]:
            if self.board == "gone":
                return 1, "kanban: board 'vm-heygen-1' does not exist."
            return 0, head + json.dumps({"task": {"id": "t_81a309b2", "status": self.card}}, indent=2)
        raise AssertionError(f"lệnh hermes ngoài dự kiến: {args}")


@pytest.fixture(autouse=True)
def fake_hermes(monkeypatch):
    fake = FakeHermes()
    monkeypatch.setattr(check_drift, "_run_hermes", fake, raising=False)
    return fake


class FakeGit:
    """`git status --porcelain` giả của thư mục skill đang dùng (mục 9); ghi lại thư mục đã hỏi."""

    def __init__(self, code=0, out=""):
        self.code, self.out, self.dirs = code, out, []

    def __call__(self, skill_dir):
        self.dirs.append(Path(skill_dir))
        return self.code, self.out


@pytest.fixture(autouse=True)
def fake_git(monkeypatch):
    fake = FakeGit()
    monkeypatch.setattr(check_drift, "_run_git", fake, raising=False)
    return fake

OPERATOR_CONFIG_OK = dedent("""\
    kanban:
      dispatch_in_gateway: true
      max_in_progress_per_profile: 1
      auto_decompose: true
    command_allowlist:
      - script execution via heredoc
      - access to Hermes secrets (Windows path)
    """)

# R44: config GỐC (<hermes-root>/config.yaml) — gateway gốc giữ dispatcher đọc kanban.* từ đây.
ROOT_CONFIG_OK = dedent("""\
    kanban:
      dispatch_in_gateway: true
      max_in_progress_per_profile: 1
      auto_decompose: true
    """)

ROOT_CONFIG_DRIFTED = dedent("""\
    kanban:
      dispatch_in_gateway: true
      auto_decompose: true
    """)

OPERATOR_CONFIG_DRIFTED = dedent("""\
    kanban:
      dispatch_in_gateway: true
      auto_decompose: true
    command_allowlist:
      - script execution via heredoc
      - access to Hermes secrets (Windows path)
      - execute_code
      - script execution via -e/-c flag
    """)


def _aux_config(enabled: bool) -> str:
    return dedent(f"""\
        auxiliary:
          vision:
            provider: xiaomi
          background_review:
            enabled: {"true" if enabled else "false"}
        """)


def _aux_config_no_background_review() -> str:
    return dedent("""\
        auxiliary:
          vision:
            provider: xiaomi
        """)


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _build_passing_tree(root: Path) -> None:
    staging = root / "profiles" / "opa-operator" / "staging"
    _write(staging / "note.md", "ghi chú bình thường, không nhắc luật cũ.\n")
    # DUCK_DB cũ vẫn còn nhưng đã bị dọn vào _superseded/ nên không tính.
    _write(staging / "_superseded" / "PACKET-old.md", "0.82 và DUCK_DB 1.0 (đã deprecated)\n")

    _write(root / "config.yaml", ROOT_CONFIG_OK)
    _write(root / "profiles" / "opa-operator" / "config.yaml", OPERATOR_CONFIG_OK)
    _write(root / "profiles" / "opa-editor" / "config.yaml", _aux_config(False))
    _write(root / "profiles" / "opa-verifier" / "config.yaml", _aux_config(False))
    # sfx.md của remotion-best-practices đã bị xoá -> không tạo file này.
    for profile, text in SOUL_OK.items():
        _write(root / "profiles" / profile / "SOUL.md", text)
    (root / check_drift.LIVE_SKILL).mkdir(parents=True)     # mục 9: thư mục skill đang dùng


def _build_failing_tree(root: Path) -> None:
    staging = root / "profiles" / "opa-operator" / "staging"
    _write(staging / "PACKET-vm-heygen-1.md", "OUTPUT_AUDIO_OFFSET và DUCK_DB 1.0 cũ\n")

    skill_dir = (root / "profiles" / "opa-operator" / "skills" / "claude-import"
                 / "dung-video-talking-head")
    skill_dir.mkdir(parents=True)

    _write(root / "config.yaml", ROOT_CONFIG_DRIFTED)
    _write(root / "profiles" / "opa-operator" / "config.yaml", OPERATOR_CONFIG_DRIFTED)
    _write(root / "profiles" / "opa-editor" / "config.yaml", _aux_config(True))
    _write(root / "profiles" / "opa-verifier" / "config.yaml", _aux_config_no_background_review())

    sfx_md = (root / "profiles" / "opa-operator" / "skills" / "claude-import"
              / "remotion-best-practices" / "rules" / "sfx.md")
    _write(sfx_md, "luật sfx cũ, đáng lẽ đã bị xoá\n")
    # SOUL.md: operator còn mẫu packet tự do, editor chưa có con trỏ, verifier thiếu hẳn file.
    _write(root / "profiles" / "opa-operator" / "SOUL.md", "## Packet\nDán số DUCK_DB vào packet.\n")
    _write(root / "profiles" / "opa-editor" / "SOUL.md", "## Editor\nTự viết edit.json.\n")


def test_passing_tree_all_pass(tmp_path):
    _build_passing_tree(tmp_path)
    results = check_drift.check_drift(tmp_path)
    assert [r["code"] for r in results] == CODES
    assert all(r["ok"] for r in results), results


def test_failing_tree_all_fail(tmp_path, fake_hermes, fake_git):
    _build_failing_tree(tmp_path)
    fake_hermes.board, fake_hermes.card = "active", "todo"
    (tmp_path / check_drift.LIVE_SKILL).mkdir(parents=True)
    fake_git.out = " M SKILL.md\n"
    results = check_drift.check_drift(tmp_path)
    assert [r["code"] for r in results] == CODES
    assert not any(r["ok"] for r in results), results
    by_code = {r["code"]: r for r in results}
    assert "PACKET-vm-heygen-1.md" in by_code["1"]["msg"]
    assert "dung-video-talking-head" in by_code["2"]["msg"]
    assert "1" not in by_code["3"]["msg"].split("=")[1][:2]  # max_ipp None, không phải 1
    assert "opa-editor" in by_code["4"]["msg"] and "opa-verifier" in by_code["4"]["msg"]
    assert "execute_code" in by_code["5"]["msg"] and "-e/-c" in by_code["5"]["msg"]
    assert "sfx.md" in by_code["6"]["msg"]
    assert all(p in by_code["7"]["msg"] for p in ("opa-operator", "opa-editor", "opa-verifier"))
    assert "vm-heygen-1" in by_code["8"]["msg"] and "todo" in by_code["8"]["msg"]
    assert "SKILL.md" in by_code["9"]["msg"]


def _item(root, code):
    return {r["code"]: r for r in check_drift.check_drift(root)}[code]


# ------------------------------------------------ mục 3: config gốc (R44)


def test_check3_reads_root_config_not_the_operator_copy(tmp_path):
    """R44 (MF-2): dispatcher là singleton của gateway gốc, đọc kanban.* từ <hermes-root>/config.yaml
    — mục 3 chấm config đó; bản trong opa-operator chỉ in để tham khảo, không đổi PASS/FAIL."""
    _build_passing_tree(tmp_path)
    _write(tmp_path / "profiles" / "opa-operator" / "config.yaml", OPERATOR_CONFIG_DRIFTED)
    result = _item(tmp_path, "3")
    assert result["ok"], result
    assert "config.yaml" in result["msg"] and "opa-operator" in result["msg"]
    _write(tmp_path / "config.yaml", ROOT_CONFIG_DRIFTED)
    _write(tmp_path / "profiles" / "opa-operator" / "config.yaml", OPERATOR_CONFIG_OK)
    assert not _item(tmp_path, "3")["ok"]


def test_check3_auto_decompose_must_stay_on_in_root_config(tmp_path):
    _build_passing_tree(tmp_path)
    _write(tmp_path / "config.yaml", ROOT_CONFIG_OK.replace("auto_decompose: true", "auto_decompose: false"))
    result = _item(tmp_path, "3")
    assert not result["ok"] and "auto_decompose=False" in result["msg"]


def test_check3_missing_root_config_fails(tmp_path):
    _build_passing_tree(tmp_path)
    (tmp_path / "config.yaml").unlink()
    result = _item(tmp_path, "3")
    assert not result["ok"] and "config.yaml" in result["msg"]


# ------------------------------------------------ mục 7: con trỏ SOUL.md (§13.1 mục 2)


@pytest.mark.parametrize("profile, text, needle", [
    ("opa-operator", f"đọc {SKILL_DIR}/releases/1.1.0/stages/OPERATOR.md\n", "dung-video-talking-head@1.1"),
    ("opa-operator", f"dung-video-talking-head@1.1 — đọc {SKILL_DIR}/SKILL.md\n", "OPERATOR.md"),
    ("opa-editor", "dung-video-talking-head@1.1 — xem SKILL.md của skill\n", "SKILL.md"),
    ("opa-verifier", f"dung-video-talking-head@1.0 — {SKILL_DIR}/SKILL.md\n", "dung-video-talking-head@1.1"),
])
def test_check7_needs_marker_and_skill_path(tmp_path, profile, text, needle):
    """Mỗi SOUL.md cần cả dấu `dung-video-talking-head@1.1` lẫn đường dẫn trong thư mục skill:
    operator → releases/<ver>/stages/OPERATOR.md, editor/verifier → SKILL.md."""
    _build_passing_tree(tmp_path)
    _write(tmp_path / "profiles" / profile / "SOUL.md", text)
    result = _item(tmp_path, "7")
    assert not result["ok"] and profile in result["msg"] and needle in result["msg"]


def test_check7_accepts_windows_paths_and_later_patch_versions(tmp_path):
    _build_passing_tree(tmp_path)
    win = SKILL_DIR.replace("/", "\\")
    _write(tmp_path / "profiles" / "opa-operator" / "SOUL.md",
           f"dung-video-talking-head@1.1.1: {win}\\releases\\<ver>\\stages\\OPERATOR.md — SOUL KHÔNG áp dụng\n")
    _write(tmp_path / "profiles" / "opa-editor" / "SOUL.md",
           f"dung-video-talking-head@1.1.1 {win}\\SKILL.md — SOUL KHÔNG áp dụng\n")
    assert _item(tmp_path, "7")["ok"]


def test_check7_needs_precedence_phrase(tmp_path):
    """R46 (MF-6): con trỏ phải nói nó đè quy trình riêng của SOUL — thiếu `KHÔNG áp dụng` ⇒ FAIL."""
    _build_passing_tree(tmp_path)
    _write(tmp_path / "profiles" / "opa-editor" / "SOUL.md",
           f"dung-video-talking-head@1.1 — đọc {SKILL_DIR}/SKILL.md, lệnh đầu là stage.py\n")
    result = _item(tmp_path, "7")
    assert not result["ok"] and "opa-editor" in result["msg"] and "KHÔNG áp dụng" in result["msg"]


def test_check7_marker_path_and_phrase_must_share_one_line(tmp_path):
    _build_passing_tree(tmp_path)
    _write(tmp_path / "profiles" / "opa-verifier" / "SOUL.md",
           f"dung-video-talking-head@1.1 — đọc {SKILL_DIR}/SKILL.md\n§9 KHÔNG áp dụng cho card đó.\n")
    result = _item(tmp_path, "7")
    assert not result["ok"] and "opa-verifier" in result["msg"] and "một dòng" in result["msg"]


def test_operator_md_m0_holds_the_exact_soul_lines(tmp_path):
    """R46: hai dòng SOUL nằm nguyên văn ở OPERATOR.md §M0 (có phiên bản) và chính chúng đạt mục 7."""
    from thlib import paths
    text = (paths.release_dir("1.1.0") / "stages" / "OPERATOR.md").read_text(encoding="utf-8")
    m0 = text[text.index("## M0"):]
    assert SOUL_LINE_WORKER in m0 and SOUL_LINE_OPERATOR in m0
    _build_passing_tree(tmp_path)
    assert _item(tmp_path, "7")["ok"]


def test_check7_missing_soul_file_fails(tmp_path):
    _build_passing_tree(tmp_path)
    (tmp_path / "profiles" / "opa-verifier" / "SOUL.md").unlink()
    result = _item(tmp_path, "7")
    assert not result["ok"] and "opa-verifier" in result["msg"] and "SOUL.md" in result["msg"]


# ------------------------------------------------ mục 8: card + board đã archive (§13.1 mục 4)


def test_check8_board_removed_to_archive_passes_without_show(tmp_path, fake_hermes):
    """`hermes kanban boards rm vm-heygen-1` chuyển board vào kanban/boards/_archived/ — board biến
    khỏi `boards list --all` và card archive theo board; không gọi `show` lên board không còn."""
    result = _item(tmp_path, "8")
    assert result["ok"], result
    assert fake_hermes.calls == [["boards", "list", "--all", "--json"]]


def test_check8_flagged_board_needs_archived_card(tmp_path, fake_hermes):
    fake_hermes.board = "flag"
    assert _item(tmp_path, "8")["ok"]
    assert ["--board", "vm-heygen-1", "show", "t_81a309b2", "--json"] in fake_hermes.calls
    fake_hermes.card = "blocked"
    result = _item(tmp_path, "8")
    assert not result["ok"] and "t_81a309b2" in result["msg"] and "blocked" in result["msg"]


def test_check8_active_board_fails_even_with_archived_card(tmp_path, fake_hermes):
    fake_hermes.board = "active"
    result = _item(tmp_path, "8")
    assert not result["ok"] and "vm-heygen-1" in result["msg"]


def test_check8_parses_json_without_banner_too(tmp_path, fake_hermes):
    fake_hermes.board, fake_hermes.banner = "flag", False
    assert _item(tmp_path, "8")["ok"]


def test_check8_cli_error_fails_with_its_text(tmp_path, monkeypatch):
    monkeypatch.setattr(check_drift, "_run_hermes", lambda root, args: (1, "kanban: database is locked"))
    result = _item(tmp_path, "8")
    assert not result["ok"] and "database is locked" in result["msg"]


def test_check8_missing_hermes_exe_fails_without_running_anything(tmp_path, monkeypatch):
    monkeypatch.undo()                                   # _run_hermes thật: tmp_path không có hermes.exe
    result = _item(tmp_path, "8")
    assert not result["ok"] and "hermes.exe" in result["msg"]


# ------------------------------------------------ mục 9: thư mục skill đang dùng sạch (FS-8)


def test_check9_dirty_live_skill_fails(tmp_path, fake_git):
    """FS-8: worker sửa được skill đang dùng (skill_manage, tool file, terminal) và SKILL.md router không
    nằm trong MANIFEST ⇒ `git status --porcelain` của thư mục đó phải rỗng."""
    _build_passing_tree(tmp_path)
    fake_git.out = " M SKILL.md\n?? releases/1.1.0/stages/NOTE.md\n"
    result = _item(tmp_path, "9")
    assert not result["ok"] and "SKILL.md" in result["msg"] and "NOTE.md" in result["msg"]
    assert fake_git.dirs == [tmp_path / check_drift.LIVE_SKILL]


def test_check9_clean_live_skill_passes(tmp_path, fake_git):
    _build_passing_tree(tmp_path)
    assert _item(tmp_path, "9")["ok"] and fake_git.dirs == [tmp_path / check_drift.LIVE_SKILL]


def test_check9_git_error_or_missing_dir_fails(tmp_path, fake_git):
    result = _item(tmp_path, "9")                        # chưa có thư mục skill ⇒ không gọi git
    assert not result["ok"] and "dung-video-talking-head" in result["msg"] and fake_git.dirs == []
    _build_passing_tree(tmp_path)
    fake_git.code, fake_git.out = 128, "fatal: not a git repository"
    result = _item(tmp_path, "9")
    assert not result["ok"] and "not a git repository" in result["msg"]


def test_run_git_reads_porcelain_without_touching_the_index(tmp_path, monkeypatch):
    """_run_git thật: `git --no-optional-locks -C <dir> status --porcelain` (không ghi index)."""
    monkeypatch.undo()
    repo = tmp_path / "skill"
    repo.mkdir()
    import subprocess
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    assert check_drift._run_git(repo) == (0, "")
    (repo / "SKILL.md").write_text("router\n", encoding="utf-8")
    code, out = check_drift._run_git(repo)
    assert code == 0 and "?? SKILL.md" in out


# ------------------------------------------------ mục 1: loại trừ _superseded/


def test_check1_ignores_files_under_superseded(tmp_path):
    staging = tmp_path / "profiles" / "opa-operator" / "staging"
    _write(staging / "_superseded" / "vm-heygen-1-20260910" / "PACKET-a.md",
           "0.82 và DUCK_DB đầy trong này\n")
    _write(root_config := tmp_path / "profiles" / "opa-operator" / "config.yaml", OPERATOR_CONFIG_OK)
    _write(tmp_path / "profiles" / "opa-editor" / "config.yaml", _aux_config(False))
    _write(tmp_path / "profiles" / "opa-verifier" / "config.yaml", _aux_config(False))
    results = check_drift.check_drift(tmp_path)
    assert dict((r["code"], r["ok"]) for r in results)["1"] is True


def test_check1_catches_py_file_too(tmp_path):
    staging = tmp_path / "profiles" / "opa-operator" / "staging"
    _write(staging / "create_kanban_old.py", "OFFSET = 'OUTPUT_AUDIO_OFFSET'\n")
    _write(tmp_path / "profiles" / "opa-operator" / "config.yaml", OPERATOR_CONFIG_OK)
    _write(tmp_path / "profiles" / "opa-editor" / "config.yaml", _aux_config(False))
    _write(tmp_path / "profiles" / "opa-verifier" / "config.yaml", _aux_config(False))
    result = {r["code"]: r for r in check_drift.check_drift(tmp_path)}["1"]
    assert not result["ok"] and "create_kanban_old.py" in result["msg"]


def test_check1_missing_staging_dir_passes(tmp_path):
    """Không có thư mục staging (đã dọn/không tồn tại) -> không FAIL vô cớ."""
    _write(tmp_path / "profiles" / "opa-operator" / "config.yaml", OPERATOR_CONFIG_OK)
    _write(tmp_path / "profiles" / "opa-editor" / "config.yaml", _aux_config(False))
    _write(tmp_path / "profiles" / "opa-verifier" / "config.yaml", _aux_config(False))
    result = {r["code"]: r for r in check_drift.check_drift(tmp_path)}["1"]
    assert result["ok"]


# ------------------------------------------------ mục 2: glob "**" khớp cả cấp 0


def test_check2_matches_directory_directly_under_skills(tmp_path):
    """"skills/**/dung-video-talking-head" phải khớp cả khi không có cấp trung
    gian (skills/dung-video-talking-head), không chỉ khi lồng sâu hơn."""
    (tmp_path / "profiles" / "opa-editor" / "skills" / "dung-video-talking-head").mkdir(parents=True)
    result = {r["code"]: r for r in check_drift.check_drift(tmp_path)}["2"]
    assert not result["ok"]
    assert "opa-editor/skills/dung-video-talking-head" in result["msg"].replace("\\", "/")


# ------------------------------------------------ mục 5: các dạng entry cấm khác nhau


@pytest.mark.parametrize("bad_entry", ["execute_code", "script execution via -e/-c flag"])
def test_check5_flags_each_forbidden_entry_alone(tmp_path, bad_entry):
    cfg = dedent(f"""\
        kanban:
          max_in_progress_per_profile: 1
          auto_decompose: true
        command_allowlist:
          - script execution via heredoc
          - {bad_entry}
        """)
    _write(tmp_path / "profiles" / "opa-operator" / "config.yaml", cfg)
    result = {r["code"]: r for r in check_drift.check_drift(tmp_path)}["5"]
    assert not result["ok"] and bad_entry in result["msg"]


# ------------------------------------------------ đọc YAML khi PyYAML vắng mặt


def test_minimal_yaml_fallback_matches_pyyaml(tmp_path, monkeypatch):
    """Ép rơi về bộ đọc thô (mô phỏng máy thiếu PyYAML) và kiểm nó rút đúng giá
    trị y hệt PyYAML cho các khoá check_drift cần."""
    monkeypatch.setattr(check_drift, "_HAS_YAML", False)
    _write(tmp_path / "config.yaml", ROOT_CONFIG_DRIFTED)
    _write(tmp_path / "profiles" / "opa-operator" / "config.yaml", OPERATOR_CONFIG_DRIFTED)
    _write(tmp_path / "profiles" / "opa-editor" / "config.yaml", _aux_config(False))
    _write(tmp_path / "profiles" / "opa-verifier" / "config.yaml", _aux_config(False))
    results = {r["code"]: r for r in check_drift.check_drift(tmp_path)}
    assert not results["3"]["ok"] and "None" in results["3"]["msg"]  # thiếu max_in_progress_per_profile
    assert results["4"]["ok"]
    assert not results["5"]["ok"] and "execute_code" in results["5"]["msg"]


# ------------------------------------------------ CLI main()


def test_cli_prints_one_line_per_item_and_exit_code(tmp_path, capsys):
    _build_passing_tree(tmp_path)
    code = check_drift.main(["--hermes-root", str(tmp_path)])
    out = capsys.readouterr().out.splitlines()
    assert code == 0
    assert [ln.split()[0] for ln in out] == CODES
    assert all(" PASS " in f" {ln} " for ln in out)


def test_cli_exits_1_when_any_item_fails(tmp_path, capsys, fake_hermes, fake_git):
    _build_failing_tree(tmp_path)
    fake_hermes.board = "active"
    fake_git.out = "?? stray.md\n"
    code = check_drift.main(["--hermes-root", str(tmp_path)])
    out = capsys.readouterr().out.splitlines()
    assert code == 1
    assert all(" FAIL " in f" {ln} " for ln in out)


def test_cli_default_hermes_root_is_documented_path():
    assert check_drift.DEFAULT_HERMES_ROOT == "C:/Users/Minh PC/AppData/Local/hermes"
