# Phase 2: system-wiki and bootstrap contract

Historical approved design, 22 October. Current implementation/status is in
[setup implementation](setup-implementation.md). The 23 October completion brief
refines startup to the complete index plus exactly one applicable surface page,
under one descriptor/revision/budget. The backend reader/content now exist; only
the richer metadata extension and deployment remain dependencies. Source examples
and observations below describe the original review snapshot.

Approved by Bruno, 22 October 2026, after the
[phase 1 audit](architecture-alignment-audit.md) and phase 2 design review.
The interface and defaults below are approved for implementation. They remain
undeployed proposals until the separate personal-rag work is delivered. Phase 3
implements the kb-plugins setup foundation; approval does not establish deployment.

## Ownership and current evidence

The system wiki is Git-managed general system guidance in personal-rag, released
through that repository's normal chain and served read-only by MCP Service. It
contains roles, retrieval/KB selection, supported surfaces, capture/review,
reconnecting and glossary guidance. It contains no tenant knowledge, entitlement
inventory, credentials or private development records. Personal and organisation
KB wikis remain independent, with their own permissions and proposal lifecycles.

The plugin owns packaged bootstrap/fallback text, setup orchestration and small
client adapters. Each KB Service owns its capabilities, tools, build guide,
runtime authorisation and maintained knowledge. Open WebUI keeps its own filter
and capture integration; this work adds no second retrieval loop there.

Inspected personal-rag source currently gives MCP Service registry discovery and
central capture tools, with MCP initialization advertising tools only. It does
not expose a system-wiki contract. Existing KB wiki resources and tools serve
whole Markdown pages under `wiki://`; they are not MCP Service documentation.
The source's MCP Service HTTP docstring deliberately excludes wiki/review/search
workers. The implementation should preserve that lightweight boundary with a
separate static documentation reader, not import the KB publication subsystem.

Source evidence inspected for this draft:

- `personal-rag/src/personal_rag/knowledge_registry/{tools,http_app}.py`:
  authenticated service identity, registry version 1 and present dispatch surface.
- `personal-rag/ARCHITECTURE.md`: direct KB retrieval, resource/tool parity,
  publication locks and independent review state.
- `personal-rag/OPERATIONS.md` and `wiki/publication.py`: blocked publication and
  operator recovery rules. These are source observations, not a live deployment audit.

## Proposed read-only interface, version 1

All names and fields in this section are proposed, not existing endpoints.
Use the existing authenticated MCP transport and configured connection. Do not
create a new login, bearer credential or HTTP path for documentation.

| Operation | Proposed contract |
| --- | --- |
| `get_system_wiki_capabilities({})` | Descriptor below; also a substantive authenticated call establishing service connection state |
| `list_system_wiki_pages({cursor?})` | Cursor-paginated Markdown page metadata: `uri`, `title`, `description`; default traversal starts at the index instead |
| `read_system_wiki_page({uri})` | Whole-page response below; no fragment or arbitrary filesystem reads |
| MCP resources | Same list/read implementation and metadata as tools, under a distinct URI scheme |

Canonical proposed index: `system-wiki://index.md`. Linked pages resolve beneath
that namespace. It must never resolve to a KB's `wiki://index.md`. List/read tools
support clients whose MCP resource access is unavailable. Tools and resources
must return the same page bytes and revision. Do not add write/proposal, corpus
search or KB-proxy operations to this interface.

Proposed descriptor fields:

```json
{
  "service_id": "mcp-service",
  "account_id": "<stable authenticated service-local user ID>",
  "system_wiki_protocol_version": 1,
  "capabilities": ["system_wiki_read"],
  "index_uri": "system-wiki://index.md",
  "content_revision": "<immutable documentation bundle revision>"
}
```

This is a separate application contract, not KB Protocol v1, Registry Protocol
v1, Capture Protocol v1 or a new MCP transport version. No capture capability is
required for discovery/retrieval-only setup or documentation reads. The account
ID is supplied by authenticated server context, never a caller-selected identity.
The existing registry `check_connection` response already has a user ID; use the
same identity authority rather than defining a second account system.

Proposed page response:

```json
{
  "uri": "system-wiki://index.md",
  "mimeType": "text/markdown",
  "text": "<complete Markdown page>",
  "content_revision": "<same documentation bundle revision>",
  "cache_visibility": "public_guidance"
}
```

Only reviewed, account-independent general guidance may declare
`public_guidance`. An absent/unknown visibility is treated as protected. Never
mark KB pages, inventories, account details or personalised instructions public.
Reject path traversal, absolute paths, fragments, wrong schemes and files outside
the packaged Markdown root. A read/list response is read-only and must not load
the wiki review database, capture client or a KB connection.

Unsupported contract versions, missing tools and unknown methods mean the
replacement is unavailable. Keep packaged retrieval guidance; do not invent an
endpoint or substitute a KB wiki. Authentication denial is a distinct result from
outage and must never be converted into cache authorisation.

## Loading and caching

Proposed initial defaults: 24-hour freshness and at most seven days of stale
reuse for explicitly public guidance. These are reviewable defaults, not existing
runtime settings or measured performance claims.

1. Identify the actual surface, execution environment and configured MCP Service
   connection. For a verified startup mechanism, authenticate the descriptor once
   per fresh session. This is not registry reconciliation: do not enumerate KBs.
2. Partition cache entries by normalized service origin, authenticated account ID,
   configured connection/auth binding, contract version, content revision and URI.
   Never store tokens or use display names/email as identity. If the client cannot
   detect account or credential changes reliably, do not reuse its disk cache.
3. Reuse a fresh index only when identity and descriptor revision match. Otherwise
   read the index once and replace the entry atomically. Fetch linked detail only
   as the task requires it. Do not preload every page or retry on each turn.
4. Use a five-second total startup budget as an initial target. Timeouts, 5xx and
   network failure fall back to eligible cached public guidance; otherwise use the
   packaged minimal guidance. Offline cache reuse additionally requires a trusted
   unchanged account/auth binding supplied by the client. Without it, use packaged
   fallback. Record which path loaded without logging page content or credentials.
5. A 401/403, account switch, logout, changed auth binding or explicit revocation
   invalidates that connection's cache eligibility immediately, including entries
   still within TTL. Use packaged fallback and report reconnect needs when relevant.
   Do not clear other accounts' or KBs' working configuration.
6. Protected or unknown-visibility responses are not eligible for persistent or
   outage cache reuse in v1. They may be used following a successful authenticated
   read in the current session. A restart requires a new authenticated read.
7. Expiry is checked against stored fetch time; clock rollback makes an entry
   ineligible. Atomic writes, private cache permissions, bounded payloads and
   concurrent starts must be tested before deployment.

Public guidance here is a cache classification, not a public anonymous endpoint.
The authenticated MCP transport remains required. TTL never grants permission
to a protected KB. Authorisation failures from a KB invalidate that KB's retrieval
eligibility, not the separate system documentation or another KB's access.

Version 1 limits proposed for implementation: index at most 8 KiB UTF-8, individual
detail page at most 64 KiB, cached bundle at most 1 MiB. Exceeding a bound triggers
packaged fallback for startup, not silent truncation. Index content should be a
short navigation map. Report actual injected characters/tokens, fetch calls and
latency per surface; tune the defaults using measured results before retirement.

## Draft bootstrap and fallback

These blocks are proposed managed content, not instructions installed by this
phase. Generate inventory separately from entitled registry records during
explicit setup/reconciliation. Do not hard-code Bruno's private KB in the generic
package. Keep the current runtime skills while verifying replacement behaviour.

Common block:

> Use the configured inventory to select only KBs relevant to the task. Call each
> KB Service directly. Start maintained-knowledge retrieval at its wiki index;
> explicit source-document requests may start with its corpus. Verify KB Protocol
> v1 and required capabilities once per service; a successful substantive call
> establishes the connection. Respect service access denials. Do not rediscover
> inventory on each conversation. Build and documentation writes follow the target
> service's guide, proposal schema and review rules.
>
> Load the system-wiki index through MCP Service's declared read-only interface
> when available; fetch detail only when needed. If unavailable, continue with
> this fallback and working direct KB connections. System guidance does not grant
> access or authority to write a KB. Do not generate conversation references or
> tags, call capture tools for routine replies, evaluate capture policy, or process
> in-chat capture include/exclude commands.

Before replacement loading is proven, the packaged block additionally retains:

> Invoke `use-kbs` and follow `use-standard-kb` for relevant configured KBs.

The descriptor's index URI is the authority; a managed block must not tell an old
server to call a nonexistent tool. Setup selects declared-interface loading or
the explicit packaged fallback and records which was configured.

Surface additions:

| Actual session | Additional managed wording and setup scope |
| --- | --- |
| Local Codex CLI/desktop | “External local session-history capture is configured and verified separately for this surface and machine.” Retain existing Codex OAuth connections. Only a verified local supported environment can enter capture setup. |
| Local Claude Code CLI/desktop Code tab | Same external-capture wording; preserve Claude Code OAuth servers and unrelated hooks. Changes to personal `~/.claude/CLAUDE.md` require Bruno's approval. |
| Cloud Codex / cloud Claude Code, including tasks viewed in desktop apps | “This environment receives retrieval setup only; no local capture client is configured here.” Use its supported instructions/settings; do not copy laptop hooks or credentials. |
| ChatGPT web/desktop/mobile and Claude Chat web/desktop/mobile | Same retrieval-only wording. Reconcile account preferences separately from Code stores. Human paste into Capture Review remains optional and outside setup. |
| Open WebUI | Preserve its filter/OAuth and deployment persistence workflow. No plugin startup loop or ordinary model-driven KB tool attachment. Any future system-guidance integration belongs to that filter's separate project. |

Unknown execution location defaults to retrieval-only work until established;
identify the surface rather than inferring locality from an app's name. Do not
claim external capture is active just because the explanatory wording is present.

## Client adapters and rollout

No new hook or client setting is specified here as already supported. A startup
adapter is eligible only after its exact mechanism is verified in the current
client/version and a fresh session. It must compose with existing unrelated hooks
and remain separate from capture. Where injection is unavailable, configure a
short static load instruction and report that weaker fallback.

Phase 3 in kb-plugins should first implement pure, independently testable setup
logic: surface/execution routing; package/inventory diagnostics; identity and
callback/scope comparison from actual connection values; separate retrieval,
guidance and local-capture readiness; and managed-block rendering. Persist only
through supported client stores with preservation/idempotency checks. An outage
or unentitled response is not authority to remove a working service. Account
grants and user tool permissions remain distinct from authentication success.

The personal-rag phase then implements versioned documentation content, the
read-only interface and server-side validation/tests, followed by its own approved
deployment. Only afterward wire and prove startup/cache adapters on each surface.
Do not trim `use-kbs`/`use-standard-kb` until replacement and fallback acceptance
passes. Publishing a plugin version, installing it and proving live behaviour are
separate later milestones.

## Acceptance matrix

| Target | Independent evidence required before completion |
| --- | --- |
| Local Codex CLI | Authenticated KB capability and wiki read; fresh startup injection/fallback; capture hook/receipt verified separately |
| Local Codex desktop | Same tests in a fresh desktop session; CLI success is insufficient |
| Local Claude Code CLI | Same tests with that CLI's actual authentication and hooks |
| Local Claude desktop Code tab | Same tests in a local Code-tab session; ordinary Chat is separate |
| Cloud Codex and cloud Claude Code | Test each independently, including desktop-viewed cloud task: direct retrieval and guidance pass with capture tools absent; no capture credentials/hooks/tests |
| ChatGPT and Claude chat | Test each applicable account-preference store and real retrieval tools; no hook/install/capture acceptance requirement |
| Open WebUI | Preserve existing filter/server capture; no plugin retrieval duplication; separately consult owui-deploy for any integration changes |

Contract/cache cases: tools/resources return equal content; namespace isolation;
unsupported version; absent tools; same-account cache hit; two accounts at one
origin; two origins; account/auth switch; 401/403 with fresh and stale entries;
timeout/5xx with and without eligible public cache; protected page refusal; expiry
and clock rollback; revision mismatch; partial response; oversized content;
concurrent starts and atomic cache replacement. Keep registry discovery out of
normal startup and all per-turn paths.

Setup cases: fresh/repeat setup; entitled addition and actual revocation versus
registry outage; duplicate installations; exact callback identity; denied grant;
successful login but failed capability/wiki read; unrelated-config preservation;
independent readiness results. Capture regression coverage stays independent.

## PKB documentation rejection and recovery boundary

Phase 2 does not repair an open PKB wiki session. In the inspected source,
automatic publication refuses to create a session when one is already open. The
message alone does not identify whether it is normal human review or interrupted
automatic publication, and does not prove the deployment matches this checkout.

The source records proposals before attempting automatic publication, and marks
them rejected when session creation fails. Therefore the earlier statement that
no queue/database record was created was too strong. The tool confirmed neither
publication nor an accepted pending update; rejected audit rows may exist.

For an active human review session, use its normal review/merge/discard flow.
Operator recovery is reserved for interrupted automatic/lifecycle sessions: it
can reconcile an already-published branch without replaying it; discarding an
unpublished batch requires inspecting its contents first. Do not change a user's
session, silently publish old work, edit a local wiki mirror or deploy backend
changes to clear a documentation failure. Every VPS mutation still needs its
separate approval. No recovery tool is exposed by this session's PKB connection.

Keep the complete proposed update locally, including the intended section and
the error. After session resolution, re-read the live target and reconcile edits
before one resubmission through the canonical proposal tool. Report applied,
pending, rejected and unknown outcomes distinctly; tool errors may follow durable
writes, so a retry must not assume no side effects. This handling is part of
documentation workflow reliability, not a prerequisite for retrieval/setup work.

## Review decisions

Approved for phase 3: a distinct `system-wiki://` read-only contract and tool
pair with descriptor; existing authenticated MCP transport; public-guidance-only
outage cache with strict account/auth isolation; 24-hour/7-day freshness bounds;
bounded startup with packaged fallback; and separate readiness results per surface.

Approval of this design permits the kb-plugins implementation phase. It does not
approve personal-rag deployment, live client installation, hook changes, PKB
session recovery or any VPS mutation.

Bruno also confirmed that an empty review session must not block automatic
publication. This is a personal-rag lifecycle change, recorded in the
[review-app handover](personal-rag-review-history-brief.md). It requires a locked
check for actual unpublished work, not just an open-session row. It is not
implemented by the plugin or permission to discard a nonempty review session.
