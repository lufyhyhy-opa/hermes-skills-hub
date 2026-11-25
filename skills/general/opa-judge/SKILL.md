---
name: opa-judge
description: Use khi Phase 4 REVIEW cần second opinion từ model khác để giảm self-review bias. Triggers — "second opinion", "cross-model review", "judge review", "adversarial review bằng model khác", "double review". KHÔNG use cho — lần review đầu (dùng code-reviewer agent), bug fix lẻ, style-only review. Yêu cầu ít nhất 1 additional API key (OpenAI hoặc Google).
license: MIT
version: 1.0
---

# OPA Judge — Cross-model adversarial review

> Problem: Self-review bias — cùng model viết code + review = miss own blind spots.
> Solution: Gửi code tới model khác (GPT-5 / Gemini 2.5), so sánh findings, escalate disagreements.

## Khi nào dùng

- Phase 4 REVIEW đã chạy bằng Claude (reviewer chính)
- Code có risk cao: auth, payment, data migration, public API
- Review chính trả APPROVE nhưng confidence thấp
- User muốn thêm 1 layer verification

## Khi nào KHÔNG dùng

- Review lần đầu (dùng code-reviewer agent)
- Trivial changes (typo, comment update)
- Budget concerns (mỗi judge call tốn tokens ở 2 providers)

## Fallback khi chưa có consent gửi code ra external API

Không tự động gọi OpenAI/Google. Thay vào đó có thể chạy **independent internal review** bằng hai Hermes subagent read-only:

1. **Spec reviewer** — đọc acceptance/source-of-truth, kiểm diff và trả finding có `severity + path:line + evidence`, kết thúc bằng `SPEC_VERDICT: PASS|BLOCK`.
2. **Code/security reviewer** — trace contract/auth/async/demo-write-lock/error path, trả finding có `severity + path:line + reproduction`, kết thúc bằng `CODE_VERDICT: PASS|BLOCK`.

Ghi nhãn đúng: đây là independent internal review, **không phải cross-model judge**. Không dùng kết quả này để claim đã có second opinion từ provider/model khác.

### Freshness rule

- Chụp baseline diff trước dispatch.
- Mọi source mutation sau dispatch làm verdict đang chạy hoặc đã trả về trở thành stale đối với phần delta.
- Sau khi sửa finding/copy/code, chạy lại static/runtime gate bị ảnh hưởng và dispatch delta review hoặc full review mới trước release verdict.
- Không đổi report từ `PENDING` sang `PASS` chỉ dựa trên test/build nếu reviewer bắt buộc chưa trả kết quả.

---

## Workflow

### Step 1 — Collect review context

Gather:
1. **Diff** — `git diff main...HEAD` (hoặc diff staged)
2. **Primary review** — output từ code-reviewer agent (Claude)
3. **File context** — full files touched (not just diff, judge cần đọc context)

### Step 2 — Select judge model

Priority:
1. **OpenAI GPT-5** (`OPENAI_API_KEY` env var) — nếu có
2. **Google Gemini 2.5 Pro** (`GOOGLE_API_KEY`) — nếu có
3. **Ollama local** (`ollama list | grep -q "llama3"`) — free fallback, weaker

Nếu không có API key nào → STOP, hướng dẫn user set env var.

### Step 3 — Construct judge prompt

```
You are an adversarial code reviewer. You are reviewing code that was written AND already reviewed by another AI model (Claude).

Your goal: find issues that the primary reviewer MISSED. Focus on:
1. Bugs the primary reviewer overlooked
2. Security issues not flagged
3. False positives — findings in primary review that are actually wrong
4. Edge cases not considered

Primary review:
---
{primary_review_output}
---

Code diff:
---
{git_diff}
---

Output format:
- NEW_FINDING: issue not in primary review (severity + file:line + evidence)
- DISAGREE: finding in primary where you think reviewer was wrong (why)
- CONFIRM: important finding you agree with (brief nod)
- MISSED: specific edge case or attack vector not considered

End with: JUDGE_VERDICT: AGREE_WITH_PRIMARY | OVERRIDE_TO_BLOCK | ESCALATE_TO_HUMAN
```

### Step 4 — Execute judge call

Dùng API trực tiếp:

**OpenAI:**
```bash
curl -s https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer REDACTED \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-5",
    "messages": [{"role": "user", "content": "<judge_prompt>"}],
    "temperature": 0.2
  }' | jq -r '.choices[0].message.content'
```

**Google Gemini:**
```bash
curl -s "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key=${GOOGLE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{"parts": [{"text": "<judge_prompt>"}]}],
    "generationConfig": {"temperature": 0.2}
  }' | jq -r '.candidates[0].content.parts[0].text'
```

### Step 5 — Compare + synthesize

| Judge verdict | Action |
|---|---|
| `AGREE_WITH_PRIMARY` | Proceed — confidence boosted |
| `OVERRIDE_TO_BLOCK` | Show disagreement to user, recommend BLOCK |
| `ESCALATE_TO_HUMAN` | Show both reviews side-by-side, user decides |

Output format:

```
## Cross-Model Review Summary

### Primary reviewer (Claude): APPROVE_WITH_CHANGES
  - 2 HIGH, 1 MEDIUM findings

### Judge (GPT-5): AGREE_WITH_PRIMARY
  - Confirmed: 2 of 3 findings
  - New finding: missing rate limit on /api/export (HIGH)
  - Disagreed: "race condition in cache.ts" — judge says: single-threaded Node, not a real race

### Synthesis
  Combined findings: 3 HIGH, 1 MEDIUM
  Disagreements: 1 (resolved: judge convincing, removing false positive)

  Final verdict: APPROVE_WITH_CHANGES
  → Fix: add rate limit to /api/export (HIGH)
  → Fix: auth token expiry check (HIGH from primary)
```

### Step 6 — Cost tracking

Log judge cost to `.planning/events.jsonl`:
```json
{"ts": "...", "tool": "opa-judge", "model": "gpt-5", "tokens_in": 4200, "tokens_out": 1800, "cost_usd": 0.12}
```

---

## Safety & Autonomous Council Rules

1. **Ưu tiên Tự Phản Biện Nội Bộ (Internal Council Review):** Mặc định sử dụng Hội đồng nội bộ Hermes (`Spec reviewer` + `Code/Quality reviewer`) để phản biện chéo mà không cần dừng lại hỏi xin phép gửi code ra ngoài.
2. **API key masked** trong mọi output.
3. **Tự động hợp nhất bất đồng (Autonomous Synthesis):** Nếu 2 góc nhìn phản biện khác nhau, Hội đồng tự phân tích bằng chứng thực tế (`file:line`, số liệu, logic) để chọn phương án tối ưu nhất và tự sửa lỗi lên bản v2/v3 ($\ge 9.0/10$), **không dừng pipeline để bắt Anh Huy phân xử thủ công**.

## Integration

Phase 4 REVIEW enhanced workflow:
```
Phase 4.1: Primary review (code-reviewer agent / Claude)
Phase 4.2: Judge review (opa-judge / GPT-5 or Gemini) — optional, for high-risk code
Phase 4.3: Synthesis → final verdict
Phase 4.4: User approval → proceed to Phase 5
```
