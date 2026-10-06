"""V410-T04B focused regression — Review finding / aggregation / currentness convergence.

Positive/negative contract for exact-subject Review currentness (§9.1),
machine-reconstructible material finding records with the T04A root-defect-class
binding (§9.2) and deterministic multi-review aggregation (§9.3) of
`standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md`, per L3 Wave D
(`docs/implementation/4.10.0/L3_WAVE_D_R1.md` § V410-T04B), Task Pack R1 and the
R3 bounded repair (Fresh Independent Review R1 P1-1/P1-2).

R3 additions: a current material `REVIEW_RESULT` without the structured
`findings.records` projection (stable identity + severity + root-defect class +
evidence) fails closed instead of satisfying the aggregate, and independent
finding IDs converge only through the existing finding-family duplicate
relation (`duplicate_of`), never by guessing from root-class similarity, order
or count; ambiguous/conflicting equivalence fails closed.

Consumes the integrated T04A root-defect-class authority
(`standards/DEVELOPMENT_WORKFLOW.md` §4) and the existing Review
finding/aggregation family (`schemas/review-finding-v1.schema.json`,
`schemas/review-aggregation-v1.schema.json`, `scripts/v40_rules.py`,
`scripts/v40_semantics.py`); redefines nothing and creates no second Review
lifecycle, event family, state dimension or registry. `reduce_current_aggregate`
below is the test oracle for the documented §9.3 reduction, not a runtime
artifact. Purely local; no network, no runtime execution.
"""

from __future__ import annotations

import itertools
import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_protocol_schemas import assert_supported_schema, validate_subset  # noqa: E402
from v40_rules import SEVERITY_RANK  # noqa: E402
from v40_semantics import validate_review_aggregation  # noqa: E402

PROTOCOL = "standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md"
EVENT_V2 = "schemas/agent-event-v2.schema.json"
FINDING_V1 = "schemas/review-finding-v1.schema.json"
AGGREGATION_V1 = "schemas/review-aggregation-v1.schema.json"
WORKFLOW = "standards/DEVELOPMENT_WORKFLOW.md"
TEMPLATE = "templates/agent-event-comment.md"
STATE_DIMENSIONS = "registries/state-dimensions-v1.json"

CANONICAL_WORKFLOW_STATES = {
    "planned",
    "ready",
    "claimed",
    "implementing",
    "review-ready",
    "reviewing",
    "changes-requested",
    "validation-needed",
    "merge-ready",
    "blocked",
    "done",
}

# T04A root-defect classes are owned by DEVELOPMENT_WORKFLOW.md §4; the machine
# ids below are consumed as that owner's projection. Any drift on either side
# (class list, ids or 1:1 correspondence) must fail this suite.
EXPECTED_ROOT_CLASS_PROJECTION = (
    ("PRODUCT_SEMANTICS_AUTHORITY_CONTRADICTION", "product semantics / authority contradiction"),
    ("ARCHITECTURE_PUBLIC_CONTRACT", "architecture / public contract"),
    ("IMPLEMENTATION_DEFECT", "implementation defect"),
    ("TEST_FIXTURE_EVIDENCE_DEFECT", "test / fixture / evidence defect"),
    ("ENVIRONMENT_TOOLCHAIN_EXTERNAL_BOUNDARY", "environment / toolchain / external boundary"),
    ("EXECUTION_ATTRIBUTION_DEFECT", "execution / attribution defect"),
    ("GATE_APPLICABILITY_AUTHORITY_AMBIGUITY", "gate applicability 或 authority ambiguity"),
)

SUBJECT_A = "a" * 40
SUBJECT_B = "b" * 40

SEVERITIES = {"P0", "P1", "P2", "P3"}


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def load_schema(rel: str) -> dict:
    return json.loads(read(rel))


def protocol_section_9() -> str:
    text = read(PROTOCOL)
    start = text.index("## 9. Review event invariants")
    end = text.index("## 10. Builder / Reviewer / Validator routing")
    return text[start:end]


def protocol_subsection(heading: str) -> str:
    section = protocol_section_9()
    start = section.index(heading)
    rest = section[start + len(heading) :]
    next_heading = rest.find("\n### ")
    return rest if next_heading == -1 else rest[:next_heading]


def protocol_block_after(heading: str, *, fence: str = "```text") -> str:
    subsection = protocol_subsection(heading)
    return subsection[
        subsection.index(fence) + len(fence) : subsection.index("```", subsection.index(fence) + 1)
    ]


def workflow_root_class_block() -> str:
    workflow = read(WORKFLOW)
    start = workflow.index("### Repair routing：root defect class")
    end = workflow.index("### Non-converging repair")
    section = workflow[start:end]
    return section[
        section.index("```text") + len("```text") : section.index("```", section.index("```text") + 1)
    ]


def normalize_lines(block: str) -> list[str]:
    return [" ".join(line.split()) for line in block.strip().splitlines() if line.strip()]


def parse_protocol_projection(block: str) -> list[tuple[str, str]]:
    rows = []
    for line in block.strip().splitlines():
        if not line.strip():
            continue
        machine_id, prose = re.split(r"\s{2,}", line.strip(), maxsplit=1)
        rows.append((machine_id, prose))
    return rows


def workflow_root_classes() -> list[str]:
    """The owner's class list, with its trailing cross-reference annotation removed."""
    return [
        re.sub(r"（[^）]*）$", "", line).strip() for line in normalize_lines(workflow_root_class_block())
    ]


def findings_schema() -> dict:
    return load_schema(EVENT_V2)["properties"]["findings"]


def record_schema() -> dict:
    return findings_schema()["properties"]["records"]["items"]


def template_review_example_block() -> str:
    template = read(TEMPLATE)
    marker = "## REVIEW_RESULT example"
    section = template[template.index(marker) + len(marker) :]
    start = section.index("```yaml") + len("```yaml")
    return section[start : section.index("```", start)]


def parse_example_buckets_and_records(block: str) -> tuple[dict[str, int], list[str]]:
    """Minimal reader for the canonical writer fixture: buckets + record severities."""
    buckets: dict[str, int] = {}
    severities: list[str] = []
    for raw_line in block.splitlines():
        line = raw_line.strip()
        bucket = re.fullmatch(r"p([0-3]):\s*(\d+)", line)
        if bucket:
            buckets[f"p{bucket.group(1)}"] = int(bucket.group(2))
        severity = re.fullmatch(r"severity:\s*(P[0-3])", line)
        if severity:
            severities.append(severity.group(1))
    return buckets, severities


def review_result_event(findings: object, *, sha: str = SUBJECT_A, status: str = "FAIL") -> dict:
    return {
        "schema": "ai-dev/event-v2",
        "event": "REVIEW_RESULT",
        "actor_role": "reviewer",
        "operator_kind": "chatgpt-web",
        "operator_id": "chatgpt-web:reviewer-r1",
        "session_ref": "review-session-1",
        "transport_actor": "github:kaicreator-mm",
        "task": "#857",
        "pr": "#888",
        "sha": sha,
        "review_policy": "required",
        "status": status,
        "findings": findings,
        "next_state": "changes-requested",
    }


def record(
    finding_id: str,
    severity: str = "P1",
    root_class: str = "IMPLEMENTATION_DEFECT",
    duplicate_of: str | None = None,
) -> dict:
    entry = {
        "finding_id": finding_id,
        "severity": severity,
        "root_defect_class": root_class,
        "evidence_refs": ["#857:comment-1"],
    }
    if duplicate_of is not None:
        entry["duplicate_of"] = duplicate_of
    return entry


def fact(
    event_ref: str,
    *,
    sha: str = SUBJECT_A,
    status: str = "FAIL",
    operator_id: str = "chatgpt-web:reviewer-r1",
    records: tuple[dict, ...] = (),
    buckets: dict | None = None,
) -> dict:
    assert isinstance(records, tuple), "records fixtures must be tuples of records"
    return {
        "event_ref": event_ref,
        "sha": sha,
        "status": status,
        "operator_id": operator_id,
        "records": records,
        "buckets": buckets,
    }


def disposition(
    event_ref: str,
    finding_id: str,
    duplicate_of: str,
    *,
    sha: str = SUBJECT_A,
) -> dict:
    """Durable `review-finding-v1` DUPLICATE disposition fact (same-family shape)."""
    return {
        "event_ref": event_ref,
        "sha": sha,
        "finding_id": finding_id,
        "duplicate_of": duplicate_of,
        "status": "DUPLICATE",
    }


ROOT_DEFECT_CLASSES = frozenset(machine_id for machine_id, _ in EXPECTED_ROOT_CLASS_PROJECTION)


def _record_well_formed(entry: object) -> bool:
    """§9.2: identity + severity + root-defect class + evidence must all be present."""
    if not isinstance(entry, dict):
        return False
    if not isinstance(entry.get("finding_id"), str) or not entry["finding_id"]:
        return False
    if entry.get("severity") not in SEVERITIES:
        return False
    if entry.get("root_defect_class") not in ROOT_DEFECT_CLASSES:
        return False
    evidence = entry.get("evidence_refs")
    if not isinstance(evidence, list) or not evidence:
        return False
    if not all(isinstance(ref, str) and ref for ref in evidence):
        return False
    duplicate_of = entry.get("duplicate_of")
    if duplicate_of is not None and (not isinstance(duplicate_of, str) or not duplicate_of):
        return False
    return True


def reduce_current_aggregate(facts: list[dict], live_subject: str, dispositions: tuple[dict, ...] = ()) -> dict:
    """Reference reduction of GITHUB_AGENT_INTERACTION_PROTOCOL.md §9.1–§9.3.

    Deterministic test oracle: exact-subject currentness, the §9.2 writer/
    conformance gate for current material findings (well-formed records and
    exact bucket↔record reconstruction), identity / explicit `duplicate_of`
    convergence — at emission or via a later durable same-subject
    `review-finding-v1` DUPLICATE disposition — with retained provenance,
    fail-closed conflicts and blocker-dominant judgment (the existing
    `finding-union-blocker-dominance` aggregation policy). Never resolves
    authority from reviewer/model count, ordering or similarity.
    """
    current = [item for item in facts if item["sha"] == live_subject]
    result: dict = {
        "current_subject": live_subject,
        "historical_facts": tuple(sorted(item["event_ref"] for item in facts if item["sha"] != live_subject)),
        "historical_dispositions": tuple(
            sorted(item["event_ref"] for item in dispositions if item["sha"] != live_subject)
        ),
        "state": "NO_CURRENT_REVIEW",
        "judgment": None,
        "findings": (),
        "conflicts": (),
        "unresolved_blocker_refs": (),
    }

    def fail_closed(state: str, conflicts: tuple[str, ...]) -> dict:
        result.update(state=state, conflicts=tuple(sorted(conflicts)))
        return result

    if not current:
        return result

    verdicts = sorted({item["status"] for item in current})
    if len(verdicts) > 1:
        result.update(state="FAIL_CLOSED_VERDICT_CONFLICT", conflicts=tuple(verdicts))
        return result

    # §9.2 writer/admission/conformance gate: a current REVIEW_RESULT that
    # reports material findings (non-PASS verdict, any structured record, or a
    # positive severity bucket) must carry a well-formed records projection
    # whose per-severity counts exactly reconstruct the reported buckets; an
    # opaque payload is not machine-reconstructible and fails closed instead of
    # becoming a judgment.
    for item in current:
        buckets = item.get("buckets")
        reports_material = item["status"] != "PASS" or bool(item["records"]) or bool(buckets and any(buckets.values()))
        if not reports_material:
            continue
        if not item["records"] or any(not _record_well_formed(entry) for entry in item["records"]):
            return fail_closed("FAIL_CLOSED_NON_RECONSTRUCTIBLE_FINDING", (item["event_ref"],))
        if buckets is not None:
            for index, severity in enumerate(("P0", "P1", "P2", "P3")):
                claimed = buckets.get(f"p{index}", 0)
                reconstructed = sum(1 for entry in item["records"] if entry["severity"] == severity)
                if claimed != reconstructed:
                    return fail_closed("FAIL_CLOSED_NON_RECONSTRUCTIBLE_FINDING", (item["event_ref"],))

    grouped: dict[str, list[tuple[str, dict]]] = {}
    for item in current:
        origin = f"{item['operator_id']}:{item['event_ref']}"
        for entry in item["records"]:
            grouped.setdefault(entry["finding_id"], []).append((origin, entry))

    # §9.2 duplicate equivalence: explicit durable `duplicate_of` links only.
    linked_somewhere = {fid for fid in grouped if any(e.get("duplicate_of") for _, e in grouped[fid])}
    duplicates: dict[str, list[tuple[str, str, dict]]] = {}
    for fid in sorted(grouped):
        for origin, entry in grouped[fid]:
            if entry.get("duplicate_of"):
                duplicates.setdefault(entry["duplicate_of"], []).append((fid, origin, entry))
    for fid in sorted(grouped):
        has_linked = any(e.get("duplicate_of") for _, e in grouped[fid])
        has_unlinked = any(not e.get("duplicate_of") for _, e in grouped[fid])
        if has_linked and has_unlinked:
            return fail_closed("FAIL_CLOSED_AMBIGUOUS_EQUIVALENCE", (fid,))

    # §9.2 post-hoc reconciliation: durable same-subject `review-finding-v1`
    # DUPLICATE dispositions consumed as a separate fact stream. One finding id
    # may carry exactly one disposition target; a disposition contradicting an
    # in-emission `duplicate_of` link is competing, not latest-wins.
    current_dispositions = sorted(
        (d for d in dispositions if d["sha"] == live_subject),
        key=lambda d: (d["finding_id"], d["event_ref"]),
    )
    disposition_link: dict[str, str] = {}
    disposition_refs: dict[str, list[str]] = {}
    for item in current_dispositions:
        fid, target = item["finding_id"], item["duplicate_of"]
        if fid == target:
            return fail_closed("FAIL_CLOSED_AMBIGUOUS_EQUIVALENCE", (fid,))
        if fid in disposition_link and disposition_link[fid] != target:
            return fail_closed("FAIL_CLOSED_AMBIGUOUS_EQUIVALENCE", (fid,))
        emission_target = next(
            (entry["duplicate_of"] for _, entry in grouped.get(fid, ()) if entry.get("duplicate_of")),
            None,
        )
        if emission_target is not None and emission_target != target:
            return fail_closed("FAIL_CLOSED_AMBIGUOUS_EQUIVALENCE", (fid,))
        disposition_link[fid] = target
        disposition_refs.setdefault(fid, []).append(item["event_ref"])

    # Union-graph validation over emission + disposition links: every link must
    # point at a known canonical finding of the same subject — no
    # reconciliation of unknown ids, no self-links, no chains, no cycles.
    combined: dict[str, str] = {}
    for entries in grouped.values():
        for _, entry in entries:
            if entry.get("duplicate_of"):
                combined[entry["finding_id"]] = entry["duplicate_of"]
    for fid, target in disposition_link.items():
        combined[fid] = target
    for fid, target in sorted(combined.items()):
        if fid not in grouped or target == fid or target not in grouped or target in combined:
            return fail_closed("FAIL_CLOSED_AMBIGUOUS_EQUIVALENCE", (fid, target))

    target_severities_by_id = {fid: {entry["severity"] for _, entry in grouped[fid]} for fid in grouped}
    target_classes_by_id = {fid: {entry["root_defect_class"] for _, entry in grouped[fid]} for fid in grouped}
    for target in sorted(duplicates):
        for fid, _, entry in duplicates[target]:
            if (
                entry["severity"] not in target_severities_by_id[target]
                or entry["root_defect_class"] not in target_classes_by_id[target]
            ):
                return fail_closed("FAIL_CLOSED_FINDING_CONFLICT", (fid, target))

    # Merge: emission-linked ids first, then post-hoc disposition-reconciled
    # ids; agreeing emission+disposition links are consumed once (provenance
    # refs still recorded). Reconciliation never rewrites original facts.
    merged = {
        fid: list(entries)
        for fid, entries in grouped.items()
        if fid not in linked_somewhere and fid not in disposition_link
    }
    duplicate_ids_by_target: dict[str, tuple[str, ...]] = {}
    disposition_refs_by_target: dict[str, tuple[str, ...]] = {}
    for target in sorted(duplicates):
        duplicate_ids_by_target[target] = tuple(sorted(fid for fid, _, _ in duplicates[target]))
        merged.setdefault(target, list(grouped[target]))
        merged[target].extend((origin, entry) for _, origin, entry in duplicates[target])
    for fid in sorted(disposition_link):
        target = disposition_link[fid]
        if fid not in linked_somewhere:
            merged[target].extend(grouped[fid])
        duplicate_ids_by_target[target] = tuple(
            sorted(set(duplicate_ids_by_target.get(target, ())) | {fid})
        )
        disposition_refs_by_target[target] = tuple(
            sorted(set(disposition_refs_by_target.get(target, ())) | set(disposition_refs.get(fid, ())))
        )

    logical: list[dict] = []
    conflicts: list[str] = []
    for finding_id in sorted(merged):
        group = merged[finding_id]
        severities = sorted({entry["severity"] for _, entry in group})
        root_classes = sorted({entry["root_defect_class"] for _, entry in group})
        if len(severities) > 1 or len(root_classes) > 1:
            conflicts.append(finding_id)
            continue
        logical.append(
            {
                "finding_id": finding_id,
                "severity": severities[0],
                "root_defect_class": root_classes[0],
                "blocking": severities[0] in {"P0", "P1"},
                "provenance": tuple(sorted({origin for origin, _ in group})),
                "evidence_refs": tuple(
                    sorted({ref for _, entry in group for ref in entry["evidence_refs"]})
                ),
                "duplicate_ids": duplicate_ids_by_target.get(finding_id, ()),
                "disposition_refs": disposition_refs_by_target.get(finding_id, ()),
            }
        )
    if conflicts:
        result.update(state="FAIL_CLOSED_FINDING_CONFLICT", conflicts=tuple(sorted(conflicts)))
        return result

    unresolved = tuple(entry["finding_id"] for entry in logical if entry["blocking"])
    judgment = "CHANGES_REQUESTED" if unresolved else {"PASS": "PASS", "FAIL": "CHANGES_REQUESTED"}[verdicts[0]]
    result.update(
        state="CURRENT",
        judgment=judgment,
        findings=tuple(logical),
        unresolved_blocker_refs=unresolved,
    )
    return result


class ReviewCurrentnessTests(unittest.TestCase):
    """L3 positive case 2 / negative case 1: exact-subject currentness."""

    def test_review_subject_is_the_event_level_exact_sha(self) -> None:
        subsection = protocol_subsection("### 9.1 Review subject and exact-subject currentness")
        self.assertIn("bound to exactly one subject: the event-level exact `sha`", subsection)

    def test_current_and_stale_facts_are_defined_by_subject_equality(self) -> None:
        block = protocol_block_after("### 9.1 Review subject and exact-subject currentness")
        self.assertIn("current facts = accepted Review facts whose exact subject == the live current", block)
        self.assertIn("stale facts   = Review facts bound to any other subject", block)

    def test_stale_facts_are_historical_only_and_never_transferred(self) -> None:
        subsection = protocol_subsection("### 9.1 Review subject and exact-subject currentness")
        self.assertIn("Only current facts may satisfy the Review condition", subsection)
        self.assertIn("never counted, re-bound or transferred as current", subsection)
        self.assertIn("A previous subject's `PASS` never satisfies a successor subject", subsection)

    def test_successor_review_is_legal_only_under_existing_owner_rules(self) -> None:
        subsection = protocol_subsection("### 9.1 Review subject and exact-subject currentness")
        self.assertIn("Successor/delta review is legal only under the existing owner rules", subsection)
        self.assertIn("full re-review", subsection)
        self.assertIn("binds to the new exact subject", subsection)

    def test_ambiguous_subject_fails_closed(self) -> None:
        subsection = protocol_subsection("### 9.1 Review subject and exact-subject currentness")
        self.assertIn("currentness fails closed", subsection)
        self.assertIn("stays unsatisfied rather than being guessed", subsection)


class FindingRecordContractTests(unittest.TestCase):
    """L3 positive case 1 / negative case 3: machine-reconstructible findings."""

    def test_protocol_requires_reconstructible_new_material_findings(self) -> None:
        subsection = protocol_subsection("### 9.2 Machine finding records")
        # R3 P1-1: the new-writer contract is normative MUST, not prose SHOULD.
        self.assertIn(
            "Newly emitted `REVIEW_RESULT` events that report material findings MUST be "
            "machine-reconstructible",
            subsection,
        )
        self.assertIn("every material finding MUST be projected into `findings.records`", subsection)
        self.assertIn("REVIEW_RESULT.findings", subsection)
        self.assertIn("never satisfy this new-writer contract", subsection)
        self.assertIn("never promoted into a current judgment", subsection)
        block = protocol_block_after("### 9.2 Machine finding records", fence="```yaml")
        for token in (
            "records:",
            "finding_id:",
            "severity:",
            "root_defect_class:",
            "evidence_refs:",
            "duplicate_of:",
        ):
            with self.subTest(token=token):
                self.assertIn(token, block)

    def test_schema_accepts_a_conforming_review_result_event(self) -> None:
        schema = load_schema(EVENT_V2)
        assert_supported_schema(schema)
        event = review_result_event(
            {
                "p1": 1,
                "records": [
                    record("RV-1", "P1"),
                    record("RV-2", "P2", "TEST_FIXTURE_EVIDENCE_DEFECT"),
                    record("RV-3", "P1", "IMPLEMENTATION_DEFECT", duplicate_of="RV-1"),
                ],
            }
        )
        self.assertEqual(validate_subset(event, schema), [])

    def test_missing_identity_severity_root_class_or_evidence_is_rejected(self) -> None:
        items = record_schema()
        complete = record("RV-1")
        for field_name in ("finding_id", "severity", "root_defect_class", "evidence_refs"):
            with self.subTest(missing=field_name):
                incomplete = {key: value for key, value in complete.items() if key != field_name}
                self.assertTrue(validate_subset(incomplete, items))
        for override in (
            {"finding_id": ""},
            {"evidence_refs": []},
            {"evidence_refs": [""]},
            {"duplicate_of": ""},
        ):
            with self.subTest(invalid=override):
                self.assertTrue(validate_subset({**complete, **override}, items))

    def test_empty_records_array_is_rejected(self) -> None:
        self.assertTrue(validate_subset({"records": []}, findings_schema()))

    def test_historical_bucket_findings_remain_valid_history(self) -> None:
        self.assertEqual(validate_subset({"p0": 0, "p1": 1, "p2": 2, "p3": 0}, findings_schema()), [])
        schema = load_schema(EVENT_V2)
        legacy = review_result_event({"p0": 0, "p1": 1, "p2": 2, "p3": 0})
        self.assertEqual(validate_subset(legacy, schema), [])

    def test_record_vocabulary_reuses_the_existing_finding_family(self) -> None:
        family = load_schema(FINDING_V1)
        items = record_schema()
        record_properties = set(items["properties"])
        family_properties = set(family["properties"])
        # Only `root_defect_class` is additive; every other member — including
        # the `duplicate_of` equivalence link — already exists in the canonical
        # Review finding contract.
        self.assertEqual(record_properties - family_properties, {"root_defect_class"})
        self.assertEqual(
            items["properties"]["severity"]["enum"], family["properties"]["severity"]["enum"]
        )
        self.assertEqual(sorted(items["properties"]["severity"]["enum"]), sorted(SEVERITY_RANK))
        self.assertEqual(
            items["properties"]["evidence_refs"]["items"], family["properties"]["evidence_refs"]["items"]
        )
        self.assertEqual(
            items["properties"]["duplicate_of"], family["properties"]["duplicate_of"]
        )

    def test_template_states_the_new_writer_contract(self) -> None:
        template = read(TEMPLATE)
        self.assertIn("REQUIRED for new material findings", template)
        self.assertIn("never satisfy the new-writer contract", template)
        self.assertIn("duplicate_of", template)
        self.assertIn("MUST equal the per-severity record counts", template)
        self.assertIn("review-finding-v1` durable `DUPLICATE` disposition", template)

    def test_template_example_is_bucket_record_consistent(self) -> None:
        # R4 P1-1: the canonical writer fixture must satisfy its own MUST —
        # bucket counts exactly reconstruct from the example's records.
        block = template_review_example_block()
        buckets, severities = parse_example_buckets_and_records(block)
        self.assertTrue(buckets, "fixture must declare severity buckets")
        self.assertTrue(severities, "fixture must declare records")
        reconstructed = {f"p{index}": severities.count(f"P{index}") for index in range(4)}
        self.assertEqual(buckets, reconstructed)


class RootDefectClassBindingTests(unittest.TestCase):
    """L3 positive case 4: root-defect classification binds to T04A authority."""

    def test_protocol_projection_matches_the_workflow_owner_classes(self) -> None:
        projection = protocol_block_after("### 9.2 Machine finding records")
        self.assertEqual(
            parse_protocol_projection(projection),
            list(EXPECTED_ROOT_CLASS_PROJECTION),
        )

    def test_workflow_owner_still_lists_the_same_classes(self) -> None:
        self.assertEqual(
            workflow_root_classes(), [prose for _, prose in EXPECTED_ROOT_CLASS_PROJECTION]
        )
        # The owner's own cross-reference annotation is preserved, not projected.
        self.assertIn(
            "gate applicability 或 authority ambiguity（→ 上一节）",
            normalize_lines(workflow_root_class_block()),
        )

    def test_schema_enum_matches_the_projection_exactly(self) -> None:
        items = record_schema()
        self.assertEqual(
            items["properties"]["root_defect_class"]["enum"],
            [machine_id for machine_id, _ in EXPECTED_ROOT_CLASS_PROJECTION],
        )

    def test_projection_adds_no_class_and_owns_no_repair_routing(self) -> None:
        subsection = protocol_subsection("### 9.2 Machine finding records")
        self.assertIn("It adds, removes and redefines no class, and it owns no repair routing", subsection)
        self.assertIn("Routing a finding's root defect class to repair/escalation stays owned by", subsection)
        self.assertIn("`DEVELOPMENT_WORKFLOW.md` §4", subsection)


class DeterministicAggregationTests(unittest.TestCase):
    """L3 positive cases 2–3 / negative cases 1–4: deterministic currentness and aggregation."""

    def test_only_current_subject_facts_enter_the_aggregate(self) -> None:
        facts = [
            fact("e-stale", sha=SUBJECT_B, status="PASS", records=(record("RV-9"),)),
            fact("e-current", sha=SUBJECT_A, records=(record("RV-1"),)),
        ]
        result = reduce_current_aggregate(facts, SUBJECT_A)
        self.assertEqual(result["state"], "CURRENT")
        self.assertEqual(result["historical_facts"], ("e-stale",))
        self.assertEqual([entry["finding_id"] for entry in result["findings"]], ["RV-1"])

    def test_stale_review_pass_never_satisfies_a_successor_subject(self) -> None:
        facts = [fact("e-old", sha=SUBJECT_B, status="PASS", records=())]
        result = reduce_current_aggregate(facts, SUBJECT_A)
        self.assertEqual(result["state"], "NO_CURRENT_REVIEW")
        self.assertIsNone(result["judgment"])
        self.assertEqual(result["historical_facts"], ("e-old",))

    def test_current_material_finding_without_structured_records_fails_closed(self) -> None:
        # R3 P1-1: a bucket-only / opaque current payload can no longer satisfy
        # the aggregate path.
        result = reduce_current_aggregate([fact("e-opaque", status="FAIL", records=())], SUBJECT_A)
        self.assertEqual(result["state"], "FAIL_CLOSED_NON_RECONSTRUCTIBLE_FINDING")
        self.assertIsNone(result["judgment"])
        self.assertEqual(result["conflicts"], ("e-opaque",))

    def test_current_record_missing_identity_severity_class_or_evidence_fails_closed(self) -> None:
        malformed_variants = (
            {"finding_id": ""},
            {},
            {**record("RV-1"), "severity": "P9"},
            {**record("RV-1"), "root_defect_class": "INVENTED_CLASS"},
            {**record("RV-1"), "evidence_refs": []},
        )
        for variant in malformed_variants:
            with self.subTest(variant=variant):
                result = reduce_current_aggregate(
                    [fact("e-r1", records=(variant,))], SUBJECT_A
                )
                self.assertEqual(result["state"], "FAIL_CLOSED_NON_RECONSTRUCTIBLE_FINDING")
                self.assertIsNone(result["judgment"])

    def test_historical_bucket_only_review_is_never_promoted_to_a_current_judgment(self) -> None:
        facts = [
            fact("e-old-bucket", sha=SUBJECT_B, status="FAIL", records=()),
            fact("e-current-pass", status="PASS", records=()),
        ]
        result = reduce_current_aggregate(facts, SUBJECT_A)
        self.assertEqual(result["state"], "CURRENT")
        self.assertEqual(result["judgment"], "PASS")
        self.assertEqual(result["historical_facts"], ("e-old-bucket",))
        self.assertEqual(result["findings"], ())

    def test_same_identity_facts_converge_with_provenance_preserved(self) -> None:
        # Same-`finding_id` convergence path (coordinated identity).
        facts = [
            fact("e-r1", records=(record("RV-1"),), operator_id="chatgpt-web:reviewer-r1"),
            fact("e-r2", records=(record("RV-1"),), operator_id="claude-code:reviewer-r2"),
        ]
        result = reduce_current_aggregate(facts, SUBJECT_A)
        self.assertEqual(result["state"], "CURRENT")
        self.assertEqual(len(result["findings"]), 1)
        self.assertEqual(
            result["findings"][0]["provenance"],
            ("chatgpt-web:reviewer-r1:e-r1", "claude-code:reviewer-r2:e-r2"),
        )
        self.assertEqual(result["findings"][0]["duplicate_ids"], ())

    def test_independent_duplicate_ids_converge_only_through_explicit_duplicate_linkage(self) -> None:
        # R3 P1-2: independent reviewers need not coordinate IDs; the same
        # logical defect under a different ID converges only via the durable
        # `duplicate_of` relation, preserving both reviewers' provenance.
        facts = [
            fact("e-r1", records=(record("RV-1"),), operator_id="chatgpt-web:reviewer-r1"),
            fact(
                "e-r2",
                records=(record("RV-7", duplicate_of="RV-1"),),
                operator_id="claude-code:reviewer-r2",
            ),
        ]
        result = reduce_current_aggregate(facts, SUBJECT_A)
        self.assertEqual(result["state"], "CURRENT")
        self.assertEqual(len(result["findings"]), 1)
        converged = result["findings"][0]
        self.assertEqual(converged["finding_id"], "RV-1")
        self.assertEqual(converged["duplicate_ids"], ("RV-7",))
        self.assertEqual(
            converged["provenance"],
            ("chatgpt-web:reviewer-r1:e-r1", "claude-code:reviewer-r2:e-r2"),
        )
        self.assertEqual(result["unresolved_blocker_refs"], ("RV-1",))

    def test_independent_ids_without_linkage_remain_distinct_findings(self) -> None:
        # Root-class equality alone is classification evidence, never identity.
        facts = [
            fact("e-r1", records=(record("RV-1", "P1", "IMPLEMENTATION_DEFECT"),)),
            fact(
                "e-r2",
                records=(record("RV-7", "P1", "IMPLEMENTATION_DEFECT"),),
                operator_id="claude-code:reviewer-r2",
            ),
        ]
        result = reduce_current_aggregate(facts, SUBJECT_A)
        self.assertEqual(result["state"], "CURRENT")
        self.assertEqual(
            [entry["finding_id"] for entry in result["findings"]], ["RV-1", "RV-7"]
        )
        self.assertEqual(result["unresolved_blocker_refs"], ("RV-1", "RV-7"))

    def test_duplicate_link_to_unknown_target_fails_closed(self) -> None:
        facts = [
            fact("e-r1", records=(record("RV-1"),)),
            fact(
                "e-r2",
                records=(record("RV-7", duplicate_of="RV-404"),),
                operator_id="claude-code:reviewer-r2",
            ),
        ]
        result = reduce_current_aggregate(facts, SUBJECT_A)
        self.assertEqual(result["state"], "FAIL_CLOSED_AMBIGUOUS_EQUIVALENCE")
        self.assertIsNone(result["judgment"])

    def test_duplicate_chain_or_cycle_fails_closed(self) -> None:
        chain = [
            fact("e-r1", records=(record("RV-1"),)),
            fact(
                "e-r2",
                records=(record("RV-7", duplicate_of="RV-1"),),
                operator_id="claude-code:reviewer-r2",
            ),
            fact(
                "e-r3",
                records=(record("RV-8", duplicate_of="RV-7"),),
                operator_id="other:reviewer-r3",
            ),
        ]
        cycle = [
            fact("e-r1", records=(record("RV-1", duplicate_of="RV-7"),)),
            fact(
                "e-r2",
                records=(record("RV-7", duplicate_of="RV-1"),),
                operator_id="claude-code:reviewer-r2",
            ),
        ]
        for facts in (chain, cycle):
            with self.subTest(linkage=[item["event_ref"] for item in facts]):
                result = reduce_current_aggregate(facts, SUBJECT_A)
                self.assertEqual(result["state"], "FAIL_CLOSED_AMBIGUOUS_EQUIVALENCE")
                self.assertIsNone(result["judgment"])

    def test_one_identity_cannot_be_both_canonical_and_duplicate(self) -> None:
        facts = [
            fact("e-r1", records=(record("RV-1"),)),
            fact(
                "e-r2",
                records=(
                    record("RV-7"),
                    record("RV-7", duplicate_of="RV-1"),
                ),
                operator_id="claude-code:reviewer-r2",
            ),
        ]
        result = reduce_current_aggregate(facts, SUBJECT_A)
        self.assertEqual(result["state"], "FAIL_CLOSED_AMBIGUOUS_EQUIVALENCE")
        self.assertIsNone(result["judgment"])

    def test_duplicate_link_with_conflicting_classification_fails_closed(self) -> None:
        severity_conflict = [
            fact("e-r1", records=(record("RV-1", "P1"),)),
            fact(
                "e-r2",
                records=(record("RV-7", "P3", "IMPLEMENTATION_DEFECT", duplicate_of="RV-1"),),
                operator_id="claude-code:reviewer-r2",
            ),
        ]
        root_conflict = [
            fact("e-r1", records=(record("RV-1", "P1", "IMPLEMENTATION_DEFECT"),)),
            fact(
                "e-r2",
                records=(
                    record("RV-7", "P1", "TEST_FIXTURE_EVIDENCE_DEFECT", duplicate_of="RV-1"),
                ),
                operator_id="claude-code:reviewer-r2",
            ),
        ]
        for facts in (severity_conflict, root_conflict):
            with self.subTest(records=facts):
                result = reduce_current_aggregate(facts, SUBJECT_A)
                self.assertEqual(result["state"], "FAIL_CLOSED_FINDING_CONFLICT")
                self.assertIsNone(result["judgment"])
                self.assertEqual(result["conflicts"], ("RV-1", "RV-7"))

    def test_duplicate_convergence_is_invariant_to_event_order(self) -> None:
        facts = [
            fact("e-r1", records=(record("RV-1"),), operator_id="chatgpt-web:reviewer-r1"),
            fact(
                "e-r2",
                records=(record("RV-7", duplicate_of="RV-1"),),
                operator_id="claude-code:reviewer-r2",
            ),
        ]
        expected = reduce_current_aggregate(facts, SUBJECT_A)
        for ordering in itertools.permutations(facts):
            with self.subTest(ordering=[item["event_ref"] for item in ordering]):
                self.assertEqual(reduce_current_aggregate(list(ordering), SUBJECT_A), expected)

    def test_reduction_is_invariant_to_event_order(self) -> None:
        facts = [
            fact("e-1", records=(record("RV-1"),)),
            fact("e-2", records=(record("RV-2", "P2"),), operator_id="claude-code:reviewer-r2"),
            fact("e-3", sha=SUBJECT_B, status="PASS", records=()),
        ]
        expected = reduce_current_aggregate(facts, SUBJECT_A)
        for ordering in itertools.permutations(facts):
            with self.subTest(ordering=[item["event_ref"] for item in ordering]):
                self.assertEqual(reduce_current_aggregate(list(ordering), SUBJECT_A), expected)

    def test_conflicting_current_verdicts_fail_closed(self) -> None:
        facts = [
            fact("e-pass", status="PASS", records=()),
            fact("e-fail", status="FAIL", records=(), operator_id="claude-code:reviewer-r2"),
        ]
        result = reduce_current_aggregate(facts, SUBJECT_A)
        self.assertEqual(result["state"], "FAIL_CLOSED_VERDICT_CONFLICT")
        self.assertIsNone(result["judgment"])
        self.assertEqual(result["conflicts"], ("FAIL", "PASS"))

    def test_conflicting_finding_classification_fails_closed(self) -> None:
        severity_conflict = [
            fact("e-r1", records=(record("RV-1", "P1"),)),
            fact("e-r2", records=(record("RV-1", "P3"),), operator_id="claude-code:reviewer-r2"),
        ]
        root_conflict = [
            fact("e-r1", records=(record("RV-1", "P1", "IMPLEMENTATION_DEFECT"),)),
            fact(
                "e-r2",
                records=(record("RV-1", "P1", "TEST_FIXTURE_EVIDENCE_DEFECT"),),
                operator_id="claude-code:reviewer-r2",
            ),
        ]
        for facts in (severity_conflict, root_conflict):
            with self.subTest(records=facts):
                result = reduce_current_aggregate(facts, SUBJECT_A)
                self.assertEqual(result["state"], "FAIL_CLOSED_FINDING_CONFLICT")
                self.assertIsNone(result["judgment"])
                self.assertEqual(result["conflicts"], ("RV-1",))

    def test_reviewer_and_model_count_create_no_authority(self) -> None:
        majority_pass = [
            fact("e-pass-1", status="PASS", records=(), operator_id="chatgpt-web:reviewer-r1"),
            fact("e-pass-2", status="PASS", records=(), operator_id="claude-code:reviewer-r2"),
            fact("e-pass-3", status="PASS", records=(), operator_id="other:reviewer-r3"),
            fact("e-fail", status="FAIL", records=(), operator_id="human:reviewer-r4"),
        ]
        result = reduce_current_aggregate(majority_pass, SUBJECT_A)
        self.assertEqual(result["state"], "FAIL_CLOSED_VERDICT_CONFLICT")
        self.assertIsNone(result["judgment"])

        single_report = reduce_current_aggregate(
            [fact("e-r1", records=(record("RV-1"),))], SUBJECT_A
        )
        repeated_reports = reduce_current_aggregate(
            [
                fact("e-r1", records=(record("RV-1"),), operator_id="chatgpt-web:reviewer-r1"),
                fact("e-r2", records=(record("RV-1"),), operator_id="claude-code:reviewer-r2"),
                fact("e-r3", records=(record("RV-1"),), operator_id="other:reviewer-r3"),
            ],
            SUBJECT_A,
        )
        self.assertEqual(single_report["judgment"], repeated_reports["judgment"])
        self.assertEqual(
            single_report["findings"][0]["severity"], repeated_reports["findings"][0]["severity"]
        )
        self.assertEqual(len(repeated_reports["findings"]), 1)
        # Duplicated reports of one logical defect never escalate its severity.
        self.assertEqual(repeated_reports["findings"][0]["duplicate_ids"], ())

    def test_unresolved_blocking_finding_dominates_the_judgment(self) -> None:
        result = reduce_current_aggregate(
            [fact("e-r1", status="PASS", records=(record("RV-1", "P0"),))], SUBJECT_A
        )
        self.assertEqual(result["state"], "CURRENT")
        self.assertEqual(result["judgment"], "CHANGES_REQUESTED")
        self.assertEqual(result["unresolved_blocker_refs"], ("RV-1",))

    def test_aggregate_is_accepted_by_the_existing_aggregation_contract(self) -> None:
        result = reduce_current_aggregate(
            [fact("e-r1", records=(record("RV-1", "P1"),))], SUBJECT_A
        )
        aggregate = {
            "judgment": result["judgment"],
            "requested_route": "changes-requested",
            "requested_route_authority": "NON_AUTHORITATIVE_DERIVED_STATE",
            "finding_refs": [entry["finding_id"] for entry in result["findings"]],
            "unresolved_blocker_refs": list(result["unresolved_blocker_refs"]),
        }
        findings = [
            {
                "finding_id": entry["finding_id"],
                "severity": entry["severity"],
                "blocking": entry["blocking"],
            }
            for entry in result["findings"]
        ]
        self.assertEqual(validate_review_aggregation(aggregate, findings), [])

        forbidden_pass = {**aggregate, "judgment": "PASS"}
        errors = validate_review_aggregation(forbidden_pass, findings)
        self.assertIn(
            "PASS forbidden while unresolved valid blocker exists",
            errors,
        )

        # The duplicate-converged reduction feeds the same contract: one logical
        # finding (the canonical id), duplicate id retained only as provenance.
        converged = reduce_current_aggregate(
            [
                fact("e-r1", records=(record("RV-1", "P1"),)),
                fact(
                    "e-r2",
                    records=(record("RV-7", duplicate_of="RV-1"),),
                    operator_id="claude-code:reviewer-r2",
                ),
            ],
            SUBJECT_A,
        )
        self.assertEqual([entry["finding_id"] for entry in converged["findings"]], ["RV-1"])
        converged_aggregate = {
            **aggregate,
            "finding_refs": [entry["finding_id"] for entry in converged["findings"]],
            "unresolved_blocker_refs": list(converged["unresolved_blocker_refs"]),
        }
        self.assertEqual(
            validate_review_aggregation(
                converged_aggregate,
                [
                    {
                        "finding_id": entry["finding_id"],
                        "severity": entry["severity"],
                        "blocking": entry["blocking"],
                    }
                    for entry in converged["findings"]
                ],
            ),
            [],
        )

    def test_aggregation_policy_and_route_authority_are_reused_not_redefined(self) -> None:
        schema = load_schema(AGGREGATION_V1)
        self.assertEqual(
            schema["properties"]["aggregation_policy"]["const"], "finding-union-blocker-dominance"
        )
        self.assertEqual(
            schema["properties"]["requested_route_authority"]["const"],
            "NON_AUTHORITATIVE_DERIVED_STATE",
        )
        for member in ("judgment", "finding_refs", "unresolved_blocker_refs", "conflict_refs"):
            with self.subTest(member=member):
                self.assertIn(member, schema["required"])
        subsection = protocol_subsection("### 9.3 Deterministic aggregation")
        self.assertIn("schemas/review-aggregation-v1.schema.json", subsection)
        self.assertIn("finding-union-blocker-dominance", subsection)
        self.assertIn("conflict_refs", subsection)


class WriterBucketConsistencyTests(unittest.TestCase):
    """R4 P1-1: positive severity buckets must reconstruct exactly from records."""

    def test_positive_bucket_without_matching_record_fails_closed(self) -> None:
        result = reduce_current_aggregate(
            [fact("e-opaque", records=(record("RV-1", "P1"),), buckets={"p0": 0, "p1": 1, "p2": 1, "p3": 0})],
            SUBJECT_A,
        )
        self.assertEqual(result["state"], "FAIL_CLOSED_NON_RECONSTRUCTIBLE_FINDING")
        self.assertIsNone(result["judgment"])

    def test_record_without_its_bucket_entry_fails_closed(self) -> None:
        result = reduce_current_aggregate(
            [fact("e-undercount", records=(record("RV-1", "P1"), record("RV-2", "P2")), buckets={"p1": 1, "p2": 0})],
            SUBJECT_A,
        )
        self.assertEqual(result["state"], "FAIL_CLOSED_NON_RECONSTRUCTIBLE_FINDING")
        self.assertIsNone(result["judgment"])

    def test_consistent_buckets_reconstruct_and_duplicate_records_count(self) -> None:
        result = reduce_current_aggregate(
            [
                fact(
                    "e-writer",
                    records=(
                        record("RV-1", "P1"),
                        record("RV-2", "P2", "TEST_FIXTURE_EVIDENCE_DEFECT"),
                        record("RV-3", "P2", "TEST_FIXTURE_EVIDENCE_DEFECT", duplicate_of="RV-2"),
                    ),
                    buckets={"p0": 0, "p1": 1, "p2": 2, "p3": 0},
                )
            ],
            SUBJECT_A,
        )
        self.assertEqual(result["state"], "CURRENT")
        self.assertEqual(result["judgment"], "CHANGES_REQUESTED")
        self.assertEqual([entry["finding_id"] for entry in result["findings"]], ["RV-1", "RV-2"])
        self.assertEqual(result["findings"][1]["duplicate_ids"], ("RV-3",))

    def test_all_zero_buckets_without_records_stay_legal_for_pass(self) -> None:
        result = reduce_current_aggregate(
            [fact("e-clean", status="PASS", records=(), buckets={"p0": 0, "p1": 0, "p2": 0, "p3": 0})],
            SUBJECT_A,
        )
        self.assertEqual(result["state"], "CURRENT")
        self.assertEqual(result["judgment"], "PASS")

    def test_protocol_states_the_bucket_record_reconstruction_rule(self) -> None:
        subsection = protocol_subsection("### 9.2 Machine finding records")
        self.assertIn(
            "A newly emitted event that reports severity bucket counts MUST be exactly reconstructible "
            "from its own `records`",
            subsection,
        )
        self.assertIn("bucket `pN` MUST equal the number of `records` entries with `severity: PN`", subsection)
        self.assertIn("A positive bucket without a matching record is an opaque material finding", subsection)
        self.assertIn("fails the current new-writer/aggregate conformance path", subsection)
        self.assertIn("Duplicate records count in the emitting event's bucket counts", subsection)


class PostHocDuplicateReconciliationTests(unittest.TestCase):
    """R4 P1-2: durable same-subject review-finding-v1 DUPLICATE disposition path."""

    def test_independent_unlinked_finding_reconciles_via_later_disposition(self) -> None:
        facts = [
            fact("e-r1", records=(record("RV-1", "P1"),), operator_id="chatgpt-web:reviewer-r1"),
            fact(
                "e-r2",
                records=(record("RV-7", "P1"),),
                operator_id="claude-code:reviewer-r2",
            ),
        ]
        dispositions = (disposition("d-1", "RV-7", "RV-1"),)
        result = reduce_current_aggregate(facts, SUBJECT_A, dispositions)
        self.assertEqual(result["state"], "CURRENT")
        self.assertEqual(len(result["findings"]), 1)
        converged = result["findings"][0]
        self.assertEqual(converged["finding_id"], "RV-1")
        self.assertEqual(converged["duplicate_ids"], ("RV-7",))
        self.assertEqual(converged["disposition_refs"], ("d-1",))
        self.assertEqual(
            converged["provenance"],
            ("chatgpt-web:reviewer-r1:e-r1", "claude-code:reviewer-r2:e-r2"),
        )
        self.assertEqual(result["unresolved_blocker_refs"], ("RV-1",))

    def test_reconciliation_is_invariant_to_stream_order(self) -> None:
        facts = [
            fact("e-r1", records=(record("RV-1", "P1"),), operator_id="chatgpt-web:reviewer-r1"),
            fact("e-r2", records=(record("RV-7", "P1"),), operator_id="claude-code:reviewer-r2"),
        ]
        dispositions = (disposition("d-1", "RV-7", "RV-1"),)
        expected = reduce_current_aggregate(facts, SUBJECT_A, dispositions)
        stream = [("fact", item) for item in facts] + [("disp", item) for item in dispositions]
        for ordering in itertools.permutations(stream):
            order_facts = [item for kind, item in ordering if kind == "fact"]
            order_disps = tuple(item for kind, item in ordering if kind == "disp")
            with self.subTest(ordering=[item["event_ref"] for _, item in ordering]):
                self.assertEqual(
                    reduce_current_aggregate(order_facts, SUBJECT_A, order_disps),
                    expected,
                )

    def test_unreconciled_independent_ids_stay_distinct(self) -> None:
        facts = [
            fact("e-r1", records=(record("RV-1", "P1"),)),
            fact("e-r2", records=(record("RV-7", "P1"),), operator_id="claude-code:reviewer-r2"),
        ]
        result = reduce_current_aggregate(facts, SUBJECT_A, ())
        self.assertEqual(result["state"], "CURRENT")
        self.assertEqual([entry["finding_id"] for entry in result["findings"]], ["RV-1", "RV-7"])

    def test_stale_cross_subject_disposition_never_reconciles(self) -> None:
        facts = [
            fact("e-r1", records=(record("RV-1", "P1"),)),
            fact("e-r2", records=(record("RV-7", "P1"),), operator_id="claude-code:reviewer-r2"),
        ]
        dispositions = (disposition("d-stale", "RV-7", "RV-1", sha=SUBJECT_B),)
        result = reduce_current_aggregate(facts, SUBJECT_A, dispositions)
        self.assertEqual(result["state"], "CURRENT")
        self.assertEqual([entry["finding_id"] for entry in result["findings"]], ["RV-1", "RV-7"])
        self.assertEqual(result["historical_dispositions"], ("d-stale",))

    def test_competing_dispositions_fail_closed(self) -> None:
        facts = [
            fact("e-r1", records=(record("RV-1", "P1"), record("RV-2", "P2"))),
            fact("e-r2", records=(record("RV-7", "P1"),), operator_id="claude-code:reviewer-r2"),
        ]
        dispositions = (
            disposition("d-a", "RV-7", "RV-1"),
            disposition("d-b", "RV-7", "RV-2"),
        )
        result = reduce_current_aggregate(facts, SUBJECT_A, dispositions)
        self.assertEqual(result["state"], "FAIL_CLOSED_AMBIGUOUS_EQUIVALENCE")
        self.assertIsNone(result["judgment"])

    def test_disposition_contradicting_emission_link_fails_closed(self) -> None:
        facts = [
            fact("e-r1", records=(record("RV-1", "P1"), record("RV-2", "P2"))),
            fact(
                "e-r2",
                records=(record("RV-7", "P1", "IMPLEMENTATION_DEFECT", duplicate_of="RV-1"),),
                operator_id="claude-code:reviewer-r2",
            ),
        ]
        dispositions = (disposition("d-1", "RV-7", "RV-2"),)
        result = reduce_current_aggregate(facts, SUBJECT_A, dispositions)
        self.assertEqual(result["state"], "FAIL_CLOSED_AMBIGUOUS_EQUIVALENCE")
        self.assertIsNone(result["judgment"])

    def test_disposition_agreeing_with_emission_link_converges_once(self) -> None:
        facts = [
            fact("e-r1", records=(record("RV-1", "P1"),)),
            fact(
                "e-r2",
                records=(record("RV-7", "P1", "IMPLEMENTATION_DEFECT", duplicate_of="RV-1"),),
                operator_id="claude-code:reviewer-r2",
            ),
        ]
        dispositions = (disposition("d-1", "RV-7", "RV-1"),)
        result = reduce_current_aggregate(facts, SUBJECT_A, dispositions)
        self.assertEqual(result["state"], "CURRENT")
        self.assertEqual(len(result["findings"]), 1)
        converged = result["findings"][0]
        self.assertEqual(converged["duplicate_ids"], ("RV-7",))
        self.assertEqual(
            converged["provenance"],
            ("chatgpt-web:reviewer-r1:e-r1", "claude-code:reviewer-r2:e-r2"),
        )
        self.assertEqual(converged["disposition_refs"], ("d-1",))

    def test_disposition_with_unknown_id_or_target_fails_closed(self) -> None:
        base = [fact("e-r1", records=(record("RV-1", "P1"),))]
        unknown_target = reduce_current_aggregate(
            base, SUBJECT_A, (disposition("d-1", "RV-7", "RV-1"),)
        )
        self.assertEqual(unknown_target["state"], "FAIL_CLOSED_AMBIGUOUS_EQUIVALENCE")
        unknown_source = reduce_current_aggregate(
            base, SUBJECT_A, (disposition("d-1", "RV-1", "RV-404"),)
        )
        self.assertEqual(unknown_source["state"], "FAIL_CLOSED_AMBIGUOUS_EQUIVALENCE")
        self_link = reduce_current_aggregate(
            base, SUBJECT_A, (disposition("d-1", "RV-1", "RV-1"),)
        )
        self.assertEqual(self_link["state"], "FAIL_CLOSED_AMBIGUOUS_EQUIVALENCE")

    def test_disposition_chain_fails_closed(self) -> None:
        facts = [
            fact("e-r1", records=(record("RV-1", "P1"),)),
            fact("e-r2", records=(record("RV-7", "P1"),), operator_id="claude-code:reviewer-r2"),
            fact("e-r3", records=(record("RV-8", "P1"),), operator_id="other:reviewer-r3"),
        ]
        dispositions = (
            disposition("d-a", "RV-7", "RV-1"),
            disposition("d-b", "RV-8", "RV-7"),
        )
        result = reduce_current_aggregate(facts, SUBJECT_A, dispositions)
        self.assertEqual(result["state"], "FAIL_CLOSED_AMBIGUOUS_EQUIVALENCE")
        self.assertIsNone(result["judgment"])

    def test_reconciled_pair_with_conflicting_classification_fails_closed(self) -> None:
        facts = [
            fact("e-r1", records=(record("RV-1", "P1", "IMPLEMENTATION_DEFECT"),)),
            fact(
                "e-r2",
                records=(record("RV-7", "P3", "IMPLEMENTATION_DEFECT"),),
                operator_id="claude-code:reviewer-r2",
            ),
        ]
        dispositions = (disposition("d-1", "RV-7", "RV-1"),)
        result = reduce_current_aggregate(facts, SUBJECT_A, dispositions)
        self.assertEqual(result["state"], "FAIL_CLOSED_FINDING_CONFLICT")
        self.assertIsNone(result["judgment"])

    def test_protocol_states_the_durable_reconciliation_path(self) -> None:
        subsection = protocol_subsection("### 9.2 Machine finding records")
        self.assertIn("Emission and reconciliation are separate durable facts", subsection)
        self.assertIn(
            "a later durable `review-finding-v1` finding fact with `status: DUPLICATE`, "
            "`resolution_code: DUPLICATE` and `duplicate_of: <canonical finding_id>`",
            subsection,
        )
        self.assertIn("a disposition bound to another subject is stale history and is never consumed", subsection)
        self.assertIn(
            "Competing dispositions (one finding id linked to different targets), a disposition "
            "contradicting an in-emission `duplicate_of` link",
            subsection,
        )
        self.assertIn("never by latest-wins, ordering, majority or count", subsection)
        self.assertIn("both provenance records stay in the converged finding", subsection)
        aggregation = protocol_subsection("### 9.3 Deterministic aggregation")
        self.assertIn(
            "reconciliation may also arrive after emission as a durable same-subject `DUPLICATE` "
            "disposition",
            aggregation,
        )
        self.assertIn("without rewriting the original reviewer facts", aggregation)


class OwnerBoundaryNegativeTests(unittest.TestCase):
    """L3 negative case 5: no new family, dimension, waiver or gate authority."""

    def test_no_new_review_event_type_is_introduced(self) -> None:
        event_values = load_schema(EVENT_V2)["properties"]["event"]["enum"]
        review_types = {value for value in event_values if "REVIEW" in value}
        self.assertEqual(review_types, {"REVIEW_DECISION", "REVIEW_RESULT"})
        for invented in ("REVIEW_FINDING", "REVIEW_FINDING_RECORD", "REVIEW_AGGREGATE", "FINDING_RECORD"):
            with self.subTest(invented=invented):
                self.assertNotIn(invented, event_values)

    def test_no_new_workflow_state_is_introduced_in_section_9(self) -> None:
        used_states = set(re.findall(r"state:([a-z-]+)", protocol_section_9()))
        self.assertTrue(used_states <= CANONICAL_WORKFLOW_STATES, used_states - CANONICAL_WORKFLOW_STATES)

    def test_aggregate_fails_closed_on_non_reconstructible_material_findings(self) -> None:
        subsection = protocol_subsection("### 9.3 Deterministic aggregation")
        self.assertIn("not machine-reconstructible", subsection)
        self.assertIn("fails closed for that subject", subsection)
        self.assertIn("instead of deriving a judgment from an opaque payload", subsection)

    def test_duplicate_equivalence_is_explicit_and_fails_closed(self) -> None:
        subsection = protocol_subsection("### 9.3 Deterministic aggregation")
        self.assertIn(
            "converge by stable identity or by an explicit durable `duplicate_of` equivalence",
            subsection,
        )
        self.assertIn("independent IDs without that relation remain distinct findings", subsection)
        equivalence = protocol_subsection("### 9.2 Machine finding records")
        self.assertIn("Duplicate equivalence is deterministic and fails closed", equivalence)
        self.assertIn("no chains or cycles", equivalence)
        self.assertIn(
            "A missing target, a chain or cycle, or a materially conflicting linked record MUST NOT "
            "be guessed, majority-resolved or silently merged",
            equivalence,
        )
        identity = protocol_subsection("### 9.2 Machine finding records")
        self.assertIn(
            "two records represent the same logical defect only when they share one `finding_id`",
            identity,
        )
        self.assertIn(
            "Root-defect-class equality is classification evidence, never logical-defect identity",
            identity,
        )
        self.assertIn("similarity, ordering and count never establish equivalence", identity)

    def test_no_event_order_majority_or_count_authority_is_granted(self) -> None:
        subsection = protocol_subsection("### 9.3 Deterministic aggregation")
        self.assertIn("invariant to event order or transport arrival order", subsection)
        self.assertIn("fail closed", subsection)
        self.assertIn(
            "MUST NOT be resolved by majority, latest-wins, reviewer/model count, provider or "
            "model reputation, cost, turnaround or file count",
            subsection,
        )
        self.assertIn("reviewer/model count is coverage evidence only, never verdict authority", subsection)
        self.assertNotIn("MAY waive", subsection)
        self.assertNotIn("majority vote decides", subsection)

    def test_evidence_verdict_authority_separation_is_stated(self) -> None:
        subsection = protocol_subsection("### 9.2 Machine finding records")
        self.assertIn("`Evidence != Verdict != Authority`", subsection)
        self.assertIn("merge/release authority remains with the existing Gate Authority chain", subsection)

    def test_validation_and_release_authority_are_not_taken(self) -> None:
        subsection = protocol_subsection("### 9.3 Deterministic aggregation")
        self.assertIn(
            "It introduces no new event family, status dimension, lifecycle, scheduler, registry, "
            "Validation authority or Release authority.",
            subsection,
        )

    def test_no_new_state_dimension_or_review_registry_is_added(self) -> None:
        registry = json.loads(read(STATE_DIMENSIONS))
        dimensions = registry["dimensions"]
        dimension_ids = {entry["dimension_id"] for entry in dimensions}
        self.assertIn("review_judgment", dimension_ids)
        self.assertFalse({"review_currentness", "review_finding"} & dimension_ids, dimension_ids)
        review_dimension = next(entry for entry in dimensions if entry["dimension_id"] == "review_judgment")
        self.assertEqual(review_dimension["vocabulary_ref"], "schemas/review-aggregation-v1.schema.json")
        for invented in (
            "schemas/review-currentness-v1.schema.json",
            "schemas/review-finding-v2.schema.json",
            "schemas/review-aggregation-v2.schema.json",
        ):
            with self.subTest(invented=invented):
                self.assertFalse((ROOT / invented).exists())

    def test_template_stays_within_the_existing_review_result_surface(self) -> None:
        template = read(TEMPLATE)
        self.assertIn("## REVIEW_RESULT example", template)
        self.assertIn("records:", template)
        self.assertNotIn("optional additive machine shape", template)


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
