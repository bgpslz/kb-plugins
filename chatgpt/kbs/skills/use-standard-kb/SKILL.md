---
name: use-standard-kb
description: Retrieve maintained knowledge and source evidence from a selected configured KB Service. Use when retrieval detail is needed after KB operating instructions have been loaded; does not set up connections or load the system guide.
metadata:
  version: "1.0.1"
  kb_protocol_version: 1
---

# Use a standard KB

This is an optional retrieval helper, not a transitional instruction loader.
`use-kbs` loads the system-wiki operating instructions; this skill supplies
retrieval detail for a KB relevant to the user's request. Follow already-loaded
guidance without reloading it. If guidance is missing, load it through `use-kbs`
first; when unavailable, its packaged fallback preserves direct retrieval.
Neither path requires this helper to be invoked for every question.

Select the relevant KB from the configured inventory. If the user's intended KB
is ambiguous, ask rather than querying all KBs. Require KB Protocol 1 and use
only declared capabilities. A successful substantive read establishes the
connection; do not repeat connection checks after success.

For ordinary personal or organisation knowledge, start at `wiki://index.md`
unless a relevant canonical page is already reliably known. Read whole relevant
pages and follow their links. Use the retrieval corpus when the wiki leaves a
gap, or start with sources when the user explicitly asks for source evidence.

Choose chunk search for what source material says; document metadata search for
records, senders, dates, URLs or folders; table tools for spreadsheet/table
questions; and specialised tools such as `x` only when declared and relevant.
Filter before ranking, keep separate intents in separate calls and preserve
provenance. Ranked candidates are not a quota of facts to include.

Stop when the evidence is sufficient. Accept an empty result unless the query
was poorly phrased; do not keep varying it to force a match. Do not silently
switch KBs or credentials after an access refusal, or use cached protected pages
to bypass one. Provide query plans, scores and traces only when requested.
