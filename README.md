# KB plugins

Versioned marketplace packages for the generic multi-knowledge-base workflow.

- `chatgpt/kbs` serves ChatGPT and Codex. It contains OpenAI
  invocation metadata and expects ChatGPT bearer-token connections or Codex
  OAuth connections to be configured per service.
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
`use-kbs` is the transition system-instruction bootstrap. Open WebUI is the
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

Source **1.3.5 is unreleased**. Both distributions include setup adapters, the
index-plus-surface startup core, the small use-kbs instruction bootstrap, a short
shared fallback, and explicit build/development workflows. use-standard-kb remains
packaged until replacement acceptance. Installed clients are unchanged.

Personal-rag has implemented and deployed the system-wiki contract as c9ad645.
Authenticated native resource listing and complete index/local-Codex reads passed
in this existing chat. The [contract handover](docs/personal-rag-system-wiki-contract-followup.md)
is resolved. A native startup bridge and fresh-session instruction-based loading
still need independent proof before installed guidance is retired.

Open WebUI's separate [filter handover](docs/owui-system-wiki-handover.md) covers
system instructions for answerer/planner/worker, avoiding persisted/captured
injections and a second retrieval loop. That work is not completed by this plugin.

## Source development

Canonical setup helpers, bootstrap, fallback and release inventory live in `setup/`.
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
