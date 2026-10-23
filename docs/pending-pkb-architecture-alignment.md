> Historical record: the canonical project has moved to
> `projects/knowledge-base-system/`. Do not submit this old full-section draft
> to the deprecated personal-rag compatibility page. Reconcile against the live
> component page; see [current status](setup-implementation.md).

# Personal-KB documentation update — pending review

Current status, 22 October 2026: proposal **53**, origin
`a01e91eb040e455ea4fb58ecab8dc5a7`, accepted by PKB Service as **pending human review**.
It has not been published. Target: `projects/personal-rag-system.md`,
section `sec_fec4dd`. The live target was re-read before resubmission.

Subsequent phase 2 approval and phase 3 source changes are recorded in the
[unsent supplement](pending-pkb-setup-foundation.md). The text below is the exact
earlier submission; it has not been silently changed to imply proposal 53 was amended.

The original automatic attempt was rejected because a review session was open.
Bruno subsequently merged the three approved proposals. A fresh read-only merge
preview then showed zero approved changes and no net file differences, while
automatic publication still reported an open session. Source shows that the
review page creates a session when visited; returning there after Merge can
therefore recreate an empty session. No session was closed or recovered here.

A subsequent explicit `auto_apply=false` request successfully queued proposal 53
through the normal review workflow. Rejected rows from earlier automatic attempts
may exist; those attempts did not confirm publication or an accepted pending
update. Do not retry this pending proposal as another submission.

## Submitted section content

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

Bruno then authorised phase 2. A draft now proposes a short bootstrap, separate read-only system-wiki interface, account-isolated public-guidance cache with authentication-failure invalidation, packaged fallback and per-surface acceptance matrix. Its interface names and defaults remain proposals for design review before phase 3; no endpoint or loader is implemented or deployed. Bruno merged the three previously approved changes. A subsequent live preview showed zero approved changes and no net file differences, but an open session still prevented automatic publication. This update was therefore submitted for ordinary human review. A separate feature brief for session changes and decision history was prepared for personal-rag; implementation and deployment of that feature are outside this plugin work. Bruno's approval between phases and separate service-deployment gates remain in force. No installed configuration, OAuth connections, capture hooks or live deployments were changed during these phases.
