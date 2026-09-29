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

MCP Service owns the registry and Capture Protocol v1. `setup-kbs` uses it for
registry reconciliation and capture compatibility checks. During normal
conversations, retrieval still goes directly to materially relevant KB
Services; after an eligible reply is composed, `use-kbs` makes one fail-soft,
pre-destination `capture_chat_turn` append to MCP Service for later human
routing in the Capture Review Application. It never fans capture out to KB
Services or queries MCP Service inventory at runtime.
