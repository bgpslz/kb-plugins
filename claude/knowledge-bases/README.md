# Knowledge Bases plugin for Claude

Version 1.0.0 contains four generic skills: `use-kbs`, `use-standard-kb`,
`setup-kbs`, and `build-kb`. The MCP Service registry is needed only during
setup/reconciliation. Normal retrieval, wiki work, build guidance and chat
capture go directly to each configured KB Service.

Claude Chat, Desktop, mobile, and Claude Code retain OAuth for MCP Service and
each KB Service where available. Authentication transport does not change the
retrieval protocol. `setup-kbs` and `build-kb` are user-invoked only; `use-kbs`
remains model-invoked because it is the standing conversation router.
