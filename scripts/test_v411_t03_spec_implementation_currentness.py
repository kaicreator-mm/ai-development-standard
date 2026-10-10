"""V411-T03 focused regression: accepted spec implementation currentness.

Encodes the V411-T03 Task Pack P01-P03/N01-N08 oracles for concern J05
(ACCEPTED_SPEC_IMPLEMENTATION_CURRENTNESS) as:

1. deterministic section-scoped textual contract checks against the
   accepted-spec-to-implementation reconciliation clauses added to
   `standards/INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md` (SS3-9/11-12); and
2. a fixture-driven reconciliation decision model that binds those clauses to
   concrete verdicts (RECONCILED / NONMATERIAL / NOT_RUN / STALE / BLOCKED /
   INCOMPATIBLE / UNKNOWN) over accepted-spec, producer-subject, consumer-window
   and dimension evidence projections.

The decision states are compatibility-domain evidence vocabulary in this test
only; the standard deliberately does not mint new Gate/Validation/Release
states. The seven logical projection fields stay text-proposed only (owned by
the centrally designated wiring task); the v1 schema is asserted untouched.
Purely offline, standard library only.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "standards" / "INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md"
SCHEMA = ROOT / "schemas" / "compatibility-record-v1.schema.json"

CANONICAL_HEADINGS = (
    "# Interface & Compatibility Governance Standard",
    "## 1. Purpose",
    "## 2. Authority boundary",
    "## 3. Exact subject and baseline binding",
    "## 4. Change operation is not compatibility outcome",
    "## 5. Compatibility is multi-dimensional and extensible",
    "## 6. Producer, consumer, and window evidence",
    "## 7. Generated clients and derived artifacts",
    "## 8. Deprecation and removal",
    "## 9. Fast Path and materiality",
    "## 10. Required forbidden-inference matrix",
    "## 11. Machine-contract relation",
    "## 12. Failure handling",
)

# The five identity/authority/subject refs that must be individually present
# for any reconciliation decision; the two list-valued projection fields are
# checked for presence separately (empty list is explicit, None is missing).
IDENTITY_REFS = (
    "spec_baseline_ref",
    "proposed_delta_ref",
    "acceptance_authority_ref",
    "accepted_spec_current_ref",
    "implementation_subject_ref",
)

# The seven logical fields of the accepted-spec evidence projection (Task Pack
# S4). They are asserted present in the standard's prose and absent from the
# v1 schema: any additive machine projection is centrally owned wiring.
PROJECTION_REFS = IDENTITY_REFS + (
    "affected_producer_consumer_windows",
    "revalidation_refs",
)

# Decision-model vocabulary (test-level oracles bound to the standard clauses).
DECISION_STATES = {
    "RECONCILED",
    "NONMATERIAL",
    "NOT_RUN",
    "STALE",
    "BLOCKED",
    "INCOMPATIBLE",
    "UNKNOWN",
}

# Evidence kinds that never prove a current implementation or behavior.
NON_BEHAVIORAL_EVIDENCE_KINDS = frozenset({"archive_merge", "codegen", "checker_only"})

# v1 reader surface mirrored from schemas/compatibility-record-v1.schema.json
# for the N08 historical-compat oracle (no network, no jsonschema dependency).
V1_SCHEMA_PROPERTIES = {
    "schema_version",
    "record_id",
    "contract",
    "baseline",
    "candidate",
    "change_operations",
    "dimensions",
    "producer_refs",
    "consumer_refs",
    "compatibility_window_ref",
    "notes_ref",
}
V1_REQUIRED = {
    "schema_version",
    "record_id",
    "contract",
    "baseline",
    "candidate",
    "change_operations",
    "dimensions",
}
V1_OUTCOME_ENUM = {
    "COMPATIBLE",
    "CONDITIONALLY_COMPATIBLE",
    "INCOMPATIBLE",
    "UNKNOWN",
    "NOT_APPLICABLE",
}

REQUIRED_DIMENSIONS = ("wire", "source", "behavior")


def standard_text() -> str:
    return STANDARD.read_text(encoding="utf-8")


def section(heading: str) -> str:
    text = standard_text()
    start = text.index(heading)
    rest = text[start + len(heading) :]
    next_heading = rest.find("\n## ")
    return rest if next_heading == -1 else rest[:next_heading]


def decide(projection: dict) -> dict:
    """Deterministic V411-T03 S4 reconciliation decision model.

    Maps an accepted-spec evidence projection plus per-window dimension
    evidence to exactly one decision state with traceable reasons. Rule order
    is fail-closed: explicit nonmaterial proportionality, missing identity,
    untestable externals, drift, non-behavioral GREEN, accepted-not-implemented,
    superseded evidence subject, per-window coverage/outcomes, then RECONCILED.
    """
    reasons: list[str] = []
    if projection.get("nonmaterial") and not projection.get("affected_producer_consumer_windows"):
        return decision(
            "NONMATERIAL",
            ["explicit proportionate nonmaterial disposition; no empty heavyweight record"],
        )
    missing = [
        ref for ref in IDENTITY_REFS if not projection.get(ref)
    ]
    missing += [
        ref
        for ref in ("affected_producer_consumer_windows", "revalidation_refs")
        if projection.get(ref) is None
    ]
    if missing:
        return decision(
            "UNKNOWN", [f"missing required projection field: {ref}" for ref in missing]
        )
    windows = projection["affected_producer_consumer_windows"]
    if not windows:
        return decision("UNKNOWN", ["no evidenced affected producer/consumer window"])
    untestable = [w["consumer_ref"] for w in windows if w.get("external_untestable")]
    if untestable:
        return decision(
            "NOT_RUN",
            [
                f"material untestable external consumer {ref} explicitly NOT_RUN; "
                "routed to an exact-subject Validation owner"
                for ref in untestable
            ],
        )
    if projection.get("drifted_material_scope"):
        return decision(
            "STALE",
            [
                f"prior evidence STALE for drifted {scope}; revalidation required"
                for scope in projection["drifted_material_scope"]
            ],
        )
    if projection.get("evidence_kind") in NON_BEHAVIORAL_EVIDENCE_KINDS:
        return decision(
            "BLOCKED",
            [
                "archive merge/codegen/checker-only GREEN is not current "
                "implementation or behavior evidence; no Validation or Release promotion"
            ],
        )
    if not projection.get("implements_accepted_delta"):
        return decision(
            "BLOCKED",
            [
                "accepted spec current revision is not the shipped producer "
                "implementation subject; an accepted spec is not code and "
                "acceptance is not implementation"
            ],
        )
    if projection.get("evidence_subject_ref") != projection["implementation_subject_ref"]:
        return decision(
            "STALE",
            [
                "required dimensions were observed on a superseded subject; current "
                "implementation assertion rejected; revalidation required"
            ],
        )
    for window in windows:
        outcomes = window.get("dimension_outcomes") or {}
        for dim in window.get("required_dimensions", ()):
            observed = outcomes.get(dim)
            if observed is None:
                reasons.append(
                    f"still-supported window {window['consumer_ref']} lacks required "
                    f"{dim} evidence"
                )
            elif observed == "INCOMPATIBLE":
                reasons.append(
                    f"still-supported window {window['consumer_ref']} is INCOMPATIBLE "
                    f"on {dim}"
                )
    if any("INCOMPATIBLE" in reason for reason in reasons):
        return decision("INCOMPATIBLE", reasons)
    if reasons:
        return decision("UNKNOWN", reasons)
    return decision(
        "RECONCILED",
        [
            "accepted spec, current producer implementation, and supported consumer "
            "windows reconciled for the named contract/window; no Validation or "
            "Release PASS is implied"
        ],
    )


def decision(state: str, reasons: list[str]) -> dict:
    assert state in DECISION_STATES
    return {"decision": state, "reasons": reasons}


def evidenced_window(consumer_ref: str, outcomes: dict | None = None) -> dict:
    window = {
        "consumer_ref": consumer_ref,
        "required_dimensions": REQUIRED_DIMENSIONS,
    }
    if outcomes is not None:
        window["dimension_outcomes"] = outcomes
    return window


def v1_reader_accepts(record: object) -> bool:
    """Minimal structural v1 reader mirroring compatibility-record-v1 schema.

    Mirrors required keys, the closed property sets (`additionalProperties`:
    false) and the outcome enum so the historical-reader oracle runs offline.
    """
    if not isinstance(record, dict):
        return False
    if record.get("schema_version") != 1:
        return False
    if not V1_REQUIRED <= set(record):
        return False
    if not set(record) <= V1_SCHEMA_PROPERTIES:
        return False
    contract = record["contract"]
    if not isinstance(contract, dict) or set(contract) != {"kind", "identity"}:
        return False
    if not all(isinstance(value, str) and value for value in contract.values()):
        return False
    for side in ("baseline", "candidate"):
        part = record[side]
        if not isinstance(part, dict) or "sha_or_digest" not in part:
            return False
        if not set(part) <= {"version_ref", "sha_or_digest"}:
            return False
        if not isinstance(part["sha_or_digest"], str) or not part["sha_or_digest"]:
            return False
    operations = record["change_operations"]
    if not isinstance(operations, list) or len(operations) < 1:
        return False
    if not all(isinstance(op, str) and op for op in operations):
        return False
    dimensions = record["dimensions"]
    if not isinstance(dimensions, list) or len(dimensions) < 1:
        return False
    for dim in dimensions:
        if not isinstance(dim, dict):
            return False
        if not {"name", "outcome", "evidence_refs"} <= set(dim):
            return False
        if not set(dim) <= {"name", "outcome", "evidence_refs", "notes_ref"}:
            return False
        if dim["outcome"] not in V1_OUTCOME_ENUM:
            return False
        if not isinstance(dim["evidence_refs"], list):
            return False
    return True


# ---------------------------------------------------------------------------
# Fixtures: accepted spec S1, producer revisions H0 (old) / H1 (new), supported
# consumers C0 / C1, per Task Pack S3 scenarios.
# ---------------------------------------------------------------------------

AUTHORIZED_AUTHORITY = "authority/frozen-issue-comment"
ACCEPTED_S1 = "spec/S1@accepted-delta-sha"

P01_PROJECTION = {
    "spec_baseline_ref": "spec/S1@baseline-sha",
    "proposed_delta_ref": ACCEPTED_S1,
    "acceptance_authority_ref": AUTHORIZED_AUTHORITY,
    "accepted_spec_current_ref": ACCEPTED_S1,
    "implementation_subject_ref": "producer/H1@sha",
    "evidence_subject_ref": "producer/H1@sha",
    "implements_accepted_delta": True,
    "revalidation_refs": [],
    "affected_producer_consumer_windows": [
        evidenced_window(
            "consumer/C0@v1",
            {"wire": "COMPATIBLE", "source": "COMPATIBLE", "behavior": "COMPATIBLE"},
        ),
        evidenced_window(
            "consumer/C1@v2",
            {"wire": "COMPATIBLE", "source": "COMPATIBLE", "behavior": "COMPATIBLE"},
        ),
    ],
}

P02_HISTORICAL_H0 = {
    "spec_baseline_ref": "spec/S1@baseline-sha",
    "proposed_delta_ref": ACCEPTED_S1,
    "acceptance_authority_ref": AUTHORIZED_AUTHORITY,
    "accepted_spec_current_ref": ACCEPTED_S1,
    "implementation_subject_ref": "producer/H0@sha",
    "implements_accepted_delta": False,
    "revalidation_refs": [],
    "affected_producer_consumer_windows": [evidenced_window("consumer/C0@v1")],
}

P03_NONMATERIAL = {"nonmaterial": True, "affected_producer_consumer_windows": []}

HISTORICAL_V1_RECORD = {
    "schema_version": 1,
    "record_id": "compat-2024-001",
    "contract": {"kind": "openapi", "identity": "svc.orchestrator.api"},
    "baseline": {"version_ref": "v1.0.0", "sha_or_digest": "b0" * 20},
    "candidate": {"version_ref": "v1.1.0", "sha_or_digest": "c0" * 20},
    "change_operations": ["add-field"],
    "dimensions": [
        {"name": "wire", "outcome": "COMPATIBLE", "evidence_refs": ["evidence/wire-run"]}
    ],
    "producer_refs": ["producer/H0"],
    "consumer_refs": ["consumer/C0"],
    "compatibility_window_ref": "support-line/v1",
}


class StandardStructureTests(unittest.TestCase):
    """Bounded-delta guards: regression slicing and shared vocabulary survive."""

    def test_canonical_headings_are_preserved_in_order(self) -> None:
        text = standard_text()
        positions = []
        for heading in CANONICAL_HEADINGS:
            with self.subTest(heading=heading):
                self.assertIn(heading, text)
            positions.append(text.index(heading))
        self.assertEqual(positions, sorted(positions))

    def test_forbidden_inference_matrix_is_unchanged(self) -> None:
        matrix = section("## 10. Required forbidden-inference matrix")
        for row in (
            "| wire-safe | source compatible |",
            "| schema/checker passes | behavior compatible |",
            "| new provider + new consumer pass | old/external consumer compatible |",
            "| dimension missing or `UNKNOWN` | compatible |",
            "| generated client/codegen succeeds | generated artifact is contract authority or proves compatibility |",
        ):
            with self.subTest(row=row):
                self.assertIn(row, matrix)

    def test_decision_states_stay_test_level_not_new_standard_states(self) -> None:
        # The standard states currentness conditions in prose; the named
        # decision vocabulary of this test must not be minted as new tokens.
        text = standard_text()
        for token in ("`RECONCILED`", "`STALE`", "`NONMATERIAL`"):
            with self.subTest(token=token):
                self.assertNotIn(token, text)

    def test_canonical_state_tokens_in_amended_clauses_stay_canonical(self) -> None:
        text = standard_text()
        gate_like = set(re.findall(r"`(PASS|FAIL|BLOCKED|NOT_RUN|NOT_APPLICABLE|UNKNOWN)`", text))
        self.assertTrue(gate_like)
        invented = set(
            re.findall(r"`(IMPLEMENTED|SHIPPED|CURRENT|RECONCILED|STALE|NONMATERIAL)`", text)
        )
        self.assertFalse(invented, invented)


class AcceptedSpecBindingClauseTests(unittest.TestCase):
    """SS3-S5 clauses binding spec identity/authority to shipped subjects."""

    def test_accepted_spec_identity_fields_are_bound_in_section_3(self) -> None:
        # Binding clause for the projection fields used by P01/N01/N07.
        body = section("## 3. Exact subject and baseline binding")
        self.assertIn("MUST additionally bind the accepted specification itself", body)
        for field in ("spec_baseline_ref", "proposed_delta_ref", "acceptance_authority_ref", "accepted_spec_current_ref"):
            with self.subTest(field=field):
                self.assertIn(f"`{field}`", body)
        self.assertIn("ADDED/MODIFIED/REMOVED", body)

    def test_acceptance_or_archival_never_substitutes_for_shipped_identity(self) -> None:
        # N01 textual basis: acceptance is a decision about intent.
        body = section("## 3. Exact subject and baseline binding")
        self.assertIn("Acceptance or archival of a specification delta is a recorded decision about intent", body)
        self.assertIn(
            "MUST NOT substitute for the exact baseline/candidate identity of the actually shipped contract artifacts",
            body,
        )

    def test_accepted_operations_do_not_imply_implementation(self) -> None:
        # S4/N01 textual basis: an accepted spec is not code.
        body = section("## 4. Change operation is not compatibility outcome")
        self.assertIn("An accepted `ADDED` operation does not imply that any producer ships the added surface", body)
        self.assertIn("an accepted `MODIFIED` operation does not imply that any producer implements the modified behavior", body)
        self.assertIn("an accepted `REMOVED` operation does not imply that the removal has shipped", body)
        self.assertIn("An accepted spec is not code", body)
        self.assertIn("acceptance is a change fact, never an implementation outcome", body)

    def test_reconciliation_dimensions_are_observed_on_the_current_subject(self) -> None:
        # N02 textual basis: evidence on a superseded subject proves nothing current.
        body = section("## 5. Compatibility is multi-dimensional and extensible")
        self.assertIn(
            "the required wire, source, and behavior dimensions MUST be observed on the current producer subject",
            body,
        )
        self.assertIn("not on a superseded subject", body)


class WindowCurrentnessClauseTests(unittest.TestCase):
    """SS6/SS8 clauses for supported windows, drift, and removal currentness."""

    def test_every_still_supported_affected_window_must_be_evidenced(self) -> None:
        # N04 textual basis.
        body = section("## 6. Producer, consumer, and window evidence")
        self.assertIn(
            "An accepted specification change that names affected producer/consumer windows MUST have every still-supported affected window evidenced for the required dimensions",
            body,
        )

    def test_drift_invalidates_only_the_drifted_material_scope(self) -> None:
        # N06 textual basis: stale-not-false, bounded revalidation.
        body = section("## 6. Producer, consumer, and window evidence")
        self.assertIn("A window tested once does not remain current by default", body)
        self.assertIn("drift makes prior evidence stale for exactly the drifted material scope", body)
        self.assertIn("MUST be revalidated before being relied on again", body)
        self.assertIn("Drift MUST NOT be generalized to unrelated windows", body)
        self.assertIn("preserved as history rather than rewritten", body)

    def test_removed_operation_requires_current_producer_and_all_windows(self) -> None:
        # N03 textual basis: C1 success cannot erase a C0 break.
        body = section("## 8. Deprecation and removal")
        self.assertIn(
            "An accepted REMOVED change ships only when the current producer implementation no longer provides the removed surface",
            body,
        )
        self.assertIn(
            "A new producer/new consumer success MUST NOT be recorded as current removal compatibility",
            body,
        )
        self.assertIn("that window remains `INCOMPATIBLE` until it is re-evidenced", body)


class MaterialityAndProjectionClauseTests(unittest.TestCase):
    """SS9/SS11/SS12 clauses: proportionality, proposed fields, fail-closed."""

    def test_nonmaterial_accepted_change_gets_proportionate_disposition(self) -> None:
        # P03 textual basis.
        body = section("## 9. Fast Path and materiality")
        self.assertIn(
            "An accepted specification change with no affected producer or consumer MAY receive an explicit proportionate nonmaterial disposition without creating a compatibility record",
            body,
        )

    def test_non_behavioral_green_never_manufactures_a_claim(self) -> None:
        # N05 textual basis.
        body = section("## 9. Fast Path and materiality")
        self.assertIn("Archive merge, codegen success, or checker-only GREEN is not materiality evidence", body)
        self.assertIn("MUST NOT manufacture an implementation or consumer claim", body)

    def test_seven_logical_projection_fields_are_proposed_only(self) -> None:
        # Task Pack S4/S5: fields stay prose-proposed; wiring is centrally owned.
        body = section("## 11. Machine-contract relation")
        for field in PROJECTION_REFS:
            with self.subTest(field=field):
                self.assertIn(f"`{field}`", body)
        self.assertIn("proposed logical fields only", body)
        self.assertIn("this standard does not add them to `schemas/compatibility-record-v1.schema.json`", body)
        self.assertIn("centrally designated wiring task", body)

    def test_v1_records_stay_readable_without_retroactive_fields(self) -> None:
        # N08 textual basis.
        body = section("## 11. Machine-contract relation")
        self.assertIn("Records that are valid under the v1 schema MUST remain readable by v1 readers", body)
        self.assertIn("no new mandatory field applies retroactively", body)

    def test_reconciliation_is_not_a_gate_validation_or_release_state(self) -> None:
        # P01 oracle: no Validation/Release PASS may be inferred.
        body = section("## 11. Machine-contract relation")
        self.assertIn(
            "A reconciliation disposition is compatibility-domain evidence vocabulary, "
            "not a Gate, Validation, or Release state",
            body,
        )
        self.assertIn("never converts compatibility into release authority", body)

    def test_fail_closed_routing_for_unknown_stale_and_untestable(self) -> None:
        # N07 + pack S6 textual basis.
        body = section("## 12. Failure handling")
        self.assertIn("stays `UNKNOWN`/`BLOCKED`, never implemented", body)
        self.assertIn("is stale, not false", body)
        self.assertIn("routes to revalidation for the affected scope", body)
        self.assertIn("remains explicitly `NOT_RUN` and routes to an exact-subject Validation owner", body)
        self.assertIn("Current assertions MUST remain distinguishable from historical reports", body)


class PositiveReconciliationDecisionTests(unittest.TestCase):
    """Fixture-driven positive oracles P01-P03 against the decision model."""

    def test_p01_authorized_added_spec_fully_implemented_and_windowed_reconciles(self) -> None:
        verdict = decide(P01_PROJECTION)
        self.assertEqual(verdict["decision"], "RECONCILED")
        self.assertIn("no Validation or Release PASS is implied", verdict["reasons"][0])
        # No promotion fields may appear on a compatibility-domain decision.
        self.assertNotIn("validation_pass", verdict)
        self.assertNotIn("release_pass", verdict)

    def test_p02_fresh_h1_reconciliation_allowed_while_h0_history_stays_blocked(self) -> None:
        historical = decide(P02_HISTORICAL_H0)
        self.assertEqual(historical["decision"], "BLOCKED")
        self.assertIn("acceptance is not implementation", historical["reasons"][0])
        current = decide(P01_PROJECTION)
        self.assertEqual(current["decision"], "RECONCILED")
        # The fresh reconciliation must not rewrite the historical verdict.
        self.assertEqual(decide(P02_HISTORICAL_H0)["decision"], "BLOCKED")

    def test_p03_nonmaterial_change_gets_proportionate_disposition_only(self) -> None:
        verdict = decide(P03_NONMATERIAL)
        self.assertEqual(verdict["decision"], "NONMATERIAL")
        self.assertIn("explicit proportionate nonmaterial disposition", verdict["reasons"][0])
        self.assertIn("no empty heavyweight record", verdict["reasons"][0])


class NegativeReconciliationDecisionTests(unittest.TestCase):
    """Fixture-driven fail-closed oracles N01-N07 against the decision model."""

    def test_n01_accepted_spec_without_producer_shipment_stays_blocked(self) -> None:
        projection = dict(P02_HISTORICAL_H0)
        verdict = decide(projection)
        self.assertEqual(verdict["decision"], "BLOCKED")
        self.assertIn("accepted spec current revision is not the shipped producer", verdict["reasons"][0])
        self.assertNotEqual(verdict["decision"], "RECONCILED")

    def test_n02_evidence_exercising_superseded_producer_is_rejected_as_current(self) -> None:
        projection = dict(P01_PROJECTION)
        projection["evidence_subject_ref"] = "producer/H0@sha"
        verdict = decide(projection)
        self.assertEqual(verdict["decision"], "STALE")
        self.assertIn("superseded subject", verdict["reasons"][0])
        self.assertIn("current implementation assertion rejected", verdict["reasons"][0])
        self.assertIn("revalidation required", verdict["reasons"][0])

    def test_n03_old_consumer_on_removed_operation_is_incompatible_despite_c1_pass(self) -> None:
        projection = dict(P01_PROJECTION)
        projection["affected_producer_consumer_windows"] = [
            evidenced_window(
                "consumer/C0@v1",
                {"wire": "COMPATIBLE", "source": "INCOMPATIBLE", "behavior": "INCOMPATIBLE"},
            ),
            evidenced_window(
                "consumer/C1@v2",
                {"wire": "COMPATIBLE", "source": "COMPATIBLE", "behavior": "COMPATIBLE"},
            ),
        ]
        verdict = decide(projection)
        self.assertEqual(verdict["decision"], "INCOMPATIBLE")
        self.assertTrue(any("consumer/C0@v1" in reason for reason in verdict["reasons"]))
        # The C1 PASS must not erase or flip the C0 verdict.
        self.assertNotEqual(verdict["decision"], "RECONCILED")

    def test_n04_untested_still_supported_old_consumer_window_stays_unknown(self) -> None:
        projection = dict(P01_PROJECTION)
        projection["affected_producer_consumer_windows"] = [
            evidenced_window("consumer/C0@v1"),
            evidenced_window(
                "consumer/C1@v2",
                {"wire": "COMPATIBLE", "source": "COMPATIBLE", "behavior": "COMPATIBLE"},
            ),
        ]
        verdict = decide(projection)
        self.assertEqual(verdict["decision"], "UNKNOWN")
        self.assertTrue(
            any("consumer/C0@v1 lacks required" in reason for reason in verdict["reasons"])
        )

    def test_n05_checker_only_green_does_not_implement_or_promote(self) -> None:
        projection = dict(P01_PROJECTION)
        projection["evidence_kind"] = "checker_only"
        projection["implements_accepted_delta"] = False
        verdict = decide(projection)
        self.assertEqual(verdict["decision"], "BLOCKED")
        self.assertIn("checker-only GREEN is not current implementation or behavior evidence", verdict["reasons"][0])
        self.assertIn("no Validation or Release promotion", verdict["reasons"][0])
        for other_kind in ("archive_merge", "codegen"):
            with self.subTest(evidence_kind=other_kind):
                self.assertEqual(
                    decide({**projection, "evidence_kind": other_kind})["decision"],
                    "BLOCKED",
                )

    def test_n06_material_drift_makes_prior_evidence_stale_pending_revalidation(self) -> None:
        base = dict(P01_PROJECTION)
        for scope in ("producer implementation subject", "accepted spec revision", "supported consumer window"):
            with self.subTest(drifted_scope=scope):
                projection = dict(base)
                projection["drifted_material_scope"] = [scope]
                verdict = decide(projection)
                self.assertEqual(verdict["decision"], "STALE")
                self.assertIn(f"prior evidence STALE for drifted {scope}", verdict["reasons"][0])
                self.assertIn("revalidation required", verdict["reasons"][0])

    def test_n07_missing_projection_evidence_is_unknown_not_inferred(self) -> None:
        base = dict(P01_PROJECTION)
        for ref in PROJECTION_REFS:
            with self.subTest(missing_field=ref):
                projection = dict(base)
                projection[ref] = None
                verdict = decide(projection)
                self.assertEqual(verdict["decision"], "UNKNOWN")
                self.assertIn(f"missing required projection field: {ref}", verdict["reasons"])
        windowless = dict(base)
        windowless["affected_producer_consumer_windows"] = []
        verdict = decide(windowless)
        self.assertEqual(verdict["decision"], "UNKNOWN")
        self.assertIn("no evidenced affected producer/consumer window", verdict["reasons"])

    def test_untestable_external_consumer_routes_not_run_to_validation_owner(self) -> None:
        projection = dict(P01_PROJECTION)
        projection["affected_producer_consumer_windows"] = [
            {
                "consumer_ref": "external/partner-consumer",
                "required_dimensions": REQUIRED_DIMENSIONS,
                "external_untestable": True,
            }
        ]
        verdict = decide(projection)
        self.assertEqual(verdict["decision"], "NOT_RUN")
        self.assertIn("external/partner-consumer", verdict["reasons"][0])
        self.assertIn("routed to an exact-subject Validation owner", verdict["reasons"][0])


class HistoricalV1ReaderCompatTests(unittest.TestCase):
    """N08: unmodified historical v1 records stay valid; no retroactive fields."""

    def test_n08_historical_v1_record_is_accepted_without_new_fields(self) -> None:
        self.assertTrue(v1_reader_accepts(HISTORICAL_V1_RECORD))
        for field in PROJECTION_REFS:
            with self.subTest(field=field):
                self.assertNotIn(field, HISTORICAL_V1_RECORD)

    def test_v1_schema_still_rejects_unknown_fields_and_is_not_extended(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(set(schema["required"]), V1_REQUIRED)
        raw = SCHEMA.read_text(encoding="utf-8")
        for field in PROJECTION_REFS:
            with self.subTest(field=field):
                self.assertNotIn(field, raw)

    def test_broken_v1_records_are_still_rejected_by_the_v1_reader(self) -> None:
        mutated = dict(HISTORICAL_V1_RECORD)
        mutated["spec_baseline_ref"] = "spec/S1@baseline-sha"
        self.assertFalse(v1_reader_accepts(mutated))
        bad_outcome = copy.deepcopy(HISTORICAL_V1_RECORD)
        bad_outcome["dimensions"][0]["outcome"] = "PASS"
        self.assertFalse(v1_reader_accepts(bad_outcome))


class DecisionModelSideEffectTests(unittest.TestCase):
    """Pack S3: decisions must not mutate projections or historical records."""

    def test_decide_never_mutates_its_input_projection(self) -> None:
        base = dict(P01_PROJECTION)
        variants = [base, P02_HISTORICAL_H0, P03_NONMATERIAL]
        for projection in variants:
            with self.subTest(projection=projection.get("implementation_subject_ref", "nonmaterial")):
                snapshot = copy.deepcopy(projection)
                decide(projection)
                self.assertEqual(projection, snapshot)

    def test_v1_reader_does_not_mutate_the_historical_record(self) -> None:
        snapshot = copy.deepcopy(HISTORICAL_V1_RECORD)
        self.assertTrue(v1_reader_accepts(HISTORICAL_V1_RECORD))
        self.assertEqual(HISTORICAL_V1_RECORD, snapshot)


if __name__ == "__main__":
    import sys

    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
