"""V410-T07B: core-feature-freeze Product-decision support oracle.

Focused deterministic suite for the durable decision-record plumbing shipped by
this task (oracle binding: positives P1-P6 from #863@6013682453;
AUTHORITY_NEGATIVES 1-7 from #863@6040872034, cross-checked against N1-N11 of
#863@6013682453; DECISION_RECORD_SEAM 8-field design + recording rule from
#863@6040872034; L3 seed from #863@6003305569; rebind subject cea2e0cc / tree
cef6ce2e, the merged #933 integration tip = V410-T07A INTEGRATED).

The suite validates the fill-in template ``templates/product-decision-record.md``
(single fenced JSON machine-record skeleton, to-be-filled-by-authority slots,
zero decided values), the decision-path reference and the version-closure
checklist row, and proves the recording rules through a record-model validator
applied to synthetic records: a validly-shaped record with a human Product
authority owner completes; an evidence-backed negative outcome with blocking
refs is legal and complete; supersession appends without rewriting; evidence
inputs stay ref-shaped; and every no-auto-YES authority negative
(Release READY/Candidate Freeze, V01/Validation PASS, CI/Review/model-majority/
scheduler activity, missing-evidence default, stale subject binding,
implementation-role self-authorization, #861 machinery authority widening)
fails closed. The machine layer checks record CONFORMANCE only — it never
produces, defaults, or suggests a decision value, and this task NEVER makes the
``ADS_CORE_FEATURE_FREEZE_ELIGIBLE`` decision.

Purely local; no network; stdlib only.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from v34_rules import REQUIRED_CORE_ARTIFACTS, core_artifacts_complete  # noqa: E402

TEMPLATE = ROOT / "templates" / "product-decision-record.md"
REFERENCE = ROOT / "references" / "PRODUCT_DECISION_RECORD_REFERENCE.md"
CHECKLIST = ROOT / "checklists" / "version-closure.md"
PACK_DIR = ROOT / ".agent" / "execution" / "V410-T07B-R1"
OWNER_CONVERGENCE_SUITE = ROOT / "scripts" / "test_v410_owner_convergence.py"
T07A_INDEX_REL = "docs/implementation/4.10.0/PRODUCT_ACCEPTANCE_EVIDENCE_PROJECTION_R1.md"
PRD_REL = "docs/implementation/4.10.0/PRD.md"

# Exact rebind subject of this task (merged #933 integration tip; V410-T07A INTEGRATED).
REBIND_BASE_SHA = "cea2e0ccd045e8fcebaf110273129b198ed259fd"
REBIND_BASE_TREE = "cef6ce2e91cc62f4e1afe53b4a048f3fa4812fa2"

# Candidate-bound citations (fail closed on drift; rebind required, never edited in place).
T07A_INDEX_BLOB_AT_BASE = "65baefd3a1d087d3692e6e603dbe098546bc7cb1"
PRD_FROZEN_BLOB = "b0b9906035eee253aad4bff0274d3d4c8f90b9db"

SCHEMA = "v410-product-decision-record-v1"
DECISION_KEY = "ADS_CORE_FEATURE_FREEZE_ELIGIBLE"
# The two legal outcome values (PRD §1.1; both legal). These tokens exist in
# this suite ONLY as validator vocabulary and synthetic mutant data — never as
# a decided instance (no shipped surface carries a decision value).
OUTCOME_VALUES = ("YES", "NO")
OWNER_ROLE = "HUMAN_PRODUCT_AUTHORITY_OWNER"
DELEGATED_ROLE = "DELEGATED_ACTOR_WITHIN_BOUNDED_AUTHORITY"
AUTHORITY_ROLES = frozenset({OWNER_ROLE, DELEGATED_ROLE})
FORBIDDEN_ACTOR_ROLES = frozenset(
    {"BUILDER", "VALIDATOR", "REVIEWER", "CONTROLLER", "SCHEDULER", "IMPLEMENTATION_TASK", "CI", "MODEL_VOTE"}
)
AUTO_VALUE_SOURCES = frozenset(
    {
        "RELEASE_READY",
        "CANDIDATE_FROZEN",
        "CANDIDATE_FREEZE",
        "VERSION_CLOSURE",
        "CI_PASS",
        "TASK_PR_PASS",
        "REVIEW_PASS",
        "VALIDATION_PASS",
        "V01_PASS",
        "MACHINE_CONFORMANCE_PASS",
        "MODEL_VOTE_MAJORITY",
        "SCHEDULER_ACTIVITY",
        "CONTROLLER_STATE",
    }
)
MINIMUM_INPUT_IDS = frozenset(
    {
        "ACC-R1", "ACC-R2", "ACC-R3", "ACC-R4", "ACC-R6", "ACC-R7", "ACC-R11", "ACC-R12",
        "GATE-19-2", "BLOCKERS-19-3", "OWNER-CONVERGENCE", "R11-CONTRADICTION", "R12-LINEAGE",
    }
)
BINDING_CLASSES = frozenset({"CANDIDATE_BOUND", "DURABLE_STATIC", "EVENT_BOUND"})
CURRENTNESS_VALUES = frozenset({"CURRENT", "HISTORICAL"})
MACHINERY_KEY_TOKENS = ("environment", "scheduler", "compatibility_group", "admission_generation", "dispatch_lane")
EMBEDDING_KEYS = frozenset({"content", "body", "embedded_text", "copy", "excerpt", "verbatim_body"})
FORBIDDEN_VALUE_FIELDS = frozenset(
    {"default_value", "derived_value", "auto_value", "computed_value", "inferred_value"}
)
SUPERSESSION_REWRITE_KEYS = frozenset({"erases", "rewrites", "rewrites_history", "deletes_prior", "replaces_history"})
FIRST_RECORD = "NONE_FOR_FIRST_RECORD"
PLACEHOLDER_MARK = "TO_BE_RECORDED_BY_PRODUCT_AUTHORITY_ONLY"
RECORDING_RULE_PHRASES = (
    "only after the authorized product-authority act exists as durable fact",
    "never pre-fill, default, or infer the value",
)
RECORD_ID_RE = re.compile(r"^PDR-[A-Za-z0-9.\-]+$")
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(Z|[+-]\d{2}:\d{2})$")
PATH_LIKE_RE = re.compile(r"^[A-Za-z0-9_./\-]+\.(md|py|json|yaml)$")
DECIDED_TOKEN_RE = re.compile(r"\b(YES|NO)\b")

# T07B candidate write set (registered successor candidate; see the disclosed
# carried-guard rebind of scripts/test_v410_owner_convergence.py).
T07B_ALLOWED_PREFIXES = (
    ".agent/execution/V410-T07B-R1/",
    "templates/product-decision-record.md",
    "references/PRODUCT_DECISION_RECORD_REFERENCE.md",
    "checklists/version-closure.md",
    "scripts/test_v410_t07b_decision_record.py",
    "scripts/test_v410_owner_convergence.py",  # pre-authorized TASK_CANDIDATES registry rebind
)
FORBIDDEN_SURFACES = (
    "schemas/",
    "standards/",
    "scripts/v34_rules.py",
    "scripts/verify_standard.py",
    "templates/agent-event-comment.md",
    "templates/GOLDEN_INDEX.md",
    "references/V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md",
    "standard-manifest.json",
    T07A_INDEX_REL,
    "scripts/test_v410_t07a_acceptance_projection.py",
)


def parse_template_record() -> dict:
    """Extract the template's single fenced JSON skeleton; fail closed on drift."""
    text = TEMPLATE.read_text(encoding="utf-8")
    if text.count("```json") != 1:
        raise AssertionError("template must embed exactly one json record skeleton block")
    start = text.index("```json") + len("```json")
    end = text.index("```", start)
    return json.loads(text[start:end])


def git_blob_at_head(rel: str) -> str | None:
    result = subprocess.run(
        ["git", "rev-parse", f"HEAD:{rel}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def _norm(value: object) -> str:
    return re.sub(r"\s+", " ", str(value)).strip().lower()


# ---------------------------------------------------------------------------
# Record-model validator (real-record mode). Shared by the positive cases and
# every authority-negative mutant; the machine layer checks CONFORMANCE only.
# ---------------------------------------------------------------------------


def _delegation_problems(actor: dict) -> list[str]:
    problems: list[str] = []
    role = actor.get("actor_role")
    delegation = actor.get("delegation")
    if role == DELEGATED_ROLE:
        if not isinstance(delegation, dict):
            problems.append("delegated actor_authority lacks a durable delegation fact")
            return problems
        if not str(delegation.get("delegation_ref", "")).strip():
            problems.append("delegation fact missing delegation_ref")
        grantor = delegation.get("grantor")
        if grantor != OWNER_ROLE:
            problems.append(
                "delegation grantor is not the human Product authority owner; "
                "delegation chains cannot launder authority"
            )
        if not str(delegation.get("bounded_scope", "")).strip():
            problems.append("delegation fact missing its bounded scope")
    return problems


def record_problems(record: object) -> list[str]:
    """Fail-closed validator for a FILLED decision record (synthetic or real)."""
    problems: list[str] = []
    if not isinstance(record, dict):
        return ["record is not an object"]
    if record.get("record_schema") != SCHEMA:
        problems.append(f"invalid record_schema {record.get('record_schema')!r}")
    for key in record:
        if key in FORBIDDEN_VALUE_FIELDS:
            problems.append(f"forbidden auto-value field present: {key}")
        if key != "evidence_inputs" and any(tok in key.lower() for tok in MACHINERY_KEY_TOKENS):
            problems.append(f"machinery fact used outside evidence_inputs: {key}")
        if key == "authority_selection":
            problems.append("authority_selection is not a record field: machinery facts never select authority")

    identity = record.get("decision_identity")
    if not isinstance(identity, dict):
        problems.append("decision_identity missing")
    else:
        if RECORD_ID_RE.match(str(identity.get("record_id", ""))) is None:
            problems.append(f"invalid record_id {identity.get('record_id')!r}")
        if identity.get("decision_key") != DECISION_KEY:
            problems.append(f"decision_key must be {DECISION_KEY}")
        subject = identity.get("subject")
        if not isinstance(subject, dict):
            problems.append("decision_identity.subject missing")
        else:
            if "/" not in str(subject.get("repository", "")):
                problems.append("subject.repository must name owner/repository")
            if not str(subject.get("version", "")).strip():
                problems.append("subject.version missing")
            for field in ("candidate_sha", "candidate_tree"):
                if SHA_RE.match(str(subject.get(field, ""))) is None:
                    problems.append(f"subject.{field} must bind the exact 40-hex candidate identity")

    actor = record.get("actor_authority")
    if not isinstance(actor, dict):
        problems.append("actor_authority missing")
    else:
        if not str(actor.get("actor", "")).strip():
            problems.append("actor_authority.actor missing")
        role = actor.get("actor_role")
        if role in FORBIDDEN_ACTOR_ROLES:
            problems.append(f"implementation/machinery role self-authorization rejected: {role!r}")
        elif role not in AUTHORITY_ROLES:
            problems.append(f"invalid actor_role {role!r}")
        basis = str(actor.get("authority_basis", ""))
        if not basis.strip():
            problems.append("actor_authority.authority_basis missing")
        normalized_basis = re.sub(r"[^A-Z0-9]+", "_", basis.upper())
        for token in AUTO_VALUE_SOURCES:
            if token in normalized_basis:
                problems.append(
                    f"authority basis cites machine/cross-layer result {token}; such facts are "
                    "evidence inputs only and can never be the authority basis"
                )
        if not str(actor.get("authority_act_ref", "")).strip():
            problems.append(
                "recording rule violated: authority_act_ref missing — no record may exist "
                "without the authorized Product-authority act as durable fact"
            )
        if not str(actor.get("authority_owner_ref", "")).strip():
            problems.append("actor_authority.authority_owner_ref missing")
        for key in actor:
            if any(tok in str(key).lower() for tok in MACHINERY_KEY_TOKENS):
                problems.append(f"machinery fact inside actor_authority: {key}")
        problems.extend(_delegation_problems(actor))

    inputs = record.get("evidence_inputs")
    if not isinstance(inputs, list) or not inputs:
        problems.append("evidence_inputs must be a non-empty list of refs")
        inputs = []
    seen_ids: set[str] = set()
    for entry in inputs:
        if not isinstance(entry, dict):
            problems.append("evidence input is not an object")
            continue
        for emb in EMBEDDING_KEYS:
            if emb in entry:
                problems.append(f"evidence input embeds content ({emb}); inputs are refs, NEVER copies")
        input_id = str(entry.get("input_id", ""))
        if input_id not in MINIMUM_INPUT_IDS:
            problems.append(f"invalid evidence input_id {input_id!r}")
        if input_id in seen_ids:
            problems.append(f"duplicate evidence input_id {input_id!r} (multi-lane evidence counts once)")
        seen_ids.add(input_id)
        ref = str(entry.get("durable_ref", ""))
        if not ref.strip():
            problems.append(f"evidence input {input_id!r} lacks a durable_ref")
        elif PATH_LIKE_RE.match(ref) and not (ROOT / ref).is_file():
            problems.append(f"evidence ref path missing at checkout: {ref}")
        if entry.get("subject_binding") not in BINDING_CLASSES:
            problems.append(f"evidence input {input_id!r} has invalid subject_binding")
        if entry.get("currentness_at_decided_at") not in CURRENTNESS_VALUES:
            problems.append(f"evidence input {input_id!r} lacks currentness_at_decided_at")
        if not str(entry.get("ref_identity", "")).strip():
            problems.append(f"evidence input {input_id!r} lacks ref_identity (blob or event id)")
        if entry.get("subject_binding") == "CANDIDATE_BOUND":
            bound = entry.get("bound_subject")
            subject = (record.get("decision_identity") or {}).get("subject") or {}
            if not isinstance(bound, dict) or SHA_RE.match(str(bound.get("candidate_sha", ""))) is None:
                problems.append(f"CANDIDATE_BOUND evidence input {input_id!r} lacks a bound exact subject")
            elif (
                bound.get("candidate_sha") != subject.get("candidate_sha")
                or bound.get("candidate_tree") != subject.get("candidate_tree")
            ):
                problems.append(
                    f"stale binding: evidence input {input_id!r} is bound to a different exact "
                    "subject; a materially changed successor subject requires explicit "
                    "supersession via a new record on the successor subject"
                )

    value = record.get("decision_value")
    if "value_source" in record:
        source = str(record.get("value_source", ""))
        if _norm(source) != "product_authority_act":
            problems.append(
                f"value_source must be the authorized Product-authority act; machine/cross-layer "
                f"results can never produce the value: {source!r}"
            )
    if value not in OUTCOME_VALUES:
        problems.append(f"decision_value must be exactly one of the two legal outcome values; got {value!r}")
    else:
        if value == "YES":
            missing = sorted(MINIMUM_INPUT_IDS - seen_ids)
            if missing:
                problems.append(
                    f"insufficient evidence for the affirmative outcome; missing minimum inputs "
                    f"{missing}; fails closed — legal dispositions: evidence-backed negative "
                    "outcome with blocking refs, or BLOCKED_TO_PRODUCT_AUTHORITY"
                )
            stale = [
                e.get("input_id")
                for e in inputs
                if e.get("currentness_at_decided_at") != "CURRENT"
            ]
            if stale:
                problems.append(
                    f"stale/historical evidence cannot satisfy a current input: {sorted(stale)}"
                )
        else:  # the evidence-backed negative outcome: legal, but MUST name blocking refs
            blocking = record.get("blocking_evidence_refs")
            if not isinstance(blocking, list) or not blocking or not all(
                str(ref).strip() for ref in blocking
            ):
                problems.append(
                    "the evidence-backed negative outcome MUST name blocking_evidence_refs"
                )

    if not str(record.get("rationale_and_limitations", "")).strip():
        problems.append("rationale_and_limitations missing")
    if ISO_RE.match(str(record.get("decided_at", ""))) is None:
        problems.append("decided_at must be an ISO-8601 timestamp of the authorized act")
    if not str(record.get("publication_ref", "")).strip():
        problems.append("publication_ref missing (durable GitHub publication of the record)")

    supersession = record.get("supersession")
    if not isinstance(supersession, dict):
        problems.append("supersession missing")
    else:
        for key in supersession:
            if key in SUPERSESSION_REWRITE_KEYS or any(tok in str(key).lower() for tok in ("erase", "rewrite", "delete")):
                problems.append(f"supersession carries history-rewrite semantics: {key}")
        prior = supersession.get("supersedes_record_id")
        if not str(prior or "").strip():
            problems.append("supersession.supersedes_record_id missing")
        elif prior != FIRST_RECORD and not str(supersession.get("prior_record_ref", "")).strip():
            problems.append("superseding record lacks prior_record_ref (append-only lineage)")
        rule = _norm(supersession.get("supersession_rule", ""))
        if "append-only" not in rule:
            problems.append("supersession_rule must state the append-only history rule")

    rule_field = _norm(record.get("recording_rule", ""))
    for phrase in RECORDING_RULE_PHRASES:
        if phrase not in rule_field:
            problems.append(f"recording_rule field must restate the binding rule verbatim-level: {phrase!r}")
    return problems


def skeleton_problems(record: object) -> list[str]:
    """Fail-closed validator for the UNFILLED template skeleton."""
    problems: list[str] = []
    if not isinstance(record, dict):
        return ["skeleton is not an object"]
    if record.get("record_schema") != SCHEMA:
        problems.append("skeleton record_schema drift")
    identity = record.get("decision_identity") or {}
    if identity.get("decision_key") != DECISION_KEY:
        problems.append("skeleton decision_key drift")
    if "TO_BE_FILLED" not in str((identity.get("record_id", ""))):
        problems.append("skeleton record_id must stay a fill-in placeholder")
    subject = identity.get("subject") or {}
    for field in ("repository", "version", "candidate_sha", "candidate_tree"):
        if "TO_BE_FILLED" not in str(subject.get(field, "")):
            problems.append(f"skeleton subject.{field} must stay a fill-in placeholder")
    actor = record.get("actor_authority") or {}
    for field in ("actor", "actor_role", "authority_basis", "authority_act_ref"):
        if "TO_BE_FILLED" not in str(actor.get(field, "")):
            problems.append(f"skeleton actor_authority.{field} must stay a fill-in placeholder")
    inputs = record.get("evidence_inputs")
    if not isinstance(inputs, list) or not inputs:
        problems.append("skeleton evidence_inputs missing")
    else:
        entry = inputs[0]
        for field in ("input_id", "durable_ref", "subject_binding", "currentness_at_decided_at", "ref_identity"):
            if field not in entry:
                problems.append(f"skeleton evidence input lacks slot {field}")
    value = str(record.get("decision_value", ""))
    if PLACEHOLDER_MARK not in value:
        problems.append("skeleton decision_value must stay the to-be-filled-by-authority slot")
    if DECIDED_TOKEN_RE.search(value):
        problems.append("skeleton decision_value must not enumerate a decided instance")
    if ISO_RE.match(str(record.get("decided_at", ""))) is not None:
        problems.append("skeleton decided_at must stay a fill-in placeholder")
    if "TO_BE_FILLED" not in str(record.get("publication_ref", "")):
        problems.append("skeleton publication_ref must stay a fill-in placeholder")
    rule_field = _norm(record.get("recording_rule", ""))
    for phrase in RECORDING_RULE_PHRASES:
        if phrase not in rule_field:
            problems.append("skeleton must restate the binding recording rule")
    embedded = json.dumps(record)
    if DECIDED_TOKEN_RE.search(embedded):
        problems.append("skeleton carries a literal decided value token")
    return problems


def valid_record(value: str, **overrides) -> dict:
    """Build a fully conformant synthetic record (test mutant data)."""
    subject = {
        "repository": "kaicreator-mm/ai-development-standard",
        "version": "v4.10.0",
        "candidate_sha": "c0ffeec0ffeec0ffeec0ffeec0ffeec0ffee0042",
        "candidate_tree": "c0ffeec0ffeec0ffeec0ffeec0ffeec0ffee0043",
    }
    anchor = {
        "ACC-R1": (f"{T07A_INDEX_REL}#V410-ACC-R1", "CANDIDATE_BOUND"),
        "ACC-R2": (f"{T07A_INDEX_REL}#V410-ACC-R2", "CANDIDATE_BOUND"),
        "ACC-R3": (f"{T07A_INDEX_REL}#V410-ACC-R3", "CANDIDATE_BOUND"),
        "ACC-R4": (f"{T07A_INDEX_REL}#V410-ACC-R4", "CANDIDATE_BOUND"),
        "ACC-R6": (f"{T07A_INDEX_REL}#V410-ACC-R6", "CANDIDATE_BOUND"),
        "ACC-R7": (f"{T07A_INDEX_REL}#V410-ACC-R7", "CANDIDATE_BOUND"),
        "ACC-R11": (f"{T07A_INDEX_REL}#V410-ACC-R11", "CANDIDATE_BOUND"),
        "ACC-R12": (f"{T07A_INDEX_REL}#V410-ACC-R12", "CANDIDATE_BOUND"),
        "GATE-19-2": ("standards/RELEASE_STANDARD.md section 11 gate-applicability decision records", "DURABLE_STATIC"),
        "BLOCKERS-19-3": (f"{T07A_INDEX_REL}#closure_blocker_inputs", "CANDIDATE_BOUND"),
        "OWNER-CONVERGENCE": ("references/V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md", "CANDIDATE_BOUND"),
        "R11-CONTRADICTION": (f"{T07A_INDEX_REL}#V410-ACC-R11", "CANDIDATE_BOUND"),
        "R12-LINEAGE": (f"{T07A_INDEX_REL}#V410-ACC-R12", "CANDIDATE_BOUND"),
    }
    inputs = []
    for input_id in sorted(MINIMUM_INPUT_IDS):
        ref, binding = anchor[input_id]
        entry = {
            "input_id": input_id,
            "durable_ref": ref,
            "subject_binding": binding,
            "currentness_at_decided_at": "CURRENT",
            "ref_identity": T07A_INDEX_BLOB_AT_BASE if binding == "CANDIDATE_BOUND" else "durable-static-owner",
        }
        if binding == "CANDIDATE_BOUND":
            entry["bound_subject"] = dict(subject)
        inputs.append(entry)
    record = {
        "record_schema": SCHEMA,
        "decision_identity": {"record_id": "PDR-V4.10.0-0001", "decision_key": DECISION_KEY, "subject": subject},
        "actor_authority": {
            "actor": "human-product-authority-owner",
            "actor_role": OWNER_ROLE,
            "authority_basis": "Frozen Product #837 section 1.1 (PRD v0.4 blob b0b9906035eee253aad4bff0274d3d4c8f90b9db)",
            "authority_act_ref": "#9999@1",
            "authority_owner_ref": "docs/implementation/4.10.0/PRODUCT_FREEZE.md (record #837)",
        },
        "evidence_inputs": inputs,
        "decision_value": value,
        "rationale_and_limitations": "synthetic conformance record; limitations noted",
        "decided_at": "2026-10-08T00:00:00Z",
        "publication_ref": "#9999@2",
        "supersession": {
            "supersedes_record_id": FIRST_RECORD,
            "supersession_rule": "append-only; prior records remain historical; a materially changed successor subject requires a successor record",
        },
        "recording_rule": (
            "A controller/actor may RECORD a decision only after the authorized "
            "Product-authority act exists as durable fact — never pre-fill, default, or infer the value."
        ),
    }
    if value == "NO":
        record["blocking_evidence_refs"] = [f"{T07A_INDEX_REL}#V410-ACC-R11 (synthetic blocking ref)"]
    record.update(overrides)
    return record


class TemplateSurfaceTests(unittest.TestCase):
    """The template ships EMPTY: slots only, zero decided values, rules stated."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.skeleton = parse_template_record()
        cls.text = TEMPLATE.read_text(encoding="utf-8")

    def test_template_skeleton_is_conformant_and_empty(self) -> None:
        self.assertEqual(skeleton_problems(self.skeleton), [])

    def test_template_carries_all_eight_field_groups(self) -> None:
        for field in (
            "decision_identity", "actor_authority", "evidence_inputs", "decision_value",
            "rationale_and_limitations", "decided_at", "publication_ref", "supersession",
            "recording_rule", "blocking_evidence_refs",
        ):
            self.assertIn(f'"{field}"', json.dumps(self.skeleton), field)

    def test_template_states_authority_boundary_and_recording_rule(self) -> None:
        for token in (
            "RECORD_SUPPORT_ONLY=true",
            "decision_authority=PRODUCT_AUTHORITY_ONLY",
            "NO_AUTO_YES=true",
            "chains cannot launder authority",
            "BLOCKED_TO_PRODUCT_AUTHORITY",
        ):
            self.assertIn(token, self.text, token)
        lowered = _norm(self.text)
        for phrase in RECORDING_RULE_PHRASES:
            self.assertIn(phrase, lowered, phrase)

    def test_template_names_the_evidence_input_producers(self) -> None:
        self.assertIn(T07A_INDEX_REL, self.text)
        for token in ("19.2", "19.3", "R11", "R12", "owner-convergence"):
            self.assertIn(token, self.text, token)

    def test_template_contains_zero_decided_value_tokens(self) -> None:
        self.assertIsNone(DECIDED_TOKEN_RE.search(self.text), "template must not carry a decided value token")
        self.assertNotIn("decision_value\": \"YES", self.text)
        self.assertNotIn("decision_value\": \"NO", self.text)


class ReferenceAndChecklistSurfaceTests(unittest.TestCase):
    """Decision-path reference + closure checklist row: pointers, no values."""

    def test_reference_authority_header_and_sections(self) -> None:
        text = REFERENCE.read_text(encoding="utf-8")
        for token in (
            "RECORD_SUPPORT_ONLY=true",
            "decision_authority=PRODUCT_AUTHORITY_ONLY",
            "NO_AUTO_YES=true",
            "PRODUCT_DECISION=NONE",
            "ELIGIBILITY_VERDICT=NONE",
            "BLOCKED_TO_PRODUCT_AUTHORITY",
            "delegation chains cannot launder authority",
            "supersession",
            T07A_INDEX_REL,
            T07A_INDEX_BLOB_AT_BASE,
            PRD_FROZEN_BLOB,
            REBIND_BASE_SHA,
        ):
            self.assertIn(token, text, token)

    def test_reference_states_all_seven_no_auto_rules(self) -> None:
        text = REFERENCE.read_text(encoding="utf-8")
        for token in (
            "Release READY", "V01", "vote majority", "default", "successor candidate",
            "self-authorize", "machinery facts",
        ):
            self.assertIn(token, text, token)

    def test_reference_contains_zero_decided_value_tokens(self) -> None:
        self.assertIsNone(DECIDED_TOKEN_RE.search(REFERENCE.read_text(encoding="utf-8")))

    def test_checklist_row_points_at_template_and_reference(self) -> None:
        text = CHECKLIST.read_text(encoding="utf-8")
        self.assertIn("templates/product-decision-record.md", text)
        self.assertIn("references/PRODUCT_DECISION_RECORD_REFERENCE.md", text)
        self.assertIn("ADS_CORE_FEATURE_FREEZE_ELIGIBLE", text)
        self.assertIn("PRD §1.1/§19.4", text)
        self.assertIn("never imply the affirmative outcome", text)
        self.assertIn("no record may exist before the authorized Product-authority act is a durable fact", text)

    def test_frozen_authority_anchors_unchanged(self) -> None:
        self.assertEqual(git_blob_at_head(PRD_REL), PRD_FROZEN_BLOB, "Frozen Product subject drifted; rebind required")
        self.assertEqual(
            git_blob_at_head(T07A_INDEX_REL),
            T07A_INDEX_BLOB_AT_BASE,
            "the T07A acceptance-evidence index drifted from the pinned citation blob; rebind required",
        )


class PositiveConformanceTests(unittest.TestCase):
    """P1-P6 (#863@6013682453): the record path works for the Product authority."""

    def test_p1_owner_affirmative_record_completes(self) -> None:
        record = valid_record("YES")
        self.assertEqual(record_problems(record), [])

    def test_p1_all_eight_field_groups_reconstructible_by_fresh_observer(self) -> None:
        record = valid_record("YES")
        for field in (
            "record_schema", "decision_identity", "actor_authority", "evidence_inputs",
            "decision_value", "rationale_and_limitations", "decided_at", "publication_ref",
            "supersession", "recording_rule",
        ):
            self.assertIn(field, record, field)
        self.assertEqual(record["decision_identity"]["decision_key"], DECISION_KEY)

    def test_p2_negative_outcome_with_blocking_refs_is_legal_and_complete(self) -> None:
        record = valid_record("NO")
        self.assertEqual(record_problems(record), [])
        self.assertTrue(record["blocking_evidence_refs"])

    def test_p2_negative_outcome_without_blocking_refs_is_rejected(self) -> None:
        record = valid_record("NO")
        record["blocking_evidence_refs"] = []
        self.assertTrue(any("blocking_evidence_refs" in p for p in record_problems(record)))

    def test_p3_bounded_delegated_actor_with_durable_delegation_fact(self) -> None:
        record = valid_record(
            "YES",
            actor_authority={
                "actor": "delegated-product-actor",
                "actor_role": DELEGATED_ROLE,
                "authority_basis": "durable delegation fact inside bounded delegatable authority",
                "authority_act_ref": "#9999@3",
                "authority_owner_ref": "docs/implementation/4.10.0/PRODUCT_FREEZE.md (record #837)",
                "delegation": {
                    "delegation_ref": "#9999@4",
                    "grantor": OWNER_ROLE,
                    "bounded_scope": "record the core-feature-freeze eligibility decision for the v4.10.0 exact subject only",
                },
            },
        )
        self.assertEqual(record_problems(record), [])

    def test_p5_supersession_chain_appends_without_rewriting(self) -> None:
        successor = valid_record("YES")
        successor["decision_identity"]["record_id"] = "PDR-V4.10.0-0002"
        successor["supersession"] = {
            "supersedes_record_id": "PDR-V4.10.0-0001",
            "prior_record_ref": "#9999@2",
            "supersession_rule": "append-only; prior records remain historical; a materially changed successor subject requires a successor record",
        }
        self.assertEqual(record_problems(successor), [])

    def test_p5_history_rewrite_semantics_rejected(self) -> None:
        record = valid_record("YES")
        record["supersession"]["erases"] = "prior record"
        self.assertTrue(any("history-rewrite" in p for p in record_problems(record)))
        record2 = valid_record("YES")
        record2["supersession"]["supersedes_record_id"] = "PDR-V4.10.0-0001"
        problems = record_problems(record2)
        self.assertTrue(any("prior_record_ref" in p for p in problems))

    def test_p6_evidence_inputs_are_refs_never_copies(self) -> None:
        record = valid_record("NO")
        record["evidence_inputs"][0]["content"] = "embedded evidence body must be rejected"
        self.assertTrue(any("embeds content" in p for p in record_problems(record)))
        record2 = valid_record("NO")
        record2["evidence_inputs"][0]["durable_ref"] = ""
        self.assertTrue(any("durable_ref" in p for p in record_problems(record2)))


class AuthorityNegativeTests(unittest.TestCase):
    """AUTHORITY_NEGATIVES 1-7 (#863@6040872034): no-auto-YES, fail closed."""

    def test_an1_release_ready_or_candidate_freeze_cannot_be_the_basis(self) -> None:
        for basis in ("Release READY state justifies this outcome", "Candidate Freeze completed so the value follows"):
            record = valid_record("YES")
            record["actor_authority"]["authority_basis"] = basis
            problems = record_problems(record)
            self.assertTrue(
                any("authority basis cites machine/cross-layer result" in p for p in problems),
                basis,
            )
        record = valid_record("YES")
        record["actor_authority"]["authority_basis"] = "RELEASE_READY recorded by the closure controller"
        self.assertTrue(any("RELEASE_READY" in p for p in record_problems(record)))
        record = valid_record("YES")
        record["value_source"] = "CANDIDATE_FROZEN"
        problems = record_problems(record)
        self.assertTrue(any("value_source" in p and "CANDIDATE_FROZEN" in p for p in problems))

    def test_an2_v01_or_validation_pass_cannot_be_the_basis(self) -> None:
        record = valid_record("YES")
        record["actor_authority"]["authority_basis"] = "V01_PASS and Validation PASS evidence"
        self.assertTrue(any("V01_PASS" in p or "VALIDATION_PASS" in p for p in record_problems(record)))

    def test_an3_ci_review_conformance_model_majority_scheduler_cannot_decide(self) -> None:
        for source in ("CI_PASS", "REVIEW_PASS", "MACHINE_CONFORMANCE_PASS", "MODEL_VOTE_MAJORITY", "SCHEDULER_ACTIVITY", "CONTROLLER_STATE"):
            record = valid_record("YES")
            record["value_source"] = source
            self.assertTrue(
                any(source in p for p in record_problems(record)),
                source,
            )

    def test_an4_missing_evidence_never_defaults_to_affirmative(self) -> None:
        record = valid_record("YES")
        record["evidence_inputs"] = []
        problems = record_problems(record)
        self.assertTrue(any("insufficient evidence" in p for p in problems))
        self.assertTrue(any("BLOCKED_TO_PRODUCT_AUTHORITY" in p for p in problems))
        partial = valid_record("YES")
        partial["evidence_inputs"] = [e for e in partial["evidence_inputs"] if e["input_id"] not in {"ACC-R11", "ACC-R12"}]
        self.assertTrue(any("insufficient evidence" in p for p in record_problems(partial)))
        stale = valid_record("YES")
        for entry in stale["evidence_inputs"]:
            if entry["input_id"] == "ACC-R12":
                entry["currentness_at_decided_at"] = "HISTORICAL"
        self.assertTrue(any("stale/historical evidence" in p for p in record_problems(stale)))
        defaulted = valid_record("YES")
        defaulted["default_value"] = "YES"
        self.assertTrue(any("default_value" in p for p in record_problems(defaulted)))

    def test_an5_stale_decision_never_binds_a_changed_successor_subject(self) -> None:
        record = valid_record("YES")
        record["evidence_inputs"][0]["bound_subject"] = {
            "candidate_sha": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            "candidate_tree": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        }
        problems = record_problems(record)
        self.assertTrue(any("stale binding" in p and "supersession" in p for p in problems))

    def test_an6_implementation_roles_cannot_self_authorize(self) -> None:
        for role in ("BUILDER", "VALIDATOR", "REVIEWER", "CONTROLLER", "SCHEDULER"):
            record = valid_record("YES")
            record["actor_authority"]["actor_role"] = role
            self.assertTrue(any("self-authorization rejected" in p for p in record_problems(record)), role)

    def test_an6_delegation_chains_cannot_launder_authority(self) -> None:
        record = valid_record("YES")
        record["actor_authority"] = {
            "actor": "validator-actor",
            "actor_role": DELEGATED_ROLE,
            "authority_basis": "claims delegation",
            "authority_act_ref": "#9999@5",
            "authority_owner_ref": "docs/implementation/4.10.0/PRODUCT_FREEZE.md (record #837)",
            "delegation": {"delegation_ref": "#9999@6", "grantor": "REVIEWER", "bounded_scope": "everything"},
        }
        problems = record_problems(record)
        self.assertTrue(any("cannot launder authority" in p for p in problems))
        record2 = valid_record("YES")
        record2["actor_authority"]["actor_role"] = DELEGATED_ROLE
        problems2 = record_problems(record2)
        self.assertTrue(any("durable delegation fact" in p for p in problems2))

    def test_an7_machinery_facts_never_widen_or_select_authority(self) -> None:
        record = valid_record("YES")
        record["actor_authority"]["compatibility_group"] = "g1"
        self.assertTrue(any("machinery fact inside actor_authority" in p for p in record_problems(record)))
        record2 = valid_record("YES")
        record2["authority_selection"] = "admission_generation=2"
        self.assertTrue(any("authority_selection" in p for p in record_problems(record2)))
        record3 = valid_record("YES")
        record3["execution_environment_widens_authority"] = "LOCAL"
        self.assertTrue(any("machinery fact" in p for p in record_problems(record3)))

    def test_recording_rule_no_record_without_authority_act(self) -> None:
        record = valid_record("YES")
        del record["actor_authority"]["authority_act_ref"]
        self.assertTrue(any("recording rule violated" in p for p in record_problems(record)))
        record2 = valid_record("YES")
        record2["recording_rule"] = "value may be inferred from green gates"
        self.assertTrue(any("recording_rule field" in p for p in record_problems(record2)))


class PackAndCandidateSurfaceTests(unittest.TestCase):
    """Pack inventory, subject binding, disclosed registry rebind, write-set guard."""

    def test_pack_core_inventory_exact_set(self) -> None:
        text = (PACK_DIR / "MANIFEST.yaml").read_text(encoding="utf-8")
        lines = text.splitlines()
        start = lines.index("core_artifacts:")
        items: list[str] = []
        for line in lines[start + 1 :]:
            if not line.startswith("  - "):
                break
            items.append(line[4:].strip())
        self.assertTrue(core_artifacts_complete(items))
        self.assertEqual(set(items), set(REQUIRED_CORE_ARTIFACTS))

    def test_pack_manifest_binds_exact_rebind_subject_and_authority_boundary(self) -> None:
        text = (PACK_DIR / "MANIFEST.yaml").read_text(encoding="utf-8")
        self.assertIn(f"base_sha: {REBIND_BASE_SHA}", text)
        self.assertIn(f"base_tree: {REBIND_BASE_TREE}", text)
        self.assertIn("task_id: V410-T07B", text)
        self.assertIn("V410-T07A@cea2e0ccd045e8fcebaf110273129b198ed259fd INTEGRATED", text)
        self.assertIn("F1_BOUNDED_IMPLEMENTATION", text)
        boundary = " ".join(text.splitlines())
        self.assertIn("SUPPORTS but NEVER MAKES the ADS_CORE_FEATURE_FREEZE_ELIGIBLE decision", boundary)
        self.assertIn("PRODUCT_DECISION=NONE", boundary)
        self.assertIn("ELIGIBILITY_VERDICT=NONE", boundary)
        lowered = _norm(text)
        self.assertIn("never pre-fill, default, or infer the value", lowered)

    def test_contract_states_authority_boundary_verbatim(self) -> None:
        text = (PACK_DIR / "EXECUTION_CONTRACT.md").read_text(encoding="utf-8")
        lowered = _norm(text)
        self.assertIn("supports but never makes the", lowered)
        self.assertIn("ads_core_feature_freeze_eligible` decision", lowered)
        self.assertIn("product_decision=none", lowered)
        self.assertIn("eligibility_verdict=none` for this entire chain", lowered)
        for phrase in RECORDING_RULE_PHRASES:
            self.assertIn(phrase, lowered, phrase)

    def test_disclosed_carried_guard_rebind_is_registered(self) -> None:
        import test_v410_owner_convergence as oc  # carried suite, import-safe

        entries = oc.CandidateShapeTests.TASK_CANDIDATES
        active = [entry["task"] for entry in entries if entry.get("active")]
        self.assertEqual(active, ["V410-T07B"], "exactly one active candidate: the T07B registry entry")
        entry = next(e for e in entries if e["task"] == "V410-T07B")
        self.assertEqual(entry["base"], REBIND_BASE_SHA)
        for prefix in T07B_ALLOWED_PREFIXES:
            self.assertTrue(
                any(p.startswith(tuple(entry["prefixes"])) for p in [prefix]),
                f"T07B registered prefixes must cover {prefix}",
            )
        t07a = next(e for e in entries if e["task"] == "V410-T07A")
        self.assertNotIn("active", t07a)  # flag moved, entry and frozen r1_tip retained
        self.assertIn("r1_tip", t07a)

    def test_t07b_candidate_diff_stays_inside_registered_prefixes(self) -> None:
        result = subprocess.run(
            ["git", "diff", "--name-only", f"{REBIND_BASE_SHA}...HEAD", "--"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            self.fail(f"cannot diff against {REBIND_BASE_SHA}...HEAD: {result.stderr.strip()}")
        changed = {line.strip() for line in result.stdout.splitlines() if line.strip()}
        outside = sorted(p for p in changed if not p.startswith(T07B_ALLOWED_PREFIXES))
        self.assertEqual(outside, [], "T07B candidate paths must stay inside the registered prefixes")
        offenders = sorted(set(changed) & set(FORBIDDEN_SURFACES))
        self.assertEqual(offenders, [], "T06B-owned / T07A deliverable / authority surfaces must stay untouched")

    def test_deliverable_files_present(self) -> None:
        for path in (
            TEMPLATE,
            REFERENCE,
            CHECKLIST,
            PACK_DIR / "MANIFEST.yaml",
            PACK_DIR / "EXECUTION_CONTRACT.md",
            PACK_DIR / "TEST_MATRIX.yaml",
            PACK_DIR / "FAILURE_MATRIX.yaml",
            PACK_DIR / "IMPLEMENTATION_MAP.md",
            PACK_DIR / "REVIEW_CHECKLIST.md",
        ):
            self.assertTrue(path.is_file(), path)

    def test_pack_surfaces_declare_no_decision_made(self) -> None:
        # Decided-instance patterns only: house-identifier compounds (DISP-NO-*)
        # and the two verbatim frozen task-pack quotes in EXECUTION_CONTRACT.md
        # are vocabulary/identifiers, never decided instances.
        instance_patterns = (
            re.compile(r'"decision_value"\s*:\s*"(YES|NO)"'),
            re.compile(r"ELIGIBILITY_VERDICT=(YES|NO)\b"),
            re.compile(r'"decision_value"\s*:\s*"(YES|NO)\s'),
        )
        for rel in ("TEST_MATRIX.yaml", "FAILURE_MATRIX.yaml", "IMPLEMENTATION_MAP.md", "REVIEW_CHECKLIST.md"):
            text = (PACK_DIR / rel).read_text(encoding="utf-8")
            scrubbed = re.sub(r"DISP-[A-Z0-9\-]+", "", text)
            for pattern in instance_patterns:
                self.assertIsNone(pattern.search(scrubbed), f"{rel} must not carry a decided instance")
            self.assertIsNone(
                DECIDED_TOKEN_RE.search(scrubbed),
                f"{rel} must not carry a decided value token",
            )


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
