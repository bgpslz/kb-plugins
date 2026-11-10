# KB plugins

Versioned marketplace packages for the generic multi-knowledge-base workflow.

New users: start with [Install KBs](INSTALL.md). Once installed, ask the plugin
to set up your knowledge bases; it supplies the connection and sign-in guide.

- `chatgpt/kbs` serves ChatGPT and Codex. It contains OpenAI
  invocation metadata and expects ChatGPT bearer-token connections or Codex
  OAuth connections to be configured per service. Local Codex Desktop/CLI setup
  configures native MCP OAuth, verifies reads and refresh, and saves each machine's
  actual connection mappings. Cloud ChatGPT uses service-local bearer-token apps.
  Installing the skills does not establish these connections; see the complete
  [setup guide](setup/openai-client-setup.md) and its linked technical reference.
- `claude/kbs` serves Claude Chat, Desktop, mobile, and Claude Code.
  It preserves OAuth connections and uses Claude's explicit-invocation
  metadata for setup and build workflows.

Both packages contain the same core skills: `use-kbs`,
`use-standard-kb`, `setup-kbs`, `build-kb`, and `maintain-project-docs`. KB-specific build guidance and
all retrieval, ingestion, and wiki tools remain in the individual KB services
rather than this repository.

MCP Service owns the registry and Capture Protocol v1. `setup-kbs` reconciles
services and handles capture separately for supported local Code sessions;
chat and cloud Code setup includes retrieval/guidance without assumed capture.
`use-kbs` loads the current system operating instructions; `use-standard-kb` is
an optional retrieval helper for selected KBs, not a second startup step. Open WebUI is the
primary surface for capturable ordinary chat and needs no KB plugin.
Open WebUI server capture, local session capture and manual paste feed the same
Capture Store and human review queue. See [local capture](local-capture/README.md).
Source updates do not reconcile installed plugins or personal standing instructions.

The development-only `maintain-project-docs` skill preserves full repository documentation, distils material updates into the configured owner PKB, and follows authorised organisation documentation workflows. Shared system-use guidance belongs in the system wiki. Owner/path approval requires the matching service implementation; source changes do not deploy that backend or update installed packages.

## Development workflow

Confirmed by Bruno on 2026-10-16: work directly on `main` normally in
`kb-plugins`, `personal-rag` and the `llm-wiki` application/template repository.
Branches are exceptional when changes need isolation; explain the reason to
Bruno. Wiki content repositories managed by llm-wiki may retain review branches
for both PKBs and OKBs through the same mechanism, including multi-editor use.
Approval authorisation differs by KB. Identify the repository and affected KB
explicitly, and distinguish review commits from publication on canonical main.

Record material decisions when agreed, including workflow decisions without
code changes, with rationale, scope and implementation/publication status.
Maintain repository documentation and distilled personal project documentation
through the configured wiki proposal service; report pending or failed updates
explicitly. Source drafts and unreleased skills do not imply live publication.

## Architecture alignment

Bruno approved the [architecture handover](docs/architecture-alignment-handover.md)
and [bootstrap contract](docs/system-wiki-bootstrap-contract.md). The current
[implementation and acceptance status](docs/setup-implementation.md) supersedes
the earlier audit's implementation observations.

Source **1.4.0 is published** (main 3fa8198); local Codex and Claude marketplace installations report 1.4.0. Both installed distributions include setup adapters, the
index-plus-surface startup core, the small use-kbs instruction bootstrap, a short
shared fallback, and explicit build/development workflows. Other machines and
cloud installations remain unverified.

Source **1.4.1 is published on GitHub** (implementation commit `5bdd702`). The setup skill now explains the
connection/instruction workflow and reports inventory, retrieval, instruction
persistence, guidance delivery and capture separately. `use-standard-kb` remains
as an optional retrieval helper; it is not required after every guide load or by
the fallback. Plugin presentation now distinguishes these jobs. This source
revision does not update installed plugins, personal instructions or services.
Both configured local marketplaces point to this checkout and read the 1.4.1
package. Claude's marketplace update succeeded; Codex's Git-only upgrade does
not apply to this local source. Installed plugin metadata still reports 1.4.0;
client updates and fresh-session acceptance remain separate. See
[the clarification and publication record](docs/setup-clarity-20261026.md).

Personal-rag has implemented and deployed the system-wiki contract as c9ad645.
Authenticated native resource listing and complete index/local-Codex reads passed
in this existing chat. The [contract handover](docs/personal-rag-system-wiki-contract-followup.md)
is resolved. A fresh local Codex CLI context has now loaded the installed bootstrap and complete
authenticated system-wiki index/surface pages. Native startup bridges and other
surfaces remain independent acceptance work; fallback guidance is retained.

Open WebUI's separate [filter handover](docs/owui-system-wiki-handover.md) covers
system instructions for answerer/planner/worker, avoiding persisted/captured
injections and a second retrieval loop. That work is not completed by this plugin.

See [service and collector versioning](docs/service-versions.md) for the new
version-bump rule, diagnostics and release boundaries.

## Source development

Canonical setup helpers, bootstrap, retrieval helper, fallback and release inventory live in `setup/`.
Run `python3 scripts/sync-packages.py --write` to regenerate packaged copies;
omit `--write` to check. `scripts/check-packages.py` checks both source versions,
inventory and generated resource parity. These commands do not publish/install.

[Setup evidence](setup/GUIDE.md), [native adapters](setup/native-setup.md) and the
[system-wiki client](setup/system-wiki-client.md) document their boundaries.
Use `python3 setup/reconcile.py evidence.json` for a read-only readiness report
and managed-instruction draft. Native persistence is separately authorised and
does not establish OAuth or fresh-session acceptance.

```sh
python3.12 -m unittest discover -s setup -p 'test_*.py'
python3.12 local-capture/test_capture.py
python3 scripts/sync-packages.py
python3 scripts/check-packages.py
```

Capture installation/readiness stays separate. Local capture supports macOS;
cloud/ordinary chat setup must not install a laptop collector. See
[local capture](local-capture/README.md).

Source **1.4.2** removes obsolete capture-policy metadata from setup inventories
and fallback wording. Humans choose destinations in Capture Review. Collection
and installed-client state are unchanged; see [the retirement record](docs/capture-policy-retirement-20261026.md).

Source **1.4.3** consumes finalized registry protocol 2. Discovery evidence must
include that protocol before changing inventory. Canonical metadata names are
`type_id` and `description`; old evidence aliases normalize deterministically.
Connections use explicit `mcp_url`; nullable `account_url` is a separate account
page. This changes source packages, not installed caches or credentials.

Source **1.4.4 is published on GitHub** (implementation `dabeab9`). Setup now names the existing local OAuth app and
cloud token route, supports natural-language setup and plugin onboarding, and
requires a client app-connection check before a new Codex native entry. The
shared package no longer requires the token PKB app on every surface. See the
[packaging decision, live-guidance handover and acceptance matrix](docs/pkb-connection-routing-20261110.md).

Source **1.4.5 is published on GitHub** (implementation `9989668`), correcting that registered-app preference
after native Codex recovery and a registered-app CIMD failure on 10 November.
The complete manual/assistant-guided recipe covers native configuration, scopes,
browser consent, exact-route reads, refresh and local mappings. Registered-app
presence no longer forbids selecting native setup. See the
[recovery evidence and release boundaries](docs/codex-native-setup-20261110.md).
Client installation, personal instructions, broker settings and backend guidance have separate acceptance boundaries.
