# OpenAI connection and instruction targets

## Choose the route for the actual client

| Execution surface | Preferred PKB connection | Authentication |
| --- | --- | --- |
| Local Codex Desktop or CLI | **PKB Service (OAuth)** | Existing registered OAuth app; sign in through Casdoor. Reuse a working native OAuth connection as well. |
| Cloud ChatGPT | **PKB Service (token)** | Service-local token entered in the connector's credential field. OAuth has not worked here; investigation remains open. |
| Cloud Codex or unknown execution | Verify that environment's supported connection mechanism | Do not infer local OAuth or cloud ChatGPT token support from a desktop window. |

Use the connection's display name in user instructions. Users should not need to
choose server identifiers, edit CLI configuration or understand app IDs. Resolve
technical identity as the assistant and retain the actual connection ID in setup
evidence. These known Bruno PKB mappings are not a universal tenant inventory:

| Registered app | App ID | MCP endpoint |
| --- | --- | --- |
| PKB Service (OAuth) | `asdk_app_6ab29f2769908191afa0c980c197354e` | `https://bruno-rag.summerleaze.com/mcp` |
| PKB Service (token) | `asdk_app_6ab2b686b2d08191a794afb44cd95e37` | `https://bruno-rag.summerleaze.com/mcp` |

**PKB Service (OAuth)** is the preferred display name for the connection formerly
called **PKB Service v2**. Recognise either name during the transition and match
the same app ID and endpoint. Plugin guidance cannot itself rename the registered
app in the provider's directory: if the client still shows the former name,
identify it by that ID rather than creating a second app. When setting up a
connection with an editable display name, use **PKB Service (OAuth)**. Preserve
existing grants and identities when repairing an existing installation.

First inspect tools and the client's plugin/connection state. Reuse **PKB Service (OAuth)**
locally; when missing, find and recommend that existing app through the
supported plugin manager. Directory search may omit private/workspace apps;
use the client's workspace/personal listing and known app identity before
concluding that it does not exist. Preserve its registration, grant, endpoint,
callbacks and scopes. Do not create a replacement custom app or another native
MCP entry merely because it is absent from `codex mcp list` or file inspection.
App-backed connections and native MCP servers are separate inventories. Existing
native names such as `pkb_service` or `casdoor_pkb_service` are local labels.

The shared KBs package declares only MCP Service in `.app.json`. It recommends
the surface-appropriate PKB app during setup instead of making both PKB apps
mandatory dependencies. No verified alternative-dependency or per-client app
selector is available in the packaging contract. Do not invent selector fields
or require cloud users to authenticate the local OAuth app. Removing a package
mapping is not an instruction to uninstall the user's existing connection.

## Diagnose before changing anything

| Observed state | Recovery action |
| --- | --- |
| Not installed, confirmed in the client's plugin listing | Recommend/install the named app for this surface through the supported manager, then connect it. |
| Installed but disconnected, confirmed by client status | Enable/connect the existing app and complete its sign-in flow. Preserve its identity. |
| Authentication expired or rejected (for example 401/invalid grant) | Reconnect the same app. Local OAuth should open Summerleaze/Casdoor sign-in; an old Auth0 grant may need renewed consent. Do not assert that migration caused the failure without testing. |
| Tools unavailable in this chat, installation/authentication unconfirmed | Check enablement, workspace/account, policy and tool exposure; refresh/restart in a fresh chat. Inspect app-detail/DNS/timeout failures separately. Missing tools alone proves neither uninstall nor grant expiry. |
| 403/access denied | Follow the actual denial and check membership/administrator permissions. Do not bypass it with another credential or protected cache. |

The assistant can guide browser consent but the user completes sign-in in the
native flow. Never request passwords, service tokens or OAuth secrets in chat.
For cloud ChatGPT, use the registry record's explicit `account_url` and the
service's token UI, then enter the token in **PKB Service (token)**. Do not derive
account URLs or ask MCP Service to issue/relay a KB token. Do not silently switch
authentication routes after a denial. Keep investigating cloud OAuth separately
so the supported route can eventually be standardised.

Public OAuth discovery is diagnostic evidence only. Check the protected-resource
metadata and its declared authorization server when investigating registration,
callback/resource/scope issues. Casdoor discovery does not test a saved grant.
Cached tool definitions do not prove current installation or authenticated access.

After connection or re-authentication, verify KB Protocol 1, required capabilities
and a substantive `wiki://index.md` read through that exact connection. Record
client, actual connection identity and outcome. Token and native OAuth reads do not establish
access through the app-backed OAuth connection.
Test fresh and existing-user setup on Desktop and CLI independently, and cloud
token setup separately. Do not report these passed from source/package tests.

## Instruction targets and native adapters

Cloud ChatGPT Custom Instructions and local Codex instructions are independent.
The audited local Codex store is `~/.codex/AGENTS.md`; verify the current client's
supported mechanism before applying. Reconcile local stores per machine and
cloud Code stores in their actual execution environment. Cloud ChatGPT account
preferences do not configure Codex. Verify placement/persistence where manual UI
work is necessary.

The [native adapter](native-setup.md) inspects supported file stores, not app-backed
connections or their grants. A new Codex native entry requires a separate client
check confirming no matching app connection exists, recorded with
`--codex-apps-checked`. This is an operator assertion, not automated discovery.
Prefer repairing/recommending the existing OAuth app; a native addition is only for
an explicitly intended native route after checking both inventories. Native
configuration presence is not authenticated wiki-read acceptance.

Tool-approval preferences are a separate user choice, not an authentication
requirement or an automatic “Allow all tools” default. Do not expand permissions
merely to avoid prompts. Identify the actual OAuth client used by login before
requesting administrator grants, rather than granting similarly named apps.
