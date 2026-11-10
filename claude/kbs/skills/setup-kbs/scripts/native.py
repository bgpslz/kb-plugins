#!/usr/bin/env python3
"""Inspect native Code settings, plan additive changes, and explicitly save a plan.

Python 3.11+. Never reads OAuth credential stores or starts an MCP server/login.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
import tomllib
from urllib.parse import urlsplit

from reconcile import CODE, START, END, reconcile_block


class SetupError(ValueError):
    pass


def digest(data):
    return hashlib.sha256(data).hexdigest()


def endpoint(value):
    """Accept credential-free HTTPS URLs and HTTP loopback; never echo bad URLs."""
    if not isinstance(value, str) or any(c.isspace() for c in value):
        raise SetupError('Invalid endpoint')
    try:
        p = urlsplit(value)
        if p.username or p.password or p.query or p.fragment or not p.hostname or '${' in value:
            raise ValueError()
        if p.scheme != 'https' and not (p.scheme == 'http' and p.hostname in {'127.0.0.1', 'localhost', '::1'}):
            raise ValueError()
        _ = p.port
    except ValueError:
        raise SetupError('Endpoint must be HTTPS (or HTTP loopback), without credentials/query/fragment') from None
    # Keep paths and explicit ports exact; do not collapse distinct MCP resources.
    return p._replace(scheme=p.scheme.lower(), netloc=p.netloc.lower()).geturl()


def read_file(path, snapshots):
    try:
        data = path.read_bytes() if path.exists() else None
    except OSError:
        raise SetupError('Cannot read native configuration') from None
    snapshots[str(path)] = digest(data) if data is not None else None
    return data


def parse(path, snapshots, kind='json'):
    data = read_file(path, snapshots)
    try:
        result = (tomllib.loads(data.decode()) if kind == 'toml' else json.loads(data)) if data is not None else {}
        if not isinstance(result, dict):
            raise ValueError()
        return result
    except (ValueError, UnicodeError):
        raise SetupError('Invalid native configuration; refusing to replace it') from None


def servers(mapping, source, records):
    if not isinstance(mapping, dict):
        raise SetupError('Invalid native server map')
    for name, data in mapping.items():
        if not isinstance(data, dict):
            raise SetupError('Invalid native server entry')
        record = {'connection_id': name, 'source': source, 'enabled': data.get('enabled', True) is not False,
                  'transport': data.get('type', 'http' if 'url' in data else 'stdio'),
                  'authentication': 'not_tested', 'wiki_read': 'not_tested'}
        try:
            record['url'] = endpoint(data.get('url'))
        except SetupError:
            record['url'] = None
            record['endpoint_unresolved_or_non_http'] = True
        oauth = data.get('oauth', {})
        if not isinstance(oauth, dict):
            raise SetupError('Invalid OAuth settings')
        record['pre_registered_client'] = bool(oauth.get('client_id') or data.get('clientId'))
        # Whitelist only public callback metadata. Never expose headers/env/secrets.
        try:
            callback = oauth.get('callback_url')
            record['saved_callback'] = endpoint(callback) if callback else None
        except SetupError:
            record['saved_callback'] = None
        records.append(record)


def inspect(surface, execution, home, project, codex_home=None):
    if surface not in CODE or execution not in {'local', 'cloud', 'unknown'}:
        raise SetupError('Native adapters require an explicit Code surface and execution location')
    home, project = Path(home).absolute(), Path(project).absolute()
    snapshots, records, issues = {}, [], []
    client = 'codex' if surface.startswith('codex') else 'claude'
    if client == 'codex':
        config_dir = Path(codex_home).absolute() if codex_home else home / '.codex'
        user_path = config_dir / 'config.toml'
        config = parse(user_path, snapshots, 'toml')
        servers(config.get('mcp_servers', {}), 'user', records)
        directories = []
        for directory in (project, *project.parents):
            directories.append(directory)
            if (directory / '.git').exists():
                break
        for directory in reversed(directories):
            path = directory / '.codex/config.toml'
            if path == user_path:
                continue
            data = parse(path, snapshots, 'toml')
            servers(data.get('mcp_servers', {}), 'project:' + str(directory), records)
        issues.append('project_trust_managed_policy_and_app_connections_require_native_verification')
        instruction_path = config_dir / 'AGENTS.md'
    else:
        profile = parse(home / '.claude.json', snapshots)
        servers(profile.get('mcpServers', {}), 'user', records)
        local = profile.get('projects', {}).get(str(project), {})
        servers(local.get('mcpServers', {}), 'local', records)
        servers(parse(project / '.mcp.json', snapshots).get('mcpServers', {}), 'project', records)
        enabled = {}
        for path in (home / '.claude/settings.json', project / '.claude/settings.json', project / '.claude/settings.local.json'):
            settings = parse(path, snapshots)
            enabled.update(settings.get('enabledPlugins', {}))
        installed = parse(home / '.claude/plugins/installed_plugins.json', snapshots).get('plugins', {})
        for plugin, on in enabled.items():
            if on is not True:
                continue
            installations = installed.get(plugin, [])
            applicable = [i for i in installations if i.get('scope') == 'user' or i.get('projectPath') == str(project)]
            if len(applicable) != 1:
                issues.append('enabled_plugin_installation_unresolved:' + plugin)
                continue
            root = Path(applicable[0]['installPath'])
            data = parse(root / '.mcp.json', snapshots)
            servers(data.get('mcpServers', data), 'plugin:' + plugin, records)
            manifest = parse(root / '.claude-plugin/plugin.json', snapshots)
            inline = manifest.get('mcpServers', {})
            if isinstance(inline, dict):
                servers(inline, 'plugin:' + plugin, records)
            elif inline:
                issues.append('plugin_external_mcp_configuration_requires_inspection:' + plugin)
        issues.append('project_approvals_managed_policy_and_hosted_connectors_require_native_verification')
        instruction_path = home / '.claude/CLAUDE.md'
    read_file(instruction_path, snapshots)
    urls = {r['url'] for r in records if r['url']}
    duplicates = [u for u in sorted(urls) if sum(r['url'] == u for r in records) > 1]
    return {'surface': surface, 'execution': execution, 'home': str(home), 'project': str(project),
            'codex_home': str(config_dir) if client == 'codex' else None,
            'connections': records, 'duplicate_endpoints': duplicates, 'issues': issues,
            'snapshots': snapshots, 'instruction_path': str(instruction_path),
            'readiness': 'configuration_observed_only', 'capture_actions': []}


def file_for(report, scope):
    home, project = Path(report['home']), Path(report['project'])
    if report['surface'].startswith('codex'):
        if scope not in {'user', 'project'}:
            raise SetupError('Codex supports user/project configuration targets')
        return Path(report['codex_home']) / 'config.toml' if scope == 'user' else project / '.codex/config.toml'
    if scope not in {'user', 'local', 'project'}:
        raise SetupError('Unknown Claude scope')
    return project / '.mcp.json' if scope == 'project' else home / '.claude.json'


def plan(report, scope='user', desired=None, block=None, codex_apps_checked=False):
    if report['execution'] != 'local':
        raise SetupError('Cloud/unknown execution: inspect only; no host-local persistence plan')
    if block is not None and desired:
        raise SetupError('Plan one settings file or instructions at a time')
    if block is not None:
        if not block.startswith(START) or not block.endswith(END) or block.count(START) != 1 or block.count(END) != 1:
            raise SetupError('Expected one complete managed instruction block')
        path = Path(report['instruction_path'])
        reconcile_block(path.read_bytes().decode() if path.exists() else '', block)
        changes = []
        action = 'instructions'
    else:
        path = file_for(report, scope)
        changes = []
        action = 'connections'
        for item in desired or []:
            if set(item) != {'connection_id', 'url'} or not re.fullmatch(r'[A-Za-z0-9_-]+', item['connection_id']):
                raise SetupError('Desired connection needs only connection_id and credential-free url')
            url = endpoint(item['url'])
            existing = report['connections']
            same_url = [r for r in existing if r['url'] == url]
            if same_url:
                if not any(r['enabled'] for r in same_url):
                    raise SetupError('Existing endpoint is disabled; reconcile it explicitly')
                continue  # Reuse any configured scope/plugin, regardless of requested alias.
            if any(r['connection_id'] == item['connection_id'] for r in existing):
                raise SetupError('Connection name already configured; refusing replacement')
            if any('plugin' in i and 'unresolved' in i or 'external_mcp' in i for i in report['issues']):
                raise SetupError('Inspect unresolved plugin configuration before adding a connection')
            if any(r.get('endpoint_unresolved_or_non_http') and r['transport'] != 'stdio' for r in existing):
                raise SetupError('Resolve unknown HTTP endpoints before adding a connection')
            if any(c['connection_id'] == item['connection_id'] for c in changes):
                raise SetupError('Duplicate desired connection name')
            if report['surface'].startswith('codex') and codex_apps_checked is not True:
                raise SetupError('Check app-backed OAuth alternatives before adding a native server; record that inspection and explicit selection of native setup with --codex-apps-checked. App presence alone does not establish access or block native setup.')
            if url not in {c['url'] for c in changes}:
                changes.append({'connection_id': item['connection_id'], 'url': url})
    return {'schema_version': 1, 'inspection': report, 'action': action, 'scope': scope,
            'target': str(path), 'additions': changes, 'managed_block': block,
            'authentication': 'separate_native_login_required', 'capture_actions': [],
            'codex_apps_checked': codex_apps_checked is True}


def candidate(proposal):
    report, path = proposal['inspection'], Path(proposal['target'])
    old = path.read_bytes() if path.exists() else None
    if proposal['action'] == 'instructions':
        return reconcile_block(old.decode() if old else '', proposal['managed_block']).encode()
    if not proposal['additions']:
        return old
    if report['surface'].startswith('codex'):
        text = old.decode() if old else ''
        for item in proposal['additions']:
            text += '\n\n[mcp_servers.' + json.dumps(item['connection_id']) + ']\nurl = ' + json.dumps(item['url']) + '\n'
        tomllib.loads(text)  # Reject incompatible inline-table layouts rather than rewriting them.
        return text.encode()
    data = json.loads(old) if old else {}
    if proposal['scope'] == 'local':
        settings = data.setdefault('projects', {}).setdefault(report['project'], {})
    else:
        settings = data
    mapping = settings.setdefault('mcpServers', {})
    for item in proposal['additions']:
        if item['connection_id'] in mapping:
            raise SetupError('Refusing replacement of an existing connection')
        mapping[item['connection_id']] = {'type': 'http', 'url': item['url']}
    return (json.dumps(data, indent=2, ensure_ascii=False) + '\n').encode()


def apply(proposal, personal_claude_approved=False):
    if proposal.get('schema_version') != 1:
        raise SetupError('Unknown native plan version')
    previous = proposal['inspection']
    if os.environ.get('CLAUDE_CONFIG_DIR') and previous['surface'].startswith('claude'):
        raise SetupError('Custom Claude configuration directory needs manual resolution')
    if previous['execution'] != 'local':
        raise SetupError('Local persistence is unavailable for cloud/unknown execution')
    current = inspect(previous['surface'], previous['execution'], previous['home'], previous['project'], previous['codex_home'])
    if current != previous:
        raise SetupError('Configuration changed after inspection; create and review a new plan')
    rebuilt = plan(current, proposal['scope'], proposal['additions'], proposal['managed_block'],
                   proposal.get('codex_apps_checked', False))
    if rebuilt != proposal:
        raise SetupError('Plan is inconsistent; recreate it from current native configuration')
    if proposal['action'] == 'instructions' and previous['surface'].startswith('claude') and not personal_claude_approved:
        raise SetupError('Personal Claude instructions require Bruno approval')
    path = Path(proposal['target'])
    # macOS itself aliases /var and /tmp. Inspect links only within the selected
    # store boundary, not system-level aliases above that boundary.
    roots = [Path(previous[k]) for k in ('home', 'project')]
    boundary = next((root for root in roots if path.is_relative_to(root)), path.parent)
    for part in (path, *path.parents):
        if part.is_symlink():
            raise SetupError('Refusing native writes through symlinks')
        if part == boundary:
            break
    if path.exists() and not stat.S_ISREG(path.stat().st_mode):
        raise SetupError('Target is not a regular file')
    before = path.read_bytes() if path.exists() else None
    after = candidate(proposal)
    if before == after:
        return {'status': 'unchanged', 'target': str(path), 'authentication': 'not_tested'}
    if os.name != 'posix':
        raise SetupError('Automatic persistence is verified for POSIX stores only; use the manual path')
    path.parent.mkdir(parents=True, exist_ok=True)
    lock = path.with_name(path.name + '.kbs-setup.lock')
    try:
        lock_fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise SetupError('Another setup write or an interrupted setup lock requires inspection') from None
    backup = temporary = None
    try:
        os.close(lock_fd)
        # Recheck under our writer lock. Other applications must not edit concurrently.
        if (path.read_bytes() if path.exists() else None) != before:
            raise SetupError('Configuration changed before write')
        if before is not None:
            fd, backup = tempfile.mkstemp(prefix=path.name + '.before-kbs-', dir=path.parent)
            with os.fdopen(fd, 'wb') as stream:
                stream.write(before)
                stream.flush()
                os.fsync(stream.fileno())
        mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o600
        fd, temporary = tempfile.mkstemp(prefix=path.name + '.kbs-', dir=path.parent)
        with os.fdopen(fd, 'wb') as stream:
            os.fchmod(stream.fileno(), mode)
            stream.write(after)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
        temporary = None
        if path.read_bytes() != after:
            raise SetupError('Saved settings changed during persistence verification; inspect backup')
        if proposal['action'] == 'connections':
            saved = inspect(previous['surface'], 'local', previous['home'], previous['project'], previous['codex_home'])
            for c in proposal['additions']:
                if not any(r['connection_id'] == c['connection_id'] and r['url'] == c['url'] for r in saved['connections']):
                    raise SetupError('Native re-read did not find a saved connection; inspect backup')
        return {'status': 'saved_and_reread', 'target': str(path), 'backup': backup,
                'authentication': 'not_tested', 'guidance_loading': 'not_tested', 'capture_actions': []}
    finally:
        if temporary:
            Path(temporary).unlink(missing_ok=True)
        lock.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=('inspect', 'plan', 'apply'))
    parser.add_argument('--surface', choices=sorted(CODE))
    parser.add_argument('--execution', choices=('local', 'cloud', 'unknown'), default='unknown')
    parser.add_argument('--home', type=Path, default=Path.home())
    parser.add_argument('--project', type=Path, default=Path.cwd())
    parser.add_argument('--codex-home', type=Path)
    parser.add_argument('--scope', choices=('user', 'local', 'project'), default='user')
    parser.add_argument('--codex-apps-checked', action='store_true',
                        help='record inspection of app-backed alternatives and explicit selection of native setup; not an absence, discovery or authentication check')
    parser.add_argument('--desired', type=Path, help='JSON list of connection_id/url pairs from authorised setup')
    parser.add_argument('--block', type=Path, help='complete managed instruction block to save')
    parser.add_argument('--plan', type=Path, help='reviewed saved plan for explicit apply')
    parser.add_argument('--personal-claude-approved', action='store_true', help='use only after Bruno approved the personal instruction edit')
    args = parser.parse_args()
    try:
        if os.environ.get('CLAUDE_CONFIG_DIR') and (args.surface or '').startswith('claude'):
            raise SetupError('Custom Claude config directory: resolve native stores manually; default adapter is not applicable')
        if args.operation == 'apply':
            if not args.plan:
                raise SetupError('Apply requires a reviewed saved plan')
            result = apply(json.loads(args.plan.read_text()), args.personal_claude_approved)
        else:
            if not args.surface:
                raise SetupError('Supply the actual Code surface')
            codex_home = args.codex_home or (Path(os.environ['CODEX_HOME']) if 'CODEX_HOME' in os.environ and args.home == Path.home() else None)
            result = inspect(args.surface, args.execution, args.home, args.project, codex_home)
            if args.operation == 'plan':
                if not args.desired and not args.block:
                    raise SetupError('Plan needs desired connections or a managed block')
                result = plan(result, args.scope, json.loads(args.desired.read_text()) if args.desired else None,
                              args.block.read_bytes().decode().strip() if args.block else None, args.codex_apps_checked)
        print(json.dumps(result, indent=2))
        return 0
    except SetupError as exc:
        print(str(exc), file=sys.stderr)
        return 2
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        # Native parse errors can contain credential-bearing source lines.
        print('Native setup refused or could not verify the operation. Inspect inputs, current configuration and any backup; no credentials are logged.', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
