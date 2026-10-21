#!/usr/bin/env python3
"""Bounded source-contract application model, NOT a controller/native fence proof.

Independent oracle: frozen #1244 Product blob 488fee5..., A01-A17. Facts below
are isolated fixtures, never evidence that S01/S04 actually meet those facts.
No network, native Task mutation, old-key admission or source repair occurs.
"""
from copy import deepcopy
from dataclasses import dataclass, field, replace
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


@dataclass(frozen=True)
class NativeObservation:
    """Independent fixture read from native state, not the request's outcome.

    Expected integration tree is separately predicted from the permitted diff;
    source tree and integration tree need not be equal on a merge target.
    These literals are model premises, not real GitHub proof.
    """
    ref: str = "native-read/1"
    source: str = "immutable-source"
    source_tree: str = "source-tree"
    target_before: str = "target-before"
    integration: str = "actual-merge"
    expected_tree: str = "actual-tree"
    tree: str = "actual-tree"
    method: str = "merge"
    parents: tuple = ("target-before", "immutable-source")
    checkout: str = "actual-merge"
    checkout_tree: str = "actual-tree"


@dataclass(frozen=True)
class CurrentRead:
    ref: str
    sequence: int
    revision: int
    phase: str
    facts: Facts
    ratification: str | None


@dataclass
class EvidenceAuthority:
    """Separate model authority: caller self-reports cannot mint issued reads."""
    facts: Facts = Facts()
    native: NativeObservation | None = NativeObservation()
    revision: int = 0
    sequence: int = 0
    issued: dict = field(default_factory=dict)

    def tick(self):
        self.sequence += 1
        return self.sequence

    def read(self, phase, ratification=None):
        sequence = self.tick()
        token = CurrentRead(f"current-read/{sequence}", sequence, self.revision,
                            phase, self.facts, ratification)
        self.issued[token.ref] = token
        return token

    def change(self, **changes):
        self.facts = replace(self.facts, **changes)
        self.revision += 1

    def current(self, token):
        return (isinstance(token, CurrentRead)
                and self.issued.get(token.ref) == token
                and token.revision == self.revision and token.facts == self.facts
                and self.facts.eligible())


class Acceptance:
    """Model the current disjoint operation; never writes the held old store."""
    def __init__(self, authority=None):
        self.authority = authority if authority is not None else EvidenceAuthority()
        self.old = {"key": "original-builder-key", "generation": None,
                    "status": "UNKNOWN/HOLD", "accepted_bindings": "UNKNOWN",
                    "resources": "UNKNOWN", "terminal": None}
        self.task = "existing-task"
        self.selection = None
        self.request = None
        self.actual = None
        self.verified = None
        self.ratification_attempt = None
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
        native = self.authority.native
        valid = (not self.hold and facts == expected and facts.eligible()
                 and facts == self.authority.facts and native is not None
                 and actual.get("ack") == "known"
                 and actual.get("operation") == self.selection["operation"]
                 and actual.get("source") == expected.source
                 and actual.get("target_before") == expected.target
                 and native.source == expected.source and native.source_tree == expected.tree
                 and native.target_before == expected.target
                 and native.parents == (expected.target, expected.source)
                 and native.tree == native.expected_tree
                 and native.checkout == native.integration and native.checkout_tree == native.tree
                 and native.method == "merge"
                 and all(actual.get(name) == getattr(native, name) for name in
                         ("source", "target_before", "integration", "method", "parents",
                          "checkout", "checkout_tree", "tree", "expected_tree"))
                 and actual.get("compensation") is True
                 and actual.get("post_checks") is True)
        if not valid:
            self.hold = True
            self.incidents.append("UNRATIFIED actual integration outcome")
            return "UNRATIFIED"
        self.verified = {"actual": deepcopy(actual), "native": native}
        return "VERIFIED_OUTCOME"

    def publish_ratification(self, operation, receipt, acknowledged=True):
        if (self.hold or not self.verified or self.ratification_attempt
                or operation != self.selection["operation"] or not receipt
                or self.authority.facts != self.selection["facts"]
                or not self.authority.facts.eligible()
                or self.authority.native != self.verified["native"]):
            return "BLOCKED"
        self.ratification_attempt = {"receipt": receipt, "acknowledged": acknowledged}
        if acknowledged is not True:
            self.hold = True
            self.incidents.append("UNRATIFIED ratification publication acknowledgement")
            return "UNRATIFIED"
        actual = self.verified["actual"]
        self.ratified = {name: actual[name] for name in
                        ("source", "target_before", "integration", "tree", "operation")}
        self.ratified.update(receipt=receipt, native_ref=self.verified["native"].ref,
                             readback=False, read_sequence=None)
        return "RATIFICATION_PUBLISHED"

    def readback_ratification(self, receipt, binding):
        if (self.hold or not self.ratified or self.ratified["readback"]
                or self.authority.facts != self.selection["facts"]
                or not self.authority.facts.eligible()
                or self.authority.native != self.verified["native"]):
            return "BLOCKED"
        expected = {k: v for k, v in self.ratified.items()
                    if k not in {"readback", "read_sequence"}}
        if receipt != self.ratified["receipt"] or binding != expected:
            self.hold = True
            self.incidents.append("UNRATIFIED ratification readback missing/mismatched")
            return "UNRATIFIED"
        self.ratified["readback"] = True
        self.ratified["read_sequence"] = self.authority.tick()
        return "RATIFICATION_READ_BACK"

    def final(self, operation, integration, tree, facts, receipt, current=None):
        if (self.hold or not self.ratified or not self.selection
                or operation != self.selection["operation"]
                or facts != self.selection["facts"] or not facts.eligible()
                or not self.ratified["readback"]
                or not self.authority.current(current) or current.phase != "final"
                or current.facts != facts
                or current.ratification != self.ratified["receipt"]
                or current.sequence <= self.ratified["read_sequence"]
                or self.authority.native != self.verified["native"]
                or integration != self.ratified["integration"]
                or tree != self.ratified["tree"] or not receipt):
            return "BLOCKED"
        if self.delivery:
            return self.delivery["receipt"]
        self.delivery = {"task": self.task, "operation": operation,
                         "integration": integration, "tree": tree,
                         "receipt": receipt, "readback": False,
                         "ratification": self.ratified["receipt"], "current": current}
        return receipt

    def consume_delivery(self, receipt):
        if self.hold or not self.delivery or receipt != self.delivery["receipt"]:
            return "BLOCKED"
        if not self.authority.current(self.delivery["current"]):
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
        assert model.ratified.get("readback"), "ratification not read back"
        assert model.delivery["ratification"] == model.ratified["receipt"]
        current = model.delivery["current"]
        assert model.authority.issued.get(current.ref) == current
        assert current.phase == "final" and current.sequence > model.ratified["read_sequence"]
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
        self.assertEqual(self.m.observe(outcome(), self.f), "VERIFIED_OUTCOME")
        self.ratify(self.m)
        self.assertEqual((self.m.done, self.m.wakes), (0, 0))

    def ratify(self, model):
        self.assertEqual(model.publish_ratification("selection/1", "ratification/1"),
                         "RATIFICATION_PUBLISHED")
        binding = {k: v for k, v in model.ratified.items()
                   if k not in {"readback", "read_sequence"}}
        self.assertEqual(model.readback_ratification("ratification/1", binding),
                         "RATIFICATION_READ_BACK")

    def fresh(self, model=None):
        model = model if model is not None else self.m
        return model.authority.read("final", "ratification/1")

    def delivered(self):
        self.integrated()
        current = self.fresh()
        self.assertEqual(self.m.final("selection/1", "actual-merge", "actual-tree",
                                     self.f, "delivery/1", current), "delivery/1")
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
        self.ratify(self.m)
        current = self.fresh()
        self.rejected(lambda: self.m.old_result(self.f.source, "old-validation"), "STALE_AUTHORITY")
        self.rejected(lambda: self.m.final("old-grant", "actual-merge", "actual-tree", self.f, "old-receipt", current))
        self.m.final("selection/1", "actual-merge", "actual-tree", self.f, "delivery/1", current)
        self.m.consume_delivery("delivery/1")
        self.rejected(lambda: self.m.final("selection/1", "actual-merge", "actual-tree", self.f, "duplicate", current), "delivery/1")
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

    def test_P1_01_observation_and_publication_do_not_replace_ratification_readback(self):
        self.selected()
        self.m.request_integration("selection/1", self.f)
        self.assertEqual(self.m.observe(outcome(), self.f), "VERIFIED_OUTCOME")
        self.assertIsNone(self.m.ratified)
        current = self.fresh()
        self.rejected(lambda: self.m.final("selection/1", "actual-merge", "actual-tree",
                                           self.f, "d", current))
        self.m.publish_ratification("selection/1", "ratification/1")
        current = self.fresh()
        self.rejected(lambda: self.m.final("selection/1", "actual-merge", "actual-tree",
                                           self.f, "d", current))
        binding = {k: v for k, v in self.m.ratified.items()
                   if k not in {"readback", "read_sequence"}}
        self.m.readback_ratification("ratification/1", binding)
        # Even a FINAL-labelled read made before ratification readback is stale.
        self.rejected(lambda: self.m.final("selection/1", "actual-merge", "actual-tree",
                                           self.f, "d", current))
        fresh = self.fresh()
        self.assertEqual(self.m.final("selection/1", "actual-merge", "actual-tree",
                                     self.f, "d", fresh), "d")
        self.assertEqual((self.m.done, self.m.wakes), (0, 0))

    def test_P1_01_failed_unknown_publication_and_mismatched_missing_readback(self):
        for failure in ("failed-publication", "unknown-publication", "missing-readback",
                        "wrong-ref", "operation", "source", "target_before", "integration", "tree"):
            with self.subTest(failure=failure):
                m = Acceptance()
                m.select(self.f, "selection/1"); m.readback("selection/1", self.f)
                m.request_integration("selection/1", self.f)
                m.observe(outcome(), self.f)
                actual = deepcopy(m.actual)
                if failure.endswith("publication"):
                    ack = False if failure == "failed-publication" else None
                    self.assertEqual(m.publish_ratification("selection/1", "ratification/1", ack), "UNRATIFIED")
                else:
                    m.publish_ratification("selection/1", "ratification/1")
                    binding = {k: v for k, v in m.ratified.items()
                               if k not in {"readback", "read_sequence"}}
                    if failure == "missing-readback":
                        binding = None
                    elif failure != "wrong-ref":
                        binding[failure] = "incorrect"
                    ref = "wrong" if failure == "wrong-ref" else "ratification/1"
                    self.assertEqual(m.readback_ratification(ref, binding), "UNRATIFIED")
                self.assertEqual(m.actual, actual)
                self.assertTrue(m.hold and m.incidents)
                current = self.fresh(m)
                before = m.snapshot()
                self.assertEqual(m.final("selection/1", "actual-merge", "actual-tree",
                                         self.f, "d", current), "BLOCKED")
                self.assertEqual(m.snapshot(), before)
                self.assertEqual((m.done, m.wakes), (0, 0))
                invariant(m, self.old)

    def test_P1_02_coordinated_self_report_corruption_cannot_change_native_oracle(self):
        for corruption in (
                {"tree": "wrong", "expected_tree": "wrong", "checkout_tree": "wrong"},
                {"integration": "wrong", "checkout": "wrong"},
                {"source": "other", "parents": ("target-before", "other")},
                {"target_before": "other", "parents": ("other", "immutable-source")}):
            with self.subTest(corruption=corruption):
                m = Acceptance()
                native = m.authority.native
                m.select(self.f, "selection/1"); m.readback("selection/1", self.f)
                m.request_integration("selection/1", self.f)
                actual = outcome(**corruption)
                self.assertEqual(m.observe(actual, self.f), "UNRATIFIED")
                self.assertEqual(m.actual, actual)
                self.assertEqual(m.authority.native, native)
                self.assertIsNone(m.verified)
                self.assertIsNone(m.ratified)
                self.assertEqual((m.done, m.wakes), (0, 0))
                invariant(m, self.old)

    def test_P1_02_wrong_native_tree_or_missing_native_read_still_unratified(self):
        for native in (None, replace(NativeObservation(), tree="wrong", checkout_tree="wrong"),
                       replace(NativeObservation(), source_tree="wrong")):
            m = Acceptance(EvidenceAuthority(native=native))
            m.select(self.f, "selection/1"); m.readback("selection/1", self.f)
            m.request_integration("selection/1", self.f)
            self.assertEqual(m.observe(outcome(), self.f), "UNRATIFIED")
            self.assertIsNone(m.ratified)
            invariant(m, self.old)

    def test_P2_01_preselection_same_snapshot_cannot_prove_fresh_final_current(self):
        preselection = self.m.authority.read("selection")
        early_final = self.fresh()
        self.integrated()
        for old in (None, preselection, early_final):
            self.rejected(lambda: self.m.final("selection/1", "actual-merge", "actual-tree",
                                               self.f, "d", old))
        fresh = self.fresh()
        fake = replace(fresh, ref="unissued-current")
        self.rejected(lambda: self.m.final("selection/1", "actual-merge", "actual-tree",
                                           self.f, "d", fake))
        self.assertEqual(self.m.final("selection/1", "actual-merge", "actual-tree",
                                     self.f, "d", fresh), "d")

    def test_P2_01_late_finding_permission_target_and_revision_reject_old_true_replay(self):
        for changes in ({"findings_clear": False}, {"permission": False},
                        {"target": "late-target"}, {"dependencies": False}):
            with self.subTest(changes=changes):
                m = Acceptance()
                m.select(self.f, "selection/1"); m.readback("selection/1", self.f)
                m.request_integration("selection/1", self.f); m.observe(outcome(), self.f)
                self.ratify(m)
                old = self.fresh(m)
                m.authority.change(**changes)
                for token in (old, self.fresh(m)):
                    before = m.snapshot()
                    self.assertEqual(m.final("selection/1", "actual-merge", "actual-tree",
                                             self.f, "d", token), "BLOCKED")
                    self.assertEqual(m.snapshot(), before)
                # Restoring equal bytes/booleans does not make an old issued read fresh.
                m.authority.change(**{k: getattr(self.f, k) for k in changes})
                before = m.snapshot()
                self.assertEqual(m.final("selection/1", "actual-merge", "actual-tree",
                                         self.f, "d", old), "BLOCKED")
                self.assertEqual(m.snapshot(), before)
                new = self.fresh(m)
                self.assertEqual(m.final("selection/1", "actual-merge", "actual-tree",
                                         self.f, "d", new), "d")
                m.authority.change(permission=False)
                before = m.snapshot()
                self.assertEqual(m.consume_delivery("d"), "BLOCKED")
                self.assertEqual(m.snapshot(), before)
                self.assertEqual((m.done, m.wakes), (0, 0))
                invariant(m, self.old)

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

    def test_P2_01_bypassed_current_guard_is_detected_by_rejected_state_oracle(self):
        self.integrated()
        old = self.fresh()
        self.m.authority.change(permission=False)
        before = self.m.snapshot()
        with patch.object(self.m.authority, "current", return_value=True):
            self.m.final("selection/1", "actual-merge", "actual-tree", self.f, "d", old)
        with self.assertRaises(AssertionError):
            self.assertEqual(self.m.snapshot(), before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
