# KBs plugin for ChatGPT and Codex

Version 1.3.4 adds `maintain-project-docs` alongside `use-kbs`,
`use-standard-kb`, `setup-kbs` and `build-kb`.
Retrieval and build guidance go directly to relevant KB Services. MCP Service owns
registry reconciliation and Capture Protocol v1; the model has no capture duties.

Three routes feed the same human review queue: Open WebUI server capture, local
Claude Code/Codex session capture, and manual paste for other surfaces. See
[local capture installation](../../local-capture/README.md). Install and verify
local capture before replacing old instructions or installing retrieval-only skills.
`capture_policy` remains review metadata; in-chat exclude/include is retired.

The plugin's `.app.json` registers the ChatGPT bearer-token apps for MCP Service
and PKB Service. Their separate service-local tokens are created on the
services' `/account` pages and are never returned by MCP tools.

Codex uses separately configured OAuth MCP servers (`mcp_service` for registry
reconciliation, and `pkb_service` for PKB runtime
operations). Those OAuth connections are deliberately not registered in
`.app.json`; authentication
transport stays outside the retrieval protocol.

`build-kb` inspects service-declared lifecycle, write behaviour and proposal
schema. Automatic application requires an authenticated personal owner and a
compatible service; organisation changes and protected policy pages require human
review even during bootstrap. Older reviewed services remain supported. The skill
never performs the controller's lifecycle transition.

`maintain-project-docs` preserves repository documentation and proposes distilled
architecture, decisions, status and plans to the configured owner PKB. It reports
pending/failed updates and proposes audience-appropriate organisation guidance
for human review when users are materially affected. Source release, backend
deployment and installed-client acceptance are separate milestones.

When upgrading from in-chat capture, reconcile managed instructions to v2 after
local intake verification and inspect active skill paths for duplicate older
installations. Start a fresh session to verify the new behaviour; source changes
alone do not update installed skills or cloud preferences.

For assistant-guided laptop setup without a source checkout, ask `setup-kbs` to
install local capture on this computer. See the [platform guide](skills/setup-kbs/references/local-capture-setup.md).
Capture currently supports macOS; Windows and Linux/WSL adapters and standalone
installers with bundled runtimes are planned.
