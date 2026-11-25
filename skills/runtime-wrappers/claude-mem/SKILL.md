---
name: claude-mem
description: "Reference only. thedotmack/claude-mem (Apache-2.0) GitHub about-text lists Hermes, but cloned source has no Hermes installer (Claude/OpenCode/OpenClaw only). Do not enable a second memory plane."
---

# claude-mem (reference)

Audit 2026-08-22: 22 product SKILL.md files are for the claude-mem plugin itself, not portable domain skills.

OPA already uses Hermes memory (MEMORY.md / USER.md). Mode: reject as default install.

Do not run the collector alongside Hermes memory unless the user explicitly wants a dual plane after reviewing worker footprint.
