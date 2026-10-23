"""System-wiki startup/cache invariants; fixtures never log in or touch live files."""
import asyncio
import copy
import json
from pathlib import Path
import tempfile
import unittest

import system_wiki as w


def descriptor(account='account-1', revision='revision-1'):
    return {'service_id': 'mcp-service', 'account_id': account, 'system_wiki_protocol_version': 1,
            'capabilities': ['system_wiki_read'], 'index_uri': w.INDEX, 'content_revision': revision}


def page(text='Index', revision='revision-1', visibility='public_guidance', uri=w.INDEX):
    return {'uri': uri, 'mimeType': 'text/markdown', 'text': text,
            'content_revision': revision, 'cache_visibility': visibility}


class Bridge:
    def __init__(self, desc=None, body=None, error=None):
        self.desc = descriptor() if desc is None else desc
        self.body = page() if body is None else body
        self.error = error
        self.calls = []

    async def call_tool(self, name, arguments, timeout):
        self.calls.append((name, arguments, timeout))
        if self.error:
            raise self.error
        return self.desc if name == 'get_system_wiki_capabilities' else self.body


class WikiTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'cache'
        self.now = 1000000.0
        self.context = w.Context('https://service.example/mcp', 'mcp_service', 'account-1', 'native-epoch-1', True)

    def loader(self, bridge, **kwargs):
        return w.Loader(bridge, self.root, clock=lambda: self.now, **kwargs)

    async def warm(self, body=None, context=None, desc=None):
        return await self.loader(Bridge(desc=desc, body=body)).load(context or self.context)

    async def test_online_descriptor_then_index_with_no_registry_or_capture_calls(self):
        bridge = Bridge()
        out = await self.loader(bridge).load(self.context)
        self.assertEqual(out['source'], 'live')
        self.assertEqual([c[0] for c in bridge.calls], ['get_system_wiki_capabilities', 'read_system_wiki_page'])
        self.assertEqual(out['metrics']['characters'], 5)
        self.assertIsNone(out['metrics']['tokens'])

    async def test_fresh_cache_still_authenticates_descriptor_each_session(self):
        await self.warm()
        bridge = Bridge(body=page('Should not be fetched'))
        out = await self.loader(bridge).load(self.context)
        self.assertEqual(out['source'], 'cache_fresh')
        self.assertEqual(out['text'], 'Index')
        self.assertEqual(len(bridge.calls), 1)

    async def test_stale_cache_is_replaced_online(self):
        await self.warm()
        self.now += w.FRESH_SECONDS + 1
        out = await self.loader(Bridge(body=page('Updated'))).load(self.context)
        self.assertEqual(out['source'], 'live')
        self.assertEqual(out['text'], 'Updated')

    async def test_outage_cache_requires_trusted_unchanged_native_binding(self):
        await self.warm()
        out = await self.loader(Bridge(error=OSError('PRIVATE'))).load(self.context)
        self.assertEqual(out['source'], 'cache_stale')
        untrusted = w.Context(self.context.service_url, self.context.connection_id, 'account-1', 'native-epoch-1', False)
        out = await self.loader(Bridge(error=OSError('PRIVATE'))).load(untrusted)
        self.assertEqual(out['source'], 'packaged_fallback')
        self.assertNotIn('PRIVATE', json.dumps(out))

    async def test_online_without_binding_never_persists_page_content(self):
        context = w.Context(self.context.service_url, self.context.connection_id)
        out = await self.loader(Bridge(body=page('Unique public body'))).load(context)
        self.assertEqual(out['source'], 'live')
        self.assertFalse(list(self.root.glob('*.entry.json')))

    async def test_protected_or_missing_visibility_is_never_cached(self):
        for visibility in ('protected', None, 'unknown'):
            with self.subTest(visibility=visibility):
                out = await self.warm(page('Private body', visibility=visibility))
                self.assertEqual(out['source'], 'live' if visibility == 'protected' else 'packaged_fallback')
                self.assertFalse(list(self.root.glob('*.entry.json')))
                out = await self.loader(Bridge(error=w.TransportError(503))).load(self.context)
                self.assertEqual(out['source'], 'packaged_fallback')

    async def test_auth_denials_invalidate_fresh_cache_across_loader_instances(self):
        for status in (401, 403):
            await self.warm()
            out = await self.loader(Bridge(error=w.TransportError(status))).load(self.context)
            self.assertEqual(out['source'], 'packaged_fallback')
            self.assertTrue(out['reconnect_required'])
            out = await self.loader(Bridge(error=w.TransportError(503))).load(self.context)
            self.assertEqual(out['source'], 'packaged_fallback')

    async def test_auth_denial_on_page_read_also_invalidates(self):
        await self.warm()
        self.now += w.FRESH_SECONDS + 1
        class PageDenied(Bridge):
            async def call_tool(self, name, args, timeout):
                if name == 'read_system_wiki_page':
                    raise w.TransportError(403)
                return descriptor()
        out = await self.loader(PageDenied()).load(self.context)
        self.assertEqual(out['reason'], 'auth_denied')
        out = await self.loader(Bridge(error=OSError())).load(self.context)
        self.assertEqual(out['source'], 'packaged_fallback')

    async def test_reauthentication_forces_a_new_page_read_before_cache_reuse(self):
        await self.warm()
        await self.loader(Bridge(error=w.TransportError(401))).load(self.context)
        bridge = Bridge(body=page('Reauthenticated'))
        out = await self.loader(bridge).load(self.context)
        self.assertEqual(out['source'], 'live')
        self.assertEqual(len(bridge.calls), 2)
        self.assertEqual(out['text'], 'Reauthenticated')

    async def test_account_switch_cannot_reuse_old_account_cache(self):
        await self.warm()
        other = w.Context(self.context.service_url, self.context.connection_id, 'account-2', 'epoch-2', True)
        out = await self.loader(Bridge(error=OSError())).load(other)
        self.assertEqual(out['source'], 'packaged_fallback')
        # Switching back offline does not revive a previously invalidated binding.
        out = await self.loader(Bridge(error=OSError())).load(self.context)
        self.assertEqual(out['source'], 'packaged_fallback')

    async def test_two_services_and_connection_ids_are_isolated(self):
        await self.warm()
        for url, connection in [('https://other.example/mcp', 'mcp_service'), ('https://service.example/other', 'mcp_service'), ('https://service.example/mcp', 'second_connection')]:
            out = await self.loader(Bridge(error=OSError())).load(w.Context(url, connection, 'account-1', 'native-epoch-1', True))
            self.assertEqual(out['source'], 'packaged_fallback')
        out = await self.loader(Bridge(error=OSError())).load(self.context)
        self.assertEqual(out['source'], 'cache_stale')

    async def test_auth_epoch_change_invalidates_even_when_account_is_same(self):
        await self.warm()
        changed = w.Context(self.context.service_url, self.context.connection_id, 'account-1', 'epoch-2', True)
        out = await self.loader(Bridge(error=OSError())).load(changed)
        self.assertEqual(out['source'], 'packaged_fallback')

    async def test_descriptor_account_mismatch_fails_closed(self):
        await self.warm()
        out = await self.loader(Bridge(desc=descriptor(account='account-2'))).load(self.context)
        self.assertEqual(out['reason'], 'invalid_contract')
        out = await self.loader(Bridge(error=OSError())).load(self.context)
        self.assertEqual(out['source'], 'packaged_fallback')

    async def test_revision_change_does_not_fall_back_to_old_revision_after_page_failure(self):
        await self.warm()
        class NewRevision(Bridge):
            async def call_tool(self, name, args, timeout):
                if name == 'read_system_wiki_page':
                    raise w.TransportError(503)
                return descriptor(revision='revision-2')
        out = await self.loader(NewRevision()).load(self.context)
        self.assertEqual(out['source'], 'packaged_fallback')

    async def test_unsupported_or_missing_interface_does_not_reuse_cache(self):
        await self.warm()
        for desc in [dict(descriptor(), system_wiki_protocol_version=2), dict(descriptor(), index_uri='wiki://index.md'), {}]:
            out = await self.loader(Bridge(desc=desc)).load(self.context)
            self.assertEqual(out['source'], 'packaged_fallback')
        out = await self.loader(Bridge(error=w.TransportError(404))).load(self.context)
        self.assertEqual(out['reason'], 'unsupported_interface')

    async def test_age_bound_and_clock_rollback(self):
        await self.warm()
        self.now += w.MAX_AGE_SECONDS + 1
        self.assertEqual((await self.loader(Bridge(error=OSError())).load(self.context))['source'], 'packaged_fallback')
        self.now = 999999.0
        self.assertEqual((await self.loader(Bridge(error=OSError())).load(self.context))['source'], 'packaged_fallback')

    async def test_tampered_cache_content_is_not_injected(self):
        await self.warm()
        path = next(self.root.glob('*.entry.json'))
        entry = json.loads(path.read_text())
        entry['page']['text'] = 'Tampered'
        path.write_text(json.dumps(entry))
        out = await self.loader(Bridge(error=OSError())).load(self.context)
        self.assertEqual(out['source'], 'packaged_fallback')

    async def test_oversized_index_and_inconsistent_revision_are_not_injected(self):
        for body in [page('é' * (w.INDEX_BYTES // 2 + 1)), page(''), page('  \n'), page(revision='wrong'), dict(page(), mimeType='text/html')]:
            out = await self.warm(body)
            self.assertEqual(out['source'], 'packaged_fallback')

    async def test_partial_page_or_error_envelope_falls_back_without_exposing_payload(self):
        for body in [{'text': 'PRIVATE'}, {'isError': True, 'content': [{'type': 'text', 'text': 'PRIVATE'}]}]:
            out = await self.loader(Bridge(body=body)).load(self.context)
            self.assertEqual(out['source'], 'packaged_fallback')
            self.assertNotIn('PRIVATE', json.dumps(out))

    async def test_structured_and_text_tool_results_are_supported(self):
        for desc, body in [({'structuredContent': descriptor(), 'isError': False}, {'structuredContent': page(), 'isError': False}),
                           ({'content': [{'type': 'text', 'text': json.dumps(descriptor())}]}, {'content': [{'type': 'text', 'text': json.dumps(page())}]})]:
            out = await self.loader(Bridge(desc=desc, body=body)).load(self.context)
            self.assertIn(out['source'], ('live', 'cache_fresh'))

    async def test_detail_read_is_explicit_and_does_not_prefetch_other_pages(self):
        uri = 'system-wiki://retrieval/selection.md'
        bridge = Bridge(body=page('Detail', uri=uri))
        out = await self.loader(bridge).load(self.context, uri)
        self.assertEqual(out['source'], 'live')
        self.assertEqual(len(bridge.calls), 2)
        self.assertEqual(bridge.calls[1][1], {'uri': uri})

    async def test_invalid_uri_never_reaches_bridge(self):
        for uri in ['wiki://index.md', 'system-wiki://../private.md', 'system-wiki://%2e%2e/private.md', 'system-wiki://index.md#anchor', 'system-wiki:///etc/passwd', 'system-wiki://a\\b.md']:
            bridge = Bridge()
            out = await self.loader(bridge).load(self.context, uri)
            self.assertEqual(out['source'], 'packaged_fallback')
            self.assertEqual(len(bridge.calls), 0)

    async def test_timeout_obeys_total_budget_and_fails_softly(self):
        class Hanging(Bridge):
            async def call_tool(self, name, args, timeout):
                await asyncio.sleep(1)
        started = asyncio.get_running_loop().time()
        out = await self.loader(Hanging(), budget=0.02).load(self.context)
        elapsed = asyncio.get_running_loop().time() - started
        self.assertEqual(out['source'], 'packaged_fallback')
        self.assertLess(elapsed, 0.3)

    async def test_concurrent_starts_do_not_corrupt_cache_or_block(self):
        class Slow(Bridge):
            async def call_tool(self, name, args, timeout):
                await asyncio.sleep(0.01)
                return await super().call_tool(name, args, timeout)
        first, second = await asyncio.gather(self.loader(Slow()).load(self.context), self.loader(Slow()).load(self.context))
        self.assertEqual(first['source'], 'live')
        self.assertEqual(second['source'], 'packaged_fallback')
        out = await self.loader(Bridge()).load(self.context)
        self.assertEqual(out['source'], 'cache_fresh')

    async def test_public_cache_is_private_and_contains_no_raw_binding_identifiers(self):
        await self.warm()
        self.assertEqual(self.root.stat().st_mode & 0o777, 0o700)
        for path in self.root.iterdir():
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            if path.suffix == '.json':
                self.assertNotIn('native-epoch-1', path.read_text())
                self.assertNotIn('account-1', path.read_text())

    async def test_extra_response_fields_are_neither_cached_nor_returned(self):
        body = dict(page(), token='PRIVATE', account_metadata={'secret': 'PRIVATE'})
        out = await self.warm(body)
        self.assertNotIn('PRIVATE', json.dumps(out))
        self.assertTrue(list(self.root.glob('*.entry.json')))
        for path in self.root.glob('*.json'):
            self.assertNotIn('PRIVATE', path.read_text())

    async def test_denial_does_not_invalidate_a_different_connection(self):
        await self.warm()
        other = w.Context(self.context.service_url, 'other_connection', 'account-1', 'native-epoch-1', True)
        await self.warm(context=other)
        await self.loader(Bridge(error=w.TransportError(403))).load(self.context)
        out = await self.loader(Bridge(error=OSError())).load(other)
        self.assertEqual(out['source'], 'cache_stale')

    async def test_detail_size_bound_is_not_the_index_bound(self):
        uri = 'system-wiki://detail.md'
        out = await self.loader(Bridge(body=page('x' * (w.INDEX_BYTES + 1), uri=uri))).load(self.context, uri)
        self.assertEqual(out['source'], 'live')
        out = await self.loader(Bridge(body=page('x' * (w.PAGE_BYTES + 1), revision='revision-2', uri=uri), desc=descriptor(revision='revision-2'))).load(self.context, uri)
        self.assertEqual(out['source'], 'packaged_fallback')

    async def test_two_calls_share_one_timeout_budget(self):
        class SlowBoth(Bridge):
            async def call_tool(self, name, args, timeout):
                await asyncio.sleep(0.02)
                return await super().call_tool(name, args, timeout)
        bridge = SlowBoth()
        out = await self.loader(bridge, budget=0.03).load(self.context)
        self.assertEqual(out['source'], 'packaged_fallback')
        self.assertEqual(out['metrics']['calls'], 2)
        self.assertFalse(list(self.root.glob('*.entry.json')))

    async def test_cache_quota_and_atomic_replacement(self):
        for i in range(20):
            uri = f'system-wiki://page{i}.md'
            await self.loader(Bridge(body=page('x' * w.PAGE_BYTES, uri=uri))).load(self.context, uri)
        self.assertLessEqual(sum(p.stat().st_size for p in self.root.glob('*.json')), w.CACHE_BYTES)
        self.assertFalse(list(self.root.glob('.writing-*')))

    async def test_insecure_or_symlink_cache_fails_softly(self):
        self.root.mkdir(mode=0o755)
        self.assertEqual((await self.loader(Bridge()).load(self.context))['reason'], 'cache_unavailable')
        self.root.rmdir()
        destination = self.root.with_name('other')
        destination.mkdir()
        self.root.symlink_to(destination, target_is_directory=True)
        self.assertEqual((await self.loader(Bridge()).load(self.context))['reason'], 'cache_unavailable')
        self.assertEqual(list(destination.iterdir()), [])

    async def test_bridge_exception_does_not_expose_secrets(self):
        out = await self.loader(Bridge(error=RuntimeError('PRIVATE TOKEN'))).load(self.context)
        self.assertEqual(out['reason'], 'bridge_error')
        self.assertNotIn('PRIVATE TOKEN', json.dumps(out))


if __name__ == '__main__':
    unittest.main()
