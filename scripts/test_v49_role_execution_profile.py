from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path

from test_protocol_schemas import assert_supported_schema, load_schema, validate_subset

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = load_schema("role-execution-profile-v1.schema.json")
FIXTURE_DIR = ROOT / "fixtures" / "role-execution-profile-v1"
SOURCE_DIR = FIXTURE_DIR / "sources"
REFERENCE = ROOT / "references" / "ROLE_EXECUTION_PROFILE_V1_REFERENCE.md"
L2 = ROOT / "docs" / "implementation" / "4.9.0" / "L2_ARCHITECTURE_EVIDENCE.md"
EXECUTION_CONTRACT = ROOT / ".agent" / "execution" / "T-004" / "EXECUTION_CONTRACT.md"

BASE_SHA = "df94641e6082dc7a2988e73eafdffd3bf42668b9"
PACK_HEAD_SHA = "f20e485f73df1bfb01826e5c341c8340c068172a"
FROZEN_L2_BLOB = "bd41ea0175b459a6a490fd37ad579e429a58a1c3"

READ_ONLY_OWNER_PATHS = (
    "schemas/agent-capability-profile-v1.schema.json",
    "schemas/agent-capability-evidence-v1.schema.json",
    "docs/implementation/4.9.0/PRD.md",
    "docs/implementation/4.9.0/L3_REFERENCE_PACKS.md",
    "docs/implementation/4.9.0/L2_ARCHITECTURE_EVIDENCE.md",
    "docs/implementation/4.9.0/task-packs/T04_role_execution_profile.md",
)

# T-011 re-binds (CF-V49-02 #745@5992918366; classification #831@5994177360):
# - standards/EXECUTION_ARCHITECTURE_STANDARD.md: pre-existing stale pin — the
#   surface carries the T-007 section 29 append (blob 019d4df7@df94641e ->
#   ffe4788b, unchanged through BASE/pack/HEAD; absent from the T-008 write set);
# - schemas/dispatch.schema.json: the T-008 DAG-owned surface, legally mutated
#   after BASE_SHA (optional assurance_currentness_ref / role_profile_ref /
#   jit_phase_ref additions; 4607f6cb@BASE -> 7259cb35, per
#   references/EXECUTION_CONTRACT_REFS_V49_COMPATIBILITY.json).
# Both stale "unchanged since BASE_SHA" pins are re-bound to exact
# current-blob identity pins; pin constants only — any further mutation of
# either surface still fails, zero other assertion change.
#
# v4.10 integration value re-bind (claim #779@6084794791 / pre-merge
# #779@6084805500; merge commit e0315b2a): at the integrated tree the standard
# carries the v4.10 additions composed with the v4.9 section (renumbered §29 by
# the disclosed composition rebind), and the dispatch schema composes the v4.10
# additive optional fields (EXECUTION_ARCHITECTURE_STANDARD §11.1.1 "(v4.10,
# additive)" / §28) on top of the v4.9-line extension. Both pins are re-bound to
# their exact integrated blobs; pin constants only — any further mutation of
# either surface still fails, zero other assertion change.
READ_ONLY_OWNER_PATHS_REBOUND_BLOBS = {
    "standards/EXECUTION_ARCHITECTURE_STANDARD.md": "5588d2196677b1b4878563de65edf2beaa10178f",
    # Post-recovery recompose re-bind (#805 POST_RECOVERY_EXACT_RECOMPOSE,
    # #745): the recovery-integrated main merge (4c632256) legally carries the
    # recovered v4.6 dispatch wiring (+2 optional array fields) composed into
    # the same DAG-owned dispatch surface; the pin now names the exact
    # integrated blob (see the v4.10 re-bind above). Pin constant only — any
    # further mutation still fails, zero other assertion change.
    "schemas/dispatch.schema.json": "90bea62524beb0215d5f40cf0be9986786648fec",
    # T-03 re-bind (#1008/#1033): the owner-local acceptance/currentness
    # clauses on this branch legally extend the ICGS surface; the stale
    # "unmutated since BASE_SHA" pin moves to this exact integrated-blob
    # identity pin — pin constants only, any further mutation still fails.
    "standards/INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md": "15e355f6ec86370599f2dda7b61963d93fead66f",
}

PLANNING_PATHS = tuple(
    f".agent/execution/T-004/{name}"
    for name in (
        "MANIFEST.yaml",
        "EXECUTION_CONTRACT.md",
        "IMPLEMENTATION_MAP.md",
        "TEST_MATRIX.yaml",
        "FAILURE_MATRIX.yaml",
        "REVIEW_CHECKLIST.md",
    )
)

# Deterministic owner-ref grammar: <family>:<path>#<anchor>
REF_RE = re.compile(r"^([a-z][a-z0-9-]*):([A-Za-z0-9_./-]+)#([A-Za-z0-9._-]+)$")

# Owner-family policy: which refs may occupy normative authority positions.
# Every entry is an existing, read-only v4.8/v4.9 owner surface at the candidate.
CLAIM_POLICY_OWNER_REFS = {
    ("std/EXECUTION_ARCHITECTURE_STANDARD.md", "11"),
    ("std/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md", "12.1"),
}
ELIGIBILITY_OWNER_REFS = {("std/EXECUTION_ARCHITECTURE_STANDARD.md", "27.2")}
TERMINAL_AUTHORITY_OWNER_REFS = {
    ("std/EXECUTION_ARCHITECTURE_STANDARD.md", "7"),
    ("std/EXECUTION_ARCHITECTURE_STANDARD.md", "11"),
    ("std/EXECUTION_ARCHITECTURE_STANDARD.md", "12"),
    ("std/GITHUB_WORK_ITEM_CONTRACT_STANDARD.md", "12.1"),
}
INDEPENDENCE_OWNER_PATHS = {"std/ASSURANCE_PLAN_STANDARD.md"}
INDEPENDENCE_OWNER_SCHEMAS = {"schema/assurance-plan-v2.schema.json"}
EVIDENCE_OWNER_SCHEMAS = {"schema/agent-capability-evidence-v1.schema.json"}

LIFECYCLE_FIELDS = (
    "dispatch_state",
    "claim_state",
    "lifecycle_state",
    "workflow_state",
    "work_item_state",
    "dispatch_id",
)
AUTHORITY_INJECTION_FIELDS = (
    "granted_role_actions",
    "terminal_authority_grant",
    "capability_proof",
    "provider_model_provenance",
    "provider_authority",
    "model_routing_authority",
    "claim_switch",
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_profile(name: str) -> dict:
    return load_json(FIXTURE_DIR / name)


def git_object_sha(rev: str, rel_path: str) -> str:
    result = subprocess.run(
        ["git", "rev-parse", f"{rev}:{rel_path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def heading_exists(text: str, anchor: str) -> bool:
    parts = anchor.split(".")
    hashes = "#" * (1 + len(parts))
    prefixes = (f"{hashes} {anchor}.", f"{hashes} {anchor} ", f"{hashes} {anchor}\t")
    lines = text.splitlines()
    return any(line.startswith(prefixes) or line.strip() == f"{hashes} {anchor}" for line in lines)


def parse_ref(ref: str) -> tuple[str, str, str] | None:
    match = REF_RE.match(ref)
    if match is None:
        return None
    return match.group(1), match.group(2), match.group(3)


def resolve_ref(ref: str) -> tuple[str, str]:
    """Resolve one owner ref against the repository, read-only. Fail closed."""
    parsed = parse_ref(ref)
    if parsed is None:
        return "UNRESOLVED", f"ref does not match owner-ref grammar: {ref!r}"
    family, path, anchor = parsed
    if family == "ads":
        if path.startswith("std/") and path.endswith(".md"):
            file_path = ROOT / "standards" / path.removeprefix("std/")
            if not file_path.is_file():
                return "UNRESOLVED", f"standards surface missing: {path}"
            if not heading_exists(file_path.read_text(encoding="utf-8"), anchor):
                return "UNRESOLVED", f"anchor #{anchor} not found in {path}"
            return "RESOLVED", f"{path}#{anchor}"
        if path.startswith("schema/") and path.endswith(".json"):
            file_path = ROOT / "schemas" / path.removeprefix("schema/")
            if not file_path.is_file():
                return "UNRESOLVED", f"schema surface missing: {path}"
            properties = load_json(file_path).get("properties", {})
            if anchor not in properties:
                return "UNRESOLVED", f"property #{anchor} not found in {path}"
            return "RESOLVED", f"{path}#{anchor}"
        return "UNRESOLVED", f"unknown ads surface: {path}"
    if family == "fixture" and path.startswith("source-authority/"):
        file_path = SOURCE_DIR / path.removeprefix("source-authority/")
        if not file_path.is_file():
            return "UNRESOLVED", f"source-authority snapshot missing: {path}"
        status = load_json(file_path).get("status")
        if status == "CURRENT":
            return "RESOLVED", f"{path}#{anchor}"
        if status in {"RETIRED", "SUPERSEDED", "STALE"}:
            return "STALE", f"source-authority snapshot stale ({status}): {path}"
        return "UNRESOLVED", f"unknown snapshot status: {status}"
    return "UNRESOLVED", f"unknown ref family: {ref!r}"


def evaluate_requirements(requirements: list[dict]) -> dict:
    """Conflict semantics over normalized requirement sets. Order-independent."""
    merged: dict[str, str] = {}
    conflicts: list[str] = []
    for reqs in requirements:
        for key, value in reqs.items():
            if key in merged and merged[key] != value:
                conflicts.append(key)
            merged.setdefault(key, value)
    if conflicts:
        return {
            "posture": "BLOCKED_SOURCE_AUTHORITY_CONFLICT",
            "conflict_keys": sorted(set(conflicts)),
            "projected_requirements": None,
        }
    return {
        "posture": "PROJECTED",
        "conflict_keys": [],
        "projected_requirements": dict(sorted(merged.items())),
    }


def evaluate_profile(profile: dict) -> dict:
    """Deterministic fail-closed resolver. Never returns a permissive default."""
    reasons: list[str] = []
    projection = profile["source_authority_projection"]
    declared = projection["projection_state"]
    conflict_refs = projection.get("conflict_refs", [])
    unresolved_refs = projection.get("unresolved_refs", [])

    if declared == "PROJECTED" and (conflict_refs or unresolved_refs):
        return {
            "posture": "REJECTED_LYING_PROJECTION",
            "declared": declared,
            "projected_requirements": None,
            "reasons": ["PROJECTED declared while conflict_refs/unresolved_refs are non-empty"],
        }

    statuses = {ref: resolve_ref(ref) for ref in profile["source_authority_refs"]}
    stale_refs = [ref for ref, (status, _) in statuses.items() if status == "STALE"]
    missing_refs = [ref for ref, (status, _) in statuses.items() if status == "UNRESOLVED"]
    reasons.extend(statuses[ref][1] for ref in stale_refs + missing_refs)

    requirements = []
    for ref, (status, _) in statuses.items():
        parsed = parse_ref(ref)
        if status == "RESOLVED" and parsed and parsed[0] == "fixture":
            requirements.append(
                load_json(SOURCE_DIR / parsed[1].removeprefix("source-authority/"))["normalized_requirements"]
            )
    derived = evaluate_requirements(requirements)
    if derived["posture"] == "BLOCKED_SOURCE_AUTHORITY_CONFLICT":
        posture = "BLOCKED_SOURCE_AUTHORITY_CONFLICT"
    elif missing_refs:
        posture = "BLOCKED_SOURCE_REF_UNRESOLVED"
    elif stale_refs:
        posture = "WAITING_LINEAGE"
    else:
        posture = "PROJECTED"

    if declared == "PROJECTED" and posture != "PROJECTED":
        return {
            "posture": "REJECTED_LAST_WRITER_WINS",
            "declared": declared,
            "derived": posture,
            "projected_requirements": None,
            "reasons": reasons + [f"declared PROJECTED but sources derive {posture}"],
        }
    blocked_aliases = {"BLOCKED_SOURCE_REF_UNRESOLVED", "WAITING_LINEAGE"}
    declared_consistent = declared == posture or (declared in blocked_aliases and posture in blocked_aliases)
    if not declared_consistent:
        reasons.append(f"declared {declared} but sources derive {posture}")

    # Owner-family policy: normative authority positions must point INTO owners.
    def ref_matches(ref: str, owners: set[tuple[str, str]]) -> bool:
        parsed = parse_ref(ref)
        return parsed is not None and parsed[0] == "ads" and (parsed[1], parsed[2]) in owners

    claim_ref = profile["claim_policy_ref"]
    if not ref_matches(claim_ref, CLAIM_POLICY_OWNER_REFS) or resolve_ref(claim_ref)[0] != "RESOLVED":
        reasons.append(f"claim_policy_ref does not resolve into the v4.8 Claim-rule owner: {claim_ref}")
    for ref in profile["eligibility_predicate_refs"]:
        if not ref_matches(ref, ELIGIBILITY_OWNER_REFS) or resolve_ref(ref)[0] != "RESOLVED":
            reasons.append(f"eligibility ref does not point into the v4.8 hard-eligibility owner: {ref}")
    if not ref_matches(profile["terminal_authority_ref"], TERMINAL_AUTHORITY_OWNER_REFS):
        reasons.append(f"terminal_authority_ref is not an execution/work-item owner surface: {profile['terminal_authority_ref']}")
    for ref in profile.get("independence_requirement_refs", []):
        parsed = parse_ref(ref)
        allowed = (
            parsed is not None
            and parsed[0] == "ads"
            and (parsed[1] in INDEPENDENCE_OWNER_PATHS or parsed[1] in INDEPENDENCE_OWNER_SCHEMAS)
        )
        if not allowed or resolve_ref(ref)[0] != "RESOLVED":
            reasons.append(f"independence ref is not an Assurance Plan/Task/Gate owner: {ref}")
    for ref in profile.get("required_evidence_refs", []):
        parsed = parse_ref(ref)
        if parsed is None or parsed[1] not in EVIDENCE_OWNER_SCHEMAS or resolve_ref(ref)[0] != "RESOLVED":
            reasons.append(f"required_evidence_ref does not resolve into an evidence owner: {ref}")

    if any(reason.startswith(("claim_policy_ref", "eligibility ref", "terminal_authority_ref", "independence ref", "required_evidence_ref")) for reason in reasons):
        posture = "REJECTED_OVER_CLAIM"
    elif declared != "PROJECTED" and not declared_consistent:
        posture = "REJECTED_INCONSISTENT_PROJECTION"

    return {
        "posture": posture,
        "declared": declared,
        "derived": posture if posture in {"BLOCKED_SOURCE_AUTHORITY_CONFLICT", "BLOCKED_SOURCE_REF_UNRESOLVED", "WAITING_LINEAGE", "PROJECTED"} else None,
        "projected_requirements": derived["projected_requirements"] if posture == "PROJECTED" else None,
        "reasons": reasons,
    }


class RoleExecutionProfileSchemaTests(unittest.TestCase):
    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        cls.reference = REFERENCE.read_text(encoding="utf-8")
        cls.l2 = L2.read_text(encoding="utf-8")
        cls.execution_contract = EXECUTION_CONTRACT.read_text(encoding="utf-8")

    # ---------- P01: schema conformance; the only new default machine family ----------

    def test_schema_uses_repository_supported_subset(self) -> None:
        assert_supported_schema(SCHEMA)

    def test_machine_family_identity_is_role_execution_profile_v1(self) -> None:
        self.assertEqual(SCHEMA["properties"]["schema_version"]["const"], "ai-dev/role-execution-profile-v1")
        self.assertIn("Role Execution Profile v1", SCHEMA["title"])
        self.assertIn("Role Execution Profile v1 — the only new default machine family", self.l2)
        self.assertIn("`Role Execution Profile v1` is the ONLY new default machine family", self.execution_contract)

    def test_valid_profile_instances_validate(self) -> None:
        for name in ("valid_builder_profile.json", "valid_validator_profile.json"):
            with self.subTest(fixture=name):
                self.assertEqual(validate_subset(load_profile(name), SCHEMA), [])

    def test_schema_invalid_instances_reject(self) -> None:
        base = load_profile("valid_builder_profile.json")
        cases = {
            "missing_required_field": {k: v for k, v in base.items() if k != "claim_policy_ref"},
            "bad_schema_version": dict(base, schema_version="ai-dev/agent-capability-profile-v1"),
            "bad_mutation_class": dict(base, mutation_class="WHENEVER_CONVENIENT"),
            "bad_role_case": dict(base, role="Builder"),
            "empty_eligibility_refs": dict(base, eligibility_predicate_refs=[]),
            "empty_source_authority_refs": dict(base, source_authority_refs=[]),
            "free_claim_switch_value": dict(base, claim_policy_ref="NOT_REQUIRED"),
            "unanchored_owner_ref": dict(base, terminal_authority_ref="ads:std/EXECUTION_ARCHITECTURE_STANDARD.md"),
        }
        for label, value in cases.items():
            with self.subTest(case=label):
                self.assertTrue(validate_subset(value, SCHEMA))

    def test_projected_state_cannot_carry_conflict_or_unresolved_refs(self) -> None:
        value = load_profile("source_authority_conflict_profile.json")
        value["source_authority_projection"]["projection_state"] = "PROJECTED"
        self.assertTrue(validate_subset(value, SCHEMA))
        value2 = load_profile("missing_source_ref_profile.json")
        value2["source_authority_projection"]["projection_state"] = "PROJECTED"
        self.assertTrue(validate_subset(value2, SCHEMA))

    # ---------- P02: source-authority conflict => BLOCKED, never last-writer-wins ----------

    def test_conflicting_source_authorities_produce_blocked_not_last_writer_wins(self) -> None:
        profile = load_profile("source_authority_conflict_profile.json")
        self.assertEqual(validate_subset(profile, SCHEMA), [])
        result = evaluate_profile(profile)
        self.assertEqual(result["posture"], "BLOCKED_SOURCE_AUTHORITY_CONFLICT")
        self.assertIsNone(result["projected_requirements"])
        self.assertEqual(
            SCHEMA["properties"]["source_authority_projection"]["properties"]["resolution_policy"]["const"],
            "source-authorities-prevail-never-last-writer-wins",
        )

    def test_conflict_resolution_is_reference_order_independent(self) -> None:
        profile = load_profile("source_authority_conflict_profile.json")
        reversed_profile = json.loads(json.dumps(profile))
        reversed_profile["source_authority_refs"] = list(reversed(profile["source_authority_refs"]))
        reversed_profile["source_authority_projection"]["conflict_refs"] = list(
            reversed(profile["source_authority_projection"]["conflict_refs"])
        )
        first = evaluate_profile(profile)
        second = evaluate_profile(reversed_profile)
        self.assertEqual(first["posture"], "BLOCKED_SOURCE_AUTHORITY_CONFLICT")
        self.assertEqual(second["posture"], "BLOCKED_SOURCE_AUTHORITY_CONFLICT")
        self.assertEqual(first, second)

    def test_last_writer_wins_claim_is_rejected_fail_closed(self) -> None:
        profile = load_profile("last_writer_wins_reject_profile.json")
        self.assertEqual(validate_subset(profile, SCHEMA), [])
        result = evaluate_profile(profile)
        self.assertEqual(result["posture"], "REJECTED_LAST_WRITER_WINS")
        self.assertIsNone(result["projected_requirements"])

    def test_requirement_sets_conflict_semantics(self) -> None:
        agree = load_json(SOURCE_DIR / "task_requirements_authority_agreeing.json")["normalized_requirements"]
        conflict = load_json(SOURCE_DIR / "task_requirements_authority_conflicting.json")["normalized_requirements"]
        self.assertEqual(evaluate_requirements([agree])["posture"], "PROJECTED")
        blocked = evaluate_requirements([agree, conflict])
        self.assertEqual(blocked["posture"], "BLOCKED_SOURCE_AUTHORITY_CONFLICT")
        self.assertEqual(blocked["conflict_keys"], ["max_agent_freedom"])
        self.assertEqual(evaluate_requirements([conflict, agree]), blocked)

    # ---------- P03: no role actions / terminal authority derived from documents ----------

    def test_injected_authority_fields_are_rejected(self) -> None:
        base = load_profile("valid_builder_profile.json")
        for field in AUTHORITY_INJECTION_FIELDS:
            with self.subTest(field=field):
                value = dict(base)
                value[field] = {"granted": True} if field == "capability_proof" else "AUTHORIZED"
                self.assertTrue(validate_subset(value, SCHEMA))
        self.assertTrue(validate_subset(load_profile("injected_authority_fields.json"), SCHEMA))

    def test_capability_family_cannot_occupy_terminal_authority_position(self) -> None:
        profile = load_profile("over_claim_refs_profile.json")
        self.assertEqual(validate_subset(profile, SCHEMA), [])
        result = evaluate_profile(profile)
        self.assertEqual(result["posture"], "REJECTED_OVER_CLAIM")
        self.assertTrue(
            any("terminal_authority_ref" in reason for reason in result["reasons"]),
            result["reasons"],
        )
        self.assertIsNone(result["projected_requirements"])

    def test_profile_cannot_mutate_owner_surfaces_it_references(self) -> None:
        for phrase in (
            "Source authorities prevail; the profile never overrides them",
            "It does not create a second lifecycle, scheduler, claim authority, workflow state, independence authority, or capability owner",
        ):
            self.assertIn(phrase, self.reference)

    # ---------- P04: provider/model identity cannot become normative role authority ----------

    def test_provider_model_identity_fields_do_not_exist_in_schema(self) -> None:
        for field in ("provider_model_provenance", "provider_authority", "model_routing_authority", "provider_routing"):
            with self.subTest(field=field):
                self.assertNotIn(field, SCHEMA["properties"])

    def test_provider_swap_is_authority_inert(self) -> None:
        base = load_json(SOURCE_DIR / "task_requirements_authority_agreeing.json")
        swapped = json.loads(json.dumps(base))
        swapped["provider_model_provenance"] = "provider-model:other/entirely-different-model"
        first = evaluate_requirements([base["normalized_requirements"]])
        second = evaluate_requirements([swapped["normalized_requirements"]])
        self.assertEqual(first, second)
        self.assertEqual(first["posture"], "PROJECTED")

    def test_provider_identity_cannot_override_role_requirements(self) -> None:
        base = load_json(SOURCE_DIR / "task_requirements_authority_agreeing.json")
        provider_override = json.loads(json.dumps(base))
        provider_override["normalized_requirements"] = dict(
            base["normalized_requirements"], max_agent_freedom="F3_ARCHITECTURE_REQUIRED"
        )
        result = evaluate_requirements([base["normalized_requirements"], provider_override["normalized_requirements"]])
        self.assertEqual(result["posture"], "BLOCKED_SOURCE_AUTHORITY_CONFLICT")
        self.assertIn("provider/model identity", self.reference)
        self.assertIn("MODEL_USAGE_POLICY", self.reference)

    # ---------- P05: claim_policy_ref and eligibility refs resolve into v4.8 owners ----------

    def test_claim_policy_ref_resolves_into_existing_claim_rules(self) -> None:
        for name in ("valid_builder_profile.json", "valid_validator_profile.json"):
            profile = load_profile(name)
            with self.subTest(fixture=name):
                ref = profile["claim_policy_ref"]
                self.assertIn((parse_ref(ref)[1], parse_ref(ref)[2]), CLAIM_POLICY_OWNER_REFS)
                status, detail = resolve_ref(ref)
                self.assertEqual(status, "RESOLVED", detail)
        self.assertIn("atomic Claim admission rules", self.reference)
        self.assertIn("GITHUB_WORK_ITEM_CONTRACT_STANDARD.md", self.reference)

    def test_unresolvable_or_wrong_family_claim_policy_ref_rejects(self) -> None:
        profile = load_profile("over_claim_refs_profile.json")
        result = evaluate_profile(profile)
        self.assertTrue(
            any("claim_policy_ref" in reason for reason in result["reasons"]),
            result["reasons"],
        )
        status, _ = resolve_ref("fixture:claim-switch/free-switch#not-required")
        self.assertEqual(status, "UNRESOLVED")

    def test_eligibility_refs_point_into_v48_hard_eligibility_owner(self) -> None:
        for name in ("valid_builder_profile.json", "valid_validator_profile.json"):
            profile = load_profile(name)
            for ref in profile["eligibility_predicate_refs"]:
                with self.subTest(fixture=name, ref=ref):
                    self.assertIn((parse_ref(ref)[1], parse_ref(ref)[2]), ELIGIBILITY_OWNER_REFS)
                    self.assertEqual(resolve_ref(ref)[0], "RESOLVED")
        status, _ = resolve_ref("ads:std/EXECUTION_ARCHITECTURE_STANDARD.md#27.2")
        self.assertEqual(status, "RESOLVED")
        self.assertIn("Hard filters before ranking", self.reference)
        self.assertIn("eligibility_predicate_refs[]", self.reference)

    def test_eligibility_owner_is_reference_not_copied_inventory(self) -> None:
        self.assertIn("never copies owner inventories", self.reference)
        self.assertIn("additional hard predicates", self.reference)
        self.assertIn("no `REQUIRED|NOT_REQUIRED|INHERIT` switch", self.reference)

    # ---------- P06: stale/missing source refs fail closed, never permissive ----------

    def test_stale_source_ref_fails_closed_as_waiting_lineage(self) -> None:
        profile = load_profile("stale_source_ref_profile.json")
        self.assertEqual(validate_subset(profile, SCHEMA), [])
        result = evaluate_profile(profile)
        self.assertEqual(result["posture"], "WAITING_LINEAGE")
        self.assertIsNone(result["projected_requirements"])

    def test_missing_source_ref_fails_closed(self) -> None:
        profile = load_profile("missing_source_ref_profile.json")
        self.assertEqual(validate_subset(profile, SCHEMA), [])
        result = evaluate_profile(profile)
        self.assertEqual(result["posture"], "BLOCKED_SOURCE_REF_UNRESOLVED")
        self.assertIsNone(result["projected_requirements"])
        self.assertEqual(resolve_ref("ads:std/NOT_A_REAL_STANDARD.md#1")[0], "UNRESOLVED")

    def test_stale_snapshot_never_contributes_requirements(self) -> None:
        retired = load_json(SOURCE_DIR / "retired_requirements_authority.json")
        self.assertEqual(retired["status"], "RETIRED")
        self.assertEqual(resolve_ref("fixture:source-authority/retired_requirements_authority.json#current")[0], "STALE")
        self.assertIn("permissive default", self.reference)

    def test_lying_projection_is_rejected(self) -> None:
        profile = load_profile("missing_source_ref_profile.json")
        profile["source_authority_projection"] = {
            "projection_state": "PROJECTED",
            "resolution_policy": "source-authorities-prevail-never-last-writer-wins",
        }
        self.assertEqual(validate_subset(profile, SCHEMA), [])
        result = evaluate_profile(profile)
        self.assertEqual(result["posture"], "REJECTED_LAST_WRITER_WINS")

    # ---------- P07: profile presence cannot prove executor capability ----------

    def test_capability_profile_instance_is_not_a_role_profile(self) -> None:
        capability = load_profile("capability_profile_as_role_profile.json")
        capability_schema = load_schema("agent-capability-profile-v1.schema.json")
        self.assertEqual(validate_subset(capability, capability_schema), [])
        self.assertTrue(validate_subset(capability, SCHEMA))

    def test_no_capability_proof_semantics_in_profile_family(self) -> None:
        self.assertNotIn("capability_proof", SCHEMA["properties"])
        for name in ("valid_builder_profile.json", "valid_validator_profile.json"):
            profile = load_profile(name)
            result = evaluate_profile(profile)
            with self.subTest(fixture=name):
                for key in result:
                    self.assertNotIn("capab", key)
                self.assertIn(result["posture"], {"PROJECTED", "BLOCKED_SOURCE_AUTHORITY_CONFLICT", "BLOCKED_SOURCE_REF_UNRESOLVED", "WAITING_LINEAGE"})

    def test_evidence_stays_external_in_evidence_owner_family(self) -> None:
        for name in ("valid_builder_profile.json", "valid_validator_profile.json"):
            profile = load_profile(name)
            for ref in profile["required_evidence_refs"]:
                with self.subTest(fixture=name, ref=ref):
                    parsed = parse_ref(ref)
                    self.assertIn(parsed[1], EVIDENCE_OWNER_SCHEMAS)
                    self.assertEqual(resolve_ref(ref)[0], "RESOLVED")
        self.assertIn("capability stays in v4.8 evidence owner", self.reference)

    # ---------- P08: no second lifecycle; read-only owner surfaces unmutated ----------

    def test_no_lifecycle_or_workflow_state_fields(self) -> None:
        for field in LIFECYCLE_FIELDS:
            with self.subTest(field=field):
                self.assertNotIn(field, SCHEMA["properties"])
                value = load_profile("valid_builder_profile.json")
                value[field] = "CLAIMED"
                self.assertTrue(validate_subset(value, SCHEMA))

    def test_read_only_owner_surfaces_unmutated_since_base(self) -> None:
        for rel_path in READ_ONLY_OWNER_PATHS:
            with self.subTest(path=rel_path):
                self.assertEqual(
                    git_object_sha(BASE_SHA, rel_path),
                    git_object_sha("HEAD", rel_path),
                )
        # T-011 re-bind: the T-007-appended execution architecture surface and
        # the T-008-mutated dispatch surface are pinned to their exact current
        # blobs (see READ_ONLY_OWNER_PATHS_REBOUND_BLOBS provenance).
        for rel_path, pinned_blob in READ_ONLY_OWNER_PATHS_REBOUND_BLOBS.items():
            with self.subTest(path_rebound=rel_path):
                self.assertEqual(pinned_blob, git_object_sha("HEAD", rel_path))
        self.assertEqual(git_object_sha(BASE_SHA, "docs/implementation/4.9.0/L2_ARCHITECTURE_EVIDENCE.md"), FROZEN_L2_BLOB)

    def test_immutable_planning_files_unmutated_since_pack_head(self) -> None:
        for rel_path in PLANNING_PATHS:
            with self.subTest(path=rel_path):
                self.assertEqual(
                    git_object_sha(PACK_HEAD_SHA, rel_path),
                    git_object_sha("HEAD", rel_path),
                )

    def test_reference_documents_owner_ref_table_and_fail_closed_rules(self) -> None:
        self.assertIn("Owner-reference table", self.reference)
        self.assertIn("27.2", self.reference)
        self.assertIn("12.1", self.reference)
        for phrase in ("BLOCKED_SOURCE_AUTHORITY_CONFLICT", "last-writer-wins", "WAITING_LINEAGE", "never compatible by assertion"):
            self.assertIn(phrase, self.reference)


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(RoleExecutionProfileSchemaTests)
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
