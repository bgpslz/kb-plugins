# Setup evidence helper

Use `scripts/reconcile.py` beside the installed setup skill, or the standalone
`setup/reconcile.py` in a source checkout. Python 3.9+ and the standard library
are sufficient. No network, configuration writes, login or capture installation
occurs. Output is a report and a managed instruction draft based **only on supplied
observations**, not an independent live audit.

Native connection discovery and explicit additive persistence are provided by the
separate [native adapter guide](native-setup.md) in the packaged skill, or
`setup/native-setup.md` in source. The evidence evaluator itself remains read-only.

```sh
python3 <setup-directory>/reconcile.py evidence.json
python3 <setup-directory>/reconcile.py evidence.json --instructions existing-instructions.md
```

In the installed skill the script is under `scripts/`; in source it is under
`setup/`. `--instructions` reads existing text and returns `proposed_instructions`
in JSON without writing it. Inspect the draft before applying through the client's
supported setting or instruction file. Preserve unrelated instructions. Personal
`~/.claude/CLAUDE.md` changes require Bruno's approval. Unknown/duplicate/malformed
managed delimiters are refused. Repeating reconciliation is idempotent.

## Evidence format

Collect fresh capability and whole-page wiki-read results using the configured
native authentication. Do not include tokens, headers, client secrets, browser
codes or complete configuration files. The following uses synthetic identities:

```json
{
  "target": {"surface": "codex-desktop", "execution": "cloud", "os": "linux"},
  "registry": {"status": "failed"},
  "connections": [{
    "kb_uid": "example-kb-uid",
    "service_id": "example-service",
    "connection_id": "example_connection",
    "name": "Example KB",
    "type_id": "personal",
    "description": "Example project context",
    "kb_protocol_version": 1,
    "capabilities": ["wiki", "rag"],
    "access": "verified",
    "wiki_read": "verified"
  }]
}
```

`surface`: `codex-cli`, `codex-desktop`, `claude-code-cli`,
`claude-code-desktop` (Code tab), `chatgpt`, `claude-chat`, or `open-webui`.
`execution`: `local`, `cloud`, or `unknown`, describing where code runs, not where
its UI runs. `os`: `macos`, `windows`, `linux`, `wsl`, or `unknown`.

Every connection and registry KB needs `kb_uid`, `service_id`, `name`, `type_id`,
`description`, integer `kb_protocol_version` and a string-list `capabilities`. Resolve
legacy missing identities against actual service/registry evidence; do not
manufacture KB UIDs from names or a private-PKB example. A connection additionally
needs its actual `connection_id`. A native OAuth client ID is a different identity.

Record the verified registry connection separately from KB records, using the
optional top-level field below. MCP Service has no KB UID and must not be added
as a fictitious KB. `access=verified` requires an authenticated service check;
the system-wiki descriptor alone does not identify the client connection used.

```json
{
  "mcp_service": {
    "service_id": "mcp-service",
    "connection_id": "this_machines_registry_connection",
    "access": "verified"
  }
}
```

The helper emits this local binding only when its access is verified, and rejects
another service identity. Supply it, along with all existing KB mappings, when
regenerating local instructions. Omission means no binding was supplied; the
helper cannot recover an omitted mapping from arbitrary old instruction text.
Shared skills do not assume these connection names exist on another machine.
Retain separate read/refresh/fresh-connection evidence: the helper's retrieval
result does not itself test refresh or prove instruction delivery.

A verified complete registry observation must carry `registry_protocol_version: 2`
from the list/get response. Missing, old, malformed or future protocols cannot
make inventory authoritative. Existing verified connections are preserved.
Legacy supplied evidence `type`/`domain` normalizes to `type_id`/`description`;
conflicting aliases are rejected and generated blocks use canonical names.
Use explicit registry `mcp_url` for service setup; `account_url` is optional and
separate. Never infer an MCP path from an account URL.

Registry `status` and connection `access`/`wiki_read` values are `verified`,
`denied`, `failed` or `unknown`. `access=verified` means an authenticated capability
response with checked service identity, not a successful browser login. `wiki_read`
requires a substantive authenticated whole-page read. Omitted connection evidence
is unknown. Set `build_guide_available=true` only after verifying the advertised
build tool. Missing build support evidence is reported separately from retrieval.

Only `registry.status=verified`, `complete=true` and a complete
`knowledge_bases` array authorize removing absent KBs from the generated inventory.
Outage, denied/unknown access to the registry or an incomplete response preserves
existing inventory. Direct KB denials and incompatible retrieval contracts exclude
that connection from active guidance. The helper never removes connectors or
revokes server-side credentials. Missing connection evidence is not removal
authority: an explicit `connections` array is required. Supply all already-configured
connections when drafting inventory; an empty array means you have observed none,
not that discovery failed. The helper cannot recover an omitted connection from
arbitrary legacy instruction text.

Capture collection is external; the inventory contains no destination capture policy.
Capture settings never influence retrieval routing/readiness. The helper ignores any requested capture
verification for chat, cloud or unknown execution. For a local macOS Code target,
`capture_verified=true` may be supplied only after independently verifying the
current surface/machine's receipt and real hook delivery. A missing receipt does
not block retrieval. Unsupported local OS capture is reported separately.

Optional connection `oauth` compares values already observed from the native
client, exact callback generation, provider resource metadata and broker grants:

```json
{
  "expected_callback": "https://client.example/oauth/callback/actual_connection_id",
  "allowed_callbacks": ["https://client.example/oauth/callback/actual_connection_id"],
  "required_scopes": ["example:read"],
  "granted_scopes": ["example:read"],
  "expected_resource": "https://service.example/mcp",
  "observed_resource": "https://service.example/mcp",
  "broker_grant": "allowed"
}
```

These callback/resource examples are synthetic, not a provider recipe. Callback
comparison is exact; old allowed callbacks must be preserved. Resource audience
and KB endpoint are not assumed interchangeable. Missing values report unassessed
checks. Broker values are `allowed`, `denied`, `unknown`. The helper reports no
secrets, URLs or scopes from this object. It does not request grants or change
approvals. A successful KB read and an OAuth-configuration diagnosis are separate
evidence: stale provider observations must not override live authorisation.

Optional `source_version` and `installations` support installation diagnostics.
Each installation supplies `active` (boolean), `version` and a `skills` name list.
Only entries proven active count as duplicates; historical caches are not active
installations. Actual path/marketplace discovery and supported package-manager
updates remain client-specific manual steps, not automated by this helper.

Optional `system_wiki` accepts the authenticated descriptor from the approved
system-wiki contract. A compatible complete descriptor enables a static load
instruction; otherwise the packaged fallback remains. Neither result proves
startup injection. The separate system-wiki client core implements startup/cache logic but still
needs host integration. The system-wiki reader/metadata contract has been deployed
in personal-rag; verify the target connection live rather than assuming every
installation has it. See the system-wiki client guide.

## Outputs and limitations

The report separates registry authority, retrieval, guidance mode, untested
startup loading, capture, installation issues, missing KB connections and duplicate
KB connections. `connector_removals` is always empty. `managed_block` is null for
Open WebUI, whose filter owns retrieval and server-side capture.

Inspect per-connection issues even when another connection to the same KB passes.
`retrieval=verified` means all required KBs have supplied verified capability/wiki
evidence; `no_entitled_kbs` means a complete inventory confirms none. This does not
prove native settings persisted or that a fresh session loaded the guidance.

For clients without Python/local files, perform the same checks manually and
prepare the surface-specific block using the skill. Do not install a local runtime
in cloud/chat merely to run this helper. Unknown protocol/capability fields must
not be silently reported as successful. Validate persistence, instruction loading
and local capture on their own surfaces after any separately authorised install.
