# Handover: align KB plugins and skills with the current architecture

Prepared for work in `kb-plugins`, 22 October 2026.

## Objective and scope

Retain the KBs plugin as a small installation, configuration, repair and explicit
workflow package. Reduce duplicated runtime instructions and move general system
guidance into the planned system wiki. The objective is reliable setup and use
across AI clients, not preserving the existing number of skills.

This is a handover, not a record that restructuring has been implemented or
deployed. Bruno requested that the plugin work be handled in this project.
The component boundaries below are established; the proposed implementation
details and open choices should be reviewed before substantive restructuring.
Do not implement unrelated onboarding, authentication-provider migration or new
Windows/Linux capture installers.

Work normally on `main`. Preserve working connections, unrelated instructions,
hooks and capture receipts. Do not edit generated plugin-cache files as a release
method. Source changes, published packages, installed packages and live behaviour
are separate states and must be reported separately.

## Explicit scope by client and execution environment — Bruno's clarification

| Client/surface | Retrieval configuration | Capture configuration in this work |
| --- | --- | --- |
| Local Codex CLI and desktop sessions | Direct KB connections and appropriate runtime guidance | External local session-history capture, verified separately per surface |
| Local Claude Code CLI and desktop Code-tab sessions | Direct KB connections and appropriate runtime guidance | External local session-history capture, verified separately per surface |
| Cloud Codex sessions | Direct KB connections and appropriate runtime guidance | None: retrieval only |
| Cloud Claude Code sessions | Direct KB connections and appropriate runtime guidance | None: retrieval only |
| ChatGPT web, desktop and mobile chat | KB connections and retrieval guidance only | None: do not configure chat capture |
| Claude web, desktop Chat and mobile chat | KB connections and retrieval guidance only | None: do not configure chat capture |
| Open WebUI | Its existing automatic retrieval filter and OAuth connections | Its separate server-side capture integration; preserve rather than recreate it in a skill |

Claude desktop Chat and its Code tab are different surfaces. Likewise, Codex and
ChatGPT chat must not be conflated merely because they share OpenAI packaging or
an application brand. Identify both the actual surface and where the Code session
runs before proposing setup actions. A cloud Code task viewed in a desktop app
remains retrieval only; the local UI does not establish local execution or access
to local session history.
The original model-driven capture plan is superseded: no skill should make an
assistant capture a conversation. Manual paste remains an optional human workflow
outside chat and cloud Code configuration, not evidence of automatic capture.

## Architecture to preserve

### Services and data

- **MCP Service** owns identity, the Knowledge Registry, entitlements and central
  conversation-capture ingress. It exposes setup/reconciliation tools and the
  canonical `capture_chat_turn`. Capture is user-scoped and occurs before a
  human chooses KB destinations. It does not proxy KB retrieval or KB wikis.
- **Each KB Service** exposes its own wiki, RAG retrieval, capabilities and build
  guidance. Bruno's PKB and Summerleaze OKB have separate content, stores,
  authority, lifecycle and runtime access checks despite sharing application code.
- Wiki content is Git-managed Markdown; RAG uses tenant-scoped DuckDB and derived
  Qdrant indexes. The plugin owns neither source data nor retrieval algorithms.
- **Capture Review Application** owns the human choice of destinations, reviewed
  artifacts and routing into KB ingestion/wiki assessment. Bootstrap can block
  delivery to Summerleaze without blocking central collection of conversations.

### Capture is outside model behaviour

- Open WebUI captures turns server-side. Its capture filter strips injected
  `<kb-context>` before queuing the original conversation.
- Local Codex and Claude Code use session-history capture, with installed hooks
  and a scheduled backstop. The existing implementation supports macOS only.
- Cloud Codex, cloud Claude Code, ChatGPT and Claude chat receive retrieval setup
  only. Do not install capture hooks or capture-client credentials there, add
  capture directives to their profiles, require a capture test, or claim those
  sessions are collected. A user can separately choose
  to paste a transcript into Capture Review; that is outside this setup scope.
  An MCP Service discovery/reconciliation connection may still be needed; that
  connection is not configuration of a chat-capture client. Where supported,
  expose only the relevant discovery/retrieval tools to these retrieval-only surfaces;
  retain central capture tools for the external capture clients that need them.
- Never restore model-generated conversation references, KB_ref tags, routine
  capture-tool calls, per-KB capture fan-out, in-chat include/exclude commands or
  model evaluation of `capture_policy`. That field is human-review metadata.
- The local capture client's credential is separate from retrieval OAuth.

The current 1.3.4 package already reflects much of this change. Its capture
installer/runtime is useful software supporting the replacement strategy, not
obsolete model-driven capture logic to delete.

### Retrieval differs by client

- Open WebUI uses an automatic retrieval filter and per-user OAuth connections.
  Keep its MCP connections available to the filter but unattached to ordinary
  chats/models for native model-driven tool calling. The filter plans, traverses
  wikis and injects evidence. Do not add a second plugin retrieval loop there.
- Coding assistants call relevant KB Services directly and need concise guidance
  about KB selection, wiki-first retrieval and source evidence.
- Normal maintained-knowledge retrieval starts with the wiki; explicit requests
  for source documents may start with the corpus. Open WebUI's particular RAG
  gate is wiki insufficiency **and** an open-ended question. Do not accidentally
  make that filter-specific gate forbid legitimate source retrieval elsewhere.
- Runtime authorization belongs to each KB Service. A cached inventory or a
  registry entitlement is not permission to bypass a service's 401/403 response.
  Establish per-service connection state once after success; avoid repeated
  preflight checks and repeated registry discovery on every conversation.

## Current evidence and outstanding commissioning

Treat these as dated observations, not a substitute for a fresh setup audit:

- `kb-plugins` source is 1.3.4, baseline `a490b4a`. Both platform packages contain
  five skills: `setup-kbs`, `use-kbs`, `use-standard-kb`, `build-kb` and
  `maintain-project-docs`. Setup still says "four"; fix that stale assumption.
- Claude's `.mcp.json` bundles MCP Service and Bruno's PKB only. OpenAI/Codex uses
  registered app mappings or separately configured OAuth servers by surface.
  Existing hard-coded personal-PKB examples are not a general tenant inventory.
- The current setup skills already reconcile entitlements, preserve connections,
  distinguish cloud/local instructions, install local capture and check protocol
  compatibility. Much connection setup is still written guidance rather than
  tested automation. Do not describe a general setup utility as already built.
- Open WebUI's separate repository records capture/retrieval installation and
  initial live tests on 21 October. Its current planner override, worker and time
  budget have evolved since the original filter brief. Consult `owui-deploy`
  before describing live settings; do not bake those defaults into plugin skills.
- Summerleaze's endpoint is `https://slz-kb.summerleaze.com/mcp`; its service ID is
  `slzkb`. Bruno confirmed successful Open WebUI authorization/access on 22 October.
  The Open WebUI connection ID is `slzkb_service`, which is distinct from service ID.
- A callback mismatch was repaired by allowing the exact callback derived from
  that connection ID. The old `slzkb` callback and existing PKB/MCP Service callbacks
  were preserved. This is a concrete setup-validation case to automate.
- The legacy capture boundary fix was deployed in `personal-rag` at `920fb45` on
  21 October: SLZKB constructs 16 tools and six capabilities (`wiki`, `rag`,
  `documents`, `tables`, `x`, `build`), with no capture handler or local capture
  instruction. Only Bruno's existing personal `bruno`/`pkb` instance retains
  legacy compatibility. MCP Service central capture is unaffected.
- On 22 October, the registry still listed only My PKB for Bruno. Codex had PKB
  and MCP Service entries; Claude Code's plugin supplied those same two. Neither
  had an SLZKB connection. Auth0 showed no SLZKB scope grants for the displayed
  Codex/Claude Code applications. Identify the actual client used by a new login;
  do not grant every similarly named application or reuse Open WebUI's secret.
- Successful browser login is not sufficient acceptance. Verify an authenticated
  capability response and wiki read. Direct KB access can work before registry
  discovery, but automatic configured inventory still needs reconciliation.

Further registry grants and client authorizations are not accomplished by editing
this plugin. The personal-rag rollout retains separate approval gates.

## Recommended restructuring

### 1. Keep and strengthen `setup-kbs`

Make it the explicit entry point for install, check, add a newly entitled KB,
repair/reconnect and reconcile. Keep orchestration concise; move repeatable,
fragile operations into tested scripts with small client-specific adapters.

The setup workflow should:

1. Detect the client, actual execution environment (local or cloud), machine,
   active plugin/version and applicable configuration stores. Do not infer local
   execution from a desktop interface. Find duplicates without automatically
   uninstalling anything.
2. Establish the MCP Service bootstrap connection, then fetch entitled KBs during
   setup/reconciliation. Preserve already configured retrieval during outages.
   Cloud Code and ChatGPT/Claude-chat setup use this for discovery/reconciliation
   only; do not
   require central capture capabilities or capture-specific credentials/tests as
   a condition of completing retrieval-only setup.
3. Compare discovered KB identities with existing client connections. Distinguish
   immutable KB UID, service ID, display name, connection ID and OAuth client ID.
4. Generate supported client settings, exact callbacks and explicit API scopes
   from actual connection values. Prefer native OAuth login and credential stores.
   Never ask users to paste secrets in chat or include secrets in logs/commands.
5. Guide sign-in, diagnose broker/resource/scope/callback failures, and distinguish
   user sign-in from missing administrator-side app approval or KB entitlement.
6. Verify declared protocol/capabilities and a substantive authenticated wiki read.
   Do not require `capture` on a KB Service; central capture has a separate contract.
7. Persist settings through the client's supported mechanism and verify survival
   where possible. In Open WebUI's current environment-authoritative deployment,
   use its existing persistence workflow before any restart.
8. Reconcile only the managed bootstrap/inventory instructions, preserving other
   user/project rules. Personal `~/.claude/CLAUDE.md` edits need Bruno's approval.
9. Install or check external capture separately where supported, preserving its
   original capture boundary, receipts, exclusions and unrelated hooks. Run this
   step only for supported local Codex/Claude Code sessions. Cloud Code, ChatGPT
   and Claude chat require retrieval setup only.
10. Report connection readiness, guidance loading and capture readiness separately,
    including independent cloud/desktop/CLI/machine results.

Do not make retrieval setup depend on capture being supported or healthy. Do not
turn this into a general-purpose AI-client configuration manager. Account grants,
tool approvals and consequential external actions still require applicable consent;
do not hard-code "Allow all tools" as a default merely to suppress prompts.

### 2. Replace heavy runtime instructions with a bootstrap and system wiki

The planned canonical **system wiki belongs in personal-rag**, shipped through
its normal release chain and served read-only by MCP Service. It is distinct
from Bruno's PKB wiki, Summerleaze OKB wiki and the llm-wiki template. Serving
MCP Service's own documentation does not authorise proxying KB content.

Use that wiki for shared user/assistant guidance: system roles; KB selection and
retrieval; capture/review; access and reconnecting; supported surfaces; context
needs by surface; and glossary. Provide a browser-readable form from the same
content if useful rather than maintaining a second manual.

The plugin should retain enough packaged setup/fallback guidance to work before
that wiki is reachable. Normal startup should supply a short index and fetch
detail only when needed. Keep KB-specific capabilities, tool contracts, build
guides and authorization rules in each KB Service.

Write bootstrap/profile content specific to the surface and execution environment.
Cloud Code, ChatGPT and Claude-chat instructions cover retrieval only and must not
inherit local coding-capture installation or model-driven capture duties. Local
coding-client bootstrap may explain
that an external capture client handles retention without asking the model to do it.

Shrink or retire the always-invoked `use-kbs`, and move `use-standard-kb`'s general
rules to the system wiki, only after the replacement is proven. Avoid repeating
the same material in skills, global instructions, server initialization and every
tool description. A minimal fallback can preserve retrieval during outages.

### 3. Add session-start loading only where verified

Fetch the system-wiki index from MCP Service on supported coding surfaces, cache
with a TTL, fail softly to the cache and preserve unrelated hooks. Keep caches
separate for different accounts/services; handle authorization failures without
silently serving protected stale content. Do not add per-turn registry checks.

A retrieval-guidance startup mechanism is separate from a capture hook. Cloud
Code may load retrieval guidance through a verified supported mechanism, but must
not install a local capture client or imply that cloud session history is captured.

The 19 October temporary hook audit covered local sessions and found:

| Surface | Evidence then |
| --- | --- |
| Codex CLI | Context injection passed |
| Codex desktop | Unverified; computer-use boundary prevented the test |
| Claude Code CLI | Hook ran; expired model login blocked injection proof |
| Claude desktop Code tab | Context injection passed |

Re-test current installed versions and fresh sessions. These were separate tests,
not proof that CLI results apply to desktop or cloud sessions. Temporary test
hooks were removed.
Use a short static instruction to load the index where injection is unavailable;
report it as a weaker fallback. Do not retire working instructions until verified.

### 4. Retain explicit build and development workflows

- Keep `build-kb` small and explicit. Select the target KB, read existing coverage,
  obtain its `get_build_guide`, identify gaps and submit sourced proposals under
  that service's actual lifecycle/write contract. No personal/organisation-specific
  interview catalogue belongs in the plugin. Builders do not inherit personal
  owner auto-publication privileges; organisation changes require human review.
- Keep `maintain-project-docs` for authorised repository development. Preserve
  complete repository documentation and distilled owner-PKB project knowledge.
  For this system, general user guidance belongs in the system wiki; genuinely
  organisation-specific knowledge may still belong in Summerleaze OKB wiki under
  human review. Do not publish private development details to all OKB readers.

### 5. Retain the package; keep an escape route

Use the plugin to distribute versioned skills, setup resources and supported
hooks/connections. Do not require a fresh plugin release or hard-code a private
tenant connection into every package whenever a user gains a KB entitlement.
Reconcile user-specific connection configuration from registry metadata using
supported client stores, without duplicating existing bundled servers.

Make the same setup checks available through a standalone command and documented
manual path where plugins are unavailable. The website/command and plugin should
share implementation/content rather than becoming competing setup procedures.
This is a proposed improvement, not an existing delivered interface.

## Dependencies and implementation sequence

1. Inventory source, installed packages, active skill discovery and instructions.
   Preserve useful setup/capture code; identify stale wording and duplication.
2. Agree the short bootstrap and cross-repository system-wiki interface. Define
   canonical URIs/list/read tools and caching/authentication before wiring hooks;
   do not invent an endpoint and claim it is deployed.
3. Implement and test setup checks/adapters in kb-plugins. Package copies should
   be generated or checked against one maintained source, as local-capture is now.
4. Implement the canonical system wiki/read-only serving separately in personal-rag,
   with its own tests and approved deployment. Keep plugin fallbacks meanwhile.
5. Prove session-start loading on each supported surface, then trim skills and
   managed instruction blocks. Do not repeat or alter working capture installations.
6. Publish/install a new plugin version through supported mechanisms; test fresh
   sessions and upgrade from the actual installed release. Reconcile other machines
   and cloud settings explicitly, rather than claiming a source commit updates them.

The original brief requires Bruno's approval between phases and explicit approval
for each VPS mutation command. This handover does not waive either requirement.
Routine local implementation choices can proceed within the authorised scope;
do not create extra approval gates merely from a recommendation in this document.

## Acceptance and completion criteria

- Fresh setup and repeat setup preserve working connections and unrelated config.
- Entitled KB addition, revocation, duplicate installations and partial outages are
  correctly diagnosed; client removal is not presented as server-side revocation.
- Exact callback generation, scopes/resource checks, denied broker grants and
  successful-login-but-failed-tool cases are covered without exposing credentials.
- Prove authenticated KB capability and wiki reads separately on each client.
- No KB capture requirement, no model-driven capture and no extra Open WebUI
  retrieval loop. Central capture and existing Bruno compatibility remain intact.
- For supported local Code sessions, capture installation, retry/deduplication,
  original boundary/exclusion preservation
  and receipt verification pass independently of retrieval readiness.
- Cloud Codex, cloud Claude Code, ChatGPT and Claude-chat setup completes using
  retrieval acceptance alone: no
  capture hooks, capture-only credentials, model capture directives or capture
  receipt requirements. Verify both Chat versus Code and local versus cloud Code
  routing explicitly, including a cloud task viewed through a desktop app.
- System-index injection, cache/outage fallback and unavailable-hook behaviour are
  checked in fresh sessions per surface. Keep instructions short and measure the
  context/latency cost rather than assuming it is negligible.
- Build/proposal approval, organisation bootstrap and developer-documentation
  behaviour remain correct; no hidden expansion of auto-publication permissions.
- Report tested source, package versions, installed versions, changed instruction
  stores, live deployments and remaining limitations separately.
- Update kb-plugins documentation and submit a distilled update to Bruno's PKB wiki
  through the canonical proposal service; report pending/failed publication clearly.

## Starting points

In this repository: `README.md`; both platform `skills/` directories;
`claude/kbs/.mcp.json`; `claude/kbs/hooks/hooks.json`; OpenAI package manifest/app
mappings; `local-capture/`; and the packaged setup scripts/reference copies.

In personal-rag: `TERMINOLOGY.md`, `ARCHITECTURE.md`, `OPERATIONS.md`,
`docs/knowledge_base_architecture.md`, `docs/kb_retrieval_capture_audit_20261019.md`,
`docs/open_webui_retrieval_phase2_implementation.md`,
`docs/kb_capture_boundary_audit_20261021.md`,
`docs/slzkb_capture_boundary_deployment.md` and `docs/oauth_auth_broker.md`.

In owui-deploy: `docs/kb-retrieval.md`, `README.md`, the capture/retrieval functions
and `save-tool-servers.sh`. Treat its latest implementation/deployment records as
the source for Open WebUI details, not older defaults reproduced in another repo.
