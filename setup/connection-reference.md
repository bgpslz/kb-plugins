# KB connection reference for assistants and technicians

Follow this reference when carrying out the [user setup flow](openai-client-setup.md).
Perform the configuration and verification work for the user; present only the
steps requiring their action. Use friendly service names in progress messages.
Keep commands, file paths, scopes and protocol details out of the normal user
flow unless an error requires a specific explanation. Provide every required GUI
field value and action when the user must configure a connection; do not hide
those steps behind a generic request to the assistant. If local access is unavailable,
explain what is blocked and offer an appropriate technician-assisted procedure.

## Choose the actual client

| Execution surface | Connection procedure |
| --- | --- |
| Local Codex Desktop or CLI | Native MCP OAuth setup below; reuse existing working connections. |
| ChatGPT web/cloud chat | Separate registered service-local bearer-token setup below. |
| Cloud Codex or unknown execution | Verify the environment's supported connection method; laptop files and credentials do not configure a cloud executor. |

Reuse working connections and record the actual server/tool route used in tests.
An app appearing in Plugins or Apps does not prove access through that route.

## 1. Inspect and back up local Codex settings

List the existing native connections:

```sh
codex mcp list
```

The default user store is `~/.codex/config.toml`. Account for a custom `CODEX_HOME`
and trusted project `.codex/config.toml` overrides before editing. Back up the
actual target file. For an existing default file:

```sh
cp -p ~/.codex/config.toml ~/.codex/config.toml.before-kb-setup-$(date +%Y%m%d-%H%M%S)
```

Keep backups private. If no file exists, create its directory and a private file.
Match existing entries by endpoint and service identity, retaining their names.
Investigate disabled entries before enabling them. Add only missing sections;
avoid duplicate TOML sections and preserve unrelated settings.

## 2. Configure and authenticate MCP Service first

Use an existing MCP Service connection or the bootstrap endpoint supplied by
the deployment's operator. The following Casdoor examples use reserved
`example.org` addresses. Replace
them with the deployment's supplied MCP Service address and discovered KB
addresses before saving or running commands:

```toml
[mcp_servers.casdoor_mcp_service]
url = "https://mcp-service.example.org/mcp"
scopes = ["openid", "email", "profile", "offline_access", "kb_registry:read"]
```

An omitted `enabled` means enabled; handle an existing `enabled = false`
explicitly. If the matching entry has another name, keep it and substitute that
name in every command and saved mapping. Authenticate the native connection:

```sh
codex mcp login casdoor_mcp_service --oauth-client-registration cimd
```

Complete the browser flow. In this example, the issuer is
`https://mcp-service.example.org/auth`; Google supplies sign-in identity.
The resource must be `https://mcp-service.example.org/mcp`. Let Codex generate
its client identity and callback. Complete sign-in on each machine; do not copy
credentials between machines or paste them into chat.

If login goes to a retired issuer, stop and check the selected connection and
discovery. Obtain the correct endpoint, issuer and scopes from the deployment;
do not use the example addresses as live settings.

In Codex, through this exact native server:

1. Call `get_system_wiki_capabilities`; verify service `mcp-service`, system-wiki
   protocol 1 and the required read capability.
2. Read complete `system-wiki://index.md` and `system-wiki://local-codex.md` at
   the descriptor's matching revision, following `use-kbs` validation rules.
3. Call `list_knowledge_bases`; require Registry Protocol 2 before treating a
   complete result as the authoritative entitlement inventory.

If new tools are not exposed, reload or start a fresh local Codex chat. Verify
through the named native server, rather than a registered `codex_apps` route.

## 3. Configure each requested KB

Use each entitled record's `kb_uid`, `service_id`, explicit `mcp_url`, protocol
and capabilities. Discovery does not itself connect or grant access to that KB.
Configure only KBs requested for this client. Obtain required scopes from service
metadata or operator guidance; do not derive them from display names.

For a personal KB and an organisation KB, add only missing sections, or edit the intended
existing sections while preserving unrelated fields:

```toml
[mcp_servers.casdoor_pkb_service]
url = "https://pkb.example.org/mcp"
scopes = ["openid", "email", "profile", "offline_access", "personal_rag:read"]

[mcp_servers.casdoor_org_kb]
url = "https://organisation-kb.example.org/mcp"
scopes = ["openid", "email", "profile", "offline_access", "personal_rag:read"]
```

Both KBs use the historical API scope `personal_rag:read`; MCP Service uses
`kb_registry:read`. The other scopes supply identity claims and refresh access.
The `:read` suffix does not override service authorization or wiki review rules.

Authenticate each connection separately using its actual local name. Finish one
browser flow before starting the next:

```sh
codex mcp login casdoor_pkb_service --oauth-client-registration cimd
codex mcp login casdoor_org_kb --oauth-client-registration cimd
```

The resource must be that KB's exact `/mcp` endpoint. Native Codex and registered
apps use different OAuth client identities; test the route being configured.

Through each selected native server call `get_kb_capabilities`, verify KB Protocol
1, service identity and required capabilities, then call `read_wiki_page` with
`{"uri":"wiki://index.md"}` and read the complete page. Verify the Build Guide
separately if build readiness is requested. A KB in bootstrap may permit its
designated builder to read; report lifecycle separately and do not change it.

## 4. Verify refresh, then save this client's mappings

After a new login or grant repair, repeat each authenticated read beyond the
actual access-token lifetime without manually reconnecting. For example, with
six-minute access tokens, wait at least seven minutes after the initial read,
then repeat it. Test all newly authenticated services over one waiting period
where practical. Read again from a fresh local Codex connection to verify saved
credentials.

A post-expiry read verifies continued access. If diagnosing refresh rotation,
use redacted client logs or broker metadata rather than exporting tokens. Normal
access-token expiry should not require another interactive login.

Save the verified MCP Service connection name and each KB's UID, service ID and
connection name in this machine's managed local KB instructions. Use the default
`~/.codex/AGENTS.md`, accounting for custom Codex homes, and preserve unrelated
instructions. The evidence helper's optional `mcp_service` binding is described
in the setup evidence guide (`GUIDE.md` in source; `setup-evidence.md` in the installed skill). For this example the mappings are:

| Service | Local connection ID |
| --- | --- |
| MCP Service | `casdoor_mcp_service` |
| Personal KB | `casdoor_pkb_service` |
| Organisation KB | `casdoor_org_kb` |

Subsequent sessions use these local mappings, not assumed example names.
Copying the plugin does not copy configuration or authentication. Repair missing
or failed mappings through explicit setup; do not create connections or switch
credentials during ordinary retrieval.

Report configuration, authenticated reads, refresh, fresh-connection reads,
instruction persistence/delivery and capture separately. Capture installation is
independent and is not part of this connection recipe.

## Troubleshooting

| Observed evidence | Action |
| --- | --- |
| `codex` is unavailable or a login option is unsupported | Check `codex --version` and `codex mcp login --help`; locate the installed desktop CLI if needed. |
| No suitable native entry | Configure the requested connection from inspected bootstrap/registry values. |
| Entry exists but tools are absent | Check effective enablement, client/runtime, reload and startup errors; missing tools do not prove token expiry. |
| Native refresh returns `invalid_grant` or invalid/revoked refresh credential | Record the exact route/error; reauthorize that existing native entry once and verify refresh. Do not change lifetimes to hide failure. |
| Registered app's saved issuer/resource differs from live discovery | Stop reconnect retries against unchanged metadata; investigate that saved registration. |
| Registered ChatGPT CIMD is rejected for `private_key_jwt` when Casdoor accepts only `none` with PKCE | Report this route-specific incompatibility. For requested Codex setup, use the verified native procedure; do not weaken broker validation. |
| 403/access denied | Respect the denial; check membership/policy without another credential or protected-cache bypass. |
| Network/DNS failure | Diagnose reachability separately; do not recreate apps or revoke credentials. |

## ChatGPT bearer-token setup is separate

For ChatGPT web/cloud chat retain the registered MCP Service connection and use
the appropriate registered service-local bearer-token KB connections, such as
**PKB Service (token)**. Native Codex configuration cannot configure those hosted
connections.

Use registry records' explicit `account_url` and `mcp_url`. If registry access is
missing, obtain bootstrap instructions from the operator. Sign into the KB's
account page, create its service-local token and enter it privately in the
registered connection's credential UI. Never put tokens in chat, shell arguments,
plugin ZIPs or examples. If `account_url` is null, obtain the supported procedure
rather than deriving an account URL. MCP Service credentials do not authorize a
KB Service. Verify capabilities and a whole wiki-page read through that exact
registered token connection, then save its mapping. Native OAuth success does
not validate token access. Keep this established ChatGPT workaround separate
from both native Codex setup and registered-app OAuth investigation.

## Package and adapter boundaries

The package's `.app.json` declares registered MCP Service only. Native Codex
connections still require the setup above.

The [native adapter](native-setup.md) inspects, backs up and adds URL entries or
saves a reviewed instruction block. It does not authenticate or save scopes for
new entries: complete scope configuration and login above. Its
`--codex-apps-checked` assertion records inspection of alternatives and explicit
selection of native setup, not absence of a matching app or verified access.
Keep existing tool approval settings. Update installed plugins through their
supported manager; backend system guidance has a separate release process.
