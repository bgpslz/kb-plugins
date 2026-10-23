# AGENTS.md

## Service versions — before significant commits

Codex and Claude Code must identify the affected services/components and propose
an explicit patch or minor version bump before committing a significant set of
changes. Use patches for compatible fixes and minors for compatible new features;
state the old/new versions and rationale. Propose breaking/major changes separately.
Documentation-only changes do not automatically require a service bump. Keep
manifests, reported versions, canonical sources, generated copies and tests in
sync. Version proposals do not authorise deployment or client installation.

The source release inventory is `setup/package.json`; collector versions live in
`local-capture/capture.py`. Use `scripts/sync-packages.py --write` and package
checks after shared edits. Never edit installed plugin caches as a release method.

## Project workflow

Read README.md and relevant docs first. Work on main normally, preserve unrelated
changes, and keep capture/retrieval/instruction readiness separate. Backend
services belong to personal-rag and Open WebUI filters to owui-deploy; each has
its own release process and approvals. Keep documentation and authorised PKB
project updates consistent; report failed/pending updates explicitly.

Use the configured KB inventory and authentication. Follow the session's KB
instructions; do not discover registry inventory during ordinary runtime or
capture conversations through model calls.
