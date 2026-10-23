# Claude connection and instruction targets

Claude Chat web/desktop/mobile uses remote OAuth connectors. Claude Code uses
native OAuth servers, preferring this plugin's bundled `mcp-service` and
`pkb-service` where applicable. Reauthorize through the client's supported MCP
flow; do not add duplicate user/project/local-scoped servers. Guide addition of
an unbundled entitled KB only when needed. Never request secrets in chat or ask
MCP Service to issue/relay a KB token. Separate Chat, local Code and cloud Code
connections; a desktop Code tab may execute remotely.

Cloud Claude profile preferences are account-level Chat instructions. Local Code
user instructions are `~/.claude/CLAUDE.md`, independent per machine; changing
Bruno's personal file requires his approval. Cloud Code needs instructions in
its own supported execution environment. Updating one store does not update the
others. Verify the current client mechanism and placement/persistence after
separately authorised changes.

The [native adapter](native-setup.md) discovers user/local/project and enabled
plugin servers before planning additions. Keep bundled endpoints rather than
duplicating them. Saving a native entry does not approve project servers, connect
OAuth, or prove the Desktop Code tab has loaded it; verify those separately.

Tool permissions/“Always allow” are separate user choices, not requirements for
successful authentication. Preserve existing approvals and distinguish missing
broker grants from a user's incomplete login. Identify the actual OAuth client
before requesting administrator approval; do not copy Open WebUI credentials.
