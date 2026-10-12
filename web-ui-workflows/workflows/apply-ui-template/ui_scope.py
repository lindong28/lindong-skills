"""Identity and complete denominator shared by the UI runner and finalizer."""
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit

KINDS = {'style', 'attribute', 'text', 'count', 'no-horizontal-overflow', 'allowed-values', 'predicate', 'manual'}
STEPS = {'click': 1, 'hover': 1, 'press': 1, 'focus': 1, 'fill': 2, 'select': 2, 'scrollintoview': 1}

def require(test, message):
    if not test:
        raise ValueError(message)


def unique(items, label):
    require(isinstance(items, list) and bool(items), label + ' must be a nonempty list')
    ids = [x['id'] for x in items]
    require(all(isinstance(x, str) and x for x in ids) and len(set(ids)) == len(ids), label + ' IDs must be unique nonempty strings')


def validate(design, project):
    require(design['schema_version'] == project['schema_version'] == 1, 'Unsupported schema_version')
    require(all(isinstance(design['template'][k], str) and design['template'][k] for k in ('id', 'source')), 'Template identity is required')
    require(isinstance(project['project'], str) and bool(project['project']), 'Project identity is required')
    unique(design['rules'], 'rules'); unique(project['cases'], 'cases'); unique(project['viewports'], 'viewports')
    rule_ids = {r['id'] for r in design['rules']}
    for r in design['rules']:
        require(r['kind'] in KINDS, 'Unsupported rule kind: ' + str(r['kind']))
        require(all(isinstance(r[k], str) and r[k] for k in ('source', 'role', 'description')), 'Rule source, role and description are required')
        if r['kind'] in {'style', 'attribute', 'text', 'count'}:
            require('expected' in r, 'Missing expected value')
        if r['kind'] in {'style', 'attribute', 'allowed-values'}:
            require(isinstance(r.get('property'), str) and r['property'], 'Missing property')
        if r['kind'] == 'allowed-values':
            allowed = r.get('allowed')
            require(isinstance(allowed, list) and bool(allowed) and all(isinstance(v, str) and v for v in allowed), 'allowed-values needs a nonempty list of computed values')
            require(type(r.get('own_text', False)) is bool, 'own_text must be a boolean')
        if r['kind'] == 'count':
            require(type(r['expected']) is int and r['expected'] >= 0, 'Count must be a nonnegative integer')
        if r['kind'] == 'text':
            require(isinstance(r['expected'], str) and r.get('match', 'exact') in {'exact', 'contains'}, 'Invalid text check')
    for v in project['viewports']:
        require(all(type(v[k]) is int and 100 <= v[k] <= 10000 for k in ('width', 'height')), 'Invalid viewport dimensions')
    require(isinstance(project.get('roles', {}), dict), 'roles must be an object')
    base = urlsplit(project['base_url'])
    require(base.scheme in {'http', 'https'} and base.hostname and not base.username and not base.password, 'base_url must be HTTP(S), without credentials')
    for c in project['cases']:
        require(isinstance(c['ready'], str) and c['ready'], 'Each case needs a content-ready boolean expression')
        require(isinstance(c['path'], str) and c['path'].startswith('/') and not c['path'].startswith('//'), 'Case paths must be origin-relative')
        require(isinstance(c['state'], str) and c['state'], 'Case state must be named')
        require(isinstance(c.get('roles', {}), dict), 'Case roles must be an object')
        for key, reason in c.get('exclude', {}).items():
            require(key in rule_ids and isinstance(reason, str) and reason.strip(), 'NA needs a known rule and reason')
        for step in c.get('steps', []):
            require(step['action'] in STEPS and isinstance(step['args'], list) and len(step['args']) == STEPS[step['action']], 'Invalid state step')
            require(all(isinstance(a, str) for a in step['args']), 'Step arguments must be strings')
            require(isinstance(step.get('reason'), str) and step['reason'].strip(), 'State step needs its authorized effect/reason')
        for binding in {**project.get('roles', {}), **c.get('roles', {})}.values():
            require(isinstance(binding, dict), 'Role binding must be an object')
            require(any(isinstance(binding.get(k), str) and binding[k] for k in ('selector', 'expression')), 'Binding needs selector or expression')
            require(isinstance(binding.get('exclude', 'x'), str) and binding.get('exclude', 'x'), 'Binding exclude must be a nonempty selector')



def digest(data):
    return hashlib.sha256(data).hexdigest()


def load_scope(path, design_path=None, project_path=None):
    path = Path(path).resolve()
    raw = path.read_bytes()
    scope = json.loads(raw)
    require(scope['schema_version'] == 1, 'Unsupported scope schema_version')
    require(all(isinstance(scope[k], str) and scope[k].strip() for k in ('id', 'objective')), 'Scope id and objective are required')
    require(scope['application'] in {'style', 'scenario', 'ux'}, 'Unsupported scope application')
    inputs = {}
    for name, supplied in [('design', design_path), ('project', project_path)]:
        binding = scope[name]
        require(isinstance(binding['path'], str) and binding['path'].strip(), 'Scope input path is required')
        relative = Path(binding['path'])
        require(not relative.is_absolute(), 'Scope input paths must be relative to scope file')
        target = (path.parent / relative).resolve()
        data = target.read_bytes()
        require(binding['sha256'] == digest(data), 'Scope ' + name + ' hash differs from the complete input')
        if supplied is not None:
            require(Path(supplied).resolve() == target and Path(supplied).read_bytes() == data, '--' + name + ' differs from scope input identity')
        inputs[name] = data
    validate(json.loads(inputs['design']), json.loads(inputs['project']))
    return scope, digest(raw), inputs


def scope_identity(scope, sha256):
    return {k: scope[k] for k in ('id', 'objective', 'application')} | {'sha256': sha256}


def validate_scope_report(report, scope, sha256, inputs):
    require(report.get('scope') == scope_identity(scope, sha256), 'Report scope identity mismatch')
    design, project = (json.loads(inputs[k]) for k in ('design', 'project'))
    require(report['input_sha256'] == {k: digest(v) for k, v in inputs.items()}, 'Report input hashes differ from complete scope')
    require(report['project'] == project['project'] and report['template'] == design['template'], 'Report project or template identity mismatch')
    expected = {(c['id'], v['id']): (c, v) for c in project['cases'] for v in project['viewports']}
    found = set()
    for row in report['cases']:
        key = (row['case'], row['viewport']['id'])
        require(key in expected and key not in found, 'Unknown or duplicate scope case / viewport')
        found.add(key)
        case, viewport = expected[key]
        require(row['viewport'] == viewport and row['path'] == case['path'] and row['state'] == case['state'], 'Scope case / viewport identity mismatch')
        require(type(row['executed']) is bool, 'Invalid executed flag')
        if not row['executed']:
            require(all(r['status'] == 'UNCHECKED' for r in row['results']), 'Unexecuted scope rows must remain UNCHECKED')
    require(found == set(expected), 'Incomplete scope case / viewport matrix')


def completion_status(cases):
    if any(c.get('error') or c.get('cleanup_error') for c in cases):
        return 'ERROR'
    statuses = [r['status'] for c in cases for r in c['results']]
    if 'FAIL' in statuses:
        return 'FAIL'
    if not cases or not statuses or 'UNCHECKED' in statuses or any(not c['executed'] for c in cases):
        return 'UNCHECKED'
    return 'COMPLETE'
