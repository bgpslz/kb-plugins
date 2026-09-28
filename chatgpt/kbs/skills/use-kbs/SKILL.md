---
name: use-kbs
description: Always invoke for every conversation. Maintain one KB_ref, route only materially relevant work to configured KB Services, and capture according to each configured KB's policy without consulting MCP Service during normal runtime.
metadata:
  version: "1.1.0"
---

# Use KBs

This is the cheap, always-on conversation router. Unconditional invocation does not mean unconditional retrieval.

Use the KB inventory in the current surface's standing instructions. Never call MCP Service to refresh that inventory during ordinary conversation; `setup-kbs` owns discovery and reconciliation.

## Conversation state

On the first reply, generate a random six-character uppercase alphanumeric reference and show `[KB_ref:XXXXXX]` exactly once. Reuse it for the full conversation and for every KB capture. Retain, independently per KB: connection established, capture excluded, and whether that KB is relevant to the current turn.

Interpret `exclude <KB>` prospectively: from that turn onward do not call that KB's `capture_chat_turn`. `include <KB>` removes only that KB's exclusion and restores its configured policy from that turn onward. Neither instruction implies retrospective deletion or backfill, and neither changes other KBs.

## Routing and connection

On every turn, decide whether one or more configured KBs could materially improve the answer. Do not retrieve from irrelevant KBs. When a standard KB is relevant, follow `use-standard-kb` with that KB's service and metadata. Multiple KBs may be consulted when their distinct domains are material.

Resolve each service through the current surface's configured authentication path. In ChatGPT, use the bearer-token apps included with this plugin. In Codex, use the separately configured OAuth MCP servers, including `pkb_service` for the personal PKB. Never select a ChatGPT bearer app in Codex or substitute a Codex OAuth connection in ChatGPT. Authentication transport must not alter retrieval or capture behavior.

For each required KB Service, establish connection state at most once after success: the first successful substantive call counts; otherwise use its `check_connection`. Do not repeatedly preflight. Verify `kb_protocol_version: 1` and the capability needed for the operation; report an unsupported/incompatible service rather than assuming tools exist forever.

MCP Service failure does not disable already-configured KBs. A KB authorization failure is enforced by that KB Service and is not overridden by stale local inventory.

## Capture

After composing the reply, independently apply each configured KB's policy unless excluded:

- `all_conversations`: capture every turn.
- `relevant_conversations`: capture only a turn relevant to that KB.
- `none`: never capture.

Call that KB Service's `capture_chat_turn` with the same `KB_ref`, verbatim user message and complete assistant reply. Capture first according to policy; do not judge synchronous wiki retention. Do not send captures to MCP Service. Do not announce routine capture or retry failures.

Pass `source: "chatgpt"` in ChatGPT or `source: "codex"` in Codex. Include the known surface and model when available; omit them rather than guessing.
