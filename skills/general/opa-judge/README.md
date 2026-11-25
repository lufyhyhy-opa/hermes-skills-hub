# opa-judge

Cross-model adversarial review cho Phase 4. Gửi code diff tới model thứ 2 (GPT-5 / Gemini 2.5) để tìm blind spots mà primary reviewer (Claude) miss.

## Setup

Set ít nhất 1 API key:

```bash
export OPENAI_API_KEY="sk-..."     # GPT-5
export GOOGLE_API_KEY="AIza..."    # Gemini 2.5 Pro
```

Hoặc dùng Ollama local (free, weaker):
```bash
ollama pull llama3
```

## Trigger

```
"second opinion cho PR này"
"cross-model review"
"judge review code"
```

## Safety

- Hỏi user confirm trước khi gửi code ra external API
- Judge chỉ recommend, KHÔNG override production decisions
- Disagreements luôn escalate tới user

## Cost

Mỗi judge call ~2k-6k tokens input + ~1k-2k output. Cost logged vào `.planning/events.jsonl`.
