#!/usr/bin/env python3
"""Check source package inventory and shared-file parity without changing files.

This checks a checkout, not installed plugins, credentials or live services.
Run with Python 3.9+; only the standard library is required.
"""
import argparse
import json
from pathlib import Path
import sys

from importlib.util import module_from_spec, spec_from_file_location


def check(root):
    errors = []
    release = json.loads((root / 'setup/package.json').read_text())
    packages = (root / 'chatgpt/kbs', root / 'claude/kbs')
    inventories = []
    versions = []

    def read(path):
        try:
            return path.read_bytes()
        except OSError as exc:
            errors.append(f'{path.relative_to(root)}: {type(exc).__name__}')
            return None

    for package, manifest in zip(packages, ('.codex-plugin/plugin.json', '.claude-plugin/plugin.json')):
        raw = read(package / manifest)
        try:
            version = json.loads(raw)['version'] if raw is not None else None
            if not isinstance(version, str) or not version:
                raise ValueError('missing version')
        except (ValueError, KeyError, TypeError):
            errors.append(f'{package.relative_to(root)}/{manifest}: invalid manifest/version')
            version = None
        if version != release['version']:
            errors.append(f'{package.relative_to(root)}: version differs from source release inventory')
        versions.append(version)
        skills = {p.name for p in (package / 'skills').iterdir() if p.is_dir()}
        if skills != set(release['skills']):
            errors.append(f'{package.relative_to(root)}: differs from source skill inventory')
        inventories.append(skills)
        if not skills:
            errors.append(f'{package.relative_to(root)}: empty skill inventory')
        for skill in sorted(skills):
            read(package / 'skills' / skill / 'SKILL.md')
        print(f'{package.relative_to(root)}: version {version}; {len(skills)} skills: {", ".join(sorted(skills))}')

    if versions[0] != versions[1]:
        errors.append('package versions differ')
    if inventories[0] != inventories[1]:
        errors.append('package skill inventories differ')

    # Client-specific setup instructions live in separate references.
    for skill in sorted(inventories[0] & inventories[1]):
        a, b = [read(p / 'skills' / skill / 'SKILL.md') for p in packages]
        if a is not None and b is not None:
            if a != b.replace(b'disable-model-invocation: true\n', b''):
                errors.append(f'{skill}: shared skill content differs')

    shared = {
        'local-capture/capture.py': 'scripts/capture.py',
        'local-capture/install.py': 'scripts/install.py',
        'local-capture/SETUP.md': 'references/local-capture-setup.md',
    }
    for source, target in shared.items():
        original = read(root / source)
        for package in packages:
            path = package / 'skills/setup-kbs' / target
            copy = read(path)
            if original is not None and copy is not None and copy != original:
                errors.append(f'{path.relative_to(root)}: differs from {source}')
    spec = spec_from_file_location('sync_packages', Path(__file__).with_name('sync-packages.py'))
    sync = module_from_spec(spec)
    spec.loader.exec_module(sync)
    for path, expected in sync.resources(root):
        actual = read(path)
        if actual is not None and actual != expected:
            errors.append(f'{path.relative_to(root)}: shared source resource drift')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1],
                        help='source checkout to check (defaults to this script\'s checkout)')
    args = parser.parse_args()
    try:
        errors = check(args.root)
    except OSError as exc:
        print(f'Cannot inspect checkout: {type(exc).__name__}', file=sys.stderr)
        return 1
    for error in errors:
        print(f'ERROR: {error}', file=sys.stderr)
    if not errors:
        print('Shared skills and capture resources match. Installed/live state was not checked.')
    return int(bool(errors))


if __name__ == '__main__':
    sys.exit(main())
