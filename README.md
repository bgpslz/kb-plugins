# KB plugins

Versioned marketplace packages for the generic multi-knowledge-base workflow.

- `chatgpt/kbs` serves ChatGPT and Codex. It contains OpenAI
  invocation metadata and expects ChatGPT bearer-token connections or Codex
  OAuth connections to be configured per service.
- `claude/kbs` serves Claude Chat, Desktop, mobile, and Claude Code.
  It preserves OAuth connections and uses Claude's explicit-invocation
  metadata for setup and build workflows.

Both packages contain the same four logical skills: `use-kbs`,
`use-standard-kb`, `setup-kbs`, and `build-kb`. KB-specific build guidance and
all retrieval, ingestion, and wiki tools remain in the individual KB services
rather than this repository.

MCP Service owns the registry and Capture Protocol v1. `setup-kbs` reconciles
services and installs local capture; `use-kbs` only routes relevant retrieval.
Open WebUI server capture, local session capture and manual paste feed the same
Capture Store and human review queue. See [local capture](local-capture/README.md).
Source updates do not reconcile installed plugins or personal standing instructions.
