"""Toolchain pinning is tested with controlled executables, no real solver required."""
import hashlib
import importlib.util
import tempfile
import types
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / "suite" / "toolchain.py"
spec = importlib.util.spec_from_file_location("ads_formal_toolchain", MODULE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class ToolchainTests(unittest.TestCase):
    def test_exact_version_and_hash_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            executable = Path(tmp) / "fake-z3"
            executable.write_text("#!/bin/sh\necho 'Z3 version 5.3.3 - 64 bit'\n")
            executable.chmod(0o755)
            digest = hashlib.sha256(executable.read_bytes()).hexdigest()
            inventory = {"smokes": {"z3": {"binary_sha256": digest, "version": "5.3.3"}}}
            opts = types.SimpleNamespace(z3=str(executable))
            selected = [{"tool": "z3"}]
            self.assertEqual(mod.toolchain_alignment(opts, selected, inventory)["status"], "PASS")
            inventory["smokes"]["z3"]["binary_sha256"] = "0" * 64
            self.assertEqual(mod.toolchain_alignment(opts, selected, inventory)["status"], "FAIL")
            inventory["smokes"]["z3"]["binary_sha256"] = digest
            inventory["smokes"]["z3"]["version"] = "99.0"
            self.assertEqual(mod.toolchain_alignment(opts, selected, inventory)["status"], "FAIL")
            inventory["smokes"]["z3"]["version"] = "5.3.3"
            executable.write_text("#!/bin/sh\necho tampered\n")
            self.assertEqual(mod.toolchain_alignment(opts, selected, inventory)["status"], "FAIL")

    def test_missing_and_zero_selected_cases(self):
        self.assertEqual(mod.toolchain_alignment(None, [], {})["status"], "NOT_RUN")
        opts = types.SimpleNamespace(z3="/definitely/nonexistent/z3")
        self.assertEqual(mod.toolchain_alignment(opts, [{"tool": "z3"}], {})["status"], "NOT_RUN")

    def test_tlc_jar_is_pinned_independently_of_java(self):
        with tempfile.TemporaryDirectory() as tmp:
            jar = Path(tmp) / "tla2tools.jar"
            jar.write_bytes(b"simulated TLC")
            java = Path(tmp) / "fake-java"
            java.write_text("#!/bin/sh\necho 'openjdk version 21.0.12.1'\n")
            java.chmod(0o755)
            digest = hashlib.sha256(jar.read_bytes()).hexdigest()
            opts = types.SimpleNamespace(tlc_jar=str(jar), java=str(java))
            inventory = {"smokes": {"tlc": {"jar_sha256": digest}}}
            res = mod.toolchain_alignment(opts, [{"tool": "tlc"}], inventory)
            self.assertEqual(res["status"], "PASS")
            self.assertFalse(res["checks"][0]["java_binary_hash_pinned"])
            jar.write_bytes(b"tampered TLC")
            self.assertEqual(mod.toolchain_alignment(opts, [{"tool": "tlc"}], inventory)["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
