---
name: setup-kbs
description: Set up or repair KB connections and saved operating instructions for the current client. Use for an explicit setup request; verify local capture separately.
metadata:
  version: "1.3.8"
---

# Set up knowledge bases

Make the user's permitted knowledge bases usable in this client, and arrange for
its assistant to load the current KB operating instructions. Run this skill for
an explicit setup, connection check, addition or repair request. Ordinary chats
use the saved setup; they do not repeat discovery or reconciliation.

## Which skill does what?

| Skill | Job |
| --- | --- |
| `setup-kbs` | Configure or repair connections and saved instructions, then report what was verified. |
| `use-kbs` | Load the system-wiki index and the applicable client page before substantive work in a new context; restore them when context is lost. |
| `use-standard-kb` | Optional retrieval help for a selected KB: read its wiki, choose source tools and stop when the evidence is sufficient. |

The live system-wiki supplies operating guidance. The retrieval helper does not
replace that guide or configure anything. There is no required two-skill sequence
for each question: load missing guidance with `use-kbs`, then retrieve as the
loaded guide requires. Consult `use-standard-kb` only when its retrieval detail
is useful. A system-wiki outage uses the packaged fallback, without depending
on that helper being invoked.

## 1. Identify the client and preserve its existing setup

Setup must work for a non-technical user. Do everything the tools allow yourself
(inspect, compare, verify); give the user only the clicks and sign-ins that need
them, as numbered plain-English steps with the exact button names, names and
addresses to copy, and a visible success check. Never reply "ask the assistant"
or send them to a command line for a normal step.

For Claude, follow the client guide's Connectors flow: a missing KB is added as a
connector in Customize → Connectors, using the name and `mcp_url` from the
registry, and success is what the user sees on that screen and in a Code
session's + → Connectors list.

For local Codex, follow the client guide's step-by-step graphical setup flow.
Read its technical notes and linked reference before doing the work. When user
input is needed, provide the exact Settings path, server Name, Streamable HTTP
selection, URL, fields to leave blank, Save/Authenticate actions and browser steps.
Do not replace required configuration instructions with “ask the assistant”.
Carry out steps yourself when tools permit, without making the user repeat them.
Keep file paths, commands and protocol detail in the technical reference; include
every field value and action the user actually needs in the normal setup flow.

Identify the client, machine and actual execution location. A cloud task remains
cloud when viewed in a desktop app. Read the relevant
[client connection guide](references/client-setup.md) for its authentication and
instruction settings. Existing connection names are local labels, not universal
service identifiers. For local Codex Desktop/CLI, follow the client guide's
linked native OAuth configuration recipe: inspect/back up local settings,
configure MCP Service, authenticate with the supported native CIMD flow, discover
entitled KBs, configure and authenticate each requested KB, then verify reads and
refresh. Perform local configuration work for the user when available; the user
completes browser sign-in. Installing this plugin does not perform these steps.
Cloud ChatGPT uses its separate service-local bearer-token connection procedure.
Inspect registered apps as well as native servers, but an app's presence does
not prove access or block an explicitly selected native route. Preserve working
connections and their names; do not replace them merely to match an example.

Preserve working endpoints, native credentials, callbacks and unrelated settings.
Reuse configured or bundled servers before adding one. Diagnose an unknown client
registration or missing grant separately from an incomplete user login. Use the
actual client's callback, resource and scopes; never request secrets in chat or
reuse another client's secret. Open WebUI uses its own filter and server-side
capture, so do not attach this plugin's retrieval loop to its ordinary chats.

## 2. Discover permitted KBs and verify access

First establish MCP Service access using the deployment's supplied bootstrap
endpoint and the client guide; do not assume a new client already has it. Through
the selected authenticated MCP Service connection, verify
Registry Protocol 2 and obtain the entitled KB list. Discovery belongs to this
explicit setup step; `use-kbs` must not rediscover it on every chat or turn.

Use the record’s explicit `mcp_url` for the connection and optional `account_url`
for its separate token page. Never derive one URL from the other. Confirm
`registry_protocol_version=2` in the list response before treating it as authoritative.

Match each immutable KB UID and service ID to the client's actual connection ID.
For each required KB, verify KB Protocol 1, the required capabilities and a
substantive authenticated wiki read. A successful login or registry listing alone
does not prove access. If build support is being checked, also read its Build
Guide; report a build-only failure separately from retrieval.

After new OAuth login or grant repair, repeat reads beyond access-token expiry
without another sign-in and check a fresh connection. Test multiple services over
one waiting period where practical. Record the exact native server or registered
app route for each result; do not substitute another route to declare success.
Report refresh as unverified if it could not be checked. Diagnose issuer/resource
and client-registration errors separately from rejected refresh credentials.

An unavailable or incomplete registry response must not erase configured KBs.
A complete authoritative response may remove revoked entries from the managed
inventory. Live 401/403 responses govern access; do not bypass them with another
credential or protected cached content. Removing a client connection does not
revoke its server-side credential.

## 3. Save and test the instruction-loading arrangement

Generate the managed `kbs-instructions v2` block from the packaged canonical
sources. Save the actual MCP Service binding and each KB's local connection ID
with its immutable KB UID/service ID; example `casdoor_*` names are not assumed
on other machines. It saves the KB inventory and tells `use-kbs` to read the complete
system-wiki index plus the applicable surface page at one validated revision.
Check the live descriptor and read both pages; declaration of the interface
alone is not evidence that the instructions reached the assistant. If loading
fails, preserve working retrieval with the packaged fallback and report degraded
guidance. A server update or a file read-back does not prove startup loading.

Reconcile only the managed block through the client's supported instruction
setting. Preserve unrelated instructions; inspect malformed or ambiguous legacy
blocks rather than replacing the whole file. Save only within the user's
requested scope. A check or proposed instruction draft does not authorise a save.
Changing Bruno's personal `~/.claude/CLAUDE.md` requires his approval. Each machine,
Chat account and cloud execution environment has its own instruction store.

After changing installed skills or instructions, verify them in a fresh session.
Report instruction-based loading as such. Do not claim an automatic startup hook
or verified resume/separate-agent loading without evidence from that context.
A working automatic hook is not a prerequisite for using instruction-based
loading. Do not remove another working instruction source just because its
replacement files exist.

## 4. Report separate results

| Result | Evidence to report |
| --- | --- |
| KB inventory | Whether discovery was authoritative and complete, and which connections were retained, added or left unresolved. |
| Retrieval | Which required KBs passed authenticated capability and wiki reads. |
| Instructions saved | Where the managed block was saved, or whether it is still a draft. |
| Guidance delivery | Whether complete matching-revision pages reached this context; distinguish that from fresh-session, resume and separate-agent tests. |
| Capture | Verified separately, not requested, unsupported or unverified. |

Do not collapse these into an unqualified “setup complete”. Chat and cloud Code
setup covers retrieval and guidance; it requires no capture installation or
capture receipts. Local capture problems must not prevent working retrieval or
instruction setup. Use only declared build/capture capabilities and report their
optional checks independently.

## Optional tools and local capture

- For repeatable readiness reports and instruction drafts, use the read-only
  [evidence helper](scripts/reconcile.py) and its [input guide](references/setup-evidence.md).
  It evaluates supplied evidence; it does not discover settings, log in or save.
- For authorised local Code configuration changes, use the
  [native adapter](scripts/native.py) and [save procedure](references/native-setup.md).
  Inspect/plan before saving. Cloud tasks cannot edit a user's host-local settings.
- For a plugin-version or duplicate-installation problem, inspect source, package
  and active paths separately. Historical caches alone are not duplicate active
  installations. Use the supported plugin manager, never an installed-cache edit.
- For explicitly requested automatic-loader integration, use the
  [developer guide](references/system-wiki-client.md). Host integration requires
  an authenticated bridge; a settings entry does not establish one.
- For requested local capture on supported macOS Codex/Claude Code sessions, use
  the [capture guide](references/local-capture-setup.md) and [installer](scripts/install.py).
  Check Python 3.11+ and the actual OS. No Windows/Linux installer is shipped.
  Preserve exclusions, receipts, hook trust and unrelated hooks. Enter capture
  credentials through the native Keychain prompt, never chat, arguments or logs.
  Verify real new deliveries per machine and CLI/desktop surface before claiming
  readiness. Do not install capture for cloud Code or ordinary ChatGPT/Claude chat.

Capture stays outside the assistant: no routine capture-tool calls, reference
tags or in-chat include/exclude commands. A human chooses destinations in Capture
Review; optional manual paste is separate from setup.
