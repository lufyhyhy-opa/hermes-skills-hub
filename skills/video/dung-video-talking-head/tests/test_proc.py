# tests/test_proc.py — thlib.proc.run: process con nặng có trần thời gian, quá hạn giết cả cây (R47).
import subprocess
import sys
import time

import pytest

from thlib import proc

# Con sinh một cháu ghi nhịp vào file mỗi 0,1 s (như remotion.cmd → node → Chrome) rồi cả hai ngủ;
# cháu thừa hưởng ống stdout của con.
_GRANDCHILD = "import sys, time\nwhile True:\n    open(sys.argv[1], 'a').write('x')\n    time.sleep(0.1)\n"
_CHILD = ("import subprocess, sys, time\n"
          "subprocess.Popen([sys.executable, '-c', sys.argv[1], sys.argv[2]])\n"
          "print('con đã chạy', flush=True)\n"
          "time.sleep(60)\n")


def test_run_returns_completed_process_and_honours_check():
    got = proc.run([sys.executable, "-c", "print('ok')"], timeout=30, capture_output=True, text=True)
    assert got.returncode == 0 and got.stdout.strip() == "ok"
    with pytest.raises(subprocess.CalledProcessError):
        proc.run([sys.executable, "-c", "raise SystemExit(4)"], timeout=30, check=True)


def test_timeout_kills_whole_tree_without_hanging(tmp_path):
    """Quá hạn ⇒ TimeoutExpired ngay (không treo chờ ống stdout mà cháu còn giữ) và cháu cũng chết."""
    beat = tmp_path / "beat.txt"
    t0 = time.monotonic()
    with pytest.raises(subprocess.TimeoutExpired) as exc:
        proc.run([sys.executable, "-c", _CHILD, _GRANDCHILD, str(beat)], timeout=2,
                 capture_output=True, text=True, encoding="utf-8")
    assert time.monotonic() - t0 < 20
    assert exc.value.timeout == 2 and "con đã chạy" in (exc.value.output or "")
    size = beat.stat().st_size
    assert size > 0                                           # cháu đã chạy thật
    time.sleep(1.0)
    assert beat.stat().st_size == size                        # và đã bị giết cùng cây
