from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "standards" / "INCIDENT_RECOVERY_FEEDBACK_STANDARD.md"
REFERENCE = ROOT / "references" / "INCIDENT_RECOVERY_REFERENCE.md"


class IncidentRecoveryFeedbackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.standard = STANDARD.read_text(encoding="utf-8")
        cls.reference = REFERENCE.read_text(encoding="utf-8")

    def test_incident_history_is_append_oriented(self) -> None:
        self.assertIn("append-oriented incident facts", self.standard)
        self.assertIn("MUST preserve prior facts", self.standard)
        self.assertIn("later recovery event does not erase earlier failure evidence", self.standard)

    def test_incident_facts_are_not_collapsed(self) -> None:
        for token in ("DETECTED != MITIGATED", "RECOVERED != VERIFIED", "VERIFIED != FOLLOW_UP_COMPLETE"):
            self.assertIn(token, self.standard)

    def test_recovery_reuses_owning_authorities(self) -> None:
        for token in ("v4.4 Deployment Governance", "v4.2 Data/Migration Governance", "configuration/credential", "external-system mutation"):
            self.assertIn(token, self.standard)
        self.assertIn("incident does not grant that authority", self.reference)

    def test_recovery_requires_verification(self) -> None:
        self.assertIn("MUST NOT be treated as permanent-fix truth", self.standard)
        self.assertIn("service responds again != root cause fixed", self.standard)
        self.assertIn("rollback completed != corrective change verified", self.standard)

    def test_material_incident_routes_engineering_feedback(self) -> None:
        for token in ("reproducible defect/bug evidence", "regression or test scenario", "product/architecture decision", "standard/process gap"):
            self.assertIn(token, self.standard)
        self.assertIn("MUST preserve a durable reference", self.standard)

    def test_closure_does_not_erase_follow_up_or_rewrite_prior_evidence(self) -> None:
        self.assertIn("Incident closure MUST NOT erase required unresolved follow-up", self.standard)
        self.assertIn("MUST NOT rewrite a prior exact Release/Deployment/Validation result", self.standard)


if __name__ == "__main__":
    unittest.main()
