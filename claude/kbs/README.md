# KBs plugin for Claude

Version 1.2.0 contains four generic skills: `use-kbs`, `use-standard-kb`,
`setup-kbs`, and `build-kb`. Normal retrieval, wiki work, and build guidance go
directly to materially relevant KB Services. MCP Service supplies the registry
during setup and Capture Protocol v1 at runtime: each eligible turn is appended
once, pre-destination and fail-soft, for human routing in the Capture Review
Application. Runtime never queries registry inventory or falls back to legacy
per-KB capture fan-out.

Claude web, Desktop, and mobile use remote OAuth connectors for MCP Service and
each KB Service. Claude Code loads the plugin's bundled `mcp-service` for
registry reconciliation and central capture, plus its bundled
`pkb-service`, from `.mcp.json`; users complete OAuth authorization through
`/mcp` without adding duplicate servers. Authentication
transport does not change the retrieval protocol.
Cloud Claude profile preferences and local Claude Code user instructions in
`~/.claude/CLAUDE.md` are reconciled independently. `setup-kbs` and `build-kb`
are user-invoked only; `use-kbs` remains model-invoked because it is the
standing conversation router.
