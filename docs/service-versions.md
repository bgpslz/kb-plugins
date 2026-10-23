# Plugin and collector versions

23 October 2026. Source package 1.4.0 and local collector 1.1.0 are unreleased.
Existing installed versions are independent; no cache or client installation was
changed by this implementation.

Before a significant commit, Codex and Claude Code must propose the affected
patch/minor bumps and rationale; see AGENTS.md and CLAUDE.md. Application,
protocol and immutable build identifiers have different roles.

The collector reports JSON with service/version/build_id through:

```sh
python3 local-capture/capture.py --version
```

Use the installed collector's actual path to inspect that copy. This command
exits without reading Keychain, opening receipts, installing hooks or contacting
MCP Service. Its build_id fingerprints the collector's source bytes once at
process import. Its MCP client handshake uses the same maintained VERSION.
The collector is standalone so it does not infer Git identity from whichever
checkout or cache happens to contain it.

The source distribution inventory is setup/package.json; manifests and generated
copies must agree. After canonical changes, run sync-packages.py --write, the
package checks and local-capture regressions. Publishing GitHub commits, refreshing
a marketplace, updating installed clients and proving live behaviour remain
separate operations.

Personal-rag's docs/service_versions.md documents backend /health, /version,
MCP initialize/authenticated GET /mcp and worker CLI/startup reports. Open WebUI
filter diagnostics are documented in owui-deploy/docs/service_versions.md.
Third-party binaries keep upstream versions; do not relabel them as plugin releases.

The PKB memory update failed with the existing repository-ownership error; its
complete content and unknown-publication boundary are retained in
[pending memory update](pending-pkb-service-versioning.md). Repository rules are
saved; shared-memory publication is unconfirmed.
