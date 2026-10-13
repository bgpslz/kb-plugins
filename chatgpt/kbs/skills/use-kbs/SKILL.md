---
name: use-kbs
description: Always invoke for every conversation. Route materially relevant requests to configured KB Services and preserve connection state.
metadata:
  version: "1.3.2"
---

# Use KBs

Chat capture is handled by external clients. Do not generate capture references or
tags, call chat capture tools for routine replies, evaluate capture policies, or
implement in-chat exclude/include commands. `capture_policy` is review metadata.

Invoke for every conversation; retrieve only when a configured KB is materially relevant.
Use the KB inventory in the current standing instructions. `setup-kbs` owns discovery
and reconciliation; do not query MCP Service for inventory during ordinary conversation.

For each relevant standard KB, follow `use-standard-kb` with its service and metadata.
Maintain connection state per service. The first successful substantive call establishes
connection; otherwise use `check_connection`. After success, do not preflight again.
Verify KB Protocol version 1 and the capability required for the operation. A registry
outage does not disable an already-configured KB; runtime authorization belongs to the
KB Service.

Use the authentication path configured for the current surface. In ChatGPT use the
plugin's bearer-token apps; in Codex use separately configured OAuth MCP servers
(`pkb_service` for My PKB); in Claude use remote OAuth connectors or the Claude Code
plugin's bundled OAuth servers. Do not substitute another surface's authentication.
