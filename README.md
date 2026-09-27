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
all retrieval, ingestion, wiki, and capture tools remain in the individual KB
services rather than this repository.

The MCP Service is consulted only by `setup-kbs` for registry reconciliation.
It is not a normal conversation dependency.
