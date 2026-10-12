#!/usr/bin/env python3
"""Idempotent macOS installer; prepare first, then activate hooks and daily sweep.

Never changes notify or standing instructions. Preserves unrelated hooks and
settings. Token entry is an interactive Keychain operation, never a CLI token
argument. Use Python 3.11+ for TOML validation. --home permits isolated dry runs.
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import plistlib
import shlex
import shutil
import subprocess
import sys
import tomllib

START = '# BEGIN kbs-local-capture'
END = '# END kbs-local-capture'


def codex_config(existing, command):
    if existing.count(START) != existing.count(END) or existing.count(START) > 1:
        raise ValueError('Malformed managed capture block')
    if START in existing:
        before, rest = existing.split(START, 1)
        _, after = rest.split(END, 1)
        existing = before.rstrip() + '\n' + after.lstrip('\n')
    parsed = tomllib.loads(existing)
    if parsed.get('features', {}).get('hooks') is False or parsed.get('allow_managed_hooks_only'):
        raise ValueError('Codex configuration disables local hooks; reconcile explicitly')
    blocks = [START]
    for event in ('Stop', 'SessionEnd'):
        blocks += [f'[[hooks.{event}]]', f'[[hooks.{event}.hooks]]', 'type = "command"',
                   'command = ' + json.dumps(command), 'timeout = 3', '']
    blocks += [END]
    result = existing.rstrip() + '\n\n' + '\n'.join(blocks) + '\n'
    tomllib.loads(result)
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
    return json.dumps(config, indent=2) + '\n'


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
    __import__('os').umask(0o077)
    install(args.home, args.account, args.activate)
    print('Prepared local capture. Review/trust Codex hooks using /hooks. Verify a new turn on each app before retiring old instructions.')


if __name__ == '__main__':
    main()
