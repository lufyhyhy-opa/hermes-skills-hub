# tests/conftest.py — fixture dùng chung cho bộ test thlib.
# Bảng fixture: .superpowers/sdd/2026-09-11-talking-head-rulebook-1.1-r0a/
# contracts-and-fixtures.md. Mỗi task nối thêm fixture của mình vào đây.
import csv
import json
from pathlib import Path

import pytest

from thlib import align, audio, lint, mix, paths, picture, planner, rules, scripts_v3, sfxlib, voice

FIXTURES = Path(__file__).parent / "fixtures"
# Pack SFX 1.0.0 (bản copy trong worktree, Ruling R3; legacy/1.0.0 theo R36) — nguồn của bảng 25 cue cũ.
PACK_SFX = paths.SKILL / "legacy" / "1.0.0" / "assets" / "sfx"


def _with_onsets(words, pauses, R):
    """Bản sao `words` có thêm `on` (onset thật S04 qua voice.correct_onsets)."""
    onsets = voice.correct_onsets(words, pauses, R)
    return [{**w, "on": on} for w, on in zip(words, onsets)]


@pytest.fixture(scope="session")
def rules_110():
    """Bộ luật 1.1.0 đã nạp — dùng chung cho mọi test cần tra rules.json."""
    return rules.load("1.1.0")


@pytest.fixture(scope="session")
def v3_sections():
    """60 mục VIDEO SCRIPT/APPLY CUSTOM MOTION đã tách, từ bản sao read-only
    trong tests/fixtures/scripts/."""
    return scripts_v3.load_v3(scripts_v3.find_v3_file(FIXTURES / "scripts"))


@pytest.fixture(scope="session")
def eval_rows():
    """Bảng đánh giá HYBRID/talking-head (đã mở rộng các dòng gộp khoảng số)."""
    return scripts_v3.load_eval(FIXTURES / "scripts" / "60-kich-ban-heygen-talking-head.md")


@pytest.fixture(scope="session")
def fixture_v2_words():
    """Từ whisper thô của video 02 — chỉ số của edit.json 1.0.0 tham chiếu tới đây."""
    path = FIXTURES / "v2" / "words_whisper.json"
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def scan_rows():
    """Kết quả quét whisper 25 s đầu × 60 file thật (bản sao read-only của
    audit/video_v3_mapping.csv) — dùng làm oracle cho thlib.mapping."""
    path = FIXTURES / "scan" / "video_v3_mapping.csv"
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


@pytest.fixture(scope="session")
def v2_vo_mono():
    """vo-clean của video 02 (bản 1.0.0, trục của words_whisper.json), mono (L+R)/2."""
    return audio.decode_mono(FIXTURES / "v2" / "vo-clean.m4a")


@pytest.fixture(scope="session")
def fixture_v2_pauses_full(v2_vo_mono, v3_sections, fixture_v2_words, rules_110):
    """Dict đúng dạng pauses.json của video 02: khoảng ngắt S04, designed_breaks
    từ lời v3, VO_REF, độ dài, mốc hết lời."""
    script = v3_sections[2]["script"]
    words = align.align(script, fixture_v2_words)["words"]
    pauses = voice.find_pauses(v2_vo_mono, rules_110)
    duration = len(v2_vo_mono) / audio.SR
    return {
        "pauses": [[t0, t1] for t0, t1 in pauses],
        "designed_breaks": align.designed_breaks(script, words),
        "vo_ref": voice.vo_ref(v2_vo_mono, rules_110),
        "duration_s": duration,
        "last_word_end": voice.last_word_end(words, pauses, duration),
    }


@pytest.fixture(scope="session")
def fixture_v2_whisper_words_on(fixture_v2_words, fixture_v2_pauses_full, rules_110):
    """Từ whisper thô + `i` + `on` — dùng với edit_legacy.json (chỉ số cũ)."""
    words = [{"i": i, **w} for i, w in enumerate(fixture_v2_words)]
    return _with_onsets(words, fixture_v2_pauses_full["pauses"], rules_110)


@pytest.fixture(scope="session")
def fixture_v2_words_corrected(v3_sections, fixture_v2_words, fixture_v2_pauses_full, rules_110):
    """Từ hiển thị theo lời v3 đã căn + `on` — chỉ số của edit_v11.json tham chiếu tới đây."""
    words = align.align(v3_sections[2]["script"], fixture_v2_words)["words"]
    return _with_onsets(words, fixture_v2_pauses_full["pauses"], rules_110)


@pytest.fixture(scope="session")
def v2_edit_v11():
    """edit.json 1.1 của video 02 (chỉ số theo fixture_v2_words_corrected)."""
    return json.loads((FIXTURES / "v2" / "edit_v11.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def sfx_manifest_110():
    """sfx_manifest.json của bản 1.1.0 (10 file đã đo)."""
    return sfxlib.load_manifest("1.1.0")


@pytest.fixture(scope="session")
def sfx_signals_110(sfx_manifest_110):
    """Tín hiệu mono của mọi file trong manifest 1.1.0, tra theo khoá manifest."""
    return {k: sfxlib.load_signal("1.1.0", k) for k in sfx_manifest_110["files"]}


@pytest.fixture(scope="session")
def v2plan(fixture_v2_words_corrected, fixture_v2_pauses_full, v2_edit_v11,
           sfx_manifest_110, sfx_signals_110, v2_vo_mono, rules_110):
    """Kết quả planner trên video 02 với preset standard: (sfx_plan, cues_audio)."""
    return planner.plan(fixture_v2_words_corrected, fixture_v2_pauses_full, v2_edit_v11, [],
                        sfx_manifest_110, sfx_signals_110, v2_vo_mono, rules_110, "standard")


@pytest.fixture(scope="session")
def v2_lock(fixture_v2_words_corrected, v2_edit_v11, v2plan, fixture_v2_pauses_full, rules_110):
    """picture_lock của video 02: picture.build_lock trên sfx_plan của planner."""
    return picture.build_lock(fixture_v2_words_corrected, v2_edit_v11, v2plan[0],
                              fixture_v2_pauses_full, rules_110)


@pytest.fixture(scope="session")
def v2plan_and_stem(v2plan, v2_vo_mono, v2_lock, sfx_manifest_110):
    """(sfx_plan, stem, vo, picture_lock, manifest) của video 02: stem dựng từ
    cues_audio của planner bằng mix.render_stem trên trục vo-clean; picture_lock
    là khoá hình thật (picture.build_lock) — L9 chấm trên đúng khoá BUILD ghi."""
    plan, cues_audio = v2plan
    stem = mix.render_stem(cues_audio, len(v2_vo_mono))
    return plan, stem, v2_vo_mono, v2_lock, sfx_manifest_110


@pytest.fixture(scope="session")
def old_cues_plan_and_stem(v2plan_and_stem, fixture_v2_pauses_full):
    """25 cue SFX cũ của video 02 (tests/fixtures/v2/old_cues.json): plan đổi bằng
    lint.old_cues_to_plan; stem dựng từ file pack 1.0.0 (legacy/1.0.0/assets/sfx/<src bỏ 'sfx/'>,
    giải mã thô × volume, đặt ở from/30 s — như prototype/planner_v11.py dòng
    379–389). vo, picture_lock và manifest dùng chung với bản của planner."""
    _, _, vo, lock, manifest = v2plan_and_stem
    old = json.loads((FIXTURES / "v2" / "old_cues.json").read_text(encoding="utf-8"))
    raw = {c["src"]: audio.decode_mono(PACK_SFX / c["src"].removeprefix("sfx/")) for c in old}
    files = {src.removeprefix("sfx/"): sfxlib.measure(x) for src, x in raw.items()}
    plan = lint.old_cues_to_plan(old, fixture_v2_pauses_full, files)
    stem = mix.render_stem([{"start_s": c["from"] / lint.LEGACY_FPS,
                             "samples": raw[c["src"]] * c["volume"]} for c in old], len(vo))
    return plan, stem, vo, lock, manifest
