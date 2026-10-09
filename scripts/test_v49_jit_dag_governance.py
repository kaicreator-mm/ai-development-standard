"""T-009 deterministic JIT/DAG mutation classification tests (v4.9).

Executable oracles G01-G06 for references/JIT_DAG_MUTATION_GOVERNANCE_V49_REFERENCE.md
against fixtures/jit-dag-governance/**.

Authority: the v4.3 Task DAG Governance stays canonical and is consumed by exact
refs — the material mutation class vocabulary is parsed at runtime from
standards/TASK_DAG_GOVERNANCE_STANDARD.md §3 and the mutation-record required
fields are loaded at runtime from schemas/dag-mutation-record-v1.schema.json.
Nothing owner-owned is redefined or duplicated here (G06).
"""
from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
GOVERNANCE_STANDARD = ROOT / "standards" / "TASK_DAG_GOVERNANCE_STANDARD.md"
GOVERNANCE_REFERENCE = ROOT / "references" / "TASK_DAG_GOVERNANCE_REFERENCE.md"
MUTATION_RECORD_SCHEMA = ROOT / "schemas" / "dag-mutation-record-v1.schema.json"
WIRING_REFERENCE = ROOT / "references" / "JIT_DAG_MUTATION_GOVERNANCE_V49_REFERENCE.md"
EXECUTION_STANDARD = ROOT / "standards" / "EXECUTION_ARCHITECTURE_STANDARD.md"
PRD = ROOT / "docs" / "implementation" / "4.9.0" / "PRD.md"
L2_EVIDENCE = ROOT / "docs" / "implementation" / "4.9.0" / "L2_ARCHITECTURE_EVIDENCE.md"
FIXTURES = ROOT / "fixtures" / "jit-dag-governance"

PHASE_ACTION = "jit_phase_dispatch_same_issue"
FAIL_CLOSED_ROUTE = "FAIL_CLOSED_PRESERVE_PRIOR_LIVE_DAG"
CONCERN_CLASSES = (
    "ADD",
    "ADD_DEPENDENCY",
    "REMOVE_DEPENDENCY",
    "SPLIT",
    "MERGE",
    "SUPERSEDE",
    "DEFER",
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_owner_mutation_classes(standard_text: str) -> set[str]:
    """Owner §3 vocabulary — parsed from the owner standard, never restated here."""
    section = standard_text.split("## 3. Material mutation classes", 1)[1]
    block = section.split("```text", 1)[1].split("```", 1)[0]
    return {line.strip() for line in block.splitlines() if line.strip()}


def parse_reference_json_block(reference_text: str, marker: str) -> dict:
    chunk = reference_text.split(marker, 1)[1]
    block = chunk.split("```json", 1)[1].split("```", 1)[0]
    return json.loads(block)


def record_defects(record: object, schema: dict) -> list[str]:
    """Completeness of a dag-mutation-record-v1, validated against the OWNER schema:
    required fields present; emptiness judged by the schema's own minLength/minItems."""
    if not isinstance(record, dict):
        return ["RECORD_ABSENT"]
    defects: list[str] = []
    properties = schema["properties"]
    for field in schema["required"]:
        if field not in record or record[field] is None:
            defects.append(f"RECORD_FIELD_MISSING:{field}")
            continue
        prop = properties.get(field, {})
        value = record[field]
        if isinstance(value, str) and len(value) < prop.get("minLength", 0):
            defects.append(f"RECORD_FIELD_EMPTY:{field}")
        elif isinstance(value, list) and len(value) < prop.get("minItems", 0):
            defects.append(f"RECORD_FIELD_EMPTY:{field}")
    return defects


def evaluate_currentness(proposal: dict, facts_plane: dict) -> str:
    """Owner §9: the record is current only for the exact subject it reviewed."""
    bound = proposal.get("bound_topology_digest")
    if not bound or bound == "UNKNOWN":
        return "UNKNOWN_CURRENTNESS"
    if bound != facts_plane["live_topology_digest"]:
        return "STALE"
    packs = facts_plane["task_pack_refs_current"]
    record = proposal.get("mutation_record")
    refs = record.get("task_pack_impact_refs", []) if isinstance(record, dict) else []
    for ref in refs:
        if packs.get(ref) != "CURRENT":
            return "STALE"
    return "CURRENT"


def classify_and_route(
    proposal: dict,
    facts_plane: dict,
    owner_classes: set[str],
    bookkeeping_actions: set[str],
    routes: dict,
    special_routes: dict,
    record_schema: dict,
) -> dict:
    """Deterministic pure classifier (reference §2). Identical inputs => identical outcome.

    Fixed evaluation order: unknown action -> semantic mutation (telemetry, record,
    currentness, readiness, native hydration) -> bookkeeping (topology effects,
    envelope) -> bookkeeping-only.
    """
    action = proposal["action"]

    def decision(
        classification: str,
        route: str,
        reasons: list[str],
        topology_changed: bool = False,
        native_performed: bool = False,
        record_required: bool = False,
    ) -> dict:
        return {
            "proposal_id": proposal["id"],
            "classification": classification,
            "route": route,
            "reasons": reasons,
            "semantic_topology_changed": topology_changed,
            "native_mutation_performed": native_performed,
            "mutation_record_required": record_required,
        }

    def fail_closed(reasons: list[str]) -> dict:
        return decision(
            "FAIL_CLOSED",
            special_routes["fail_closed_route"],
            reasons + [FAIL_CLOSED_ROUTE],
        )

    # 1. unknown action: ambiguous semantic impact fails closed (owner §10, reference §2.3)
    if action not in owner_classes and action not in bookkeeping_actions:
        return fail_closed(["FAIL_CLOSED_AMBIGUOUS_ACTION"])

    # 2. semantic mutation: route to the v4.3 owner with record + native hydration
    if action in owner_classes:
        if proposal.get("telemetry_only_justification"):
            return fail_closed(["FAIL_CLOSED_TELEMETRY_CANNOT_AUTHORIZE"])
        defects = record_defects(proposal.get("mutation_record"), record_schema)
        if defects:
            return fail_closed(["FAIL_CLOSED_MISSING_MUTATION_RECORD"] + defects)
        currentness = evaluate_currentness(proposal, facts_plane)
        if currentness == "UNKNOWN_CURRENTNESS":
            return fail_closed(["FAIL_CLOSED_UNKNOWN_CURRENTNESS"])
        if currentness == "STALE":
            return fail_closed(["FAIL_CLOSED_STALE_MUTATION_RECORD"])
        if action == "REMOVE_DEPENDENCY" and proposal.get("fabricates_readiness"):
            return fail_closed(["FAIL_CLOSED_READINESS_FABRICATION"])
        hydration = proposal.get("native_hydration") or {}
        if not hydration.get("authorized_executor"):
            # owner §7: explicit controller/local handoff with read-back equality check
            return decision(
                "SEMANTIC_MUTATION",
                special_routes["unavailable_native_capability_route"],
                ["NATIVE_CAPABILITY_UNAVAILABLE_CONTROLLER_HANDOFF_REQUIRED"],
                topology_changed=True,
            )
        if not (hydration.get("performed") and hydration.get("read_back")):
            if hydration.get("textual_dependency_list_only"):
                return fail_closed(["FAIL_CLOSED_TEXTUAL_LIST_NOT_NATIVE"])
            return decision(
                "SEMANTIC_MUTATION",
                special_routes["unavailable_native_capability_route"],
                ["NATIVE_EXECUTION_STILL_OWED"],
                topology_changed=True,
            )
        return decision(
            "SEMANTIC_MUTATION",
            routes[action]["route"],
            ["ROUTED_TO_V43_GOVERNANCE_WITH_MUTATION_RECORD_AND_NATIVE_HYDRATION"],
            topology_changed=True,
            native_performed=True,
            record_required=True,
        )

    # 3. bookkeeping: execution-container operations only (reference §2.1)
    if action == PHASE_ACTION:
        # §29.2 envelope predicate first: a phase not proven in-envelope is BLOCKED,
        # never auto-admitted (Frozen Product L; §29.7 binding L)
        conditions = proposal["envelope_conditions"]
        if any(value is True or value is None for value in conditions.values()):
            return decision(
                "BLOCKED", "BLOCKED_OUT_OF_TASK_ENVELOPE", ["JIT_PHASE_NOT_PROVEN_IN_ENVELOPE"]
            )
    effects = proposal["effects"]
    if any(value is True or value is None for value in effects.values()):
        return fail_closed(["FAIL_CLOSED_BOOKKEEPING_WITH_TOPOLOGY_EFFECTS"])
    return decision(
        "BOOKKEEPING",
        "NO_MUTATION_REQUIRED",
        ["EXECUTION_CONTAINER_BOOKKEEPING_ONLY"],
    )


class JitDagGovernanceClassification(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.owner_standard = GOVERNANCE_STANDARD.read_text(encoding="utf-8")
        cls.owner_reference = GOVERNANCE_REFERENCE.read_text(encoding="utf-8")
        cls.wiring_reference = WIRING_REFERENCE.read_text(encoding="utf-8")
        cls.execution_standard = EXECUTION_STANDARD.read_text(encoding="utf-8")
        cls.prd = PRD.read_text(encoding="utf-8")
        cls.l2 = L2_EVIDENCE.read_text(encoding="utf-8")
        cls.record_schema = load_json(MUTATION_RECORD_SCHEMA)
        cls.owner_refs = load_json(FIXTURES / "owner_refs.json")
        cls.classification_table = load_json(FIXTURES / "classification_table.json")
        cls.currentness_facts = load_json(FIXTURES / "currentness_facts.json")
        cls.proposals = load_json(FIXTURES / "proposals.json")["proposals"]
        cls.owner_classes = parse_owner_mutation_classes(cls.owner_standard)
        cls.reference_wiring = parse_reference_json_block(
            cls.wiring_reference, "## 3. Routing table (machine-readable)"
        )
        cls.reference_bookkeeping = parse_reference_json_block(
            cls.wiring_reference, "Bookkeeping action vocabulary"
        )

    def decide(self, proposal: dict) -> dict:
        return classify_and_route(
            proposal,
            self.currentness_facts["planes"][proposal["fact_plane"]],
            self.owner_classes,
            set(self.classification_table["bookkeeping_actions"]),
            self.reference_wiring["routes"],
            self.reference_wiring,
            self.record_schema,
        )

    # ---------- G01: bookkeeping is NOT semantic mutation and never mutates topology ----------

    def test_g01_bookkeeping_is_not_semantic_mutation(self) -> None:
        bookkeeping = [
            proposal
            for proposal in self.proposals
            if proposal["action"] in self.classification_table["bookkeeping_actions"]
            and proposal["expected"]["classification"] == "BOOKKEEPING"
        ]
        self.assertGreaterEqual(len(bookkeeping), 6)
        for proposal in bookkeeping:
            with self.subTest(proposal=proposal["id"]):
                outcome = self.decide(proposal)
                self.assertEqual(outcome["classification"], "BOOKKEEPING")
                self.assertEqual(outcome["route"], "NO_MUTATION_REQUIRED")
                self.assertIn("EXECUTION_CONTAINER_BOOKKEEPING_ONLY", outcome["reasons"])
                self.assertFalse(outcome["semantic_topology_changed"])
                self.assertFalse(outcome["native_mutation_performed"])
                self.assertFalse(outcome["mutation_record_required"])

    def test_g01_bookkeeping_never_silently_changes_semantic_topology(self) -> None:
        for proposal in self.proposals:
            outcome = self.decide(proposal)
            if outcome["classification"] in {"BOOKKEEPING", "FAIL_CLOSED", "BLOCKED"}:
                with self.subTest(proposal=proposal["id"]):
                    self.assertFalse(outcome["semantic_topology_changed"])
                    self.assertFalse(outcome["native_mutation_performed"])
        self.assertIn(
            "Bookkeeping NEVER silently changes semantic topology", self.wiring_reference
        )

    def test_g01_bookkeeping_vocabulary_matches_reference_and_fixture(self) -> None:
        self.assertEqual(
            set(self.classification_table["bookkeeping_actions"]),
            set(self.reference_bookkeeping["bookkeeping_actions"]),
        )
        invariants = self.classification_table["bookkeeping_invariants"]
        self.assertFalse(invariants["semantic_topology_changed"])
        self.assertEqual(invariants["native_edges_changed"], 0)
        self.assertEqual(invariants["semantic_tasks_created"], 0)
        self.assertEqual(invariants["semantic_tasks_closed_or_superseded"], 0)

    def test_g01_classifier_is_deterministic(self) -> None:
        for proposal in self.proposals:
            with self.subTest(proposal=proposal["id"]):
                self.assertEqual(self.decide(proposal), self.decide(proposal))

    # ---------- G02: each mutation class routes exactly per the reference ----------

    def test_g02_owner_vocabulary_equals_reference_routing_table_and_fixture(self) -> None:
        self.assertEqual(
            self.owner_classes, set(self.reference_wiring["routes"]), "owner §3 vocabulary"
        )
        self.assertEqual(
            set(self.classification_table["expected_routes"]),
            self.owner_classes,
            "fixture expected routes",
        )
        for action, route in self.classification_table["expected_routes"].items():
            with self.subTest(action=action):
                self.assertEqual(self.reference_wiring["routes"][action]["route"], route)

    def test_g02_every_concern_class_routes_exactly_per_reference(self) -> None:
        routed_actions: set[str] = set()
        for proposal in self.proposals:
            outcome = self.decide(proposal)
            if outcome["classification"] == "SEMANTIC_MUTATION" and outcome[
                "route"
            ].startswith("V43_MUTATION_"):
                routed_actions.add(proposal["action"])
                with self.subTest(proposal=proposal["id"]):
                    self.assertEqual(
                        outcome["route"],
                        proposal["expected"]["route"],
                        "classifier route must equal fixture expectation",
                    )
                    self.assertEqual(
                        outcome["route"],
                        self.reference_wiring["routes"][proposal["action"]]["route"],
                        "classifier route must equal the reference routing table",
                    )
                    self.assertEqual(
                        outcome["route"],
                        self.classification_table["expected_routes"][proposal["action"]],
                        "classifier route must equal the fixture route table",
                    )
        for action in CONCERN_CLASSES:
            self.assertIn(action, routed_actions)
        self.assertIn("CHANGE_LANE", routed_actions)
        self.assertIn("CHANGE_INTEGRATION_OWNER", routed_actions)

    def test_g02_dependency_removal_cannot_fabricate_readiness(self) -> None:
        proposal = self.by_id("SM04_REMOVE_DEPENDENCY_fabricates_readiness")
        outcome = self.decide(proposal)
        self.assertEqual(outcome["classification"], "FAIL_CLOSED")
        self.assertIn("FAIL_CLOSED_READINESS_FABRICATION", outcome["reasons"])
        self.assertFalse(outcome["native_mutation_performed"])
        self.assertIn("MUST NOT fabricate readiness", self.owner_standard)

    # ---------- G03: runtime proposals need record + native hydration; text is not graph ----------

    def test_g03_routed_runtime_proposals_carry_record_and_native_hydration(self) -> None:
        for proposal in self.proposals:
            outcome = self.decide(proposal)
            if outcome["route"].startswith("V43_MUTATION_") and proposal[
                "origin"
            ] == "runtime_jit":
                with self.subTest(proposal=proposal["id"]):
                    self.assertIsInstance(proposal.get("mutation_record"), dict)
                    self.assertTrue(proposal["mutation_record"]["requested_by"])
                    self.assertTrue(proposal["mutation_record"]["approved_by"])
                    hydration = proposal["native_hydration"]
                    self.assertTrue(hydration["authorized_executor"])
                    self.assertTrue(hydration["performed"])
                    self.assertTrue(hydration["read_back"])
                    self.assertIn(
                        "ROUTED_TO_V43_GOVERNANCE_WITH_MUTATION_RECORD_AND_NATIVE_HYDRATION",
                        outcome["reasons"],
                    )
                    self.assertTrue(outcome["mutation_record_required"])

    def test_g03_missing_or_incomplete_record_fails_closed(self) -> None:
        for proposal_id in (
            "SM11_runtime_semantic_without_mutation_record",
            "SM16_runtime_incomplete_mutation_record",
        ):
            with self.subTest(proposal=proposal_id):
                outcome = self.decide(self.by_id(proposal_id))
                self.assertEqual(outcome["classification"], "FAIL_CLOSED")
                self.assertIn("FAIL_CLOSED_MISSING_MUTATION_RECORD", outcome["reasons"])
                self.assertFalse(outcome["native_mutation_performed"])
        self.assertIn(
            "it does not perform the mutation by itself", self.wiring_reference
        )

    def test_g03_textual_dependency_list_cannot_substitute_for_native_graph(self) -> None:
        outcome = self.decide(self.by_id("SM12_runtime_textual_dependency_list_only"))
        self.assertEqual(outcome["classification"], "FAIL_CLOSED")
        self.assertIn("FAIL_CLOSED_TEXTUAL_LIST_NOT_NATIVE", outcome["reasons"])
        self.assertIn("CANNOT substitute for native", self.wiring_reference)
        self.assertIn(
            "MUST NOT substitute for native live dependency edges", self.owner_standard
        )

    def test_g03_unavailable_native_capability_requires_explicit_handoff(self) -> None:
        outcome = self.decide(self.by_id("SM13_runtime_native_capability_unavailable"))
        self.assertEqual(outcome["classification"], "SEMANTIC_MUTATION")
        self.assertEqual(outcome["route"], "V43_NATIVE_MUTATION_HANDOFF")
        self.assertFalse(outcome["native_mutation_performed"])
        self.assertIn("create an explicit controller/local handoff", self.owner_standard)

    # ---------- G04: mutation currentness; stale proposals fail closed ----------

    def test_g04_stale_mutation_record_fails_closed(self) -> None:
        outcome = self.decide(self.by_id("SM14_runtime_stale_mutation_record"))
        self.assertEqual(outcome["classification"], "FAIL_CLOSED")
        self.assertIn("FAIL_CLOSED_STALE_MUTATION_RECORD", outcome["reasons"])
        self.assertEqual(outcome["route"], FAIL_CLOSED_ROUTE)
        self.assertFalse(outcome["native_mutation_performed"])
        self.assertIn(
            "drift requires re-evaluation before native mutation", self.owner_standard
        )
        self.assertIn("preserve the prior live DAG", self.owner_standard)

    def test_g04_unknown_currentness_fails_closed(self) -> None:
        outcome = self.decide(self.by_id("SM15_runtime_unknown_currentness"))
        self.assertEqual(outcome["classification"], "FAIL_CLOSED")
        self.assertIn("FAIL_CLOSED_UNKNOWN_CURRENTNESS", outcome["reasons"])
        self.assertFalse(outcome["native_mutation_performed"])

    def test_g04_currentness_owner_sections_cited(self) -> None:
        self.assertIn("## 9. Mutation currentness", self.owner_standard)
        self.assertIn("## 10. Failure handling", self.owner_standard)
        self.assertIn("§9", self.wiring_reference)
        self.assertIn("§10", self.wiring_reference)

    # ---------- G05: Frozen Product L + L2 JIT/DAG negatives with exact refs ----------

    def test_g05_frozen_product_l_exact_ref(self) -> None:
        self.assertIn("### L. Task-DAG scope protection", self.prd)
        self.assertIn(
            "cannot invent new semantic implementation work/dependencies outside Frozen Task authority",
            self.prd,
        )
        self.assertEqual(
            self.owner_refs["frozen_product_item_L"],
            "docs/implementation/4.9.0/PRD.md",
        )

    def test_g05_execution_standard_exact_refs(self) -> None:
        self.assertIn(
            "A material topology change (new semantic Task, added/removed blocked-by edge, "
            "split/merge/supersede) is not a JIT phase: it routes to v4.3 Task DAG mutation "
            "governance with the corresponding mutation evidence.",
            self.execution_standard,
        )
        self.assertIn("changes route to v4.3 governance (§29.2). [K02/K09]",
                      self.execution_standard)

    def test_g05_l2_negatives_exact_refs(self) -> None:
        self.assertIn(
            "JIT phase not in Assurance Plan/Task Pack treated as in-envelope => reject",
            self.execution_standard,
        )
        self.assertIn(
            "runtime scope invention", self.l2
        )

    def test_g05_jit_phase_outside_envelope_blocked_never_auto_admitted(self) -> None:
        for proposal_id in (
            "LNEG01_phase_outside_envelope_scope_widening",
            "LNEG02_undeclared_phase_never_in_envelope",
        ):
            with self.subTest(proposal=proposal_id):
                outcome = self.decide(self.by_id(proposal_id))
                self.assertEqual(outcome["classification"], "BLOCKED")
                self.assertEqual(outcome["route"], "BLOCKED_OUT_OF_TASK_ENVELOPE")
                self.assertNotEqual(outcome["classification"], "BOOKKEEPING")
                self.assertFalse(outcome["native_mutation_performed"])

    def test_g05_material_topology_change_is_never_bookkeeping(self) -> None:
        outcome = self.decide(self.by_id("LNEG03_topology_effect_mislabeled_as_bookkeeping"))
        self.assertEqual(outcome["classification"], "FAIL_CLOSED")
        self.assertIn("FAIL_CLOSED_BOOKKEEPING_WITH_TOPOLOGY_EFFECTS", outcome["reasons"])
        outcome_unknown = self.decide(self.by_id("LNEG04_unknown_action_smaller_units"))
        self.assertIn("FAIL_CLOSED_AMBIGUOUS_ACTION", outcome_unknown["reasons"])

    def test_g05_telemetry_cannot_authorize_mutation(self) -> None:
        outcome = self.decide(self.by_id("TEL01_telemetry_only_split_request"))
        self.assertEqual(outcome["classification"], "FAIL_CLOSED")
        self.assertIn("FAIL_CLOSED_TELEMETRY_CANNOT_AUTHORIZE", outcome["reasons"])
        self.assertFalse(outcome["native_mutation_performed"])
        self.assertIn("advisory evidence only", self.wiring_reference)
        self.assertIn("cannot independently authorize a mutation", self.wiring_reference)

    def test_g05_exact_refs_resolve_on_disk(self) -> None:
        exact_refs = [
            self.owner_refs["governance_owner_standard"],
            self.owner_refs["mutation_record_schema"],
            self.owner_refs["governance_owner_reference"],
            self.owner_refs["wiring_reference"],
            self.owner_refs["jit_predicate_owner"],
            self.owner_refs["frozen_product_item_L"],
            self.owner_refs["frozen_l2_evidence"],
        ]
        for ref in exact_refs:
            with self.subTest(ref=ref):
                self.assertTrue((ROOT / ref).is_file(), f"exact ref does not resolve: {ref}")
        for test_ref in self.owner_refs["governance_owner_tests"]:
            self.assertTrue((ROOT / test_ref).is_file(), f"owner test missing: {test_ref}")

    # ---------- G06: no second governance lifecycle; owner cited, not copied ----------

    def test_g06_semantic_vocabulary_owned_by_v43_standard_only(self) -> None:
        parsed = parse_owner_mutation_classes(self.owner_standard)
        self.assertEqual(
            parsed,
            {"ADD", "SPLIT", "MERGE", "SUPERSEDE", "ADD_DEPENDENCY", "REMOVE_DEPENDENCY",
             "CHANGE_LANE", "CHANGE_INTEGRATION_OWNER", "DEFER"},
        )
        # the classifier receives the owner vocabulary as a runtime input; a class that
        # the owner standard does not define can never route as a known mutation
        stranger = dict(self.by_id("SM01_runtime_ADD"))
        stranger["id"] = "STRANGER"
        stranger["action"] = "NOT_AN_OWNER_CLASS"
        outcome = classify_and_route(
            stranger,
            self.currentness_facts["planes"]["current"],
            self.owner_classes,
            set(self.classification_table["bookkeeping_actions"]),
            self.reference_wiring["routes"],
            self.reference_wiring,
            self.record_schema,
        )
        self.assertEqual(outcome["classification"], "FAIL_CLOSED")

    def test_g06_record_fields_loaded_from_owner_schema(self) -> None:
        required = self.record_schema["required"]
        for field in (
            "requested_by",
            "approved_by",
            "reason",
            "old_edges",
            "new_edges",
            "validation_impact_ref",
        ):
            self.assertIn(field, required)
        self.assertEqual(self.owner_refs["mutation_record_schema"],
                         "schemas/dag-mutation-record-v1.schema.json")
        self.assertIn("dag-mutation-record-v1", self.wiring_reference)

    def test_g06_wiring_reference_cites_owner_by_exact_refs(self) -> None:
        for exact_ref in (
            "standards/TASK_DAG_GOVERNANCE_STANDARD.md",
            "§3",
            "§4",
            "§6",
            "§7",
            "§9",
            "§10",
            "§11",
            "schemas/dag-mutation-record-v1.schema.json",
            "references/TASK_DAG_GOVERNANCE_REFERENCE.md",
            "scripts/test_v43_task_dag_governance.py",
            "scripts/test_v43_dag_mutation_contract.py",
            "standards/EXECUTION_ARCHITECTURE_STANDARD.md",
            "§29.2",
            "b9fe0cc7089f64929b4bcf45f7230d950e864db2",
            "4f358ba2b32e01ae17ddcdf970151cf28e44bb3f",
        ):
            with self.subTest(exact_ref=exact_ref):
                self.assertIn(exact_ref, self.wiring_reference)

    def test_g06_no_second_lifecycle_and_non_normative_posture(self) -> None:
        self.assertIn("Non-normative", self.wiring_reference)
        self.assertIn("no second governance lifecycle", self.wiring_reference)
        self.assertIn("cites it, it does not copy or replace it", self.wiring_reference)
        self.assertIn("SINGLE OWNER", self.wiring_reference)
        for non_goal in ("a second DAG service", "a new Task/workflow state vocabulary"):
            self.assertIn(non_goal, self.owner_standard)

    # ---------- fixture integrity ----------

    def by_id(self, proposal_id: str) -> dict:
        for proposal in self.proposals:
            if proposal["id"] == proposal_id:
                return proposal
        raise AssertionError(f"proposal not found: {proposal_id}")

    def test_fixture_ids_unique_and_expectations_in_vocabulary(self) -> None:
        ids = [proposal["id"] for proposal in self.proposals]
        self.assertEqual(len(ids), len(set(ids)))
        for proposal in self.proposals:
            with self.subTest(proposal=proposal["id"]):
                self.assertIn(
                    proposal["expected"]["classification"],
                    {"BOOKKEEPING", "SEMANTIC_MUTATION", "FAIL_CLOSED", "BLOCKED"},
                )
                self.assertIn(proposal["origin"], {"runtime_jit", "planning"})
                self.assertIn(proposal["fact_plane"], self.currentness_facts["planes"])
        routed = {
            proposal["expected"]["route"]
            for proposal in self.proposals
            if proposal["expected"]["classification"] == "SEMANTIC_MUTATION"
        }
        allowed = (
            {entry["route"] for entry in self.reference_wiring["routes"].values()}
            | {self.reference_wiring["unavailable_native_capability_route"]}
        )
        self.assertTrue(routed <= allowed)


if __name__ == "__main__":
    unittest.main()
