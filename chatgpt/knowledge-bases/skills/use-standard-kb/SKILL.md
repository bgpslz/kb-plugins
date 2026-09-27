---
name: use-standard-kb
description: Generic retrieval workflow for a configured KB Service using the standard OKF/RAG protocol. Invoke through use-kbs only for KBs materially relevant to the current request.
metadata:
  version: "1.0.0"
  kb_protocol_version: 1
---

# Use a standard KB

Infer the target KB/service from `use-kbs`; if ambiguous, ask which configured KB rather than querying all of them. Require protocol version 1 and only call declared capabilities.

For deterministic personal or organisation knowledge, use the target KB's wiki first. Start at `wiki://index.md` unless a canonical relevant URI is already reliably known in this conversation. Follow links efficiently, read whole relevant pages, backtrack promptly, and avoid listing or brute-force search when traversal is sufficient.

Fall back to the target KB's retrieval corpus only when the wiki is insufficient or the request asks for source evidence. Use chunk search for what source material says; document metadata search for records, senders, dates, URLs or folders; table search/fetch/value tools for spreadsheet and table questions; and specialised capabilities such as `x` only when declared and relevant. Filter before ranking, preserve provenance, keep separate intents in separate calls, and treat ranking as evidence guidance rather than proof. Avoid unnecessary RAG calls.

Stop once evidence is sufficient. Do not silently substitute another KB after a requested KB read fails. Give diagnostic traversal pages, query plans, scores or traces only when explicitly requested.
