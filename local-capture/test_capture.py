"""Fixture tests for defensive extraction, retries, MCP handshake and installation."""
import importlib.util
import io
from contextlib import redirect_stderr
import json
from pathlib import Path
import tempfile
import subprocess
import sys
import unittest
from unittest.mock import patch


def module(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(name + '.py'))
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


capture = module('capture')
install = module('install')


def event(kind, **kwargs):
    return {'type': 'event_msg', 'timestamp': '2026-10-12T14:00:00Z', 'payload': {'type': kind, **kwargs}}


class CaptureTests(unittest.TestCase):
    def test_version_is_read_only_and_reports_actual_collector_source(self):
        result = subprocess.run([sys.executable, '-B', str(Path(capture.__file__)), '--version'],
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        info = json.loads(result.stdout)
        self.assertEqual(info, capture.version_info())
        self.assertTrue(info['build_id'].startswith('sha256:'))

    def test_codex_modern_uses_visible_items_only_and_holds_incomplete(self):
        rows = [
            {'type': 'unknown', 'payload': []},
            {'type': 'session_meta', 'payload': {'id': 'thread', 'cwd': '/project', 'originator': 'codex_desktop'}},
            {'type': 'turn_context', 'payload': {'model': 'gpt-model'}},
            {'type': 'response_item', 'payload': {'role': 'user', 'type': 'message', 'content': [{'type': 'input_text', 'text': 'injected file'}]}},
            event('item_completed', item={'type': 'UserMessage', 'content': [{'type': 'text', 'text': 'Prompt'}]}),
            event('item_completed', item={'type': 'Reasoning', 'raw_content': 'secret'}),
            event('item_completed', item={'type': 'CommandExecution', 'stdout': 'secret'}),
            event('item_completed', item={'type': 'AgentMessage', 'phase': 'commentary', 'content': [{'type': 'text', 'text': 'Progress'}]}),
            event('item_completed', item={'type': 'AgentMessage', 'phase': 'final_answer', 'content': [{'type': 'text', 'text': 'Reply'}]}),
            event('task_complete'),
            event('item_completed', item={'type': 'UserMessage', 'content': [{'type': 'text', 'text': 'Still running'}]}),
        ]
        (turn,) = capture.parse_codex(rows)
        self.assertEqual(turn['raw_user_text'], 'Prompt')
        self.assertEqual(turn['assistant_text'], 'Progress\n\nReply')
        self.assertEqual(turn['surface'], 'codex-desktop')
        self.assertEqual(turn['model'], 'gpt-model')
        self.assertEqual(capture.parse_codex([rows[1] | {'payload': rows[1]['payload'] | {'source': {'subagent': 'id'}}}] + rows[2:]), [])

    def test_codex_legacy_does_not_duplicate_response_users(self):
        rows = [{'type': 'session_meta', 'payload': {'id': 'id', 'cwd': '/project'}},
                event('user_message', message='Prompt'),
                {'type': 'response_item', 'payload': {'type': 'message', 'role': 'user', 'content': 'Prompt'}},
                {'type': 'response_item', 'payload': {'type': 'message', 'role': 'assistant', 'channel': 'analysis', 'content': 'hidden'}},
                {'type': 'response_item', 'payload': {'type': 'message', 'role': 'assistant', 'channel': 'final', 'content': 'Reply'}},
                event('task_complete')]
        (turn,) = capture.parse_codex(rows)
        self.assertEqual(turn['raw_user_text'], 'Prompt')
        self.assertEqual(turn['assistant_text'], 'Reply')
        self.assertEqual(capture.parse_codex(rows[:-1] + [event('turn_aborted')]), [])

    def test_claude_ignores_tools_sidechains_and_incomplete(self):
        user = {'type': 'user', 'sessionId': 'session', 'cwd': '/project', 'timestamp': '2026-10-12T14:00:00Z',
                'message': {'content': 'Prompt'}}
        rows = [user, {'type': 'assistant', 'message': {'model': 'claude-model', 'stop_reason': 'tool_use',
                'content': [{'type': 'text', 'text': 'Progress'}, {'type': 'thinking', 'thinking': 'secret'}, {'type': 'tool_use', 'input': 'secret'}]}},
                user | {'message': {'content': [{'type': 'tool_result', 'content': 'secret'}, {'type': 'text', 'text': 'also hidden'}]}},
                user | {'isSidechain': True},
                {'type': 'assistant', 'message': {'model': 'claude-model', 'stop_reason': 'end_turn', 'content': [{'type': 'text', 'text': 'Reply'}]}},
                user | {'message': {'content': 'Next prompt'}}]
        (turn,) = capture.parse_claude(rows)
        self.assertEqual(turn['raw_user_text'], 'Prompt')
        self.assertEqual(turn['assistant_text'], 'Progress\n\nReply')

    def test_claude_drops_app_notices_summaries_and_app_events(self):
        base = {'type': 'user', 'sessionId': 'session', 'cwd': '/project', 'timestamp': '2026-10-12T14:00:00Z'}
        def user(content, **flags):
            return base | {'message': {'content': content}} | flags
        def reply(text):
            return {'type': 'assistant', 'message': {'model': 'claude-model', 'stop_reason': 'end_turn',
                                                     'content': [{'type': 'text', 'text': text}]}}
        notice = '<system-reminder>\nSession status: done\n</system-reminder>'
        rows = [
            # A notice block before the typed text, and an inline notice.
            user([{'type': 'text', 'text': notice}, {'type': 'text', 'text': 'Prompt ' + notice + 'here'}],
                 origin={'kind': 'human'}),
            # A notice-only row mid-turn neither starts nor ends the turn.
            user(notice),
            reply('Reply'),
            # App events after a finished turn end it; the replies to them are dropped.
            user('<task-notification>done</task-notification>', origin={'kind': 'task-notification'}),
            reply('Unprompted reply'),
            user(notice),
            reply('Another unprompted reply'),
            user('This session is being continued from a previous conversation.',
                 isCompactSummary=True, isVisibleInTranscriptOnly=True),
            reply('Resuming'),
            user('Second prompt'),
            reply('Second reply'),
            # A screenshot sent without text is still a turn of its own.
            user([{'type': 'image', 'source': {'data': 'secret'}}], origin={'kind': 'human'}),
            user('[Image: source: /tmp/shot.png]', isMeta=True),
            reply('Image reply'),
        ]
        first, second, third = capture.parse_claude(rows)
        self.assertEqual(first['raw_user_text'], 'Prompt here')
        self.assertEqual(first['assistant_text'], 'Reply')
        self.assertEqual(second['raw_user_text'], 'Second prompt')
        self.assertEqual(second['assistant_text'], 'Second reply')
        self.assertEqual(third['raw_user_text'], '[Image not captured]')
        self.assertEqual(third['assistant_text'], 'Image reply')

    def test_sends_only_after_success_and_deduplicates_replays(self):
        turn = {'source': 'codex', 'raw_user_text': 'Prompt', 'assistant_text': 'Reply', 'kb_ref': 'session', 'cwd': '/project'}
        class Client:
            calls = 0
            fail = True
            def capture(self, turn):
                self.calls += 1
                if self.fail:
                    raise ValueError('offline')
                return 'cap_1'
        client = Client()
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp)
            with self.assertRaises(ValueError):
                capture.send_turns([turn], {}, data, client)
            client.fail = False
            capture.send_turns([turn], {}, data, client)
            capture.send_turns([turn], {}, data, client)
            self.assertEqual(client.calls, 2)
            capture.send_turns([turn | {'kb_ref': 'other'}], {'excluded_projects': ['/project*']}, data, client)
            self.assertEqual(client.calls, 2)
            with capture.sqlite3.connect(data / 'state.sqlite3') as db:
                self.assertNotIn('Prompt', str(db.execute('SELECT * FROM sent').fetchall()))

    def test_mcp_session_header_sse_and_queued_validation(self):
        requests = []
        class Response:
            def __init__(self, body, headers): self.body, self.headers = body, headers
            def __enter__(self): return self
            def __exit__(self, *args): pass
            def read(self, n): return self.body
        def opener(req, timeout):
            value = json.loads(req.data); requests.append((value, dict(req.header_items())))
            if value['method'] == 'initialize':
                self.assertEqual(value['params']['clientInfo']['version'], capture.VERSION)
                return Response(b'{"result": {}}', {'Mcp-Session-Id': 'session-header'})
            if value['method'] == 'notifications/initialized': return Response(b'', {})
            return Response(b'event: message\ndata: {"result":{"structuredContent":{"status":"queued","capture_id":"cap"}}}\n\n', {})
        client = capture.McpClient('fake-test-token', opener)
        client.initialise()
        self.assertEqual(client.capture({'source': 'codex', 'cwd': '/private', 'timestamp': 'now', 'raw_user_text': 'Prompt'}), 'cap')
        self.assertEqual(requests[2][1]['Mcp-session-id'], 'session-header')
        self.assertNotIn('cwd', requests[2][0]['params']['arguments'])

    def test_cli_rejects_unsupported_platforms_before_writing_files(self):
        for platform in ("win32", "linux"):
            with self.subTest(platform=platform), tempfile.TemporaryDirectory() as tmp:
                home = Path(tmp) / "unwritten-home"
                with patch.object(install.sys, "platform", platform), patch.object(install.sys, "argv", ["install.py", "--account", "test@example.com", "--home", str(home)]), redirect_stderr(io.StringIO()) as stderr:
                    with self.assertRaises(SystemExit) as error:
                        install.main()
                self.assertEqual(error.exception.code, 2)
                self.assertIn("supports macOS only", stderr.getvalue())
                self.assertFalse(home.exists())

    def test_installer_is_idempotent_preserves_notify_hooks_and_policy(self):
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            (home/'.codex').mkdir()
            config = home/'.codex/config.toml'
            config.write_text('notify = ["computer-use"]\n[[hooks.Stop]]\n[[hooks.Stop.hooks]]\ntype="command"\ncommand="existing"\n')
            (home/'.claude').mkdir()
            (home/'.claude/settings.json').write_text('{"permissions":{"allow":["Read"]},"note":"a \u2014 b"}', encoding='utf-8')
            policy = install.install(home, 'test@example.com')
            initial = config.read_text()
            collector_policy = json.loads(policy.read_text()) | {'excluded_projects': ['/private/*']}
            policy.write_text(json.dumps(collector_policy))
            install.install(home, 'test@example.com')
            self.assertEqual(config.read_text(), initial)
            self.assertIn('computer-use', initial)
            self.assertIn('command="existing"', initial)
            self.assertEqual(json.loads(policy.read_text())['excluded_projects'], ['/private/*'])
            self.assertEqual(json.loads((home/'.claude/settings.json').read_text())['permissions'], {'allow': ['Read']})
            self.assertIn('a \u2014 b', (home/'.claude/settings.json').read_text(encoding='utf-8'))
            self.assertEqual(len(install.tomllib.loads(initial)['hooks']['Stop']), 2)

    def test_codex_rewrite_without_end_marker_is_updated_in_place(self):
        old = '/usr/bin/python3 /home/.local/share/kbs-capture/capture.py hook --source codex'
        new = '/opt/python3.12 /home/.local/share/kbs-capture/capture.py hook --source codex'
        def entry(event, command):
            return (f'[[hooks.{event}]]\n[[hooks.{event}.hooks]]\ntype = "command"\n'
                    f'command = "{command}"\ntimeout = 3\n')
        # As Codex leaves it after the user trusts the hooks: END marker gone,
        # trust records and other tables after the block.
        rewritten = ('notify = ["computer-use"]\n\n# BEGIN kbs-local-capture\n'
                     + entry('Stop', old) + '\n' + entry('SessionEnd', old)
                     + '\n[hooks.state."config.toml:stop:0:0"]\ntrusted_hash = "sha256:abc"\n\n'
                     + '[mcp_servers.kb]\nurl = "https://kb.example/mcp"\n')
        result = install.codex_config(rewritten, new)
        self.assertEqual(result, rewritten.replace(old, new))
        self.assertEqual(install.codex_config(result, new), result)
        # Without either marker, existing entries are still found rather than duplicated.
        unmarked = rewritten.replace('# BEGIN kbs-local-capture\n', '')
        self.assertEqual(install.codex_config(unmarked, new), unmarked.replace(old, new))

    def test_codex_unrecognised_capture_entry_fails_closed(self):
        # A reformatted entry is not recognised; adding a second would duplicate it.
        reformatted = ('[[hooks.Stop]]\n[[hooks.Stop.hooks]]\ntype="command"\n'
                       'command="python3 /h/.local/share/kbs-capture/capture.py hook --source codex"\n')
        with self.assertRaises(ValueError):
            install.codex_config(reformatted, 'python3 /h/.local/share/kbs-capture/capture.py hook --source codex')


if __name__ == '__main__':
    unittest.main()
