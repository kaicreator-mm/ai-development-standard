from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import unittest

from verify_event_writer_surfaces import classify_v1_reference, scan_writer_surfaces, writer_surface_paths

ROOT = Path(__file__).resolve().parents[1]

RELEASE_GATES = {
    "full-regression",
    "critical-journey",
    "hidden-validation",
    "packaging",
}


@dataclass(frozen=True)
class ValidationPlan:
    kind: str
    validation_scope: str
    required_gates: frozenset[str]


def validate_validation_plan(plan: ValidationPlan) -> list[str]:
    errors: list[str] = []
    expected_scope = {
        "ordinary-leaf": "concern",
        "platform-specific-leaf": "concern",
        "integration-owner": "integration",
        "closure-owner": "closure",
    }.get(plan.kind)
    if expected_scope is None:
        return [f"unknown work-item kind: {plan.kind}"]
    if plan.validation_scope != expected_scope:
        errors.append(f"{plan.kind} must use validation_scope={expected_scope}")

    gates = set(plan.required_gates)
    if plan.kind == "ordinary-leaf":
        if "scoped-tests" not in gates:
            errors.append("ordinary leaf requires scoped-tests")
        forbidden = gates & ({"real-platform", "cross-component"} | RELEASE_GATES)
        if forbidden:
            errors.append(f"ordinary leaf inherited unrelated gates: {sorted(forbidden)}")
    elif plan.kind == "platform-specific-leaf":
        for required in ("scoped-tests", "real-platform"):
            if required not in gates:
                errors.append(f"platform-specific leaf requires {required}")
        forbidden = gates & ({"cross-component"} | RELEASE_GATES)
        if forbidden:
            errors.append(f"platform-specific leaf inherited release/integration gates: {sorted(forbidden)}")
    elif plan.kind == "integration-owner":
        if "cross-component" not in gates:
            errors.append("integration owner requires cross-component gate")
        forbidden = gates & RELEASE_GATES
        if forbidden:
            errors.append(f"integration owner inherited closure-only gates: {sorted(forbidden)}")
    elif plan.kind == "closure-owner":
        missing = RELEASE_GATES - gates
        if missing:
            errors.append(f"closure owner missing release gates: {sorted(missing)}")
    return errors


def validate_hidden_successor_lifecycle(record: dict) -> list[str]:
    errors: list[str] = []
    required = (
        "prior_candidate_sha",
        "prior_pack_identity",
        "prior_hidden_status",
        "escape_class",
        "release_significant",
        "product_fix_sha",
        "product_fix_in_successor",
        "successor_candidate_sha",
        "successor_pack_identity",
        "pack_strengthening_independent",
        "successor_hidden_status",
        "successor_release_state",
    )
    for field in required:
        if field not in record:
            errors.append(f"missing {field}")
    if errors:
        return errors

    if record["prior_hidden_status"] != "PASS":
        errors.append("regression scenario must start from an actual prior Hidden PASS")
    if record["escape_class"] not in {"HIDDEN_PACK_BLIND_SPOT", "BOTH_VISIBLE_AND_HIDDEN_GAP"}:
        errors.append("release-significant escaped defect must be classified as a Hidden blind spot for this lifecycle")
    if record["release_significant"] is not True:
        errors.append("scenario must be release-significant")
    if record["product_fix_sha"] == record["prior_candidate_sha"]:
        errors.append("escaped product defect must be fixed on a new identity")
    if record["product_fix_in_successor"] is not True:
        errors.append("successor candidate must actually contain the product fix")
    if record["successor_candidate_sha"] == record["prior_candidate_sha"]:
        errors.append("product fix must create a successor candidate identity")
    if record["successor_pack_identity"] == record["prior_pack_identity"]:
        errors.append("Hidden blind-spot strengthening must create a new immutable pack identity")
    if record["pack_strengthening_independent"] is not True:
        errors.append("strengthened pack must remain independent from the visible regression implementation")
    if record["successor_hidden_status"] != "PASS":
        errors.append("successor release cannot qualify before successor Hidden PASS")
    if record["successor_release_state"] == "READY" and record["successor_hidden_status"] != "PASS":
        errors.append("READY cannot be derived without successor Hidden PASS")
    return errors


class V33SemanticRegression(unittest.TestCase):
    def test_issue25_validation_ownership_positive_matrix(self) -> None:
        cases = [
            ValidationPlan("ordinary-leaf", "concern", frozenset({"scoped-tests"})),
            ValidationPlan("platform-specific-leaf", "concern", frozenset({"scoped-tests", "real-platform"})),
            ValidationPlan("integration-owner", "integration", frozenset({"cross-component"})),
            ValidationPlan("closure-owner", "closure", frozenset(RELEASE_GATES)),
        ]
        for plan in cases:
            with self.subTest(plan=plan):
                self.assertEqual(validate_validation_plan(plan), [])

    def test_issue25_validation_ownership_rejects_wrong_layer_gates(self) -> None:
        invalid = [
            ValidationPlan("ordinary-leaf", "concern", frozenset({"scoped-tests", "hidden-validation"})),
            ValidationPlan("platform-specific-leaf", "concern", frozenset({"scoped-tests"})),
            ValidationPlan("integration-owner", "integration", frozenset({"cross-component", "packaging"})),
            ValidationPlan("closure-owner", "closure", frozenset(RELEASE_GATES - {"hidden-validation"})),
            ValidationPlan("integration-owner", "concern", frozenset({"cross-component"})),
        ]
        for plan in invalid:
            with self.subTest(plan=plan):
                self.assertTrue(validate_validation_plan(plan), plan)

    def hidden_successor_record(self) -> dict:
        return {
            "prior_candidate_sha": "1" * 40,
            "prior_pack_identity": "hidden-pack-r7:sha256:old",
            "prior_hidden_status": "PASS",
            "escape_class": "HIDDEN_PACK_BLIND_SPOT",
            "release_significant": True,
            "product_fix_sha": "2" * 40,
            "product_fix_in_successor": True,
            "successor_candidate_sha": "3" * 40,
            "successor_pack_identity": "hidden-pack-r8:sha256:new",
            "pack_strengthening_independent": True,
            "successor_hidden_status": "PASS",
            "successor_release_state": "READY",
        }

    def test_issue30_hidden_blind_spot_successor_lifecycle(self) -> None:
        self.assertEqual(validate_hidden_successor_lifecycle(self.hidden_successor_record()), [])

    def test_issue30_hidden_blind_spot_rejects_evidence_reuse_shortcuts(self) -> None:
        base = self.hidden_successor_record()
        mutations = [
            dict(base, product_fix_sha=base["prior_candidate_sha"]),
            dict(base, product_fix_in_successor=False),
            dict(base, successor_candidate_sha=base["prior_candidate_sha"]),
            dict(base, successor_pack_identity=base["prior_pack_identity"]),
            dict(base, pack_strengthening_independent=False),
            dict(base, successor_hidden_status="NOT_RUN"),
            dict(base, escape_class="VISIBLE_TEST_GAP"),
        ]
        for record in mutations:
            with self.subTest(record=record):
                self.assertTrue(validate_hidden_successor_lifecycle(record), record)

    def test_issue32_manifest_driven_writer_surface_scan(self) -> None:
        surfaces = writer_surface_paths(ROOT)
        self.assertIn("standards/CHATGPT_WEB_ROLE.md", surfaces)
        self.assertIn("prompts/local-agent-bootstrap.md", surfaces)
        self.assertIn("templates/agent-event-comment.md", surfaces)
        self.assertIn("AGENTS.md", surfaces)
        self.assertGreater(len(surfaces), 20)
        self.assertEqual(scan_writer_surfaces(ROOT), [])

    def test_issue32_v1_classifier_is_mutation_sensitive(self) -> None:
        historical = ["Historical `ai-dev:event:v1` comments remain valid history and are read-only compatibility evidence."]
        self.assertEqual(classify_v1_reference(historical, 0), "historical-compatibility")

        prohibition = ["New writers MUST NOT emit `ai-dev:event:v1`."]
        self.assertEqual(classify_v1_reference(prohibition, 0), "explicit-prohibition")

        stale_mutations = [
            "For new work publish `ai-dev:event:v1` after validation.",
            "For new work, set schema to `ai-dev:event:v1`.",
            "Historical `ai-dev:event:v1` is readable; for new work set schema to `ai-dev:event:v1`.",
            "Legacy compatibility writer: set schema to `ai-dev:event:v1`.",
            "Historical compatibility writer should publish `ai-dev:event:v1`.",
            "Legacy compatibility writer must serialize `ai-dev:event:v1`.",
            "Historical compatibility writer should generate schema `ai-dev:event:v1`.",
            "Legacy compatibility adapter may transmogrify output into `ai-dev:event:v1`.",
            "Historical `ai-dev:event:v1` comments remain valid history and are read-only compatibility evidence. Writer may serialize it.",
        ]
        for line in stale_mutations:
            with self.subTest(line=line):
                self.assertEqual(classify_v1_reference([line], 0), "stale-or-unclassified")

        adjacent_schema_mask_attempt = [
            "Historical `ai-dev:event:v1` comments remain valid history and are read-only compatibility evidence.",
            "Set schema to `ai-dev:event:v1`.",
        ]
        self.assertEqual(classify_v1_reference(adjacent_schema_mask_attempt, 1), "stale-or-unclassified")


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(V33SemanticRegression)
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
