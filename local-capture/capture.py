#!/usr/bin/env python3
"""Fail-soft local Claude Code/Codex capture, independent of model instructions.

Only recognised visible text and completed turns enter Capture Protocol v1.
Hooks detach a worker; a launchd sweep retries recent sessions. Credentials live
in macOS Keychain. SQLite holds hashes/receipts, never transcript text or tokens.
Unknown records are ignored and incomplete turns are held for the next trigger.
--version reports the collector version and a process-stable source-content hash.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import fnmatch
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import time
from urllib.request import Request, urlopen

VERSION = '1.1.0'
try:
    BUILD_ID = 'sha256:' + hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
except OSError:
    BUILD_ID = None  # Diagnostics must not disable fail-soft capture.


def version_info():
    return {'service': 'kbs-local-capture', 'version': VERSION, 'build_id': BUILD_ID}


ENDPOINT = 'https://mcp-service.summerleaze.com/mcp'
KEYCHAIN_SERVICE = 'kbs-local-capture'
DATA = Path.home() / 'Library/Application Support/kbs-capture'


def text_content(content):
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ''
    return '\n'.join(x['text'] for x in content if isinstance(x, dict)
                     and isinstance(x.get('type'), str) and x['type'].lower() in ('text', 'input_text', 'output_text')
                     and isinstance(x.get('text'), str))


def records(path):
    with path.open(encoding='utf-8') as stream:
        for line in stream:
            try:
                item = json.loads(line)
                if isinstance(item, dict):
                    yield item
            except (ValueError, UnicodeError):
                continue


def parse_claude(rows):
    prompt, replies, meta, completed = [], [], {}, False
    result = []
    def finish():
        if prompt and replies and completed:
            result.append(meta | {'raw_user_text': '\n\n'.join(prompt),
                                  'assistant_text': '\n\n'.join(replies), 'attachments': []})
    for row in rows:
        if row.get('isSidechain') or row.get('isMeta'):
            continue
        msg = row.get('message') or {}
        if not isinstance(msg, dict):
            continue
        content = msg.get('content')
        if row.get('type') == 'user':
            if isinstance(content, list) and any(isinstance(x, dict) and x.get('type') == 'tool_result' for x in content):
                continue
            text = text_content(content)
            if not text.strip():
                continue
            if completed:
                finish()
                prompt, replies, completed = [], [], False
            prompt.append(text)
            meta = {'source': 'claude', 'surface': 'claude-code',
                    'kb_ref': row.get('sessionId'), 'cwd': row.get('cwd'),
                    'timestamp': row.get('timestamp'), 'model': meta.get('model')}
        elif row.get('type') == 'assistant' and prompt:
            text = text_content(content)
            if text:
                replies.append(text)
            if msg.get('model'):
                meta['model'] = msg['model']
            if msg.get('stop_reason') in ('end_turn', 'stop_sequence'):
                completed = True
    finish()
    return result


def parse_codex(rows):
    useful = []
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get('payload', {}), dict):
            continue
        payload = row.get('payload', {})
        kind = payload.get('type')
        if row.get('type') in ('session_meta', 'turn_context'):
            useful.append(row)
        elif row.get('type') == 'event_msg' and kind in ('user_message', 'task_complete', 'task_finished', 'turn_aborted', 'task_aborted'):
            useful.append(row)
        elif row.get('type') == 'event_msg' and kind == 'item_completed' and isinstance(payload.get('item'), dict) and payload['item'].get('type') in ('UserMessage', 'AgentMessage'):
            useful.append(row)
        elif row.get('type') == 'response_item' and kind == 'message' and payload.get('role') in ('user', 'assistant'):
            useful.append(row)
    rows = useful
    meta = next((r.get('payload', {}) for r in rows if r.get('type') == 'session_meta'), {})
    source = meta.get('source') or meta.get('thread_source')
    if isinstance(source, dict) or source in ('subagent', 'cloud'):
        return []
    surface = 'codex-desktop' if 'desktop' in str(meta.get('originator', '')).lower() else 'codex-cli'
    base = {'source': 'codex', 'surface': surface,
            'kb_ref': meta.get('id') or meta.get('session_id'), 'cwd': meta.get('cwd')}
    modern = any(r.get('type') == 'event_msg' and r.get('payload', {}).get('type') == 'item_completed'
                 and r.get('payload', {}).get('item', {}).get('type') == 'UserMessage' for r in rows)
    event_users = any(r.get('type') == 'event_msg' and r.get('payload', {}).get('type') == 'user_message' for r in rows)
    prompt, replies, result = [], [], []
    model, cwd, stamp = None, base['cwd'], None
    for row in rows:
        payload = row.get('payload') or {}
        if not isinstance(payload, dict):
            continue
        kind = payload.get('type')
        if row.get('type') == 'turn_context':
            model, cwd = payload.get('model') or model, payload.get('cwd') or cwd
        if modern and row.get('type') == 'event_msg' and kind == 'item_completed':
            item = payload.get('item') or {}
            if item.get('type') == 'UserMessage':
                text = text_content(item.get('content'))
                if text.strip():
                    prompt.append(text)
                    stamp = stamp or row.get('timestamp')
            elif item.get('type') == 'AgentMessage' and item.get('phase') in ('commentary', 'final_answer', 'final'):
                text = text_content(item.get('content'))
                if text and prompt:
                    replies.append(text)
        elif not modern:
            if row.get('type') == 'event_msg' and kind == 'user_message':
                text = payload.get('message')
                if isinstance(text, str) and text.strip():
                    prompt.append(text)
                    stamp = stamp or row.get('timestamp')
            elif row.get('type') == 'response_item' and kind == 'message':
                role = payload.get('role')
                kinds = (payload.get('internal_chat_message_metadata_passthrough') or {}).get('content_item_kinds', [])
                if role == 'user' and not event_users and ('user.text' in kinds or not kinds):
                    text = text_content(payload.get('content'))
                    # Legacy environment/instruction records are not user prompts.
                    if text.strip() and not text.startswith(('# AGENTS.md instructions', '<environment_context>')):
                        prompt.append(text)
                        stamp = stamp or row.get('timestamp')
                elif role == 'assistant' and payload.get('channel') in ('commentary', 'final') and prompt:
                    text = text_content(payload.get('content'))
                    if text:
                        replies.append(text)
        if row.get('type') == 'event_msg' and kind in ('task_complete', 'task_finished'):
            if prompt and replies:
                result.append(base | {'cwd': cwd, 'timestamp': stamp, 'model': model,
                                      'raw_user_text': '\n\n'.join(prompt),
                                      'assistant_text': '\n\n'.join(replies), 'attachments': []})
            prompt, replies, stamp = [], [], None
        elif row.get('type') == 'event_msg' and kind in ('turn_aborted', 'task_aborted'):
            prompt, replies, stamp = [], [], None
    return result


def excluded(cwd, config):
    return any(fnmatch.fnmatchcase(str(cwd or ''), pattern) for pattern in config.get('excluded_projects', []))


def turn_key(turn):
    fields = {k: turn.get(k) for k in ('source', 'raw_user_text', 'assistant_text', 'kb_ref', 'attachments')}
    return hashlib.sha256(json.dumps(fields, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def rpc_decode(raw):
    text = raw.decode('utf-8')
    try:
        return json.loads(text)
    except ValueError:
        # Streamable HTTP may return SSE rather than application/json.
        for block in text.replace('\r\n', '\n').split('\n\n'):
            data = '\n'.join(line[5:].lstrip() for line in block.splitlines() if line.startswith('data:'))
            if data:
                value = json.loads(data)
                if 'result' in value or 'error' in value:
                    return value
    raise ValueError('No JSON-RPC result')


class McpClient:
    def __init__(self, token, opener=urlopen):
        self.token, self.opener, self.session = token, opener, None

    def request(self, method, params, request_id=None):
        data = {'jsonrpc': '2.0', 'method': method, 'params': params}
        if request_id is not None:
            data['id'] = request_id
        headers = {'Authorization': 'Bearer ' + self.token, 'Content-Type': 'application/json',
                   'Accept': 'application/json, text/event-stream'}
        if self.session:
            headers['Mcp-Session-Id'] = self.session
            headers['MCP-Protocol-Version'] = '2025-03-26'
        req = Request(ENDPOINT, json.dumps(data).encode(), headers, method='POST')
        with self.opener(req, timeout=20) as response:
            session = response.headers.get('Mcp-Session-Id')
            if session:
                self.session = session
            raw = response.read(2_000_000)
        return rpc_decode(raw) if request_id is not None else None

    def initialise(self):
        value = self.request('initialize', {'protocolVersion': '2025-03-26', 'capabilities': {},
                             'clientInfo': {'name': 'kbs-local-capture', 'version': VERSION}}, 1)
        if value.get('error') or not self.session:
            raise ValueError('MCP initialise failed')
        self.request('notifications/initialized', {})

    def capture(self, turn):
        args = {k: v for k, v in turn.items() if k not in ('cwd', 'timestamp') and v is not None}
        value = self.request('tools/call', {'name': 'capture_chat_turn', 'arguments': args}, 2)
        result = value.get('result') or {}
        if value.get('error') or result.get('isError') or (result.get('structuredContent') or {}).get('status') != 'queued':
            raise ValueError('Capture was not queued')
        return result['structuredContent'].get('capture_id')


def log_failure(data, kind):
    # Never log exceptions containing headers, tokens, transcript text or bodies.
    with (data / 'capture.log').open('a', encoding='utf-8') as out:
        out.write(datetime.now(timezone.utc).isoformat() + ' FAILED ' + kind + '\n')


def send_turns(turns, config, data, client):
    with sqlite3.connect(data / 'state.sqlite3', timeout=0.1) as db:
        db.execute('CREATE TABLE IF NOT EXISTS sent (turn_hash TEXT PRIMARY KEY, capture_id TEXT, sent_at TEXT)')
        for turn in turns:
            if excluded(turn.get('cwd'), config):
                continue
            if not turn.get('kb_ref') or len(turn['kb_ref']) > 64 or not turn.get('cwd'):
                continue
            if config.get('capture_from'):
                try:
                    stamp = datetime.fromisoformat(str(turn.get('timestamp') or '').replace('Z', '+00:00'))
                    boundary = datetime.fromisoformat(config['capture_from'].replace('Z', '+00:00'))
                    if stamp.tzinfo is None or boundary.tzinfo is None or stamp < boundary:
                        continue
                except ValueError:
                    continue
            if any(not turn.get(k) or len(turn[k]) > 100_000 for k in ('raw_user_text', 'assistant_text')):
                log_failure(data, 'turn-size')
                continue
            key = turn_key(turn)
            # Serialize workers across hooks and sweeps; server dedupe covers lost receipts.
            db.execute('BEGIN IMMEDIATE')
            try:
                if db.execute('SELECT 1 FROM sent WHERE turn_hash=?', (key,)).fetchone():
                    db.rollback()
                    continue
                capture_id = client.capture(turn)
                db.execute('INSERT INTO sent VALUES (?, ?, ?)', (key, capture_id, datetime.now(timezone.utc).isoformat()))
                db.commit()
            except Exception:
                db.rollback()
                raise


def run_worker(args):
    data = Path(args.data).expanduser()
    data.mkdir(parents=True, exist_ok=True, mode=0o700)
    try:
        config = json.loads((data / 'config.json').read_text())
        token = subprocess.run(['/usr/bin/security', 'find-generic-password', '-s', KEYCHAIN_SERVICE,
                                '-a', config['keychain_account'], '-w'], capture_output=True, text=True,
                               check=True, timeout=10).stdout.strip()
        if not token:
            raise ValueError('Missing token')
        client = McpClient(token)
        client.initialise()
        roots = {'claude': [Path.home()/'.claude/projects'],
                 'codex': [Path.home()/'.codex/sessions', Path.home()/'.codex/archived_sessions']}
        if args.path:
            paths = [(args.source, Path(args.path).expanduser())]
        else:
            cutoff = datetime.fromisoformat(config['capture_from']).timestamp()
            paths = [(source, path) for source, dirs in roots.items() for root in dirs
                     for path in root.rglob('*.jsonl') if path.stat().st_mtime >= cutoff]
        for source, path in paths:
            # Never accept arbitrary file paths from a malformed hook.
            if not any(path.resolve().is_relative_to(root.resolve()) for root in roots[source]):
                continue
            if 'subagents' in path.parts:
                continue
            try:
                parser = parse_claude if source == 'claude' else parse_codex
                send_turns(parser(records(path)), config, data, client)
            except Exception as exc:
                log_failure(data, type(exc).__name__)
    except Exception as exc:
        log_failure(data, type(exc).__name__)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', action='version', version=json.dumps(version_info(), sort_keys=True))
    parser.add_argument('mode', choices=['hook', 'worker', 'sweep'])
    parser.add_argument('--source', choices=['claude', 'codex'])
    parser.add_argument('--path')
    parser.add_argument('--data', default=str(DATA))
    args = parser.parse_args()
    os.umask(0o077)
    if args.mode == 'hook':
        try:
            event = json.loads(sys.stdin.read(65536))
            if event.get('hook_event_name') not in ('Stop', 'SessionEnd') or not event.get('transcript_path'):
                return
            subprocess.Popen([sys.executable, str(Path(__file__).resolve()), 'worker', '--source', args.source,
                              '--path', event['transcript_path'], '--data', args.data],
                             stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                             start_new_session=True, close_fds=True)
        except Exception:
            pass
    else:
        run_worker(args)


if __name__ == '__main__':
    main()
