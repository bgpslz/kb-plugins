> Historical record: the canonical project has moved to
> `projects/knowledge-base-system/`. Do not submit this old full-section draft
> to the deprecated personal-rag compatibility page. Reconcile against the live
> component page; see [current status](setup-implementation.md).

# Personal-KB supplement — not yet submitted

22 October 2026. Complete revised section for `projects/personal-rag-system.md`,
anchor `sec_fec4dd`, preserving the earlier architecture signals.

Proposal 53 already targets this section and is pending human review. The exposed
proposal tool has no amendment operation. This updated draft is retained locally
to avoid creating a competing same-section proposal. After proposal 53 is resolved,
re-read the live section, reconcile intervening edits and submit the current status
through the canonical proposal service. This supplement is not published or queued.

## Revised section content

<a id="sec_fec4dd"></a>
## Current Architecture Signals

- DuckDB is a core component.
- Qdrant is a core component.
- MCP is a core component.
- CLI access is a core part of the system.
- Local-first ingestion is mostly applicable.
- Retrieval uses lexical, vector, or hybrid search depending on a sophisticated heuristic.
- A manual override option exists for search mode.
- `metadata.duckdb` is the metadata source of truth, including provenance.
- The system is initially for Bruno as one user, but is designed to cope with small multi-user usage, up to four users per machine.
- Provisional (Gemini-sourced, see [2026-07-21 Gemini Memory Summary](/sources/2026-07-21-gemini-memory-summary.md)): deterministic or regex heuristics should run before the LLM in query parsing and retrieval, with the LLM invoked afterward for semantic enrichment or filter merging; this matches the existing lexical/vector/hybrid heuristic above rather than replacing it.
- Provisional: the system should inject dynamic temporal context explicitly (e.g. "today", start-of-month) rather than operating time-blind, and should enforce structured output via schema/JSON-mode constraints with regex fallbacks.

### KB plugin alignment — 22 October 2026

Bruno authorised starting the plugin architecture alignment. The first phase audited source packages, local installations, active skill discovery and instruction stores, and added a read-only package consistency check. Both source packages remain at 1.3.4 with five skills; runtime guidance has not been retired or rewritten. The local Codex session exposed two identical 1.3.4 distribution paths; Claude's local install registry selected 1.3.3, which lacks the development-documentation skill. These observations do not establish the state of other machines or fresh sessions.

The agreed architecture keeps the plugin focused on installation, configuration, repair and explicit build/development workflows. Shared guidance is planned for a separate system wiki maintained with the service code and served read-only by MCP Service. That wiki is distinct from personal and organisation KB wikis. Its interface and startup-loading mechanism remain to be agreed and implemented.

Capture is independent of model behaviour. Supported local Codex and Claude Code sessions use separately verified external session-history capture. Cloud Code and ChatGPT/Claude chat receive retrieval setup only; a desktop interface does not establish local execution. Open WebUI retains its separate server-side capture and retrieval filter. Human transcript paste is optional, not automatic collection.

The audit found setup instructions that still require central capture checks and local intake before completing retrieval configuration. Those dependencies must be separated, alongside explicit surface/execution detection and authenticated capability/wiki-read verification. Existing capture code and package copies match; seven capture regression tests passed. Live capture delivery, other clients, deployments and startup injection were not verified.

Bruno approved the phase 2 bootstrap/system-wiki design and authorised phase 3. The setup foundation is now implemented in unreleased plugin source: a shared standard-library evidence evaluator, per-surface readiness reporting, exact OAuth callback/resource/scope diagnostics, installation/connection checks and managed-instruction drafts that preserve unrelated text. Native local Code adapters now discover configured scopes and enabled plugin endpoints, avoid duplicate additions, and offer explicit additive persistence with stale-plan checks, private backups, permission preservation and read-back verification. Both packages are generated from the same setup sources. Retrieval acceptance is independent of local capture, and Open WebUI receives no extra model-driven retrieval loop. Forty-four setup tests and seven capture regression tests pass.

Real read-only inspection located Codex's user PKB/MCP Service entries and Claude Code's enabled plugin entries. Native CLI format smoke tests used temporary configuration or one-off overrides and did not alter real settings. Persistence support covers the tested local POSIX stores; account/cloud preferences, custom Claude directories, managed-policy/trust checks and actual OAuth login still use each client's native/manual flow. No credential store is read by the adapter. Runtime retrieval skills and real installed configuration remain unchanged; authenticated new-connection and fresh-session acceptance are still separate tests. The next dependency is the separately implemented and approved personal-rag system-wiki reader/content release, for which a concrete implementation brief is prepared, followed by client loader/cache work, per-surface startup proof and plugin publication/installation.

Bruno also confirmed that a harmless empty human wiki review session must not block otherwise authorised automatic publication. The personal-rag handover now calls for locked checks for actual unpublished/dirty work and preservation of accepted work and decision history. This backend fix is not implemented or deployed by the plugin work. Phase approval does not waive separate deployment, installation or VPS mutation gates.

Subsequent client work adds an inactive system-wiki loading/cache core behind a native authenticated async bridge. It validates account/revision, persists only explicitly public guidance, invalidates eligibility on auth denial or account/auth-binding change, bounds outage reuse and startup transport time, and falls back to packaged retrieval guidance. The complete source setup suite now has 76 passing tests, alongside seven unchanged capture regressions. The core reads no credential store and installs no hook. A trusted host account/auth binding is required for persistent reuse. Backend tools and a verified native startup bridge are still absent from this chat's observed interface, so authenticated integration and per-surface fresh-session proof remain outstanding. The user-identified parallel chat's recent visible work concerns review history/lazy sessions; it does not yet establish the separate system-wiki serving interface.
