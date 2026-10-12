---
name: setup-kbs
description: Explicit-only, idempotent initial setup and reconciliation for the KBs plugin, MCP Service registry, KB connections, compatibility, and surface-specific standing instructions.
disable-model-invocation: true
metadata:
  version: "1.3.0"
---

# Setup KBs

Use only when explicitly asked to install, set up, update, repair, or reconcile knowledge bases.

1. Verify all four plugin skills are installed. Do not reinstall an already-correct plugin.
2. Configure or verify the separate MCP Service connection with OAuth. It owns the setup-time registry and the capture ingress used by external capture clients. In Claude web, Desktop, and mobile, use the remote OAuth connector. In Claude Code, use this plugin's bundled `mcp-service` server and complete its OAuth authorization through `/mcp`; do not add a duplicate user-, project-, or local-scoped server. Reconnect the existing service when needed, and never assume either connection configures the other or another machine.
3. Call MCP Service `check_connection`, verify Capture Protocol version 1 and the availability of `capture_chat_turn`, then call `list_knowledge_bases`. If unavailable or incompatible, report that registry reconciliation or central capture cannot be verified as applicable; do not invent entitlements, disable already-configured KB retrieval connections, or configure legacy per-KB capture as a fallback.
4. Compare active entitlements with KB Services currently available on each applicable surface. For each missing service, guide the user through its OAuth connection. In Claude web, Desktop, and mobile, use a remote connector. In Claude Code, prefer a server bundled by this plugin, including `pkb-service` for the personal PKB, and complete OAuth authorization through `/mcp`; do not create a duplicate manually configured server. Guide connection of an unbundled entitled KB Service only when needed. Never ask MCP Service to issue or relay a KB token. For a trusted PKB Service connector, select **Always allow** for its tools if the user wants to avoid approval prompts; explain that this permits tool use without asking. Configure Claude Code tool permissions separately when the user wants the same behavior there, and verify each setting before reporting a no-recurring-approval setup complete.
5. Verify each KB Service connection's `kb_protocol_version` and capabilities for direct retrieval and other declared operations. Do not require a KB Service to expose legacy chat capture, and do not require unavailable optional capabilities. A `build` declaration requires `get_build_guide`.
6. Detect revoked/removed entries, remove them from standing configuration, and tell the user the stale connector can be removed. Security still depends on the KB Service revoking credentials server-side.
7. Preserve correct configuration and reconcile the managed standing-instruction block after local capture verification, when inventory or protocol metadata changed.

## Standing-instruction reconciliation

Treat these as independent configuration targets:

- **Cloud Claude profile preferences:** edited in Claude's account settings under the profile preferences prompt; stored with the Claude account and used by cloud Claude conversations, including web, Desktop, and mobile.
- **Local Claude Code user instructions:** stored in `~/.claude/CLAUDE.md`; local per machine and used by Claude Code sessions on that machine.

When the user uses both cloud Claude and Claude Code, reconcile both stores. Updating or verifying either store does not establish that the other has been updated. Do not describe Claude Desktop profile preferences as a route to local Claude Code instructions. Reconcile `~/.claude/CLAUDE.md` on each machine where the user runs Claude Code.

Generate a separate surface-appropriate managed `kbs-instructions v2` block for each
applicable target. Include every active KB's name, type/domain description, service,
KB Protocol version and capabilities. Retain `capture_policy` as registry metadata for
human review only; it must not govern model behaviour or automated intake.

The block must state: invoke `use-kbs`; retrieve only from materially relevant configured
KBs; follow `use-standard-kb`; establish connection state once after success (otherwise
use `check_connection`); verify KB Protocol version 1 and required capabilities; never
query MCP Service for inventory during normal runtime. Preserve the appropriate
surface's existing OAuth or bearer-app authentication path.

Describe the three capture routes: Open WebUI is the main captured chat surface, with
server-side capture; local Claude Code and Codex use session-history capture installed
on each machine; other web, desktop, mobile and cloud coding sessions are pasted into
the Capture Review Application. Capture destinations are selected by a human there.
No in-chat reference generation, tags, tool calls, capture-policy evaluation or
exclude/include commands remain. This does not change direct KB retrieval.

For a local machine, complete the installation below before removing old capture rules.
Only replace the delimited managed block; preserve all other instructions. Obtain the
user's approval before changing their personal `~/.claude/CLAUDE.md`. Reconcile cloud
preferences independently; do not claim that source edits update installed plugins or
cloud settings. If a surface cannot be updated programmatically, provide its complete
block and verify placement after the user applies it.

## Local session capture installation

Use the packaged [installer](scripts/install.py) with a durable Python 3.11+ interpreter:
`python3.11 <skill-directory>/scripts/install.py --account <MCP-Service-email> --activate`.
The shared implementation is maintained in `kb-plugins/local-capture`; both packages
carry identical installer/runtime copies. Never request a token in chat or pass it as
an argument. The installer prompts directly through macOS Keychain for the user's
MCP Service bearer token, created at `https://mcp-service.summerleaze.com/account`.
This token is separate from the app's retrieval OAuth connections.

Installation preserves unrelated config, including Codex `notify`, and writes Stop and
SessionEnd hooks plus a daily launchd backstop. It defaults to all local projects from
installation time. Optional `excluded_projects` shell glob patterns match the session
working directory in `~/Library/Application Support/kbs-capture/config.json`; an empty
list includes all. This is a machine setting, not an in-chat command. Preserve existing
exclusions and the original capture boundary on reinstall.

Codex requires review/trust of the exact new hook definitions through `/hooks`.
Verify one new completed turn from each used surface reaches the Capture Review queue,
and test Claude desktop's Code tab separately. Check local `capture.log` for failures.
Only after successful intake verification reconcile the old managed instruction blocks
and install the retrieval-only `use-kbs` release. Do not claim activation merely because
files were written. Offline failures remain eligible for the next hook or sweep.

There are no cloud-session hooks, share-link scrapers, web export automation or Compliance
API capture routes. Keep Capture Protocol v1's field names, limits and queue contract.
