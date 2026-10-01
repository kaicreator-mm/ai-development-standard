"""T08 central wiring regression. Run: python -m unittest scripts.test_v45_adoption_wiring -v.

Checks repository assets and semantic negative examples, not real runtime/integration PASS.
"""
from __future__ import annotations

import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
OWNERS = (
    "OBSERVABILITY_RUNTIME_EVIDENCE_STANDARD",
    "INCIDENT_RECOVERY_FEEDBACK_STANDARD",
    "MAINTENANCE_EOL_HOTFIX_STANDARD",
)
REFERENCES = (
    "OBSERVABILITY_RUNTIME_REFERENCE",
    "INCIDENT_RECOVERY_REFERENCE",
    "MAINTENANCE_EOL_HOTFIX_REFERENCE",
)
CONTRACTS = (
    "runtime-observation-context-v1.schema.json",
    "incident-event-v1.schema.json",
    "maintenance-policy-v1.schema.json",
)


def text(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def markdown_slug(heading: str) -> str:
    heading = re.sub(r"<[^>]+>", "", heading).replace("`", "").strip().lower()
    heading = re.sub(r"[^\w\- ]", "", heading, flags=re.UNICODE)
    return re.sub(r"\s+", "-", heading).strip("-")


def markdown_anchors(body: str) -> set[str]:
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    for line in body.splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        base = markdown_slug(match.group(1))
        if not base:
            continue
        count = counts.get(base, 0)
        anchors.add(base if count == 0 else f"{base}-{count}")
        counts[base] = count + 1
    return anchors


def ref_resolves(ref: str) -> bool:
    path, _, fragment = ref.partition("#")
    source = ROOT / path
    if not source.is_file():
        return False
    return not fragment or fragment in markdown_anchors(source.read_text(encoding="utf-8"))


class TestV45AdoptionWiring(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads(text("standard-manifest.json"))["sections"]
        cls.coverage = json.loads(text("templates/golden/STANDARD_COVERAGE.json"))["coverage"]

    def test_three_current_owners_and_references(self) -> None:
        for owner, reference in zip(OWNERS, REFERENCES):
            owner_path = f"standards/{owner}.md"
            reference_path = f"references/{reference}.md"
            self.assertEqual(self.manifest["normative_standards"].count(owner_path), 1)
            self.assertEqual(self.manifest["references"].count(reference_path), 1)
            self.assertTrue((ROOT / owner_path).is_file())
            self.assertTrue((ROOT / reference_path).is_file())
        self.assertEqual(len(self.manifest["normative_standards"]), len(set(self.manifest["normative_standards"])))

    def test_t01_machine_contracts_are_discovered_once(self) -> None:
        for contract in CONTRACTS:
            path = f"schemas/{contract}"
            self.assertEqual(self.manifest["machine_contracts"].count(path), 1)
            schema = json.loads(text(path))
            self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
            self.assertEqual(schema["type"], "object")
            self.assertTrue(schema["required"])

    def test_golden_exact_one_per_active_owner_and_real_anchors(self) -> None:
        active = self.manifest["normative_standards"]
        covered = [row["standard"] for row in self.coverage]
        self.assertEqual(set(covered), set(active))
        self.assertEqual(len(covered), len(active), "duplicate owner or missing Golden row")
        for row in self.coverage:
            for field in ("golden_ref", "forbidden_ref", "rationale_ref"):
                self.assertTrue(ref_resolves(row[field]), f"{row['standard']} {field}: {row[field]}")

    def test_applicability_distinguishes_nonruntime_from_required_unknown(self) -> None:
        adoption = text("standards/PROJECT_ADOPTION.md")
        overrides = text("templates/project/.dev-standard/PROJECT_OVERRIDES.md")
        migration = text("docs/implementation/4.5.0/MIGRATION_ADOPTION.md")
        for document in (adoption, overrides):
            for field in ("v4.runtime", "v4.incident", "v4.maintenance"):
                self.assertIn(field, document)
            for state in ("NOT_APPLICABLE", "NOT_RUN", "BLOCKED"):
                self.assertIn(state, document)
        for phrase in ("non-deployed library", "required but unavailable", "historical", "result-SHA"):
            self.assertIn(phrase, migration)

    def test_existing_owners_remain_distinct(self) -> None:
        migration = text("docs/implementation/4.5.0/MIGRATION_ADOPTION.md")
        for owner in ("TESTING_STANDARD.md", "TEST_DATA_AND_SCENARIO_STANDARD.md", "VALIDATION_STANDARD.md", "RELEASE_STANDARD.md"):
            self.assertIn(owner, migration)
        for negative in (
            "Deployment/activation successful → runtime healthy",
            "Backport source PASS → result-SHA PASS",
            "Legacy release/incident/support record",
            "Required but missing capability",
        ):
            self.assertIn(negative, migration)


if __name__ == "__main__":
    unittest.main()
