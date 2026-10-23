---
name: maintain-project-docs
description: Maintain repository documentation and distil material development changes into configured personal and organisation KB wikis when that project workflow is authorised. Excludes ordinary KB retrieval.
metadata:
  version: "1.3.5"
  kb_protocol_version: 1
---

# Maintain project documentation

Use during material development work when the user has authorised a project documentation workflow and the destination KBs are established. Do not invoke for ordinary retrieval, and do not invent a destination from the developer's identity.

Preserve the project's existing repository documentation contract, including architecture, implementation details, rationale, history, operations and outstanding work. Read the repository instructions and current documents first.

Maintain three independently intelligible layers: full documentation in repositories; distilled current architecture, significant decisions and rationale, status, open questions, plans and workflows in the owner's personal KB wiki; and capabilities, benefits, limitations and usage guidance in the organisation KB wiki. Information flows from repositories to the personal KB, then to the organisation KB. Tailor each layer to its audience, avoiding unnecessary duplication and cross-links between layers. Repository-local provenance belongs in repository records; a wiki synthesis must be understandable without opening code or private source records.

For this KB system, shared user-facing operating guidance belongs in personal-rag's Git-managed system wiki, served read-only by MCP Service. Do not duplicate that guidance into Summerleaze OKB wiki. The owner's PKB retains project-development knowledge; organisation-specific knowledge and authorised organisation documentation still use their own reviewed workflow. System-wiki edits follow repository/release rules, not KB proposal tools.

Use the configured KB routing/authentication for this surface. Read the destination's root index and relevant existing pages, verify protocol v1 and wiki/build capabilities, and inspect the current proposal tool schema. Do not edit a local wiki mirror as a substitute for updating the canonical service. Do not change authentication or submit private content to a different KB after a failure.

Submit a coherent distilled update through the target service's proposal tool, including affected indexes. Treat a coding task that already authorises this workflow as permission to submit its documentation proposals; avoid a new confirmation for each routine update. With an auto_apply-capable service, use explicit true when immediate publication is warranted for the authenticated personal owner, explicit false when human judgment is needed, and omitted/null to use backend path defaults otherwise. The backend alone decides authorisation. Policy pages always require human approval; controllers/builders do not inherit personal ownership. On older services, use their reviewed proposal schema and report the pending review.

When a change materially affects users, propose a separate non-technical organisation-wiki update with auto_apply=false when supported. Include only information appropriate for all that KB's authorised readers. Do not copy private personal context or detailed operational/security material into the organisation wiki. Organisation review must not block development.

Read tool results and report applied changes separately from queued proposals. Report failed personal-KB updates, the affected documentation and retry work explicitly; do not silently claim the layers are consistent. If the service is unavailable or a proposal cannot be submitted, retain the complete proposed content in the authorised project workspace and report that it still needs submission. Do not retry indefinitely or deploy service changes merely to clear a documentation failure.
