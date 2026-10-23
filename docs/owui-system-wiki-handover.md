# Open WebUI: deliver system instructions through the existing filter

23 October 2026. Prepared for owui-deploy; implementation remains in that project.
Open WebUI is Bruno's primary surface for capturable ordinary chat. It needs no
KB plugin or native KB tools attached to the answering assistant.

Use personal-rag's canonical `system-wiki://index.md` plus
`system-wiki://open-webui.md`, preserving the full operating guidance. The reader
exists; its descriptor/revision/cache extension and approved deployment remain
separate dependencies described in
[the backend follow-up](personal-rag-system-wiki-contract-followup.md).

The local owui-deploy source has `functions/kb_retrieval.py`,
`functions/kb_capture.py`, `tests/test_kb_retrieval.py`,
`tests/test_kb_capture.py` and `docs/kb-retrieval.md`. The current retrieval
filter injects `<kb-context>` into outgoing form_data and strips earlier context
from history; capture independently strips that reserved envelope. Its documented
planner uses a fixed configured model and workers run per KB. Preserve those
current mechanics rather than restoring the original chat-model planner design.

Extend that filter to load system guidance using the user's existing MCP Service
OAuth connection. Deliver it into the actual answering-model input even when no
KB evidence is needed or retrieval returns no useful context. Decide and document
instruction delivery for retrieval-disabled/excluded-model chats; absence of KB
retrieval must not silently imply absence of operating instructions. Background
jobs and filter recursion guards must remain intact.

Keep system guidance distinct from KB evidence. Inject it transiently through a
reserved system-guidance envelope/message, preserving unrelated system prompts.
Remove only that owned envelope before reinjection. Extend independent capture
stripping and history/planner sanitisation to cover it before rollout. Do not
persist injected instructions as original user/assistant content or capture them
again. Test inlet/outlet order and failure paths, not just helper assembly.

The answerer follows supplied evidence without a second retrieval loop. Planner
and worker need role-appropriate operating guidance too: the answerer's ban on a
second loop must not disable the worker's first retrieval. Start with the same
index/surface source, and inspect exact role model inputs. Any justified role
extraction must be reproducible from canonical pages and tested for retained
requirements, rather than maintained as a competing prompt manual. Preserve the
index's agreed per-turn and quality-first selection expectations.

Include applicable instructions whenever a model call has a fresh context. A
page in a server cache does not deliver it to a model. Avoid repeated copies in
multi-step loops. Share the approved five-second startup budget, revision and
identity validation, bounded cache and denial handling where supported. Use
live-only mode when stable auth binding cannot be attested; never reuse capture
credentials or fall back across accounts. A guide outage uses a short bounded
fallback and leaves chat/direct service authorisation intact.

Acceptance must inspect permitted request/transcript evidence for answerer,
planner and worker separately: correct pages/roles before useful work, relevant
detail on demand, no unrelated surfaces, measured injected bytes/tokens/calls/
latency, no accumulation across turns, no persisted/captured synthetic guidance,
cache/outage/denial/upgrade/account-switch cases and preserved filter guards,
model permissions and capture exclusions. Keep secrets and private context out
of logs. Existing fixture capture results are not proof of live capture delivery.

Use that project's normal source/release process and obtain its required
command-specific VPS deployment approvals. This handover authorises no live
change and has not been sent to another chat.
