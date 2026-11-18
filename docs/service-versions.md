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
published to GitHub with local marketplace sources verified; installed metadata
still reports 1.4.0. Setup and bootstrap skill metadata
1.3.5 → 1.3.6 and the retrieval helper 1.0.0 → 1.0.1 describe their changed text.
The helper remains available under its existing name; invocation policies are
preserved. Runtime helper APIs, the 1.1.0 collector, authentication and backend
protocols are unchanged. Both package manifests and generated resources use the
canonical setup inventory. See [the decision and validation](setup-clarity-20261026.md).

## Registry metadata retirement — 26 October 2026

Plugin source 1.4.1 → 1.4.2 removes the obsolete capture-policy inventory field.
This compatible plugin patch accepts records without that metadata; the backend
separately advances its breaking registry discovery contract to protocol 2 and
MCP Service 2.0.0. KB/Capture/system-wiki protocol versions stay 1. Collector
runtime 1.1.0 is unchanged. Source publication does not upgrade installed clients.

## PKB route correction — 10 November 2026

Published source KBs **1.4.3 → 1.4.4** is a compatible setup repair;
setup/bootstrap text **1.3.6 → 1.3.7**. Both package manifests and generated
copies agree. Natural-language setup/onboarding selects the named local OAuth
or cloud token app without requiring both, and new Codex native entries require
a separate app-inventory check. Collector/backend versions are unchanged.
Implementation `dabeab9` is published on GitHub; see [validation and pending live acceptance](pkb-connection-routing-20261110.md).

## Documentation destination correction — 16 November 2026

Source KBs **1.4.7 → 1.4.8** and `maintain-project-docs`
**1.3.5 → 1.3.6** are compatible instruction fixes. The source inventory and both
package manifests carry the patch. Collector and
backend versions are unchanged.

Bruno's revised policy places shared KB-system explanations, architecture,
plans, decisions and development histories in personal-rag's system wiki.
Current explanations and histories are separate linked files, with plain English
before technical detail. My PKB retains personal purposes, priorities,
preferences and original source evidence; organisation-specific knowledge follows
the relevant organisation KB's review rules. Other projects retain their own
authorised documentation destinations.

The controlling policy is in personal-rag's `AGENTS.md` and
`docs/system_wiki.md`; `docs/wiki-reorganisation-20261115/REVIEW.md` records the
coordinated migration. System-wiki edits use application source review and
release, with no implemented proposal interface. Replacement system pages must
be published and verified before the coordinated PKB reductions are merged.
This skill correction does not perform that migration or create another PKB
system-history proposal.

The canonical skill is now `setup/project-docs.md`; `sync-packages.py` generates
both distributions and package checks verify their parity with that source.
Repository/package changes do not establish GitHub publication, marketplace
refresh, installed-cache updates or system-wiki deployment. None is authorised
by the version proposal.

Validation: 95 setup tests and 8 collector regressions passed; generation/parity
checks, both packaged skill validators and `git diff --check` passed. Skill
validation used personal-rag's existing Python environment for PyYAML; no
dependency was installed. These are local source checks, not publication or
runtime acceptance.

Bruno authorised publication with “Deploy”. Implementation `f763afb` was pushed
to `bgpslz/kb-plugins/main` and the remote ref was verified on 16 November.
The release inventory now marks the source published. Both source distributions
are available on GitHub; this receipt and generated inventory copies follow in
a metadata/documentation commit.

The existing Summerleaze workspace marketplace's **Sync now** completed with
**Needs attention**, zero updated and one failed. Its error asks to check the
repository, branch and GitHub connection access. The configured repository is
`https://github.com/bgpslz/kb-plugins`, path repository root, ref `main`, matching
the verified source. Last synced revision remains `c9b77b2`; the plugin detail
page observed before the attempt reported 1.4.5. No GitHub permission or
marketplace configuration was changed. Workspace publication remains blocked
pending diagnosis/repair of that sync error; its cause is not established.

Installed caches were not modified and active 1.4.8 loading is unverified.
No system-wiki deployment or PKB migration/proposal was performed.

## Claude Code collector fix and system-wiki proposal routing — 18 November 2026

Collector **1.1.0 → 1.1.1** and source KBs **1.4.8 → 1.4.9** are
compatible fixes. KBs 1.4.9 also carries `maintain-project-docs`
**1.3.6 → 1.4.0**, described below. The source inventory, both package manifests and the bundled
`setup-kbs` collector copies carry them.

A check of the installed collector found that Claude Code turns could include
text the user did not type. App notices (`<system-reminder>` blocks) inside a
user message and compaction summaries were captured as prompts. Task
notifications and similar app events started turns of their own. The collector
now strips those notices, skips compaction summaries and rows whose
`origin.kind` is not `human`, and closes a finished turn at such a row so
unprompted replies are not appended to it. A screenshot sent without text,
previously merged into the preceding turn, is now its own turn with the prompt
`[Image not captured]`. Codex parsing is unchanged.

Validation: 9 collector regressions, including a new fixture for these cases,
the package generation and parity checks, and an offline comparison over the
573 Claude Code turns on the maintainer's Mac since installation. No injected
text remained in any prompt. Upgrading changes the content hash of 71 of those
turns, so the first sweep after installation would queue them again for
Capture Review. The installed collector, still 1.1.0, was not changed.
Publication, marketplace refresh and installation remain separate operations.

`maintain-project-docs` 1.4.0 adds a compatible workflow: shared KB-system
explanations, plans, decisions, history and outcomes are now submitted to the
system wiki through MCP Service's maintainer-reviewed proposal tools
(`get_system_documentation_status`, `read_system_documentation_page`,
`propose_system_documentation_write`), replacing the instruction that no
proposal interface existed. Personal KB wikis receive only the owner's personal
purposes, priorities, preferences and source evidence, and zero personal-KB
proposals is a valid outcome. When material is transposed it keeps its full
detail, and material no longer current moves to linked history pages. Release
version numbers are not hardcoded in explanations. Submitting a proposal does
not approve, export, release or publish it. Both package READMEs and the root
README describe the new routing.

Bruno authorised publication and collector installation on 18 November.
Implementation `54b34bd` was pushed to `bgpslz/kb-plugins/main` and the remote
ref verified. The release inventory now marks the source published.

- **Claude Code on the maintainer's Mac:** after a marketplace update, plugin
  `kbs@kb-plugins` updated from 1.4.6 to 1.4.9 at `54b34bd`. It loads on restart.
- **Codex:** the workspace-directory copy on that Mac reports 1.4.8. No workspace
  marketplace sync was attempted for 1.4.9. Claude Desktop and claude.ai
  distribution were not checked.
- **Collector:** `install.py` refused to run because Codex had rewritten
  `~/.codex/config.toml` when trusting the hooks. The rewrite kept the managed
  block's hooks and trust entries but dropped its `# END kbs-local-capture`
  marker. Nothing was written. Because the 1.1.1 hook commands, launchd job and
  configuration are identical to 1.1.0, the runtime `capture.py` was copied into
  `~/.local/share/kbs-capture/` instead; `--version` reports 1.1.1. Credentials,
  receipts, exclusions, the capture start time, hooks and Codex trust are
  unchanged. Reinstalling on any machine where Codex has trusted the hooks will
  fail the same way until the installer tolerates that rewrite.
- **Acceptance:** a launchd backstop sweep exited 0 and queued 55 corrected turns,
  with no new failures. Afterwards, all 724 turns eligible since installation had
  receipts. The corrected turns appear again in Capture Review.
