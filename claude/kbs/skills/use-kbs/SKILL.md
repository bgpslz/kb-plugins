---
name: use-kbs
description: Always invoke for every conversation. Maintain one KB_ref, route only materially relevant work to configured KB Services, and send each eligible turn once to MCP Service for human-reviewed routing.
metadata:
  version: "1.2.0"
---

# Use KBs

This is the cheap, always-on conversation router. Unconditional invocation does not mean unconditional retrieval.

Use the KB inventory in the current surface's standing instructions. Never call MCP Service to refresh that inventory during ordinary conversation; `setup-kbs` owns discovery and reconciliation. The only ordinary-runtime MCP Service call is the final, fail-soft capture append described below.

## Conversation state

On the first reply, generate a random six-character uppercase alphanumeric reference and show `[KB_ref:XXXXXX]` exactly once. Reuse it for the full conversation and every MCP Service capture. Retain, independently per KB: connection established, capture excluded, and whether that KB is relevant to the current turn.

Interpret `exclude <KB>` prospectively: from that turn onward, omit that KB's policy when deciding whether a turn is eligible for central capture. `include <KB>` removes only that KB's exclusion and restores its configured policy from that turn onward. Neither instruction implies retrospective deletion or backfill, and neither changes other KBs. If another non-excluded KB makes the turn eligible, the destination-independent capture still enters review; exclusion does not pre-decide the human's later routing choice.

## Routing and connection

On every turn, decide whether one or more configured KBs could materially improve the answer. Do not retrieve from irrelevant KBs. When a standard KB is relevant, follow `use-standard-kb` with that KB's service and metadata. Multiple KBs may be consulted when their distinct domains are material.

Resolve each service through the current surface's configured OAuth path. In Claude web, Desktop, and mobile, use the connected remote OAuth connectors. In Claude Code, use the plugin's bundled OAuth MCP servers, including `mcp-service` for capture. Never assume a cloud Claude connector configures Claude Code or that one machine's Claude Code connection configures another. Authentication transport must not alter retrieval or capture behavior.

For each required KB Service, establish connection state at most once after success: the first successful substantive call counts; otherwise use its `check_connection`. Do not repeatedly preflight. Verify `kb_protocol_version: 1` and the capability needed for the operation; report an unsupported/incompatible service rather than assuming tools exist forever.

MCP Service failure does not disable already-configured KBs. A KB authorization failure is enforced by that KB Service and is not overridden by stale local inventory.

## Capture

After composing the reply, independently evaluate each configured KB's policy unless that KB is excluded:

- `all_conversations`: capture every turn.
- `relevant_conversations`: capture only a turn relevant to that KB.
- `none`: never capture.

If at least one non-excluded policy qualifies, call MCP Service's Capture Protocol v1 `capture_chat_turn` exactly once with the same `KB_ref`, verbatim user message, complete assistant reply, and attachment names. This capture is pre-destination: do not select a KB, classify retention value, or judge wiki relevance. The Capture Review Application handles destinations later.

Never call a KB Service's legacy `capture_chat_turn` from this router and never fall back to per-KB fan-out when MCP Service is unavailable. Capture is the last action of the turn; do not retry or announce routine capture failures. MCP Service capture failure is non-fatal and does not affect direct KB retrieval.

Pass `source: "claude"` and the known Claude surface and model when available; omit optional values rather than guessing.
