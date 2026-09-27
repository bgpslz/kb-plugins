---
name: build-kb
description: Explicit-only generic workflow to build or enrich any configured KB that declares the build capability, using that KB Service's own get_build_guide content.
metadata:
  version: "1.0.0"
  kb_protocol_version: 1
---

# Build a KB

Use only when the user explicitly asks to build, enrich, populate, revisit, or be interviewed for a KB.

Identify the target from configured KBs; ask only if ambiguous. Verify protocol version 1 and the `build` and `wiki` capabilities. If `build` is absent, explain that this service does not support the standard build workflow.

Read `wiki://index.md` and traverse relevant existing pages before asking questions. Then call the target KB Service's `get_build_guide`. Treat its response as resource-like KB-specific guidance, not executable interview state. The generic plugin must not carry personal or organisation-specific questionnaires.

Compare the guide with existing wiki coverage. Offer or ask about useful gaps, corrections, and deeper areas; do not repeat adequately answered questions. Keep the exchange natural and progressive. Retrieval may corroborate details when useful, but absence of results is not evidence of absence and retrieved material does not override the user's correction.

Before a write/proposal, show the compact proposed treatment, provenance, uncertainty, and conflicts and obtain confirmation. Use the target KB's standard reviewed write/proposal workflow. Never claim a proposal has been applied. Continue with another gap only when the user wants to.
