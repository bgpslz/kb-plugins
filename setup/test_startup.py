"""Whole startup instructions: no partial delivery, extra traversal or renewed budget."""
import asyncio
import unittest

import system_wiki as w
import test_system_wiki as fixtures

Bridge, descriptor, page = fixtures.Bridge, fixtures.descriptor, fixtures.page


class BundleBridge(Bridge):
    async def call_tool(self, name, arguments, timeout):
        self.calls.append((name, arguments, timeout))
        if self.error:
            raise self.error
        return self.desc if name == 'get_system_wiki_capabilities' else page(
            'Complete ' + arguments['uri'], uri=arguments['uri'], revision=self.desc['content_revision'])


class StartupTests(unittest.IsolatedAsyncioTestCase):
    setUp = fixtures.WikiTests.setUp
    loader = fixtures.WikiTests.loader
    warm = fixtures.WikiTests.warm
    async def startup(self, bridge, surface='codex-desktop', execution='local', **kwargs):
        return await self.loader(bridge, **kwargs).load_startup(self.context, surface, execution)

    async def test_startup_delivers_only_two_complete_pages_and_one_descriptor(self):
        bridge = BundleBridge()
        out = await self.startup(bridge)
        self.assertTrue(out['complete'])
        self.assertEqual(out['delivery'], 'host_delivery_required')
        self.assertEqual([c[0] for c in bridge.calls], ['get_system_wiki_capabilities'] + ['read_system_wiki_page'] * 2)
        self.assertEqual(out['required_uris'], [w.INDEX, 'system-wiki://local-codex.md'])
        for p in out['pages']:
            self.assertIn(p['text'], out['text'])
        self.assertEqual(out['metrics']['utf8_bytes'], len(out['text'].encode()))

    async def test_actual_location_selects_surface_and_unknown_cannot_claim_local(self):
        cases = [('codex-cli', 'local', 'local-codex'), ('claude-code-desktop', 'local', 'local-claude-code'),
                 ('codex-desktop', 'cloud', 'other-harnesses'), ('claude-code-cli', 'unknown', 'other-harnesses'),
                 ('chatgpt', 'local', 'other-harnesses'), ('claude-chat', 'cloud', 'other-harnesses')]
        for surface, execution, expected in cases:
            out = await self.startup(BundleBridge(), surface, execution)
            self.assertEqual(out['required_uris'][1], f'system-wiki://{expected}.md')

    async def test_open_webui_and_unknown_harness_are_not_native_targets(self):
        for surface in ('open-webui', 'unverified-app', None, ['invalid']):
            bridge = BundleBridge()
            out = await self.startup(bridge, surface)
            self.assertFalse(out['complete'])
            self.assertEqual(out['reason'], 'unsupported_surface')
            self.assertEqual(bridge.calls, [])

    async def test_missing_surface_discards_live_index_and_never_caches_partial_startup(self):
        class Missing(BundleBridge):
            async def call_tool(self, name, args, timeout):
                if args.get('uri') == 'system-wiki://local-codex.md':
                    raise w.TransportError(404)
                return await super().call_tool(name, args, timeout)
        out = await self.startup(Missing())
        self.assertFalse(out['complete'])
        self.assertEqual(out['pages'], [])
        self.assertEqual(out['text'], self.loader(Bridge()).fallback)
        self.assertFalse(list(self.root.glob('*.entry.json')))

    async def test_second_page_revision_change_cannot_mix_instructions(self):
        class Mixed(BundleBridge):
            async def call_tool(self, name, args, timeout):
                value = await super().call_tool(name, args, timeout)
                if args.get('uri') == 'system-wiki://local-codex.md':
                    value['content_revision'] = 'different'
                return value
        out = await self.startup(Mixed())
        self.assertEqual(out['reason'], 'invalid_contract')
        self.assertFalse(out['complete'])
        self.assertFalse(list(self.root.glob('*.entry.json')))

    async def test_fresh_startup_cache_authenticates_once_without_refetching(self):
        await self.startup(BundleBridge())
        bridge = BundleBridge()
        out = await self.startup(bridge)
        self.assertEqual(out['source'], 'cache_fresh')
        self.assertEqual(out['metrics']['calls'], 1)
        self.assertTrue(out['complete'])

    async def test_outage_requires_both_pages_at_one_revision(self):
        await self.warm()  # Index only is insufficient.
        out = await self.startup(BundleBridge(error=OSError()))
        self.assertFalse(out['complete'])
        await self.startup(BundleBridge())
        out = await self.startup(BundleBridge(error=w.TransportError(503)))
        self.assertEqual(out['source'], 'cache_stale')
        self.assertTrue(out['complete'])

    async def test_new_revision_failed_startup_does_not_revive_old_bundle_later(self):
        await self.startup(BundleBridge())
        class Upgrade(BundleBridge):
            async def call_tool(self, name, args, timeout):
                if name == 'read_system_wiki_page':
                    raise w.TransportError(503)
                return descriptor(revision='revision-2')
        self.assertFalse((await self.startup(Upgrade()))['complete'])
        self.assertFalse((await self.startup(BundleBridge(error=OSError())))['complete'])

    async def test_denial_on_surface_invalidates_previously_cached_bundle(self):
        await self.startup(BundleBridge())
        self.now += w.FRESH_SECONDS + 1
        class Denied(BundleBridge):
            async def call_tool(self, name, args, timeout):
                if args.get('uri') == 'system-wiki://local-codex.md':
                    raise w.TransportError(403)
                return await super().call_tool(name, args, timeout)
        out = await self.startup(Denied())
        self.assertTrue(out['reconnect_required'])
        self.assertFalse((await self.startup(BundleBridge(error=OSError())))['complete'])

    async def test_combined_size_can_exceed_index_limit_without_truncation(self):
        class Large(BundleBridge):
            async def call_tool(self, name, args, timeout):
                if name == 'get_system_wiki_capabilities':
                    return descriptor()
                return page('é' * 3000, uri=args['uri'])
        out = await self.startup(Large())
        self.assertTrue(out['complete'])
        self.assertGreater(out['metrics']['utf8_bytes'], w.INDEX_BYTES)
        self.assertEqual([len(p['text']) for p in out['pages']], [3000, 3000])

    async def test_three_calls_share_total_startup_budget(self):
        class Slow(BundleBridge):
            async def call_tool(self, name, args, timeout):
                await asyncio.sleep(0.02)
                return await super().call_tool(name, args, timeout)
        out = await self.startup(Slow(), budget=0.05)
        self.assertFalse(out['complete'])
        self.assertEqual(out['metrics']['calls'], 3)
        self.assertFalse(list(self.root.glob('*.entry.json')))

    async def test_current_reader_envelope_without_metadata_is_not_fabricated(self):
        class CurrentReader(BundleBridge):
            async def call_tool(self, name, args, timeout):
                if name == 'get_system_wiki_capabilities':
                    raise w.TransportError(404)
                return {'structuredContent': {'uri': args['uri'], 'mimeType': 'text/markdown', 'text': 'Real guide'}}
        out = await self.startup(CurrentReader())
        self.assertFalse(out['complete'])
        self.assertEqual(out['reason'], 'unsupported_interface')

if __name__ == '__main__':
    unittest.main()
