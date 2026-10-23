"""Setup behavioural checks: client boundaries, evidence, outages and preservation."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('reconcile', Path(__file__).with_name('reconcile.py'))
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)


def evidence(surface='codex-desktop', execution='local', os_name='macos'):
    return {'target': {'surface': surface, 'execution': execution, 'os': os_name},
            'connections': [{'kb_uid': 'kb-1', 'service_id': 'service-1', 'connection_id': 'connection-1',
                             'name': 'Example KB', 'type': 'personal', 'domain': 'Test context',
                             'kb_protocol_version': 1, 'capabilities': ['wiki', 'rag'],
                             'access': 'verified', 'wiki_read': 'verified'}]}


class ReconcileTests(unittest.TestCase):
    def test_local_supported_capture_is_independent(self):
        e = evidence()
        self.assertEqual(r.evaluate(e)['retrieval'], 'verified')
        self.assertEqual(r.evaluate(e)['capture'], 'not_verified')
        e['capture_verified'] = True
        self.assertEqual(r.evaluate(e)['capture'], 'verified')

    def test_cloud_desktop_and_chat_never_inherit_capture(self):
        for surface, execution in [(s, 'cloud') for s in r.CODE] + [('chatgpt', 'local'), ('claude-chat', 'local')] + [(s, 'unknown') for s in r.CODE]:
            with self.subTest(surface=surface, execution=execution):
                e = evidence(surface, execution)
                e['capture_verified'] = True  # Old local receipts must be ignored.
                out = r.evaluate(e)
                self.assertEqual(out['capture'], 'not_applicable')
                self.assertEqual(out['retrieval'], 'verified')
                self.assertNotIn('External local session-history', out['managed_block'])

    def test_every_local_code_surface_and_unsupported_os(self):
        for surface in r.CODE:
            self.assertEqual(r.evaluate(evidence(surface))['capture'], 'not_verified')
            for os_name in ('windows', 'linux', 'wsl', 'unknown'):
                out = r.evaluate(evidence(surface, os_name=os_name))
                self.assertEqual(out['capture'], 'unsupported')
                self.assertEqual(out['retrieval'], 'verified')

    def test_open_webui_does_not_get_a_second_loop(self):
        out = r.evaluate(evidence('open-webui'))
        self.assertIsNone(out['managed_block'])
        self.assertEqual(out['retrieval'], 'filter_owned')

    def test_successful_login_is_not_sufficient(self):
        e = evidence()
        e['connections'][0]['wiki_read'] = 'unknown'
        self.assertEqual(r.evaluate(e)['retrieval'], 'not_verified')
        e['connections'][0]['wiki_read'] = 'verified'
        e['connections'][0]['access'] = 'unknown'
        self.assertEqual(r.evaluate(e)['retrieval'], 'not_verified')

    def test_service_denial_cannot_be_overridden_by_inventory(self):
        for denied in ('access', 'wiki_read'):
            e = evidence()
            e['registry'] = {'status': 'verified', 'complete': True, 'knowledge_bases': copy.deepcopy(e['connections'])}
            e['connections'][0][denied] = 'denied'
            out = r.evaluate(e)
            self.assertEqual(out['retrieval'], 'not_verified')
            self.assertNotIn('"kb_uid": "kb-1"', out['managed_block'])

    def test_registry_failure_and_partial_response_preserve_configured_inventory(self):
        for status, complete in [('failed', True), ('denied', True), ('unknown', True), ('verified', False)]:
            e = evidence()
            e['registry'] = {'status': status, 'complete': complete, 'knowledge_bases': []}
            out = r.evaluate(e)
            self.assertEqual(out['retrieval'], 'verified')
            self.assertIn('"kb_uid": "kb-1"', out['managed_block'])
            self.assertEqual(out['connector_removals'], [])

    def test_complete_revocation_only_removes_managed_inventory(self):
        e = evidence()
        e['registry'] = {'status': 'verified', 'complete': True, 'knowledge_bases': []}
        out = r.evaluate(e)
        self.assertNotIn('"kb_uid": "kb-1"', out['managed_block'])
        self.assertEqual(out['connector_removals'], [])
        self.assertEqual(out['retrieval'], 'no_entitled_kbs')

    def test_missing_complete_registry_payload_cannot_erase_inventory(self):
        e = evidence()
        e['registry'] = {'status': 'verified', 'complete': True}
        with self.assertRaises(ValueError):
            r.evaluate(e)

    def test_new_entitlement_is_reported_missing_not_configured(self):
        e = evidence()
        kb = dict(e['connections'][0], kb_uid='kb-2', service_id='service-2')
        e['registry'] = {'status': 'verified', 'complete': True, 'knowledge_bases': [e['connections'][0], kb]}
        out = r.evaluate(e)
        self.assertEqual(out['missing_kb_uids'], ['kb-2'])
        self.assertEqual(out['retrieval'], 'not_verified')
        self.assertNotIn('service-2', out['managed_block'])

    def test_missing_connection_inventory_is_not_an_empty_inventory(self):
        e = evidence()
        del e['connections']
        with self.assertRaises(KeyError):
            r.evaluate(e)

    def test_uid_service_mismatch_is_not_accepted(self):
        e = evidence()
        e['registry'] = {'status': 'verified', 'complete': True, 'knowledge_bases': [dict(e['connections'][0], service_id='other')]}
        self.assertEqual(r.evaluate(e)['retrieval'], 'not_verified')

    def test_duplicates_keep_a_ready_connection_without_removing_either(self):
        e = evidence()
        e['connections'].append(dict(e['connections'][0], connection_id='bad-duplicate', access='denied'))
        out = r.evaluate(e)
        self.assertEqual(out['duplicate_kb_uids'], ['kb-1'])
        self.assertEqual(out['retrieval'], 'verified')
        self.assertIn('connection-1', out['managed_block'])
        self.assertNotIn('bad-duplicate', out['managed_block'])
        self.assertEqual(out['connector_removals'], [])

    def test_capture_policy_and_optional_build_do_not_gate_retrieval(self):
        e = evidence()
        e['connections'][0].update(capabilities=['wiki', 'build'], capture_policy='all_conversations')
        out = r.evaluate(e)
        self.assertEqual(out['retrieval'], 'verified')
        self.assertIn('build_guide_not_verified', out['connections'][0]['issues'])
        self.assertEqual(out['capture'], 'not_verified')

    def test_protocol_and_wiki_capability_are_required(self):
        for patch in [{'kb_protocol_version': 2}, {'capabilities': ['rag']}]:
            e = evidence()
            e['connections'][0].update(patch)
            self.assertEqual(r.evaluate(e)['retrieval'], 'not_verified')

    def test_exact_callback_scopes_resource_and_broker_diagnostics(self):
        observed = {'expected_callback': 'https://app.example/callback/actual_id',
                    'allowed_callbacks': ['https://app.example/callback/old_id'],
                    'required_scopes': ['read'], 'granted_scopes': [],
                    'expected_resource': 'service-a', 'observed_resource': 'service-b', 'broker_grant': 'denied'}
        self.assertEqual(set(r.oauth_diagnostics(observed)), {'callback_mismatch', 'missing_scopes', 'resource_mismatch', 'broker_grant_denied'})
        observed.update(allowed_callbacks=observed['allowed_callbacks'] + [observed['expected_callback']], granted_scopes=['read'], observed_resource='service-a', broker_grant='allowed')
        self.assertEqual(r.oauth_diagnostics(observed), [])
        self.assertIn('old_id', observed['allowed_callbacks'][0])

    def test_system_wiki_falls_back_unless_contract_is_complete(self):
        e = evidence()
        descriptor = {'service_id': 'mcp-service', 'account_id': 'account-1', 'system_wiki_protocol_version': 1,
                      'capabilities': ['system_wiki_read'], 'index_uri': 'system-wiki://index.md', 'content_revision': 'rev1'}
        self.assertEqual(r.evaluate(e)['guidance'], 'packaged_fallback')
        e['system_wiki'] = descriptor
        self.assertEqual(r.evaluate(e)['guidance'], 'declared_interface_static_instruction')
        self.assertEqual(r.evaluate(e)['startup_loading'], 'not_tested')
        for patch in [{'system_wiki_protocol_version': 2}, {'account_id': None}, {'account_id': {'bad': True}}, {'index_uri': 'wiki://index.md'}, {'capabilities': None}]:
            e['system_wiki'] = dict(descriptor, **patch)
            self.assertEqual(r.evaluate(e)['guidance'], 'packaged_fallback')

    def test_instruction_preservation_and_idempotence(self):
        block = r.evaluate(evidence())['managed_block']
        prefix, suffix = 'My unrelated rules\r\n', '\r\nOther project guidance\r\n'
        old = prefix + r.START + '\nOld managed rules\n' + r.END + suffix
        new = r.reconcile_block(old, block)
        self.assertTrue(new.startswith(prefix))
        self.assertTrue(new.endswith(suffix))
        self.assertEqual(r.reconcile_block(new, block), new)
        for old in ['', 'Existing rules', 'Existing rules\n', 'Existing rules\n\n']:
            new = r.reconcile_block(old, block)
            self.assertTrue(new.startswith(old))
            self.assertEqual(r.reconcile_block(new, block), new)

    def test_ambiguous_managed_instructions_are_refused(self):
        block = r.evaluate(evidence())['managed_block']
        for old in [r.START, r.END, block + block, r.END + r.START, '<!-- kbs-instructions v1 -->old' + r.END]:
            with self.assertRaises(ValueError):
                r.reconcile_block(old, block)

    def test_metadata_cannot_break_managed_block(self):
        for name in ['Example\n' + r.END, '<!-- kbs-instructions v2 -->', 'bad\x00name']:
            e = evidence()
            e['connections'][0]['name'] = name
            with self.assertRaises(ValueError):
                r.evaluate(e)

    def test_installation_diagnostics_do_not_remove_old_caches(self):
        e = evidence()
        e.update(source_version='1.3.4', installations=[{'active': True, 'version': '1.3.3', 'skills': []}, {'active': False, 'version': '1.2.1'}])
        out = r.evaluate(e)
        self.assertNotIn('multiple_active_installations', out['installation_issues'])
        e['installations'][1]['active'] = True
        self.assertIn('multiple_active_installations', r.evaluate(e)['installation_issues'])

    def test_cli_only_reads_inputs_and_never_echoes_unknown_secret_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            data = directory / 'evidence.json'
            text = directory / 'instructions.md'
            e = evidence(execution='cloud')
            e['target']['secret'] = 'DO_NOT_ECHO'
            data.write_text(json.dumps(e))
            text.write_text('Unrelated rules')
            before = {p.name: p.read_bytes() for p in directory.iterdir()}
            result = subprocess.run([sys.executable, str(Path(r.__file__)), str(data), '--instructions', str(text)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertNotIn('DO_NOT_ECHO', result.stdout)
            self.assertIn('proposed_instructions', json.loads(result.stdout))
            self.assertEqual(before, {p.name: p.read_bytes() for p in directory.iterdir()})
            data.write_text('not JSON DO_NOT_ECHO')
            result = subprocess.run([sys.executable, str(Path(r.__file__)), str(data)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertNotIn('DO_NOT_ECHO', result.stderr)


if __name__ == '__main__':
    unittest.main()
