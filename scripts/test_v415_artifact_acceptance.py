#!/usr/bin/env python3
"""Bounded source-contract application model, NOT a controller/native fence proof.

Independent oracle: frozen #1244 Product blob 488fee5..., A01-A17. Facts below
are isolated fixtures, never evidence that S01/S04 actually meet those facts.
No network, native Task mutation, old-key admission or source repair occurs.
"""
from copy import deepcopy
from dataclasses import dataclass, replace
import hashlib
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
PRODUCT = "docs/intake/i1225-unavailable-ledger/PROPOSAL.md"
PRODUCT_BLOB = "488fee5f6237a7d5d791bf67b04bb155f282b522"


@dataclass(frozen=True)
class Facts:
    adopted: bool = True
    amendment: str = "task/amendment/1"
    source: str = "immutable-source"
    tree: str = "source-tree"
    blobs: tuple = (("schema.json", "exact-blob"),)
    target: str = "target-before"
    published_before: bool = True
    provenance: bool = True
    disjoint: bool = True
    consumers_verified: bool = True
    old_consumer: bool = False
    old_request: bool = False
    effect_obligations_resolved: bool = True
    exclusive_overlap: bool = False
    deployment_unknown: bool = False
    source_checks: bool = True
    negative_checks: bool = True
    review_current: bool = True
    checkout_current: bool = True
    permission: bool = True
    dependencies: bool = True
    findings_clear: bool = True
    complete_reads: bool = True
    plan_current: bool = True
    owner_refs: tuple = ("adopted-owner", "old-key-HOLD", "effect-owner")
    conflict: bool = False
    repair_write: bool = False
    replacement: bool = False

    def eligible(self):
        required = (self.adopted, self.amendment, self.source, self.tree,
                    self.blobs, self.target, self.published_before, self.provenance,
                    self.disjoint, self.consumers_verified,
                    self.effect_obligations_resolved, self.source_checks,
                    self.negative_checks, self.review_current, self.checkout_current,
                    self.permission, self.dependencies, self.findings_clear,
                    self.complete_reads, self.plan_current, self.owner_refs)
        return all(required) and all(value is False for value in (self.old_consumer, self.old_request,
            self.exclusive_overlap, self.deployment_unknown, self.conflict,
            self.repair_write, self.replacement))


class Acceptance:
    """Model the current disjoint operation; never writes the held old store."""
    def __init__(self):
        self.old = {"key": "original-builder-key", "generation": None,
                    "status": "UNKNOWN/HOLD", "accepted_bindings": "UNKNOWN",
                    "resources": "UNKNOWN", "terminal": None}
        self.task = "existing-task"
        self.selection = None
        self.request = None
        self.actual = None
        self.ratified = None
        self.delivery = None
        self.done = 0
        self.wakes = 0
        self.incidents = []
        self.hold = False

    def snapshot(self):
        return deepcopy(vars(self))

    def select(self, facts, receipt):
        if self.hold or self.selection or not facts.eligible() or not receipt:
            return "BLOCKED"
        self.selection = {"operation": receipt, "task": self.task, "facts": facts,
                          "readback": False}
        return "SELECTED"

    def readback(self, operation, facts):
        if (self.hold or not self.selection or operation != self.selection["operation"]
                or facts != self.selection["facts"] or not facts.eligible()):
            return "BLOCKED"
        self.selection["readback"] = True
        return "READ_BACK"

    def request_integration(self, operation, facts):
        # All pre-effect guards execute before creating the model native request.
        if (self.hold or not self.selection or not self.selection["readback"]
                or operation != self.selection["operation"]
                or facts != self.selection["facts"] or not facts.eligible()):
            return "BLOCKED"
        if self.request:
            return "EXISTING_REQUEST"
        self.request = {"id": "native-request/1", "operation": operation,
                        "source": facts.source, "target": facts.target}
        return "REQUESTED"

    def observe(self, actual, facts):
        if not self.request or self.actual is not None:
            return "BLOCKED"
        # Actual request/outcome evidence is preserved even when qualification fails.
        self.actual = deepcopy(actual)
        expected = self.selection["facts"]
        valid = (not self.hold and facts == expected and facts.eligible()
                 and actual.get("ack") == "known"
                 and actual.get("operation") == self.selection["operation"]
                 and actual.get("source") == expected.source
                 and actual.get("target_before") == expected.target
                 and bool(actual.get("integration")) and bool(actual.get("tree"))
                 and actual.get("method") == "merge"
                 and actual.get("parents") == (expected.target, expected.source)
                 and actual.get("checkout") == actual.get("integration")
                 and actual.get("checkout_tree") == actual.get("tree")
                 and actual.get("tree") == actual.get("expected_tree")
                 and actual.get("compensation") is True
                 and actual.get("post_checks") is True)
        if not valid:
            self.hold = True
            self.incidents.append("UNRATIFIED actual integration outcome")
            return "UNRATIFIED"
        self.ratified = deepcopy(actual)
        return "RATIFIED_INTEGRATION"

    def final(self, operation, integration, tree, facts, receipt):
        if (self.hold or not self.ratified or not self.selection
                or operation != self.selection["operation"]
                or facts != self.selection["facts"] or not facts.eligible()
                or integration != self.ratified["integration"]
                or tree != self.ratified["tree"] or not receipt):
            return "BLOCKED"
        if self.delivery:
            return self.delivery["receipt"]
        self.delivery = {"task": self.task, "operation": operation,
                         "integration": integration, "tree": tree,
                         "receipt": receipt, "readback": False}
        return receipt

    def consume_delivery(self, receipt):
        if self.hold or not self.delivery or receipt != self.delivery["receipt"]:
            return "BLOCKED"
        if self.delivery["readback"]:
            return "EXISTING_DELIVERY"
        self.delivery["readback"] = True
        self.done += 1
        self.wakes += 1
        return "DELIVERED"

    def old_result(self, source, grant):
        # Byte equality conveys no authority; retain external old history separately.
        return "STALE_AUTHORITY"

    def conflicting_operation(self, operation):
        if self.selection and operation != self.selection["operation"]:
            self.incidents.append("conflicting operation requires owner resolution")
            self.hold = True
            return "HOLD"
        return "NO_CONFLICT"

    def late_accepted_overlap(self):
        self.incidents.append("genuine old accepted binding reveals material overlap")
        self.hold = True
        return "HOLD"


def outcome(**changes):
    value = dict(ack="known", operation="selection/1", source="immutable-source",
                 target_before="target-before", integration="actual-merge",
                 tree="actual-tree", expected_tree="actual-tree", method="merge",
                 parents=("target-before", "immutable-source"), checkout="actual-merge",
                 checkout_tree="actual-tree", compensation=True, post_checks=True)
    value.update(changes)
    return value


def invariant(model, old):
    assert model.old == old, "held old store mutated"
    assert model.done in (0, 1) and model.wakes == model.done, "duplicate effects"
    if model.done:
        assert model.delivery and model.delivery["readback"] and model.ratified
    if model.delivery:
        assert model.selection and model.ratified
        assert model.delivery["operation"] == model.selection["operation"]
        assert model.delivery["integration"] == model.ratified["integration"]
        assert model.delivery["tree"] == model.ratified["tree"]


class ArtifactAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.m = Acceptance()
        self.old = deepcopy(self.m.old)
        self.f = Facts()

    def tearDown(self):
        invariant(self.m, self.old)

    def rejected(self, call, expected="BLOCKED"):
        before = self.m.snapshot()
        self.assertEqual(call(), expected)
        self.assertEqual(self.m.snapshot(), before)

    def selected(self):
        self.assertEqual(self.m.select(self.f, "selection/1"), "SELECTED")
        self.assertEqual(self.m.readback("selection/1", self.f), "READ_BACK")

    def integrated(self):
        self.selected()
        self.assertEqual(self.m.request_integration("selection/1", self.f), "REQUESTED")
        self.assertEqual(self.m.observe(outcome(), self.f), "RATIFIED_INTEGRATION")
        self.assertEqual((self.m.done, self.m.wakes), (0, 0))

    def delivered(self):
        self.integrated()
        self.assertEqual(self.m.final("selection/1", "actual-merge", "actual-tree",
                                     self.f, "delivery/1"), "delivery/1")
        self.assertEqual(self.m.done, 0)  # publication must be read back first
        self.assertEqual(self.m.consume_delivery("delivery/1"), "DELIVERED")

    def test_frozen_independent_product_oracle(self):
        content = (ROOT / PRODUCT).read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()
        self.assertEqual(blob, PRODUCT_BLOB)
        for case in range(1, 18):
            self.assertIn(f"| A{case:02d} |", content.decode())

    def test_normative_owner_and_receiving_links(self):
        # Source wiring only. Lifecycle behavior is independently exercised below.
        exe = (ROOT / "standards/EXECUTION_ARCHITECTURE_STANDARD.md").read_text(encoding="utf8")
        section = exe.split("### 23.5 ", 1)[1].split("## 24.", 1)[0]
        for text in ("RELEASE_STANDARD11.7A", "29.1 CURRENT", "UNKNOWN material overlap",
                     "final Task-delivery", "no Builder write"):
            self.assertIn(text.lower(), section.lower())
        release = (ROOT / "standards/RELEASE_STANDARD.md").read_text(encoding="utf8")
        route = release.split("#### Distinct immutable-artifact acceptance", 1)[1].split("#### Source closure", 1)[0]
        for heading in ("Preconditions for pre-effect selection", "Selection, integration and post-effect verification",
                        "Final Task-delivery decision and dependency consumption", "Conflicts, late facts and stop conditions"):
            self.assertIn(heading, route)
        for text in ("All six", "actual ratified integration SHA/tree", "canonical accepted delivery receipt",
                     "UNRATIFIED/HOLD", "no old-key generation/resource/terminal mutation"):
            self.assertIn(text, route)
        for path in ("standards/LOCAL_AGENT_HANDOFF_PROTOCOL.md", "references/MANUAL_REFERENCE_FLOW_V49.md"):
            consumer = (ROOT / path).read_text(encoding="utf8")
            self.assertIn("EXE_ARCH23.5", consumer)
            self.assertIn("RELEASE11.7A", consumer)

    def test_unknown_material_predicates_fail_closed_without_effects(self):
        for field in Facts.__dataclass_fields__:
            if isinstance(getattr(self.f, field), bool):
                with self.subTest(field=field):
                    self.rejected(lambda: self.m.select(replace(self.f, **{field: None}), "s"))

    def test_guard_bypass_mutants_change_rejected_full_state(self):
        for field in ("disjoint", "consumers_verified", "review_current", "plan_current"):
            m = Acceptance()
            before = m.snapshot()
            with patch.object(Facts, "eligible", return_value=True):
                m.select(replace(self.f, **{field: False}), "selection/1")
            with self.subTest(field=field), self.assertRaises(AssertionError):
                self.assertEqual(m.snapshot(), before)

    def test_A01_ordered_positive_requires_final_readback(self):
        self.rejected(lambda: self.m.consume_delivery("selection/1"))
        self.delivered()
        self.assertEqual((self.m.done, self.m.wakes), (1, 1))

    def test_A02_asserted_boundary_and_missing_readback(self):
        self.rejected(lambda: self.m.select(replace(self.f, consumers_verified=False), "s"))
        self.m.select(self.f, "selection/1")
        self.rejected(lambda: self.m.request_integration("selection/1", self.f))

    def test_A03_old_authorized_consumer_or_pending_request(self):
        for field in ("old_consumer", "old_request"):
            with self.subTest(field=field):
                self.rejected(lambda: self.m.select(replace(self.f, **{field: True}), "s"))

    def test_A04_different_old_head_and_current_expected_head_guard(self):
        self.selected()
        self.rejected(lambda: self.m.old_result("different-source", "old-grant"), "STALE_AUTHORITY")
        self.rejected(lambda: self.m.request_integration("selection/1", replace(self.f, source="different-source")))

    def test_A05_bug_conflict_and_no_repair_write(self):
        for change in ({"source_checks": False}, {"negative_checks": False},
                       {"conflict": True}, {"repair_write": True}):
            self.rejected(lambda: self.m.select(replace(self.f, **change), "s"))

    def test_A06_no_replacement_epoch_counter_or_key_escape(self):
        for proposed in ("new-epoch", "renamed-task", "generation-1000000"):
            self.rejected(lambda: self.m.select(replace(self.f, replacement=True), proposed))

    def test_A07_exclusive_overlap_or_unknown_disjointness(self):
        for change in ({"exclusive_overlap": True}, {"disjoint": False}):
            self.rejected(lambda: self.m.select(replace(self.f, **change), "s"))

    def test_A08_external_effect_unknown_retains_obligation(self):
        for change in ({"deployment_unknown": True}, {"effect_obligations_resolved": False}):
            self.rejected(lambda: self.m.select(replace(self.f, **change), "s"))

    def test_A09_historical_checks_or_review_not_current(self):
        for field in ("source_checks", "review_current"):
            self.rejected(lambda: self.m.select(replace(self.f, **{field: False}), "s"))

    def test_A10_full_current_inputs_at_each_decision(self):
        self.selected()
        for field in ("findings_clear", "permission", "complete_reads", "plan_current", "dependencies"):
            changed = replace(self.f, **{field: False})
            self.rejected(lambda: self.m.request_integration("selection/1", changed))
        self.m.request_integration("selection/1", self.f)
        self.m.observe(outcome(), self.f)
        self.rejected(lambda: self.m.final("selection/1", "actual-merge", "actual-tree",
                                           replace(self.f, permission=False), "d"))

    def test_A11_checkout_identity_not_just_run_head(self):
        self.rejected(lambda: self.m.select(replace(self.f, checkout_current=False), "s"))
        self.selected()
        self.m.request_integration("selection/1", self.f)
        self.assertEqual(self.m.observe(outcome(checkout="old-synthetic-merge"), self.f), "UNRATIFIED")
        self.assertIsNotNone(self.m.actual)
        self.assertIsNone(self.m.ratified)

    def test_A12_unknown_ack_and_mismatched_post_tree_preserve_effects(self):
        for change in ({"ack": "unknown"}, {"checkout_tree": "wrong-tree"},
                       {"parents": ("wrong-target", "immutable-source")},
                       {"compensation": False}):
            m = Acceptance()
            m.select(self.f, "selection/1"); m.readback("selection/1", self.f)
            m.request_integration("selection/1", self.f)
            actual = outcome(**change)
            self.assertEqual(m.observe(actual, self.f), "UNRATIFIED")
            self.assertEqual(m.actual, actual)
            self.assertIsNotNone(m.request)
            self.assertTrue(m.incidents)
            self.assertEqual((m.done, m.wakes), (0, 0))
            before = m.snapshot()
            self.assertEqual(m.request_integration("selection/1", self.f), "BLOCKED")
            self.assertEqual(m.snapshot(), before)
            invariant(m, self.old)

    def test_A13_late_material_acceptance_holds_without_erasing_history(self):
        self.delivered()
        history = (deepcopy(self.m.selection), deepcopy(self.m.ratified), deepcopy(self.m.delivery))
        self.assertEqual(self.m.late_accepted_overlap(), "HOLD")
        self.assertEqual(history, (self.m.selection, self.m.ratified, self.m.delivery))
        self.assertEqual((self.m.done, self.m.wakes), (1, 1))
        self.rejected(lambda: self.m.consume_delivery("delivery/1"))

    def test_A14_delivery_is_not_old_terminal_or_runtime_qualification(self):
        self.delivered()
        self.assertEqual(self.m.old, self.old)
        self.assertNotIn("runtime_pass", vars(self.m))
        self.assertNotIn("rq", vars(self.m))

    def test_A15_proposal_or_missing_prior_amendment_not_authority(self):
        for change in ({"adopted": False}, {"amendment": ""}, {"owner_refs": ()},
                       {"published_before": False}, {"blobs": ()}, {"provenance": False}):
            self.rejected(lambda: self.m.select(replace(self.f, **change), "s"))

    def test_A16_same_bytes_old_grant_and_duplicates_never_substitute(self):
        self.selected()
        self.rejected(lambda: self.m.old_result(self.f.source, "old-grant"), "STALE_AUTHORITY")
        self.rejected(lambda: self.m.request_integration("old-grant", self.f))
        self.m.request_integration("selection/1", self.f)
        self.rejected(lambda: self.m.request_integration("selection/1", self.f), "EXISTING_REQUEST")
        self.m.observe(outcome(), self.f)
        self.rejected(lambda: self.m.old_result(self.f.source, "old-validation"), "STALE_AUTHORITY")
        self.rejected(lambda: self.m.final("old-grant", "actual-merge", "actual-tree", self.f, "old-receipt"))
        self.m.final("selection/1", "actual-merge", "actual-tree", self.f, "delivery/1")
        self.m.consume_delivery("delivery/1")
        self.rejected(lambda: self.m.final("selection/1", "actual-merge", "actual-tree", self.f, "duplicate"), "delivery/1")
        self.rejected(lambda: self.m.consume_delivery("delivery/1"), "EXISTING_DELIVERY")
        self.assertEqual(self.m.delivery["receipt"], "delivery/1")

    def test_A17_selection_or_integration_only_never_completes_task(self):
        self.selected()
        self.rejected(lambda: self.m.final("selection/1", "actual-merge", "actual-tree", self.f, "d"))
        self.m.request_integration("selection/1", self.f)
        self.assertEqual(self.m.observe(outcome(post_checks=False), self.f), "UNRATIFIED")
        self.rejected(lambda: self.m.final("selection/1", "actual-merge", "actual-tree", self.f, "d"))
        self.rejected(lambda: self.m.consume_delivery("selection/1"))

    def test_conflicting_current_operation_requires_owner_resolution(self):
        self.selected()
        self.assertEqual(self.m.conflicting_operation("selection/2"), "HOLD")
        self.rejected(lambda: self.m.request_integration("selection/1", self.f))

    def test_mutants_premature_delivery_old_store_and_attribution_detected(self):
        for mutation in ("premature", "old-generation", "duplicate", "old-grant"):
            mutant = Acceptance()
            mutant.select(self.f, "selection/1")
            if mutation == "premature":
                mutant.done = mutant.wakes = 1
            elif mutation == "old-generation":
                mutant.old["generation"] = 1000000
            elif mutation == "duplicate":
                mutant.done = mutant.wakes = 2
            else:
                mutant.ratified = outcome()
                mutant.delivery = {"operation": "old-grant", "integration": "actual-merge", "tree": "actual-tree"}
            with self.subTest(mutation=mutation), self.assertRaises(AssertionError):
                invariant(mutant, self.old)


if __name__ == "__main__":
    unittest.main(verbosity=2)
