import copy
import importlib.util
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('batch', ROOT / 'verify-ui.py')
batch = importlib.util.module_from_spec(spec); spec.loader.exec_module(batch)


class BatchTests(unittest.TestCase):
    def setUp(self):
        self.design = json.loads((ROOT / 'examples/effective-design.json').read_text())
        self.project = json.loads((ROOT / 'examples/project.json').read_text())

    def test_template_identity_needs_source_not_version(self):
        self.assertNotIn('version', self.design['template'])
        batch.validate(self.design, self.project)
        legacy = copy.deepcopy(self.design)
        legacy['template']['version'] = '1'
        batch.validate(legacy, self.project)
        for field in ('id', 'source'):
            altered = copy.deepcopy(self.design)
            altered['template'][field] = ''
            with self.subTest(field=field), self.assertRaises(ValueError):
                batch.validate(altered, self.project)

    def test_invalid_inputs_rejected(self):
        for field, value in [('kind', 'unimplemented'), ('source', ''), ('id', '')]:
            d = copy.deepcopy(self.design); d['rules'][0][field] = value
            with self.subTest(field=field), self.assertRaises((ValueError, KeyError)):
                batch.validate(d, self.project)
        p = copy.deepcopy(self.project); p['cases'][0]['exclude'] = {'value-size': ''}
        with self.assertRaises(ValueError): batch.validate(self.design, p)
        p = copy.deepcopy(self.project); p['cases'][0]['path'] = '//other-host/'
        with self.assertRaises(ValueError): batch.validate(self.design, p)
        scale = dict(id='scale', role='value', kind='allowed-values', property='font-size', allowed=['14px'], source='fixture scale', description='Type scale')
        for broken in ({'allowed': []}, {'allowed': [14]}, {'property': ''}, {'own_text': 'yes'}):
            d = copy.deepcopy(self.design); d['rules'].append({**scale, **broken})
            with self.subTest(broken=broken), self.assertRaises(ValueError):
                batch.validate(d, self.project)
        p = copy.deepcopy(self.project); p['roles']['value']['exclude'] = ''
        with self.assertRaises(ValueError): batch.validate(self.design, p)

    def test_real_browser_controls(self):
        class Handler(SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs): super().__init__(*args, directory=str(ROOT / 'examples'), **kwargs)
            def log_message(self, *_): pass
        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
        try:
            with tempfile.TemporaryDirectory() as temp:
                folder = Path(temp)
                self.design['rules'].extend([
                    dict(id='collapsed-child',role='collapsed-child',kind='count',expected=0,source='Closed details fixture',description='Closed descendants are not visible'),
                    dict(id='boot-width',role='boot',kind='predicate',source='Fixture initial layout',description='Initial viewport equals declared viewport'),
                    dict(id='visible-child',role='visible-child',kind='count',expected=1,source='CSS visibility inheritance',description='Visible child overrides hidden parent'),
                    dict(id='visible-not-zero',role='visible-child',kind='count',expected=0,source='Known failure control',description='Must detect the visible child'),
                    dict(id='type-scale',role='scale',kind='allowed-values',property='font-size',allowed=['12px','14px'],own_text=True,source='Fixture type scale',description='Every text sample sits on the scale; the brand is excluded'),
                    dict(id='page-overflow',role='page',kind='no-horizontal-overflow',source='Fixture page width',description='The page does not scroll sideways')])
                self.project['roles'].update({'collapsed-child':{'selector':'#collapsed-child'},'boot':{'expression':"({pass:Number(document.documentElement.dataset.bootWidth)===innerWidth,samples:1,detail:'initial viewport'})"},'visible-child':{'selector':'#visible-child'},
                                              'scale':{'selector':'.scale','exclude':'.brand'},'page':{'selector':'html'}})
                good = self.project['cases'][0]
                bad = copy.deepcopy(good); bad.update(id='bad', path='/fixture.html?broken=1', state='broken sizing and missing failure')
                # Inspect the broken state without blocking all other checks on its disabled disclosure.
                bad['steps'] = []
                missing = copy.deepcopy(good); missing.update(id='missing', roles={'value':{'selector':'.does-not-exist'}})
                na = copy.deepcopy(good); na.update(id='na', exclude={'canvas':'This fixture case has no chart'})
                timeout = copy.deepcopy(good); timeout.update(id='timeout', ready='false', steps=[])
                self.project.update(base_url=f'http://127.0.0.1:{server.server_port}', cases=[good,bad,missing,na,timeout])
                (folder/'design.json').write_text(json.dumps(self.design)); (folder/'project.json').write_text(json.dumps(self.project))
                scope = dict(schema_version=1,id='browser-fixture',objective='All fixture cases and widths',application='scenario')
                for name in ('design','project'):
                    scope[name] = dict(path=name+'.json',sha256=batch.hashlib.sha256((folder/(name+'.json')).read_bytes()).hexdigest())
                (folder/'scope.json').write_text(json.dumps(scope))
                cmd = [sys.executable, str(ROOT/'verify-ui.py'), '--design', str(folder/'design.json'), '--project', str(folder/'project.json'),
                       '--scope',str(folder/'scope.json'), '--output', str(folder/'results'), '--jobs','2','--capacity-reason','Two isolated contexts sharing local CPU and fixture server', '--timeout','3','--direct']
                p = subprocess.run(cmd, capture_output=True, text=True, timeout=160)
                self.assertEqual(p.returncode, 2, p.stdout+p.stderr) # readiness timeout is an execution issue
                report = json.loads((folder/'results/results.json').read_text())
                self.assertEqual(len(report['cases']),10)
                self.assertEqual(report['scope']['id'],'browser-fixture')
                for case in report['cases']:
                    self.assertNotIn('cleanup_error',case)
                    results = {r['rule']:r['status'] for r in case['results']}
                    if case['case']=='timeout':
                        self.assertEqual(set(results.values()),{'UNCHECKED'})
                    else:
                        self.assertNotIn('error',case,case)
                        self.assertEqual(results['neutral'],'PASS')
                        self.assertEqual(results['boot-width'],'PASS')
                        self.assertEqual(results['collapsed-child'],'PASS')
                        self.assertEqual(results['visible-child'],'PASS')
                        self.assertEqual(results['visible-not-zero'],'FAIL')
                        self.assertEqual(results['canvas'],'NA' if case['case']=='na' else 'UNCHECKED')
                        self.assertEqual(results['value-size'], {'bad':'FAIL','missing':'UNCHECKED'}.get(case['case'],'PASS'))
                        self.assertEqual(results['summary'],'FAIL' if case['case']=='bad' else 'PASS')
                        self.assertEqual(results['data'],'FAIL' if case['case']=='bad' else 'PASS')
                        self.assertIn('/fixture.css', case['assets'])
                        details = {r['rule']: r for r in case['results']}
                        if case['case'] == 'bad':
                            self.assertEqual(results['type-scale'], 'FAIL')
                            self.assertEqual([(f['observed'], f['count'], f['elements']) for f in details['type-scale']['failures']], [('13px', 1, ['span#body-text.scale'])])
                            self.assertEqual(results['page-overflow'], 'FAIL')
                            culprits = [c['element'] for f in details['page-overflow']['failures'] for c in f['culprits']]
                            self.assertEqual(culprits, ['div#page-wide.wide'])  # the scroller-clipped decoy is not blamed
                        else:
                            self.assertEqual(results['type-scale'], 'PASS')
                            self.assertEqual(details['type-scale']['samples'], 2)  # brand sample excluded
                            self.assertEqual(results['page-overflow'], 'PASS')
                # Same input identity, intentionally narrow rerun: never import previous green values.
                cmd[cmd.index(str(folder/'results'))] = str(folder/'rerun')
                for flag in ('--design','--project'):
                    index = cmd.index(flag); del cmd[index:index+2]
                p = subprocess.run(cmd+['--case','na'],capture_output=True,text=True,timeout=60)
                self.assertEqual(p.returncode,1,p.stdout+p.stderr)
                rerun=json.loads((folder/'rerun/results.json').read_text())
                self.assertEqual(sum(c['executed'] for c in rerun['cases']),2)
                self.assertTrue(all(r['status']=='UNCHECKED' for c in rerun['cases'] if not c['executed'] for r in c['results']))
        finally:
            server.shutdown(); server.server_close(); thread.join()

if __name__=='__main__': unittest.main()
