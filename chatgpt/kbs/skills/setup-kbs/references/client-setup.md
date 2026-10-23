# OpenAI connection and instruction targets

Codex uses separately configured native OAuth MCP servers: `mcp_service` for
discovery/reconciliation and `pkb_service` for Bruno's existing PKB. These are
examples of configured identities, not every tenant's inventory. Reconnect the
existing server rather than adding a duplicate. Cloud Code needs its own supported
connection configuration; desktop viewing does not make it local.

ChatGPT uses registered service-local bearer apps where available (`mcp-service`,
`pkb-service` in the current package). When missing, use the registry entry's
setup URL and service `/account` login/token UI, followed by native app connection.
Never ask MCP Service to issue/relay a KB token or substitute ChatGPT bearer apps
for Codex OAuth. Do not ask for tokens in chat.

Cloud ChatGPT Custom Instructions and local Codex instructions are independent.
The audited local Codex store is `~/.codex/AGENTS.md`; verify the current client's
supported mechanism before applying. Reconcile local stores per machine and
cloud Code stores in their actual execution environment. Cloud ChatGPT account
preferences do not configure Codex. Verify placement/persistence where manual UI
work is necessary.

The [native adapter](native-setup.md) can discover/save supported local Code
configuration without replacing existing connections. Use native OAuth after an
authorised addition; configuration presence is not authenticated wiki-read
acceptance. Obtain callbacks from the actual native flow, not a URL-hash recipe
or another release/client's callback.

Tool-approval preferences are a separate user choice, not an authentication
requirement or an automatic “Allow all tools” default. Do not expand permissions
merely to avoid prompts. Identify the actual OAuth client used by login before
requesting administrator grants, rather than granting similarly named apps.
