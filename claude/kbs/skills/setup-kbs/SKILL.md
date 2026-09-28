---
name: setup-kbs
description: Explicit-only, idempotent initial setup and reconciliation for the KBs plugin, MCP Service registry, KB connections, compatibility, and surface-specific standing instructions.
disable-model-invocation: true
metadata:
  version: "1.1.3"
---

# Setup KBs

Use only when explicitly asked to install, set up, update, repair, or reconcile knowledge bases.

1. Verify all four plugin skills are installed. Do not reinstall an already-correct plugin.
2. Configure or verify the separate MCP Service connection with OAuth. In Claude web, Desktop, and mobile, use the remote OAuth connector. In Claude Code, use this plugin's bundled `mcp-service` server and complete its OAuth authorization through `/mcp`; do not add a duplicate user-, project-, or local-scoped server. Reconnect the existing service when needed, and never assume either connection configures the other or another machine.
3. Call MCP Service `check_connection`, then `list_knowledge_bases`. If unavailable, report that grants/revocations cannot be reconciled; do not invent entitlements or disable already-configured KB runtime connections.
4. Compare active entitlements with KB Services currently available on each applicable surface. For each missing service, guide the user through its OAuth connection. In Claude web, Desktop, and mobile, use a remote connector. In Claude Code, prefer a server bundled by this plugin, including `pkb-service` for the personal PKB, and complete OAuth authorization through `/mcp`; do not create a duplicate manually configured server. Guide connection of an unbundled entitled KB Service only when needed. Never ask MCP Service to issue or relay a KB token. For a trusted PKB Service connector, select **Always allow** for its tools if the user wants to avoid approval prompts; explain that this permits tool use without asking. Configure Claude Code tool permissions separately when the user wants the same behavior there, and verify each setting before reporting a no-recurring-approval setup complete.
5. Verify each connection's `kb_protocol_version` and capabilities. Do not require unavailable optional capabilities. A `build` declaration requires `get_build_guide`.
6. Detect revoked/removed entries, remove them from standing configuration, and tell the user the stale connector can be removed. Security still depends on the KB Service revoking credentials server-side.
7. Preserve correct configuration and rewrite only the managed standing-instruction block for each applicable instruction store when inventory or protocol metadata changed.

## Standing-instruction reconciliation

Treat these as independent configuration targets:

- **Cloud Claude profile preferences:** edited in Claude's account settings under the profile preferences prompt; stored with the Claude account and used by cloud Claude conversations, including web, Desktop, and mobile.
- **Local Claude Code user instructions:** stored in `~/.claude/CLAUDE.md`; local per machine and used by Claude Code sessions on that machine.

When the user uses both cloud Claude and Claude Code, reconcile both stores. Updating or verifying either store does not establish that the other has been updated. Do not describe Claude Desktop profile preferences as a route to local Claude Code instructions. Reconcile `~/.claude/CLAUDE.md` on each machine where the user runs Claude Code.

Generate a separate surface-appropriate managed `kbs-instructions v1` block for each applicable target. Each block must contain every active KB's name, type/domain description, service display name, protocol version, capabilities, and capture policy. Both versions must state: invoke `use-kbs`; use one local `KB_ref`; retrieve only from materially relevant configured KBs; follow `use-standard-kb`; establish each required KB Service's connection state at most once after success; otherwise use `check_connection`; verify `kb_protocol_version: 1` and the capability required for the operation; apply each KB's capture policy independently; honor prospective per-KB `exclude <KB>` and `include <KB>` without deletion or backfill; and use MCP Service only for setup/reconciliation, never ordinary runtime.

The surface-specific clauses must differ:

- The cloud Claude block must require the connected remote OAuth KB Service connectors and must pass `source: "claude"` with the known cloud Claude surface for chat capture.
- The Claude Code block must require the separately configured OAuth MCP servers and must pass `source: "claude"` with the known Claude Code surface for chat capture.

The two blocks therefore need not be byte-for-byte identical. When a surface cannot create a connection or update its instruction store programmatically, give concise steps and the complete block for that target, wait for the user to complete them, then verify tool availability and instruction placement before reporting reconciliation complete.
