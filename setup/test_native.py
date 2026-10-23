"""Native store round trips and boundary tests, using isolated homes/projects."""
import copy
import json
import os
from pathlib import Path
import stat
import tempfile
import tomllib
import unittest
from unittest.mock import patch

import native as n
from reconcile import render_block


class NativeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name) / 'home'
        self.project = Path(self.tmp.name) / 'project'
        self.home.mkdir()
        self.project.mkdir()
        (self.project / '.git').mkdir()
        self.env = patch.dict(os.environ)
        self.env.start()
        self.addCleanup(self.env.stop)
        os.environ.pop('CLAUDE_CONFIG_DIR', None)

    def write(self, path, content):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)

    def inspect(self, surface='codex-cli', execution='local'):
        return n.inspect(surface, execution, self.home, self.project)

    def desired(self, name='new_kb', url='https://kb.example/mcp'):
        return [{'connection_id': name, 'url': url}]

    def test_codex_surgical_addition_preserves_headers_hooks_and_notify(self):
        p = self.home / '.codex/config.toml'
        original = '# Personal notes\nnotify = ["my-notifier"]\n[hooks]\nstate = { enabled = true }\n[mcp_servers.old]\nurl = "https://old.example/mcp"\nhttp_headers = { Authorization = "PRIVATE" }\n'
        self.write(p, original)
        p.chmod(0o640)
        observed = self.inspect()
        self.assertNotIn('PRIVATE', json.dumps(observed))
        proposal = n.plan(observed, desired=self.desired())
        result = n.apply(proposal)
        self.assertEqual(result['status'], 'saved_and_reread')
        self.assertTrue(p.read_text().startswith(original))
        self.assertEqual(tomllib.loads(p.read_text())['mcp_servers']['new_kb']['url'], 'https://kb.example/mcp')
        self.assertEqual(Path(result['backup']).read_text(), original)
        self.assertEqual(stat.S_IMODE(Path(result['backup']).stat().st_mode), 0o600)
        self.assertEqual(stat.S_IMODE(p.stat().st_mode), 0o640)

    def test_repeat_setup_reuses_configured_endpoint_and_is_noop(self):
        first = n.plan(self.inspect(), desired=self.desired())
        n.apply(first)
        repeated = n.plan(self.inspect(), desired=self.desired('different_alias'))
        self.assertEqual(repeated['additions'], [])
        before = list(self.home.rglob('*'))
        self.assertEqual(n.apply(repeated)['status'], 'unchanged')
        self.assertEqual(before, list(self.home.rglob('*')))

    def test_same_name_different_resource_refuses_replacement(self):
        self.write(self.home / '.codex/config.toml', '[mcp_servers.new_kb]\nurl="https://old.example/mcp"\n')
        with self.assertRaises(n.SetupError):
            n.plan(self.inspect(), desired=self.desired())

    def test_codex_project_layers_are_inspected_before_user_addition(self):
        self.write(self.project / '.codex/config.toml', '[mcp_servers.project_kb]\nurl="https://kb.example/mcp"\n')
        p = n.plan(self.inspect(), desired=self.desired())
        self.assertEqual(p['additions'], [])
        self.assertEqual(n.apply(p)['status'], 'unchanged')
        self.assertFalse((self.home / '.codex/config.toml').exists())

    def test_codex_custom_config_home_is_explicit(self):
        custom = self.home / 'custom'
        observed = n.inspect('codex-desktop', 'local', self.home, self.project, custom)
        n.apply(n.plan(observed, desired=self.desired()))
        self.assertTrue((custom / 'config.toml').exists())
        self.assertFalse((self.home / '.codex/config.toml').exists())

    def test_claude_user_project_and_local_stores_round_trip(self):
        for scope in ('user', 'project', 'local'):
            with self.subTest(scope=scope):
                proposal = n.plan(self.inspect('claude-code-cli'), scope, self.desired('server_' + scope, 'https://' + scope + '.example/mcp'))
                self.assertEqual(n.apply(proposal)['status'], 'saved_and_reread')
        profile = json.loads((self.home / '.claude.json').read_text())
        self.assertIn('server_user', profile['mcpServers'])
        self.assertIn('server_local', profile['projects'][str(self.project)]['mcpServers'])
        self.assertIn('server_project', json.loads((self.project / '.mcp.json').read_text())['mcpServers'])
        self.assertEqual(len(self.inspect('claude-code-desktop')['connections']), 3)

    def test_claude_preserves_unrelated_settings_and_private_auth(self):
        p = self.home / '.claude.json'
        original = {'theme': 'dark', 'oauthAccount': {'private': 'PRIVATE'},
                    'projects': {str(self.project): {'trust': True}},
                    'mcpServers': {'old': {'type': 'http', 'url': 'https://old.example/mcp', 'headers': {'Authorization': 'PRIVATE'}}}}
        self.write(p, json.dumps(original))
        observed = self.inspect('claude-code-cli')
        self.assertNotIn('PRIVATE', json.dumps(observed))
        n.apply(n.plan(observed, desired=self.desired()))
        saved = json.loads(p.read_text())
        del saved['mcpServers']['new_kb']
        self.assertEqual(saved, original)

    def plugin(self):
        root = self.home / '.claude/plugins/cache/market/kbs/1.3.4'
        self.write(root / '.mcp.json', json.dumps({'mcpServers': {'bundled': {'type': 'http', 'url': 'https://kb.example/mcp'}}}))
        self.write(root / '.claude-plugin/plugin.json', '{"name":"kbs","version":"1.3.4"}')
        self.write(self.home / '.claude/settings.json', '{"enabledPlugins":{"kbs@market":true}}')
        self.write(self.home / '.claude/plugins/installed_plugins.json', json.dumps({'plugins': {'kbs@market': [{'scope': 'user', 'installPath': str(root), 'version': '1.3.4'}]}}))
        return root

    def test_enabled_plugin_server_is_reused(self):
        self.plugin()
        observed = self.inspect('claude-code-cli')
        self.assertEqual(observed['connections'][0]['source'], 'plugin:kbs@market')
        p = n.plan(observed, desired=self.desired())
        self.assertEqual(p['additions'], [])
        self.assertEqual(n.apply(p)['status'], 'unchanged')
        self.assertFalse((self.home / '.claude.json').exists())

    def test_plugin_disabled_by_project_is_not_treated_as_enabled(self):
        self.plugin()
        self.write(self.project / '.claude/settings.local.json', '{"enabledPlugins":{"kbs@market":false}}')
        self.assertEqual(self.inspect('claude-code-cli')['connections'], [])

    def test_unresolved_enabled_plugin_blocks_new_connection(self):
        self.write(self.home / '.claude/settings.json', '{"enabledPlugins":{"kbs@market":true}}')
        with self.assertRaises(n.SetupError):
            n.plan(self.inspect('claude-code-cli'), desired=self.desired())

    def test_cloud_or_unknown_execution_cannot_write_local_settings(self):
        for surface in n.CODE:
            for execution in ('cloud', 'unknown'):
                with self.assertRaises(n.SetupError):
                    n.plan(self.inspect(surface, execution), desired=self.desired())
        self.assertEqual(list(self.home.iterdir()), [])

    def test_stale_plan_and_unrelated_concurrent_edit_are_refused(self):
        proposal = n.plan(self.inspect(), desired=self.desired())
        self.write(self.home / '.codex/config.toml', 'model = "changed"\n')
        with self.assertRaises(n.SetupError):
            n.apply(proposal)
        self.assertNotIn('new_kb', (self.home / '.codex/config.toml').read_text())

    def test_plugin_changes_invalidate_plan(self):
        root = self.plugin()
        proposal = n.plan(self.inspect('claude-code-cli'), desired=self.desired('new', 'https://new.example/mcp'))
        self.write(root / '.mcp.json', '{"mcpServers":{}}')
        with self.assertRaises(n.SetupError):
            n.apply(proposal)

    def test_managed_instructions_preserve_unrelated_text(self):
        p = self.home / '.codex/AGENTS.md'
        self.write(p, 'Other rules\n')
        block = render_block('codex-cli', 'local', [])
        proposal = n.plan(self.inspect(), block=block)
        n.apply(proposal)
        self.assertTrue(p.read_text().startswith('Other rules\n'))
        self.assertEqual(n.apply(n.plan(self.inspect(), block=block))['status'], 'unchanged')

    def test_personal_claude_instructions_have_separate_approval_gate(self):
        block = render_block('claude-code-cli', 'local', [])
        proposal = n.plan(self.inspect('claude-code-cli'), block=block)
        with self.assertRaises(n.SetupError):
            n.apply(proposal)
        self.assertFalse((self.home / '.claude/CLAUDE.md').exists())
        self.assertEqual(n.apply(proposal, personal_claude_approved=True)['status'], 'saved_and_reread')

    def test_malformed_settings_cannot_be_overwritten(self):
        self.write(self.home / '.codex/config.toml', 'http_headers = { "PRIVATE')
        with self.assertRaises(n.SetupError) as error:
            self.inspect()
        self.assertNotIn('PRIVATE', str(error.exception))

    def test_symlink_writes_are_refused(self):
        source = self.home / 'source.toml'
        source.write_text('')
        p = self.home / '.codex/config.toml'
        p.parent.mkdir()
        p.symlink_to(source)
        with self.assertRaises(n.SetupError):
            n.apply(n.plan(self.inspect(), desired=self.desired()))
        self.assertEqual(source.read_text(), '')

    def test_incompatible_inline_toml_layout_is_not_reformatted(self):
        p = self.home / '.codex/config.toml'
        self.write(p, 'mcp_servers = {}\n')
        with self.assertRaises(ValueError):
            n.apply(n.plan(self.inspect(), desired=self.desired()))
        self.assertEqual(p.read_text(), 'mcp_servers = {}\n')

    def test_endpoint_secrets_are_not_printed_or_accepted(self):
        p = self.home / '.codex/config.toml'
        self.write(p, '[mcp_servers.existing]\nurl="https://user:PRIVATE@kb.example/mcp?token=PRIVATE"\n')
        self.assertNotIn('PRIVATE', json.dumps(self.inspect()))
        with self.assertRaises(n.SetupError):
            n.plan(self.inspect(), desired=self.desired(url='https://kb.example/mcp?token=PRIVATE'))

    def test_tampered_plan_cannot_write_an_arbitrary_target(self):
        proposal = n.plan(self.inspect(), desired=self.desired())
        proposal['target'] = str(self.home / 'unrelated.txt')
        with self.assertRaises(n.SetupError):
            n.apply(proposal)
        self.assertFalse((self.home / 'unrelated.txt').exists())

    def test_disabled_existing_server_is_not_silently_enabled_or_duplicated(self):
        self.write(self.home / '.codex/config.toml', '[mcp_servers.kb]\nurl="https://kb.example/mcp"\nenabled=false\n')
        with self.assertRaises(n.SetupError):
            n.plan(self.inspect(), desired=self.desired())

    def test_existing_writer_lock_is_preserved(self):
        p = self.home / '.codex/config.toml'
        self.write(p, '')
        lock = p.with_name(p.name + '.kbs-setup.lock')
        lock.write_text('other writer')
        with self.assertRaises(n.SetupError):
            n.apply(n.plan(self.inspect(), desired=self.desired()))
        self.assertEqual(lock.read_text(), 'other writer')
        self.assertEqual(p.read_text(), '')


if __name__ == '__main__':
    unittest.main()
