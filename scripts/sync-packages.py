#!/usr/bin/env python3
"""Generate/check both plugin packages from shared instruction/helper sources.

Canonical setup, bootstrap, retrieval and fallback text live in setup/. This
script writes source-package copies only; it never edits installed caches.
"""
import argparse
from pathlib import Path
import sys


def resources(root):
    for platform in ('chatgpt', 'claude'):
        skill = root / platform / 'kbs/skills/setup-kbs'
        text = (root / 'setup/SKILL.md').read_bytes()
        if platform == 'chatgpt':
            yield skill / 'references/client-setup.md', (root / 'setup/openai-client-setup.md').read_bytes()
            yield skill / 'references/connection-reference.md', (root / 'setup/connection-reference.md').read_bytes().replace(b'(openai-client-setup.md)', b'(client-setup.md)')
        if platform == 'claude':
            text = text.replace(b'\nmetadata:\n', b'\ndisable-model-invocation: true\nmetadata:\n', 1)
        yield skill / 'SKILL.md', text
        yield root / platform / 'kbs/skills/use-kbs/SKILL.md', (root / 'setup/bootstrap.md').read_bytes()
        yield root / platform / 'kbs/skills/use-standard-kb/SKILL.md', (root / 'setup/retrieval.md').read_bytes()
        yield root / platform / 'kbs/skills/use-kbs/references/fallback.md', (root / 'setup/fallback.md').read_bytes()
        for source, target in (
            ('setup/reconcile.py', 'scripts/reconcile.py'),
            ('setup/package.json', 'scripts/package.json'),
            ('setup/native.py', 'scripts/native.py'),
            ('setup/system_wiki.py', 'scripts/system_wiki.py'),
            ('setup/fallback.md', 'scripts/fallback.md'),
            ('setup/GUIDE.md', 'references/setup-evidence.md'),
            ('setup/native-setup.md', 'references/native-setup.md'),
            ('setup/system-wiki-client.md', 'references/system-wiki-client.md'),
            ('local-capture/capture.py', 'scripts/capture.py'),
            ('local-capture/install.py', 'scripts/install.py'),
            ('local-capture/SETUP.md', 'references/local-capture-setup.md'),
        ):
            yield skill / target, (root / source).read_bytes()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='update source package copies; default is check only')
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    changed = []
    for path, data in resources(args.root):
        if not path.exists() or path.read_bytes() != data:
            changed.append(str(path.relative_to(args.root)))
            if args.write:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
    for path in changed:
        print(('Updated ' if args.write else 'Drift: ') + path)
    if not changed:
        print('Shared package resources match canonical source.')
    return int(bool(changed) and not args.write)


if __name__ == '__main__':
    sys.exit(main())
