# Plugin and collector versions

23 October 2026. Source package 1.4.0 was published at 3fa8198. Supported marketplace commands
installed Codex 1.4.0 and updated Claude 1.3.3 to 1.4.0 (restart to load).
The installed local collector now reports 1.1.0; credentials, receipts, exclusions
and hook configuration were preserved. Other machines/cloud clients are unverified.

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


## Deployment and acceptance follow-up — 23 October 2026

Backend release c77cbe4 now reports MCP Service 1.3.0 and PKB Service 1.1.0
through normal authenticated check_connection/get_kb_capabilities tools, including
application/build/Git metadata. All twelve backend application health checks pass.
The two legacy Bruno PKB MCP units now run as rag:rag through scoped systemd
overrides; bruno performed administration, rag application/Git operations. No
sudo grant, credential replacement or blanket Git trust exception was introduced.

A fresh ephemeral Codex CLI model context using installed plugin 1.4.0 read the
bootstrap, fetched the complete system-wiki descriptor/index/local-Codex page
through existing OAuth and applied its guidance. This is new CLI instruction-based
loading evidence, not native hook/cache or desktop/cloud acceptance. Working
fallbacks remain. The installed collector executable reports build
sha256:e4d946ba58ae45435f3d231ae929ee69490d7dd48dacb801d00fb51cd6b222df;
no new capture delivery was invoked as an acceptance test.

The earlier preference ownership error is resolved. Canonical OAuth proposals
62 (preference) and 63 (project decisions) returned status=applied for Bruno’s PKB
wiki. The retained draft statuses are historical and superseded by those receipts.
Bruno subsequently ran the established admin-authenticated installer for both
Open WebUI filters. Runtime logs and exact source hashes verify capture 0.4.0 and
retrieval 0.3.0; active/global flags and stored valves match the pre-update backup.
The earlier failed JSON import is superseded by this completed installation. Source validation and
these live checks remain separate evidence.


## Setup clarity patch — 26 October 2026

Source KBs package 1.4.0 → 1.4.1 is a compatible instruction/presentation patch,
prepared but not published or installed. Setup and bootstrap skill metadata
1.3.5 → 1.3.6 and the retrieval helper 1.0.0 → 1.0.1 describe their changed text.
The helper remains available under its existing name; invocation policies are
preserved. Runtime helper APIs, the 1.1.0 collector, authentication and backend
protocols are unchanged. Both package manifests and generated resources use the
canonical setup inventory. See [the decision and validation](setup-clarity-20261026.md).
