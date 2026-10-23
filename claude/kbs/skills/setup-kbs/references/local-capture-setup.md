# Set up local capture on this computer

This is the user guide and the assistant's platform-specific procedure. It applies
on the computer running the coding client, including a laptop; installing on
another Mac does not configure this computer.

## Ask the AI to do it

Install the KBs plugin through the client's plugin browser. In Codex desktop with
local tools, or Claude Desktop's **Code** tab with a **Local** environment, ask:

> Use setup-kbs to install local chat capture on this laptop for Codex and Claude
> Code. Detect my operating system, use the installer included in the installed
> plugin, and handle the setup for me. Preserve existing settings and help me
> verify that captures arrive before retiring the old capture instructions.

The same request works in either coding CLI. The setup skill is explicit-only.
Ordinary Claude Chat, cloud coding sessions and clients without local computer
access cannot install hooks on this laptop; switch to a local coding session.
The user does not need to clone the source repository or understand Git.
Marketplace authentication or fetching may still need the client's own Git support.

## Platform status

| Environment | Local capture status | Credential storage / retry job |
| --- | --- | --- |
| macOS, native Codex and Claude Code | Implemented; installer configures both clients once | macOS Keychain / launchd |
| Windows, native clients | Not implemented yet; do not run the macOS installer | Windows credential storage / Task Scheduler are required |
| Linux or Windows WSL | Not implemented yet | A separate Linux credential and scheduling adapter is required |

macOS and native Windows are the initial desktop targets. Linux/WSL is a later
CLI-focused target. WSL sessions have their own home, paths and credentials;
Windows-native installation must not be represented as covering WSL sessions.

## macOS: assistant-guided installation

1. Confirm this is a local macOS coding session with permission to update the
   user's local hook settings, Keychain item and launchd definition. Obtain the
   MCP Service account email; never request the bearer token in chat.
2. Locate `scripts/install.py` and `scripts/capture.py` beside this installed
   `setup-kbs` skill. Use those packaged files. Do not require a Git clone or
   hard-code another user's home, account, interpreter or plugin cache version.
3. Discover a persistent Python **3.11 or later** and check its version and
   executable path. No pip packages are needed. Check existing interpreters
   first; use a client's runtime-discovery capability when available. An app's
   bundled Python is not guaranteed on every client or suitable for unattended
   hooks if its path disappears on upgrade. Do not bind hooks to a temporary
   virtual environment or disposable download directory.
4. If no suitable interpreter exists, offer the official [Python macOS
   installer](https://www.python.org/downloads/macos/). Homebrew is an alternative
   only when already available or explicitly chosen. The AI can guide the GUI
   installation or use the selected package manager; do not assume `brew` exists.
5. Prepare the installation with the discovered absolute interpreter path:
   `<python> <installed-skill>/scripts/install.py --account <email>`.
   It preserves existing hooks, Codex `notify`, project exclusions and the original
   capture boundary. It installs both clients and the daily retry job definition.
6. In a **user-visible Terminal**, run the same command with `--activate`. The
   macOS `security` prompt stores the MCP Service bearer token directly in
   Keychain. The user obtains the token from
   [MCP Service account](https://mcp-service.summerleaze.com/account).
   Never request or pass the token through chat, shell arguments, a temporary
   file or a logged tool interaction. If this client cannot open an interactive
   prompt, supply the exact discovered command for the user to run in Terminal.
7. Verify the Keychain item's existence without reading its secret into tool
   output, the loaded launchd job and installed hook definitions. Restart the
   coding clients. In Codex, help the user review/trust Stop and SessionEnd via
   `/hooks`; do not bypass trust. Check Claude settings and test its Desktop Code
   tab separately when used.
8. Complete a new turn on each used surface. Verify a server `queued`
   acknowledgement in receipts and the conversation in the user's Capture Review
   queue. Distinguish a manual sweep from an actual hook-triggered capture.
   Do not report successful activation merely because configuration files exist.
9. Only after verification reconcile that computer's managed standing instructions
   to v2 and use the retrieval-only skill release. Preserve unrelated instructions
   and working OAuth connections; personal Claude instructions need the user's
   approval. Start fresh sessions and confirm model-generated tags and routine
   chat-capture calls are gone while automatic capture continues.

All local projects are included from the first install time; historical turns are
not backfilled. Exclusions are explicit globs in the private capture configuration.
One shared runtime services both local apps. Cloud Code and web/mobile chat receive
retrieval setup only. Human paste into Capture Review is optional and outside that
setup; Open WebUI retains its separate server-side route.

## Windows: current instructions and implementation requirements

The user can install and use the KBs plugin for retrieval on native Windows, but
release 1.3.3 does **not** provide Windows local capture. The installer stops before
writing settings there. Until a Windows capture release is available, use Open
WebUI capture or manual paste. Do not retire a working existing capture route merely
because the retrieval-only plugin has been installed.

A Windows setup skill must detect native Windows versus WSL before proceeding. A
Python install by itself will not make the current Mac capture program work. Do
not give `brew`, `/usr/bin/security` or `launchctl` instructions on Windows.

The Windows implementation needs:

- A user-scoped persistent runtime and configuration directory, native transcript
  paths and command quoting, and detached worker launch without console windows.
- Windows credential storage with direct user secret entry, never plaintext token
  files or token arguments.
- A per-user Task Scheduler retry job at login and daily, retaining missed work.
- Native Windows tests of Codex and Claude Code hooks, secure token access,
  offline retries, deduplication, reinstallation and Desktop Code-tab capture.

## Remove the Python prerequisite: planned packaging

A user-downloadable, signed installer with a bundled runtime can remove the need
to install Python separately. Provide macOS and Windows packages, a direct token
entry screen, per-user installation, uninstall/update support and the same queue
verification. This packaging is **planned, not shipped**. The immediate macOS
option is AI-guided installation from the already installed plugin.

## Sources

- [Codex plugins](https://learn.chatgpt.com/docs/plugins)
- [Codex hooks and trust](https://learn.chatgpt.com/docs/hooks)
- [Claude Desktop local environments](https://code.claude.com/docs/en/desktop)
- [Claude Code native Windows and WSL](https://code.claude.com/docs/en/setup)
