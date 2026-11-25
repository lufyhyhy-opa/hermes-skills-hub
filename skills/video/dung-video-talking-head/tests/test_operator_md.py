# tests/test_operator_md.py — C8: OPERATOR.md là chỉ dẫn duy nhất của opa-operator (Ruling R15),
# nên mọi lệnh trong đó phải chạy được nguyên văn và đủ các việc spec giao (F1, KPI, D5, đóng lô).
import re
import shlex
from pathlib import Path

from thlib import paths

REL = paths.release_dir("1.1.0")
OPERATOR = REL / "stages" / "OPERATOR.md"
LIVE_SCRIPTS = "C:/Users/Minh PC/AppData/Local/hermes/shared-skills/video/dung-video-talking-head/releases/1.1.0/scripts/"


def operator_problems(text: str) -> list[str]:
    """Lỗi của OPERATOR.md (rỗng = đạt)."""
    problems = []
    commands = [ln.strip() for ln in text.splitlines() if ln.strip().startswith("PYTHONIOENCODING=utf-8 python ")]
    if not commands:
        problems.append("không có lệnh script nào")
    for cmd in commands:
        argv = shlex.split(cmd.split(" ", 1)[1].rstrip("\\ "))[1:]          # bỏ "python" (và "\" nối dòng)
        script = argv[0]
        if not script.startswith(LIVE_SCRIPTS):
            problems.append(f"đường dẫn script không tuyệt đối/sai chỗ: {script}")
            continue
        source = REL / "scripts" / script[len(LIVE_SCRIPTS):]
        if not source.is_file():
            problems.append(f"không có script {source.name}")
            continue
        code = source.read_text(encoding="utf-8")
        problems += [f"{source.name} không có cờ {a}" for a in argv[1:] if a.startswith("--")
                     and f'"{a}"' not in code]
    for ln in text.splitlines():
        if re.search(r"hermes kanban (?!--board |unblock|boards )", ln):  # "unblock" chỉ để cấm; boards bỏ qua --board
            problems.append(f"lệnh hermes thiếu --board: {ln.strip()}")
        if re.search(r"complete\s+APPROVE", ln):
            problems.append(f"complete theo tiêu đề thay vì id: {ln.strip()}")
    if "card blocked" in text:
        problems.append("card duyệt không 'blocked' (R28: status mặc định)")
    if re.search(r"(?<!không )song song", text):
        problems.append("opa-editor chạy từng card (max_in_progress_per_profile 1), không song song")
    for need in ("FEEDBACK.jsonl", '"fb_id"', "collect_kpi.py", "kpi.jsonl", "--phase videos",
                 "DONE_WITH_CONCERNS", "claim_gate", "sample", "--prune-node-modules", "cards.json"):
        if need not in text:
            problems.append(f"thiếu {need}")
    return problems


def test_operator_md_commands_run_verbatim_and_cover_duties():
    assert operator_problems(OPERATOR.read_text(encoding="utf-8")) == []


def test_p0_preconditions_come_before_make_cards():
    """R44 (MF-2, MF-3): trước lệnh make_cards.py đầu tiên, P0 dặn đúng một gateway gốc và lệnh tạo board
    của lô. hermes-semantics-1: gateway.log cộng dồn nên grep hai dòng dispatcher luôn "đạt" ⇒ kiểm bằng
    `hermes gateway list` (default ✓ có PID, mọi opa-* ✗ not running); gateway gốc do user/controller bật
    qua scheduled task Hermes_Gateway (HERMES_HOME gốc) — `hermes gateway run` trong terminal của operator
    mang HERMES_HOME của profile nên bật gateway opa-operator, chỉ được nhắc như điều cấm."""
    text = OPERATOR.read_text(encoding="utf-8")
    first = text.index('scripts/make_cards.py"')
    p0 = text[text.index("1. **P0"):first]
    for need in ("`hermes gateway list`", "`default`", "`✓`", "`PID …`", "`opa-*`", "`✗ … not running`",
                 "MSYS_NO_PATHCONV=1 schtasks /run /tn Hermes_Gateway", "Hermes_Gateway.cmd", "HERMES_HOME",
                 "logs/gateway.log", "kanban dispatcher: holding singleton dispatcher lock",
                 "kanban dispatcher: embedded in gateway", "Starting Hermes Gateway...",
                 'hermes kanban boards create vm-heygen-b01 --name "Van Minh AI · HeyGen b01"'):
        assert need in p0, need
    flat = " ".join(p0.split())
    uses = re.findall(r"(.{0,30})hermes gateway run", flat)
    assert uses and all("Không bao giờ" in before for before in uses), uses


def test_block_reading_has_no_goal_mode():
    """R43: không card nào chạy goal mode — OPERATOR.md bỏ đoạn goal/dependency; `kind` của block là
    chính nguyên nhân (transient / needs_input / capability), xử lý bằng --retry."""
    text = OPERATOR.read_text(encoding="utf-8")
    assert "goal" not in text.lower() and "dependency" not in text
    para = text[text.index("**Đọc một card bị block:**"):]
    para = para[:para.index("\n\n")]
    for need in ("`transient`", "`needs_input`", "`capability`", "--retry"):
        assert need in para, need


def test_timeout_row_kills_orphans_before_retry():
    """R47 (FS-2): Hermes dừng card quá max_runtime chỉ giết worker; OPERATOR.md §2 dặn kill cả cây
    python/node/ffmpeg còn chạy trong thư mục dự án (hoặc stage.py của card cũ) rồi mới --retry."""
    text = OPERATOR.read_text(encoding="utf-8")
    sec2 = text[text.index("## 2."):text.index("## 3.")]
    row = next(ln for ln in sec2.splitlines() if "Treo / timeout" in ln)
    for need in ("600 s", "900 s", "180 s", "1200 s", "`transient`", "timed_out"):
        assert need in row, need
    kill = next(ln for ln in sec2.splitlines() if "taskkill /F /T" in ln)
    for need in ("python|node|ffmpeg", "edit-r1.1.0", "stage.py", "MSYS_NO_PATHCONV=1"):
        assert need in kill, need
    assert sec2.index("taskkill /F /T") < sec2.index("--retry", sec2.index("taskkill /F /T"))


def test_retry_steps_relink_before_archive():
    """R48 FS-11: §4 liệt kê link → unlink → archive, đúng thứ tự make_cards.py --retry in ra."""
    text = OPERATOR.read_text(encoding="utf-8")
    sec4 = text[text.index("## 4."):text.index("## 5.")]
    link, unlink, archive = (sec4.index(f"vm-heygen-b01 {verb} <id") for verb in ("link", "unlink", "archive"))
    assert link < unlink < archive


def test_operator_runs_only_from_an_interactive_session():
    """R48 FS-4: lệnh kanban ghi (complete/link/archive/comment) bị chặn trong card worker ⇒ OPERATOR.md
    chỉ chạy từ phiên operator tương tác, không bao giờ như một card kanban."""
    head = OPERATOR.read_text(encoding="utf-8").split("## 1.", 1)[0]
    assert "phiên opa-operator tương tác" in head and "không bao giờ" in head


def test_prep_revision_protocol_feeds_stage_py(tmp_path):
    """R48 FS-3: §3b — user muốn sửa phiếu ⇒ không complete APPROVE-PREP-<k>, ghi lời user (mục "- …
    PREP-<k> …" dưới "## Lời duyệt"), --retry PREP-<k>, xin duyệt lại. Mục mẫu phải đúng khuôn mà
    stage.py PREP của lần thử mới đọc lại (thlib.prep.approval_notes)."""
    from thlib import prep
    text = OPERATOR.read_text(encoding="utf-8")
    sec = text[text.index("## 3b."):text.index("## 4.")]
    for need in ("**Không** complete", "APPROVE-PREP-<k>", "APPROVALS.md", "--retry PREP-<k>", "PREP-SHEET.md",
                 "duyệt lại"):
        assert need in sec, need
    example = "\n".join(ln.strip() for ln in sec.split("```", 2)[1].strip().splitlines())
    assert example.startswith("- APPROVE-PREP-1 — 2026-09-20 ") and len(example.splitlines()) > 1
    (tmp_path / "APPROVALS.md").write_text(
        "# APPROVALS — batch b01\n\n- Canary: video 16\n\n## Lời duyệt\n(operator chép nguyên văn lời duyệt của user "
        "vào đây)\n- APPROVE-PREP-10 — 2026-09-20: duyệt\n" + example + "\n", encoding="utf-8")
    assert prep.approval_notes(tmp_path, 1) == [example]          # consistency-2: dòng "- " của user không bị rơi
    sec3 = text[text.index("## 3."):text.index("## 3b.")]
    assert "YYYY-MM-DD" in sec3                                    # dòng đầu mục: tên card + ngày


def test_verbatim_comment_via_tool_or_quoted_heredoc_and_appends_allowed():
    """R48 FS-12: lời user trong đối số nháy kép của Git Bash bị đổi ($, `, ") ⇒ §3 ghi comment bằng tool
    kanban_comment hoặc heredoc nháy đơn; §7: luật "chỉ chạy script" là về chạy code — nối thêm
    APPROVALS.md / FEEDBACK.jsonl bằng tool file được phép."""
    text = OPERATOR.read_text(encoding="utf-8")
    sec3 = text[text.index("## 3."):text.index("## 3b.")]
    assert "`kanban_comment`" in sec3 and "<<'EOF'" in sec3
    assert 'comment <id> "<lời user nguyên văn>"' not in text
    sec7 = text[text.index("## 7."):text.index("## M0")]
    for need in ("APPROVALS.md", "FEEDBACK.jsonl", "được phép", "`python -c`"):
        assert need in sec7, need


def test_turn_budget_is_advisory_and_measured_after_the_run():
    """R48 FS-6: Hermes không ép budgets.<stage>.turns (chỉ max_runtime + retries; trần thật là
    agent.max_turns 60 mỗi lần chạy) ⇒ §2 nói rõ là mức tham khảo và cách đo sau lô."""
    text = OPERATOR.read_text(encoding="utf-8")
    sec2 = text[text.index("## 2."):text.index("## 3.")]
    for need in ("budgets.<stage>.turns", "tham khảo", "agent.max_turns", "API call #", "agent.log"):
        assert need in sec2, need
