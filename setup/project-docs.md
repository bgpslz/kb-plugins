---
name: maintain-project-docs
description: Maintain repository documentation and route material development knowledge to the project's authorised system wiki, personal KB or organisation KB. Excludes ordinary KB retrieval.
metadata:
  version: "1.3.6"
  kb_protocol_version: 1
---

# Maintain project documentation

Use during material development work when the user has authorised a project documentation workflow and the documentation destinations are established. Do not invoke for ordinary retrieval, and do not invent a destination from the developer's identity.

Preserve the project's existing repository documentation contract, including architecture, implementation details, rationale, history, operations and outstanding work. Read the repository instructions and current documents first.

Choose destinations by the project's documentation policy and the content's audience. Preserve full repository documentation. For projects whose authorised workflow uses an owner's personal KB, distil relevant architecture, decisions, rationale, status, questions, plans and workflows there; use the organisation KB for appropriate organisation knowledge. Keep each account independently intelligible, without unnecessary duplication or cross-links. Repository-local provenance belongs in repository records; a wiki synthesis must be understandable without opening code or private source records.

For Bruno's KB system, shared explanations, architecture, plans, decisions and development histories belong in personal-rag's Git-managed system wiki, served read-only by MCP Service. Keep current explanations and histories in separate files linked within that bundle. Use plain English first; histories explain the problem, decision and outcome before technical detail. My PKB retains Bruno's personal purposes, priorities, preferences and original source evidence; do not recreate a parallel shared system account there. Organisation-specific knowledge belongs in the relevant organisation KB under its review rules, rather than duplicating general system documentation.

System-wiki changes currently use application source review and release. The canonical bundle is personal-rag's `src/personal_rag/system_wiki/content/`; follow that repository's `AGENTS.md` and `docs/system_wiki.md`. There is no implemented system-wiki proposal interface: do not route these edits through KB proposal tools. Source edits and review drafts are not deployed content. For the coordinated migration in `docs/wiki-reorganisation-20261115/REVIEW.md`, publish and verify replacement system pages before merging PKB reductions.

For personal or organisation KB updates, use the configured KB routing/authentication for this surface. Read the destination's root index and relevant existing pages, verify protocol v1 and wiki/build capabilities, and inspect the current proposal tool schema. Do not edit a local KB wiki mirror as a substitute for updating the canonical service. Do not change authentication or submit private content to a different KB after a failure.

Submit a coherent distilled KB update through the target KB service's proposal tool, including affected indexes. Treat a coding task that already authorises this workflow as permission to submit its documentation proposals; avoid a new confirmation for each routine update. With an auto_apply-capable service, use explicit true when immediate publication is warranted for the authenticated personal owner, explicit false when human judgment is needed, and omitted/null to use backend path defaults otherwise. The backend alone decides authorisation. Policy pages always require human approval; controllers/builders do not inherit personal ownership. On older services, use their reviewed proposal schema and report the pending review.

When a change materially affects an organisation's users and its documentation workflow is authorised, propose a separate non-technical organisation-wiki update with auto_apply=false when supported. Include only information appropriate for all that KB's authorised readers. Do not copy private personal context or detailed operational/security material into the organisation wiki. Organisation review must not block development.

Read tool results and report source/package changes, pending review, KB publication and system-wiki release status separately. Report failed or pending documentation updates, the affected destination and retry work explicitly; do not silently claim the accounts are consistent. If the service is unavailable or a KB proposal cannot be submitted, retain the complete proposed content in the authorised project workspace and report that it still needs submission. Do not retry indefinitely or deploy service changes merely to clear a documentation failure.
