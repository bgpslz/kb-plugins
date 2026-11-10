# Native Code setup adapters

Use the packaged `scripts/native.py` or source `setup/native.py` with Python
3.11+. It discovers native configuration, plans additive changes, and saves a
reviewed plan only through an explicit `apply` command. It does not authenticate,
contact MCP endpoints, start servers, install capture, change grants/approvals,
remove connections or edit installed plugins.

## Inspect and plan

```sh
python3.12 setup/native.py inspect --surface codex-desktop --execution local
python3.12 setup/native.py inspect --surface claude-code-cli --execution local
# After inspecting alternatives and explicitly selecting native setup:
python3.12 setup/native.py plan --surface codex-cli --execution local --scope user --desired desired.json --codex-apps-checked > native-plan.json
```

In an installed skill, replace `setup/native.py` with its `scripts/native.py`.
Available Code surfaces are the same as the evidence helper. Execution must be
explicitly local before planning/saving; cloud/unknown targets permit inspection
only. No host-local configuration is copied into a remote session.

`desired.json` is a list of **authorised** additions, obtained during explicit
setup from actual entitled-service/client metadata, for example:

```json
[{"connection_id":"example_kb","url":"https://example.invalid/mcp"}]
```

The adapter is not an entitlement authority. First reconcile registry/direct KB
evidence through the setup workflow; never infer a UID, tenant URL, OAuth audience
or grant from these examples. No secret/token/header field is accepted in an
addition. HTTPS is required except HTTP loopback for local testing. Existing
credential-bearing/dynamic endpoints are not printed and may require manual
resolution before adding anything.

Native stores supported:

- Codex user `~/.codex/config.toml`, project `.codex/config.toml` layers through
  the repository root, and user `AGENTS.md`. `--codex-home` selects a verified
  custom config root; the CLI honours an already configured `CODEX_HOME` when
  inspecting the real home. User/project scopes are supported.
- Claude Code user/local servers in `~/.claude.json`, project `.mcp.json`, and
  enabled plugin servers found through the install registry and settings. User,
  project and local scopes are distinct. Only the default Claude configuration
  layout is supported; custom `CLAUDE_CONFIG_DIR` needs manual resolution.
- Claude plugin candidates come from the enabled installation registry, not a
  cache-directory scan. Unresolved enabled plugins or external MCP manifests
  block additions until inspected. Preserve bundled servers instead of duplicating
  them under a new alias.

`--home` and `--project` select an isolated home/project for testing, or the actual
locations being configured. They do not assert that this host is a cloud machine
or that a desktop task executes locally. Inspection returns only whitelisted
connection metadata, source-file hashes and limitations, not credentials. It
observes configuration candidates; managed policies, trust, project approvals,
hosted connectors, precedence/shadowing and actual tool availability still require
the native client's own verification.

Codex file inspection and `codex mcp list` do not enumerate app-backed OAuth
connections. Inspect those in the client before any native addition. The planner
refuses a new Codex native endpoint unless `--codex-apps-checked` records that
alternatives were inspected and native setup explicitly selected. A registered
app can exist yet have stale metadata or incompatible authentication; its mere
presence does not block a requested native connection. This operator assertion
is stored in the plan; it does not test installation, absence or grants.
Existing native endpoint reuse and instruction-only plans need no such assertion.

The adapter adds URL entries only; it does not persist required OAuth scopes or
authenticate them. Complete the client's scope configuration, native login and
read/refresh verification using the client guide before claiming access.

Endpoint reuse is conservative across scopes: reuse an already configured endpoint
instead of adding another name. If it is disabled, diagnose/reconnect explicitly.
Existing same-name/different-endpoint entries are never overwritten. Plans contain
no removals and no automatic OAuth client/secret or approval changes. Stored public
callback metadata is reported where available; absent callbacks remain unknown.
Obtain the exact callback through native login/provider metadata, not a hard-coded
formula. Callback/resource/scope comparison remains in the evidence helper.

## Save a reviewed plan

```sh
python3.12 setup/native.py apply --plan native-plan.json
```

Use this only when live configuration changes are authorised. A phase limited to
source work or a report does not authorise applying it to personal settings.
The command re-inspects every source and refuses stale or inconsistent plans.
Codex additions append validated TOML without rewriting unrelated bytes. Claude
JSON additions preserve unrelated values, including hooks/trust/authentication
metadata, while serialising the target file again. Unsupported/ambiguous layouts
fail without replacing them. A temporary file is atomically renamed into place,
existing file permissions are preserved, and the prior bytes are backed up in a
private sibling file. The saved file is re-read and additions rediscovered.

The writer lock coordinates this adapter's saves; native apps do not share that
lock. Avoid concurrent settings edits. A failed verification leaves the private
backup for inspection instead of overwriting a possible intervening native edit.
Automatic persistence is currently tested on POSIX stores. Windows uses the
manual/native-client path until equivalent persistence checks are verified there.

An unchanged fresh plan is a no-op. Re-running an old changed plan is refused;
inspect/plan again rather than replaying it. Backups may contain existing private
settings and are never printed. Source caches are never configuration targets.

## Managed instructions

Generate the complete managed block with the evidence helper, then plan it:

```sh
python3.12 setup/native.py plan --surface codex-cli --execution local --block managed-block.md > instruction-plan.json
python3.12 setup/native.py apply --plan instruction-plan.json
```

Connection changes and instruction changes are separate single-file plans, not
an implicitly atomic multi-file transaction. Verify the first result before
preparing the next. Only the delimited managed block changes; unrelated instruction
text is preserved and duplicate/malformed/unknown managed blocks are refused.
Personal Claude instructions additionally require Bruno's approval; the explicit
`--personal-claude-approved` flag records that prerequisite, it does not grant it.

## Acceptance after saving

`saved_and_reread` means file persistence passed, **not** authenticated retrieval,
native loading, capture or deployment readiness. Use the native MCP UI/login flow
and verify capability plus whole-page wiki reads; supply those observations to
`reconcile.py`. Test a fresh session separately on each used CLI/desktop surface.
Cloud Code and ordinary chat use their own supported stores/manual path and never
inherit local capture credentials/hooks. Browser/account preference automation
and a system-wiki startup loader are not implemented by these file adapters.

Sources checked 22 October 2026: installed Codex CLI 0.162.1 and Claude Code
2.1.287 command help, read-only native configuration inspection, and official
[Codex MCP](https://learn.chatgpt.com/docs/extend/mcp?surface=cli) and
[Claude Code MCP](https://code.claude.com/docs/en/mcp) documentation.
