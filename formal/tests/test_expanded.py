import importlib.util
import json
import os
import shutil
import tempfile
import types
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / 'suite' / 'expanded.py'
spec = importlib.util.spec_from_file_location('ads_formal_expanded', MODULE)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)
ROOT = MODULE.parents[1]
SUITE = ROOT / 'v4.19' / 'r1' / 'suite.json'

class ExpandedTests(unittest.TestCase):
    def test_paths_are_restricted(self):
        with self.assertRaises(ValueError): runner.safe_path(ROOT, '../../etc/passwd')
        with self.assertRaises(ValueError): runner.safe_path(ROOT, '/etc/passwd')

    def test_source_not_guessed(self):
        self.assertEqual(runner.source_alignment(None, {'candidate_head':'a'})['status'], 'NOT_RUN')
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(runner.source_alignment(tmp, {'candidate_head':'a'})['status'], 'BLOCKED')

    @staticmethod
    def options():
        return types.SimpleNamespace(
            z3=os.environ.get('ADS_FORMAL_Z3', shutil.which('z3') or '__missing_z3__'),
            cvc5=os.environ.get('ADS_FORMAL_CVC5', shutil.which('cvc5') or '__missing_cvc5__'),
            java='java', tlc_jar=os.environ.get('ADS_FORMAL_TLC_JAR', '/missing/tlc.jar'),
            source_checkout=None, strict_source=False, model=None, property=None,
            changed_source=None, out='/tmp/ads-formal-test-receipt.json')

    def test_unknown_solver_is_inconclusive(self):
        with tempfile.TemporaryDirectory() as tmp:
            stub = Path(tmp) / 'fake-solver'
            stub.write_text('#!/bin/sh\necho unknown\n')
            stub.chmod(0o755)
            opts = self.options()
            opts.z3 = str(stub)
            case = {'id':'unknown','tool':'z3','purpose':'proof','model':'models/authority/claim.smt2',
                    'model_id':'ADS-M-AUTHORITY','property_id':'ADS-P-AUT', 'expect':['unsat']*4+['sat']}
            self.assertEqual(runner.run_case(case, ROOT, opts)['status'], 'INCONCLUSIVE')

    def test_transitive_source_invalidation(self):
        entries = [
            {"id": "A", "sources": ["scripts/v34_rules.py"]},
            {"id": "B", "sources": [], "depends_on": ["A"]},
            {"id": "C", "sources": ["other"], "depends_on": ["B"]},
            {"id": "D", "sources": ["unrelated"]}
        ]
        self.assertEqual(runner.affected_properties(entries, ["scripts/v34_rules.py"]), ["A", "B", "C"])
        self.assertEqual(runner.affected_properties(entries, ["unmapped"]), [])

    def test_strict_source_does_not_mask_model_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            stub = Path(tmp) / 'fake-solver'
            stub.write_text('#!/bin/sh\\necho invalid-proof-output\\n')
            stub.chmod(0o755)
            opts = self.options()
            opts.z3 = str(stub)
            opts.cvc5 = str(stub)
            opts.property = 'ADS-P-AUT'
            opts.strict_source = True
            opts.out = str(Path(tmp) / 'receipt.json')
            spec = json.loads(SUITE.read_text())
            self.assertEqual(runner.main_v1(opts, SUITE, spec), 2)
            report = json.loads(Path(opts.out).read_text())
            self.assertEqual(report['model_verdict'], 'FAIL')
            self.assertEqual(report['source_alignment']['status'], 'NOT_RUN')

    def test_missing_solver_not_pass(self):
        opts=self.options()
        opts.z3='__missing_ads_solver__'
        case={'id':'no-solver','tool':'z3','purpose':'proof','model':'models/authority/claim.smt2',
              'model_id':'ADS-M-AUTHORITY','property_id':'ADS-P-AUT','expect':['unsat']*4+['sat']}
        self.assertEqual(runner.run_case(case, ROOT, opts)['status'], 'NOT_RUN')

    @unittest.skipUnless(os.environ.get('ADS_FORMAL_Z3') and os.environ.get('ADS_FORMAL_CVC5'), 'native solvers not configured')
    def test_proof_and_mutant(self):
        opts=self.options()
        spec=json.loads(SUITE.read_text())
        results=[runner.run_case(x, ROOT,opts) for x in spec['cases']]
        self.assertEqual(sum(x['status']=='PASS_MODEL' for x in results),10)
        self.assertEqual(sum(x['status']=='COUNTEREXAMPLE' for x in results),2)

    @unittest.skipUnless(os.environ.get('ADS_FORMAL_Z3') and os.environ.get('ADS_FORMAL_CVC5'), 'native solvers not configured')
    def test_diff_recheck_never_claims_current_source(self):
        opts=self.options()
        opts.changed_source=['standards/EXECUTION_PACK_STANDARD.md']
        spec=json.loads(SUITE.read_text())
        self.assertEqual(runner.main_v1(opts,SUITE,spec),2)
        r=json.loads(Path(opts.out).read_text())
        self.assertEqual(r['source_alignment']['status'],'STALE')
        self.assertEqual(r['model_verdict'],'BLOCKED')
        self.assertIn('ADS-P-AUT',r['affected_property_ids'])

    @unittest.skipUnless(os.environ.get('ADS_FORMAL_Z3') and os.environ.get('ADS_FORMAL_CVC5'), 'native solvers not configured')
    def test_strict_without_exact_checkout_blocked(self):
        opts=self.options()
        opts.strict_source=True
        spec=json.loads(SUITE.read_text())
        self.assertEqual(runner.main_v1(opts,SUITE,spec),2)
        r=json.loads(Path(opts.out).read_text())
        self.assertEqual(r['model_verdict'],'BLOCKED')

if __name__ == '__main__':
    unittest.main()
