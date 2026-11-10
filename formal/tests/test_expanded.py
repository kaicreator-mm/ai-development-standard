import importlib.util
import json
import os
import shutil
import sys
import tempfile
import types
import unittest
from unittest import mock
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / 'suite' / 'expanded.py'
sys.path.insert(0, str(MODULE.parent))  # direct importlib loader needs adjacent helpers
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
            stub.write_text('#!/bin/sh\necho invalid-proof-output\n')
            stub.chmod(0o755)
            opts = self.options()
            opts.z3 = str(stub)
            opts.cvc5 = str(stub)
            opts.property = 'ADS-P-AUT'
            opts.strict_source = True
            opts.out = str(Path(tmp) / 'receipt.json')
            spec = json.loads(SUITE.read_text())
            # This test isolates the R5 severity-precedence rule.  The stub
            # only stands in for a trusted solver when identity is mocked PASS.
            with mock.patch.object(runner, 'toolchain_alignment',
                                   return_value={'status': 'PASS', 'checks': []}):
                self.assertEqual(runner.main_v1(opts, SUITE, spec), 2)
            report = json.loads(Path(opts.out).read_text())
            self.assertEqual(report['model_verdict'], 'FAIL')
            self.assertEqual(report['source_alignment']['status'], 'NOT_RUN')

    def test_traceability_bidirectional_and_dependency_cycle(self):
        spec={"candidate_head":"c", "cases":[{"id":"case", "model_id":"M", "property_id":"P"}]}
        index={"candidate_head":"c","properties":[{"id":"P","model_id":"M","sources":["a"]}]}
        source={"candidate_head":"c","sources":[{"path":"a","blob":"a"*40,"anchors":["rule"]}]}
        trace={"subject_head":"c",
               "properties":[{"property_id":"P","case_ids":["case"],"source_paths":["a"]}],
               "sources":[{"path":"a","property_ids":["P"],"blob":"a"*40,"anchors":["rule","extra"]}]}
        self.assertEqual(runner.audit_traceability(spec,index,trace,source)["status"],"PASS")
        broken=json.loads(json.dumps(trace))
        broken["sources"][0]["property_ids"]=[]
        with self.assertRaisesRegex(ValueError,"reverse source-property"):
            runner.audit_traceability(spec,index,broken,source)
        index["properties"][0]["depends_on"]=["P"]
        with self.assertRaisesRegex(ValueError,"invalid dependency"):
            runner.audit_traceability(spec,index,trace,source)
        index["properties"][0]["depends_on"]=[]
        merged=runner.combine_source_anchors(source,trace)
        self.assertEqual(merged["sources"][0]["anchors"],["rule","extra"])
        corrupted=json.loads(json.dumps(trace))
        corrupted["sources"][0]["blob"]="0"*40
        with self.assertRaisesRegex(ValueError,"provenance blob mismatch"):
            runner.audit_traceability(spec,index,corrupted,source)
        corrupted=json.loads(json.dumps(trace))
        corrupted["sources"][0]["anchors"]=[]
        with self.assertRaisesRegex(ValueError,"trace source anchors"):
            runner.audit_traceability(spec,index,corrupted,source)
        trace["subject_head"]="old"
        with self.assertRaisesRegex(ValueError,"candidate SHA"):
            runner.audit_traceability(spec,index,trace,source)

    def test_bad_model_pin_blocks_before_tool_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            opts = self.options()
            opts.model_head = "0" * 40
            opts.strict_source = True
            opts.property = "ADS-P-AUT"
            opts.out = str(Path(tmp) / "invalid-head.json")
            spec = json.loads(SUITE.read_text())
            self.assertEqual(runner.main_v1(opts, SUITE, spec), 2)
            receipt = json.loads(Path(opts.out).read_text())
            self.assertEqual(receipt["model_verdict"], "BLOCKED")
            self.assertEqual(receipt["model_input_alignment_before"]["status"], "BLOCKED")
            self.assertEqual(receipt["checks"], [])

    def test_solver_differential_does_not_overwrite_model_results(self):
        from differential import solver_differential
        cases = []
        results = []
        for key, answer in (("model-a.smt2", "unsat"), ("model-b.smt2", "sat")):
            for tool in ("z3", "cvc5"):
                cid = key + "-" + tool
                cases.append({"id": cid, "model": key, "property_id": "P",
                              "tool": tool, "purpose": "proof"})
                results.append({"id": cid, "status": "PASS_MODEL",
                                "expected": [answer], "actual": {"answers": [answer]},
                                "inputs_sha256": {"model": key}})
        self.assertEqual([p["status"] for p in solver_differential(cases, results)],
                         ["PASS", "PASS"])
        results[-1]["actual"] = {"answers": ["unsat"]}
        self.assertEqual([p["status"] for p in solver_differential(cases, results)],
                         ["PASS", "INCONCLUSIVE"])

    def test_strict_source_rejects_unknown_tool_identity_and_zeroes_coverage(self):
        with tempfile.TemporaryDirectory() as tmp:
            fake = Path(tmp) / 'untrusted-z3'
            fake.write_text('#!/bin/sh\necho "Z3 version 5.3.3 cvc5 1.4.2"\n')
            fake.chmod(0o755)
            opts = self.options()
            opts.z3 = str(fake)
            opts.cvc5 = str(fake)
            opts.property = 'ADS-P-AUT'
            opts.strict_source = True
            opts.model_head = 'a' * 40
            opts.source_checkout = tmp
            opts.out = str(Path(tmp) / 'tool-check.json')
            spec = json.loads(SUITE.read_text())
            def mocked_result(case, root, options):
                return {
                    'id': case['id'], 'tool': case['tool'],
                    'property_id': case['property_id'], 'model_id': case['model_id'],
                    'purpose': case['purpose'],
                    'status': 'COUNTEREXAMPLE' if case['purpose'] == 'mutation' else 'PASS_MODEL',
                    'actual': {'answers': case['expect']},
                    'expected': case['expect'],
                    'inputs_sha256': {'model': case['model']}
                }
            with (
                mock.patch.object(runner, 'model_alignment', return_value={'status':'PASS'}),
                mock.patch.object(runner, 'source_alignment', return_value={'status':'PASS'}),
                mock.patch.object(runner, 'run_case', side_effect=mocked_result),
            ):
                self.assertEqual(runner.main_v1(opts, SUITE, spec), 2)
            receipt = json.loads(Path(opts.out).read_text())
            self.assertEqual(receipt['model_verdict'], 'BLOCKED')
            self.assertEqual(receipt['toolchain_alignment_before']['status'], 'FAIL')
            self.assertEqual(receipt['toolchain_alignment_after']['status'], 'FAIL')
            self.assertEqual(receipt['coverage']['source_bound_verified_obligations'], 0)

    def test_missing_tlc_emits_typed_not_run_and_nonzero_receipt(self):
        suite_path = ROOT / 'v4.19' / 'r8' / 'suite.json'
        with tempfile.TemporaryDirectory() as tmp:
            opts = self.options()
            opts.property = 'ADS-P-LC'
            opts.tlc_jar = str(Path(tmp) / 'absent-tlc.jar')
            opts.strict_source = True
            opts.out = str(Path(tmp) / 'tlc-missing-receipt.json')
            spec = json.loads(suite_path.read_text())
            selected = [c for c in spec['cases'] if c['property_id'] == 'ADS-P-LC']
            self.assertEqual(len(selected), 3)
            for c in selected:
                row = runner.run_case(c, ROOT, opts)
                self.assertEqual(row['status'], 'NOT_RUN')
                self.assertEqual(row['property_id'], 'ADS-P-LC')
                self.assertEqual(row['purpose'], c['purpose'])
                self.assertEqual(row['expected'], c['expect'])
                self.assertIsNone(row['exit_code'])
            self.assertEqual(runner.main_v1(opts, suite_path, spec), 2)
            receipt = json.loads(Path(opts.out).read_text())
            self.assertEqual(receipt['model_verdict'], 'BLOCKED')
            self.assertEqual(receipt['coverage']['source_bound_verified_obligations'], 0)
            self.assertEqual(receipt['toolchain_alignment_before']['status'], 'NOT_RUN')
            self.assertEqual(receipt['selection']['selected_case_count'], 3)
            self.assertTrue(Path(opts.out).is_file())

    def test_tampered_native_tool_never_executes(self):
        with tempfile.TemporaryDirectory() as tmp:
            opts = self.options()
            opts.property = 'ADS-P-AUT'
            opts.z3 = str(Path(tmp) / 'fake-z3')
            Path(opts.z3).write_text('#!/bin/sh\\necho unsat\\n')
            Path(opts.z3).chmod(0o755)
            opts.cvc5 = opts.z3
            opts.strict_source = True
            opts.out = str(Path(tmp) / 'untrusted-tool.json')
            spec = json.loads(SUITE.read_text())
            with mock.patch.object(runner, 'run_case', side_effect=AssertionError('must not execute')) as run:
                self.assertEqual(runner.main_v1(opts, SUITE, spec), 2)
                run.assert_not_called()
            receipt = json.loads(Path(opts.out).read_text())
            self.assertEqual(receipt['model_verdict'], 'BLOCKED')
            self.assertEqual(receipt['checks'], [])
            self.assertEqual(receipt['coverage']['source_bound_verified_obligations'], 0)

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
