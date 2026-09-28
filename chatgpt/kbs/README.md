# KBs plugin for ChatGPT and Codex

Version 1.1.0 contains four generic skills: `use-kbs`, `use-standard-kb`,
`setup-kbs`, and `build-kb`. The MCP Service registry is needed only during
setup/reconciliation. Normal retrieval, wiki work, build guidance and chat
capture go directly to each configured KB Service.

The plugin's `.app.json` registers the ChatGPT bearer-token apps for MCP Service
and PKB Service. Their separate service-local tokens are created on the
services' `/account` pages and are never returned by MCP tools.

Codex uses separately configured OAuth MCP servers (`mcp_service` for registry
reconciliation and `pkb_service` for PKB runtime operations). Those OAuth
connections are deliberately not registered in `.app.json`; authentication
transport stays outside the retrieval protocol.
