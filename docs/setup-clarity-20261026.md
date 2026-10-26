# Clear setup and retrieval skill responsibilities

The KBs source package 1.4.1 clarifies what setup does, which instructions guide
ordinary chats and how to report readiness. This is a source revision, not a
plugin publication, client installation or service deployment.

## User decision and scope

On 26 October 2026 Bruno requested a clearer setup skill after comparing it with
his global Codex KB instructions and the current system-wiki. He also asked
whether the standard retrieval skill should be removed and how it relates to
`use-kbs`. The setup revision preserves the established connection, guidance and
capture boundaries while replacing historical transition language with present
responsibilities.

`setup-kbs` explicitly configures/checks connections and saved instructions.
`use-kbs` loads the complete system-wiki index and surface guidance before work
in a new/restored context. `use-standard-kb` remains an optional retrieval helper
for selected KBs. It is not a separate system guide, automatic second startup
step or a prerequisite for fallback retrieval. Keeping its existing name avoids
breaking older explicit invocations; it has a useful retrieval role independently
of automatic-loader integration. This supersedes the suggestion that it must be
kept solely until a transition is complete. Users need not invoke both runtime
skills in sequence; the loaded guide governs retrieval.

The setup skill now separates inventory reconciliation, authenticated retrieval,
saved-instruction persistence, model-visible guidance delivery and capture.
Capture is not required for chat/cloud setup, but that does not excuse missing
guidance. Instruction-based loading can work without a native automatic hook;
verification in one existing chat does not prove fresh, resumed or separate-agent
loading elsewhere. The helper report still exposes startup_loading=not_tested;
no evidence evaluator or readiness contract changed.

## Source and distribution

Canonical setup/bootstrap/fallback text stays in setup/. The standard retrieval
helper now also has one canonical source, setup/retrieval.md, regenerated into
both packages by scripts/sync-packages.py. User-facing descriptions distinguish
instruction loading from KB retrieval. Supported invocation policies are preserved.
The setup evidence guide no longer describes the backend's already-deployed
metadata contract as unfinished work. Historical acceptance documents retain
their dates and point here for current semantics.

Package 1.4.0 → 1.4.1 is a patch for compatible instruction/presentation fixes.
Setup/bootstrap metadata is 1.3.5 → 1.3.6; retrieval-helper metadata is
1.0.0 → 1.0.1. Runtime code interfaces, collector/backend versions and protocols
are unchanged. No installed cache, ~/.codex/AGENTS.md, Claude personal instruction
file, authentication, capture job or live system-wiki was changed. Publication
and client updates follow their existing supported mechanisms separately.

## Validation

Validation passed: all 88 setup tests and eight capture regressions, shared-package
generation/parity, six revised skill frontmatter checks, package skill links,
OpenAI UI metadata and preserved invocation policies, and Git whitespace checks.
The generic Codex skill validator does not recognise Claude's existing
`disable-model-invocation` field; its true value was checked separately and the
remaining Claude frontmatter validated in a temporary normalised copy. The source
field was preserved. These are source checks, not installed-version or automatic
instruction-delivery acceptance. The task's final report records commit and
Bruno PKB project update status.
