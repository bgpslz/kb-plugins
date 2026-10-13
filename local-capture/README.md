# Local session capture

Shared standard-library implementation for both plugin distributions. `capture.py`
extracts completed visible turns from Claude Code and Codex JSONL sessions and
sends Capture Protocol v1 to MCP Service. `install.py` installs a per-machine
runtime, Stop/SessionEnd hooks, and a daily launchd sweep on macOS.

For user/laptop setup, prefer [the assistant-guided platform guide](SETUP.md).
The installed plugin already includes these scripts: no source clone or Git
knowledge is needed. macOS capture is implemented; Windows and Linux/WSL
credential/scheduler adapters and bundled-runtime installers are planned.

For developers with a source checkout, use a durable Python 3.11+ interpreter to run:

```sh
python3.11 local-capture/install.py --account your-email --activate
```

The token is entered directly at the Keychain prompt from `security`, never in
chat, argv or a file. Create the user's MCP Service token at its `/account` page.
The runtime reads the `kbs-local-capture` Keychain service with that email as
account. It uses the existing bearer authentication contract, not retrieval OAuth.
Token labels still use the existing service token type; no authentication-filter
change accompanies this release.

Codex hooks are written to `~/.codex/config.toml`; existing `notify` and hooks
are preserved. Trust the new definitions through Codex `/hooks`. Claude hooks
are written to `~/.claude/settings.json`, and the Claude plugin also ships hooks
calling the same installed runtime. Duplicate triggers are harmless because the
receipt store and server deduplicate. Verify the desktop Code tab separately.
An unloaded/new plugin does not establish that a hook fired.

The runtime lives in `~/.local/share/kbs-capture`. Configuration, receipt hashes
and logs live in `~/Library/Application Support/kbs-capture` with private modes.
A receipt is committed only after `structuredContent.status == "queued"`.
Logs contain exception classes and size failures, never text, tokens or headers.
Tool calls, outputs, file/image blocks, thinking, injected context and sidechains
are excluded. Over-limit turns fail locally rather than being silently truncated.
Unknown formats fail soft; update fixture tests when the transcript format changes.

All projects are included by default from the first install timestamp; existing
historical turns are not backfilled. Reinstall preserves that boundary. The sweep
revisits session files changed since installation, including archived Codex
sessions. Optional `excluded_projects` shell globs match the transcript working
directory (for example `/Users/you/private-project/*` plus the root itself).
Changing exclusions takes effect on the next scan and does not delete queued
captures. Removing an exclusion makes still-eligible unsent turns available again. There is no in-chat exclusion command.

Run `python3.11 local-capture/test_capture.py` for extraction, replay, offline,
MCP JSON/SSE handshake and isolated installer tests. After editing the shared
implementation, copy `capture.py` and `install.py` into both packages' setup-kbs
`scripts` directories; keep their bytes identical. Hook workers detach immediately
and do not block the app. The backstop runs daily at 03:15 machine-local time and
on login. Offline/network errors remain retryable on subsequent triggers.

Before retiring old instructions, verify real new turns from every used client
in the user's Capture Review queue. Reconcile the managed v2 block in each cloud
and local instruction store independently; changing `~/.claude/CLAUDE.md` needs
Bruno's approval. Prepared files alone do not prove live capture.

To disable: unload `com.summerleaze.kbs-capture` with launchctl, remove only its
managed Codex block and Claude handlers, and disable the plugin's Claude hooks.
Remove the corresponding Keychain item if the machine is decommissioned. Keep
other hooks and `notify`. Restore old instructions only if that capture path is
intentionally being reinstated.

References: [Codex hooks](https://learn.chatgpt.com/docs/hooks),
[Claude Code hooks](https://code.claude.com/docs/en/hooks).
No cloud hooks, scraping or Compliance API integration is part of this component.
