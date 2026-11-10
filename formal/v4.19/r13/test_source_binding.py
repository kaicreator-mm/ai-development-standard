"""R17: candidate PR protocol/schema exact Git blobs fail closed before solver startup.

This is a source-byte provenance check, not semantic equivalence or real CAS.
"""
from __future__ import annotations
import pathlib
import tempfile
import unittest
from unittest import mock
import run_proofs as proof


class CandidateSourceBindingTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="ads1366-r17-")
        self.addCleanup(self.tmp.cleanup)
        sandbox = pathlib.Path(self.tmp.name)
        fixtures = {}
        for name, (path, expected) in proof.SOURCE_BINDINGS.items():
            copied = sandbox / name
            copied.write_bytes(path.read_bytes())
            fixtures[name] = (copied, expected)
        patcher = mock.patch.object(proof, "SOURCE_BINDINGS", fixtures)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_real_candidate_fixtures_have_original_git_blobs(self):
        checks = proof.assert_source_hashes("preflight")
        self.assertEqual(len(checks), 2)
        self.assertTrue(all(x["status"] == "PASS" and
                            x["observed_git_blob"] == x["expected_git_blob"] for x in checks))

    def test_comment_only_protocol_change_blocks_solver(self):
        p = proof.SOURCE_BINDINGS["candidate_protocol"][0]
        p.write_bytes(p.read_bytes() + b"\n<!-- independent comment -->\n")
        with mock.patch.object(proof, "run_solver", side_effect=AssertionError("native must not start")) as run:
            with self.assertRaisesRegex(proof.InputBindingError, "preflight: candidate source candidate_protocol blob"):
                proof.verify()
            run.assert_not_called()

    def test_schema_one_byte_drift_blocks_solver(self):
        p = proof.SOURCE_BINDINGS["candidate_dispatch_schema"][0]
        p.write_bytes(p.read_bytes() + b" ")
        with mock.patch.object(proof, "run_solver", side_effect=AssertionError("native must not start")) as run:
            with self.assertRaisesRegex(proof.InputBindingError, "preflight: candidate source candidate_dispatch_schema blob"):
                proof.verify()
            run.assert_not_called()

    def test_missing_protocol_blocks_solver(self):
        proof.SOURCE_BINDINGS["candidate_protocol"][0].unlink()
        with mock.patch.object(proof, "run_solver", side_effect=AssertionError("native must not start")) as run:
            with self.assertRaisesRegex(proof.InputBindingError, "preflight: missing/unreadable candidate source"):
                proof.verify()
            run.assert_not_called()

    def test_postflight_protocol_drift_is_rejected(self):
        counter = {"calls": 0}
        def fake_solver(tool, path):
            counter["calls"] += 1
            if counter["calls"] == len(proof.COMMANDS) * len(proof.EXPECTED):
                p = proof.SOURCE_BINDINGS["candidate_protocol"][0]
                p.write_bytes(p.read_bytes() + b" ")
            return {"tool": tool, "matched": True, "statuses": proof.EXPECTED[path.name]}
        with mock.patch.object(proof, "assert_tool_hashes", return_value=[{"status":"PASS"}]), \
             mock.patch.object(proof, "run_solver", side_effect=fake_solver):
            with self.assertRaisesRegex(proof.InputBindingError, "postflight: candidate source candidate_protocol blob"):
                proof.verify()
        self.assertEqual(counter["calls"], len(proof.COMMANDS) * len(proof.EXPECTED))

    def test_runner_cannot_claim_live_pr_adoption_from_fixture(self):
        self.assertEqual(proof.FROZEN_CANDIDATE_PR, 1365)
        self.assertEqual(proof.FROZEN_CANDIDATE_HEAD,
                         "dac263fa4c0ab155406d2f2117459b34322cc988")
        self.assertNotIn("CLAIM_ADMISSION", proof.verify.__doc__ or "")
        # This source fixture is never an authority to publish GitHub READY or Claim.


if __name__ == "__main__":
    unittest.main()
