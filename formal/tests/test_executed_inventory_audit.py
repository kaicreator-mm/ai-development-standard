"""R20: adversarial checks of inventory auditor (local synthetic fixtures only)."""
import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

MODULE = Path(__file__).resolve().parents[1] / "coverage" / "executed_inventory_audit.py"
spec = importlib.util.spec_from_file_location("ads_r20_audit", MODULE)
audit_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit_mod)


class TestExecutedInventoryAudit(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="ads-r20-audit-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.paths = audit_mod.SOURCE_FILES
        self.declared = []
        for path, cls, n in zip(self.paths, ("Seven", "Six"), (7, 6), strict=True):
            names = [f"test_{j}" for j in range(n)]
            source = "import unittest\nclass %s(unittest.TestCase):\n" % cls
            source += "".join(f"    def {name}(self): pass\n" for name in names)
            self.write(path, source)
            self.declared.extend(f"{Path(path).stem}.{cls}.{name}" for name in names)
        self.log_ids = sorted(self.declared)
        self.make_records()
        self.repin()

    def write(self, path, text):
        file = self.root / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(text, encoding="utf-8")

    def make_records(self, status="ok", counts=(13, 13), ids=None):
        if ids is None:
            ids = self.log_ids
        log = []
        for idx, os_name in enumerate(("WSL2 Ubuntu", "Windows"), start=1):
            log.append(f"== R17 Python input-binding tests — environment {idx}: {os_name} ==\n")
            log.extend(f"{ident.split('.')[-1]} ({ident}) ... {status}\n" for ident in ids)
            log.append(f"\nRan {counts[idx - 1]} tests in 0.01s\n\nOK\n\n")
        joined = "".join(log)
        self.write(audit_mod.LOG_PATH, joined)
        records = {
            "worktree": {"head_at_execution": audit_mod.SUBJECT_HEAD},
            "combined_log_sha256": hashlib.sha256(joined.encode()).hexdigest(),
            "tested_code": {"test_files": [{"path": path, "git_blob": audit_mod.git_blob((self.root / path).read_bytes()), "tests": n}
                                           for path, n in zip(self.paths, (7, 6), strict=True)]},
            "executions": [{"environment": name, "tests_run": len(ids), "exit_code": 0,
                            "skipped": 0, "errors": 0, "failures": 0, "result": "OK"}
                           for name in ("WSL2 Ubuntu", "Windows")],
        }
        self.write(audit_mod.RECEIPT_PATH, json.dumps(records))

    def repin(self):
        self.pins = {path: audit_mod.git_blob((self.root / path).read_bytes())
                     for path in (*self.paths, audit_mod.LOG_PATH, audit_mod.RECEIPT_PATH)}
        patch = mock.patch.object(audit_mod, "PINNED", self.pins)
        patch.start()
        self.addCleanup(patch.stop)

    def replace_pin(self, path):
        self.pins[path] = audit_mod.git_blob((self.root / path).read_bytes())

    def test_exact_declared_executed_id_set_passes(self):
        result = audit_mod.audit(self.root)
        self.assertEqual(result["status"], "PASS_RECORDED_EXACT_BLOB_EXECUTION_INVENTORY")
        self.assertEqual(len(result["environments"]), 2)
        self.assertEqual(result["declared_count"], 13)

    def test_green_summary_cannot_hide_missing_method(self):
        self.make_records(ids=self.log_ids[:-1], counts=(12, 12))
        for path in (audit_mod.LOG_PATH, audit_mod.RECEIPT_PATH):
            self.replace_pin(path)
        with self.assertRaisesRegex(audit_mod.AuditBlocked, "missing/extra"):
            audit_mod.audit(self.root)

    def test_green_summary_cannot_hide_duplicate_method(self):
        self.make_records(ids=self.log_ids[:-1] + [self.log_ids[0]])
        for path in (audit_mod.LOG_PATH, audit_mod.RECEIPT_PATH):
            self.replace_pin(path)
        with self.assertRaisesRegex(audit_mod.AuditBlocked, "duplicate executed"):
            audit_mod.audit(self.root)

    def test_non_ok_method_cannot_pass_green_summary(self):
        self.make_records(status="FAIL")
        for path in (audit_mod.LOG_PATH, audit_mod.RECEIPT_PATH):
            self.replace_pin(path)
        with self.assertRaisesRegex(audit_mod.AuditBlocked, "non-OK"):
            audit_mod.audit(self.root)

    def test_source_tamper_blocks_before_semantic_read(self):
        path = self.paths[0]
        with (self.root / path).open("a", encoding="utf-8") as f:
            f.write("# edited without review\n")
        with self.assertRaisesRegex(audit_mod.AuditBlocked, "Git blob mismatch"):
            audit_mod.audit(self.root)

    def test_bad_receipt_subject_head_blocks(self):
        receipt = json.loads((self.root / audit_mod.RECEIPT_PATH).read_text())
        receipt["worktree"]["head_at_execution"] = "0" * 40
        self.write(audit_mod.RECEIPT_PATH, json.dumps(receipt))
        self.replace_pin(audit_mod.RECEIPT_PATH)
        with self.assertRaisesRegex(audit_mod.AuditBlocked, "wrong exact execution HEAD"):
            audit_mod.audit(self.root)

    def test_credible_count_but_false_receipt_test_blob_blocks(self):
        receipt = json.loads((self.root / audit_mod.RECEIPT_PATH).read_text())
        receipt["tested_code"]["test_files"][0]["git_blob"] = "f" * 40
        self.write(audit_mod.RECEIPT_PATH, json.dumps(receipt))
        self.replace_pin(audit_mod.RECEIPT_PATH)
        with self.assertRaisesRegex(audit_mod.AuditBlocked, "source/count provenance mismatch"):
            audit_mod.audit(self.root)

    def test_log_drift_without_new_pin_blocks(self):
        with (self.root / audit_mod.LOG_PATH).open("a", encoding="utf-8") as f:
            f.write("invisible change\n")
        with self.assertRaisesRegex(audit_mod.AuditBlocked, "Git blob mismatch"):
            audit_mod.audit(self.root)

    def test_wrong_execution_environment_disallowed(self):
        receipt = json.loads((self.root / audit_mod.RECEIPT_PATH).read_text())
        receipt["executions"][1]["environment"] = "Linux 2"
        self.write(audit_mod.RECEIPT_PATH, json.dumps(receipt))
        self.replace_pin(audit_mod.RECEIPT_PATH)
        with self.assertRaisesRegex(audit_mod.AuditBlocked, "execution environment metadata"):
            audit_mod.audit(self.root)


if __name__ == "__main__":
    unittest.main()
