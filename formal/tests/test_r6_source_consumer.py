"""R6 opt-in real candidate source-consumption check, not a claim admission gate."""
import hashlib
import importlib.util
import os
import subprocess
import unittest
from pathlib import Path

CANDIDATE = os.environ.get("ADS_FORMAL_CANDIDATE_CHECKOUT")
PIN = "dac263fa4c0ab155406d2f2117459b34322cc988"
RULES_BLOB = "0829be09f46dde75710bc54607a14edd7a2c4cea"


@unittest.skipUnless(CANDIDATE, "Exact candidate checkout not available; SOURCE_CONSUMER_NOT_RUN")
class CandidateGenerationConsumerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(CANDIDATE).resolve()
        head = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True, timeout=10
        ).strip()
        if head != PIN:
            raise AssertionError(f"Wrong candidate HEAD {head}, expected {PIN}")
        path = (root / "scripts" / "v34_rules.py").resolve()
        if not path.is_file() or not path.is_relative_to(root):
            raise AssertionError("Candidate source missing or escaping checkout")
        raw = path.read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
        if blob != RULES_BLOB:
            raise AssertionError(f"Candidate rules blob mismatch {blob}")
        spec = importlib.util.spec_from_file_location("ads_r6_pinned_candidate_rules", path)
        cls.rules = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.rules)

    def test_generation_transition_bounded_exhaustive(self):
        """Helper classifies generations; it is NOT a full Claim identity/authority check."""
        for reserved in range(6):
            for claimed in range(9):
                with self.subTest(reserved=reserved, claimed=claimed):
                    expected = ("IDEMPOTENT" if claimed == reserved else
                                "CLAIMED" if claimed == reserved + 1 else "STALE")
                    self.assertEqual(
                        self.rules.admission_generation_conforms(
                            reserved_generation=reserved, claimed_generation=claimed
                        ), expected
                    )

    def test_generation_invalid_inputs_fail_closed(self):
        for reserved, claimed in (
            (True, 0), (0, False), (-1, 0), (0, -1),
            (None, 0), ("0", 0), (0, 1.0)
        ):
            with self.subTest(reserved=reserved, claimed=claimed):
                with self.assertRaises(ValueError):
                    self.rules.admission_generation_conforms(
                        reserved_generation=reserved, claimed_generation=claimed
                    )

    def test_group_ref_syntax_not_authority(self):
        self.assertTrue(self.rules.authorize_non_default(None, None))
        self.assertTrue(self.rules.authorize_non_default("lane-A", "#1353@6585163422"))
        for invalid_ref in (None, "", "owner-approved", "#bad", "#1353"):
            with self.subTest(ref=invalid_ref):
                with self.assertRaises(ValueError):
                    self.rules.authorize_non_default("lane-A", invalid_ref)
        # A syntactically valid ref is not proof that current, right-family,
        # right-subject durable owner facts were actually independently read.


if __name__ == "__main__":
    unittest.main()
