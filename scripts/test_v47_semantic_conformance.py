"""v4.7 T07 unified semantic conformance tests.

These tests compose the already-merged T01-T06 owner surfaces and add only
cross-standard non-transfer/write-authority regressions. They are ordinary
test evidence, not Validation/Review/Release authority.
"""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import v47_conformance as conformance
from v47_conformance import (
    DEPENDENCY_TEST_SCRIPTS,
    EvidenceTuple,
    FROZEN_PRODUCT_NEGATIVE_COUNT,
    FROZEN_PRODUCT_NEGATIVES,
    RUNTIME_OWNER_REF,
    STATE_RULE_EXPECTATIONS,
    T07_TASK_PACK,
    T07_WRITE_SET,
    current_repo_conformance_errors,
    evidence_applies_to,
    frozen_product_conformance_errors,
    historical_manifest_compatible,
    manifest_conformance_errors,
    mutation_authorized_by_task_pack,
    parse_allowed_write_set,
    parse_frozen_product_section6_negatives,
    run_dependency_suites,
    state_registry_conformance_errors,
)

ROOT = Path(__file__).resolve().parents[1]


class UnifiedSemanticConformanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads(
            (ROOT / "standard-manifest.json").read_text(encoding="utf-8")
        )
        cls.registry = json.loads(
            (ROOT / "registries/state-dimensions-v1.json").read_text(encoding="utf-8")
        )
        cls.task_pack = (ROOT / T07_TASK_PACK).read_text(encoding="utf-8")
        cls.prd = (ROOT / "docs/implementation/4.7.0/PRD.md").read_text(encoding="utf-8")

    def test_u01_current_repository_composes_without_semantic_error(self) -> None:
        self.assertEqual(current_repo_conformance_errors(ROOT), [])

    def test_u02_task_pack_is_only_mutation_input(self) -> None:
        self.assertEqual(frozenset(parse_allowed_write_set(self.task_pack)), T07_WRITE_SET)
        self.assertTrue(mutation_authorized_by_task_pack(self.task_pack, T07_WRITE_SET))
        # This is a real canonical owner/discovery target in the manifest, but
        # registry presence must not grant T07 mutation authority over it.
        owner = "standards/DEVELOPMENT_WORKFLOW.md"
        self.assertIn(owner, self.manifest["sections"]["normative_standards"])
        self.assertFalse(mutation_authorized_by_task_pack(self.task_pack, [owner]))
        # Tool/provider/technical-necessity facts are deliberately not parameters
        # of mutation_authorized_by_task_pack and therefore cannot widen scope.

    def test_u03_same_pass_token_remains_dimension_qualified(self) -> None:
        rules = {r["rule_id"]: r for r in self.registry["forbidden_inferences"]}
        review_rule = rules["F02_REVIEW_PASS_NOT_VALIDATION_PASS"]
        self.assertEqual(review_rule["source_fact_ref"], "PASS")
        self.assertEqual(review_rule["prohibited_conclusion_ref"], "PASS")
        self.assertNotEqual(
            review_rule["source_dimension_ref"], review_rule["target_dimension_ref"]
        )
        for rule_id, expected in STATE_RULE_EXPECTATIONS.items():
            rule = rules[rule_id]
            actual = (
                rule["source_dimension_ref"],
                rule["source_fact_ref"],
                rule["target_dimension_ref"],
                rule["prohibited_conclusion_ref"],
            )
            self.assertEqual(actual, expected, rule_id)

    def test_u03_runtime_owner_is_corrected_exact_v45_pointer(self) -> None:
        runtime = next(
            d for d in self.registry["dimensions"] if d["dimension_id"] == "runtime_health"
        )
        self.assertEqual(runtime["canonical_owner_ref"], RUNTIME_OWNER_REF)
        self.assertEqual(state_registry_conformance_errors(self.registry), [])

    def test_u04_exact_sha_and_fidelity_evidence_never_transfer(self) -> None:
        source = EvidenceTuple("a" * 40, "sandbox", "focused")
        self.assertTrue(evidence_applies_to(source, source))
        self.assertFalse(
            evidence_applies_to(
                source, EvidenceTuple("b" * 40, "sandbox", "focused")
            )
        )
        self.assertFalse(
            evidence_applies_to(
                source, EvidenceTuple("a" * 40, "real-host", "focused")
            )
        )
        self.assertFalse(
            evidence_applies_to(
                source, EvidenceTuple("a" * 40, "sandbox", "integration")
            )
        )

    def test_u06_owner_conflict_fails_independent_of_entry_order(self) -> None:
        for reverse in (False, True):
            mutant = deepcopy(self.manifest)
            contender = deepcopy(mutant["semantic_authorities"]["entries"][0])
            contender["entry_id"] = "t07-competing-owner"
            contender["canonical_owner_ref"] = "standards/RELEASE_STANDARD.md"
            mutant["semantic_authorities"]["entries"].append(contender)
            if reverse:
                mutant["semantic_authorities"]["entries"].reverse()
            errors = manifest_conformance_errors(ROOT, mutant)
            self.assertTrue(
                any("competing canonical owner" in error for error in errors), errors
            )

    def test_u06_historical_manifest_keeps_sections_without_semantic_registry(self) -> None:
        self.assertTrue(historical_manifest_compatible(self.manifest))
        historical = deepcopy(self.manifest)
        historical.pop("semantic_authorities")
        self.assertEqual(historical["schema_version"], 1)
        self.assertEqual(historical["sections"], self.manifest["sections"])

    def test_u07_state_rule_mutation_fails_with_precise_rule_identity(self) -> None:
        mutant = deepcopy(self.registry)
        rule = next(
            r
            for r in mutant["forbidden_inferences"]
            if r["rule_id"] == "F07_OLD_SHA_VALIDATION_NOT_SUCCESSOR_PASS"
        )
        rule["prohibited_conclusion_ref"] = "PASS@any-successor"
        errors = state_registry_conformance_errors(mutant)
        self.assertTrue(
            any("F07_OLD_SHA_VALIDATION_NOT_SUCCESSOR_PASS" in error for error in errors),
            errors,
        )

    def test_u08_full_frozen_product_negative_catalog_fails_closed(self) -> None:
        self.assertEqual(FROZEN_PRODUCT_NEGATIVE_COUNT, 21)
        self.assertEqual(len(FROZEN_PRODUCT_NEGATIVES), FROZEN_PRODUCT_NEGATIVE_COUNT)
        self.assertEqual(len(set(FROZEN_PRODUCT_NEGATIVES)), FROZEN_PRODUCT_NEGATIVE_COUNT)
        product_negatives = parse_frozen_product_section6_negatives(self.prd)
        self.assertEqual(len(product_negatives), FROZEN_PRODUCT_NEGATIVE_COUNT)
        self.assertEqual(set(product_negatives), set(FROZEN_PRODUCT_NEGATIVES))
        self.assertEqual(frozen_product_conformance_errors(self.prd), [])

        omitted_p1_families = {
            "waiver/exception -> PASS",
            "fresh DB/install PASS -> upgrade PASS",
            "incident RECOVERED -> permanent fix/follow-up closed",
            "Skill installed/capable -> trusted/authorized",
            "Intent/Assumption record -> Frozen Product authority",
        }
        self.assertTrue(omitted_p1_families.issubset(set(FROZEN_PRODUCT_NEGATIVES)))

        for negative in FROZEN_PRODUCT_NEGATIVES:
            mutant = self.prd.replace(negative, "<removed-product-negative>", 1)
            errors = frozen_product_conformance_errors(mutant)
            self.assertTrue(
                any(negative in error for error in errors),
                f"missing Product negative did not fail closed: {negative}",
            )

        unrelated_prd_string = "JSON Schema meta-validation alone is insufficient."
        self.assertIn(unrelated_prd_string, self.prd)
        self.assertNotIn(unrelated_prd_string, set(product_negatives))
        removed_negative = FROZEN_PRODUCT_NEGATIVES[0]
        same_cardinality_substitution = tuple(
            unrelated_prd_string if negative == removed_negative else negative
            for negative in FROZEN_PRODUCT_NEGATIVES
        )
        self.assertEqual(
            len(same_cardinality_substitution), FROZEN_PRODUCT_NEGATIVE_COUNT
        )
        self.assertEqual(
            len(set(same_cardinality_substitution)), FROZEN_PRODUCT_NEGATIVE_COUNT
        )
        with patch.object(
            conformance,
            "FROZEN_PRODUCT_NEGATIVES",
            same_cardinality_substitution,
        ):
            errors = conformance.frozen_product_conformance_errors(self.prd)
        self.assertTrue(
            any(
                "Product §6 required negative missing from executable catalog" in error
                and removed_negative in error
                for error in errors
            ),
            errors,
        )
        self.assertTrue(
            any(
                "executable negative absent from Product §6 authority" in error
                and unrelated_prd_string in error
                for error in errors
            ),
            errors,
        )

        with patch.object(
            conformance,
            "FROZEN_PRODUCT_NEGATIVES",
            FROZEN_PRODUCT_NEGATIVES[:-1],
        ):
            errors = conformance.frozen_product_conformance_errors(self.prd)
        self.assertTrue(
            any("catalog cardinality drift" in error for error in errors),
            errors,
        )

    def test_u08_t01_through_t06_focused_suites_remain_green(self) -> None:
        results = run_dependency_suites(ROOT)
        self.assertEqual(set(results), set(DEPENDENCY_TEST_SCRIPTS))
        self.assertEqual(
            {name: code for name, code in results.items() if code != 0}, {}
        )


if __name__ == "__main__":
    unittest.main()
