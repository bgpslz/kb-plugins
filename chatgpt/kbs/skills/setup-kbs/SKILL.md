---
name: setup-kbs
description: Explicit-only, idempotent initial setup and reconciliation for the KBs plugin, MCP Service registry, KB connections, compatibility, and surface-specific standing instructions.
metadata:
  version: "1.1.2"
---

# Setup KBs

Use only when explicitly asked to install, set up, update, repair, or reconcile knowledge bases.

1. Verify all four plugin skills are installed. Do not reinstall an already-correct plugin.
2. Configure or verify the separate MCP Service connection. In ChatGPT, use this plugin's registered `mcp-service` bearer app; direct the user to MCP Service's `/account`, Google sign-in, one-time ChatGPT token creation, and app connection when authentication is missing. In Codex, use the separately configured OAuth MCP server `mcp_service`; never use the ChatGPT bearer app on that surface.
3. Call MCP Service `check_connection`, then `list_knowledge_bases`. If unavailable, report that grants/revocations cannot be reconciled; do not invent entitlements or disable already-configured KB runtime connections.
4. Compare active entitlements with KB Services currently available on this surface. For each missing service, use a separately configured OAuth MCP server on Codex (`pkb_service` for the personal PKB). On ChatGPT, use the registered bearer app where present (`pkb-service` for the personal PKB), direct the user to that registry entry's `setup_url` to create a separate KB-local token, then guide app connection. Never cross-use the ChatGPT bearer app and Codex OAuth server, and never ask MCP Service to issue or relay a KB token. When configuring a PKB Service app connection, whether token- or OAuth-backed, select **Configure approvals → Allow all tools** if the user wants to avoid granting approval at the start of each chat. Explain that the UI marks this choice as elevated risk because it permits tool use without asking, and verify the selection before reporting a no-recurring-approval setup complete.
5. Verify each connection's `kb_protocol_version` and capabilities. Do not require unavailable optional capabilities. A `build` declaration requires `get_build_guide`.
6. Detect revoked/removed entries, remove them from standing configuration, and tell the user the stale connector can be removed. Security still depends on the KB Service revoking credentials server-side.
7. Preserve correct configuration and rewrite only the managed standing-instruction block for each applicable instruction store when inventory or protocol metadata changed.

## Standing-instruction reconciliation

Treat these as independent configuration targets:

- **Cloud ChatGPT Custom Instructions:** edited in ChatGPT's online interfaces, such as web or mobile under **Settings → Personalization → Custom Instructions**; stored in the cloud and used by ChatGPT.
- **Local Codex instructions:** edited in Codex desktop under **Settings → Personalization → Custom Instructions** and currently represented by `~/.codex/AGENTS.md`; stored locally per machine and used by Codex.

When the user uses both ChatGPT and Codex, reconcile both stores. Updating or verifying either store does not establish that the other has been updated. Do not describe the Codex desktop Custom Instructions setting as another route to cloud ChatGPT Custom Instructions. Reconcile local Codex instructions on each machine where the user runs Codex.

Generate a separate surface-appropriate managed `kbs-instructions v1` block for each applicable target. Each block must contain every active KB's name, type/domain description, service display name, protocol version, capabilities, and capture policy. Both versions must state: invoke `use-kbs`; use one local `KB_ref`; retrieve only from materially relevant configured KBs; follow `use-standard-kb`; establish each required KB Service's connection state at most once after success; otherwise use `check_connection`; verify `kb_protocol_version: 1` and the capability required for the operation; apply each KB's capture policy independently; honor prospective per-KB `exclude <KB>` and `include <KB>` without deletion or backfill; and use MCP Service only for setup/reconciliation, never ordinary runtime.

The surface-specific clauses must differ:

- The ChatGPT block must require this plugin's registered bearer-token apps, must not substitute Codex OAuth connections, and must pass `source: "chatgpt"` for chat capture.
- The Codex block must require the separately configured OAuth MCP servers, must not substitute ChatGPT bearer apps, and must pass `source: "codex"` for chat capture.

The two blocks therefore need not be byte-for-byte identical. When a surface cannot create a connection or update its instruction store programmatically, give concise steps and the complete block for that target, wait for the user to complete them, then verify tool availability and instruction placement before reporting reconciliation complete.
