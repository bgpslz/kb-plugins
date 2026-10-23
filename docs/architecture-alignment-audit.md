# Architecture alignment: phase 1 audit

22 October 2026. Source baseline: `f77bdbf`, on `main`, initially clean.
Scope and approval sequence: [architecture handover](architecture-alignment-handover.md).

## Outcome and status

Phase 1 has inventoried this checkout, locally visible installations, this
session's skill discovery and local instruction stores. It adds a read-only
source package checker. No runtime skills have been retired or rewritten.
Bruno subsequently authorised phase 2 and approved its
[contract](system-wiki-bootstrap-contract.md). The
[phase 3 setup foundation](setup-implementation.md) is implemented in unreleased
source. This audit's inventories remain the dated pre-change baseline below.

This is a local snapshot, not a setup acceptance test. Cloud account settings,
other machines, fresh-session loading, live capture delivery, registry grants
and deployments have not been tested in this phase.

## Source packages

| Component | Observed state | Disposition |
| --- | --- | --- |
| OpenAI and Claude manifests | Both 1.3.4; each has five skills | Retain package distribution |
| `use-kbs` | 1.3.2; identical across packages | Keep until replacement loading is proven |
| `use-standard-kb` | 1.0.0; identical across packages | Preserve wiki-first and explicit source retrieval fallback |
| `setup-kbs` | 1.3.3; intentionally different client auth/store instructions | Restructure after interface agreement |
| `build-kb` | 1.2.0; same content except Claude explicit-invocation flag | Retain service-owned build/lifecycle contract |
| `maintain-project-docs` | 1.0.0; identical across packages | Retain authorised development workflow |
| Capture installer/runtime | Both packaged copies byte-identical to `local-capture/` | Preserve implementation and regression coverage |
| Capture platform guide | Both copies byte-identical to `local-capture/SETUP.md` | Keep one maintained source |
| Claude bundled servers | MCP Service and Bruno's PKB only | Existing connections are not a general tenant inventory |
| OpenAI app map | MCP Service and PKB ChatGPT app IDs | Preserve separate Codex OAuth path |
| Claude package hooks | Stop and SessionEnd invoke installed capture runtime if present | Keep; audit local/cloud routing before new release |

There is no standalone retrieval setup utility, system-wiki loader or general
client-adapter framework in this checkout. Existing executable setup code is the
macOS capture installer/runtime. Do not present prose setup steps as automation.

Shared runtime guidance is duplicated across the two distributions and managed
instruction blocks. The shared `use-kbs` file is 1,499 characters and
`use-standard-kb` is 1,565; each setup skill is over 9,000 characters. These are
file sizes, not measured injected token counts or latency. Session loading must
be measured separately before any retirement decision.

## Local installations and active discovery

| Target | Evidence | Limit |
| --- | --- | --- |
| Codex `kb-plugins/kbs/1.3.4` cache | All five skill files match source | Cache alone does not prove loading |
| Codex `workspace-directory/kbs/1.3.4` cache | All five skill files match source | Second distribution path needs reconciliation |
| Current Codex desktop session | Skill catalog exposes both copies of `use-kbs`, `use-standard-kb` and `maintain-project-docs`; setup/build are not exposed in that catalog | Does not establish fresh CLI or desktop behaviour |
| Codex config | `kbs@kb-plugins` enabled; `pkb_service` and `mcp_service` OAuth server names present | Does not prove registry or all KB readiness |
| Claude install registry/settings | `kbs@kb-plugins` enabled; registry selects 1.3.3 | No active Claude session tested |
| Claude older caches | 1.2.1, 1.3.2 and 1.3.3 present | Historical caches do not prove multiple active installs |

Claude 1.3.3 has four skills and lacks `maintain-project-docs`. The current Codex
catalog's two paths need investigation through supported installation mechanisms;
neither was removed. The Codex cache does not contain an `installed_plugins.json`
at the Claude-style location; do not assume the clients share an install registry.

## Instructions, connections and capture

- Local Codex `~/.codex/AGENTS.md` contains a managed `kbs-instructions v2` block.
  Local Claude `~/.claude/CLAUDE.md` exists but has no matching v2 delimiter.
  Both contain the older wording that other sessions “are pasted” into Capture
  Review. Future generated instructions must describe optional human paste and
  must not imply automatic capture of chat or cloud Code.
- There is no physical root `AGENTS.md` in this checkout. This session received
  the KB inventory through supplied instructions. Preserve that distinction.
- PKB OAuth returned protocol 1, wiki/build capabilities and a substantive wiki
  index read in this session. No MCP Service discovery or registry changes were
  performed. No SLZKB connection is exposed to this session.
- Codex and Claude local settings each contain two capture commands under their
  hooks. Codex also has hook state metadata, so hook maps must not be parsed as
  event arrays without checking the schema.
- The installed capture runtime matches source. Its configuration, receipt
  database and launchd definition exist. This audit did not read credentials or
  receipt contents, test job activation, or verify a new hook-triggered delivery.
  File presence is not capture readiness.
- No installed files, instruction stores, OAuth connections, hooks, exclusions,
  capture boundaries or receipts were changed.

## Findings to resolve after phase approval

| Priority | Finding and source | Required change / acceptance |
| --- | --- | --- |
| First | Both setup skills say “all four” | Check against actual package inventory; current release has five |
| First | Both setup step 3 unconditionally require Capture Protocol and `capture_chat_turn` | Retrieval-only setup must finish without capture tools, credentials or tests |
| First | Setup step 7 and migration sections gate instruction reconciliation on local intake | Split retrieval readiness, guidance loading and local capture readiness |
| First | Setup does not identify local versus cloud execution before routing Code sessions | Explicit surface/execution matrix; desktop UI alone cannot select capture installation |
| First | Shared capture descriptions and package READMEs imply paste or local capture is part of every setup | Make human paste optional; keep chat/cloud Code retrieval-only |
| Next | OpenAI setup invocation metadata defaults to local capture | Make generic setup entry point surface-aware; preserve explicit local-capture path |
| Next | Setup mentions capability checks but not a required authenticated wiki read | Verify both separately; login alone is insufficient |
| Next | Approval-prompt advice is embedded in connection setup | Keep tool permission choices explicit and separate from successful authentication |
| Next | Setup identity comparisons and callback/scope checks are prose only | Implement small tested adapters after supported stores/contracts are established |
| Later | Shared guidance duplicated in skills, profile blocks and tool descriptions | Move general guidance only after system-wiki serving and loading are proven |
| Later | No startup loader/cache/auth contract | Agree interface first; fail softly on outages without serving protected stale content after auth denial |

The handover's separate personal-rag approval/deployment gates remain in force.
No backend work, unrelated onboarding, auth-provider migration, or Windows/Linux
capture implementation is included here.

## Repeatable checks

Run `python3 scripts/check-packages.py` from any working directory using the
script's path. It checks package versions, skill inventory parity, shared skills
(allowing Claude's explicit-invocation frontmatter), and canonical capture script
and guide copies. Setup content remains client-specific. It only reads source
files; `--root` can target another checkout. A failure exits nonzero.

Checks completed:

- Current package parity check passed.
- Isolated temporary copies proved detection of changed/missing shared resources,
  unequal skill inventories, unequal versions and malformed JSON manifests.
- Existing capture regression suite passed: seven tests using Python 3.12,
  including extraction boundaries, retries/deduplication and isolated installation.

These checks do not validate setup wording, supported client settings, installed
versions, live services or fresh-session behaviour.

## Next phase for review

Phase 2 should produce a proposed bootstrap and cross-repository interface
document, before code depends on it. It must settle:

1. System-wiki index identity, read/list contract and protocol/capability discovery
   in personal-rag/MCP Service, with explicit distinction from KB wiki tools.
2. Per-surface bootstrap and fallback text, retaining current working retrieval
   until replacement loading is verified.
3. Cache account/service identity, TTL, invalidation on authentication failures,
   outage behaviour and protected-content handling.
4. A client/environment test matrix and an order for implementing setup adapters
   and proving startup loading independently of capture.

No new system-wiki endpoint is specified or claimed deployed by this audit.

## Personal-KB documentation status

The configured PKB Service rejected the distilled project update because an open
wiki session requires completion or operator recovery. Publication and an accepted
pending proposal were not confirmed; rejected database records may exist. The
complete [proposed section](pending-pkb-architecture-alignment.md)
is retained here for reconciliation and resubmission after that session is
resolved. Existing wiki sessions were not changed to clear this failure.

Subsequent live browser inspection on 22 October identified human review branch
`wiki-review/9b45c99a934e`, with three approved/committed changes not yet merged:
proposal 3 (Tirol hotel seasonality source note), proposal 7 (maintenance index),
and proposal 6 (knowledge hierarchy). The read-only merge preview confirmed these
contents. The session was left unchanged because the suggested closure was
conditional on it being empty. Normal Discard returns committed proposals to
pending; Merge publishes the staged contents. No action was taken on either.

Bruno subsequently reported merging the three approvals. A new live merge-preview
request showed zero approved changes and no net differences; automatic publication
still reported an open session. The main review GET creates a session when absent,
so returning to review after Merge can recreate an empty session. No session was
changed here. The update was then successfully submitted with `auto_apply=false`:
proposal **53**, origin `a01e91eb040e455ea4fb58ecab8dc5a7`, pending human review.
It is not published. The [saved submission](pending-pkb-architecture-alignment.md)
now records that result and the exact submitted content.
