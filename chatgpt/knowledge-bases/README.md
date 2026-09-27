# Knowledge Bases plugin for ChatGPT and Codex

Version 1.0.0 contains four generic skills: `use-kbs`, `use-standard-kb`,
`setup-kbs`, and `build-kb`. The MCP Service registry is needed only during
setup/reconciliation. Normal retrieval, wiki work, build guidance and chat
capture go directly to each configured KB Service.

ChatGPT connects to MCP Service and each KB Service with separate service-local
bearer tokens created on those services' `/account` pages. Codex retains OAuth.
Authentication transport does not change the retrieval protocol.
