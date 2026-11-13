# Set up your knowledge bases in Claude

Claude Desktop, Claude Code and Claude on the web each keep their own list of
connections. This guide is written for someone who is not technical. The
assistant does the checking and the typing it can do; you do only the clicking
and signing in that it cannot.

## What the assistant does, and what you do

**The assistant** (you only need to ask) works out which KBs you are entitled to,
which are already connected, and which are missing. For each missing KB it gives
you the exact name and address to enter, in a block you can copy. It then checks
that the KB really answers, and reports the result in plain words.

**You** click through a few screens in the Claude app and sign in with your usual
account. Nobody asks you for a password, a code or a token in the chat; if
anything does, stop.

Start by saying, in Claude Code or Claude Desktop:

> Set up my knowledge bases. Tell me which ones are already working and which
> need connecting. For each one that needs connecting, give me the name and
> address to copy and walk me through the clicks.

## Install the KBs plugin (once on Desktop, once on claude.ai)

The plugin brings the setup and retrieval skills. Claude keeps separate lists
for your computer and for your claude.ai account, so add it in **both** places.
Both use the same steps and the same address: `bgpslz/kb-plugins` (the
assistant gives you the current address). The repository must be public, or
claude.ai cannot fetch it and shows only "Failed to add marketplace".

1. **Claude Desktop (your computer):** open **Settings → Plugins**, choose
   **Add marketplace**, enter the address, click **Sync**, then add **KBs**.
2. **claude.ai (your account, for chat and Cowork):** open
   [claude.ai](https://claude.ai) in a browser, go to **Customize → Plugins →
   Add → Add marketplace**, enter the same address, then add **KBs**.
3. Check: **KBs** appears with its version in both places, and a new Code
   session lists its skills. If an old copy is stuck, remove it and add it
   again rather than clicking Update.

If "This marketplace is already added" appears although you see nothing in
Desktop, an older copy exists on your claude.ai account. Remove that marketplace
there first (**Customize → Plugins**), then add it again.

## Make a KB visible in Claude Desktop

Use this when setup finds a KB you are entitled to that is not in your
Connectors list yet. The assistant fills in the name and address from your KB
list, so you never type them from memory.

1. In Claude Desktop, click **Customize** in the sidebar, then **Connectors**.
2. Click **Add**, then **Add custom connector**.
3. Paste the name and address the assistant gave you:
   * **Name:** `{KB name}`
   * **Address:** `{mcp_url}`
4. If asked how to register, choose **CIMD**. If sign-in fails with CIMD,
   remove the connector and add it again with **DCR**. Never choose the option
   that asks for your own client ID or secret.
5. Click **Add**. A sign-in page opens in your browser. Choose your usual
   account (normally Google) and approve if asked.
6. Check it worked. Both of these should show the KB, with no commands needed:
   * In **Customize → Connectors**, `{KB name}` is listed with a tick and no
     warning.
   * In a Code session, click **+ → Connectors**. `{KB name}` is listed with its
     switch on.

If the KB is missing or shows a warning, click **Reconnect** next to it. If
sign-in says you do not have access, ask the person who manages KB access to
register your account for that KB. Then tell the assistant "done" so it can run
its own check.

Repeat the five steps for each KB that needs connecting. Finish one sign-in
before starting the next.

**Connectors only need adding once.** A connector added in Desktop is saved to
your account, so it also appears in Code sessions and, after a browser refresh,
in claude.ai chat. (Plugins are different: install them in both places, above.)

## Notes for the assistant

- **Prefer a Desktop/claude.ai connector.** For a KB with no server bundled in
  this plugin, guide the user through the connector steps above. A native
  `claude mcp add` or `~/.claude.json` entry works for Claude Code alone but
  appears on no Desktop screen, so a non-technical user cannot see or repair it.
  Use the native adapter only when the user asks, or for a terminal-only machine.
- **Show the values.** Take each KB's name and explicit `mcp_url` from the
  registry result and print them in a copyable block. Never derive one URL from
  another and never ask the user to remember an address.
- **Visual check first.** The two screens in step 5 are the success test the
  user can perform. CLI commands, `/mcp` and asking the assistant are for
  diagnosis only; do not send the user to them as the normal check. After the
  user confirms, verify with a real authenticated read and report it separately
  (retrieval, instructions, capture are reported separately, as in the skill).
- **CIMD first.** The sign-in server advertises both CIMD and DCR, and accepts
  public clients with PKCE. CIMD worked in a live test on 13 November 2026 with
  no extra steps; DCR is the fallback. Neither registration method is ever a
  reason to ask for secrets.
- **Confirm the wording.** The menu names above follow the current Claude Desktop
  and Claude documentation, but "Add custom connector" is unconfirmed against the
  live app. If the user sees different wording, follow what is on screen and
  report the difference so this guide can be corrected.
- **Duplicates.** The Claude documentation says Claude Code treats a connector at
  the same address as an existing server as one connection. This is untested
  here; on a clean machine, check that a bundled `mcp-service` or `pkb-service`
  and a connector for the same address do not both appear. Do not add a connector
  for a service the plugin already bundles; reconnect it instead (Code: `/mcp`).
- **Bundled servers.** The plugin bundles `mcp-service` and `pkb-service`. If
  either needs signing in again, point the user to **+ → Connectors** or `/mcp`
  and ask them to choose Reconnect or Authenticate. Do not add duplicates in
  user, project or local scope.
- **Never ask for secrets.** Do not request passwords, codes or tokens in chat,
  and do not ask MCP Service to issue or relay a KB token.
- **Separate stores.** Claude Chat (web, desktop, mobile), local Claude Code and
  cloud Code have separate connections and separate instruction stores. A desktop
  Code tab may execute remotely. Updating one does not update the others.

## Instructions that load the KB guidance

Cloud Claude profile preferences are account-level Chat instructions. Local Code
user instructions are `~/.claude/CLAUDE.md`, independent per machine; changing
the user's personal file needs their explicit approval, so show the managed block
first and ask. Cloud Code needs instructions in its own execution environment.
Verify placement and persistence after each separately authorised change.

## Technical notes

The [native adapter](native-setup.md) discovers user, local, project and enabled
plugin servers before planning additions. Saving a native entry does not approve
project servers, connect OAuth, or prove the Desktop Code tab has loaded it.

Tool permissions and "Always allow" are separate choices, not requirements for
authentication. Preserve existing approvals and distinguish a missing broker
grant from an incomplete login. Identify the actual OAuth client before
requesting administrator approval; do not copy Open WebUI credentials.
