#!/usr/bin/env python3
"""Run declared template checks with isolated agent-browser sessions (Python standard library)."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from urllib.parse import urljoin
import uuid

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from ui_scope import validate, require, load_scope, scope_identity
STATUSES = ('PASS', 'FAIL', 'UNCHECKED', 'NA')




class Browser:
    def __init__(self, session, config, timeout, direct):
        self.session, self.config, self.timeout = session, config, timeout
        self.env = {k: v for k, v in os.environ.items() if not k.startswith('AGENT_BROWSER_')}
        self.env['AGENT_BROWSER_DEFAULT_TIMEOUT'] = str(int(timeout * 1000))
        if direct:
            self.env = {k: v for k, v in self.env.items() if k.lower() not in {'http_proxy', 'https_proxy', 'all_proxy'}}
        self.direct = direct

    def call(self, *args):
        cmd = ['agent-browser', '--config', str(self.config), '--session', self.session, '--json',
               '--args', '--mute-audio' + (',--no-proxy-server' if self.direct else ''), *args]
        try:
            p = subprocess.run(cmd, capture_output=True, text=True, env=self.env, timeout=self.timeout + 5)
            payload = json.loads(p.stdout)
            if p.returncode or payload.get('success') is not True:
                raise RuntimeError('browser command failed')
            return payload.get('data', {})
        except Exception as e:
            # Do not echo CLI errors/URLs: browser messages may contain credentials or page text.
            raise RuntimeError(f'{args[0]} did not complete ({type(e).__name__})') from None

    def evaluate(self, expression):
        return self.call('eval', expression)['result']

    def ready(self, expression):
        end = time.monotonic() + self.timeout
        while time.monotonic() < end:
            if self.evaluate(f'Boolean({expression})') is True:
                return
            time.sleep(0.15)
        raise RuntimeError('Content readiness timed out')


def unchecked(rules, reason):
    return [dict(rule=r['id'], role=r['role'], source=r['source'], status='UNCHECKED', samples=0, detail=reason) for r in rules]


def run_case(design, project, case, viewport, args, out, config, index):
    row = dict(case=case['id'], state=case['state'], path=case['path'], viewport=viewport, results=[])
    if args.case and case['id'] not in args.case:
        row['results'] = unchecked(design['rules'], 'Not selected for this run; previous results were not imported')
        row['executed'] = False
        return row
    browser = Browser(f'ui-check-{uuid.uuid4().hex[:12]}', config, args.timeout, args.direct)
    row.update(session=browser.session, executed=True)
    url = urljoin(project['base_url'], case['path'])
    try:
        browser.call('set', 'viewport', str(viewport['width']), str(viewport['height']))
        browser.call('open', url)
        browser.ready(case['ready'])
        for step in case.get('steps', []):
            browser.call(step['action'], *step['args'])
            if step.get('ready'):
                browser.ready(step['ready'])
        observed_url = browser.evaluate('location.href')
        if observed_url != url:
            raise RuntimeError('Actual URL differs from the declared case; check redirects or navigation state')
        # Identity of what was actually served (paths only, never query strings): a stale build shows here.
        row['assets'] = browser.evaluate("[...document.querySelectorAll('link[rel=stylesheet][href],script[src]')]"
                                         ".map(e => new URL(e.href || e.src).pathname)")
        data ={'rules': design['rules'], 'bindings': {**project.get('roles', {}), **case.get('roles', {})}, 'exclude': case.get('exclude', {})}
        results = browser.evaluate('(' + (ROOT / 'check-page.js').read_text() + ')(' + json.dumps(data) + ')')
        require(isinstance(results, list) and len(results) == len(design['rules']), 'Invalid probe response')
        for expected, result in zip(design['rules'], results):
            require(result['rule'] == expected['id'] and result['status'] in STATUSES, 'Mismatched probe response')
        row['results'] = results
        if args.screenshots:
            screenshot = f'case-{index}.png'
            browser.call('screenshot', str(out / screenshot), '--full')
            row['screenshot'] = screenshot
    except Exception as e:
        row['error'] = str(e)
        if not row['results']:
            row['results'] = unchecked(design['rules'], str(e))
    finally:
        try:
            browser.call('close')
        except Exception:
            row['cleanup_error'] = 'Session close failed; inspect only session ' + browser.session
    return row


def render(report):
    def cell(value):
        return str(value).replace('|', '\\|').replace('\n', ' ')
    counts = report['counts']
    scope_text = ('完整目标：' + report['scope']['id'] + ' / ' + report['scope']['application'] + '；' + report['scope']['objective']) if report.get('scope') else '仅声明子集，无完整目标证明。'
    lines = ['# Web UI 批量核验', '', f"项目：{report['project']}；模板：{report['template']['id']}；来源：{report['template']['source']}",
             '', scope_text, '', '范围：仅本次声明并编译的规则。模板条款编译完整性、视觉阅读效果与真实业务结果需另行核验。', '',
             f"计划 case × viewport：{len(report['cases'])}；实际执行：{sum(c['executed'] for c in report['cases'])}。", '',
             '；'.join(f'{s}: {counts[s]}' for s in STATUSES), '',
             '| 页面 / 状态 | 视口 | 规则 | 结果 | 样本数 | 证据 / 未核实原因 |', '| --- | --- | --- | --- | --- | --- |']
    for c in report['cases']:
        for r in c['results']:
            lines.append('| ' + ' | '.join(map(cell, [c['case'] + ' / ' + c['state'], c['viewport']['id'], r['rule'], r['status'], r['samples'], r['detail']])) + ' |')
        if c.get('error') or c.get('cleanup_error'):
            lines.extend(['', f"执行问题 {c['case']}: {c.get('error', '')} {c.get('cleanup_error', '')}", ''])
    lines.extend(['', '## 按规则归组的失败', ''])
    for rule, cases in report['failures_by_rule'].items():
        lines.append(f'- {cell(rule)}: ' + ', '.join(map(cell, cases)))
    if not report['failures_by_rule']:
        lines.append('无 FAIL；UNCHECKED 不属于通过。')
    return '\n'.join(lines) + '\n'


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--design', type=Path)
    p.add_argument('--project', type=Path)
    p.add_argument('--scope', type=Path, help='Complete task scope binding design and project inputs')
    p.add_argument('--output', required=True, type=Path, help='New persistent output directory; never overwrite a previous run')
    p.add_argument('--jobs', required=True, type=int, help='Isolated browser concurrency, selected for target capacity')
    p.add_argument('--capacity-reason', required=True, help='Why this concurrency fits the target/browser resources')
    p.add_argument('--timeout', type=float, default=20, help='Seconds per command/content-ready wait')
    p.add_argument('--case', action='append', help='Rerun selected case IDs; others remain UNCHECKED')
    p.add_argument('--screenshots', action='store_true')
    p.add_argument('--direct', action='store_true', help='Explicitly bypass proxies for this isolated browser')
    args = p.parse_args()
    try:
        require(1 <= args.jobs <= 32 and 0 < args.timeout <= 300 and args.capacity_reason.strip(), 'Invalid concurrency, reason or timeout')
        scope = None
        if args.scope:
            scope, scope_sha256, inputs = load_scope(args.scope, args.design, args.project)
            design_bytes, project_bytes = inputs['design'], inputs['project']
        else:
            require(args.design is not None and args.project is not None, 'Provide --scope or both --design and --project')
            design_bytes, project_bytes = args.design.read_bytes(), args.project.read_bytes()
        design, project = json.loads(design_bytes), json.loads(project_bytes)
        validate(design, project)
        require(not args.case or set(args.case) <= {c['id'] for c in project['cases']}, 'Unknown --case ID')
        out = args.output.resolve()
        out.mkdir(parents=True, exist_ok=False)
    except Exception as e:
        print(f'配置无效，尚未检查页面：{type(e).__name__}: {e}', file=sys.stderr)
        return 2
    config = out / 'browser-config.json'
    config.write_text('{}\n')
    jobs = [(c, v) for c in project['cases'] for v in project['viewports']]
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = [pool.submit(run_case, design, project, c, v, args, out, config, i) for i, (c, v) in enumerate(jobs)]
        cases = [f.result() for f in futures]
    counts = {s: sum(r['status'] == s for c in cases for r in c['results']) for s in STATUSES}
    groups = {}
    for c in cases:
        for r in c['results']:
            if r['status'] == 'FAIL':
                groups.setdefault(r['rule'], []).append(c['case'] + ' / ' + c['viewport']['id'])
    report = dict(schema_version=1, created_at=datetime.now(timezone.utc).isoformat(), project=project['project'], template=design['template'],
                  input_sha256={k: hashlib.sha256(v).hexdigest() for k, v in [('design', design_bytes), ('project', project_bytes)]},
                  jobs=args.jobs, capacity_reason=args.capacity_reason, counts=counts, failures_by_rule=groups, cases=cases)
    if scope is not None:
        report['scope'] = scope_identity(scope, scope_sha256)
    (out / 'results.json').write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    (out / 'report.md').write_text(render(report))
    print(f"已核验声明范围：{len(cases)} 个页面状态/视口组合；" + '，'.join(f'{s}={counts[s]}' for s in STATUSES))
    print('已绑定完整 scope 分母；模板编译完整性仍需人工反查。' if scope else '仅声明子集，无完整目标证明。')
    print(f'完整结果：{out / "report.md"}；不代表整站视觉或业务验收。')
    print('处理 FAIL，补验 UNCHECKED；输入错误或会话清理失败先修复执行环境。')
    if any(c.get('error') or c.get('cleanup_error') for c in cases):
        return 2
    return 1 if counts['FAIL'] else 3 if counts['UNCHECKED'] else 0


if __name__ == '__main__':
    sys.exit(main())
