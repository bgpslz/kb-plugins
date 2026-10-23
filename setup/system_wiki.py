"""Inactive system-wiki client core; authenticated async bridge is host-supplied.

No credential discovery, HTTP client, registry reconciliation, hooks or capture.
Cache is opt-in and requires an account/auth binding attested by the native host.
"""
import asyncio
from contextlib import contextmanager, nullcontext
from dataclasses import dataclass
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat
import tempfile
import time

from reconcile import system_wiki_available, surface_uri
from native import endpoint

INDEX = 'system-wiki://index.md'
FRESH_SECONDS = 24 * 60 * 60
MAX_AGE_SECONDS = 7 * 24 * 60 * 60
CACHE_BYTES = 1024 * 1024
INDEX_BYTES = 8 * 1024
PAGE_BYTES = 64 * 1024


class TransportError(Exception):
    """Native bridge maps HTTP/auth/unsupported results to status, without secrets."""
    def __init__(self, status=None):
        self.status = status


class InvalidResponse(Exception):
    pass


class CacheUnavailable(Exception):
    pass


@dataclass(frozen=True)
class Context:
    service_url: str
    connection_id: str
    account_id: str = ''
    auth_binding: str = ''
    binding_verified: bool = False

    @property
    def cache_allowed(self):
        return self.binding_verified is True and bool(self.account_id) and bool(self.auth_binding)


def hashed(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def wiki_uri(uri):
    if not isinstance(uri, str) or not uri.startswith('system-wiki://'):
        raise InvalidResponse()
    relative = uri[len('system-wiki://'):]
    if not re.fullmatch(r'[A-Za-z0-9_-]+(?:/[A-Za-z0-9_-]+)*\.md', relative):
        raise InvalidResponse()
    return uri


def unwrap(result):
    if not isinstance(result, dict) or result.get('isError') is True or 'error' in result:
        raise InvalidResponse()
    if 'structuredContent' in result:
        result = result['structuredContent']
    elif isinstance(result.get('content'), list):
        blocks = result['content']
        if len(blocks) != 1 or blocks[0].get('type') != 'text':
            raise InvalidResponse()
        raw = blocks[0].get('text')
        if not isinstance(raw, str) or len(raw.encode()) > 2 * PAGE_BYTES:
            raise InvalidResponse()
        try:
            result = json.loads(raw)
        except ValueError:
            raise InvalidResponse() from None
    if not isinstance(result, dict):
        raise InvalidResponse()
    return result


def descriptor_valid(value):
    return (system_wiki_available(value)
            and len(value['account_id']) <= 2048
            and len(value['content_revision']) <= 256)


def page_valid(page, descriptor, uri):
    if (page.get('uri') != uri or page.get('mimeType') != 'text/markdown'
            or page.get('cache_visibility') not in {'public_guidance', 'protected'}
            or page.get('content_revision') != descriptor['content_revision']
            or not isinstance(page.get('text'), str) or not page['text'].strip()):
        raise InvalidResponse()
    limit = INDEX_BYTES if uri == INDEX else PAGE_BYTES
    if len(page['text'].encode()) > limit:
        raise InvalidResponse()
    return page


class Cache:
    """Dedicated private directory; one nonblocking lock covers each load.

    Lock contention fails softly; it never delays another session past its budget.
    The native host must invalidate its own binding on logout/denial independently
    of this cache. Neither binding IDs nor tokens are stored in plaintext here.
    """
    def __init__(self, root, context):
        self.root = Path(root)
        self.connection = hashed([endpoint(context.service_url), context.connection_id])
        self.binding = hashed([context.account_id, context.auth_binding])
        self.state_path = self.root / (self.connection + '.state.json')
        self.context = context

    @contextmanager
    def locked(self):
        fd = None
        try:
            import fcntl
            if self.root.is_symlink():
                raise CacheUnavailable()
            self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
            info = self.root.stat()
            if info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) & 0o077:
                raise CacheUnavailable()
            fd = os.open(self.root / '.lock', os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            yield self
        except (OSError, ImportError):
            raise CacheUnavailable() from None
        finally:
            if fd is not None:
                os.close(fd)

    def _read(self, path, limit=CACHE_BYTES):
        if path.is_symlink():
            raise CacheUnavailable()
        if not path.exists():
            return None
        info = path.stat()
        if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) & 0o077:
            raise CacheUnavailable()
        if info.st_size > limit:
            return None
        try:
            value = json.loads(path.read_bytes())
            return value if isinstance(value, dict) else None
        except (ValueError, UnicodeError):
            return None

    def _write(self, path, value):
        raw = json.dumps(value, ensure_ascii=False, sort_keys=True).encode()
        if len(raw) > CACHE_BYTES or path.is_symlink():
            raise CacheUnavailable()
        files = list(self.root.glob('*.json'))
        if any(p.is_symlink() for p in files):
            raise CacheUnavailable()
        size = sum(p.stat().st_size for p in files if p != path) + len(raw)
        # Evict content only. Losing an eligibility marker must not revive cache.
        entries = sorted((p for p in files if p.name.endswith('.entry.json') and p != path), key=lambda p: p.stat().st_mtime)
        for entry in entries:
            if size <= CACHE_BYTES:
                break
            size -= entry.stat().st_size
            entry.unlink()
        if size > CACHE_BYTES:
            raise CacheUnavailable()
        fd, tmp = tempfile.mkstemp(prefix='.writing-', dir=self.root)
        try:
            with os.fdopen(fd, 'wb') as stream:
                stream.write(raw)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(tmp, path)
        finally:
            Path(tmp).unlink(missing_ok=True)

    def state(self):
        return self._read(self.state_path, 4096) or {}

    def active(self):
        state = self.state()
        return state.get('binding') == self.binding and state.get('valid') is True

    def invalidate(self):
        state = self.state()
        if state:
            self._write(self.state_path, {**state, 'valid': False})

    def select_binding(self):
        if not self.context.cache_allowed:
            return
        state = self.state()
        if state.get('binding') != self.binding:
            self._write(self.state_path, {'binding': self.binding, 'valid': False})

    def entry_path(self, revision, uri):
        key = hashed([self.connection, self.binding, 1, revision, uri])
        return self.root / (key + '.entry.json')

    def get(self, revision, uri, now, maximum_age):
        if not self.context.cache_allowed or not self.active():
            return None
        entry = self._read(self.entry_path(revision, uri), 2 * PAGE_BYTES)
        if not entry:
            return None
        fetched = entry.get('fetched_at')
        if type(fetched) not in (float, int) or not math.isfinite(fetched) or not 0 <= now - fetched <= maximum_age:
            return None
        page = entry.get('page')
        if not isinstance(page, dict) or page.get('cache_visibility') != 'public_guidance':
            return None
        try:
            page_valid(page, {'content_revision': revision}, uri)
        except InvalidResponse:
            return None
        if entry.get('integrity') != hashed(page):
            return None
        return page

    def save(self, page, now):
        if not self.context.cache_allowed:
            return
        revision, uri = page['content_revision'], page['uri']
        target = self.entry_path(revision, uri)
        if page.get('cache_visibility') == 'public_guidance':
            # Persist whitelisted fields only; no unrelated tool/account metadata.
            page = {k: page[k] for k in ('uri', 'mimeType', 'text', 'content_revision', 'cache_visibility')}
            self._write(target, {'fetched_at': now, 'page': page, 'integrity': hashed(page)})
        elif target.exists():
            if target.is_symlink():
                raise CacheUnavailable()
            target.unlink()
        self._write(self.state_path, {'binding': self.binding, 'valid': True, 'revision': revision})

    def outage(self, uri, now, revision=None):
        if not self.context.cache_allowed or not self.active():
            return None
        revision = revision or self.state().get('revision')
        return self.get(revision, uri, now, MAX_AGE_SECONDS) if isinstance(revision, str) else None


class Loader:
    """Host bridge: async call_tool(name, arguments, timeout_seconds).

    The bridge uses an existing authenticated native connection and must map
    401/403 and network/5xx errors into TransportError. There is no new OAuth flow.
    """
    def __init__(self, bridge, cache_root=None, budget=5.0, clock=time.time, monotonic=time.monotonic):
        self.bridge, self.cache_root, self.budget = bridge, cache_root, budget
        self.clock, self.monotonic = clock, monotonic
        self.fallback = Path(__file__).with_name('fallback.md').read_text()

    async def load(self, context, uri=INDEX):
        """Read one explicit detail page; startup callers use load_startup instead."""
        return await self._load(context, [uri])

    async def load_startup(self, context, surface, execution):
        """One descriptor, two complete pages, one revision and total budget.

        Returning this bundle does not inject it: the host must deliver text to
        the model and separately record context-delivery acceptance.
        """
        uri = surface_uri(surface, execution)
        return await self._load(context, [INDEX, uri] if uri else [], startup=True)

    async def _load(self, context, uris, startup=False):
        started = self.monotonic()
        deadline = started + self.budget
        calls = 0

        def result(source, reason, pages=None):
            if self.monotonic() > deadline and pages is not None:
                source, reason, pages = 'packaged_fallback', 'budget_exhausted', None
            if pages and startup:
                text = '# KB system operating instructions\n\n' + '\n\n'.join(
                    '## ' + p['uri'] + '\n\n' + p['text'] for p in pages)
            else:
                text = pages[0]['text'] if pages else self.fallback
            out = {'source': source, 'reason': reason, 'text': text,
                   'uri': pages[0]['uri'] if pages and not startup else None,
                   'content_revision': pages[0]['content_revision'] if pages else None,
                   'reconnect_required': reason == 'auth_denied',
                   'metrics': {'calls': calls, 'characters': len(text), 'utf8_bytes': len(text.encode()),
                               'elapsed_ms': round((self.monotonic() - started) * 1000, 2), 'tokens': None}}
            if startup:
                out.update(kind='system_wiki_startup', complete=bool(pages),
                           required_uris=uris, pages=[{'uri': p['uri'], 'text': p['text']} for p in pages or []],
                           delivery='host_delivery_required')
            return out

        async def call(name, args):
            nonlocal calls
            remaining = deadline - self.monotonic()
            if remaining <= 0:
                raise asyncio.TimeoutError()
            calls += 1
            value = await asyncio.wait_for(self.bridge.call_tool(name, args, remaining), remaining)
            if self.monotonic() > deadline:
                raise asyncio.TimeoutError()
            return unwrap(value)

        try:
            endpoint(context.service_url)
            if not uris:
                return result('packaged_fallback', 'unsupported_surface')
            for uri in uris:
                wiki_uri(uri)
            if not isinstance(context.connection_id, str) or not context.connection_id:
                raise InvalidResponse()
            if context.binding_verified is True and (not isinstance(context.account_id, str) or not context.account_id
                                                       or not isinstance(context.auth_binding, str) or not context.auth_binding):
                raise InvalidResponse()
            cache = Cache(self.cache_root, context) if self.cache_root else None
            with cache.locked() if cache else nullcontext():
                if cache:
                    cache.select_binding()
                revision = None
                try:
                    descriptor = await call('get_system_wiki_capabilities', {})
                    if not descriptor_valid(descriptor):
                        raise InvalidResponse()
                    if context.cache_allowed and descriptor['account_id'] != context.account_id:
                        raise InvalidResponse()
                    revision = descriptor['content_revision']
                    if cache and cache.state().get('revision') != revision:
                        cache.invalidate()  # An observed upgrade must not revive the old bundle offline.
                    pages, sources = [], []
                    for uri in uris:
                        page = cache.get(revision, uri, self.clock(), FRESH_SECONDS) if cache else None
                        sources.append('cache_fresh' if page else 'live')
                        if page is None:
                            page = page_valid(await call('read_system_wiki_page', {'uri': uri}), descriptor, uri)
                        pages.append(page)
                    # Publish cache eligibility only after the entire requested set validates.
                    if cache:
                        for page, source in zip(pages, sources):
                            if source == 'live':
                                cache.save(page, self.clock())
                    source = 'cache_fresh' if all(s == 'cache_fresh' for s in sources) else 'live'
                    return result(source, 'authenticated_revision_match' if source == 'cache_fresh' else 'authenticated_read', pages)

                except (TransportError, OSError, asyncio.TimeoutError) as exc:
                    status = exc.status if isinstance(exc, TransportError) else None
                    if status in (401, 403):
                        if cache:
                            cache.invalidate()
                        return result('packaged_fallback', 'auth_denied')
                    outage = not isinstance(exc, TransportError) or status is None or (type(status) is int and 500 <= status <= 599)
                    if outage:
                        pages = [cache.outage(uri, self.clock(), revision) for uri in uris] if cache else []
                        if pages and all(pages) and len({p['content_revision'] for p in pages}) == 1:
                            return result('cache_stale', 'outage_with_trusted_binding', pages)
                        return result('packaged_fallback', 'unavailable')
                    if cache:
                        cache.invalidate()
                    return result('packaged_fallback', 'unsupported_interface')
                except (InvalidResponse, ValueError, TypeError, KeyError, AttributeError):
                    if cache:
                        cache.invalidate()
                    return result('packaged_fallback', 'invalid_contract')
        except CacheUnavailable:
            return result('packaged_fallback', 'cache_unavailable')
        except (ValueError, TypeError, InvalidResponse, OSError):
            return result('packaged_fallback', 'invalid_context_or_cache')
        except Exception:
            # Bridge implementation errors may contain tokens or server payloads.
            return result('packaged_fallback', 'bridge_error')
