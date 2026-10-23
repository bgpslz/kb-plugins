# PKB component update — submission failed, 23 October 2026

Destination: `projects/knowledge-base-system/kb-plugins.md` (whole page).
Requested through the canonical OAuth PKB Service proposal tool with
`auto_apply=true` under the authorised development-documentation workflow.

The service returned `isError=true`: Git refused the repository because of
`detected dubious ownership` at `/srv/llm-wiki/data/bruno`. No proposal ID or
publication receipt was returned. Durable proposal state is unknown; do not
blindly retry or run the server-suggested global Git exception. Re-read/reconcile
the canonical page and inspect proposal state after the service owner fixes its
repository access. No VPS change or recovery was attempted here.

Subsequent deployment addendum, 23 October: the backend metadata contract was
implemented at personal-rag bb13522 and deployed at c9ad645, including the native
resource request-metadata correction. Authenticated OAuth resource listing and
complete index/local-Codex reads now pass in this existing chat, with matching
source bytes and one revision. The two pages total 8,330 UTF-8 bytes. The final
backend correction passed 89 relevant tests and the six-case loader integration
script. Fresh-session startup, plugin installation and Open WebUI instruction
injection remain pending. No additional PKB proposal was attempted because the
previous repository-ownership failure has not been confirmed repaired. Before
any retry, reconcile this addendum with the live canonical page and inspect
unknown durable proposal state; the failed payload below is a historical snapshot.

The complete proposed page follows. It updates the current component page,
not the deprecated personal-rag compatibility page or old full-section drafts.

---

---
type: concept
title: KB Plugins Component
description: Generic client routing, setup, building, documentation maintenance and
  local capture.
status: draft
generated:
  by: openai/codex
  at: '2026-10-16T01:16:06Z'
private: true
sources:
- id: 2026-10-16-knowledge-base-system-development
  resource: /sources/2026-10-16-knowledge-base-system-development.md
  title: 2026-10-16 Knowledge Base System Development
---

# KB Plugins Component

The `kb-plugins` repository distributes the Knowledge Bases Plugin for ChatGPT/Codex and Claude clients. Its narrower role is setup, client adapters, system-instruction loading, minimal fallback and explicit KB build/development workflows. KB Services remain authoritative for retrieval, capabilities, access and proposals.

## Interfaces and constraints

Shared system operating guidance belongs in the Git-managed system wiki maintained with personal-rag and served read-only by MCP Service, distinct from personal and organisation knowledge wikis. Native startup requires the complete index plus the applicable surface page. Loading instructions is independent of retrieving task evidence from KBs.

Ordinary KB queries go directly to relevant KB Services. Registry reconciliation belongs to setup, not every conversation or turn. Preserve each surface's configured authentication; documentation loading must not introduce another login, scrape credentials or reuse the capture credential.

Open WebUI is Bruno's primary surface for capturable ordinary chat. Its separate filter owns retrieval and instruction delivery, with server-side capture. Its answering assistant must not add a second retrieval loop. Supported local Code capture is independently verified per machine/surface. Cloud Code and ordinary ChatGPT/Claude chat have no assumed automatic capture. Humans choose destinations in Capture Review; optional manual paste remains separate. Models do not generate capture references or routinely call capture tools.

## Current status — 23 October 2026

Bruno authorised continuing the plugin alignment against personal-rag's completion brief. Both source distributions now identify unreleased version 1.3.5. The current Codex chat still exposes installed 1.3.4 skill paths; this work changed no installed package, standing instruction store, connection, credential, hook or live service. Earlier client observations remain dated evidence, not acceptance for other clients.

The preserved setup foundation includes evidence evaluation, additive native adapters, endpoint reuse, exact identity/callback/scope checks, private backups, stale-plan refusal and preservation of unrelated settings. Retrieval readiness requires authenticated capabilities and a substantive wiki read; login or saved settings alone is insufficient.

The startup client now obtains index plus the correct surface with one descriptor, one content revision and one total startup budget. Missing pages or metadata, partial startup and mixed revisions produce a coherent short fallback. Cache isolation covers service, connection, account and trusted authentication binding; denials invalidate eligibility, and a failed upgrade cannot revive the older bundle during a later outage. Only explicitly public system guidance is persisted; no trusted binding means live-only operation.

The source use-kbs skill is a small instruction-based bootstrap, including restoration after compaction/resume or in separate agent contexts. It is weaker than deterministic host injection. The standalone retrieval manual remains packaged through staged acceptance and is not preloaded alongside successful wiki loading. Existing instructions in active sessions remain in force. Explicit build and development-documentation skills remain; shared user operating guidance is not copied into Summerleaze OKB wiki, while Bruno's PKB retains project-development knowledge.

All 88 setup tests and seven capture regressions passed, as did shared-source package checks and skill validation. These establish source behaviour, not live context delivery, OAuth commissioning, installed-version acceptance or capture receipts.

## Remaining work

Personal-rag's system-wiki reader and thirteen-page bundle exist. The inspected backend still lacks the descriptor, immutable bundle revision and page cache classifications required by the approved client. A narrow follow-up extends that existing reader, preserving its authentication and resource/tool parity. Source completion and its approved deployment are separate dependencies.

Prove an online uncached read and actual delivery of both required pages before useful work on the first native host. No authenticated native hook bridge or fresh-session model-context delivery is established here. Then verify live, cache, outage, denial, upgrade, account-switch and context-restoration paths independently per supported surface. Only after replacement acceptance reconcile installed/managed instruction sources, retire superseded guidance, publish/install and repeat acceptance.

A separate handover for owui-deploy covers actual answerer/planner/worker instruction inputs, role distinctions, transient injection, history/capture exclusions and bounded outage fallback. That work has not been implemented or deployed by this repository. Command-specific VPS approval and the separate personal Claude instruction approval remain in force.

Remaining machines/capture surfaces, native Windows/Linux credential and scheduler adapters, bundled-runtime installers and colleague rollout still require their own work.
