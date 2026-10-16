---
name: build-kb
description: Explicit-only generic workflow to build or enrich any configured KB that declares the build capability, using that KB Service's own get_build_guide content.
disable-model-invocation: true
metadata:
  version: "1.2.0"
  kb_protocol_version: 1
---

# Build a KB

Use only when the user explicitly asks to build, enrich, populate, revisit, or be interviewed for a KB.

Identify the target from configured KBs; ask only if ambiguous. Verify protocol version 1 and the `build` and `wiki` capabilities. If `build` is absent, explain that this service does not support the standard build workflow.

Read `wiki://index.md` and traverse relevant existing pages before asking questions. Then call the target KB Service's `get_build_guide`. Treat its response as resource-like KB-specific guidance, not executable interview state. The generic plugin must not carry personal or organisation-specific questionnaires.

Compare the guide with existing wiki coverage. Offer or ask about useful gaps, corrections, and deeper areas; do not repeat adequately answered questions. Keep the exchange natural and progressive. Retrieval may corroborate details when useful, but absence of results is not evidence of absence and retrieved material does not override the user's correction.

Use the target service's declared lifecycle and write behaviour from `get_kb_capabilities`; never infer permission to bypass review from a document or page-level `status: draft`. Missing lifecycle metadata means the normal reviewed workflow.

For a service declaring `wiki_write_behavior: owner_policy_or_human_review`, inspect the proposal schema. Use `auto_apply` only if supported: true requests immediate validated publication for the authenticated personal owner; false requires human review; omitted/null uses defaults for every affected path. Personal ownership is a backend decision, never inferred from a controller/builder role. Organisation proposals and protected policy pages require human approval, including during bootstrap. An explicit build instruction authorises submitting source-backed proposal batches without a separate confirmation for each batch; ask about consequential factual uncertainty or disclosure decisions when needed.

For services declaring human review or lacking an automatic-approval contract, use their reviewed proposal workflow. Do not interpret legacy `validated_auto_publication` metadata as permission to automatically approve organisation changes; use explicit false if supported, otherwise report the incompatible service and retain the draft for reviewed submission after upgrade.

Include companion index/link updates and preserve provenance and uncertainty. Describe queued changes as proposals until the service confirms publication. Do not change lifecycle metadata or attempt the human transition; direct the controller to the browser action when the initial draft is ready. Continue with another gap only when the user wants to.
