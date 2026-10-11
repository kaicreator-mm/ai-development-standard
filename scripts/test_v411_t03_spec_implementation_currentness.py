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
Purely offline: standard library only, with the optional `jsonschema` package
used for v1 record admission when importable and a standard-library walk of
the real schema document as the fallback admission path.

Known deferrals (honest, never reported as covered): the supported-consumer
completeness oracle and the C1→C2 window-drift oracle are DEFERRED_TO_T11 —
their tests stay explicitly skipped as NOT_RUN because the seven logical
projection fields alone cannot reveal an unlisted window or an authoritative
support-scope registry; the authoritative binding of real materiality checks
for nonmaterial dispositions is likewise DEFERRED_TO_T11/NOT_RUN, and this
file only enforces and tests the local fail-closed gate (review #1049 F04-R3:
a nonmaterial claim whose materiality/identity/authority refs do not resolve
against the fixture's independently attested registries — issuer, spec
baseline, accepted-delta fingerprint, evidence head — or resolve but bind to
a different subject stays BLOCKED; the registries distinguish an unverified
caller reference from a separately attested fixture finding without claiming
production verification). None of these gaps are claimed as RECONCILED or
proven here; T11/T12 integration, a real Build Host run, and a fresh R3
review remain NOT_RUN.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
import re
import unittest

try:
    import jsonschema
except ImportError:  # stdlib-only environments (CI) use the schema walk below
    jsonschema = None

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

# The v1 schema document itself is the admission authority for the N08
# historical-compat oracle: compatibility records are validated against the
# real `schemas/compatibility-record-v1.schema.json` (never a test-local
# mirror). `jsonschema` is used when importable; the stdlib fallback walks the
# schema document's own keywords so stdlib-only CI keeps the same admission.
# V1_REQUIRED only pins the schema's own required set against regressions.
V1_REQUIRED = {
    "schema_version",
    "record_id",
    "contract",
    "baseline",
    "candidate",
    "change_operations",
    "dimensions",
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
    is fail-closed: provenance-bound nonmaterial proportionality over refs
    resolved against the fixture's independently attested registries (review
    #1049 F04-R3), missing identity, untestable externals, exact-ref derived
    accepted-spec drift,
    flagged drifted scope, non-behavioral GREEN, accepted-not-implemented,
    superseded evidence subject, per-window material-dimension admission (only
    evidenced COMPATIBLE outcomes admit; the required wire/source/behavior
    floor is derived from the standard rather than trusted from the caller),
    then RECONCILED.
    """
    reasons: list[str] = []
    nonmaterial_windows = projection.get("affected_producer_consumer_windows")
    if projection.get("nonmaterial") and not nonmaterial_windows:
        # A nonmaterial disposition is a conclusion, not an input (review F04,
        # fail-closed): it is admissible only when the caller supplies a
        # provenance-bound materiality finding that actually resolves — review
        # #1049 F04-R3: a caller-supplied reference is unverified input, not
        # evidence, so every ref is additionally resolved against the fixture's
        # independently attested registries (issuer, subject, accepted-delta
        # fingerprint, evidence head) and must bind to this exact disposition.
        # A well-formed but unattested ("fake") ref fails closed BLOCKED, and
        # a bare `nonmaterial=True` assertion stays BLOCKED, never
        # NONMATERIAL. The authoritative binding of real materiality checks is
        # centrally owned wiring (DEFERRED_TO_T11, its integration oracle
        # NOT_RUN here); the local attestation gate below is what this file
        # enforces and tests.
        blocked: list[str] = []
        finding = projection.get("materiality_finding_ref")
        if not isinstance(finding, str) or not finding:
            blocked.append(
                "nonmaterial disposition lacks a provenance-bound materiality "
                "finding (checked finding bound to an evidence head); the "
                "authoritative materiality-check binding is "
                "DEFERRED_TO_T11/NOT_RUN and an unbound nonmaterial claim "
                "stays BLOCKED"
            )
        unevidenced = [
            ref
            for ref in ("acceptance_authority_ref", "spec_baseline_ref", "proposed_delta_ref")
            if not projection.get(ref)
        ]
        if nonmaterial_windows is None:
            unevidenced.append("affected_producer_consumer_windows")
        blocked.extend(
            f"nonmaterial disposition lacks separately evidenced support: {ref}"
            for ref in unevidenced
        )
        # Review #1049 F04-R3: shape checks alone treat arbitrary caller
        # strings as already-checked evidence. Every present ref must
        # additionally resolve against the attested registries and bind to
        # this exact disposition subject; anything unresolvable or mis-bound
        # fails the disposition closed below.
        blocked.extend(nonmaterial_attestation_failures(projection))
        contradictory = projection.get("contradictory_evidence_refs")
        if contradictory:
            # Disputed/misclassified change: evidence contradicting the
            # nonmaterial claim must not admit the disposition even with an
            # empty affected-window list.
            blocked.append(
                "nonmaterial disposition is disputed by contradictory evidence "
                f"{contradictory!r}; the change is treated as misclassified "
                "material and stays BLOCKED pending full re-admission"
            )
        if blocked:
            return decision("BLOCKED", blocked)
        return decision(
            "NONMATERIAL",
            [
                "explicit proportionate nonmaterial disposition supported by the "
                "independently attested materiality finding "
                f"{projection['materiality_finding_ref']} (issuer, spec baseline, "
                "accepted-delta fingerprint, and evidence head resolved against "
                "the attested-finding registry and bound to this exact "
                "disposition); no empty heavyweight record"
            ],
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
    # Derived material drift from exact refs (never a caller flag): the
    # reconciliation evidence is bound to the exact accepted delta, so an
    # accepted spec whose current revision has moved makes that scope stale.
    if projection["accepted_spec_current_ref"] != projection["proposed_delta_ref"]:
        return decision(
            "STALE",
            [
                "prior evidence STALE for drifted accepted spec revision: evidence is "
                f"bound to {projection['proposed_delta_ref']} but the current accepted "
                f"spec is {projection['accepted_spec_current_ref']}; revalidation required"
            ],
        )
    # Supplementary channel: an external drift detector may flag drifted scopes
    # directly (N06); the derived check above and the per-window admission below
    # never depend on this flag.
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
        consumer_ref = window["consumer_ref"]
        declared = window.get("required_dimensions")
        declared = declared if isinstance(declared, (list, tuple, set)) else ()
        outcomes = window.get("dimension_outcomes")
        outcomes = outcomes if isinstance(outcomes, dict) else {}
        if not declared:
            reasons.append(
                f"still-supported window {consumer_ref} declares no required material "
                "dimensions; the standard's wire, source, and behavior floor is derived "
                "from the authoritative binding and cannot be narrowed by omission"
            )
        # Material dimensions are derived, not trusted from the caller: the
        # standard's required wire/source/behavior floor (SS5) plus any
        # window-declared extras. Every outcome must be evidenced COMPATIBLE;
        # anything else (missing, INCOMPATIBLE, UNKNOWN, NOT_RUN,
        # CONDITIONALLY_COMPATIBLE, NOT_APPLICABLE, malformed) fails closed.
        extras = tuple(
            dim
            for dim in declared
            if isinstance(dim, str) and dim not in REQUIRED_DIMENSIONS
        )
        for dim in REQUIRED_DIMENSIONS + extras:
            observed = outcomes.get(dim)
            if observed == "COMPATIBLE":
                continue
            if observed is None:
                reasons.append(
                    f"still-supported window {consumer_ref} lacks required {dim} evidence"
                )
            elif observed == "INCOMPATIBLE":
                reasons.append(
                    f"still-supported window {consumer_ref} is INCOMPATIBLE on {dim}"
                )
            else:
                reasons.append(
                    f"still-supported window {consumer_ref} reports {dim} outcome "
                    f"{observed!r}; only evidenced COMPATIBLE admits reconciliation"
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


def nonmaterial_attestation_failures(projection: dict) -> list[str]:
    """Review #1049 F04-R3: a caller-supplied reference is not evidence.

    Resolves a nonmaterial disposition's identity/authority refs and its
    materiality finding against the fixture's independently attested
    registries (`ATTESTED_*` below) and returns one failure reason per ref
    that does not resolve to an attested binding, or that resolves but is not
    bound to this disposition's exact subject (authority/spec, baseline/spec,
    delta fingerprint, finding issuer/subject/delta). Absent refs are already
    reported by the caller-side presence checks; this helper only judges refs
    that are present. An empty result means every ref resolved and mutually
    binds — the only case the nonmaterial branch may admit. The authoritative
    binding of real materiality checks stays DEFERRED_TO_T11/NOT_RUN: this
    fixture-level attestation distinguishes an unverified caller reference
    from a separately attested fixture finding without claiming production
    verification.
    """
    failures: list[str] = []
    authority_ref = projection.get("acceptance_authority_ref")
    baseline_ref = projection.get("spec_baseline_ref")
    delta_ref = projection.get("proposed_delta_ref")
    authority = (
        ATTESTED_AUTHORITIES.get(authority_ref)
        if isinstance(authority_ref, str)
        else None
    )
    baseline = (
        ATTESTED_SPEC_BASELINES.get(baseline_ref)
        if isinstance(baseline_ref, str)
        else None
    )
    delta = ATTESTED_DELTAS.get(delta_ref) if isinstance(delta_ref, str) else None
    if authority_ref and authority is None:
        failures.append(
            f"acceptance_authority_ref {authority_ref!r} does not resolve to an "
            "attested acceptance authority; an unverified caller reference is "
            "not disposition evidence"
        )
    if baseline_ref and baseline is None:
        failures.append(
            f"spec_baseline_ref {baseline_ref!r} does not resolve to an attested "
            "spec baseline; an unverified caller reference is not disposition "
            "evidence"
        )
    if delta_ref and delta is None:
        failures.append(
            f"proposed_delta_ref {delta_ref!r} does not resolve to an attested "
            "accepted delta; an unverified caller reference is not disposition "
            "evidence"
        )
    # Subject binding among refs that individually resolve: one disposition
    # carries exactly one subject — the authority, the baseline, and the
    # accepted delta must all name the same spec.
    if (
        authority is not None
        and baseline is not None
        and authority["authorized_spec"] != baseline["spec"]
    ):
        failures.append(
            f"acceptance_authority_ref {authority_ref!r} is attested for spec "
            f"{authority['authorized_spec']} while spec_baseline_ref "
            f"{baseline_ref!r} attests spec {baseline['spec']}; mismatched "
            "subject binding fails closed"
        )
    if (
        baseline is not None
        and delta is not None
        and delta["spec"] != baseline["spec"]
    ):
        failures.append(
            f"proposed_delta_ref {delta_ref!r} is attested for spec "
            f"{delta['spec']} while spec_baseline_ref {baseline_ref!r} attests "
            f"spec {baseline['spec']}; mismatched subject binding fails closed"
        )
    # The finding itself: a present ref must resolve to an attested finding,
    # and the attested issuer/subject/accepted-delta-fingerprint must equal
    # this disposition's own refs (the ref names its attested evidence head).
    finding_ref = projection.get("materiality_finding_ref")
    finding = (
        ATTESTED_MATERIALITY_FINDINGS.get(finding_ref)
        if isinstance(finding_ref, str)
        else None
    )
    if finding_ref and finding is None:
        failures.append(
            f"materiality finding ref {finding_ref!r} does not resolve to an "
            "attested materiality finding (issuer, spec baseline, accepted-delta "
            "fingerprint, and evidence head all fixture-attested); a "
            "well-formed but unattested caller reference is not checked "
            "evidence"
        )
    if finding is not None:
        if finding["issuer"] != authority_ref:
            failures.append(
                f"materiality finding {finding_ref!r} is attested as issued by "
                f"{finding['issuer']!r} while the disposition claims authority "
                f"{authority_ref!r}; issuer binding fails closed"
            )
        if finding["spec_baseline_ref"] != baseline_ref:
            failures.append(
                f"materiality finding {finding_ref!r} is attested for baseline "
                f"{finding['spec_baseline_ref']!r} while the disposition claims "
                f"{baseline_ref!r}; subject binding fails closed"
            )
        if delta is not None and finding["delta_sha"] != delta["delta_sha"]:
            failures.append(
                f"materiality finding {finding_ref!r} is attested for "
                f"accepted-delta fingerprint {finding['delta_sha']} while "
                f"proposed_delta_ref {delta_ref!r} resolves to fingerprint "
                f"{delta['delta_sha']}; delta-fingerprint binding fails closed"
            )
    return failures


def evidenced_window(consumer_ref: str, outcomes: dict | None = None) -> dict:
    window = {
        "consumer_ref": consumer_ref,
        "required_dimensions": REQUIRED_DIMENSIONS,
    }
    if outcomes is not None:
        window["dimension_outcomes"] = outcomes
    return window


class _SchemaRejection(Exception):
    """Internal signal: the instance violates a walked schema constraint."""


def _stdlib_json_type_matches(instance: object, expected: str) -> bool:
    if expected == "object":
        return isinstance(instance, dict)
    if expected == "array":
        return isinstance(instance, list)
    if expected == "string":
        return isinstance(instance, str)
    if expected == "integer":
        return isinstance(instance, int) and not isinstance(instance, bool)
    if expected == "number":
        return isinstance(instance, (int, float)) and not isinstance(instance, bool)
    if expected == "boolean":
        return isinstance(instance, bool)
    if expected == "null":
        return instance is None
    return False


def _json_equal(instance: object, const: object) -> bool:
    """Type-sensitive JSON equality per Draft 2020-12 const/enum semantics.

    Python evaluates ``True == 1`` (and transitively ``[True] == [1]`` and
    ``True in [1]``) as true, which would let a JSON boolean satisfy an
    integer `const` or slip into a numeric `enum`. JSON Schema treats boolean
    as a distinct type from integer/number, so equality here is structural
    behind an explicit bool/non-bool type gate; JSON numbers 1 and 1.0 remain
    equal.
    """
    if isinstance(instance, bool) or isinstance(const, bool):
        return (
            isinstance(instance, bool)
            and isinstance(const, bool)
            and instance == const
        )
    if isinstance(instance, (int, float)) and isinstance(const, (int, float)):
        return instance == const
    if type(instance) is not type(const):
        return False
    if isinstance(instance, list):
        return len(instance) == len(const) and all(
            _json_equal(left, right) for left, right in zip(instance, const)
        )
    if isinstance(instance, dict):
        return instance.keys() == const.keys() and all(
            _json_equal(value, const[key]) for key, value in instance.items()
        )
    return instance == const


def _check_v1_constraints(instance: object, schema: dict) -> None:
    """Walk the real schema document's own keywords; raise on first violation.

    Covers the keyword set the v1 schema actually uses: `type` (including type
    lists), `const`, `enum`, `minLength`, `minItems`, `items`, `required`,
    `properties`, and `additionalProperties: false`. `const` and `enum` use
    type-sensitive JSON equality (`_json_equal`), so a JSON boolean never
    satisfies an integer const (review F03).
    """
    expected = schema.get("type")
    if expected is not None:
        allowed = expected if isinstance(expected, list) else [expected]
        if not any(_stdlib_json_type_matches(instance, kind) for kind in allowed):
            raise _SchemaRejection(
                f"expected type {expected}, got {type(instance).__name__}"
            )
    if "const" in schema and not _json_equal(instance, schema["const"]):
        raise _SchemaRejection(f"expected const {schema['const']!r}, got {instance!r}")
    if "enum" in schema and not any(
        _json_equal(instance, option) for option in schema["enum"]
    ):
        raise _SchemaRejection(f"{instance!r} is not in the schema enum")
    if isinstance(instance, str):
        minimum = schema.get("minLength")
        if minimum is not None and len(instance) < minimum:
            raise _SchemaRejection(f"string shorter than minLength {minimum}")
    if isinstance(instance, list):
        minimum = schema.get("minItems")
        if minimum is not None and len(instance) < minimum:
            raise _SchemaRejection(f"array shorter than minItems {minimum}")
        items = schema.get("items")
        if items is not None:
            for index, item in enumerate(instance):
                try:
                    _check_v1_constraints(item, items)
                except _SchemaRejection as error:
                    raise _SchemaRejection(f"items[{index}]: {error}") from None
    if isinstance(instance, dict):
        properties = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in instance:
                raise _SchemaRejection(f"missing required property {key!r}")
        if schema.get("additionalProperties") is False:
            for key in instance:
                if key not in properties:
                    raise _SchemaRejection(f"unexpected property {key!r}")
        for key, value in instance.items():
            if key in properties:
                try:
                    _check_v1_constraints(value, properties[key])
                except _SchemaRejection as error:
                    raise _SchemaRejection(f"{key}: {error}") from None


_V1_SCHEMA_DOCUMENT: dict | None = None


def v1_schema_document() -> dict:
    """The real compatibility-record-v1 schema document (read once)."""
    global _V1_SCHEMA_DOCUMENT
    if _V1_SCHEMA_DOCUMENT is None:
        _V1_SCHEMA_DOCUMENT = json.loads(SCHEMA.read_text(encoding="utf-8"))
    return _V1_SCHEMA_DOCUMENT


def _stdlib_v1_accepts(record: object) -> bool:
    try:
        _check_v1_constraints(record, v1_schema_document())
    except _SchemaRejection:
        return False
    return True


def _jsonschema_v1_accepts(record: object) -> bool:
    try:
        jsonschema.validate(record, v1_schema_document())
    except jsonschema.ValidationError:
        return False
    return True


def v1_schema_engines() -> list:
    """Available v1 admission engines as (name, accepts) pairs.

    The stdlib walk of the real schema document is always present so the
    oracle holds in stdlib-only CI; `jsonschema` is added when importable,
    and the tests assert both engines agree on every record. The schema file —
    not a test-local mirror — is the admission authority.
    """
    engines = [("stdlib-schema-walk", _stdlib_v1_accepts)]
    if jsonschema is not None:
        engines.append(("jsonschema", _jsonschema_v1_accepts))
    return engines


# ---------------------------------------------------------------------------
# Fixtures: accepted spec S1, producer revisions H0 (old) / H1 (new), supported
# consumers C0 / C1, per Task Pack S3 scenarios.
# ---------------------------------------------------------------------------

AUTHORIZED_AUTHORITY = "authority/frozen-issue-comment"
ACCEPTED_S1 = "spec/S1@accepted-delta-sha"

# Review #1049 F04-R3: a caller-supplied reference is unverified input, not
# evidence. These fixture-level registries are this test's independent
# attestation record (issued by the fixture, never by the caller): each
# attested materiality finding binds its issuer, its exact subject (spec
# baseline + accepted delta), the accepted-delta fingerprint it was issued
# against, and the evidence head it was checked at; identity/authority refs
# must resolve to attested bindings of the same subject. `decide` resolves a
# nonmaterial disposition's refs against these registries (at call time, see
# `nonmaterial_attestation_failures`) and fails closed (BLOCKED) on any
# unresolvable or mis-bound ref — including a well-formed but unregistered
# ("fake") one. The authoritative binding of real materiality checks stays
# DEFERRED_TO_T11/NOT_RUN: fixture attestation only distinguishes unverified
# caller references from separately attested fixture findings; it is not a
# production verification claim.
ATTESTED_AUTHORITIES = {
    # The fixture's acceptance authority, attested for spec S1 only.
    AUTHORIZED_AUTHORITY: {"authorized_spec": "spec/S1"},
}
ATTESTED_SPEC_BASELINES = {
    "spec/S1@baseline-sha": {"spec": "spec/S1"},
    # A second attested baseline (different spec) so the subject-binding
    # oracles can distinguish an unresolvable ref from a resolvable ref bound
    # to the wrong subject.
    "spec/S2@baseline-sha": {"spec": "spec/S2"},
}
ATTESTED_DELTAS = {
    ACCEPTED_S1: {"spec": "spec/S1", "delta_sha": "accepted-delta-sha"},
    # A second attested delta of the same spec, for the same purpose.
    "spec/S1@revised-delta-sha": {"spec": "spec/S1", "delta_sha": "revised-delta-sha"},
}
ATTESTED_MATERIALITY_FINDINGS = {
    "finding/materiality@evidence-head-sha": {
        "issuer": AUTHORIZED_AUTHORITY,
        "spec_baseline_ref": "spec/S1@baseline-sha",
        "proposed_delta_ref": ACCEPTED_S1,
        "delta_sha": "accepted-delta-sha",
        "evidence_head": "evidence-head-sha",
    },
    "finding/materiality-revised@evidence-head-sha": {
        "issuer": AUTHORIZED_AUTHORITY,
        "spec_baseline_ref": "spec/S1@baseline-sha",
        "proposed_delta_ref": "spec/S1@revised-delta-sha",
        "delta_sha": "revised-delta-sha",
        "evidence_head": "evidence-head-sha",
    },
}

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

# A nonmaterial disposition is itself separately evidenced (review F04): a
# disposition authority, the exact accepted-change binding, and a
# provenance-bound already-checked materiality finding bound to an evidence
# head. Review #1049 F04-R3: the finding ref below is admitted only because
# it resolves to a fixture-level, independently attested registry entry
# (issuer, spec baseline, accepted-delta fingerprint, evidence head) bound to
# this exact disposition — not because its string shape looks plausible; an
# unresolvable or mis-bound ref fails closed (BLOCKED). The authoritative
# binding of real materiality checks is DEFERRED_TO_T11/NOT_RUN; the decision
# model enforces the attestation binding and fails closed without it.
P03_NONMATERIAL = {
    "nonmaterial": True,
    "acceptance_authority_ref": AUTHORIZED_AUTHORITY,
    "spec_baseline_ref": "spec/S1@baseline-sha",
    "proposed_delta_ref": ACCEPTED_S1,
    "materiality_finding_ref": "finding/materiality@evidence-head-sha",
    "affected_producer_consumer_windows": [],
}

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
        # The disposition must be traceable to the provenance-bound materiality
        # finding (review F04), never to the bare caller flag. Review #1049
        # F04-R3: the finding is admitted only because it resolves to the
        # fixture's independently attested registry entry bound to this exact
        # disposition — not because the string shape looks plausible.
        self.assertIn("finding/materiality@evidence-head-sha", verdict["reasons"][0])
        self.assertIn("independently attested materiality finding", verdict["reasons"][0])


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

    def test_unknown_dimension_outcome_is_never_promoted_to_reconciled(self) -> None:
        # Review F01: an UNKNOWN outcome is not compatible (SS5/SS10); the
        # per-window admission must fail closed instead of ignoring it.
        projection = dict(P01_PROJECTION)
        projection["affected_producer_consumer_windows"] = [
            evidenced_window(
                "consumer/C0@v1",
                {"wire": "COMPATIBLE", "source": "COMPATIBLE", "behavior": "UNKNOWN"},
            ),
            evidenced_window(
                "consumer/C1@v2",
                {"wire": "COMPATIBLE", "source": "COMPATIBLE", "behavior": "COMPATIBLE"},
            ),
        ]
        verdict = decide(projection)
        self.assertEqual(verdict["decision"], "UNKNOWN")
        self.assertTrue(any("behavior" in reason for reason in verdict["reasons"]))
        self.assertNotEqual(verdict["decision"], "RECONCILED")

    def test_not_run_dimension_outcome_is_never_promoted_to_reconciled(self) -> None:
        # Review F01: NOT_RUN is missing execution, never a compatibility PASS.
        projection = dict(P01_PROJECTION)
        projection["affected_producer_consumer_windows"] = [
            evidenced_window(
                "consumer/C0@v1",
                {"wire": "COMPATIBLE", "source": "NOT_RUN", "behavior": "COMPATIBLE"},
            ),
            evidenced_window(
                "consumer/C1@v2",
                {"wire": "COMPATIBLE", "source": "COMPATIBLE", "behavior": "COMPATIBLE"},
            ),
        ]
        verdict = decide(projection)
        self.assertEqual(verdict["decision"], "UNKNOWN")
        self.assertTrue(any("source" in reason for reason in verdict["reasons"]))
        self.assertNotEqual(verdict["decision"], "RECONCILED")

    def test_illegal_dimension_outcomes_fail_closed(self) -> None:
        # Review F01: only evidenced COMPATIBLE admits; every other value
        # (enum vocabulary, malformed, or missing) fails closed.
        for outcome in ("PASS", "GREEN", "CONDITIONALLY_COMPATIBLE", "NOT_APPLICABLE", 7, "", None):
            with self.subTest(outcome=outcome):
                projection = dict(P01_PROJECTION)
                projection["affected_producer_consumer_windows"] = [
                    evidenced_window(
                        "consumer/C0@v1",
                        {"wire": "COMPATIBLE", "source": "COMPATIBLE", "behavior": outcome},
                    ),
                    evidenced_window(
                        "consumer/C1@v2",
                        {
                            "wire": "COMPATIBLE",
                            "source": "COMPATIBLE",
                            "behavior": "COMPATIBLE",
                        },
                    ),
                ]
                verdict = decide(projection)
                self.assertIn(verdict["decision"], ("UNKNOWN", "INCOMPATIBLE"))
                self.assertNotEqual(verdict["decision"], "RECONCILED")

    def test_window_with_no_required_material_dimensions_fails_closed(self) -> None:
        # Review F02 counterexample: zero declared dimensions with empty
        # outcomes must not reconcile; the required material floor is derived
        # from the authoritative binding, never defaulted to empty.
        projection = dict(P01_PROJECTION)
        projection["affected_producer_consumer_windows"] = [
            {
                "consumer_ref": "consumer/C0@v1",
                "required_dimensions": (),
                "dimension_outcomes": {},
            }
        ]
        verdict = decide(projection)
        self.assertEqual(verdict["decision"], "UNKNOWN")
        self.assertTrue(
            any(
                "declares no required material dimensions" in reason
                for reason in verdict["reasons"]
            )
        )
        self.assertNotEqual(verdict["decision"], "RECONCILED")

    @unittest.skip(
        "NOT_RUN / DEFERRED_TO_T11: detecting an omitted still-supported window "
        "requires the centrally designated wiring adapter to bind the accepted delta "
        "to the authoritative contract's supported-consumer registry; the seven "
        "logical projection fields alone cannot reveal an unlisted window, so this "
        "completeness oracle is honestly not claimed as covered here."
    )
    def test_missing_still_supported_consumer_window_fails_closed(self) -> None:
        # Deferred wiring oracle: when only the passing C1 window is listed and
        # the still-supported C0 window is omitted, the wiring adapter must
        # derive the affected-window list from the authoritative binding and
        # route such incomplete projections away from RECONCILED.
        projection = dict(P01_PROJECTION)
        projection["affected_producer_consumer_windows"] = [
            evidenced_window(
                "consumer/C1@v2",
                {"wire": "COMPATIBLE", "source": "COMPATIBLE", "behavior": "COMPATIBLE"},
            )
        ]
        self.assertNotEqual(decide(projection)["decision"], "RECONCILED")

    def test_accepted_spec_drift_to_s2_is_derived_from_exact_refs_not_flags(self) -> None:
        # Review F03: reconciliation evidence is bound to the exact accepted
        # delta; the S1 -> S2 accepted-spec move must be derived from the refs
        # themselves, with no fixture flag involved.
        projection = dict(P01_PROJECTION)
        projection["accepted_spec_current_ref"] = "spec/S2@sha"
        self.assertNotIn("drifted_material_scope", projection)
        verdict = decide(projection)
        self.assertEqual(verdict["decision"], "STALE")
        self.assertIn("accepted spec revision", verdict["reasons"][0])
        self.assertIn("revalidation required", verdict["reasons"][0])

    def test_producer_subject_drift_to_h2_is_derived_from_exact_refs_not_flags(self) -> None:
        # Review F03: the H1 -> H2 subject move is derived from the evidence
        # subject versus current subject ref comparison, not a fixture flag.
        projection = dict(P01_PROJECTION)
        projection["implementation_subject_ref"] = "producer/H2@sha"
        self.assertNotIn("drifted_material_scope", projection)
        verdict = decide(projection)
        self.assertEqual(verdict["decision"], "STALE")
        self.assertIn("superseded subject", verdict["reasons"][0])
        self.assertIn("revalidation required", verdict["reasons"][0])

    @unittest.skip(
        "NOT_RUN / DEFERRED_TO_T11: consumer-window drift (C1 -> C2) can only be "
        "derived against the authoritative supported-window registry owned by the "
        "centrally designated wiring adapter; the projection's window list is "
        "itself the claimed support scope, so this drift oracle is honestly not "
        "claimed as covered here."
    )
    def test_supported_consumer_window_drift_to_c2_is_derived_not_flagged(self) -> None:
        # Deferred wiring oracle: when the supported window moves from C1@v2 to
        # C2@v3, the adapter must rebind window evidence to the registry and
        # route the superseded-window scope to STALE for revalidation.
        projection = dict(P01_PROJECTION)
        projection["affected_producer_consumer_windows"] = [
            evidenced_window(
                "consumer/C2@v3",
                {"wire": "COMPATIBLE", "source": "COMPATIBLE", "behavior": "COMPATIBLE"},
            )
        ]
        self.assertEqual(decide(projection)["decision"], "STALE")

    def test_unevidenced_nonmaterial_disposition_fails_closed(self) -> None:
        # Review F04 counterexample: a bare nonmaterial claim with no
        # disposition authority, no exact change binding, and no provenance-
        # bound materiality finding is fail-closed BLOCKED, never NONMATERIAL.
        verdict = decide({"nonmaterial": True, "affected_producer_consumer_windows": []})
        self.assertEqual(verdict["decision"], "BLOCKED")
        self.assertNotEqual(verdict["decision"], "NONMATERIAL")
        self.assertIn(
            "nonmaterial disposition lacks a provenance-bound materiality finding",
            verdict["reasons"][0],
        )
        self.assertIn("DEFERRED_TO_T11/NOT_RUN", verdict["reasons"][0])
        for ref in ("acceptance_authority_ref", "spec_baseline_ref", "proposed_delta_ref"):
            self.assertIn(
                f"nonmaterial disposition lacks separately evidenced support: {ref}",
                verdict["reasons"],
            )

    def test_nonmaterial_without_provenance_bound_materiality_finding_is_blocked(self) -> None:
        # Review F04 (R2): `nonmaterial=True` plus empty windows plus the three
        # identity refs is still just a caller assertion; without a checked
        # materiality finding bound to an evidence head the disposition must
        # not be admitted (fail-closed BLOCKED). The authoritative real-
        # materiality binding is DEFERRED_TO_T11/NOT_RUN.
        projection = dict(P03_NONMATERIAL)
        del projection["materiality_finding_ref"]
        verdict = decide(projection)
        self.assertEqual(verdict["decision"], "BLOCKED")
        self.assertNotEqual(verdict["decision"], "NONMATERIAL")
        self.assertIn("provenance-bound materiality finding", verdict["reasons"][0])
        # A non-string finding identifier is equally unbound (malformed).
        malformed = dict(P03_NONMATERIAL)
        malformed["materiality_finding_ref"] = 7
        self.assertEqual(decide(malformed)["decision"], "BLOCKED")

    def test_disputed_nonmaterial_claim_with_contradictory_evidence_is_blocked(self) -> None:
        # Review F04 (R2) disputed/misclassified negative oracle: a nonmaterial
        # claim contradicted by evidence (even with no affected window listed)
        # must not be admitted as NONMATERIAL.
        projection = dict(P03_NONMATERIAL)
        projection["contradictory_evidence_refs"] = ["evidence/consumer-report@head"]
        verdict = decide(projection)
        self.assertEqual(verdict["decision"], "BLOCKED")
        self.assertNotEqual(verdict["decision"], "NONMATERIAL")
        self.assertTrue(
            any("contradictory evidence" in reason for reason in verdict["reasons"])
        )
        self.assertTrue(
            any("misclassified material" in reason for reason in verdict["reasons"])
        )

    def test_review_1049_falsifier_arbitrary_refs_stay_blocked(self) -> None:
        # Review #1049 F04-R3 concrete falsifier, pinned verbatim: every ref
        # is a non-empty, well-shaped string, yet none resolves to an attested
        # binding. The old shape-only gate admitted this projection as
        # NONMATERIAL; it must fail closed BLOCKED instead.
        projection = {
            "nonmaterial": True,
            "affected_producer_consumer_windows": [],
            "materiality_finding_ref": "arbitrary/not-checked",
            "acceptance_authority_ref": "arbitrary",
            "spec_baseline_ref": "s",
            "proposed_delta_ref": "d",
        }
        verdict = decide(projection)
        self.assertEqual(verdict["decision"], "BLOCKED")
        self.assertNotEqual(verdict["decision"], "NONMATERIAL")
        self.assertIn(
            "does not resolve to an attested", verdict["reasons"][0]
        )

    def test_fake_but_well_formed_unattested_finding_ref_is_blocked(self) -> None:
        # Review #1049 F04-R3: a plausible, well-formed finding ref the
        # fixture never attested is unverified caller input, not checked
        # evidence; the disposition fails closed instead of trusting the
        # ref's shape (the negative class the R2 malformed/removal oracles
        # did not cover).
        projection = dict(P03_NONMATERIAL)
        projection["materiality_finding_ref"] = "review:spec-governance@6105069"
        verdict = decide(projection)
        self.assertEqual(verdict["decision"], "BLOCKED")
        self.assertNotEqual(verdict["decision"], "NONMATERIAL")
        self.assertIn(
            "does not resolve to an attested materiality finding",
            verdict["reasons"][0],
        )

    def test_unattested_identity_refs_fail_closed(self) -> None:
        # Review #1049 F04-R3: the three identity/authority refs are no longer
        # trusted on truthiness; each well-formed but unattested value fails
        # the disposition closed.
        for ref, fake in (
            ("acceptance_authority_ref", "authority/self-declared-comment"),
            ("spec_baseline_ref", "spec/S1@unattested-baseline-sha"),
            ("proposed_delta_ref", "spec/S1@unattested-delta-sha"),
        ):
            with self.subTest(ref=ref):
                projection = dict(P03_NONMATERIAL)
                projection[ref] = fake
                verdict = decide(projection)
                self.assertEqual(verdict["decision"], "BLOCKED")
                self.assertNotEqual(verdict["decision"], "NONMATERIAL")
                self.assertTrue(
                    any(
                        "does not resolve to an attested" in reason
                        for reason in verdict["reasons"]
                    )
                )

    def test_attested_finding_bound_to_wrong_delta_fingerprint_is_blocked(self) -> None:
        # Review #1049 F04-R3: resolution is necessary but not sufficient —
        # the attested finding for the revised delta resolves against the
        # registry yet is bound to a different accepted-delta fingerprint
        # than this disposition claims; the mismatch fails closed, never
        # NONMATERIAL.
        projection = dict(P03_NONMATERIAL)
        projection["materiality_finding_ref"] = (
            "finding/materiality-revised@evidence-head-sha"
        )
        verdict = decide(projection)
        self.assertEqual(verdict["decision"], "BLOCKED")
        self.assertNotEqual(verdict["decision"], "NONMATERIAL")
        self.assertTrue(
            any("delta-fingerprint binding fails closed" in reason for reason in verdict["reasons"])
        )

    def test_attested_refs_bound_to_different_specs_fail_closed(self) -> None:
        # Review #1049 F04-R3 subject binding: every ref individually
        # resolves, but the baseline attests spec S2 while the authority and
        # the finding attest spec S1; one disposition carries exactly one
        # subject, so the mismatch fails closed.
        projection = dict(P03_NONMATERIAL)
        projection["spec_baseline_ref"] = "spec/S2@baseline-sha"
        verdict = decide(projection)
        self.assertEqual(verdict["decision"], "BLOCKED")
        self.assertNotEqual(verdict["decision"], "NONMATERIAL")
        self.assertTrue(
            any("mismatched subject binding" in reason for reason in verdict["reasons"])
        )
        self.assertTrue(
            any("subject binding fails closed" in reason for reason in verdict["reasons"])
        )

    def test_nonmaterial_claim_with_a_material_diff_is_not_nonmaterial(self) -> None:
        # Review F04: a nonmaterial label contradicted by evidenced affected
        # windows falls through to the full material admission path.
        for outcomes in (
            {"wire": "COMPATIBLE", "source": "INCOMPATIBLE", "behavior": "COMPATIBLE"},
            None,
        ):
            with self.subTest(outcomes=outcomes):
                projection = dict(P01_PROJECTION)
                projection["nonmaterial"] = True
                projection["affected_producer_consumer_windows"] = [
                    evidenced_window("consumer/C0@v1", outcomes)
                ]
                verdict = decide(projection)
                self.assertNotEqual(verdict["decision"], "NONMATERIAL")
                self.assertEqual(
                    verdict["decision"], "INCOMPATIBLE" if outcomes else "UNKNOWN"
                )


class HistoricalV1ReaderCompatTests(unittest.TestCase):
    """N08: unmodified historical v1 records stay valid; no retroactive fields.

    Admission is validated against the real v1 schema document with every
    available engine (the stdlib schema walk, plus `jsonschema` when
    importable) — never against a test-local mirror of the schema.
    """

    def test_n08_historical_v1_record_is_accepted_without_new_fields(self) -> None:
        for engine, accepts in v1_schema_engines():
            with self.subTest(engine=engine):
                self.assertTrue(accepts(HISTORICAL_V1_RECORD))
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

    def test_broken_v1_records_are_still_rejected_by_the_real_schema(self) -> None:
        mutated = dict(HISTORICAL_V1_RECORD)
        mutated["spec_baseline_ref"] = "spec/S1@baseline-sha"
        bad_outcome = copy.deepcopy(HISTORICAL_V1_RECORD)
        bad_outcome["dimensions"][0]["outcome"] = "PASS"
        for engine, accepts in v1_schema_engines():
            with self.subTest(engine=engine):
                self.assertFalse(accepts(mutated))
                self.assertFalse(accepts(bad_outcome))

    def test_v1_schema_rejects_malformed_dimension_names_and_evidence_refs(self) -> None:
        # Review F05: the previous hand-mirrored reader accepted empty or
        # non-string dimension names and empty-string evidence refs that the
        # real schema forbids (minLength on name and on evidence items).
        empty_name = copy.deepcopy(HISTORICAL_V1_RECORD)
        empty_name["dimensions"][0]["name"] = ""
        non_string_name = copy.deepcopy(HISTORICAL_V1_RECORD)
        non_string_name["dimensions"][0]["name"] = 7
        empty_evidence_ref = copy.deepcopy(HISTORICAL_V1_RECORD)
        empty_evidence_ref["dimensions"][0]["evidence_refs"] = [""]
        non_string_evidence_ref = copy.deepcopy(HISTORICAL_V1_RECORD)
        non_string_evidence_ref["dimensions"][0]["evidence_refs"] = [7]
        for engine, accepts in v1_schema_engines():
            for label, malformed in (
                ("empty dimension name", empty_name),
                ("non-string dimension name", non_string_name),
                ("empty evidence ref", empty_evidence_ref),
                ("non-string evidence ref", non_string_evidence_ref),
            ):
                with self.subTest(engine=engine, malformed=label):
                    self.assertFalse(accepts(malformed))

    def test_v1_schema_rejects_boolean_schema_version_const_violation(self) -> None:
        # Review F03 (R2): Python evaluates `True == 1`, so a loose `!=` const
        # check would let the JSON boolean `true` satisfy the schema's
        # `schema_version` integer `const 1`. Draft 2020-12 treats boolean as a
        # distinct type from integer: the stdlib walk must reject, and the
        # `jsonschema` engine must reject too when importable (otherwise that
        # half is honestly NOT_RUN, never claimed).
        mutated = copy.deepcopy(HISTORICAL_V1_RECORD)
        mutated["schema_version"] = True
        for engine, accepts in v1_schema_engines():
            with self.subTest(engine=engine):
                self.assertFalse(accepts(mutated))
        if jsonschema is None:
            # NOT_RUN: the jsonschema half of this dual-engine oracle is not
            # claimed in stdlib-only environments; only the stdlib walk ran.
            print(
                "NOT_RUN: jsonschema unavailable; boolean-const oracle ran "
                "the stdlib schema walk only"
            )


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

    def test_v1_schema_reader_does_not_mutate_the_historical_record(self) -> None:
        snapshot = copy.deepcopy(HISTORICAL_V1_RECORD)
        for engine, accepts in v1_schema_engines():
            with self.subTest(engine=engine):
                self.assertTrue(accepts(HISTORICAL_V1_RECORD))
        self.assertEqual(HISTORICAL_V1_RECORD, snapshot)


if __name__ == "__main__":
    import sys

    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
