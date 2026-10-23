# Service-versioning project update — not submitted

Destination: projects/knowledge-base-system/decisions.md (whole page).
23 October 2026. The related explicit memory submission failed with the existing
wiki Git ownership error. Do not blindly retry; inspect unknown durable proposal
state and re-read this target before reconciliation. This full draft is retained
under the authorised project-documentation workflow; publication is unconfirmed.

Complete proposed page:

+---
type: project
title: Knowledge Base System Decisions
description: Significant system choices, rationale and development documentation workflow.
status: draft
generated:
  by: openai/codex
  at: '2026-10-16T01:16:06Z'
confidence: high
private: true
sources:
- id: 2026-06-09-chatgpt-memory-summary
  resource: /sources/2026-06-09-chatgpt-memory-summary.md
  title: 2026-06-09 ChatGPT Memory Summary
- id: 2026-06-10-personal-rag-system-status
  resource: /sources/2026-06-10-personal-rag-system-status.md
  title: 2026-06-10 Personal RAG System Status
- id: 2026-06-11-rag-provenance-replication
  resource: /sources/2026-06-11-rag-provenance-replication.md
  title: 2026-06-11 RAG Provenance Replication
- id: 2026-06-15-coding-agent-working-preferences
  resource: /sources/2026-06-15-coding-agent-working-preferences.md
  title: 2026-06-15 Coding Agent Working Preferences
- id: 2026-07-21-gemini-memory-summary
  resource: /sources/2026-07-21-gemini-memory-summary.md
  title: 2026-07-21 Gemini Memory Summary
- id: 2026-09-22-chatgpt-personal-rag-intent-summary
  resource: /sources/2026-09-22-chatgpt-personal-rag-intent-summary.md
  title: 2026-09-22 ChatGPT Personal RAG Intent And Capability Summary
- id: 2026-09-22-claude-personal-rag-history-and-intent-summary
  resource: /sources/2026-09-22-claude-personal-rag-history-and-intent-summary.md
  title: 2026-09-22 Claude Personal RAG History And Intent Summary
- id: 2026-10-16-knowledge-base-system-development
  resource: /sources/2026-10-16-knowledge-base-system-development.md
  title: 2026-10-16 Knowledge Base System Development
---

# Knowledge Base System Decisions

## Significant Decisions and Documentation Workflow

Build a smaller curated KB from selected sources rather than extending an indiscriminate archive. The existing candidate builder starts a fresh DuckDB, copies selected X dependencies without vector linkage, and leaves Gmail/Drive for fresh ingestion through curated labels and routes. That direction is established; fresh parallel Qdrant collections, a curated replacement wiki, EmbeddingGemma 2 and multimodal retrieval extend it.

The candidate must remain isolated from live writers. Pin the embedding space for both indexing and queries, validate the matched DuckDB/Qdrant/lexical/media/wiki set, then promote it with a retained complete rollback set. Equal vector dimensions do not make different embedding models compatible. Keep the existing compute/authority topology until a separate deployment decision changes it.

Maintain three independently intelligible documentation layers: full architecture, rationale, implementation and history in repositories; distilled architecture, important decisions/rationale, status, open questions, plans and workflows in Bruno's PKB; practical benefits, capabilities, limitations and usage in Summerleaze OKB. Information flows in that order, with audience-appropriate synthesis and no unnecessary duplication or cross-links between layers.

Normal material development maintains repository documentation as before and proposes the distilled personal update. The new source skills request explicit automatic application when warranted for an authenticated personal owner, explicit review when needed, or backend path defaults otherwise. Owner identity is an operator-managed service record, distinct from controller/builder membership. The policy page is always human-reviewed; organisation proposals cannot bypass human approval, including during initial build. Failed personal documentation updates must be reported; pending Summerleaze documentation review must not block development.

<a id="sec_e31e01"></a>
## Drafting Relevance

- Do not propose vector-only retrieval as if it were an obvious default.
- Preserve local-first ingestion as a mostly applicable default for the personal RAG system.
- Do not flatten the search strategy into generic "hybrid retrieval"; preserve the heuristic choice among lexical, vector, and hybrid modes, plus manual override.
- Avoid proposing architectures that add hidden state, opaque behaviour, or vendor lock-in without explicit trade-off analysis.
- When discussing new implementation ideas, compare them against the confirmed existing commitments rather than starting from a generic RAG architecture.
- Do not describe the deployment as simply "local and remote" if the functional distinction matters.
- Preserve the cost constraint that broader embedding should not move to `vps` unless the VPS capacity/cost trade-off changes.
- Respect DuckDB's effectively single-user access constraint when proposing replication, ingestion, or query-serving changes.
- Before proposing changes, inspect existing docs, schemas, enum values, helper APIs, and local naming conventions.
- Do not invent schema fields, enum values, abstractions, or retrieval conventions without checking existing definitions.
- Treat `metadata.duckdb` as the authoritative metadata and provenance store; Qdrant and other derived indexes should not become the sole source of truth.
- Preserve the boundary between authoritative local state and remote/read-only serving roles unless the architecture is explicitly being changed.
- Prefer metadata-aware, filterable, inspectable, and deterministic retrieval behaviour where possible.
- Use LLMs for planning, routing, drafting, and explanation, not as the authority for durable source records or computed facts.
- Provisional: keep the deterministic-heuristic-first / LLM-second ordering and explicit temporal-context injection above distinct from unreviewed Gemini generalisation; confirm against actual pipeline code before treating as settled architecture.

## One project across repositories

The wiki project is `projects/knowledge-base-system/`. The repositories are implementation components beneath it, alongside shared architecture, decisions and plans. Other coding and non-coding projects remain separate. Default automatic documentation approval is limited to this subtree; parent indexes and unrelated projects are outside that default.

During relocation, the old Personal RAG System path retains a small forwarding page for historical update-log links. Repair current backlinks and preserve old section anchors without rewriting the append-only log or keeping two competing project accounts.

## Development branches and wiki review branches

Confirmed by Bruno on 2026-10-16: normal development in personal-rag, kb-plugins and the llm-wiki application/template repository uses main directly. Branches are exceptional when changes need isolation; explain the reason to Bruno. With no other regular editors, routine development branches add unnecessary coordination.

Wiki content repositories managed by llm-wiki may use the same review-branch mechanism for both PKBs and OKBs. It supports coherent validation and multi-editor wikis. Approval authorisation differs by KB; the branching mechanism need not. Authorised personal automatic approval can complete publication without a separate human Merge action. Organisation updates require human approval. Always identify the repository and KB and distinguish pending proposals, review commits and publication to canonical main. This supersedes the suggestion to remove branches specifically for personal wikis.

Record material decisions when agreed, including workflow decisions without code changes, with rationale, scope and publication status. Repository guidance and these prepared drafts record this clarification; the existing queued proposals predate it and still need coherent amendment before publication. The development-documentation skill and automatic-approval service changes are prepared in source, not yet installed/deployed.


## Curated stores and implementation sequence

Keep the existing text chunking strategy and valid stored chunks; extra metadata
and the model transition do not themselves require re-chunking. Build fresh
EmbeddingGemma 2 vectors from the outset, with a dedicated candidate namespace,
rather than mixing legacy text-model vectors into the new index. A DuckDB-only
candidate is an explicitly incomplete build stage, not a usable curated KB;
acceptance requires matching derived indexes and the full recovery set.

Finish the existing approval/documentation baseline first to avoid competing
changes. Then deliver common schema/model runtime, the photograph vertical slice,
matched candidate acceptance/promotion and finally audio/video. Automatic approval
deployment improves the documentation workflow but is not a media runtime dependency.

## Service application versions and build identity — 23 October 2026

Bruno required consistent versions and self-reporting across personal-rag services, the standalone local capture collector and Open WebUI filters. Application versions are distinct from compatibility protocols, process/artifact build identities and the system-wiki content revision. Source implementations now provide service/version/package/build/Git/dirty metadata on HTTP health/version responses, MCP handshakes and authenticated probes, and safe CLI version/startup diagnostics. Metadata is captured at process startup or stamped into wheel artifacts, so an old running process cannot report a newer checkout's HEAD. Standalone collectors fingerprint their source and filters carry reproducible release-source stamps.

Codex and Claude Code should explicitly propose patch or minor bumps before committing significant component changes, naming affected components and old/new values with rationale. Compatible fixes normally warrant patches and compatible new features minors; breaking changes need a separate discussion. Keep this requirement prominent in AGENTS.md and CLAUDE.md and preserve separate deployment permissions. Documentation-only edits do not automatically require service bumps.

The source change proposes MCP Service 1.3.0, KB Service 1.1.0, initial maintained versions 0.1.0 for previously unversioned owned apps/jobs, package 0.10.0, local capture 1.1.0, filter retrieval/capture 0.3.0/0.4.0 and plugin distribution 1.4.0. All remain separate from running/installed releases. Third-party binaries retain upstream versions; retired capture/transcript paths remain retired. Local source validation passed 403 tests across repositories, plus capture and wheel/loader integration checks; one optional deployed-source snapshot test was skipped. This feature has not been deployed or installed.
