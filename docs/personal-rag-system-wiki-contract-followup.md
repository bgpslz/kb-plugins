# Extend the existing system-wiki reader for client integration

23 October 2026. Follow-up to personal-rag's `docs/kb_plugins_completion_brief.md`.
This is a handover for that repository, not a second reader or deployment approval.

The current thirteen-page bundle and authenticated resource/tool reader exist in
`personal-rag/src/personal_rag/system_wiki/`. The reader inspected at current source `9d39527` (bundle work includes `ea27de2`)
returns uri/mimeType/text. The kb-plugins source client preserves the approved
richer contract and therefore cannot yet use that reader successfully.

Extend `service.py` and its existing registration in
`knowledge_registry/{tools,http_app}.py`:

1. Add `get_system_wiki_capabilities({})`, using existing authentication to derive
   a stable service-local account_id. Return service_id `mcp-service`, integer
   system_wiki_protocol_version `1`, capabilities `["system_wiki_read"]`,
   index_uri `system-wiki://index.md` and immutable content_revision.
2. Derive content_revision deterministically from the complete packaged bundle's
   relative paths and bytes, including additions/deletions. A hash must describe
   the bytes actually served; do not reuse a Git HEAD label across changed builds
   or silently hash one tree and read a subsequently changed tree.
3. Add matching content_revision and explicit cache_visibility to every page.
   Only shipped, non-account-specific system guidance is `public_guidance`.
   The client accepts `protected` for live reads without persistent content cache;
   missing/unknown classifications fail the contract. This classification never
   enables anonymous access. Do not classify arbitrary KB/private account content.
4. Preserve the existing MCP tool envelope: structuredContent is authoritative;
   Markdown may also appear in text content. Preserve resource/tool byte and
   revision parity; standard resource `_meta` may carry revision/classification.
   Native resource content and metadata must be converted explicitly by a host
   adapter before using the client's tool-shaped interface.
5. Retain authenticated read-only dispatch and namespace confinement. No new
   login, proxy, capture path or combined-read tool is needed.

Client entry point: `Loader.load_startup(context, surface, execution)` in
kb-plugins `setup/system_wiki.py`. Cold startup performs one descriptor and two
sequential page calls under a five-second total budget; a revision mismatch or
missing surface fails the whole set. Local Codex/Claude Code select their own
surface; cloud/unknown locality uses other-harnesses. The client retains the
single-page `load` operation for explicit deeper reads.

Acceptance: build/install the real wheel in an isolated environment, remove
source-checkout dependency, read every packaged page through actual registered
resource/tool handlers, compare bytes/metadata, test identity separation and
bundle upgrade/revision consistency. Feed the actual CallToolResult envelope
into the client for index plus surface startup. Test 401/403, absent metadata,
timeout, early MCP unavailability and a mid-startup revision change. Keep auth
bindings host-attested; no credential scraping or invented identity epoch.

Backend source completion, approved deployment and fresh host-context delivery
are separate milestones. This brief grants no VPS mutation, account grant,
restart or permission to message another chat. Report exact source and deployed
revisions; the client must not claim integration against a hypothetical backend.
