---
name: setup-kbs
description: Explicit-only, idempotent initial setup and reconciliation for the KBs plugin, MCP Service registry, KB connections, compatibility, and surface-specific standing instructions.
disable-model-invocation: true
metadata:
  version: "1.0.0"
---

# Setup KBs

Use only when explicitly asked to install, set up, update, repair, or reconcile knowledge bases.

1. Verify all four plugin skills are installed. Do not reinstall an already-correct plugin.
2. Configure or verify the separate MCP Service connection with OAuth. Reconnect the existing service when needed rather than creating duplicates.
3. Call MCP Service `check_connection`, then `list_knowledge_bases`. If unavailable, report that grants/revocations cannot be reconciled; do not invent entitlements or disable already-configured KB runtime connections.
4. Compare active entitlements with KB Services currently available on this surface. For each missing service, guide the user through its OAuth connection. Never ask MCP Service to issue or relay a KB token.
5. Verify each connection's `kb_protocol_version` and capabilities. Do not require unavailable optional capabilities. A `build` declaration requires `get_build_guide`.
6. Detect revoked/removed entries, remove them from standing configuration, and tell the user the stale connector can be removed. Security still depends on the KB Service revoking credentials server-side.
7. Preserve correct configuration and rewrite only the managed standing-instruction block when inventory or protocol metadata changed.

Generate a surface-appropriate `kbs-instructions v1` block containing each active KB's name, type/domain description, service display name, protocol version, capabilities, and capture policy. It must state: invoke `use-kbs`; retrieve only from materially relevant configured KBs; follow `use-standard-kb`; use one local `KB_ref`; establish required KB connection once; capture by policy; honor prospective per-KB exclude/include; and never call MCP Service during normal runtime.

Claude Chat, Desktop, mobile, and Claude Code use OAuth where available. When a surface cannot create a connection programmatically, give concise steps, wait for the user to complete them, then verify tool availability. In the current Claude UI, standing profile instructions are under Settings → Account → Profile → Instructions for Claude.
