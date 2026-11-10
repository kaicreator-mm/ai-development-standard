"""Test real independent subprocess execution, not a green test-runner label."""
import tempfile
import unittest
import importlib.util
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "v4.19" / "coverage" / "discovery_probe.py"
spec = importlib.util.spec_from_file_location("ads_formal_discovery_probe", MODULE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
REQUIRED, build_fixture, examine, run_demo = (mod.REQUIRED, mod.build_fixture, mod.examine, mod.run_demo)


class TestDiscoveryProbe(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="ads-formal-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = build_fixture(self.temp.name)

    def test_green_filtered_run_does_not_qualify_required_suite(self):
        actual = examine(self.root, "test_root.py")
        self.assertEqual(actual["subset_execution_status"], "PASS")
        self.assertEqual(actual["observed_executed_count"], 1)
        self.assertFalse(actual["declared_coverage_qualified"])
        self.assertEqual(actual["required_suite_status"], "NOT_RUN")

    def test_missing_nested_required_id_is_provable(self):
        actual = examine(self.root, "test_root.py")
        self.assertEqual(actual["missing_required_test_ids"], [REQUIRED[0]])
        self.assertEqual(actual["observed_executed_test_ids"], [REQUIRED[1]])

    def test_accurate_discovery_executes_both(self):
        actual = examine(self.root, "test_*.py")
        self.assertEqual(actual["subset_execution_status"], "PASS")
        self.assertEqual(actual["required_suite_status"], "PASS")
        self.assertEqual(actual["observed_executed_count"], 2)
        self.assertTrue(actual["declared_coverage_qualified"])

    def test_demo_negative_and_positive(self):
        self.assertEqual(run_demo()["verdict"],
                         "PASS_GREEN_COMMAND_WITH_OMITTED_REQUIRED_TEST_DETECTED")


if __name__ == "__main__":
    unittest.main()
