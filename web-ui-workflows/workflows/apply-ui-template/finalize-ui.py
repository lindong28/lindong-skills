#!/usr/bin/env python3
"""Join declared manual observations to an unchanged verify-ui report."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ui_scope import KINDS, load_scope, validate_scope_report, scope_identity, completion_status

STATUSES = ('PASS', 'FAIL', 'UNCHECKED', 'NA')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def finalize(results_bytes, design_bytes, observations_bytes, evidence_root, scope_path=None):
    original, design, observations = map(json.loads, (results_bytes, design_bytes, observations_bytes))
    require(all(x['schema_version'] == 1 for x in (original, design, observations)), 'Unsupported schema_version')
    require(original['input_sha256']['design'] == digest(design_bytes), 'Design hash differs from the executed design')
    require(original['template'] == design['template'], 'Template identity mismatch')
    require(observations['results_sha256'] == digest(results_bytes), 'Observations refer to another results file')
    scope = None
    if scope_path is not None:
        scope, scope_sha256, inputs = load_scope(scope_path)
        require(inputs['design'] == design_bytes, 'Design differs from complete scope')
        validate_scope_report(original, scope, scope_sha256, inputs)
    else:
        require('scope' not in original, 'Scope-bound results require --scope at finalization')
    rules = {r['id']: r for r in design['rules']}
    require(bool(rules) and len(rules) == len(design['rules']), 'Empty or duplicate design rules')
    require(all(r['kind'] in KINDS for r in rules.values()), 'Unknown rule kind')
    require(isinstance(original['cases'], list) and bool(original['cases']), 'Missing cases')
    indexed, case_keys = {}, set()
    for case in original['cases']:
        key = (case['case'], case['viewport']['id'])
        require(key not in case_keys, 'Duplicate case / viewport')
        case_keys.add(key)
        require(type(case['executed']) is bool, 'Invalid executed flag')
        require(len(case['results']) == len(rules), 'Incomplete original rule set')
        found = set()
        for result in case['results']:
            rid = result['rule']
            require(rid in rules and rid not in found, 'Unknown or duplicate original rule')
            found.add(rid)
            require(result['status'] in STATUSES, 'Unknown original status')
            require(all(result[k] == rules[rid][k] for k in ('role', 'source')), 'Rule identity mismatch')
            indexed[(*key, rid)] = (case, result)
    require(isinstance(observations['observations'], list), 'observations must be a list')
    notes = {}
    for note in observations['observations']:
        key = tuple(note[k] for k in ('case', 'viewport', 'rule'))
        require(key in indexed and key not in notes, 'Unknown or duplicate observation target')
        case, result = indexed[key]
        require(rules[note['rule']]['kind'] == 'manual' and result['status'] == 'UNCHECKED', 'Only pending manual rules accept observations')
        require(case['executed'] and not case.get('error') and not case.get('cleanup_error'), 'Cannot resolve an unexecuted or failed case')
        require(note['status'] in STATUSES and nonempty(note['observation']), 'Observation needs status and explanation')
        require(nonempty(note['object']), 'Name the observed object and state (or the missing object)')
        evidence = note.get('evidence', [])
        require(isinstance(evidence, list), 'evidence must be a list')
        require(note['status'] == 'UNCHECKED' or bool(evidence), 'Resolved observations require evidence')
        normalized = []
        for item in evidence:
            require(nonempty(item['path']), 'Evidence path is required')
            path = (evidence_root / item['path']).resolve()
            require(path.is_file() and digest(path.read_bytes()) == item['sha256'], 'Missing or changed evidence file')
            normalized.append({'path': str(path), 'sha256': item['sha256']})
        notes[key] = {**note, 'evidence': normalized}
    cases = []
    machine, reading = Counter(), Counter()
    for case in original['cases']:
        output = {**case, 'results': []}
        for result in case['results']:
            manual = rules[result['rule']]['kind'] == 'manual'
            note = notes.get((case['case'], case['viewport']['id'], result['rule']))
            merged = {**result, 'method': 'reading' if manual else 'machine'}
            if note:
                merged.update(status=note['status'], observation=note)
            (reading if manual else machine)[merged['status']] += 1
            output['results'].append(merged)
        cases.append(output)
    counts = {s: machine[s] + reading[s] for s in STATUSES}
    errors = sum(bool(c.get('error') or c.get('cleanup_error')) for c in cases)
    status = completion_status(cases)
    execution_status = completion_status([c for c in cases if c['executed']])
    return dict(schema_version=1, created_at=datetime.now(timezone.utc).isoformat(),
                project=original['project'], template=original['template'], status=status,
                execution_status=execution_status, scope_status=status if scope else 'UNPROVEN',
                scope=scope_identity(scope, scope_sha256) if scope else None,
                input_sha256={'results': digest(results_bytes), 'design': digest(design_bytes), 'observations': digest(observations_bytes)},
                counts={s: counts[s] for s in STATUSES},
                machine_counts={s: machine[s] for s in STATUSES}, reading_counts={s: reading[s] for s in STATUSES},
                execution_errors=errors, cases=cases)


def render(report):
    def cell(value):
        return str(value).replace('|', '\\|').replace('\n', ' ')
    labels = {'ERROR': '执行存在错误', 'FAIL': '存在未通过项', 'UNCHECKED': '尚有未核实项', 'COMPLETE': '声明项已完成（PASS / 有依据的 NA）'}
    cases = report['cases']
    lines = ['# Web UI 交付核验', '', f"本次实际执行：{labels[report['execution_status']]}。", '',
             ('完整 scope：' + labels[report['scope_status']] + '。') if report['scope'] else '仅声明子集，无完整目标证明。', '',
             f"项目：{report['project']}；模板：{report['template']['id']}；来源：{report['template']['source']}。", '',
             '范围仅限下列已声明规则和页面状态；不代表编译完整、整站美观或真实业务验收。', '',
             f"页面状态 {len({c['case'] for c in cases})} 种，视口 {len({c['viewport']['id'] for c in cases})} 种，规则 {len(cases[0]['results'])} 条；计划组合 {len(cases)}，实际执行 {sum(c['executed'] for c in cases)}，执行/清理错误 {report['execution_errors']}。", '',
             '| 方法 | PASS | FAIL | UNCHECKED | NA |', '| --- | --- | --- | --- | --- |']
    for label, field in [('机器检查', 'machine_counts'), ('实际阅读', 'reading_counts')]:
        lines.append('| ' + label + ' | ' + ' | '.join(str(report[field][s]) for s in STATUSES) + ' |')
    lines += ['', '处理 FAIL，补验 UNCHECKED；执行错误先修复再重跑。完成项无需额外动作。', '',
              '| 页面 / 状态 | 视口 | 规则 / 方法 | 结果 | 观察 / 原始读数 | 证据 |', '| --- | --- | --- | --- | --- | --- |']
    for case in cases:
        for result in case['results']:
            note = result.get('observation')
            detail = (note['object'] + '：' + note['observation']) if note else result['detail']
            evidence = '; '.join(e['path'] for e in note['evidence']) if note else ''
            lines.append('| ' + ' | '.join(cell(x) for x in [case['case'] + ' / ' + case['state'], case['viewport']['id'], result['rule'] + ' / ' + result['method'], result['status'], detail, evidence]) + ' |')
        if case.get('error') or case.get('cleanup_error'):
            lines += ['', f"执行问题 {cell(case['case'])} / {cell(case['viewport']['id'])}：{cell(case.get('error', ''))} {cell(case.get('cleanup_error', ''))}", '']
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--results', required=True, type=Path)
    parser.add_argument('--design', type=Path)
    parser.add_argument('--scope', type=Path, help='Verify complete task scope and current input hashes')
    parser.add_argument('--observations', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path, help='New output directory; original results remain unchanged')
    args = parser.parse_args()
    try:
        if args.scope:
            _, _, inputs = load_scope(args.scope, args.design)
            design_bytes = inputs['design']
        else:
            require(args.design is not None, 'Provide --scope or --design')
            design_bytes = args.design.read_bytes()
        report = finalize(args.results.read_bytes(), design_bytes, args.observations.read_bytes(), args.observations.resolve().parent, args.scope)
        args.output.mkdir(parents=True, exist_ok=False)
        (args.output / 'delivery.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
        (args.output / 'delivery.md').write_text(render(report))
    except (ValueError, OSError, KeyError, TypeError) as error:
        print(f'未生成交付结论：输入或输出无效（{type(error).__name__}）。请核对来源摘要、条目身份和证据文件；原报告保留。', file=sys.stderr)
        return 2
    print(render(report).split('| 方法')[0].strip())
    print(f"完整结果：{args.output.resolve() / 'delivery.md'}")
    print('处理 FAIL，补验 UNCHECKED；执行错误修复后重跑。')
    return {'COMPLETE': 0, 'FAIL': 1, 'ERROR': 2, 'UNCHECKED': 3}[report['status']]


if __name__ == '__main__':
    sys.exit(main())
