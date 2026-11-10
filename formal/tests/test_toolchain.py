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

    def test_mismatched_hash_never_runs_executable_even_for_version(self):
        with tempfile.TemporaryDirectory() as tmp:
            for name in ("z3", "cvc5"):
                with self.subTest(tool=name):
                    sentinel = Path(tmp) / (name + ".executed")
                    executable = Path(tmp) / ("fake-" + name)
                    executable.write_text(
                        "#!/bin/sh\nprintf 'EXECUTED' > '" + str(sentinel) +
                        "'\necho 'Z3 version 5.3.3 cvc5 1.4.2'\n"
                    )
                    executable.chmod(0o755)
                    opts = types.SimpleNamespace(z3=str(executable), cvc5=str(executable))
                    inventory = {"smokes": {name: {"binary_sha256": "0" * 64,
                                                   "version": "5.3.3"}}}
                    report = mod.toolchain_alignment(opts, [{"tool": name}], inventory)
                    self.assertEqual(report["status"], "FAIL")
                    self.assertFalse(report["checks"][0]["version_probe_executed"])
                    self.assertFalse(sentinel.exists(),
                                     "untrusted --version execution is prohibited")

    def test_bad_tlc_jar_never_starts_java_probe(self):
        with tempfile.TemporaryDirectory() as tmp:
            sentinel = Path(tmp) / "java.executed"
            java = Path(tmp) / "fake-java"
            java.write_text("#!/bin/sh\nprintf 'EXECUTED' > '" + str(sentinel) +
                            "'\necho openjdk\n")
            java.chmod(0o755)
            jar = Path(tmp) / "tla2tools.jar"
            jar.write_bytes(b"tampered TLC")
            opts = types.SimpleNamespace(java=str(java), tlc_jar=str(jar))
            inventory = {"smokes": {"tlc": {"jar_sha256": "0" * 64}}}
            report = mod.toolchain_alignment(opts, [{"tool": "tlc"}], inventory)
            self.assertEqual(report["status"], "FAIL")
            self.assertFalse(report["checks"][0]["java_version_probe_executed"])
            self.assertFalse(sentinel.exists())

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
