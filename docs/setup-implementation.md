# Plugin alignment implementation status

Updated 23 October 2026 against personal-rag's
`docs/kb_plugins_completion_brief.md` and current source `9d39527`.
Bruno's phase approvals remain in force. This is source work, not live migration
acceptance. Earlier phase observations remain in the
[audit](architecture-alignment-audit.md) and
[approved contract](system-wiki-bootstrap-contract.md).

## Delivered source

- `setup/reconcile.py`: read-only evidence evaluation, actual surface/execution
  routing, per-KB capability/wiki-read evidence, OAuth identity/callback/scope
  diagnostics, inventory revocation versus outages, duplicate diagnostics and
  managed-block drafts that preserve unrelated bytes and reject ambiguity.
- `setup/native.py`: supported Codex TOML/Claude JSON store discovery, reuse of
  native/plugin endpoints, additive plans, stale-plan refusal, private backups,
  permission-preserving atomic persistence and read-back. No login or permission
  expansion. Personal Claude instructions retain their separate approval gate.
- `setup/system_wiki.py`: single-page detail loading and two-page startup through
  a host-supplied authenticated bridge. Startup validates one descriptor, obtains
  the complete index plus applicable surface at one revision, and shares one
  five-second budget. Missing pages/metadata and mixed revisions fail coherently.
- Account/service/connection/auth-binding cache isolation, denial invalidation,
  24-hour freshness, seven-day total fetched-age bound, public-only private disk
  cache, quota, payload limits, atomic writes and nonblocking concurrency. A
  failed upgrade cannot revive the old revision on a later outage. Without a
  trusted native binding the client operates live-only.
- `setup/bootstrap.md`: small transition use-kbs skill requiring model-visible
  reads before substantive work, with restoration after context loss and no
  per-turn duplicate loading. `use-standard-kb` remains available during staged
  acceptance, but is not mandatory alongside successful wiki loading.
- A short canonical `setup/fallback.md`, independent of retired skill names,
  selected only on incomplete loading. Managed blocks and both distributions
  use this same source. The startup return value explicitly requires host delivery;
  it does not claim model injection.
- `setup/package.json`: source release version/inventory, used by package checks
  and packaged setup diagnostics. Both manifests now identify unreleased 1.3.5.
- Explicit build and development-documentation workflows remain. Shared user
  guidance for this system belongs in personal-rag's system wiki; project knowledge
  belongs in Bruno's PKB. Do not copy that shared manual to Summerleaze OKB wiki.
- Open WebUI is the primary surface for capturable ordinary chat. Plugins serve
  native setup/instruction delivery and explicit workflows. Its separate filter
  owns instruction/retrieval injection and its server integration owns capture.
  Local Code capture remains independently verified; cloud/chat has no assumed
  automatic capture. Capture runtime and existing hook definitions are unchanged.

## Cross-repository dependencies

The personal-rag reader and thirteen pages are implemented. The inspected reader
still lacks `get_system_wiki_capabilities`, content_revision and cache_visibility.
The approved client therefore selects fallback rather than fabricate metadata.
See the [narrow backend follow-up](personal-rag-system-wiki-contract-followup.md).
No system-wiki tool is exposed in this chat; no live backend revision has been
contacted by the new loader. Its deployment requires that project's approvals.

Open WebUI must inject operating instructions into actual answerer/planner/worker
calls, independently of KB evidence. The
[owui-deploy handover](owui-system-wiki-handover.md) identifies current source,
role boundaries, capture/history exclusions and acceptance. It is prepared here,
not implemented elsewhere or sent to another chat.

## Readiness and release

| Surface | Current evidence | Outstanding |
| --- | --- | --- |
| This Codex desktop chat | Existing OAuth PKB capabilities and substantive wiki reads work; exposed installed skill paths remain 1.3.4 | Backend contract/deployment; new-source installation and fresh context-delivery proof |
| Codex CLI | Earlier native parser smoke accepted HTTP shape; current source tests pass | Actual authenticated bridge, fresh CLI loading and separate capture acceptance |
| Claude Code CLI | Earlier isolated native save smoke; installed 1.3.3 was observed on 22 October | Recheck installation, prove authenticated loading; personal instruction edits need approval |
| Claude desktop Code tab | Source routing only | Verify local execution, actual loading and capture independently |
| Cloud Code / ChatGPT / Claude Chat | Source routes to other-harnesses without local capture | Each supported account/cloud store and instruction-based loading acceptance |
| Open WebUI | Separate filter/capture source inspected | Role-specific instruction delivery and live evidence in owui-deploy |

No surface is claimed migrated. Source 1.3.5 has not been published or installed;
no hook, credential, account grant, live cache, personal instruction store or VPS
was changed. Existing runtime instructions in this chat still apply. Current
source capability is not evidence about other installed clients or machines.

First complete and deploy the backend extension through its normal approvals.
Then prove an uncached authenticated index-plus-surface load enters the first
host's model context before useful work, using permitted request/transcript and
harmless marker/behaviour evidence. A hook receipt or model assertion is insufficient.
No authenticated native hook bridge is established here; instruction-based
loading is the implemented weaker alternative and still needs fresh-session proof.

After live/degraded and compaction/resume/new-context acceptance, reconcile the
actual installed package and managed stores through supported mechanisms. Remove
superseded invocation/manual sources on completed surfaces, then repeat acceptance
without them. Do not delete historical caches or unrelated hooks. Only after
acceptance publish/install through normal package mechanisms and repeat fresh-session
checks. No unrelated wiki-review-session fix is a prerequisite.

## Validation

Run from this checkout:

```sh
python3.12 -m unittest discover -s setup -p 'test_*.py'
python3.12 local-capture/test_capture.py
python3 scripts/sync-packages.py
python3 scripts/check-packages.py
git diff --check
```

There are 88 setup tests: 22 evidence, 22 native, 32 detail/cache and 12 startup
checks. The seven capture regressions remain separate. These tests establish
source behaviour and preservation only, not live OAuth, context injection,
installed-version acceptance or capture receipts. Actual injected tokens and
host latency remain unknown; helper metrics report bytes/calls/elapsed time.

## Project knowledge

The canonical PKB project now lives under `projects/knowledge-base-system/`;
the former personal-rag project page is deprecated. Do not submit the older
saved full-section drafts to that compatibility page. Reconcile new component
updates with the current canonical page and report the actual proposal result.

The component update submission on 23 October failed because the PKB service's
Git repository ownership check failed. No ID or publication receipt was returned;
durable proposal state is unknown. The
[complete retained update](pending-pkb-plugin-component-update.md) records the error
and retry boundary. No canonical publication is claimed and no server repair
was attempted.
