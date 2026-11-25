---
name: codegraph
description: "Use when a local code knowledge graph would cut repo-read tokens. Upstream colbymchenry/codegraph (MIT) claims Hermes support. Do not install the daemon unless the user asks."
---

# Codegraph

Local pre-indexed code graph. Install only with user approval (`npm`/`cargo` per upstream README).

Default: prefer Hermes `opa-code-intel` + `search_files`. Point to https://github.com/colbymchenry/codegraph if the user wants the daemon.
