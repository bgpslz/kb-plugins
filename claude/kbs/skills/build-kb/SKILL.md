---
name: build-kb
description: Explicit-only generic workflow to build or enrich any configured KB that declares the build capability, using that KB Service's own get_build_guide content.
disable-model-invocation: true
metadata:
  version: "1.1.0"
  kb_protocol_version: 1
---

# Build a KB

Use only when the user explicitly asks to build, enrich, populate, revisit, or be interviewed for a KB.

Identify the target from configured KBs; ask only if ambiguous. Verify protocol version 1 and the `build` and `wiki` capabilities. If `build` is absent, explain that this service does not support the standard build workflow.

Read `wiki://index.md` and traverse relevant existing pages before asking questions. Then call the target KB Service's `get_build_guide`. Treat its response as resource-like KB-specific guidance, not executable interview state. The generic plugin must not carry personal or organisation-specific questionnaires.

Compare the guide with existing wiki coverage. Offer or ask about useful gaps, corrections, and deeper areas; do not repeat adequately answered questions. Keep the exchange natural and progressive. Retrieval may corroborate details when useful, but absence of results is not evidence of absence and retrieved material does not override the user's correction.

Use the target service's declared lifecycle and write behaviour from `get_kb_capabilities`; never infer permission to bypass review from a document or page-level `status: draft`. Missing lifecycle metadata means the normal reviewed workflow.

For `wiki_lifecycle: bootstrap` with `wiki_write_behavior: validated_auto_publication`, the user's explicit authorization to build permits submitting complete related proposal batches without confirmation before every batch. Use `propose_wiki_write`, include companion index/link updates, preserve provenance and uncertainty, and address consequential gaps after producing a useful source-backed draft. Report changes as applied only when the service confirms successful publication. Do not change lifecycle metadata or attempt the human transition; direct the controller to the browser action when the initial draft is ready.

For a live wiki or a service without the declared bootstrap behaviour, show the compact proposed treatment, provenance, uncertainty, and conflicts and obtain confirmation before a write/proposal. Use the target KB's standard reviewed write/proposal workflow. Describe queued changes as proposals until the service confirms publication. Continue with another gap only when the user wants to.
