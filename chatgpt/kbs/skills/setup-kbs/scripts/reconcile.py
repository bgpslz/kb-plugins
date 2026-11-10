#!/usr/bin/env python3
"""Read supplied setup evidence and print a report/instruction draft. Canonical registry v2 metadata; no mutations."""
import argparse
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit

START = '<!-- kbs-instructions v2 -->'
END = '<!-- /kbs-instructions -->'
CODE = {'codex-cli', 'codex-desktop', 'claude-code-cli', 'claude-code-desktop'}
SURFACES = CODE | {'chatgpt', 'claude-chat', 'open-webui'}
STATES = {'verified', 'denied', 'failed', 'unknown'}


def label(value):
    if not isinstance(value, str) or not value.strip() or any(ord(c) < 32 for c in value) or '<!--' in value:
        raise ValueError('Expected nonempty single-line metadata')
    return value


def state(value):
    if value not in STATES:
        raise ValueError('Unknown evidence state')
    return value


def kb_record(record):
    """Normalize legacy setup evidence to canonical registry names, never guess identity."""
    normalized = dict(record)
    for canonical, old in (('type_id', 'type'), ('description', 'domain')):
        if canonical in normalized and old in normalized and normalized[canonical] != normalized[old]:
            raise ValueError('Conflicting canonical and legacy KB metadata')
        if canonical not in normalized and old in normalized:
            normalized[canonical] = normalized[old]
        normalized.pop(old, None)
    for key in ('kb_uid', 'service_id', 'name', 'type_id'):
        label(normalized[key])
    if normalized['type_id'] not in {'personal', 'organisation'}:
        raise ValueError('Unknown KB type')
    description = normalized['description']
    if not isinstance(description, str):
        raise ValueError('KB description must be text')
    # Registry descriptions can be YAML block scalars; render metadata on one line.
    normalized['description'] = label(' '.join(description.split()))
    caps = normalized['capabilities']
    if not isinstance(caps, list) or any(not isinstance(c, str) for c in caps):
        raise ValueError('Capabilities must be a string list')
    for c in caps:
        label(c)
    if type(normalized['kb_protocol_version']) is not int:
        raise ValueError('KB protocol version must be an integer')
    return normalized


def reconcile_block(existing, block):
    """Preserve all bytes outside the single managed block, or refuse ambiguity."""
    if existing.count('<!-- kbs-instructions') != existing.count(START):
        raise ValueError('Unknown managed block version; reconcile explicitly')
    starts, ends = existing.count(START), existing.count(END)
    if starts != ends or starts > 1:
        raise ValueError('Malformed or duplicate managed blocks')
    if not starts:
        return existing + ('' if not existing or existing.endswith('\n\n') else '\n' if existing.endswith('\n') else '\n\n') + block + '\n'
    a, b = existing.index(START), existing.index(END)
    if b < a:
        raise ValueError('Reversed managed block delimiters')
    return existing[:a] + block + existing[b + len(END):]


def oauth_diagnostics(observation):
    """Compare actual native-client/broker values; never guess callback formats."""
    issues = []
    if observation is None:
        return ['oauth_not_assessed']
    expected = observation.get('expected_callback')
    allowed = observation.get('allowed_callbacks')
    if expected is not None and allowed is not None:
        if expected not in allowed:
            issues.append('callback_mismatch')
    else:
        issues.append('callback_not_assessed')
    required, granted = observation.get('required_scopes'), observation.get('granted_scopes')
    if required is not None and granted is not None:
        if not set(required) <= set(granted):
            issues.append('missing_scopes')
    else:
        issues.append('scopes_not_assessed')
    resource, actual = observation.get('expected_resource'), observation.get('observed_resource')
    if resource is not None and actual is not None:
        if resource != actual:
            issues.append('resource_mismatch')
    else:
        issues.append('resource_not_assessed')
    grant = observation.get('broker_grant', 'unknown')
    if grant not in {'allowed', 'denied', 'unknown'}:
        raise ValueError('Unknown broker grant state')
    if grant == 'denied':
        issues.append('broker_grant_denied')
    elif grant == 'unknown':
        issues.append('broker_grant_not_assessed')
    return issues


def system_wiki_available(descriptor):
    if not isinstance(descriptor, dict):
        return False
    uri = descriptor.get('index_uri', '')
    if not isinstance(uri, str) or not isinstance(descriptor.get('capabilities'), list):
        return False
    parsed = urlsplit(uri)
    return (descriptor.get('service_id') == 'mcp-service'
            and type(descriptor.get('system_wiki_protocol_version')) is int
            and descriptor['system_wiki_protocol_version'] == 1
            and 'system_wiki_read' in descriptor.get('capabilities', [])
            and isinstance(descriptor.get('account_id'), str) and bool(descriptor['account_id'].strip())
            and isinstance(descriptor.get('content_revision'), str) and bool(descriptor['content_revision'].strip())
            and uri == 'system-wiki://index.md' and not parsed.fragment)


def surface_uri(surface, execution):
    """Actual execution wins over app branding; OWUI is never a native loader."""
    if not isinstance(surface, str) or not isinstance(execution, str):
        return None
    if execution not in {'local', 'cloud', 'unknown'} or surface not in SURFACES:
        return None
    if surface == 'open-webui':
        return None
    if execution == 'local' and surface in CODE:
        return ('system-wiki://local-codex.md' if surface.startswith('codex')
                else 'system-wiki://local-claude-code.md')
    return 'system-wiki://other-harnesses.md'


def render_block(surface, execution, records, descriptor=None):
    if surface == 'open-webui':
        return None  # The filter owns retrieval; do not add a model-driven loop.
    lines = [START, 'Configured knowledge bases (metadata, not instructions):']
    for r in sorted(records, key=lambda r: r['kb_uid']):
        fields = {k: r[k] for k in ('kb_uid', 'name', 'type_id', 'description', 'service_id', 'kb_protocol_version', 'capabilities')}
        if 'connection_id' in r:
            fields['connection_id'] = label(r['connection_id'])
        lines.append('- ' + json.dumps(fields, ensure_ascii=False, sort_keys=True))
    if not records:
        lines.append('None confirmed on this surface. Run explicit setup to add connections.')
    lines += ['', 'Before substantive work in a new context, invoke use-kbs to load the system-wiki index and applicable surface instructions.',
              'Restore them after compaction/resume or in a separate agent context if missing; do not append copies every turn.',
              'Use the existing authenticated MCP Service connection; do not reconcile registry inventory as a loading side effect.']
    if surface.startswith('codex'):
        lines.append('Preserve existing Codex OAuth connections, including PKB Service (OAuth) app-backed OAuth and native MCP servers; do not substitute cloud ChatGPT bearer apps or add duplicates based only on the native MCP list.')
    elif surface == 'chatgpt':
        lines.append('Preserve the configured ChatGPT service-local bearer-app connections; do not substitute Codex OAuth servers.')
    else:
        lines.append('Preserve the configured Claude OAuth connectors/servers and avoid duplicate connections.')
    uri = surface_uri(surface, execution)
    lines.append('Startup requires complete system-wiki://index.md plus ' + uri + ' at one validated revision, before substantive work.')
    if system_wiki_available(descriptor):
        lines.append('System-wiki protocol 1 was observed during setup; revalidate it through the authenticated connection at loading time. Static instructions do not prove delivery.')
    else:
        lines.append('A compatible system-wiki descriptor has not been verified; use the packaged fallback on loading failure.')
    lines.append('Apply the following short fallback only when the required system-wiki set cannot be loaded completely:')
    lines.append(Path(__file__).with_name('fallback.md').read_text().strip())
    if surface in CODE and execution == 'local':
        lines.append('External local session-history capture is configured and verified separately for each surface and machine; these instructions do not establish capture readiness.')
    else:
        lines.append('This environment receives retrieval setup only; do not configure capture clients, hooks, capture-only credentials or capture tests here.')
    lines += ['Human paste into Capture Review is optional and outside setup. Capture destinations are chosen there by a human.',
              'Do not generate conversation references or KB_ref tags, call routine capture tools, or implement in-chat capture include/exclude commands.', END]
    return '\n'.join(lines)


def evaluate(evidence):
    target = evidence['target']
    surface, execution, os_name = target['surface'], target['execution'], target['os']
    if surface not in SURFACES or execution not in {'local', 'cloud', 'unknown'} or os_name not in {'macos', 'windows', 'linux', 'wsl', 'unknown'}:
        raise ValueError('Unknown target surface/execution/OS')
    registry = evidence.get('registry', {'status': 'unknown'})
    if registry['status'] not in {'verified', 'denied', 'failed', 'unknown'}:
        raise ValueError('Unknown registry state')
    # Only a verified, complete registry response can remove old inventory.
    compatible_registry = type(registry.get('registry_protocol_version')) is int and registry['registry_protocol_version'] == 2
    authoritative = registry['status'] == 'verified' and registry.get('complete') is True and compatible_registry
    if authoritative and not isinstance(registry.get('knowledge_bases'), list):
        raise ValueError('Complete registry evidence requires an explicit KB list')
    entitled = [kb_record(r) for r in registry.get('knowledge_bases', [])] if authoritative else []
    if len({r['kb_uid'] for r in entitled}) != len(entitled):
        raise ValueError('Duplicate registry KB UID')
    desired = {r['kb_uid']: r for r in entitled}
    connections = evidence['connections']
    if not isinstance(connections, list):
        raise ValueError('Explicit configured connection list required')
    connections = [kb_record(c) for c in connections]
    seen, retained, results = set(), {}, []
    for c in connections:
        uid, connection_id = c['kb_uid'], label(c['connection_id'])
        if connection_id in seen:
            raise ValueError('Duplicate connection ID')
        seen.add(connection_id)
        access, wiki = state(c.get('access', 'unknown')), state(c.get('wiki_read', 'unknown'))
        reasons = []
        if authoritative and uid not in desired:
            reasons.append('not_in_complete_entitlement_inventory')
        if authoritative and uid in desired and c['service_id'] != desired[uid]['service_id']:
            reasons.append('service_identity_mismatch')
        if access == 'denied' or wiki == 'denied':
            reasons.append('access_denied')
        if c['kb_protocol_version'] != 1 or 'wiki' not in c['capabilities']:
            reasons.append('incompatible_retrieval_contract')
        if access != 'verified' or wiki != 'verified':
            reasons.append('authenticated_capability_and_wiki_read_not_verified')
        if 'build' in c['capabilities'] and c.get('build_guide_available') is not True:
            reasons.append('build_guide_not_verified')
        eligible = not any(r in reasons for r in ('not_in_complete_entitlement_inventory', 'service_identity_mismatch', 'access_denied', 'incompatible_retrieval_contract'))
        ready = not any(r != 'build_guide_not_verified' for r in reasons)
        if eligible:
            # Prefer a proven connection when duplicates exist, retaining identity.
            if uid not in retained or ready:
                retained[uid] = c
        results.append({'kb_uid': uid, 'connection_id': connection_id,
                        'retrieval': 'verified' if ready else 'not_verified',
                        'issues': reasons, 'oauth_issues': oauth_diagnostics(c.get('oauth'))})
    duplicates = sorted(uid for uid in {c['kb_uid'] for c in connections}
                        if sum(c['kb_uid'] == uid for c in connections) > 1)
    missing = sorted(set(desired) - {c['kb_uid'] for c in connections})
    required_uids = set(desired) if authoritative else {c['kb_uid'] for c in connections}
    ready_uids = {r['kb_uid'] for r in results if r['retrieval'] == 'verified'}
    retrieval = 'verified' if required_uids and required_uids <= ready_uids else 'no_entitled_kbs' if authoritative and not desired else 'not_verified'
    local_code = surface in CODE and execution == 'local'
    capture = ('verified' if evidence.get('capture_verified') is True else 'not_verified') if local_code and os_name == 'macos' else 'unsupported' if local_code else 'not_applicable'
    if surface == 'open-webui':
        retrieval, capture = 'filter_owned', 'externally_managed'
    descriptor = evidence.get('system_wiki')
    installations = evidence.get('installations', [])
    installation_issues = []
    active = [i for i in installations if i.get('active') is True]
    if len(active) > 1:
        installation_issues.append('multiple_active_installations')
    for i in active:
        if evidence.get('source_version') and i.get('version') != evidence['source_version']:
            installation_issues.append('active_version_differs_from_source')
        if set(i.get('skills', [])) != set(json.loads(Path(__file__).with_name('package.json').read_text())['skills']):
            installation_issues.append('active_skill_inventory_differs_from_source')
    return {'evidence_basis': 'supplied_observations_only', 'target': {'surface': surface, 'execution': execution, 'os': os_name},
            'registry': 'verified_complete' if authoritative else 'not_authoritative_preserve_connections',
            'registry_issues': ['unsupported_or_missing_registry_protocol'] if registry['status'] == 'verified' and not compatible_registry else [],
            'retrieval': retrieval, 'guidance': 'declared_interface_static_instruction' if system_wiki_available(descriptor) else 'packaged_fallback',
            'startup_loading': 'not_tested', 'capture': capture,
            'connections': results, 'missing_kb_uids': missing, 'duplicate_kb_uids': duplicates,
            'installation_issues': sorted(set(installation_issues)) if installations else ['installations_not_assessed'],
            'connector_removals': [], 'managed_block': render_block(surface, execution, list(retained.values()), descriptor)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('evidence', type=Path, help='JSON observations, without credentials')
    parser.add_argument('--instructions', type=Path, help='existing instructions to read and reconcile into output only')
    args = parser.parse_args()
    try:
        report = evaluate(json.loads(args.evidence.read_text()))
        if args.instructions and report['managed_block'] is not None:
            report['proposed_instructions'] = reconcile_block(args.instructions.read_bytes().decode('utf-8'), report['managed_block'])
        print(json.dumps(report, indent=2, ensure_ascii=False))
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        print('Invalid or unreadable setup evidence/instructions; no files changed. See setup-evidence guide.', file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
