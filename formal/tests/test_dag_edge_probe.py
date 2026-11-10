"""DAG edge evidence and authority-preserving adversarial unit tests."""
import importlib.util
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / 'v4.19' / 'coverage' / 'dag_edge_probe.py'
spec = importlib.util.spec_from_file_location('ads_dag_edge_probe', MODULE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

BASE = {'edge': 'A -> B', 'frozen_contract_ref': 'exact-contract-sha:path',
        'code_baseline_required': False, 'write_set_conflict': False,
        'join_only': True, 'native_dependency': True}


class DagEdgeProbeTests(unittest.TestCase):
    def test_join_only_reports_candidate_but_no_admission(self):
        v = module.assess_edge(BASE)
        self.assertEqual(v['classification'], 'POSSIBLE_FALSE_SERIAL_EDGE')
        self.assertEqual(v['dispatch'], 'HOLD_NATIVE_DEPENDENCY')
        self.assertFalse(v['may_mutate_native_dependencies'])
    def test_source_baseline_requirement_is_material(self):
        self.assertEqual(module.assess_edge({**BASE, 'code_baseline_required': True})['classification'],
                         'MATERIAL_SERIAL_EDGE')
    def test_overlapping_writes_remain_serial(self):
        self.assertEqual(module.assess_edge({**BASE, 'write_set_conflict': True})['classification'],
                         'MATERIAL_SERIAL_EDGE')
    def test_unknown_contract_cannot_authorize(self):
        v = module.assess_edge({**BASE, 'frozen_contract_ref': ''})
        self.assertEqual((v['classification'], v['dispatch']), ('UNKNOWN', 'NOT_AUTHORIZED'))
    def test_source_preparation_is_not_task_dispatch(self):
        v = module.assess_edge({**BASE, 'native_dependency': False})
        self.assertEqual(v['dispatch'], 'NOT_AUTHORIZED')
        self.assertEqual(v['parallel_source_preparation'], 'ONLY_IF_INDEPENDENTLY_AUTHORIZED')
    def test_type_confusion_fails_closed(self):
        v = module.assess_edge({**BASE, 'write_set_conflict': 'false'})
        self.assertEqual(v['classification'], 'UNKNOWN')
    def test_composite_demo(self):
        self.assertEqual(module.run_demo()['verdict'],
                         'PASS_FALSE_SERIAL_ADVISORY_WITHOUT_BYPASSING_NATIVE_DAG')


if __name__ == '__main__':
    unittest.main()
