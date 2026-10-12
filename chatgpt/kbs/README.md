# KBs plugin for ChatGPT and Codex

Version 1.3.0 contains `use-kbs`, `use-standard-kb`, `setup-kbs` and `build-kb`.
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
