---
name: repomix
description: "Use when packing a repo into one AI-friendly file for review or handoff. CLI: npx repomix. Upstream yamadashy/repomix (MIT)."
---

# Repomix

Pack a repository into a single file for LLM context.

```bash
npx repomix
npx repomix --output repomix-output.xml
```

Hermes already has `opa-code-intel` for in-session codebase mapping. Use Repomix when you need a portable dump for another model or a review packet.

Do not commit secrets. Respect `.gitignore` / `.repomixignore`.
