from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
V46 = ROOT / "docs" / "implementation" / "4.6.0"
SCHEMAS = ROOT / "schemas"
PACK_DIR = ROOT / ".agent" / "execution" / "_legacy" / "v4.6" / "T-008"

PRD = V46 / "PRD.md"
L2 = V46 / "L2_ARCHITECTURE_EVIDENCE.md"
L3 = V46 / "L3_REFERENCE_PACKS.md"
T08_TASK_PACK = V46 / "task-packs" / "T08_cross_standard_conformance.md"
CLOSURE_INPUTS = V46 / "CLOSURE_INPUTS.md"
UPSTREAM = V46 / "UPSTREAM_OWNER_CURRENTNESS.md"
MIGRATION = V46 / "MIGRATION_ADOPTION.md"
DOGFOOD = V46 / "dogfood"
PACKET = DOGFOOD / "session_operator_handoff_packet.json"
DOGFOOD_README = DOGFOOD / "README.md"
REFERENCE = ROOT / "references" / "AI_NATIVE_EXISTING_OWNER_INTEGRATION.md"
INTENT_STD = ROOT / "standards" / "INTENT_ASSUMPTION_GOVERNANCE_STANDARD.md"
CONTEXT_STD = ROOT / "standards" / "CONTEXT_ENGINEERING_STANDARD.md"
SKILL_STD = ROOT / "standards" / "SKILL_PROCEDURE_GOVERNANCE_STANDARD.md"

# Exact-base identity bound by .agent/execution/T-008 (T08 Execution Contract).
BOUND_BASE_SHA = "a4c5fffe6bab178dcb74b5f47afcda4aa0047c27"
BOUND_BASE_TREE = "6ae5e1a8b33a6127ecc2e94b6db45e0ca6fa30ea"
T08_TASK_PACK_BLOB = "248abb5c468240e702f383b003a93a6f503e4cfa"
L3_BLOB = "c219344d8b902bc5053adbdc2328a3147af8f7bf"
T06_MERGE = "72ea246263b052879833456a33e65e8e9056ab4c"
T07_MERGE = "a4c5fffe6bab178dcb74b5f47afcda4aa0047c27"
PACK_HEAD = "4b15205bcb591acd2eb7928b096ed9adf42a1e9d"
PACK_TREE = "99cb2f8ac2090b6e0e549e6ade7828134c30ff8b"
PACK_ARTIFACTS = {
    "EXECUTION_CONTRACT.md",
    "FAILURE_MATRIX.yaml",
    "IMPLEMENTATION_MAP.md",
    "MANIFEST.yaml",
    "REVIEW_CHECKLIST.md",
    "TEST_MATRIX.yaml",
}

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def canonical_bytes(path: Path) -> bytes:
    """Byte-faithful canonical content: LF-normalized so identity checks are
    host-checkout independent (CRLF materialization must not change identity)."""
    return path.read_bytes().replace(b"\r\n", b"\n")


def git_blob_sha(path: Path) -> str:
    content = canonical_bytes(path)
    return hashlib.sha1(b"blob %d\x00" % len(content) + content).hexdigest()


def sha256_of(path: Path) -> str:
    return hashlib.sha256(canonical_bytes(path)).hexdigest()


def load_text(path: Path) -> str:
    return canonical_bytes(path).decode("utf-8")


# Frozen Product PRD §11 forbidden inferences (exact durable lines).
PRD_FORBIDDEN = [
    "user chat -> Frozen Product automatically",
    "Agent interpretation -> user-stated fact",
    "ASSUMPTION/UNKNOWN -> durable requirement without authority",
    "historical chat/memory -> override current Git/GitHub/Frozen authority",
    "larger context dump -> higher context quality automatically",
    "external resource/tool output -> Product truth automatically",
    "tool capability -> side-effect authority",
    "Skill installed -> Skill trusted / action authorized",
    "Skill instruction -> override Frozen Product/Architecture/Task",
    "model capability -> F3 authority",
    "same GitHub account -> same logical operator/context",
    "AI-generated code compiles -> intent/domain correctness",
    "AI-authored change -> mandatory human review universally",
    "recorded model/provider -> independence automatically proven",
    "Fast Path label -> required gates waived",
]

# Frozen L2 §13 adversarial negatives (exact durable lines). The union with
# PRD §11 adds the ephemeral-only handoff truth item.
L2_FORBIDDEN = [
    "chat -> Frozen Product",
    "interpretation -> user fact",
    "assumption/unknown -> durable requirement",
    "ephemeral-only truth -> acceptable handoff",
    "historical memory -> override current Git authority",
    "large context dump -> higher quality automatically",
    "Skill installed -> trusted/authorized",
    "Skill tool capability -> side-effect authority",
    "Skill instruction -> override Task/Product authority",
    "model strength -> F3 authority",
    "same transport account -> same logical independent operator",
    "AI code compiles -> intent/domain correctness",
    "model metadata present -> independence automatically proven",
    "Fast Path -> required truth/gate waiver",
]

# Integrated forbidden-inference union (Execution Contract FI-01..FI-16):
# each item must stay guarded by its owning durable authority surfaces.
FI_UNION_GUARDS = [
    ("FI-01", [("PRD", "user chat -> Frozen Product automatically"),
               ("INTENT_STD", "Even an authentic user statement is not automatically Frozen Product.")]),
    ("FI-02", [("PRD", "Agent interpretation -> user-stated fact"),
               ("INTENT_STD", "Never relabel interpretation as the user's own words.")]),
    ("FI-03", [("PRD", "ASSUMPTION/UNKNOWN -> durable requirement without authority"),
               ("INTENT_STD", "MUST NOT self-promote into durable Product/Architecture/Task truth"),
               ("MIGRATION", "`PROMOTE_BY_OWNER` is not proof of promotion.")]),
    ("FI-04", [("L2", "ephemeral-only truth -> acceptable handoff"),
               ("CONTEXT_STD", "No required development truth may exist only in an ephemeral Agent/chat/session context."),
               ("MIGRATION", "Required development truth must be durable outside the current chat/session.")]),
    ("FI-05", [("PRD", "historical chat/memory -> override current Git/GitHub/Frozen authority"),
               ("CONTEXT_STD", "Historical chat or memory may help discovery, but it cannot override current durable authority."),
               ("MIGRATION", "Do not retrofit historical evidence.")]),
    ("FI-06", [("PRD", "larger context dump -> higher context quality automatically"),
               ("CONTEXT_STD", "Context selection is an authority/currentness problem, not a prompt-size maximization problem.")]),
    ("FI-07", [("PRD", "external resource/tool output -> Product truth automatically"),
               ("L2", "record missing evidence; do not infer Product truth")]),
    ("FI-08", [("PRD", "tool capability -> side-effect authority"),
               ("SKILL_STD", "allowed tool capability != side-effect authorization"),
               ("REFERENCE", "does not grant F3, mutation, merge or side-effect authority")]),
    ("FI-09", [("PRD", "Skill installed -> Skill trusted / action authorized"),
               ("SKILL_STD", "`installed != trusted`"),
               ("SKILL_STD", "A genuinely non-applicable Skill requires no empty machine record")]),
    ("FI-10", [("PRD", "Skill instruction -> override Frozen Product/Architecture/Task"),
               ("SKILL_STD", "MUST NOT be followed merely because the Skill is installed.")]),
    ("FI-11", [("PRD", "model capability -> F3 authority"),
               ("REFERENCE", "A stronger model does not self-promote a task to F3")]),
    ("FI-12", [("PRD", "same GitHub account -> same logical operator/context"),
               ("REFERENCE", "Same transport identity is not the same concept as logical operator/context identity"),
               ("PACKET", "same GitHub/API transport account => same logical operator/context")]),
    ("FI-13", [("PRD", "AI-generated code compiles -> intent/domain correctness")]),
    ("FI-14", [("PRD", "AI-authored change -> mandatory human review universally"),
               ("REFERENCE", "AI-authored change | human review universally mandatory")]),
    ("FI-15", [("PRD", "recorded model/provider -> independence automatically proven"),
               ("REFERENCE", "provider/model recorded != independence proven"),
               ("PACKET", "different provider/model metadata => independence proven")]),
    ("FI-16", [("PRD", "Fast Path label -> required gates waived"),
               ("L2", "Fast Path -> required truth/gate waiver"),
               ("MIGRATION", "Reduce ceremony, not truth.")]),
]

TEXTS: dict[str, str] = {}


def text_of(key: str) -> str:
    return TEXTS[key]


def flat(text: str) -> str:
    """Whitespace-insensitive view for long prose guards that may be
    line-wrapped inside markdown documents."""
    return " ".join(text.split())


class CrossStandardConformanceTests(unittest.TestCase):
    """T08 integrated conformance: durable, deterministic, fail-closed."""

    maxDiff = None

    @classmethod
    def setUpClass(cls) -> None:
        TEXTS["PRD"] = load_text(PRD)
        TEXTS["L2"] = load_text(L2)
        TEXTS["L3"] = load_text(L3)
        TEXTS["T08_TASK_PACK"] = load_text(T08_TASK_PACK)
        TEXTS["CLOSURE_INPUTS"] = load_text(CLOSURE_INPUTS)
        TEXTS["UPSTREAM"] = load_text(UPSTREAM)
        TEXTS["MIGRATION"] = load_text(MIGRATION)
        TEXTS["DOGFOOD_README"] = load_text(DOGFOOD_README)
        TEXTS["REFERENCE"] = load_text(REFERENCE)
        TEXTS["INTENT_STD"] = load_text(INTENT_STD)
        TEXTS["CONTEXT_STD"] = load_text(CONTEXT_STD)
        TEXTS["SKILL_STD"] = load_text(SKILL_STD)
        TEXTS["PACKET"] = canonical_bytes(PACKET).decode("utf-8")
        TEXTS["EXECUTION_CONTRACT"] = load_text(PACK_DIR / "EXECUTION_CONTRACT.md")
        TEXTS["MANIFEST"] = load_text(PACK_DIR / "MANIFEST.yaml")
        cls.packet = json.loads(canonical_bytes(PACKET).decode("utf-8"))

    # -------------------------------------------------------------
    # Group 1: authority currentness (durable identity facts)
    # -------------------------------------------------------------

    def test_bound_t08_task_pack_identity_is_unchanged(self) -> None:
        self.assertEqual(git_blob_sha(T08_TASK_PACK), T08_TASK_PACK_BLOB)
        self.assertIn(f"TASK_PACK_BLOB={T08_TASK_PACK_BLOB}", text_of("EXECUTION_CONTRACT"))

    def test_bound_l3_identity_is_unchanged(self) -> None:
        self.assertEqual(git_blob_sha(L3), L3_BLOB)
        self.assertIn(f"L3_BLOB={L3_BLOB}", text_of("EXECUTION_CONTRACT"))

    def test_execution_pack_binds_exact_integration_base(self) -> None:
        contract = text_of("EXECUTION_CONTRACT")
        self.assertIn(f"BASE_SHA={BOUND_BASE_SHA}", contract)
        self.assertIn(f"BASE_TREE={BOUND_BASE_TREE}", contract)
        self.assertIn(f"T06_MERGE={T06_MERGE}", contract)
        self.assertIn(f"T07_MERGE={T07_MERGE}", contract)

    def test_execution_pack_is_current_with_six_core_artifacts(self) -> None:
        self.assertEqual({p.name for p in PACK_DIR.iterdir() if p.is_file()}, PACK_ARTIFACTS)
        manifest = text_of("MANIFEST")
        self.assertIn('pack_state_at_generation: "PACK_CURRENT"', manifest)
        self.assertIn("drift_policy: \"STOP/CONTROLLER_REBIND_REQUIRED\"", manifest)

    def test_pack_head_is_the_implementation_starting_identity(self) -> None:
        ledger = text_of("CLOSURE_INPUTS")
        self.assertIn(f"PACK_HEAD={PACK_HEAD}", ledger)
        self.assertIn(f"PACK_TREE={PACK_TREE}", ledger)

    # -------------------------------------------------------------
    # Group 2: forbidden-inference union (Product §11 + L2 §13)
    # -------------------------------------------------------------

    def test_product_section11_lists_full_forbidden_inference_block(self) -> None:
        for line in PRD_FORBIDDEN:
            self.assertIn(line, text_of("PRD"))

    def test_l2_section13_lists_full_adversarial_negative_block(self) -> None:
        for line in L2_FORBIDDEN:
            self.assertIn(line, text_of("L2"))

    def test_integrated_forbidden_inference_union_is_guarded_by_owners(self) -> None:
        missing: list[str] = []
        for fi_id, guards in FI_UNION_GUARDS:
            for surface, fragment in guards:
                if fragment not in text_of(surface):
                    missing.append(f"{fi_id}: {surface} missing {fragment!r}")
        self.assertEqual(missing, [])

    def test_ephemeral_only_handoff_truth_is_union_addition_and_guarded(self) -> None:
        self.assertNotIn("ephemeral-only truth -> acceptable handoff", text_of("PRD"))
        self.assertIn("ephemeral-only truth -> acceptable handoff", text_of("L2"))
        self.assertIn("Material assumptions, decisions, blockers, exact identities and handoff state must be durable", text_of("CONTEXT_STD"))

    def test_required_truth_cannot_depend_on_hidden_session_context(self) -> None:
        self.assertIn("required truth cannot depend on hidden chat/session context", text_of("PRD"))

    # -------------------------------------------------------------
    # Group 3: owner separation (v4.1–v4.5 + existing cross-version owners)
    # -------------------------------------------------------------

    def test_exactly_three_new_v46_normative_owners_are_declared(self) -> None:
        upstream = text_of("UPSTREAM")
        for owner in (
            "1. Intent & Assumption Governance",
            "2. Context Engineering",
            "3. Skill / Reusable Agent Procedure Governance",
        ):
            self.assertIn(owner, upstream)

    def test_v41_to_v45_owner_boundaries_remain_named_and_unchallenged(self) -> None:
        upstream = text_of("UPSTREAM")
        boundaries = [
            ("Git/worktree/toolchain/config/secret/artifact/external execution", "v4.1 owners"),
            ("interface compatibility/migration", "v4.2 owners"),
            ("Architecture/Task decomposition/live DAG/profile mapping", "v4.3 owners"),
            ("Build/Artifact/Distribution/Deployment", "v4.4 owners"),
            ("runtime observation/incident/maintenance", "v4.5 owners"),
        ]
        for domain, owner in boundaries:
            self.assertIn(domain, upstream)
            self.assertIn(owner, upstream)

    def test_existing_cross_version_owners_are_referenced_not_recreated(self) -> None:
        upstream = text_of("UPSTREAM")
        for marker in (
            "F0–F3 autonomy/escalation",
            "Assurance/Independent Review/model diversity/provenance",
            "Dispatch/Handoff/recovery",
            "exact Validation truth",
            "Release truth",
        ):
            self.assertIn(marker, upstream)
        self.assertIn(
            "MUST NOT be recreated as v4.6 parallel state/object families",
            upstream,
        )

    def test_f0_f3_stays_the_single_autonomy_vocabulary(self) -> None:
        expected = [
            "F0_MECHANICAL",
            "F1_BOUNDED_IMPLEMENTATION",
            "F2_ENGINEERING_DISCRETION",
            "F3_ARCHITECTURE_REQUIRED",
        ]
        dispatch = json.loads(canonical_bytes(SCHEMAS / "dispatch.schema.json").decode("utf-8"))
        pack = json.loads(canonical_bytes(SCHEMAS / "execution-pack-manifest.schema.json").decode("utf-8"))
        self.assertEqual(dispatch["properties"]["agent_freedom"]["enum"], expected)
        self.assertEqual(pack["properties"]["agent_freedom"]["enum"], expected)
        self.assertIn("Execution Pack / Dispatch/Task authority decides applicability", text_of("REFERENCE"))

    def test_no_parallel_machine_state_families_are_created(self) -> None:
        schema_names = {p.name for p in SCHEMAS.glob("*.schema.json")}
        self.assertIn("intent-assumption-record-v1.schema.json", schema_names)
        self.assertIn("skill-metadata-v1.schema.json", schema_names)
        for forbidden in (
            "context-snapshot-v1.schema.json",
            "ai-assurance-result-v1.schema.json",
            "ai-agent-lifecycle-v1.schema.json",
            "ai-validation-result-v1.schema.json",
            "ai-release-v1.schema.json",
            "intent-assumption-record-v2.schema.json",
        ):
            self.assertNotIn(forbidden, schema_names)

    def test_validation_and_release_stay_exact_subject_downstream_owners(self) -> None:
        self.assertIn("No new AI-native PASS/READY state is introduced", text_of("REFERENCE"))
        self.assertIn("Review aggregation may reference validation results but cannot manufacture them", text_of("REFERENCE"))
        self.assertIn("no AI-native PASS state", text_of("MIGRATION"))
        self.assertIn("no AI-native READY state", text_of("MIGRATION"))
        self.assertIn(
            "reuse of existing Dispatch, Execution Pack, Assurance, Review, Validation and authority chains",
            text_of("L2"),
        )

    def test_dispatch_remains_the_executable_handoff_owner(self) -> None:
        dispatch = json.loads(canonical_bytes(SCHEMAS / "dispatch.schema.json").decode("utf-8"))
        for field in ("role", "execution_profile", "expected_base_sha", "pinned_standard_revision", "agent_freedom"):
            self.assertIn(field, dispatch["required"])
        self.assertIn("do not replace Task/Dispatch authority", text_of("MIGRATION"))
        self.assertIn("refs grant mutation authority", text_of("REFERENCE"))

    # -------------------------------------------------------------
    # Group 4: historical compatibility (no retrofit / additive only)
    # -------------------------------------------------------------

    def test_historical_evidence_keeps_original_identity_and_result(self) -> None:
        migration = text_of("MIGRATION")
        self.assertIn("Do not retrofit historical evidence.", migration)
        self.assertIn("keep their original subject identity, schema/version and result", migration)
        self.assertIn("must not relabel old evidence or manufacture currentness", migration)

    def test_absence_of_v46_records_in_historical_evidence_remains_valid(self) -> None:
        self.assertIn(
            "historical events/reviews are not retroactively required to contain Skill/Intent records",
            text_of("L2"),
        )
        self.assertIn(
            "Adopting v4.6 does not mean they were produced under Intent/Assumption or Skill metadata contracts",
            text_of("MIGRATION"),
        )

    def test_no_historical_chat_is_promoted_to_authority(self) -> None:
        self.assertIn(
            "no historical chat is promoted to authority merely because v4.6 exists",
            text_of("L2"),
        )
        self.assertIn("X overrides current durable owner/currentness", text_of("CONTEXT_STD"))

    def test_release_is_additive_non_weakening_and_v47_routing_is_explicit(self) -> None:
        prd = text_of("PRD")
        self.assertIn("Target: additive/non-weakening v4 minor release.", prd)
        self.assertIn("routed to v4.7/future-major migration planning", prd)
        self.assertIn("no guessed successor", text_of("L2"))

    # -------------------------------------------------------------
    # Group 5: Fast Path proportionality (reduce ceremony, not truth)
    # -------------------------------------------------------------

    def test_fast_path_principle_is_reduce_ceremony_not_truth(self) -> None:
        self.assertIn("Reduce ceremony, not truth.", text_of("PRD"))
        self.assertIn("Reduce ceremony, not truth.", text_of("MIGRATION"))

    def test_non_material_work_requires_no_empty_records(self) -> None:
        migration = text_of("MIGRATION")
        self.assertIn("does **not** require empty Intent/Assumption or Skill records", migration)
        self.assertIn(
            "When no durable machine record is materially needed, do not create an empty record merely to satisfy ceremony.",
            migration,
        )

    def test_fast_path_preserves_required_authority_and_gates(self) -> None:
        migration = text_of("MIGRATION")
        for gate in (
            "applicable scope/authority;",
            "exact subject identity/currentness;",
            "material unresolved intent/assumption/conflict;",
            "required Validation or Review;",
            "Candidate/Release/Repository Integration separation;",
            "applicable side-effect authority.",
        ):
            self.assertIn(gate, migration)
        self.assertIn(
            "Fast Path never bypasses a required current Task/side-effect gate.",
            text_of("SKILL_STD"),
        )

    def test_agents_cannot_self_label_work_to_bypass_gates(self) -> None:
        self.assertIn("to bypass Frozen or required gates.", text_of("PRD"))

    def test_low_adoption_level_is_not_low_risk_evidence(self) -> None:
        self.assertIn(
            "A low A0/A1 adoption level or absence of AI-native records is not evidence that work is low risk.",
            text_of("MIGRATION"),
        )

    # -------------------------------------------------------------
    # Group 6: T06 dogfood fidelity (claim/evidence dimensions stay distinct)
    # -------------------------------------------------------------

    def test_t06_canonical_packet_digest_binding_is_exact(self) -> None:
        digest = sha256_of(PACKET)
        self.assertTrue(SHA256_RE.fullmatch(digest))
        self.assertEqual(digest, "33f9c9aad5d28d58e73af52326bc8bffb61a0eb4e44cb9ff49ce16b19ba6f46b")
        self.assertIn(
            "SHA-256: `33f9c9aad5d28d58e73af52326bc8bffb61a0eb4e44cb9ff49ce16b19ba6f46b`",
            text_of("DOGFOOD_README"),
        )

    def test_t06_static_fixture_claim_stays_distinct_from_real_runtime(self) -> None:
        self.assertEqual(self.packet["claim_scope"]["fixture_claim"], "STATIC_FIXTURE_ONLY")
        readme = text_of("DOGFOOD_README")
        self.assertIn("| packet completeness/reconstruction shape | `STATIC_FIXTURE_PASS`", readme)
        self.assertIn("| real fresh external Agent/runtime reconstruction | `NOT_RUN` |", readme)
        self.assertIn(
            "No fixture/static result in this directory may be relabeled as a real-runtime PASS.",
            readme,
        )

    def test_t06_packet_does_not_prove_dimensions_it_did_not_execute(self) -> None:
        does_not_prove = set(self.packet["claim_scope"]["does_not_prove"])
        for claim in (
            "REAL_EXTERNAL_AGENT_RUNTIME_PASS",
            "REAL_MODEL_OR_PROVIDER_INDEPENDENCE",
            "FRESH_TRANSPORT_ACCOUNT",
            "EXACT_SUBJECT_VALIDATION_PASS",
            "FRESH_INDEPENDENT_REVIEW_PASS",
            "VERSION_CLOSURE_OR_RELEASE_PASS",
            "MERGE_AUTHORITY",
        ):
            self.assertIn(claim, does_not_prove)

    def test_t06_unexecuted_dimensions_stay_not_run(self) -> None:
        findings = {f["id"]: f["status"] for f in self.packet["findings_blockers"]}
        self.assertEqual(findings.get("real-fresh-agent-validation"), "NOT_RUN")
        ledger = text_of("CLOSURE_INPUTS")
        self.assertIn("MODEL_PROVIDER_INDEPENDENCE_SWEEP=NOT_RUN", ledger)
        self.assertIn("FRESH_TRANSPORT_ACCOUNT_DIMENSION=NOT_RUN", ledger)
        self.assertIn("PRODUCTION_SIDE_EFFECTS=NOT_RUN", ledger)

    def test_t06_transport_and_provider_metadata_remain_non_probative(self) -> None:
        forbidden = set(self.packet["forbidden_assumptions"])
        self.assertIn("same GitHub/API transport account => same logical operator/context", forbidden)
        self.assertIn("different provider/model metadata => independence proven", forbidden)
        self.assertIn("fixture/static PASS => real external Agent/runtime PASS", forbidden)
        self.assertIn("same GitHub/API account != same logical operator/context", text_of("DOGFOOD_README"))

    def test_closure_inputs_preserve_t06_executed_fresh_reconstruction_as_distinct_pass(self) -> None:
        ledger = text_of("CLOSURE_INPUTS")
        self.assertIn("STATIC_FIXTURE_CLAIM=PASS", ledger)
        self.assertIn("FRESH_LOGICAL_RECONSTRUCTION=PASS", ledger)
        self.assertIn("ORIGINATING_CHAT_REQUIRED=NO", ledger)
        self.assertIn("TRANSPORT_AND_PROVIDER_METADATA=NON_PROBATIVE", ledger)
        self.assertIn("T06_FRESH_INDEPENDENT_REVIEW=PASS", ledger)
        self.assertIn("no collapse of distinct dimensions into a generic `REAL_RUNTIME=PASS`", flat(text_of("CLOSURE_INPUTS")))

    def test_closure_inputs_records_t06_evidence_identities(self) -> None:
        ledger = text_of("CLOSURE_INPUTS")
        self.assertIn("PR #529", ledger)
        self.assertIn(f"T06_MERGE={T06_MERGE}", ledger)
        self.assertIn("a04771dc4e99af472e056b02f393935d511b6d73", ledger)
        self.assertIn("issuecomment-5930445323", ledger)
        self.assertIn("Issue #538", ledger)
        self.assertIn("issuecomment-5931430679", ledger)

    # -------------------------------------------------------------
    # Group 7: closure-input ledger (inputs only, no verdict authority)
    # -------------------------------------------------------------

    def test_closure_inputs_records_exact_version_subject_identity(self) -> None:
        ledger = text_of("CLOSURE_INPUTS")
        self.assertIn("INTEGRATION_TARGET=version/v4.6.0", ledger)
        self.assertIn(f"BOUND_BASE_SHA={BOUND_BASE_SHA}", ledger)
        self.assertIn(f"BOUND_BASE_TREE={BOUND_BASE_TREE}", ledger)
        self.assertIn(f"T07_MERGE={T07_MERGE}", ledger)

    def test_closure_inputs_records_t07_dependency_evidence(self) -> None:
        ledger = text_of("CLOSURE_INPUTS")
        self.assertIn("a357c942116b920285fcca7245bba7cb509d49f0", ledger)
        self.assertIn("Issue #561", ledger)
        self.assertIn("issuecomment-5932706324", ledger)
        self.assertIn("issuecomment-5934105450", ledger)
        self.assertIn("PR #533", ledger)

    def test_closure_inputs_keeps_pending_t08_gates_not_run(self) -> None:
        ledger = text_of("CLOSURE_INPUTS")
        for pending in (
            "T08_EXACT_SUBJECT_VALIDATION=NOT_RUN / PENDING",
            "T08_FRESH_INDEPENDENT_REVIEW=NOT_RUN / PENDING",
            "T08_EXACT_HEAD_CI=NOT_RUN / PENDING",
            "CANDIDATE_FREEZE=NOT_RUN / OUT_OF_SCOPE_FOR_THIS_LEDGER",
            "VERSION_CLOSURE=NOT_RUN / OUT_OF_SCOPE_FOR_THIS_LEDGER",
            "RELEASE_QUALIFICATION=NOT_RUN / OUT_OF_SCOPE_FOR_THIS_LEDGER",
            "MERGE=NOT_RUN / FORBIDDEN_FOR_BUILDER",
        ):
            self.assertIn(pending, ledger)

    def test_closure_inputs_defers_candidate_identity_to_live_reread(self) -> None:
        ledger = text_of("CLOSURE_INPUTS")
        self.assertIn("CANDIDATE_HEAD=RECORDED_ON_ISSUE_311_RESULT", ledger)
        self.assertIn("CANDIDATE_TREE=RECORDED_ON_ISSUE_311_RESULT", ledger)
        self.assertIn("must re-read the live PR HEAD/tree", ledger)

    def test_closure_inputs_records_unresolved_findings_without_downgrade(self) -> None:
        ledger = text_of("CLOSURE_INPUTS")
        self.assertIn("## 8. Unresolved findings and open items", ledger)
        self.assertIn("P0=NONE_RECORDED_AT_BUILD_TIME; P1=NONE_RECORDED_AT_BUILD_TIME", ledger)
        self.assertIn("remains BLOCKED for the affected Closure input", ledger)
        self.assertIn("core.autocrlf", ledger)

    def test_closure_inputs_issues_no_verdict_or_authorization(self) -> None:
        ledger = flat(text_of("CLOSURE_INPUTS"))
        self.assertIn(
            "does not issue or imply Candidate Freeze, Version Closure PASS/FAIL, Release Qualification, Release READY, repository integration authorization or v4.7 convergence/resolver semantics",
            ledger,
        )
        self.assertIn("PR PASS is not Version Closure or Release PASS", ledger)

    def test_closure_inputs_contains_no_manufactured_verdicts(self) -> None:
        ledger = text_of("CLOSURE_INPUTS")
        forbidden_assignments = [
            r"VERSION_CLOSURE\s*=\s*(PASS|FAIL|READY)",
            r"RELEASE_QUALIFICATION\s*=\s*(PASS|READY)",
            r"RELEASE_READY\s*=\s*(YES|PASS|TRUE)",
            r"CANDIDATE_FREEZE\s*=\s*(APPROVED|PASS|EXECUTED)",
            r"INTEGRATION_AUTHORIZED\s*=\s*(YES|PASS|TRUE)",
            r"MERGE_AUTHORIZATION\s*=\s*(YES|APPROVED|GRANTED)",
            r"V46_T08_(EXACT_SUBJECT|FRESH).*=\s*PASS",
            r"V47_CONVERGENCE\s*=\s*(PLANNED|APPROVED|PASS)",
        ]
        for pattern in forbidden_assignments:
            self.assertIsNone(
                re.search(pattern, ledger),
                f"closure-input ledger must not manufacture a verdict: {pattern}",
            )

    def test_task_pack_write_set_stays_bounded(self) -> None:
        task_pack = text_of("T08_TASK_PACK")
        self.assertIn("scripts/test_v46_cross_standard_conformance.py", task_pack)
        self.assertIn("docs/implementation/4.6.0/CLOSURE_INPUTS.md", task_pack)
        self.assertIn("No Product/L2/Task authority rewrite, no Version Closure or Release Qualification verdict", task_pack)
        self.assertIn("Do not downgrade missing evidence into PASS.", task_pack)

    def test_closure_inputs_respects_task_pack_failure_handling(self) -> None:
        ledger = flat(text_of("CLOSURE_INPUTS"))
        self.assertIn("Subject drift, unresolved P0/P1, missing required dogfood execution or an owner contradiction remains BLOCKED", ledger)


if __name__ == "__main__":
    unittest.main()
