# KBs plugin for Claude

Version 1.1.3 contains four generic skills: `use-kbs`, `use-standard-kb`,
`setup-kbs`, and `build-kb`. The MCP Service registry is needed only during
setup/reconciliation. Normal retrieval, wiki work, build guidance and chat
capture go directly to each configured KB Service.

Claude web, Desktop, and mobile use remote OAuth connectors for MCP Service and
each KB Service. Claude Code loads the plugin's bundled `mcp-service` and
`pkb-service` OAuth MCP definitions from `.mcp.json`; users complete OAuth
authorization through `/mcp` without adding duplicate servers. Authentication
transport does not change the retrieval protocol.
Cloud Claude profile preferences and local Claude Code user instructions in
`~/.claude/CLAUDE.md` are reconciled independently. `setup-kbs` and `build-kb`
are user-invoked only; `use-kbs` remains model-invoked because it is the
standing conversation router.
