"""Bounded Python test-selection probe using executed-test sentinels, not a claimed glob."""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REQUIRED = (
    "nested.test_nested.NestedTests.test_nested",
    "test_root.RootTests.test_root",
)


def build_fixture(root):
    tests = Path(root) / "tests"
    nested = tests / "nested"
    nested.mkdir(parents=True, exist_ok=True)
    (nested / "__init__.py").write_text("", encoding="utf-8")
    (tests / "test_root.py").write_text(
        "import unittest\nfrom pathlib import Path\nclass RootTests(unittest.TestCase):\n"
        "    def test_root(self):\n"
        "        Path(__file__).with_suffix('.ran').write_text('test_root.RootTests.test_root')\n"
        "        self.assertTrue(True)\n", encoding="utf-8")
    (nested / "test_nested.py").write_text(
        "import unittest\nfrom pathlib import Path\nclass NestedTests(unittest.TestCase):\n"
        "    def test_nested(self):\n"
        "        Path(__file__).with_suffix('.ran').write_text('nested.test_nested.NestedTests.test_nested')\n"
        "        self.assertTrue(True)\n", encoding="utf-8")
    return tests


def examine(test_root, pattern):
    """A green test command proves only the actually executed test IDs."""
    root = Path(test_root).resolve()
    for marker in root.rglob("*.ran"):
        marker.unlink()
    run = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(root),
         "-t", str(root), "-p", pattern, "-v"], cwd=root,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, errors="replace", timeout=20, check=False)
    observed = sorted(p.read_text("utf-8") for p in root.rglob("*.ran"))
    missing = sorted(set(REQUIRED) - set(observed))
    extra = sorted(set(observed) - set(REQUIRED))
    count_match = re.search(r"Ran (\d+) tests? in ", run.stdout)
    declared_count = int(count_match.group(1)) if count_match else None
    actual = "PASS" if run.returncode == 0 and declared_count == len(observed) else "FAIL"
    return {
        "pattern": pattern,
        "declared_required_test_ids": list(REQUIRED),
        "observed_executed_test_ids": observed,
        "command_reported_test_count": declared_count,
        "observed_executed_count": len(observed),
        "subset_execution_status": actual,
        "missing_required_test_ids": missing,
        "unclaimed_extra_test_ids": extra,
        "required_suite_status": (
            "PASS" if actual == "PASS" and not missing and not extra
            else "NOT_RUN" if missing else "FAIL"),
        "declared_coverage_qualified": actual == "PASS" and not missing and not extra,
    }


def run_demo():
    with tempfile.TemporaryDirectory(prefix="ads-formal-discovery-") as tmp:
        root = build_fixture(tmp)
        bad = examine(root, "test_root.py")
        good = examine(root, "test_*.py")
    assert bad["subset_execution_status"] == "PASS"
    assert bad["required_suite_status"] == "NOT_RUN"
    assert bad["missing_required_test_ids"] == [REQUIRED[0]]
    assert good["required_suite_status"] == "PASS"
    assert good["observed_executed_count"] == 2
    return {
        "schema": "ads/formal-test-discovery-probe/v1",
        "kind": "SYNTHETIC_PYTHON_NEGATIVE_AND_POSITIVE_DEMO_NOT_ADS_RULE_PROOF",
        "scenario": "One root test and one nested required test, with execution sentinels",
        "negative": bad,
        "positive": good,
        "verdict": "PASS_GREEN_COMMAND_WITH_OMITTED_REQUIRED_TEST_DETECTED",
        "not_proven": ["No real project CI profile or external test runner was exercised",
                       "No ADS normative language-to-runtime equivalence theorem"],
    }


if __name__ == "__main__":
    print(json.dumps(run_demo(), indent=2, ensure_ascii=False))
