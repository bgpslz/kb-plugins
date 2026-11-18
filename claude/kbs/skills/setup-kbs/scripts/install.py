#!/usr/bin/env python3
"""Idempotent macOS installer; prepare first, then activate hooks and daily sweep.

Never changes notify or standing instructions. Preserves unrelated hooks and
settings. Codex capture hooks are recognised by content, so a Codex rewrite of
the managed markers does not block reinstallation. Token entry is an interactive Keychain operation, never a CLI token
argument. Use Python 3.11+ for TOML validation. --home permits isolated dry runs.
The CLI rejects non-macOS platforms before writing any hook or runtime files.
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import plistlib
import re
import shlex
import shutil
import subprocess
import sys
import tomllib

START = '# BEGIN kbs-local-capture'
END = '# END kbs-local-capture'
EVENTS = ('Stop', 'SessionEnd')
OURS = 'kbs-capture/capture.py'
# One generated hook entry. Codex may rewrite the file when the user trusts the
# hooks (it has dropped the END marker), so entries are found by content, not
# by the markers, and updated in place to keep Codex's trust records valid.
STANZA = re.compile(r'^\[\[hooks\.(Stop|SessionEnd)\]\]\n\[\[hooks\.\1\.hooks\]\]\n'
                    r'type = "command"\ncommand = ".*kbs-capture/capture\.py.*"\ntimeout = \d+\n', re.M)


def stanza(event, command):
    return '\n'.join([f'[[hooks.{event}]]', f'[[hooks.{event}.hooks]]', 'type = "command"',
                      'command = ' + json.dumps(command), 'timeout = 3', ''])


def hook_commands(parsed, ours):
    hooks = parsed.get('hooks', {})
    return {event: [h.get('command') for group in hooks.get(event, []) for h in group.get('hooks', [])
                    if (OURS in str(h.get('command', ''))) == ours] for event in EVENTS}


def codex_config(existing, command):
    parsed = tomllib.loads(existing)
    if parsed.get('features', {}).get('hooks') is False or parsed.get('allow_managed_hooks_only'):
        raise ValueError('Codex configuration disables local hooks; reconcile explicitly')
    seen = set()
    def update(match):
        if match.group(1) in seen:
            return ''
        seen.add(match.group(1))
        return stanza(match.group(1), command)
    result = STANZA.sub(update, existing)
    missing = [event for event in EVENTS if event not in seen]
    if missing:
        block = '\n'.join([START] + [stanza(event, command) for event in missing] + [END])
        result = result.rstrip() + '\n\n' + block + '\n'
    updated = tomllib.loads(result)
    # Fail closed if an edited entry was not recognised or another hook changed.
    if (hook_commands(updated, False) != hook_commands(parsed, False)
            or hook_commands(updated, True) != {event: [command] for event in EVENTS}):
        raise ValueError('Codex capture hooks need explicit reconciliation')
    return result


def claude_config(existing, command):
    config = json.loads(existing or '{}')
    hooks = config.setdefault('hooks', {})
    for event in ('Stop', 'SessionEnd'):
        groups = hooks.setdefault(event, [])
        # Remove only our own handlers when the interpreter/path changes.
        cleaned = []
        for group in groups:
            group = dict(group)
            group['hooks'] = [h for h in group.get('hooks', [])
                              if 'kbs-capture/capture.py' not in h.get('command', '')]
            if group['hooks']:
                cleaned.append(group)
        cleaned.append({'hooks': [{'type': 'command', 'command': command, 'timeout': 3}]})
        hooks[event] = cleaned
    return json.dumps(config, indent=2, ensure_ascii=False) + '\n'


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text() != text:
        backup = path.with_suffix(path.suffix + '.before-kbs-capture')
        if not backup.exists():
            shutil.copy2(path, backup)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(text)
    temporary.replace(path)


def install(home, account, activate=False):
    data = home / 'Library/Application Support/kbs-capture'
    runtime = home / '.local/share/kbs-capture'
    data.mkdir(parents=True, exist_ok=True, mode=0o700)
    runtime.mkdir(parents=True, exist_ok=True)
    capture = runtime / 'capture.py'
    command_base = shlex.quote(sys.executable) + ' ' + shlex.quote(str(capture))
    codex = home / '.codex/config.toml'
    claude = home / '.claude/settings.json'
    codex_text = codex_config(codex.read_text() if codex.exists() else '', command_base + ' hook --source codex')
    claude_text = claude_config(claude.read_text() if claude.exists() else '', command_base + ' hook --source claude')
    config_path = data / 'config.json'
    config = json.loads(config_path.read_text()) if config_path.exists() else {
        'capture_from': datetime.now(timezone.utc).isoformat(), 'excluded_projects': [],
    }
    config['keychain_account'] = account
    config['endpoint'] = 'https://mcp-service.summerleaze.com/mcp'
    write(config_path, json.dumps(config, indent=2) + '\n')
    shutil.copy2(Path(__file__).with_name('capture.py'), capture)
    write(codex, codex_text)
    write(claude, claude_text)
    job = home / 'Library/LaunchAgents/com.summerleaze.kbs-capture.plist'
    payload = {'Label': 'com.summerleaze.kbs-capture',
               'ProgramArguments': [sys.executable, str(capture), 'sweep'],
               'StartCalendarInterval': {'Hour': 3, 'Minute': 15},
               'RunAtLoad': True, 'ProcessType': 'Background',
               'StandardOutPath': str(data/'launchd.log'), 'StandardErrorPath': str(data/'launchd.log')}
    job.parent.mkdir(parents=True, exist_ok=True)
    job.write_bytes(plistlib.dumps(payload))
    if activate:
        if home != Path.home():
            raise ValueError('Cannot activate an isolated install')
        # -w without a password asks securely; no token appears in argv or files.
        subprocess.run(['/usr/bin/security', 'add-generic-password', '-U', '-s', 'kbs-local-capture',
                        '-a', account, '-w'], check=True)
        domain = 'gui/' + str(__import__('os').getuid())
        subprocess.run(['/bin/launchctl', 'bootout', domain, str(job)], capture_output=True)
        subprocess.run(['/bin/launchctl', 'bootstrap', domain, str(job)], check=True)
    return config_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--account', required=True, help='MCP Service account email; not a token')
    parser.add_argument('--home', type=Path, default=Path.home())
    parser.add_argument('--activate', action='store_true', help='Prompt for Keychain token and load launchd')
    args = parser.parse_args()
    if sys.platform != "darwin":
        parser.error("Local capture currently supports macOS only; see the setup-kbs platform guide. Windows and Linux/WSL adapters are not implemented.")
    __import__('os').umask(0o077)
    install(args.home, args.account, args.activate)
    print('Prepared local capture. Review/trust Codex hooks using /hooks. Verify a new turn on each app before retiring old instructions.')


if __name__ == '__main__':
    main()
