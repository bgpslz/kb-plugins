# Set up your knowledge bases in Codex

If you are reading this guide through KBs in **ChatGPT or Codex**, the **KBs**
plugin is already installed and enabled in **Plugins**. That is the first
requirement for this system.

To install KBs on another computer, or help someone get started, use the
[installation instructions](https://github.com/bgpslz/kb-plugins/blob/main/INSTALL.md).

The steps below configure **native connections for local Codex**, on the computer
you want to use. Use the **Codex desktop app** for the settings, then the browser
window it opens for sign-in. This is the verified local Codex connection route.

Creating a registered connection for ChatGPT's cloud service is a different
procedure, performed at **chatgpt.com in a browser**. That registered OAuth route
hit the Casdoor incompatibility described below. It is not the route used by
these Codex instructions.

## 1. Start setup

Start a Codex chat and say:

> Set up my knowledge bases on this computer. Check any connections already
> configured, tell me which ones need adding, and give me the exact server names
> and addresses to enter. Guide me through the settings and sign-in steps, then
> check that access works and stays connected.

Keep that chat open while you complete the following steps. If a server is
already configured, Codex should check it rather than ask you to add it again.
If Codex does not have the MCP Service address, ask the person who provides your
KB access for it before continuing.

## 2. Connect MCP Service

MCP Service tells Codex which knowledge bases your account can access.
Add it to the desktop app's native **MCPs** list as follows.

1. Open **Settings → Plugins → MCPs**.
2. Choose **Add**, then the option to add a custom MCP server. This opens
   **Connect to a custom MCP**.
3. Enter the following values for **MCP Service**:

   | Field | Value |
   | --- | --- |
   | **Name** | `casdoor_mcp_service` |
   | **Type** | **Streamable HTTP** |
   | **URL** | Copy the **MCP Service address supplied by Codex** |
   | **Bearer token env var** | Leave blank |
   | **Headers** | Leave blank |
   | **Headers from environment variables** | Leave blank |

4. Click **Save** and return to the MCP server list. The switch beside the new
   server should be on.
5. Click **Authenticate** beside `casdoor_mcp_service`. The connection form has
   no OAuth selector: this Authenticate button starts OAuth sign-in after saving.
6. On your KB system's sign-in page, choose **Google**, select the account that
   has KB access, and complete the sign-in and any consent requested.
7. Return to the Codex chat and say:

   > MCP Service sign-in is complete. Check that connection and list the
   > knowledge bases available to me.

## 3. Connect your knowledge bases

Tell Codex which of the available knowledge bases you want to use. It should
provide the exact **Name** and **URL** to enter for each one.

Codex should list each selected knowledge base, such as **My PKB** or
**Organisation KB**, with its connection name and server address. Copy those
values: each knowledge base has its own address. Use only the knowledge bases
confirmed as available to your account.

For **each** selected knowledge base:

1. Return to **Settings → Plugins → MCPs → Add** and open the custom MCP form.
2. Copy its **Name** and **URL** from the values supplied by Codex.
3. Select **Streamable HTTP**. Leave **Bearer token env var**, **Headers** and
   **Headers from environment variables** blank, as for MCP Service.
4. Click **Save**, return to the list and check that the server is switched on.
5. Click **Authenticate** beside that server and complete Google sign-in and
   consent. Finish this connection before starting the next one.
6. Return to the chat and tell Codex which knowledge base you have signed into.

## 4. Check and finish

Once you have signed into the selected knowledge bases, tell Codex:

> Check MCP Service and each selected knowledge base using the native MCP
> connections we just configured. Read their overview pages, check that access
> still works after seven minutes without another sign-in, and save this
> computer's setup for future chats. Tell me which connections passed.

Codex should carry out the checks and save the local setup. The seven-minute
wait checks that you will not have to sign in again whenever a short-lived access
token expires. You can then use the confirmed knowledge bases in future Codex
chats on this computer. Repeat setup on each additional computer.

If Codex asks you to restart or open a fresh chat to load the new connections,
do so and ask it to finish the same checks.

## If a step fails

Show the error to Codex and tell it which server you were connecting. Keep the
existing entries while it checks the problem; do not create another copy or keep
repeating sign-in. The technical notes below identify the material issues found
with this deployment.

## Technical notes for the assistant or technician

### Scopes and OAuth are discovered by Codex

The graphical form needs the server name, Streamable HTTP and the full MCP URL.
It does not need a bearer token, custom headers or an OAuth dropdown. Codex starts
OAuth from **Authenticate** and obtains the service's scope from discovery.

The deployment checked on 10 November 2026 advertises the following scopes.
Verify the actual metadata for the deployment being configured:

| Service | Required API scope |
| --- | --- |
| MCP Service | `kb_registry:read` |
| Personal and organisation KBs in the example deployment | `personal_rag:read` |

[Codex's documented behavior](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)
is to use the scope in the authentication challenge, or the protected-resource
metadata if the challenge omits it. Its OAuth library can also request
`offline_access` for refresh. Therefore users should not be sent looking for a
scope field absent from the graphical form. Check the actual requested/granted
scopes if sign-in or refresh fails. The previously verified explicit scope lists
and technician-assisted configuration are in the [connection reference](connection-reference.md).

Codex selects CIMD automatically when discovery advertises CIMD and the compatible
public-client method. The CLI recipe in the reference explicitly selects CIMD
if a technician needs to diagnose registration. Do not send non-technical users
to the command line as the normal setup procedure.

### Native Codex and registered apps use different OAuth routes

This procedure uses **MCPs → Servers** in Codex. It does not create a registered
app through the ChatGPT website. The native Codex client verified in this
installation is `https://chatgpt.com/oauth/codex/client.json`; the registered-app
client is `https://chatgpt.com/oauth/client.json`.

The old registered PKB OAuth app retained Auth0 metadata. A new registered app
reached Casdoor but failed because its client metadata selected `private_key_jwt`
while the deployed Casdoor accepted only `none` with PKCE. These findings do not
show a failure of native Codex OAuth. Do not substitute registered `codex_apps`
reads or the ChatGPT token route to declare native setup successful.

### Use the correct issuer and resource

Obtain the issuer from the live service metadata. For example, an MCP Service
at `https://mcp-service.example.org/mcp` might use issuer
`https://mcp-service.example.org/auth`. These are example addresses, not live
connection values. Each resource must be the exact service URL, including `/mcp`.
If saved settings contain a retired issuer or an origin-only resource, inspect
discovery and the selected connection rather than repeating consent. A rejected refresh token needs repair of
that existing grant; it is a different problem from stale app metadata.
Respect service access denials and check entitlement rather than trying another
credential to bypass them.

### Save and verify this machine's mappings

Reuse suitable existing names and preserve unrelated configuration. During setup,
record the actual MCP Service connection and each KB's UID, service ID and local
connection name in this computer's managed KB instructions. Example `casdoor_*`
names are not assumed to exist on another machine. Discovery of a KB alone does
not establish its connection or grant access.

Validate system-wiki protocol 1 and complete matching-revision index/local-Codex
pages, Registry Protocol 2, and KB Protocol 1 plus substantive KB wiki reads.
After new login or grant repair, verify post-expiry reads and access from a fresh
Codex connection. Report any unverified result explicitly. Save instructions
without changing unrelated instructions; capture setup remains separate.

The native connections in the verified local installation passed login/read
checks and post-expiry reads;
PKB refresh rotation was also confirmed against broker metadata. That recovery
used native Codex login commands. The graphical procedure above follows the
observed form and documented discovery behavior; its complete new-user flow
still needs acceptance on a second computer. Do not report that test as already passed.

For configuration files, explicit scope lists, recovery commands and package
boundaries, use the [assistant/technician connection reference](connection-reference.md).
ChatGPT's separate bearer-token procedure is also in that reference; it does not
configure Codex on a user's computer.
