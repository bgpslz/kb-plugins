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
