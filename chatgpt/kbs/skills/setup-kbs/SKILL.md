---
name: setup-kbs
description: Explicit-only, idempotent initial setup and reconciliation for the KBs plugin, MCP Service registry, KB connections, compatibility, and surface-specific standing instructions.
metadata:
  version: "1.3.3"
---

# Setup KBs

Use only when explicitly asked to install, set up, update, repair, or reconcile knowledge bases.

1. Verify all four plugin skills are installed and inspect the active skill paths and versions. Check for duplicate installations from different marketplaces or workspace sources; a current source checkout does not prove the active plugin is current. Update stale installations through the supported plugin manager, preserving working connections. Do not reinstall an already-correct plugin or edit generated cache files as a deployment method.
2. Configure or verify the separate MCP Service connection. It owns the setup-time registry and the capture ingress used by external capture clients. In ChatGPT, use this plugin's registered `mcp-service` bearer app; direct the user to MCP Service's `/account`, Google sign-in, one-time ChatGPT token creation, and app connection when authentication is missing. In Codex, use the separately configured OAuth MCP server `mcp_service`; never use the ChatGPT bearer app on that surface.
3. Call MCP Service `check_connection`, verify Capture Protocol version 1 and the availability of `capture_chat_turn`, then call `list_knowledge_bases`. If unavailable or incompatible, report that registry reconciliation or central capture cannot be verified as applicable; do not invent entitlements, disable already-configured KB retrieval connections, or configure legacy per-KB capture as a fallback.
4. Compare active entitlements with KB Services currently available on this surface. For each missing service, use a separately configured OAuth MCP server on Codex (`pkb_service` for the personal PKB). On ChatGPT, use the registered bearer app where present (`pkb-service` for the personal PKB), direct the user to that registry entry's `setup_url` to create a separate KB-local token, then guide app connection. Never cross-use the ChatGPT bearer app and Codex OAuth server, and never ask MCP Service to issue or relay a KB token. When configuring a PKB Service app connection, whether token- or OAuth-backed, select **Configure approvals → Allow all tools** if the user wants to avoid granting approval at the start of each chat. Explain that the UI marks this choice as elevated risk because it permits tool use without asking, and verify the selection before reporting a no-recurring-approval setup complete.
5. Verify each KB Service connection's `kb_protocol_version` and capabilities for direct retrieval and other declared operations. Do not require a KB Service to expose legacy chat capture, and do not require unavailable optional capabilities. A `build` declaration requires `get_build_guide`.
6. Detect revoked/removed entries, remove them from standing configuration, and tell the user the stale connector can be removed. Security still depends on the KB Service revoking credentials server-side.
7. Preserve correct configuration and reconcile the managed standing-instruction block after local capture verification, when inventory or protocol metadata changed.

## Standing-instruction reconciliation

Treat these as independent configuration targets:

- **Cloud ChatGPT Custom Instructions:** edited in ChatGPT's online interfaces, such as web or mobile under **Settings → Personalization → Custom Instructions**; stored in the cloud and used by ChatGPT.
- **Local Codex instructions:** edited in Codex desktop under **Settings → Personalization → Custom Instructions** and currently represented by `~/.codex/AGENTS.md`; stored locally per machine and used by Codex.

When the user uses both ChatGPT and Codex, reconcile both stores. Updating or verifying either store does not establish that the other has been updated. Do not describe the Codex desktop Custom Instructions setting as another route to cloud ChatGPT Custom Instructions. Reconcile local Codex instructions on each machine where the user runs Codex.

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

## Migration verification

After intake verification, check each applicable standing-instruction store for a
legacy managed block and reconcile it to v2. Check project instructions as well as
global instructions without replacing unrelated project rules. Confirm only the
intended plugin installation supplies the runtime skills. Removal of a duplicate
plugin requires an explicit removal request; obtain it when needed.

Start a fresh session after changing instructions or installed skills. Verify that
a simple completed exchange is captured by the local route without a model-generated
reference tag or chat-capture call. Existing sessions can retain old instructions.
Report source version, installed version, instruction targets changed, verified
capture surfaces and remaining targets separately; cloud settings and other Macs
are independent migrations.

## Local session capture installation

For a local-capture setup request, read the packaged [platform guide](references/local-capture-setup.md). Run setup on the requested computer, detect its OS and native/WSL environment, and use this installed skill's scripts; do not require the user to clone a repository or know Git. Prefer assistant-guided setup from a local coding desktop session. Discover a persistent Python 3.11+ interpreter before offering installation; do not assume Homebrew, a bundled Python runtime or another machine's paths. The current capture implementation supports macOS only. On Windows or Linux, explain the missing credential/scheduler adapters and the current capture alternatives rather than running the macOS installer or claiming activation.

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
