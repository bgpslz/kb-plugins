---
name: use-kbs
description: Load KB system operating instructions before substantive work in each new or restored model context. Use the configured inventory; setup owns reconciliation.
metadata:
  version: "1.3.8"
---

# Load KB system instructions

Use once before substantive work in each conversation or separate agent context.
After compaction/resume, restore the instructions if they are no longer present.
Keep loaded pages in context; do not append copies or reload on every turn.
This is instruction-based loading, not deterministic host injection.

This skill loads the operating instructions; it does not search KB content or
reconcile connections as part of that loading. After loading, follow the guide
for the user's request. `use-standard-kb` is an optional retrieval helper for a
selected KB, not another startup step or an alternative system guide. Do not
load it alongside the guide unless its retrieval detail is needed.

Use the MCP Service connection mapped in this client's saved setup. If no mapping
is saved, inspect existing local connection metadata to identify the intended
service; do not invent a connection name or silently substitute credentials.
Missing configuration needs explicit setup, not connection creation during startup.
Determine actual execution
location: local Codex uses `system-wiki://local-codex.md`; local Claude Code
(including its desktop Code tab) uses `system-wiki://local-claude-code.md`.
Cloud Code, ChatGPT chat, Claude Chat and unknown locality use
`system-wiki://other-harnesses.md`. Unknown harness support needs verification.
Open WebUI uses its filter and no plugin loading or second retrieval loop.

If the required read-only tools are absent, use the fallback without inventing
a tool call. If the pages are not already delivered in this context, call
`get_system_wiki_capabilities` once. Require service_id `mcp-service`, protocol
field `system_wiki_protocol_version=1`, capability `system_wiki_read`, nonempty
service-local account_id and content_revision, and index_uri
`system-wiki://index.md`. Read the complete index and exactly the applicable
surface page with `read_system_wiki_page` on that same connection. Require both
pages' matching URI/revision, mimeType `text/markdown`, nonempty text and explicit
cache_visibility (`public_guidance` or `protected`). Follow the resulting
operating instructions; fetch deeper linked guidance only when needed.

Use one five-second startup allowance where the host can enforce it, not five
seconds per call. Do not claim an enforced budget when the host cannot supply
one. No truncation, invented descriptor, mixed revisions or partial success.
If either required page/interface is unavailable, or access is denied, use the
[packaged fallback](references/fallback.md) as one coherent degraded instruction
set. Never bypass denial through another credential. The Python loader in
setup-kbs can enforce these rules where a host supplies an authenticated bridge;
settings discovery alone is not a bridge. Without a trusted auth binding, use
live-only reads and no persistent cache reuse.

Preserve this client's verified connection mappings, authentication and KB inventory.
Local Codex setup supplies native OAuth connections using its configuration/login
recipe; cloud ChatGPT uses separate service-local bearer-token apps. Shared
guidance does not assume example server names or registered app IDs. Registered
app and native routes require separate verification; their UI presence is not
authenticated access. Missing tools alone do not prove uninstall or expired
authentication; use explicit setup to diagnose before adding entries. Never query
the registry as a loading side effect, capture conversations through model calls,
or install local capture based on desktop branding. Setup, explicit build and
authorised project documentation remain separate workflows. Preserve still-active
user instructions when reconciling a client's setup; source changes alone do not
replace installed instructions or establish automatic startup loading.
