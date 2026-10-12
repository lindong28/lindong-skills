import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import subprocess
import sys
import unittest

SPEC = importlib.util.spec_from_file_location('finalize_ui', Path(__file__).resolve().parents[1] / 'finalize-ui.py')
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def encode(value):
    return json.dumps(value).encode()


class FinalizeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.evidence = self.root / 'reading.txt'
        self.evidence.write_text('Observed complete item identity at both viewport widths.')
        self.design = {'schema_version': 1, 'template': {'id': 'synthetic', 'version': '1', 'source': 'fixture'},
                       'rules': [{'id': name, 'role': name, 'source': 'fixture#' + name, 'kind': kind}
                                 for name, kind in [('size', 'style'), ('hierarchy', 'manual'), ('state', 'manual')]]}
        self.results = {'schema_version': 1, 'project': 'fixture', 'template': self.design['template'],
                        'input_sha256': {'design': MODULE.digest(encode(self.design))}, 'cases': []}
        for cid in ('list', 'detail'):
            for vid in ('wide', 'narrow'):
                self.results['cases'].append({'case': cid, 'state': 'ready', 'path': '/' + cid,
                                             'viewport': {'id': vid, 'width': 1000 if vid == 'wide' else 390, 'height': 800},
                                             'executed': True,
                                             'results': [dict(rule=r['id'], role=r['role'], source=r['source'],
                                                              status='PASS' if r['kind'] == 'style' else 'UNCHECKED',
                                                              samples=1 if r['kind'] == 'style' else 0, detail='fixture')
                                                         for r in self.design['rules']]})
        self.notes = {'schema_version': 1, 'observations': []}
        for case in self.results['cases']:
            for rule in ('hierarchy', 'state'):
                self.notes['observations'].append(dict(case=case['case'], viewport=case['viewport']['id'], rule=rule,
                                                      status='PASS', object='Fixture list/detail in declared ready state',
                                                      observation='Read identity and state without truncation.',
                                                      evidence=[{'path': 'reading.txt', 'sha256': MODULE.digest(self.evidence.read_bytes())}]))

    def tearDown(self):
        self.temp.cleanup()

    def run_report(self):
        self.notes['results_sha256'] = MODULE.digest(encode(self.results))
        return MODULE.finalize(encode(self.results), encode(self.design), encode(self.notes), self.root)

    def test_current_template_without_version_and_old_identity_preserved(self):
        old_template = copy.deepcopy(self.design['template'])
        current_template = {k: v for k, v in old_template.items() if k != 'version'}
        self.design['template'] = current_template
        self.results['template'] = current_template
        self.results['input_sha256']['design'] = MODULE.digest(encode(self.design))
        report = self.run_report()
        self.assertEqual(report['status'], 'COMPLETE')
        self.assertEqual(report['template'], current_template)
        self.assertIn('来源：fixture', MODULE.render(report))
        self.results['template'] = old_template
        with self.assertRaisesRegex(ValueError, 'Template identity mismatch'):
            self.run_report()

    def test_complete_and_distinct_failure_unchecked_na(self):
        original = copy.deepcopy(self.results)
        report = self.run_report()
        self.assertEqual(report['status'], 'COMPLETE')
        self.assertEqual(report['reading_counts']['PASS'], 8)
        self.assertEqual(self.results, original)
        self.assertIn('页面状态 2 种，视口 2 种，规则 3 条', MODULE.render(report))
        self.notes['observations'][0]['status'] = 'FAIL'
        self.assertEqual(self.run_report()['status'], 'FAIL')
        self.notes['observations'][0]['status'] = 'NA'
        self.assertEqual(self.run_report()['counts']['NA'], 1)
        self.notes['observations'].pop()
        self.assertEqual(self.run_report()['status'], 'UNCHECKED')

    def test_machine_failure_cannot_be_hidden(self):
        self.results['cases'][0]['results'][0]['status'] = 'FAIL'
        self.assertEqual(self.run_report()['status'], 'FAIL')
        self.notes['observations'][0]['rule'] = 'size'
        with self.assertRaisesRegex(ValueError, 'Only pending manual'):
            self.run_report()
        self.results['cases'][0]['results'][0]['status'] = 'UNCHECKED'
        with self.assertRaisesRegex(ValueError, 'Only pending manual'):
            self.run_report()

    def test_unexecuted_and_errors_are_not_resolved(self):
        for field, value in [('executed', False), ('error', 'readiness failed'), ('cleanup_error', 'close failed')]:
            with self.subTest(field=field):
                case = self.results['cases'][0]
                old = copy.deepcopy(case)
                case[field] = value
                with self.assertRaisesRegex(ValueError, 'unexecuted or failed'):
                    self.run_report()
                self.notes['observations'] = [n for n in self.notes['observations'] if (n['case'], n['viewport']) != ('list', 'wide')]
                report = self.run_report()
                self.assertEqual(report['status'], 'UNCHECKED' if field == 'executed' else 'ERROR')
                self.results['cases'][0] = old
                self.notes['observations'].extend([dict(case='list', viewport='wide', rule=r, status='UNCHECKED',
                                                       object='not observed', observation='pending') for r in ('hierarchy', 'state')])

    def test_identity_and_evidence_rejections(self):
        self.notes['results_sha256'] = 'wrong'
        with self.assertRaisesRegex(ValueError, 'another results'):
            MODULE.finalize(encode(self.results), encode(self.design), encode(self.notes), self.root)
        self.results['input_sha256']['design'] = 'wrong'
        with self.assertRaisesRegex(ValueError, 'Design hash'):
            self.run_report()
        self.results['input_sha256']['design'] = MODULE.digest(encode(self.design))
        self.evidence.write_text('changed evidence')
        with self.assertRaisesRegex(ValueError, 'changed evidence'):
            self.run_report()

    def test_unknown_duplicate_and_missing_observations(self):
        note = copy.deepcopy(self.notes['observations'][0])
        self.notes['observations'].append(note)
        with self.assertRaisesRegex(ValueError, 'Unknown or duplicate'):
            self.run_report()
        self.notes['observations'].pop()
        self.notes['observations'][0]['rule'] = 'other'
        with self.assertRaisesRegex(ValueError, 'Unknown or duplicate'):
            self.run_report()
        self.notes['observations'][0] = note
        note['evidence'] = []
        with self.assertRaisesRegex(ValueError, 'require evidence'):
            self.run_report()
        note['status'] = 'UNCHECKED'
        self.assertEqual(self.run_report()['status'], 'UNCHECKED')


class ScopeTests(unittest.TestCase):
    setUp = FinalizeTests.setUp
    tearDown = FinalizeTests.tearDown

    def bind_scope(self):
        for rule in self.design['rules']:
            rule['description'] = 'Specific fixture requirement'
            if rule['kind'] == 'style':
                rule.update(property='font-size', expected='14px')
        self.project = dict(schema_version=1, project='fixture', base_url='http://127.0.0.1:8765',
                            viewports=[c['viewport'] for c in self.results['cases'][:2]],
                            cases=[dict(id=cid, path='/'+cid, state='ready', ready='true') for cid in ('list','detail')])
        scope = dict(schema_version=1, id='fixture-task', objective='Complete fixture requirements', application='scenario')
        for name, value in [('design',self.design),('project',self.project)]:
            raw = encode(value)
            (self.root / (name+'.json')).write_bytes(raw)
            scope[name] = dict(path=name+'.json', sha256=MODULE.digest(raw))
        self.scope_path = self.root/'scope.json'
        self.scope_path.write_bytes(encode(scope))
        self.results['input_sha256'] = {k:scope[k]['sha256'] for k in ('design','project')}
        self.results['scope'] = MODULE.scope_identity(scope, MODULE.digest(self.scope_path.read_bytes()))

    def run_report(self):
        self.notes['results_sha256'] = MODULE.digest(encode(self.results))
        return MODULE.finalize(encode(self.results), encode(self.design), encode(self.notes), self.root, self.scope_path)

    def test_complete_partial_and_empty_execution(self):
        self.bind_scope()
        report = self.run_report()
        self.assertEqual((report['execution_status'],report['scope_status']),('COMPLETE','COMPLETE'))
        for case in self.results['cases'][2:]:
            case['executed'] = False
            for result in case['results']: result['status'] = 'UNCHECKED'
        self.notes['observations'] = [n for n in self.notes['observations'] if n['case']=='list']
        report = self.run_report()
        self.assertEqual((report['execution_status'],report['scope_status'],report['status']),('COMPLETE','UNCHECKED','UNCHECKED'))
        self.assertIn('完整 scope：尚有未核实项', MODULE.render(report))
        for case in self.results['cases']:
            case['executed'] = False
            for result in case['results']: result['status'] = 'UNCHECKED'
        self.notes['observations'] = []
        self.assertEqual(self.run_report()['execution_status'],'UNCHECKED')

    def test_truncated_and_forged_report_rejected(self):
        self.bind_scope()
        original = copy.deepcopy(self.results)
        mutations = [lambda r:r['cases'].pop(),
                     lambda r:r['cases'][0].update(case='forged'),
                     lambda r:r['cases'][0]['viewport'].update(width=999),
                     lambda r:r['cases'][0]['viewport'].update(id='forged'),
                     lambda r:r['cases'][0].update(path='/other'),
                     lambda r:r['cases'][0].update(state='other'),
                     lambda r:r.update(project='other'),
                     lambda r:r['cases'][0]['results'].pop(),
                     lambda r:r['cases'][0]['results'][0].update(source='other'),
                     lambda r:r['cases'][0]['results'][0].update(role='other'),
                     lambda r:r['cases'][0].update(executed=False),
                     lambda r:r['scope'].update(id='other'),
                     lambda r:r['input_sha256'].update(project='other')]
        for index, mutate in enumerate(mutations):
            self.results = copy.deepcopy(original)
            mutate(self.results)
            with self.subTest(index=index), self.assertRaises(ValueError): self.run_report()

    def test_input_deletion_and_scope_downgrade_rejected(self):
        self.bind_scope()
        for name, key in [('design','rules'),('project','cases'),('project','viewports')]:
            path = self.root/(name+'.json'); raw = path.read_bytes()
            altered = json.loads(raw); altered[key].pop(); path.write_bytes(encode(altered))
            with self.subTest(name=name,key=key), self.assertRaisesRegex(ValueError,'hash differs'): self.run_report()
            path.write_bytes(raw)
        self.notes['results_sha256'] = MODULE.digest(encode(self.results))
        with self.assertRaisesRegex(ValueError,'require --scope'):
            MODULE.finalize(encode(self.results),encode(self.design),encode(self.notes),self.root)
        _,_,inputs = MODULE.load_scope(self.scope_path, self.root/'design.json',self.root/'project.json')
        self.assertEqual(inputs['design'],encode(self.design))
        other = self.root/'same-bytes.json'; other.write_bytes(inputs['design'])
        with self.assertRaisesRegex(ValueError,'identity'): MODULE.load_scope(self.scope_path,other)

    def test_cli_scope_and_legacy_output(self):
        self.bind_scope()
        self.notes['results_sha256'] = MODULE.digest(encode(self.results))
        (self.root/'results.json').write_bytes(encode(self.results))
        (self.root/'observations.json').write_bytes(encode(self.notes))
        command = [sys.executable, str(Path(MODULE.__file__)), '--results',str(self.root/'results.json'),
                   '--observations',str(self.root/'observations.json')]
        run = subprocess.run(command+['--scope',str(self.scope_path),'--output',str(self.root/'delivery')],capture_output=True,text=True)
        self.assertEqual(run.returncode,0,run.stderr)
        self.assertIn('本次实际执行：声明项已完成',run.stdout)
        self.assertIn('完整 scope：声明项已完成',run.stdout)
        wrong = self.root/'copy.json'; wrong.write_bytes(encode(self.design))
        run = subprocess.run(command+['--scope',str(self.scope_path),'--design',str(wrong),'--output',str(self.root/'rejected')],capture_output=True,text=True)
        self.assertEqual(run.returncode,2)
        self.assertFalse((self.root/'rejected').exists())
        del self.results['scope']
        self.notes['results_sha256'] = MODULE.digest(encode(self.results))
        (self.root/'results.json').write_bytes(encode(self.results))
        (self.root/'observations.json').write_bytes(encode(self.notes))
        run = subprocess.run(command+['--design',str(self.root/'design.json'),'--output',str(self.root/'legacy')],capture_output=True,text=True)
        self.assertEqual(run.returncode,0,run.stderr)
        self.assertIn('仅声明子集，无完整目标证明',run.stdout)

    def test_legacy_reports_have_no_complete_scope_proof(self):
        self.notes['results_sha256'] = MODULE.digest(encode(self.results))
        report = MODULE.finalize(encode(self.results),encode(self.design),encode(self.notes),self.root)
        self.assertEqual(report['status'],'COMPLETE')
        self.assertEqual(report['scope_status'],'UNPROVEN')
        self.assertIn('仅声明子集，无完整目标证明',MODULE.render(report))


if __name__ == '__main__':
    unittest.main()
