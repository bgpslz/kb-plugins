# System-wiki client core — inactive pending integration

`scripts/system_wiki.py` in the packaged skill (source `setup/system_wiki.py`)
implements the approved read/cache/fallback behaviour. Python 3.11+ is required.
This core does not install a startup hook. `use-kbs` supplies instruction-based
loading; `use-standard-kb` is an optional retrieval helper, independent of whether
this core is integrated. This core does not discover tokens, read a credential
store, perform HTTP/OAuth,
reconcile registry inventory or configure capture.

## Authenticated bridge boundary

The native host supplies an async object with:

```python
async def call_tool(name, arguments, timeout_seconds):
    # Use the host's existing authenticated MCP connection and its deadline.
    # Return the decoded MCP tool result; never return credentials.
    ...
```

Only `get_system_wiki_capabilities` and `read_system_wiki_page` are called. The
descriptor is authenticated on every fresh load. Use `load_startup(context, surface, execution)` for the complete index plus
applicable surface page, with one descriptor and one total budget. The older
`load(context, uri)` reads a single explicit detail page; it is insufficient
for startup. No unrelated page is prefetched. Whole-page results may
be direct payloads, MCP `structuredContent`, or one JSON text content block.
Resource access is unnecessary for a host with tool access.

Map native 401/403 to `TransportError(401/403)`, unsupported methods to a distinct
non-outage status (for example 404), and 5xx/network failures to their status or
`TransportError()`. Exceptions/messages are never used as instructions or logged.
Never infer auth denial or availability by parsing arbitrary server prose.
Bridge cancellation/deadline support must be verified before startup integration.

The core has no built-in subprocess bridge: launching another coding model to call
MCP tools, scraping its credentials or creating a bearer token would introduce a
second runtime/authentication path. The actual native startup/read API must be
identified and tested per surface first. A static load instruction and existing
retrieval skills remain the fallback where startup injection is unavailable.

## Host context and cache eligibility

```python
context = Context(
    service_url=actual_mcp_endpoint,
    connection_id=actual_native_connection_id,
    account_id=authenticated_service_local_account_id,
    auth_binding=nonsecret_native_auth_epoch,
    binding_verified=True,
)
result = await Loader(bridge, dedicated_private_cache_directory).load_startup(
    context, surface='codex-desktop', execution='local',
)
# The host must deliver result['text'] to the model; returning it is not injection.
```

This is a host integration example, not a currently installed hook. The endpoint
and connection ID come from the actual native connection. `account_id` must match
the authenticated descriptor. `auth_binding` is a nonsecret stable native identity
for the current account/credential generation, **not a token, token hash, email,
display name or caller-selected assurance**. The host must revoke its attestation
on logout, account/auth change, 401/403 or explicit revocation independently of
the cache; it must not reassert an old binding as unchanged after a denial.

Leave binding fields unverified if the native surface cannot provide that evidence.
Successful online pages can still be used, but are not persisted/reused from disk.
No cache directory is needed when persistent caching is disabled. Inspecting an
account name or finding a config entry alone does not prove the binding.

## Implemented behaviour

- The descriptor/page contract matches the approved v1 names and canonical
  `system-wiki://index.md`. No substitution of a KB's `wiki://` namespace.
- Descriptor validation precedes page/cache use. A valid matching revision and
  trusted binding allow a fresh index cache hit after one descriptor call.
- A 24-hour freshness interval and seven-day **total fetched age** bound public
  outage reuse. This conservative interpretation does not add another seven days
  after freshness expires. Clock rollback makes an entry ineligible.
- Only explicit `public_guidance` pages are persisted. Protected visibility is usable only after that session's authenticated read.
  Missing/unknown visibility fails contract validation. Extra tool
  fields are not persisted. A later protected response removes that URI's old
  public entry.
- Keys partition normalized endpoint (including its path), connection, account/
  auth binding, protocol, revision and URI. An active-binding marker prevents
  switching accounts/credentials away and back offline from reviving old content.
- A 401/403 invalidates persistent eligibility, including fresh entries. Recovery
  requires a successful new page read. Unsupported/malformed contracts fail to
  packaged guidance rather than guessing an endpoint or using an old schema.
- The initial async transport budget is five seconds total. Local filesystem
  operations are bounded by size and checked against the budget, but are not a
  hard real-time guarantee against an unresponsive filesystem. Lock contention
  falls back immediately; there is no per-turn retry or hook installation.
- Private cache directories/files, atomic replacement, content-integrity checks,
  a one-MiB disk budget and oldest-content eviction prevent partial/unbounded
  cache reads. Only content entries are evicted, not denial/binding markers.
  Cache is unavailable on unsupported locking platforms or unsafe directories.
- Index/detail limits are eight/64 KiB UTF-8. Invalid, partial or oversized
  responses are not truncated into the prompt. Canonical Markdown URIs reject
  traversal, encoding tricks, fragments, backslashes and wrong schemes.

Output distinguishes live, authenticated fresh cache, outage cache and packaged
fallback, with a reason, reconnect flag, exact characters/UTF-8 bytes, tool calls
and elapsed milliseconds. Token count is explicitly unknown until measured by
the native tokenizer. The returned text is for the model context; operational
logs should record metadata only, not page content or credentials.

## Verification and remaining acceptance

Run `python3.12 setup/test_system_wiki.py` or the complete setup unittest discovery.
Fixtures cover identity/connection/service separation, auth denials, revision
changes, protected content, expiry, tampering, response envelopes, detail reads,
timeouts, concurrency, permissions, quotas and secret-safe failures.

The backend contract is implemented in personal-rag bb13522 and deployed as
c9ad645 on 23 October, including a native resource request-metadata correction.
The actual plugin loader passed the backend's isolated authentication/dispatch
integration script. Native OAuth resource listing and complete index/local-Codex
reads also passed against production in this existing chat, with source-identical
bytes and matching revision/classification. That is live read/context delivery,
not fresh-session startup or a verified abstract Python bridge. The named tool
catalogue in this chat predates deployment; resource access required no new login.
See personal-rag's `docs/system_wiki_deployment_20261023.md` for the receipt.

Startup returns `kind=system_wiki_startup`, complete/degraded status, the required
URIs, validated page text, one revision and metrics. The combined instruction
text includes both entire pages. The eight-KiB index limit is per page; it does
not limit the combined bundle. Missing, malformed or differently versioned pages
produce one coherent fallback and no partial instruction set. A revision observed
online invalidates older eligibility even if the new startup fails. Outage reuse
requires every required page at one eligible revision. Cache content and model
context retention are independent: the host/bootstrap restores missing context
after compaction/resume or in a new agent; disk cache does not prove delivery.

`setup/bootstrap.md`, generated as use-kbs in both packages, supplies the weaker
instruction-based path through the host's normal model-visible MCP tools. It
requires the same complete contract and falls back without inventing metadata.
It does not enforce a tool deadline where the host exposes none. Successful
loading does not preload the optional retrieval helper or the conditional fallback. Unknown
locality uses other-harnesses; Open WebUI is excluded from this native loader.

Before activation, prove an online uncached read and context delivery in one
actual host using its existing connection. No supported authenticated subprocess
bridge has been established here. OpenAI documents plugin SessionStart hooks,
but hook availability/trust alone does not establish MCP access or delivery:
[official packaging guidance](https://developers.openai.com/plugins/build/plugins).
No second coding model, secret scraping or new token flow is introduced.

Then verify live/cache/outage/denial paths, actual injected tokens/latency,
compaction/resume, separate agent contexts and fresh-session delivery independently
on each target. Keep working installed guidance until those tests pass; only then
retire superseded instructions for that surface. Publishing and installing are
separate milestones. Open WebUI's own instruction delivery remains a separate
filter handover, repository document `docs/owui-system-wiki-handover.md`.
