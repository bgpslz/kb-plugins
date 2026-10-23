---
name: setup-kbs
description: Explicit-only installation, check, repair and reconciliation of KB connections, protocol compatibility and surface-specific instructions; local Code capture is verified separately.
disable-model-invocation: true
metadata:
  version: "1.3.5"
---

# Setup KBs

Use when explicitly asked to install, check, add, repair or reconcile KB setup.

## Identify and reconcile

1. Identify the actual client/surface, machine and execution environment before
   selecting actions. A cloud Code task viewed in a desktop app remains cloud.
   Open WebUI is the primary surface for capturable ordinary chat. ChatGPT and Claude Chat receive retrieval/guidance setup with no assumed automatic capture. Unknown execution permits retrieval
   setup but no capture installation. Open WebUI retains its separate filter/OAuth
   and server capture; add no second retrieval loop or model tool attachment.
2. Inspect source/package/active skill paths and versions independently. The current
   package inventory is in scripts/package.json. use-kbs is the transition
   instruction loader; use-standard-kb remains until replacement acceptance. Diagnose duplicate active sources without uninstalling
   them. Historical caches alone are not duplicate active installations. Use the
   supported plugin manager; never release by editing generated plugin caches.
3. Read the [client connection guide](references/client-setup.md) for the target
   authentication and instruction stores. Preserve existing connections and native
   credentials. During explicit setup only, establish MCP Service, verify Registry
   Protocol 1 and fetch entitled KBs. Registry outage/incomplete results preserve
   configured retrieval. Capture Protocol/tools/credentials are not prerequisites.
4. Match immutable KB UID, service ID and actual connection ID separately; display
   names and OAuth client IDs are not interchangeable. Reuse bundled/native servers
   before adding an entitled service. Use actual client callback/resource/scope
   values and diagnose missing broker grants separately from user login. Preserve
   old callbacks. Never request secrets in chat or reuse another client's secret.
5. Verify each KB's authenticated capability response, KB Protocol 1 and required
   capabilities, then a substantive authenticated wiki read. Login alone is
   insufficient. A declared build capability requires get_build_guide; optional
   capability failures are separate from retrieval. Runtime 401/403 takes precedence
   over cached inventory. A complete authoritative registry response can remove a
   revoked KB from managed inventory; client removal does not revoke credentials.

For repeatable diagnostics and instruction drafts, use the packaged
[evidence helper](scripts/reconcile.py) following its
[schema/manual path](references/setup-evidence.md). It reads supplied evidence and
prints JSON; it does not log in, discover native settings or mutate configuration.
Report unassessed checks honestly. Do not require a source clone to use it.

For native Code configuration discovery and additive persistence, use the
[native adapter](scripts/native.py) with its
[supported stores and save procedure](references/native-setup.md). Inspect/plan
first. An explicit save is separate from a report/source-only request. Preserve
existing endpoints across scopes/plugins, and verify authentication/loading
independently of file read-back. Cloud/unknown execution cannot save host-local
settings; account Chat preferences retain their manual/native UI path.

## Instructions and readiness

Reconcile only the managed `kbs-instructions v2` block. Preserve unrelated rules;
malformed/ambiguous legacy blocks require explicit reconciliation, not replacement
of the whole file. The helper can read an existing file and output a proposed
replacement. Apply through the client's supported setting only within authorised
scope; personal `~/.claude/CLAUDE.md` changes require Bruno's approval. Reconcile
account preferences and each machine/cloud Code instruction store independently.

Use use-kbs as the small instruction-based bootstrap: before substantive work,
load the complete system-wiki index plus the applicable surface page at one
validated revision. Restore missing instructions after compaction/resume or in
a separate agent context. Do not preload the legacy manual beside successful
loading. Keep use-standard-kb available during staged replacement; remove it
only after live and degraded acceptance on affected surfaces. Generate managed
blocks and their short fallback from the packaged canonical sources.

Use the packaged retrieval fallback unless MCP Service actually declares the
compatible system-wiki interface. That interface is a separate dependency, not
assumed deployed. A static instruction is weaker than tested startup injection.
A startup hook alone is insufficient: prove the complete required pages reach
the model before useful work, including fresh, resumed and separate contexts.
Do not retire working guidance or mark a surface complete before that evidence.

For explicit loader integration work, read the
[system-wiki client guide](references/system-wiki-client.md). The packaged core
provides load_startup(context, surface, execution) for the two-page bundle. Its
host integration remains inactive: it requires an authenticated bridge and optional
trusted account/auth binding. Do not manufacture either from a config entry.

Report registry reconciliation, retrieval readiness, guidance loading and capture
readiness independently. Start a fresh session after changing installed skills or
instructions. Chat/cloud Code setup completes with retrieval acceptance alone:
no capture hooks, capture-only credentials, model capture directives or receipts.
Local capture health must not block retrieval setup or instruction generation.

## Supported local capture only

For supported **local Codex/Claude Code on macOS**, read the
[capture guide](references/local-capture-setup.md) and use the packaged
[installer](scripts/install.py). Detect OS/native versus WSL and a durable Python
3.11+ first. No Windows/Linux installer is shipped. Unsupported local capture
does not prevent retrieval setup. Human paste is optional and outside setup.

Preserve the capture boundary, exclusions, receipts and unrelated hooks/notify.
Credentials are entered directly through the native Keychain prompt, never chat,
arguments or logs; they are separate from retrieval OAuth. Preserve hook trust.
Verify real new hook-triggered turns/receipts for each used CLI/desktop surface
and machine before claiming capture readiness. Keep working external capture
while updating retrieval guidance; reconcile any legacy capture migration using
the capture guide. No capture setup applies to cloud Code or ordinary chat.
