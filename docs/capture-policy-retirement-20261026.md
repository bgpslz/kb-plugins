# Capture-policy metadata retirement

Source 1.4.2 removes the obsolete registry `capture_policy` field from saved
setup inventories and fallback instructions. Human review chooses destinations;
external collection is independent of registry destination metadata. This is a
compatible plugin patch from 1.4.1, including when consuming registry protocol 2
records without the field. KB protocol compatibility remains 1.

The canonical setup renderer no longer copies the field. Both source packages
were regenerated. The collector has no registry-field reader; its unrelated test
variable was renamed to describe machine collection policy. Collector version
1.1.0 and behaviour are unchanged. Open WebUI filters live in owui-deploy and
have no reader of this field. The old personal-rag model-driven router is removed
in the matching backend release.

In-chat opt-out remains planned, not implemented: deterministic commands/buttons,
central conversation exclusion that removes earlier captures and refuses retries,
Open WebUI chat state, whole-session scans for local Codex/Claude history,
optional hooks subject to verification, and clear client-history limitations.
The full backlog is maintained in personal-rag's system roadmap. Current model
prohibitions remain until the feature and system-wiki changes are released.

Validation: source package parity passes; Python 3.12 setup/bootstrap/native tests
pass 88 cases and local collector tests pass 8. Source publication and installed
plugin/standing-instruction updates are separate; no installed cache was edited.

Source implementation commit **21fef40** is published on the existing GitHub main.
The backend release is live: normal authenticated discovery reports registry
protocol 2, no removed field on either record, and no capture label on My PKB's
discovery capabilities. Both system-guide changes and central migration are
verified. Bruno PKB documentation changes 97/98 are applied, including the deferred
opt-out. Installed plugin metadata, saved instructions and fresh-client acceptance
remain separate from source publication; collector runtime was not changed.

## Final registry cleanup approved before use

Bruno approved completing MCP Service 2.0.0/registry protocol 2 without another
version increment: he has not started using it and there are no other users.
Plugin 1.4.3 validates the registry response version, preserves working connections
when discovery is incompatible, normalizes canonical type/description names from
legacy evidence, and uses explicit MCP/account URLs. Backend removal of the unused
retrieval profile and the per-KB capture tool is separate from this source package.
The deferred deterministic chat opt-out remains unimplemented.
