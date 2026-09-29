# KBs plugin for ChatGPT and Codex

Version 1.2.0 contains four generic skills: `use-kbs`, `use-standard-kb`,
`setup-kbs`, and `build-kb`. Normal retrieval, wiki work, and build guidance go
directly to materially relevant KB Services. MCP Service supplies the registry
during setup and Capture Protocol v1 at runtime: each eligible turn is appended
once, pre-destination and fail-soft, for human routing in the Capture Review
Application. Runtime never queries registry inventory or falls back to legacy
per-KB capture fan-out.

The plugin's `.app.json` registers the ChatGPT bearer-token apps for MCP Service
and PKB Service. Their separate service-local tokens are created on the
services' `/account` pages and are never returned by MCP tools.

Codex uses separately configured OAuth MCP servers (`mcp_service` for registry
reconciliation and central capture, and `pkb_service` for PKB runtime
operations). Those OAuth connections are deliberately not registered in
`.app.json`; authentication
transport stays outside the retrieval protocol.
