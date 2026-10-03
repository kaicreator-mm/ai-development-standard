from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "standards" / "ARCHITECTURE_DESIGN_STANDARD.md"
REFERENCE = ROOT / "references" / "ARCHITECTURE_DECISION_REFERENCE.md"


class ArchitectureDesignTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.standard = STANDARD.read_text(encoding="utf-8")
        cls.reference = REFERENCE.read_text(encoding="utf-8")
        cls.lower = cls.standard.lower()

    def test_material_design_facts_are_bounded(self) -> None:
        for phrase in (
            "Decision / scope",
            "Drivers",
            "Invariants",
            "Boundaries / ownership",
            "Alternatives considered",
            "Rationale",
            "Trade-offs",
            "Failure modes",
            "Evidence / assumptions / UNKNOWNs",
            "Escape hatch / evolution path",
        ):
            self.assertIn(phrase, self.standard)

    def test_high_impact_unknown_does_not_become_implementation_freedom(self) -> None:
        self.assertIn("A high-impact `UNKNOWN` MUST NOT silently become implementation freedom", self.standard)
        self.assertIn("may not select its preferred architecture pattern", self.standard)
        self.assertIn("Never leave a high-impact UNKNOWN as an implicit choice", self.reference)

    def test_l2_remains_research_and_freeze_owner(self) -> None:
        self.assertIn("L2 remains the architecture research/evidence workflow and Freeze mechanism", self.standard)
        self.assertIn("does not replace L2 prompts", self.standard)

    def test_v42_keeps_compatibility_and_migration_ownership(self) -> None:
        self.assertIn("v4.2 remains semantic owner of compatibility outcomes and persistent-state transition/recovery", self.standard)
        self.assertIn("architecture decision -> compatibility PASS", self.standard)
        self.assertIn("reference v4.2 evidence rather than redefining it", self.standard)

    def test_no_universal_architecture_paradigm(self) -> None:
        for term in ("microservices", "monoliths", "event sourcing", "CQRS", "Kubernetes", "serverless"):
            self.assertIn(term, self.standard)
        self.assertIn("`popular pattern -> correct architecture` is forbidden", self.standard)

    def test_fast_path_is_proportional(self) -> None:
        self.assertIn("Fast Path changes with no material architecture decision need not produce empty design artifacts", self.standard)
        self.assertIn("Fast Path MUST NOT be used to avoid architecture evidence", self.standard)

    def test_format_is_not_mandatory_adr(self) -> None:
        self.assertIn("does **not** mandate one ADR filename/template/tool", self.standard)
        self.assertIn("Use only material fields; do not create empty boilerplate", self.reference)


if __name__ == "__main__":
    unittest.main()
