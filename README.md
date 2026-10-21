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
services and installs local capture; `use-kbs` only routes relevant retrieval.
Open WebUI server capture, local session capture and manual paste feed the same
Capture Store and human review queue. See [local capture](local-capture/README.md).
Source updates do not reconcile installed plugins or personal standing instructions.

The development-only `maintain-project-docs` skill preserves full repository documentation, distils material updates into the configured owner PKB, and proposes user guidance for organisation review. Owner/path approval requires the matching service implementation; source changes do not deploy that backend or update installed packages.

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

## Architecture alignment handover

See [the 22 October handover](docs/architecture-alignment-handover.md) for the
proposed plugin/skill restructuring, current architecture, per-surface scope,
system-wiki dependency and acceptance criteria. Codex/Claude Code setup includes
retrieval and external local capture; ChatGPT/Claude-chat setup is retrieval only.
The handover does not indicate that restructuring has been implemented.
