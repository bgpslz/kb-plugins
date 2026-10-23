# KBs plugin for Claude

Source 1.4.0 is unreleased. `use-kbs` is now a small instruction-based bootstrap
for the system-wiki index plus applicable surface page; `setup-kbs` supplies
setup adapters and the startup/cache core. Explicit `build-kb` and
`maintain-project-docs` remain. `use-standard-kb` stays packaged until replacement
acceptance; installed instructions have not been retired.

Open WebUI is the primary surface for capturable ordinary chat, using its own
filters without a KB plugin. Three routes feed the same human review queue: Open WebUI server capture, local
Claude Code/Codex session capture, and manual paste for other surfaces. See
[local capture installation](../../local-capture/README.md). Local Code capture is
verified separately per surface and machine. Cloud Code and Claude Chat receive
retrieval setup only; capture is not a prerequisite for retrieval or its guidance.
`capture_policy` remains review metadata; in-chat exclude/include is retired.

Claude web, Desktop, and mobile use remote OAuth connectors for MCP Service and
each KB Service. Claude Code loads the plugin's bundled `mcp-service` for
registry reconciliation, plus its bundled
`pkb-service`, from `.mcp.json`; users complete OAuth authorization through
`/mcp` without adding duplicate servers. Authentication
transport does not change the retrieval protocol.
Cloud Claude profile preferences and local Claude Code user instructions in
`~/.claude/CLAUDE.md` are reconciled independently. `setup-kbs` and `build-kb`
are user-invoked only; `use-kbs` remains model-invoked because it is the
standing conversation router.

`build-kb` inspects service-declared lifecycle, write behaviour and proposal
schema. Automatic application requires an authenticated personal owner and a
compatible service; organisation changes and protected policy pages require human
review even during bootstrap. Older reviewed services remain supported. The skill
never performs the controller's lifecycle transition.

`maintain-project-docs` preserves repository documentation and proposes distilled
architecture, decisions, status and plans to the configured owner PKB. It reports
pending/failed updates and maintains authorised organisation documentation.
Shared system-use guidance belongs in the system wiki, not Summerleaze OKB wiki. Source release, backend
deployment and installed-client acceptance are separate milestones.

When migrating a working local capture route, preserve and verify its replacement
before retiring it. Reconcile retrieval instructions independently and inspect
active skill paths for duplicates. Fresh-session tests, source changes, installed
skills and cloud preferences are separate states.

The setup revision adds native adapters, a read-only evidence/report helper and
managed-instruction drafts; see its [guide](skills/setup-kbs/references/setup-evidence.md).
The helper does not log in or save settings. The native adapter can save an
explicit approved plan with backups and stale-plan checks. Startup integration
still needs the backend contract extension and actual context-delivery proof;
see the [client guide](skills/setup-kbs/references/system-wiki-client.md).

For assistant-guided laptop setup without a source checkout, ask `setup-kbs` to
install local capture on this computer. See the [platform guide](skills/setup-kbs/references/local-capture-setup.md).
Capture currently supports macOS; Windows and Linux/WSL adapters and standalone
installers with bundled runtimes are planned.
