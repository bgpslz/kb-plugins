---
name: maintain-project-docs
description: Maintain repository documentation and propose shared KB-system explanations, plans, decisions, development history and outcomes to the system wiki through MCP Service. Personal KB wikis receive only the owner's personal purposes, preferences and source evidence. Excludes ordinary KB retrieval.
metadata:
  version: "1.4.0"
  kb_protocol_version: 1
---

# Maintain project documentation

Use during material development work when the user has authorised a project documentation workflow and the documentation destinations are established. Do not invoke for ordinary retrieval, and do not invent a destination from the developer's identity.

## Repository documentation

Preserve the project's existing repository documentation contract, including architecture, implementation details, rationale, history, operations and outstanding work. Read the repository instructions and current documents first. Preserve full repository documentation; repository-local provenance belongs in repository records.

## Choosing destinations

Choose destinations by the project's documentation policy and the content's audience:

- **System wiki.** Shared KB-system explanations, architecture, plans, decisions, development history and implementation outcomes go to the shared system wiki, served by MCP Service. They never go to a personal or organisation KB wiki.
- **Personal KB wiki.** For KB-system work, the owner's personal KB wiki receives only that owner's personal purposes, priorities, preferences and original source evidence. Do not recreate a parallel shared system account there. Zero personal-KB proposals is a valid outcome, and the usual one for system development.
- **Organisation KB wiki.** Organisation-specific knowledge belongs in the relevant organisation KB and follows that wiki's human-review rules. Do not duplicate general system documentation there.

Projects other than the KB system follow their own authorised documentation destinations.

## Writing and transposing content

Keep each account independently intelligible, without unnecessary duplication or cross-links. A wiki page must be understandable without opening code or private source records.

Keep plain-English pages for users separate from developer and history pages. User-facing explanations use plain English and explain any technical term they need. Developer and history pages may use technical language; histories explain the problem, decision and outcome before technical detail. Keep current explanations and histories in separate linked files.

When transposing existing material into the system wiki, from repository documents, KB pages or drafts, carry its detail across in full. Do not condense, summarise or prune it: summarising has previously lost substantial detail. Material that no longer describes the current shape of the system moves to a linked history page rather than being discarded. When unsure whether detail still matters, keep it.

Do not hardcode release versions (release, package or pin numbers) in system-wiki or repository explanations. Refer to "the current release" or the client's normal update mechanism instead. Compatibility-protocol numbers that clients check, such as KB protocol 1, may be stated. Version fields in package metadata and dated release or history records are not explanations and keep their versions.

## Submitting system-wiki changes

Authorised agents submit system-wiki changes through MCP Service, using the configured authentication for this surface:

1. Call `get_system_documentation_status` to check the account's submission scope. Any authenticated user may propose a constrained clarification of a designated existing explanation (`purpose: "clarification"`). Only configured system admins may submit general changes (`purpose: "system_change"`). If the scope does not cover the change, do not submit it; retain the content and report it.
2. Read each affected page and its base hash with `read_system_documentation_page`, starting at `index.md` and following relevant links. These are the current approved staging pages, not the live release. Use a null base hash for a new page.
3. Submit with `propose_system_documentation_write`. Supply complete pages, the exact base hashes, evidence, companion index and link repairs, and a stable `request_id`; add `associated_code` and `supersedes` when they apply. For a clarification, give every change a `clarification` object (`original`, `replacement`, `reader_confusion`), replace only that exact passage and preserve every other byte. Never include caller identity or auto-approval fields. A retry reuses the same request body. Exclude credentials, private conversation detail and personal facts from shared wording.

Proposals queue for maintainer review. Submitting does not approve, export, release or publish anything: staging approval and export to application source are separate admin steps, and the application's source review and release remain the only writer of the published guide. Do not route system-wiki changes through KB proposal tools. For the KB system, the canonical bundle is personal-rag's `src/personal_rag/system_wiki/content/`; edit it directly only when the task is explicitly source work under that repository's `AGENTS.md` and `docs/system_wiki.md`. Source edits, staging proposals and review drafts are not deployed content. When system content moves out of a personal KB, publish and verify the replacement system pages before merging the personal-KB reductions.

## Personal and organisation KB updates

For personal or organisation KB updates, use the configured KB routing/authentication for this surface. Read the destination's root index and relevant existing pages, verify protocol v1 and wiki/build capabilities, and inspect the current proposal tool schema. Do not edit a local KB wiki mirror as a substitute for updating the canonical service. Do not change authentication or submit private content to a different KB after a failure.

Submit a coherent distilled KB update through the target KB service's proposal tool, including affected indexes. Treat a coding task that already authorises this workflow as permission to submit its documentation proposals; avoid a new confirmation for each routine update. With an auto_apply-capable service, use explicit true when immediate publication is warranted for the authenticated personal owner, explicit false when human judgment is needed, and omitted/null to use backend path defaults otherwise. The backend alone decides authorisation. Policy pages always require human approval; controllers/builders do not inherit personal ownership. On older services, use their reviewed proposal schema and report the pending review.

When a change materially affects an organisation's users and its documentation workflow is authorised, propose a separate non-technical organisation-wiki update with auto_apply=false when supported. Include only information appropriate for all that KB's authorised readers. Do not copy private personal context or detailed operational/security material into the organisation wiki. Organisation review must not block development.

## Reporting

Read tool results and report source/package changes, pending system-documentation proposals, pending KB review, KB publication and system-wiki release status separately. Report failed or pending documentation updates, the affected destination and retry work explicitly; do not silently claim the accounts are consistent. If the service is unavailable or a proposal cannot be submitted, retain the complete proposed content in the authorised project workspace and report that it still needs submission. Do not retry indefinitely or deploy service changes merely to clear a documentation failure.
