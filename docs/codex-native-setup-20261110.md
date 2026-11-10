# Native Codex setup correction — 10 November 2026

KBs 1.4.5 is a published compatible patch over 1.4.4 (implementation `9989668`). The source now
contains the complete local Codex native OAuth configuration procedure rather
than recommending a registered OAuth app and assuming connections already exist.
The implementation was committed and pushed on 10 November. The existing workspace
marketplace was synced through OpenAI Console: revision `9989668d31c7a1ffaf82ba44dbacf9389ff48ecb`,
Completed, one Updated, zero Failed. The refreshed KBs detail page reports 1.4.5.
The current Mac mini chat still has its 1.4.4 cache; a fresh client chat must verify
loading 1.4.5. Personal instructions, OAuth credentials and backend were not changed.

## Findings and verified boundaries

The Mac mini had enabled native `casdoor_pkb_service`, `casdoor_mcp_service` and
`casdoor_slzkb` entries, with three disabled older names targeting the same
respective endpoints. Registered app views did not establish which route worked.
Original session history confirms successful native PKB reads through
`mcp__casdoor_pkb_service__read_wiki_page`, including at 12:19 UTC. Local logs
record rejected native PKB refresh credentials at 13:52, before the diagnostic
chat began. Explicit registered `codex_apps` PKB capability attempts at 16:04 and
16:06 returned authentication-request messages, not capabilities or content.
The precise cause of invalidating the native grants remains unproven.

The registered PKB OAuth app's saved `supported_auth` retained the Auth0 issuer
and endpoints and the origin-only PKB resource. These were observed in Chrome's
read-only app-detail network response, not inferred from live discovery.
Its downloadable wrapper only referenced the app ID; it contained no OAuth
configuration. A fresh registered app discovered Casdoor and the correct `/mcp`
resource, but Casdoor rejected ChatGPT's CIMD `private_key_jwt` declaration.
Native Codex uses a different CIMD document, with `/oauth/codex/client.json`.
This registered-route incompatibility is distinct from the established ChatGPT
bearer-token workaround and does not prove native Codex OAuth is incompatible.

Native PKB reauthorization succeeded at 17:18. A native read at 17:26:20 passed
after the six-minute access-token lifetime; broker metadata confirmed a new
access token and rotated refresh credential. A fresh process using desktop
runtime 0.167.0-alpha.3.2 also read successfully. No tokens were copied between
machines or exported for this test. Native MCP Service and SLZKB were subsequently
authorized and passed service/capability and substantive wiki reads. MCP Service
returned Registry Protocol 2 and both entitled KBs. SLZKB reported bootstrap
lifecycle. Subsequent native MCP Service and SLZKB reads at 18:06 UTC passed
beyond access-token expiry without another sign-in; their refresh-token rotation
was not separately fingerprinted.
The MacBook native configuration/refresh flow remains independently unverified.

No disabled native entries or registered apps were deleted. The failed registered
test app is not the working native PKB connection. Broker settings and token
lifetimes were not changed.

## Released guidance changes

- `setup/openai-client-setup.md` gives the non-technical user the actual Codex
  Settings path, every required connection field, blank fields, Save/Authenticate
  actions, sign-in and final checks. Material discovery/scope/compatibility issues
  follow below the procedure. It does not replace configuration steps with a
  generic instruction to ask the assistant. Its linked
  `setup/connection-reference.md` gives the assistant/technician effective
  configuration, deployment TOML/scopes, sequential native CIMD logins, browser
  expectations, exact-route reads, expiry and persistence checks, local mappings,
  troubleshooting and separate ChatGPT token setup. The assistant carries out
  configuration work where tools permit; when user input is needed the guide
  supplies each required GUI step. Users are not instructed to use Terminal or edit files.
- Shared skills distinguish setup from ordinary retrieval. They use saved local
  mappings and do not assume example names or the old registered app ID.
- `--codex-apps-checked` remains an operator assertion but now records inspection
  and deliberate native-route selection. Mere app presence no longer implies
  that adding the intended native connection is forbidden. No login or grant
  verification was added to the adapter.
- The evidence helper can persist an explicitly verified MCP Service connection
  ID separately from KB mappings. It does not invent a registry KB UID or claim
  that static metadata verifies authentication/refresh.
- The existing registered MCP Service dependency and ChatGPT token route remain.
  Source generation does not remove stale registered apps or installed copies.
- Published-facing setup/installation prose uses generic personal/organisation
  KB names. Users obtain real addresses from setup; technical examples use reserved
  `example.org` domains. Private deployment names and live addresses remain only
  in the development/operations history, not the distributed setup instructions.

Released versions: shared OpenAI/Claude KBs packages **1.4.4 → 1.4.5**;
setup/bootstrap skills **1.3.7 → 1.3.8**. Other skills and collector remain unchanged.
This is a compatible correction to setup guidance and generated local bindings;
it changes no service protocol, server authorization or capture behavior.

## Separate rollout work

The workspace catalog is updated; verify each client through its supported
plugin manager and a fresh chat. Do not edit installed caches. Reconcile local instructions only
through an authorized setup operation and verify a fresh session. The shared
system wiki is owned by personal-rag and needs its own reviewed update/release;
this repository does not deploy it. The existing routing handover is historical
evidence, not the current registered-app recommendation. Owner PKB project
documentation must distinguish GitHub/catalog publication from client loading and
backend deployment. No organisation-wiki publication is requested here.

## Release validation

All 95 setup tests passed, including separate local names for two machines and
refusal to emit an unverified/misidentified registry binding. Canonical generation,
package checks and whitespace checks passed. These source checks do not install
1.4.5 or prove MacBook acceptance. The native adapter still saves URL entries
only; the guide explicitly completes scopes/login outside that adapter.

The owner PKB component page has release proposal **116**, origin
`e6e81e04231842a6be58dc51db0351b8`, **pending human review**. It supersedes
prepublication proposal 115; the reviewer should use 116 rather than the draft.
No wiki publication or organisation-wiki update is claimed.
