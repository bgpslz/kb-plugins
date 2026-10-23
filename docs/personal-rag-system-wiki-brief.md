# Brief for personal-rag: canonical read-only system wiki

22 October 2026. Bruno approved the
[bootstrap/interface design](system-wiki-bootstrap-contract.md) and requested
this implementation handover. Implementation belongs in **personal-rag**; this
brief neither changes that repository nor authorises deployment/VPS mutations.

Status clarification: Bruno subsequently reported that this implementation is well
advanced in personal-rag. Use this brief as the approved integration reference,
not as a new instruction to duplicate or restart the backend work. Reconcile with
its actual implementation and deployment evidence before wiring client loaders.

## Outcome

Ship one Git-managed documentation bundle with the personal-rag application and
serve it read-only through MCP Service's existing authenticated MCP endpoint.
The plugin can then load a small index and fetch shared guidance as needed,
eventually reducing duplicated skill/profile/server instructions. Keep existing
plugin fallback/runtime guidance until loading and outage behaviour are proven
independently on every supported surface.

The system wiki is general operating guidance, distinct from Bruno's personal wiki,
Summerleaze's organisation wiki and the llm-wiki template. MCP Service still does
not proxy KB content or run KB search/ingestion/review workers. No model-driven
chat capture duties are introduced.

## Implement the approved contract

Use the exact descriptor/tool/URI fields in the approved design, not a second
interface. These names are approved for implementation, not currently deployed:

- `get_system_wiki_capabilities({})`: `service_id="mcp-service"`, authenticated
  stable `account_id`, `system_wiki_protocol_version=1`, capability
  `system_wiki_read`, `index_uri="system-wiki://index.md"`, immutable bundle
  `content_revision`.
- `list_system_wiki_pages({cursor?})`: paginated page URI/title/description.
- `read_system_wiki_page({uri})`: whole Markdown page, canonical URI, MIME type,
  text, matching bundle revision and explicit cache visibility.
- Equivalent MCP resources/list/read backed by the same reader and bytes. Add
  resource capability/dispatch through the existing authenticated session flow;
  retain tools for clients without resource access. Use standard MCP metadata
  encoding for revision/cache metadata and test tool/resource parity.

Reuse existing identity and authentication. `account_id` must come from the same
service-local authenticated user authority as registry `check_connection`, never
caller input or display name. Keep Registry Protocol v1, Capture Protocol v1 and
KB Protocol v1 independent of this new documentation contract. Retrieval-only
clients must not require central capture capabilities/credentials to read docs.

Mark reads/listing/descriptor read-only in MCP safety annotations. No write,
proposal, capture, arbitrary file-read, KB proxy or search operation belongs in
the documentation reader. Do not add a second account/token flow or an invented
HTTP documentation endpoint as a prerequisite.

## Content and packaging

Maintain the source bundle in personal-rag and include it in actual installed
release artifacts, not only the development checkout. Pick a small dedicated
package-data location consistent with that repository's build configuration.
Prove reads from an installed artifact with no source checkout available.
Version content deterministically with the bundle/release; all pages and the
descriptor for a release share the immutable revision. Avoid responses that mix
revisions during an upgrade.

Initial pages should cover:

1. A short index linking to focused details.
2. Service/component roles and identity terminology (KB UID, service ID,
   connection ID, OAuth client ID).
3. Relevant-KB selection, direct service access, wiki-first maintained knowledge,
   explicit source retrieval, protocol/capability checks and evidence handling.
4. Surface/execution differences: local Code versus cloud Code versus ordinary
   Chat, including a cloud task viewed through a desktop interface.
5. External capture and human review boundaries; capture policy as human-review
   metadata and optional human paste. No model capture calls/references/tags.
6. Access/reconnect troubleshooting and independent readiness results.
7. A glossary and links to the appropriate service-owned build/proposal guidance.

Keep private tenant data, inventories, credentials and operational development
details out. KB-specific build guides and authorisation rules stay in each KB
Service. Open WebUI retains its own retrieval filter and separate server capture;
its wiki-insufficiency/open-ended RAG gate must not become a universal prohibition
on source retrieval in other clients. Use current owui-deploy records for its
details rather than copying planner defaults here.

## Reader and cache boundary

Use a lightweight static reader, not the tenant wiki/review subsystem. Bind its
root server-side. Accept canonical listed `system-wiki://` Markdown URIs only;
reject traversal, encoded traversal, wrong schemes, fragments, absolute paths,
symlink escapes, unknown files and paths outside the bundle. Preserve whole-page
semantics. The reader must work without KB data directories or review databases.

The approved initial budgets are 8 KiB UTF-8 for the index, 64 KiB per detail
page and 1 MiB client cache; oversized startup guidance falls back rather than
being silently truncated. Public-cache eligibility requires the explicit
`cache_visibility="public_guidance"` marker on reviewed account-independent
guidance. Missing/unknown visibility is protected. An authenticated transport
does not make account data eligible for public caching.

The plugin owns the later client loader/cache: account/service/auth-binding
isolation, 24-hour freshness, at most seven days public stale reuse, five-second
initial startup budget, no protected outage reuse and invalidation on 401/403,
logout/account switch/revocation. This server task supplies the fields needed for
that behaviour. It must not implement per-turn registry discovery or retire the
packaged fallback before client acceptance.

## Source seams to inspect

- `src/personal_rag/knowledge_registry/tools.py`: present registry and capture
  definitions/dispatch, response envelopes and user identity.
- `src/personal_rag/knowledge_registry/http_app.py`: existing authenticated
  initialize/session/tool dispatch; currently tools-only capabilities.
- `src/personal_rag/mcp/metadata.py` and current annotation tests.
- Existing KB `wiki/mcp_resources.py` and `wiki/mcp_tools.py` for MCP response
  conventions only. Do not reuse their tenant-root/publication dependencies.
- Package-data configuration, normal release chain and registry HTTP tests.

The current source still has MCP Service initialization wording about eligible
turn capture. Replace outdated assistant capture directions with a short accurate
service-role/index pointer; keep external capture clients' canonical tools intact.
Do not inject the whole documentation bundle in initialize or every tool description.

## Acceptance and rollout

Test descriptor identity/version and wrong versions; authenticated/denied reads;
account separation; pagination; whole-page content; tool/resource metadata parity;
all path-boundary cases; deterministic revision; payload budgets; installed artifact
access and absence of KB/review/corpus side effects. Existing registry/capture
contracts and direct KB tools must continue to pass their regressions.

Report separately: tested source, packaged release, installed/deployed version,
changed server metadata and live authenticated descriptor/index read. Obtain the
applicable release/VPS approvals; approval of this design is not a deployment
receipt. A browser-readable form is optional if served from the same content,
not a second maintained manual.

After backend deployment, return the exact working descriptor, revision and live
test evidence to kb-plugins. The next client work is loader/cache implementation,
fresh-session proof per surface, measured context/latency costs, then trimming
runtime duplication and publishing/installing a plugin release.

## Separate review-app issue

The newer `docs/wiki_review_history_deployment_20261022.md` records Session
changes/Decision history deployed at source `1242501`, with an empty session still
open. That deployment does not claim the empty-session publication fix. Current
`wiki/publication.py` still rejects any open session when creating an automatic
one. The separately approved requirement remains in the
[review-app brief](personal-rag-review-history-brief.md): harmless empty human
sessions must not block otherwise authorised publication, with locked checks that
preserve actual unpublished work and decision history. Keep this lifecycle patch
independent of the read-only system wiki.
