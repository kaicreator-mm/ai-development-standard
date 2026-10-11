"""V411-T04 focused test: reuse-first modes and source/license currentness.

Encodes the V411-T04 task-pack §3 positive/negative oracles (P01–P05, N01–N07)
as (a) section-scoped textual contract checks binding the decision model to the
owner-local clauses in `standards/DEPENDENCY_TOOLCHAIN_GOVERNANCE_STANDARD.md`
(§6 reuse materiality, §9 exact source/license/NOTICE currentness, §13 failure
routing) and `standards/ARCHITECTURE_DESIGN_STANDARD.md` (§15 reuse-first
adoption and BUILD_NEW), and (b) fixture-driven deterministic decisions over
the J12 H1/H2/H3/BUILD_NEW contract including license drift, revision staleness
and fail-closed routing. Purely textual/offline; no network, no runtime.

R2 bounded repair (#1043 R2-F01..F04): source/license-file/NOTICE observations
are modeled as independent facts, each pinned to the revision it was actually
taken at — an observation taken at another revision is history and fails the
reliance stale, and a green status with no revision binding never authorizes.
The upstream inspector and the project license-policy owner are distinct,
non-interchangeable evidence roles. Material rights-bearing drift behind a
non-copying mode demands refreshed mode-matched evidence and otherwise fails
closed to STALE without a blanket H3 demotion. Negative fixtures for these
floors are additionally derived by an in-file oracle that reads the required
facts out of the owner clauses and never calls the decision model, so the
model and the clauses falsify together instead of self-attesting.

Acceptance boundary (NOT_RUN): T04 is an owner-local documentation deliverable
and has no production decision hook. This suite is owner-local offline
acceptance only; the in-file evaluator is not an online production contract
proof and no agreement with one is claimed. Central wiring of the reuse floors
into shared prompts/schemas/manifest is T11, binding reuse dispositions to
executed validation evidence is T12, and real upstream read-back of pinned
identities and executed builds on a real build host are out of scope for this
offline task (fixtures use synthetic local identities and synthetic
observation content). Those obligations stay recorded in
`NOT_RUN_OBLIGATIONS` as NOT_RUN and are not claimed as verified by this
suite.
"""

from __future__ import annotations

from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]

DEPENDENCY_STANDARD = "standards/DEPENDENCY_TOOLCHAIN_GOVERNANCE_STANDARD.md"
ARCHITECTURE_STANDARD = "standards/ARCHITECTURE_DESIGN_STANDARD.md"

# Gate states the standards already own; T04 must not mint new ones.
CANONICAL_GATE_STATES = {"PASS", "FAIL", "BLOCKED", "NOT_RUN", "NOT_APPLICABLE"}

MODE_ALIASES = {
    "H1": "PATTERN_HARVEST",
    "H2": "SPEC_MODULE_RECONSTRUCTION",
    "H3": "DIRECT_CODE_REUSE",
    "BUILD_NEW": "BUILD_NEW",
    "FAST_PATH": "FAST_PATH",
}
ALLOWED_DECISIONS = {"ALLOWED", "FAST_PATH_ALLOWED", "BLOCKED", "UNKNOWN", "STALE"}
# Capabilities a verdict can grant; none of them is a gate or release state.
ALLOWED_GRANTS = {"local_spec_module", "bounded_code_reuse", "local_build"}

FULL_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
# Only owner decisions and direct inspection count as evidence; popular
# visibility, docs and arbitrary checkers do not (task-pack N05/N07).
OWNER_EVIDENCE_SOURCES = {"owner_decision", "inspected_upstream", "recorded_disposition"}
UNTRUSTED_EVIDENCE_SOURCES = {"README", "unpinned_latest", "arbitrary_checker"}

# F05/F04: obligations this documentation-only task cannot execute are
# recorded as NOT_RUN, never claimed as verified. T11/T12 are the
# owner-assigned successor tasks; upstream read-back and real build execution
# are deferred because this suite is offline, and the in-file evaluator is an
# owner-local offline acceptance oracle, not an online production contract.
NOT_RUN_OBLIGATIONS = {
    "T11": (
        "wire the reuse decision floors into shared L1/L2/L3 prompts, schemas "
        "and the manifest (central wiring task); operative contract consistency "
        "with those T11 surfaces is NOT_RUN here"
    ),
    "T12": (
        "bind reuse dispositions to executed validation evidence at the owning "
        "gate (Validation owner); operative contract consistency with T12 gates "
        "is NOT_RUN here"
    ),
    "upstream_readback": (
        "dereference pinned upstream identities against the real upstream; "
        "fixtures carry synthetic local identities and synthetic observation "
        "content only and claim no real upstream right"
    ),
    "production_contract": (
        "the in-file evaluator is an owner-local offline acceptance oracle for "
        "this documentation-only task; agreement with an online production "
        "decision contract is NOT_RUN and is not claimed"
    ),
    "real_build_host": (
        "no executed build or validation on a real build host is performed; "
        "this suite stays textual/offline by design"
    ),
}


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def dependency_standard() -> str:
    return read(DEPENDENCY_STANDARD)


def architecture_standard() -> str:
    return read(ARCHITECTURE_STANDARD)


def section(text: str, start_heading: str, next_heading: str) -> str:
    start = text.index(start_heading)
    end = text.index(next_heading) if next_heading else len(text)
    return text[start:end]


def dependency_change_policy() -> str:
    return section(dependency_standard(), "## 6. Change policy", "## 7.")


def dependency_provenance_license() -> str:
    return section(dependency_standard(), "## 9. Provenance, registry", "## 10.")


def dependency_failure_handling() -> str:
    return section(dependency_standard(), "## 13. Failure handling", "## 14.")


def architecture_reuse_section() -> str:
    return section(architecture_standard(), "## 15. Reuse-first adoption", "")


def evaluate_reuse(case: dict) -> dict:
    """Deterministic J12 disposition per the V411-T04 contract (§4).

    Modes have distinct evidence floors; labels never erase materiality;
    revision/path/behavior drift and observed license/NOTICE changes are
    stale or fail closed; missing license/NOTICE/rights facts fail closed to
    the project license/security authority. The model never emits gate-state
    mutations or release permission.
    """
    missing: list[str] = []
    obligations: set[str] = set()
    grants: frozenset = frozenset()
    notes: dict = {}
    mode = MODE_ALIASES[case["claimed_mode"]]

    # N06: material source/code facts reclassify the change regardless of any
    # optional label; docs-only/Fast-Path labels never erase materiality and
    # the material mode is derived from observed facts rather than the claim.
    material_copy = bool(case.get("copied_source")) or bool(case.get("upstream_artifact_parity"))
    if case.get("material_upstream_delta") or material_copy:
        obligations.add("validation_impact")
        if case.get("claimed_mode") == "FAST_PATH":
            notes["fast_path_refused"] = True
        if mode == "FAST_PATH":
            # An actual vendored-source or license/NOTICE delta keeps the full
            # material-mode obligations (ADS §15): observed reused material is
            # direct code reuse whatever the work was labelled.
            mode = "DIRECT_CODE_REUSE"

    # N04: physical copying or artifact parity with the upstream is material
    # direct source adoption in every mode; it must meet the H3 floor instead
    # of laundering provenance through H1/H2/BUILD_NEW.
    if material_copy and mode != "DIRECT_CODE_REUSE":
        mode = "DIRECT_CODE_REUSE"

    # N07: evidence authority is explicit — only owner decisions, direct
    # upstream inspection or a recorded disposition are authoritative; any
    # other provider, named untrusted or merely unknown, is non-authoritative
    # and cannot substitute an owner decision or real current validation.
    evidence_sources = set(case.get("evidence_sources", []))
    non_authoritative = sorted(evidence_sources - OWNER_EVIDENCE_SOURCES)
    for source in non_authoritative:
        missing.append(f"owner_or_inspected_evidence:{source}")

    decision: str
    if mode == "FAST_PATH":
        # P05: proportional Fast Path without mandatory research/catalog.
        decision = "FAST_PATH_ALLOWED"

    elif mode == "PATTERN_HARVEST":
        if not case.get("upstream_pattern_ref"):
            missing.append("upstream_pattern_ref")
        if not case.get("local_design_owned"):
            missing.append("local_design_owned")
        decision = "BLOCKED" if missing else "ALLOWED"
        grants = frozenset()  # no direct-copy or behavior-equivalence right

    if mode == "SPEC_MODULE_RECONSTRUCTION":
        for field, name in (
            ("origin_disclosed", "origin_disclosed"),
            ("derivation_disclosed", "derivation_disclosed"),
            ("local_contract", "local_contract"),
            ("differential_tests", "differential_behavior_failure_tests"),
        ):
            if not case.get(field):
                missing.append(name)
        decision = "BLOCKED" if missing else "ALLOWED"
        grants = frozenset({"local_spec_module"}) if decision == "ALLOWED" else frozenset()

    elif mode == "DIRECT_CODE_REUSE":
        sha = case.get("upstream_full_sha") or ""
        identity_unknown = (
            bool(non_authoritative)
            or not case.get("upstream_repo")
            or not FULL_SHA_RE.match(sha)
            or not case.get("material_paths")
            or not evidence_sources.intersection(OWNER_EVIDENCE_SOURCES)
        )
        if not case.get("upstream_repo"):
            missing.append("upstream_repo")
        if not FULL_SHA_RE.match(sha):
            missing.append("pinned_full_sha")
        if not case.get("material_paths"):
            missing.append("material_paths")
        if not evidence_sources.intersection(OWNER_EVIDENCE_SOURCES):
            missing.append("authoritative_evidence_source")

        # F02: the upstream inspector and the project license-policy owner are
        # distinct, non-interchangeable roles. An authoritative bounded-reuse
        # verdict needs an independently attributable current upstream
        # inspection AND an independent project license-policy ruling; neither
        # evidence source can stand in for the other and a green policy boolean
        # without an owner attribution rules nothing.
        has_current_inspection = "inspected_upstream" in evidence_sources
        has_policy_authority = (
            "owner_decision" in evidence_sources
            and case.get("license_policy_authority") == "owner_decision"
        )
        if not has_current_inspection:
            missing.append("current_upstream_inspection_evidence")
        if not has_policy_authority:
            missing.append("independent_license_policy_authority")

        # N01: reliance on a new revision never inherits the historic permission.
        historic = case.get("historic_permission_revision")
        current = case.get("current_reliance_revision")
        if historic and current and historic != current:
            notes["historic_permission_preserved"] = {
                "revision": historic,
                "inheritable": False,
            }
            obligations.update({"license_authority_disposition", "validation_impact"})
        # An explicitly observed license/NOTICE change is material drift on its
        # own; it never needs a historic/current pair to fail closed (§§6/9/13).
        if case.get("upstream_license_changed") or case.get("upstream_notice_changed"):
            missing.append("license_notice_observation_at_current_revision")
            obligations.update({"license_authority_disposition", "validation_impact"})

        # N02: cited-vs-used or relied-vs-pinned revision mismatch, or any
        # upstream path/behavior drift, makes the prior permission stale (§13).
        stale = (
            (bool(case.get("l2_cited_revision")) and bool(sha) and case["l2_cited_revision"] != sha)
            or (bool(current) and bool(sha) and current != sha)
            or bool(case.get("upstream_path_drift"))
            or bool(case.get("upstream_behavior_drift"))
        )
        if stale:
            obligations.update({"fresh_equivalence_source_check", "validation_impact"})

        # F01: observations carry their own identity. Source, license-file and
        # NOTICE observations are three independent facts, each pinned to the
        # revision it was actually taken at (revision + observed content/blob).
        # Only an observation bound to the relied revision authorizes; one
        # taken at another revision is history and makes the reliance stale;
        # a green status with no revision binding at all is unattributable and
        # fails closed (§9 "as observed at that revision, not as remembered").
        relied_revision = current or (sha if FULL_SHA_RE.match(sha) else "")
        observation_identities = (
            (
                "source",
                bool(case.get("source_observation_blob")),
                case.get("source_observation_revision"),
                case.get("source_observation_blob"),
                "source_observation_at_relied_revision",
            ),
            (
                "license",
                case.get("license_observation") == "inspected_authorized",
                case.get("license_observation_revision"),
                case.get("license_observation_content"),
                "inspected_license_observation_at_relied_revision",
            ),
            (
                "notice",
                case.get("notice_observation") == "present",
                case.get("notice_observation_revision"),
                case.get("notice_observation_content"),
                "notice_observation_at_relied_revision",
            ),
        )
        observation_elsewhere = False
        license_bound_now = False
        if relied_revision:
            for kind, claimed, at_revision, content, marker in observation_identities:
                if claimed and at_revision == relied_revision and content:
                    if kind == "license":
                        license_bound_now = True
                    continue
                missing.append(marker)
                if claimed and at_revision:
                    observation_elsewhere = True
        # Without a license observation bound to the relied revision the rights
        # state is unknown/conflicting/missing: fail closed with the project
        # license/security authority (§9); upstream visibility resolves nothing.
        if not license_bound_now:
            obligations.add("license_authority_disposition")
        if observation_elsewhere:
            stale = True
            obligations.update({"fresh_equivalence_source_check", "validation_impact"})
            notes["observation_bound_to_other_revision"] = True

        # F02: the policy ruling must cover the relied revision. A ruling
        # recorded at a historic revision is inherited history, not current
        # authority; it fails closed instead of authorizing.
        if case.get("license_policy_authorized"):
            if has_policy_authority and relied_revision and case.get("license_policy_revision") != relied_revision:
                missing.append("license_policy_disposition_at_relied_revision")
        else:
            missing.append("license_policy_disposition")
        if not case.get("attribution"):
            missing.append("attribution")
        if not case.get("local_behavior_tests"):
            missing.append("local_behavior_tests")

        if stale:
            decision = "STALE"
        elif identity_unknown:
            decision = "UNKNOWN"
        elif missing:
            decision = "BLOCKED"
        else:
            decision = "ALLOWED"
        grants = frozenset({"bounded_code_reuse"}) if decision == "ALLOWED" else frozenset()

    elif mode == "BUILD_NEW":
        if not case.get("comparators_considered"):
            missing.append("mature_comparators_considered")
        if not case.get("build_new_rationale"):
            missing.append("concrete_build_new_rationale")
        if not case.get("decision_owner"):
            missing.append("accountable_decision_owner")
        decision = "BLOCKED" if missing else "ALLOWED"
        grants = frozenset({"local_build"}) if decision == "ALLOWED" else frozenset()
        notes["not_a_silent_default"] = True

    # F03: material rights-bearing drift behind a non-copying mode invalidates
    # the mode's own self-description. The mode keeps its shape and floor (no
    # blanket H3 demotion), but it must present refreshed, mode-matched
    # evidence at the new material state; an allowed verdict resting on a
    # stale self-description is downgraded to STALE and loses every grant
    # (§13: drift behind already-relied-on reuse is stale until re-checked).
    if (
        decision == "ALLOWED"
        and case.get("material_upstream_delta")
        and mode in ("PATTERN_HARVEST", "SPEC_MODULE_RECONSTRUCTION", "BUILD_NEW")
        and not case.get("refreshed_mode_matched_evidence")
    ):
        decision = "STALE"
        grants = frozenset()
        obligations.update({"fresh_equivalence_source_check", "validation_impact"})
        notes["stale_material_self_description"] = True

    return {
        "subject": case["subject"],
        "mode": mode,
        "decision": decision,
        "missing": missing,
        "obligations": obligations,
        "grants": grants,
        "notes": notes,
        "gate_mutations": (),
    }


def h1_case(**overrides: object) -> dict:
    case = {
        "subject": "H1 fixture",
        "claimed_mode": "H1",
        "upstream_pattern_ref": True,
        "local_design_owned": True,
    }
    case.update(overrides)
    return case


def h2_case(**overrides: object) -> dict:
    case = {
        "subject": "H2 fixture",
        "claimed_mode": "H2",
        "origin_disclosed": True,
        "derivation_disclosed": True,
        "local_contract": True,
        "differential_tests": True,
        "evidence_sources": ["inspected_upstream"],
    }
    case.update(overrides)
    return case


def h3_case(**overrides: object) -> dict:
    # NOTE: `upstream_full_sha`, the observation revision pins and the
    # observation contents below are synthetic 40-hex fixture identities and
    # synthetic observation content. They are never dereferenced against a
    # real upstream and claim no real upstream right; real read-back stays
    # recorded in NOT_RUN_OBLIGATIONS and is not claimed as observed.
    case = {
        "subject": "H3 fixture",
        "claimed_mode": "H3",
        "upstream_repo": "upstream/example-lib",
        "upstream_full_sha": "b" * 40,
        "material_paths": ["src/example.rs"],
        "source_observation_revision": "b" * 40,
        "source_observation_blob": "blob:src/example.rs@b",
        "license_observation": "inspected_authorized",
        "license_observation_revision": "b" * 40,
        "license_observation_content": "license-text@b:MIT",
        "notice_observation": "present",
        "notice_observation_revision": "b" * 40,
        "notice_observation_content": "notice-content@b",
        "license_policy_authorized": True,
        "license_policy_authority": "owner_decision",
        "license_policy_revision": "b" * 40,
        "attribution": True,
        "local_behavior_tests": True,
        "evidence_sources": ["inspected_upstream", "owner_decision"],
    }
    case.update(overrides)
    return case


def build_new_case(**overrides: object) -> dict:
    case = {
        "subject": "BUILD_NEW fixture",
        "claimed_mode": "BUILD_NEW",
        "comparators_considered": ["mature-competitor-lib"],
        "build_new_rationale": ["incompatible-license", "vendor-coupling"],
        "decision_owner": "architecture-owner",
    }
    case.update(overrides)
    return case


class DependencyReuseMaterialityTests(unittest.TestCase):
    """Pack §3 N06 binding: §6 classifies reuse deltas by material effect, not labels."""

    def test_reuse_deltas_are_material_by_effect_not_by_label(self) -> None:
        section_text = dependency_change_policy()
        self.assertIn("Reuse-sourced deltas follow the same materiality rule.", section_text)
        self.assertIn("Vendored or copied upstream source", section_text)
        self.assertIn("a changed upstream revision or source path behind material already relied on", section_text)
        self.assertIn("an upstream license/NOTICE change", section_text)

    def test_docs_only_or_fast_path_label_does_not_reclassify(self) -> None:
        section_text = dependency_change_policy()
        self.assertIn("A docs-only/chore label or a Fast Path claim does not change this classification.", section_text)

    def test_existing_validation_impact_discipline_is_preserved(self) -> None:
        section_text = dependency_change_policy()
        self.assertIn("Material dependency, lock, registry/source or toolchain deltas MUST participate", section_text)
        self.assertIn("`VALIDATION_IMPACT_DECISION`", section_text)
        self.assertIn("Evidence reuse is forbidden when impact is affected or unknown.", section_text)


class DependencySourceLicenseCurrentnessTests(unittest.TestCase):
    """Pack §3 P03/N01/N05 binding: §9 binds reuse to exact revision-scoped facts."""

    def test_reuse_is_bound_to_exact_revision_scoped_provenance(self) -> None:
        section_text = dependency_provenance_license()
        self.assertIn("the upstream repository, the full commit SHA relied on", section_text)
        self.assertIn("the material paths taken from it", section_text)
        self.assertIn(
            "the license file and NOTICE content as observed at that revision, "
            "not as remembered or as currently advertised",
            section_text,
        )
        self.assertIn("the project license-policy disposition authorizing the specific reuse mode", section_text)

    def test_observations_are_revision_bound_and_not_inheritable(self) -> None:
        section_text = dependency_provenance_license()
        self.assertIn("These observations are revision-bound.", section_text)
        self.assertIn("it does not inherit the earlier license/NOTICE observation", section_text)
        self.assertIn("the earlier observation stays valid only as history", section_text)
        self.assertIn("Re-observation and, where material, Validation Impact review are required", section_text)

    def test_public_availability_is_not_a_reuse_right(self) -> None:
        section_text = dependency_provenance_license()
        self.assertIn("Public availability of an upstream repository is not by itself evidence of a reuse right.", section_text)
        self.assertIn("fail-closed with the project license/security authority", section_text)
        self.assertIn("MUST NOT assume a lawful reuse basis from visibility, popularity or a README claim.", section_text)

    def test_existing_project_policy_authority_is_preserved(self) -> None:
        section_text = dependency_provenance_license()
        self.assertIn("project/risk-authoritative controls", section_text)
        self.assertIn("does not make every project", section_text)

    def test_central_wiring_is_routed_to_t11_not_done_here(self) -> None:
        section_text = dependency_provenance_license()
        self.assertIn("central wiring task (T11)", section_text)
        self.assertIn("records only owner-local duties and does not edit those surfaces", section_text)


class DependencyFailureRoutingTests(unittest.TestCase):
    """Pack §3 N01/N02/N05/N07 binding: §13 routes missing/drifted reuse facts."""

    def test_missing_identity_license_or_policy_fails_closed_to_authority(self) -> None:
        section_text = dependency_failure_handling()
        self.assertIn("keep the reuse disposition non-authoritative (`BLOCKED`/unknown)", section_text)
        self.assertIn("with the project license/security authority", section_text)
        self.assertIn("upstream visibility does not resolve it", section_text)

    def test_upstream_drift_makes_prior_permission_stale(self) -> None:
        section_text = dependency_failure_handling()
        self.assertIn("the prior permission is stale", section_text)
        self.assertIn("fresh source/equivalence tests plus Validation Impact precede further reliance", section_text)

    def test_reuse_record_is_never_release_or_legality_permission(self) -> None:
        section_text = dependency_failure_handling()
        self.assertIn("A reuse record is provenance/currentness input only", section_text)
        self.assertIn("MUST NOT be promoted to Validation PASS, license legality or release permission", section_text)

    def test_existing_failure_lines_are_preserved(self) -> None:
        section_text = dependency_failure_handling()
        self.assertIn("execution `BLOCKED`, not project requirement mutation", section_text)
        self.assertIn("preserve the owning gate as non-PASS according to its authority", section_text)


class ArchitectureReuseModeTests(unittest.TestCase):
    """Pack §3 P01–P05 binding: ADS §15 owns mode selection with distinct floors."""

    def test_reuse_mode_is_an_accountable_choice_with_distinct_floors(self) -> None:
        section_text = architecture_reuse_section()
        self.assertIn("## 15. Reuse-first adoption and BUILD_NEW", section_text)
        self.assertIn("explicit accountable choice with distinct evidence floors, not a convenience default", section_text)
        for mode in ("Pattern harvest (H1)", "Source-inspired re-specification (H2)", "Direct code reuse (H3)", "BUILD_NEW"):
            with self.subTest(mode=mode):
                self.assertIn(mode, section_text)

    def test_h1_does_not_infer_copy_or_equivalence(self) -> None:
        section_text = architecture_reuse_section()
        self.assertIn("similarity MUST NOT be read as direct copying or behavior equivalence", section_text)

    def test_h2_requires_disclosure_and_differential_tests(self) -> None:
        section_text = architecture_reuse_section()
        self.assertIn("disclosed origin and derivation context", section_text)
        self.assertIn("differential/behavior/failure tests exposing divergence and risks", section_text)
        self.assertIn("provenance laundering and MUST NOT pass as local design", section_text)

    def test_h3_is_bounded_and_never_release_permission(self) -> None:
        section_text = architecture_reuse_section()
        self.assertIn("exact immutable upstream identity and material paths", section_text)
        self.assertIn("license/NOTICE observed at that revision with the project license-policy disposition", section_text)
        self.assertIn("it is never Validation PASS or release permission", section_text)
        self.assertIn("stale until freshly re-checked", section_text)

    def test_build_new_requires_comparators_rationale_and_owner(self) -> None:
        section_text = architecture_reuse_section()
        self.assertIn("materially plausible mature comparators", section_text)
        self.assertIn("concrete incompatible-license/coupling/security/maintenance rationale", section_text)
        self.assertIn("a decision owner", section_text)
        self.assertIn("It is not a silent default", section_text)
        self.assertIn("keep it blocked", section_text)

    def test_ownership_split_and_no_l1_l2_l3_auto_promotion(self) -> None:
        section_text = architecture_reuse_section()
        self.assertIn("Architecture owns the mode selection, alternatives and local contracts", section_text)
        self.assertIn("owns upstream identity, license/NOTICE currentness and reuse invalidation", section_text)
        self.assertIn("Validation alone owns executed proof", section_text)
        self.assertIn("No mode auto-promotes across L1→L2→L3", section_text)
        self.assertIn("no reuse disposition mints a gate or release state", section_text)

    def test_fast_path_stays_proportional_but_labels_do_not_erase_materiality(self) -> None:
        section_text = architecture_reuse_section()
        self.assertIn("requires no mandatory external research or reuse catalog", section_text)
        self.assertIn("The label does not erase material obligations", section_text)
        self.assertIn("keeps the obligations above regardless of how the work was labelled", section_text)

    def test_existing_design_decision_and_fast_path_semantics_are_preserved(self) -> None:
        text = architecture_standard()
        self.assertIn("Alternatives considered", text)
        self.assertIn("A Frozen L2 decision outranks later implementation preference", text)
        self.assertIn("Fast Path changes with no material architecture decision need not produce empty design artifacts", text)
        self.assertIn("Fast Path MUST NOT be used to avoid architecture evidence", text)


class ReuseDecisionPositiveTests(unittest.TestCase):
    """Fixture-driven oracles for task-pack P01–P05."""

    def test_p01_pattern_harvest_is_allowed_without_copy_rights(self) -> None:
        verdict = evaluate_reuse(h1_case(subject="P01 cited pattern, local design"))
        self.assertEqual(verdict["subject"], "P01 cited pattern, local design")
        self.assertEqual(verdict["mode"], "PATTERN_HARVEST")
        self.assertEqual(verdict["decision"], "ALLOWED")
        self.assertEqual(verdict["missing"], [])
        self.assertEqual(verdict["grants"], frozenset())
        self.assertEqual(verdict["obligations"], set())
        self.assertEqual(verdict["gate_mutations"], ())

    def test_p01_copied_source_reclassifies_out_of_h1(self) -> None:
        verdict = evaluate_reuse(h1_case(subject="P01 misuse", copied_source=True))
        self.assertEqual(verdict["mode"], "DIRECT_CODE_REUSE")
        self.assertNotEqual(verdict["decision"], "ALLOWED")

    def test_p02_spec_reconstruction_with_disclosed_derivation_is_admissible(self) -> None:
        verdict = evaluate_reuse(h2_case(subject="P02 disclosed re-specification"))
        self.assertEqual(verdict["mode"], "SPEC_MODULE_RECONSTRUCTION")
        self.assertEqual(verdict["decision"], "ALLOWED")
        self.assertEqual(verdict["grants"], frozenset({"local_spec_module"}))
        self.assertEqual(verdict["missing"], [])
        self.assertEqual(verdict["obligations"], set())
        self.assertEqual(verdict["gate_mutations"], ())

    def test_p03_direct_reuse_with_exact_source_and_license_is_bounded(self) -> None:
        verdict = evaluate_reuse(h3_case(subject="P03 pinned reuse"))
        self.assertEqual(verdict["subject"], "P03 pinned reuse")
        self.assertEqual(verdict["mode"], "DIRECT_CODE_REUSE")
        self.assertEqual(verdict["decision"], "ALLOWED")
        self.assertEqual(verdict["grants"], frozenset({"bounded_code_reuse"}))
        self.assertEqual(verdict["missing"], [])
        self.assertEqual(verdict["obligations"], set())
        self.assertNotIn("RELEASE_PASS", verdict["grants"])
        self.assertEqual(verdict["gate_mutations"], ())

    def test_p04_accountable_build_new_is_admissible_not_default(self) -> None:
        verdict = evaluate_reuse(build_new_case(subject="P04 accountable BUILD_NEW"))
        self.assertEqual(verdict["mode"], "BUILD_NEW")
        self.assertEqual(verdict["decision"], "ALLOWED")
        self.assertEqual(verdict["grants"], frozenset({"local_build"}))
        self.assertEqual(verdict["missing"], [])
        self.assertTrue(verdict["notes"]["not_a_silent_default"])
        self.assertEqual(verdict["gate_mutations"], ())

    def test_p05_fast_path_needs_no_mandatory_research_or_catalog(self) -> None:
        verdict = evaluate_reuse(
            h1_case(subject="P05 immaterial local change", claimed_mode="FAST_PATH")
        )
        self.assertEqual(verdict["mode"], "FAST_PATH")
        self.assertEqual(verdict["decision"], "FAST_PATH_ALLOWED")
        self.assertEqual(verdict["obligations"], set())
        self.assertEqual(verdict["missing"], [])
        self.assertEqual(verdict["grants"], frozenset())
        self.assertEqual(verdict["gate_mutations"], ())


class ReuseDecisionNegativeTests(unittest.TestCase):
    """Fixture-driven fail-closed oracles for task-pack N01–N07."""

    def test_n01_new_revision_cannot_inherit_historic_license_permission(self) -> None:
        verdict = evaluate_reuse(
            h3_case(
                subject="N01 license drifted at revision B",
                historic_permission_revision="a" * 40,
                current_reliance_revision="b" * 40,
                upstream_license_changed=True,
            )
        )
        self.assertEqual(verdict["decision"], "BLOCKED")
        self.assertEqual(
            verdict["notes"]["historic_permission_preserved"],
            {"revision": "a" * 40, "inheritable": False},
        )
        self.assertIn("license_notice_observation_at_current_revision", verdict["missing"])
        self.assertIn("license_authority_disposition", verdict["obligations"])
        self.assertIn("validation_impact", verdict["obligations"])
        self.assertEqual(verdict["grants"], frozenset())
        self.assertEqual(verdict["gate_mutations"], ())

    def test_n02_cited_revision_differs_from_used_revision_is_stale(self) -> None:
        verdict = evaluate_reuse(
            h3_case(
                subject="N02 L2 cited A, L3 uses B",
                upstream_full_sha="b" * 40,
                l2_cited_revision="a" * 40,
            )
        )
        self.assertEqual(verdict["decision"], "STALE")
        self.assertIn("fresh_equivalence_source_check", verdict["obligations"])
        self.assertEqual(verdict["grants"], frozenset())
        self.assertEqual(verdict["gate_mutations"], ())

    def test_n02_material_path_drift_is_stale(self) -> None:
        verdict = evaluate_reuse(
            h3_case(subject="N02 upstream path drift", upstream_path_drift=True)
        )
        self.assertEqual(verdict["decision"], "STALE")
        self.assertIn("fresh_equivalence_source_check", verdict["obligations"])
        self.assertEqual(verdict["gate_mutations"], ())

    def test_n02_behavior_drift_is_stale_even_without_revision_mismatch(self) -> None:
        # F03: behavior drift behind already-relied-on reuse is material drift
        # on its own; it cannot stay allowed without fresh equivalence.
        verdict = evaluate_reuse(
            h3_case(subject="N02 upstream behavior drift", upstream_behavior_drift=True)
        )
        self.assertEqual(verdict["decision"], "STALE")
        self.assertIn("fresh_equivalence_source_check", verdict["obligations"])
        self.assertIn("validation_impact", verdict["obligations"])
        self.assertEqual(verdict["grants"], frozenset())
        self.assertEqual(verdict["gate_mutations"], ())

    def test_n02_relied_revision_diverging_from_pinned_identity_is_stale(self) -> None:
        # F03: the revision actually relied on must match the pinned source
        # identity; a divergence is stale even when the L2 citation matches.
        verdict = evaluate_reuse(
            h3_case(
                subject="N02 relied C, pinned B",
                upstream_full_sha="b" * 40,
                current_reliance_revision="c" * 40,
            )
        )
        self.assertEqual(verdict["decision"], "STALE")
        self.assertIn("fresh_equivalence_source_check", verdict["obligations"])
        self.assertIn("validation_impact", verdict["obligations"])
        self.assertEqual(verdict["grants"], frozenset())
        self.assertEqual(verdict["gate_mutations"], ())

    def test_n01_license_change_alone_fails_closed_without_historic_pair(self) -> None:
        # F03: an explicitly observed license change is material drift by
        # itself and never needs a historic/current revision pair to matter.
        verdict = evaluate_reuse(
            h3_case(subject="N01 license changed, no historic pair", upstream_license_changed=True)
        )
        self.assertEqual(verdict["decision"], "BLOCKED")
        self.assertIn("license_notice_observation_at_current_revision", verdict["missing"])
        self.assertIn("license_authority_disposition", verdict["obligations"])
        self.assertIn("validation_impact", verdict["obligations"])
        self.assertEqual(verdict["grants"], frozenset())
        self.assertEqual(verdict["gate_mutations"], ())

    def test_n01_notice_change_alone_fails_closed_without_historic_pair(self) -> None:
        verdict = evaluate_reuse(
            h3_case(subject="N01 NOTICE changed, no historic pair", upstream_notice_changed=True)
        )
        self.assertEqual(verdict["decision"], "BLOCKED")
        self.assertIn("license_notice_observation_at_current_revision", verdict["missing"])
        self.assertIn("license_authority_disposition", verdict["obligations"])
        self.assertIn("validation_impact", verdict["obligations"])
        self.assertEqual(verdict["grants"], frozenset())
        self.assertEqual(verdict["gate_mutations"], ())

    def test_n02_license_change_behind_drift_is_stale_with_owner_disposition(self) -> None:
        # Combined drift: any material drift wins over green-looking static
        # facts and routes to stale with owner disposition plus Validation
        # Impact before further reliance.
        verdict = evaluate_reuse(
            h3_case(
                subject="N02 license change behind behavior drift",
                upstream_behavior_drift=True,
                upstream_license_changed=True,
            )
        )
        self.assertEqual(verdict["decision"], "STALE")
        self.assertIn("license_notice_observation_at_current_revision", verdict["missing"])
        for obligation in (
            "fresh_equivalence_source_check",
            "license_authority_disposition",
            "validation_impact",
        ):
            with self.subTest(obligation=obligation):
                self.assertIn(obligation, verdict["obligations"])
        self.assertEqual(verdict["grants"], frozenset())
        self.assertEqual(verdict["gate_mutations"], ())

    def test_n03_build_new_without_comparators_or_owner_is_blocked(self) -> None:
        verdict = evaluate_reuse(
            build_new_case(
                subject="N03 silent BUILD_NEW",
                comparators_considered=[],
                build_new_rationale=[],
                decision_owner=None,
            )
        )
        self.assertEqual(verdict["decision"], "BLOCKED")
        for missing in (
            "mature_comparators_considered",
            "concrete_build_new_rationale",
            "accountable_decision_owner",
        ):
            with self.subTest(missing=missing):
                self.assertIn(missing, verdict["missing"])
        self.assertEqual(verdict["grants"], frozenset())
        self.assertEqual(verdict["gate_mutations"], ())

    def test_n04_undisclosed_rewrite_is_provenance_laundering(self) -> None:
        verdict = evaluate_reuse(
            h2_case(
                subject="N04 LLM-rewrite laundering",
                origin_disclosed=False,
                derivation_disclosed=False,
                differential_tests=False,
            )
        )
        self.assertEqual(verdict["mode"], "SPEC_MODULE_RECONSTRUCTION")
        self.assertEqual(verdict["decision"], "BLOCKED")
        for missing in (
            "origin_disclosed",
            "derivation_disclosed",
            "differential_behavior_failure_tests",
        ):
            with self.subTest(missing=missing):
                self.assertIn(missing, verdict["missing"])
        self.assertEqual(verdict["grants"], frozenset())
        self.assertEqual(verdict["gate_mutations"], ())

    def test_n04_copied_source_under_h2_claim_meets_the_h3_floor(self) -> None:
        # F02: physical copying under an H2 claim is material direct adoption;
        # it must meet the H3 floor instead of staying a local spec module.
        verdict = evaluate_reuse(
            h2_case(subject="N04 H2 claimed over copied source", copied_source=True)
        )
        self.assertEqual(verdict["mode"], "DIRECT_CODE_REUSE")
        self.assertNotEqual(verdict["decision"], "ALLOWED")
        self.assertEqual(verdict["grants"], frozenset())
        self.assertIn("validation_impact", verdict["obligations"])
        self.assertIn("pinned_full_sha", verdict["missing"])
        self.assertEqual(verdict["gate_mutations"], ())

    def test_n04_artifact_parity_with_upstream_is_not_local_re_specification(self) -> None:
        # F02: an H2 output at artifact parity with the upstream is physically
        # equivalent to copying and cannot pass as local re-specification.
        verdict = evaluate_reuse(
            h2_case(subject="N04 H2 artifact parity", upstream_artifact_parity=True)
        )
        self.assertEqual(verdict["mode"], "DIRECT_CODE_REUSE")
        self.assertNotEqual(verdict["decision"], "ALLOWED")
        self.assertEqual(verdict["grants"], frozenset())
        self.assertIn("validation_impact", verdict["obligations"])
        self.assertEqual(verdict["gate_mutations"], ())

    def test_n04_copied_source_under_build_new_claim_meets_the_h3_floor(self) -> None:
        # F02: no claimed mode exempts physical copying from the H3 floor.
        verdict = evaluate_reuse(
            build_new_case(subject="N04 BUILD_NEW claimed over copied source", copied_source=True)
        )
        self.assertEqual(verdict["mode"], "DIRECT_CODE_REUSE")
        self.assertNotEqual(verdict["decision"], "ALLOWED")
        self.assertEqual(verdict["grants"], frozenset())
        self.assertIn("validation_impact", verdict["obligations"])
        self.assertEqual(verdict["gate_mutations"], ())

    def test_n05_public_repository_does_not_create_reuse_rights(self) -> None:
        case = h3_case(
            subject="N05 conflicting license, missing NOTICE",
            license_observation="conflicting",
            notice_observation="missing",
            license_policy_authorized=False,
        )
        verdict = evaluate_reuse(case)
        self.assertEqual(verdict["decision"], "BLOCKED")
        self.assertIn("license_authority_disposition", verdict["obligations"])
        self.assertEqual(verdict["grants"], frozenset())
        # Visibility alone changes nothing: the same case with a private fork
        # receives the identical fail-closed verdict.
        private = evaluate_reuse({**case, "upstream_repo": "internal/example-lib"})
        self.assertEqual(private["decision"], verdict["decision"])
        self.assertEqual(private["missing"], verdict["missing"])
        self.assertEqual(verdict["gate_mutations"], ())

    def test_n06_docs_only_label_with_vendored_source_keeps_full_obligations(self) -> None:
        verdict = evaluate_reuse(
            h3_case(
                subject="N06 relabelled vendored source",
                claimed_mode="FAST_PATH",
                label_only_claim=True,
                material_upstream_delta=True,
                actual_mode="H3",
                upstream_full_sha=None,
                license_observation=None,
                notice_observation=None,
                license_policy_authorized=False,
                attribution=False,
                local_behavior_tests=False,
                evidence_sources=["inspected_upstream"],
            )
        )
        self.assertNotEqual(verdict["decision"], "FAST_PATH_ALLOWED")
        self.assertTrue(verdict["notes"]["fast_path_refused"])
        self.assertIn("validation_impact", verdict["obligations"])
        self.assertEqual(verdict["mode"], "DIRECT_CODE_REUSE")
        self.assertIn("pinned_full_sha", verdict["missing"])
        self.assertIn("license_policy_disposition", verdict["missing"])
        self.assertEqual(verdict["gate_mutations"], ())

    def test_n06_material_delta_without_any_label_flag_refuses_fast_path(self) -> None:
        # F01 counterexample: the material delta alone — with no label-only
        # claim and no claimed actual mode — must still refuse the Fast Path
        # and apply the H3 floor.
        verdict = evaluate_reuse(
            h3_case(
                subject="N06 material delta, no label flags",
                claimed_mode="FAST_PATH",
                material_upstream_delta=True,
                upstream_full_sha=None,
                license_observation=None,
                notice_observation=None,
                license_policy_authorized=False,
                attribution=False,
                local_behavior_tests=False,
            )
        )
        self.assertNotEqual(verdict["decision"], "FAST_PATH_ALLOWED")
        self.assertEqual(verdict["mode"], "DIRECT_CODE_REUSE")
        self.assertTrue(verdict["notes"]["fast_path_refused"])
        self.assertIn("validation_impact", verdict["obligations"])
        self.assertEqual(verdict["grants"], frozenset())
        self.assertEqual(verdict["gate_mutations"], ())

    def test_n06_removing_or_flipping_each_label_flag_keeps_the_material_floor(self) -> None:
        # Labels are optional claims: removing or flipping any of them must
        # leave the material floor untouched.
        stripped = {
            "upstream_full_sha": None,
            "license_observation": None,
            "notice_observation": None,
            "license_policy_authorized": False,
            "attribution": False,
            "local_behavior_tests": False,
        }
        label_variants = (
            {"label_only_claim": True, "actual_mode": "H3"},
            {"actual_mode": "H3"},  # label_only_claim removed
            {"label_only_claim": False, "actual_mode": "H3"},
            {"label_only_claim": True},  # actual_mode removed
            {"label_only_claim": True, "actual_mode": "H1"},  # misleading label
            {},  # every label flag removed
        )
        baseline = None
        for index, variant in enumerate(label_variants):
            verdict = evaluate_reuse(
                h3_case(
                    subject=f"N06 label variant {index}",
                    claimed_mode="FAST_PATH",
                    material_upstream_delta=True,
                    **stripped,
                    **variant,
                )
            )
            with self.subTest(variant=variant):
                self.assertNotEqual(verdict["decision"], "FAST_PATH_ALLOWED")
                self.assertEqual(verdict["mode"], "DIRECT_CODE_REUSE")
                self.assertIn("validation_impact", verdict["obligations"])
            if baseline is None:
                baseline = verdict
            else:
                self.assertEqual(verdict["mode"], baseline["mode"])
                self.assertEqual(verdict["decision"], baseline["decision"])
                self.assertEqual(verdict["missing"], baseline["missing"])
                self.assertEqual(verdict["obligations"], baseline["obligations"])

    def test_n06_label_only_claim_without_material_delta_is_immaterial(self) -> None:
        # The inverse direction: a label flag alone, with no observed material
        # delta, does not invent materiality.
        verdict = evaluate_reuse(
            h1_case(
                subject="N06 label-only, immaterial",
                claimed_mode="FAST_PATH",
                label_only_claim=True,
            )
        )
        self.assertEqual(verdict["decision"], "FAST_PATH_ALLOWED")
        self.assertEqual(verdict["obligations"], set())
        self.assertEqual(verdict["gate_mutations"], ())

    def test_n07_readme_and_unpinned_claims_are_not_owner_evidence(self) -> None:
        verdict = evaluate_reuse(
            h3_case(
                subject="N07 README/unpinned claims",
                upstream_full_sha=None,
                license_policy_authorized=True,
                evidence_sources=["README", "unpinned_latest", "arbitrary_checker"],
            )
        )
        self.assertEqual(verdict["decision"], "UNKNOWN")
        for marker in ("owner_or_inspected_evidence:README", "owner_or_inspected_evidence:unpinned_latest"):
            with self.subTest(marker=marker):
                self.assertIn(marker, verdict["missing"])
        self.assertNotEqual(verdict["decision"], "ALLOWED")
        self.assertEqual(verdict["grants"], frozenset())
        self.assertEqual(verdict["gate_mutations"], ())

    def test_n07_unknown_checker_with_green_facts_is_not_authoritative(self) -> None:
        # F06 counterexample: an unknown evidence provider plus synthetic
        # green lights never mints an allowed reuse right.
        verdict = evaluate_reuse(
            h3_case(subject="N07 unknown checker", evidence_sources=["unknown_checker"])
        )
        self.assertEqual(verdict["decision"], "UNKNOWN")
        self.assertNotEqual(verdict["decision"], "ALLOWED")
        self.assertIn("owner_or_inspected_evidence:unknown_checker", verdict["missing"])
        self.assertIn("authoritative_evidence_source", verdict["missing"])
        self.assertEqual(verdict["grants"], frozenset())
        self.assertEqual(verdict["gate_mutations"], ())

    def test_n07_absent_or_non_owner_evidence_fails_closed(self) -> None:
        for evidence in ([], ["docs_page"], ["owner_friend_summary"]):
            verdict = evaluate_reuse(
                h3_case(subject="N07 evidence admission", evidence_sources=evidence)
            )
            with self.subTest(evidence=evidence):
                self.assertEqual(verdict["decision"], "UNKNOWN")
                self.assertIn("authoritative_evidence_source", verdict["missing"])
                self.assertEqual(verdict["grants"], frozenset())
                self.assertEqual(verdict["gate_mutations"], ())

    def test_n07_named_untrusted_sources_are_never_owner_authoritative(self) -> None:
        self.assertFalse(UNTRUSTED_EVIDENCE_SOURCES & OWNER_EVIDENCE_SOURCES)
        for source in sorted(UNTRUSTED_EVIDENCE_SOURCES):
            verdict = evaluate_reuse(
                h3_case(subject=f"N07 {source}", evidence_sources=[source])
            )
            with self.subTest(source=source):
                self.assertEqual(verdict["decision"], "UNKNOWN")
                self.assertIn(f"owner_or_inspected_evidence:{source}", verdict["missing"])
                self.assertEqual(verdict["gate_mutations"], ())


class OwnerBoundaryNegativeTests(unittest.TestCase):
    """No minted gate states, no universal vendoring/legal verdict, no second research lifecycle."""

    ALL_NEW_TEXT_SOURCES = (
        dependency_change_policy,
        dependency_provenance_license,
        dependency_failure_handling,
        architecture_reuse_section,
    )

    def test_no_new_gate_state_is_introduced_in_the_new_clauses(self) -> None:
        for source in self.ALL_NEW_TEXT_SOURCES:
            section_text = source()
            used = set(re.findall(r"`(PASS|FAIL|BLOCKED|NOT_RUN|NOT_APPLICABLE|UNKNOWN|STALE)`", section_text))
            minted = used - CANONICAL_GATE_STATES
            self.assertFalse(minted, f"{source.__name__}: {minted}")

    def test_no_blanket_vending_or_universal_legal_verdict(self) -> None:
        for text in (dependency_standard(), architecture_standard()):
            self.assertNotIn("MUST vendor", text)
            self.assertNotIn("MUST be vendored", text)
            self.assertNotIn("license PASS", text)
            self.assertNotIn("reuse is lawful", text)

    def test_no_second_research_lifecycle_or_l2_takeover(self) -> None:
        section_text = architecture_reuse_section()
        self.assertNotIn("replaces L2", section_text)
        self.assertNotIn("owns L2 research", section_text)
        self.assertNotIn("auto-promotes across L1→L2→L3 is allowed", section_text)

    def test_decision_model_never_mints_gate_or_release_states(self) -> None:
        fixtures = [
            h1_case(),
            h1_case(copied_source=True),
            h2_case(),
            h2_case(origin_disclosed=False),
            h3_case(),
            h3_case(upstream_full_sha=None),
            build_new_case(),
            build_new_case(decision_owner=None),
        ]
        for case in fixtures:
            with self.subTest(subject=case["subject"]):
                verdict = evaluate_reuse(case)
                self.assertIn(verdict["decision"], ALLOWED_DECISIONS)
                self.assertNotIn(verdict["decision"], {"PASS", "NOT_APPLICABLE", "RELEASE_PASS"})
                self.assertTrue(verdict["grants"] <= ALLOWED_GRANTS)
                self.assertEqual(verdict["gate_mutations"], ())


class CrossOwnerScopeReconciliationTests(unittest.TestCase):
    """F04: Dependency §9 and ADS §15 must agree at their clause intersection.

    The full artifact/license floor is scoped to reuse-right-bearing material
    (physically copied source or artifacts, especially H3); H1/H2 carry the
    mode-matched provenance floors of ADS §15. Neither side may claim the
    unrestricted three-mode binding again, and the decision model must agree
    with the reconciled scoping.
    """

    def test_dependency_floor_is_scoped_to_reuse_right_bearing_material(self) -> None:
        section_text = dependency_provenance_license()
        # The unrestricted binding of pattern/re-specification/direct reuse to
        # the full floor is gone.
        self.assertNotIn(
            "an upstream pattern, a re-specified module or directly reused source — is additionally bound",
            section_text,
        )
        self.assertIn("reuse-right-bearing material", section_text)
        self.assertIn("physically copied upstream source or artifacts", section_text)
        self.assertIn("mode-matched", section_text)
        self.assertIn("ARCHITECTURE_DESIGN_STANDARD.md", section_text)
        # The direct-copy escape hatch stays closed on the Dependency side too.
        self.assertIn("never lowers the direct-copy rule", section_text)

    def test_architecture_section_mirrors_the_scoping_without_lowering_direct_copy(self) -> None:
        section_text = architecture_reuse_section()
        self.assertIn("mode-matched", section_text)
        self.assertIn("DEPENDENCY_TOOLCHAIN_GOVERNANCE_STANDARD.md", section_text)
        self.assertIn("reuse-right-bearing material", section_text)
        self.assertIn("physically copied upstream source or artifacts", section_text)
        self.assertIn("artifact parity with upstream", section_text)
        self.assertIn("never lowers the direct-copy rule", section_text)

    def test_decision_model_agrees_with_reconciled_floor_scoping(self) -> None:
        # Text/model intersection: pattern-only H1 needs no pinned SHA, while
        # the same cases with physical copying or artifact parity demand the
        # full H3 floor.
        clean = evaluate_reuse(h1_case(subject="reconciled H1, no copy"))
        self.assertEqual(clean["decision"], "ALLOWED")
        self.assertNotIn("pinned_full_sha", clean["missing"])
        copied_h1 = evaluate_reuse(
            h1_case(subject="reconciled H1 with copy", copied_source=True)
        )
        self.assertEqual(copied_h1["mode"], "DIRECT_CODE_REUSE")
        self.assertIn("pinned_full_sha", copied_h1["missing"])
        copied_h2 = evaluate_reuse(
            h2_case(subject="reconciled H2 with copy", copied_source=True)
        )
        self.assertEqual(copied_h2["mode"], "DIRECT_CODE_REUSE")
        self.assertNotEqual(copied_h2["decision"], "ALLOWED")
        parity_h2 = evaluate_reuse(
            h2_case(subject="reconciled H2 at parity", upstream_artifact_parity=True)
        )
        self.assertEqual(parity_h2["mode"], "DIRECT_CODE_REUSE")
        self.assertNotEqual(parity_h2["decision"], "ALLOWED")


class ContractBoundDecisionTraceTests(unittest.TestCase):
    """F05: verdicts are traced to the owner clauses that require them.

    Keyword-only self-attestation is not acceptance: each refusal is checked
    against the §13 routing clause that mandates it, each allowance against
    the floor clauses that define it, and material facts must converge on the
    same floor across every claimed label. Losing the owner clause or
    loosening the model makes these tests fail in either direction.
    """

    def test_every_refusal_is_backed_by_the_owner_failure_routing_clause(self) -> None:
        routing = dependency_failure_handling()
        refusal_clause = {
            "BLOCKED": "keep the reuse disposition non-authoritative (`BLOCKED`/unknown)",
            "STALE": "the prior permission is stale",
            "UNKNOWN": "keep the reuse disposition non-authoritative (`BLOCKED`/unknown)",
        }
        refusal_matrix = [
            h3_case(subject="trace unknown identity", upstream_full_sha=None),
            h3_case(subject="trace no owner evidence", evidence_sources=["unknown_checker"]),
            h3_case(subject="trace stale citation", l2_cited_revision="a" * 40),
            h3_case(subject="trace stale path", upstream_path_drift=True),
            h3_case(subject="trace stale behavior", upstream_behavior_drift=True),
            h3_case(subject="trace stale reliance", current_reliance_revision="c" * 40),
            h3_case(subject="trace license drift", upstream_license_changed=True),
            h3_case(subject="trace notice drift", upstream_notice_changed=True),
            h3_case(subject="trace conflicting license", license_observation="conflicting"),
            h3_case(subject="trace no policy", license_policy_authorized=False),
            h2_case(subject="trace laundering", origin_disclosed=False),
            h2_case(subject="trace copied under H2", copied_source=True),
            h1_case(subject="trace copied under H1", copied_source=True),
            build_new_case(subject="trace silent build-new", decision_owner=None),
        ]
        for case in refusal_matrix:
            verdict = evaluate_reuse(case)
            with self.subTest(subject=case["subject"], decision=verdict["decision"]):
                self.assertIn(verdict["decision"], refusal_clause)
                self.assertEqual(verdict["grants"], frozenset())
                self.assertEqual(verdict["gate_mutations"], ())
                self.assertIn(refusal_clause[verdict["decision"]], routing)

    def test_every_allowance_is_backed_by_the_owner_floor_clauses(self) -> None:
        dep9 = dependency_provenance_license()
        arch15 = architecture_reuse_section()
        allowance_matrix = [
            (
                h1_case(subject="trace allowed H1"),
                arch15,
                ("Pattern harvest (H1)", "mode-matched"),
            ),
            (
                h2_case(subject="trace allowed H2"),
                arch15,
                ("Source-inspired re-specification (H2)", "differential/behavior/failure tests"),
            ),
            (
                h3_case(subject="trace allowed H3"),
                dep9,
                (
                    "the upstream repository, the full commit SHA relied on",
                    "the license file and NOTICE content as observed at that revision",
                    "the project license-policy disposition authorizing the specific reuse mode",
                ),
            ),
            (
                build_new_case(subject="trace allowed BUILD_NEW"),
                arch15,
                ("BUILD_NEW", "It is not a silent default"),
            ),
        ]
        for case, clause_text, backing_phrases in allowance_matrix:
            verdict = evaluate_reuse(case)
            with self.subTest(subject=case["subject"]):
                self.assertEqual(verdict["decision"], "ALLOWED")
                self.assertEqual(verdict["gate_mutations"], ())
                for phrase in backing_phrases:
                    self.assertIn(phrase, clause_text)

    def test_material_facts_force_the_same_floor_across_all_claimed_labels(self) -> None:
        # Cross-mode invariant: the same physically-copied material labelled
        # four different ways converges on one H3-floor verdict, and an honest
        # H3 claim over the same missing facts is refused just as hard.
        stripped = {
            "upstream_repo": None,
            "upstream_full_sha": None,
            "material_paths": None,
            "license_observation": None,
            "notice_observation": None,
            "license_policy_authorized": False,
            "attribution": False,
            "local_behavior_tests": False,
            "evidence_sources": ["inspected_upstream"],
        }
        label_variants = (
            {"claimed_mode": "FAST_PATH", "material_upstream_delta": True},
            {"claimed_mode": "FAST_PATH", "copied_source": True},
            {"claimed_mode": "H1", "copied_source": True},
            {"claimed_mode": "H2", "copied_source": True},
        )
        baseline = None
        for variant in label_variants:
            verdict = evaluate_reuse(
                {**stripped, "subject": "material invariance", **variant}
            )
            with self.subTest(claimed=variant["claimed_mode"]):
                self.assertEqual(verdict["mode"], "DIRECT_CODE_REUSE")
                self.assertNotIn(verdict["decision"], {"ALLOWED", "FAST_PATH_ALLOWED"})
                self.assertIn("validation_impact", verdict["obligations"])
                self.assertEqual(verdict["grants"], frozenset())
                self.assertEqual(verdict["gate_mutations"], ())
            if baseline is None:
                baseline = verdict
            else:
                self.assertEqual(verdict["decision"], baseline["decision"])
                self.assertEqual(verdict["missing"], baseline["missing"])
        honest_h3 = evaluate_reuse(
            {**stripped, "subject": "material invariance", "claimed_mode": "H3"}
        )
        self.assertEqual(honest_h3["decision"], baseline["decision"])
        self.assertEqual(honest_h3["missing"], baseline["missing"])

    def test_acceptance_limitations_are_recorded_as_not_run(self) -> None:
        self.assertEqual(
            set(NOT_RUN_OBLIGATIONS),
            {"T11", "T12", "upstream_readback", "production_contract", "real_build_host"},
        )
        for obligation, note in NOT_RUN_OBLIGATIONS.items():
            with self.subTest(obligation=obligation):
                self.assertTrue(note.strip())
        # The module docstring states the boundary honestly: this suite is
        # owner-local offline acceptance only — it cannot claim completeness
        # for central wiring (T11), executed evidence (T12), an online
        # production contract, or real upstream observation.
        doc = sys.modules[__name__].__doc__ or ""
        self.assertIn("Acceptance boundary (NOT_RUN)", doc)
        self.assertIn("owner-local offline", doc)
        self.assertIn("not an online production contract", doc)
        self.assertIn("T11", doc)
        self.assertIn("T12", doc)
        self.assertIn("NOT_RUN_OBLIGATIONS", doc)


class RevisionBoundObservationTests(unittest.TestCase):
    """F01/R2: every observation is an independent fact pinned to the relied revision.

    A license/NOTICE/source observation taken at another revision is history,
    never current authority; a green status without a revision binding at all
    is unattributable; either half of the license/NOTICE pair alone does not
    authorize.
    """

    def test_f01_observations_at_old_revision_do_not_authorize_new_reliance(self) -> None:
        # The exact R2 finding: green license/NOTICE/source booleans observed
        # at revision A carried over to a reliance on revision B must not stay
        # ALLOWED — the reliance goes stale until freshly re-observed at B.
        verdict = evaluate_reuse(
            h3_case(
                subject="F01 A observations, B reliance",
                historic_permission_revision="a" * 40,
                current_reliance_revision="b" * 40,
                source_observation_revision="a" * 40,
                source_observation_blob="blob:src/example.rs@a",
                license_observation_revision="a" * 40,
                license_observation_content="license-text@a:MIT",
                notice_observation_revision="a" * 40,
                notice_observation_content="notice-content@a",
            )
        )
        self.assertEqual(verdict["decision"], "STALE")
        self.assertNotIn("bounded_code_reuse", verdict["grants"])
        self.assertEqual(verdict["grants"], frozenset())
        self.assertTrue(verdict["notes"]["observation_bound_to_other_revision"])
        for marker in (
            "source_observation_at_relied_revision",
            "inspected_license_observation_at_relied_revision",
            "notice_observation_at_relied_revision",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, verdict["missing"])
        for obligation in ("fresh_equivalence_source_check", "validation_impact"):
            with self.subTest(obligation=obligation):
                self.assertIn(obligation, verdict["obligations"])
        self.assertEqual(verdict["gate_mutations"], ())

    def test_f01_one_misbound_observation_is_enough_to_go_stale(self) -> None:
        # A-observation must not silently inherit into B-reliance — even a
        # single observation identity pinned at the old revision breaks the
        # authorization.
        verdict = evaluate_reuse(
            h3_case(
                subject="F01 license still pinned at A",
                current_reliance_revision="c" * 40,
                upstream_full_sha="c" * 40,
                source_observation_revision="c" * 40,
                source_observation_blob="blob:src/example.rs@c",
                license_observation_revision="a" * 40,
                license_observation_content="license-text@a:MIT",
                notice_observation_revision="c" * 40,
                notice_observation_content="notice-content@c",
                license_policy_revision="c" * 40,
            )
        )
        self.assertEqual(verdict["decision"], "STALE")
        self.assertIn("inspected_license_observation_at_relied_revision", verdict["missing"])
        self.assertTrue(verdict["notes"]["observation_bound_to_other_revision"])
        self.assertEqual(verdict["grants"], frozenset())
        self.assertEqual(verdict["gate_mutations"], ())

    def test_f01_green_status_without_revision_binding_fails_closed(self) -> None:
        # The unbound variant of the same hole: green booleans with no
        # observation identity at all are unattributable memory, not
        # observation, and fail closed instead of authorizing.
        verdict = evaluate_reuse(
            h3_case(
                subject="F01 unbound green booleans",
                source_observation_revision=None,
                source_observation_blob=None,
                license_observation_revision=None,
                license_observation_content=None,
                notice_observation_revision=None,
                notice_observation_content=None,
            )
        )
        self.assertEqual(verdict["decision"], "BLOCKED")
        self.assertNotIn("bounded_code_reuse", verdict["grants"])
        for marker in (
            "source_observation_at_relied_revision",
            "inspected_license_observation_at_relied_revision",
            "notice_observation_at_relied_revision",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, verdict["missing"])
        self.assertIn("license_authority_disposition", verdict["obligations"])
        self.assertEqual(verdict["gate_mutations"], ())

    def test_f01_notice_observation_alone_does_not_authorize(self) -> None:
        verdict = evaluate_reuse(
            h3_case(
                subject="F01 NOTICE observed, license not",
                license_observation=None,
                license_observation_revision=None,
                license_observation_content=None,
            )
        )
        self.assertEqual(verdict["decision"], "BLOCKED")
        self.assertIn("inspected_license_observation_at_relied_revision", verdict["missing"])
        self.assertIn("license_authority_disposition", verdict["obligations"])
        self.assertEqual(verdict["grants"], frozenset())
        self.assertEqual(verdict["gate_mutations"], ())

    def test_f01_license_observation_alone_does_not_authorize(self) -> None:
        verdict = evaluate_reuse(
            h3_case(
                subject="F01 license observed, NOTICE not",
                notice_observation=None,
                notice_observation_revision=None,
                notice_observation_content=None,
            )
        )
        self.assertEqual(verdict["decision"], "BLOCKED")
        self.assertIn("notice_observation_at_relied_revision", verdict["missing"])
        self.assertEqual(verdict["grants"], frozenset())
        self.assertEqual(verdict["gate_mutations"], ())

    def test_f01_independent_observations_are_checked_one_by_one(self) -> None:
        # Source, license-file and NOTICE are distinct observation identities:
        # binding two of them to the relied revision while the third stays at
        # the old one leaves exactly the third broken, and never inherits.
        verdict = evaluate_reuse(
            h3_case(
                subject="F01 per-identity binding",
                current_reliance_revision="c" * 40,
                upstream_full_sha="c" * 40,
                license_policy_revision="c" * 40,
            )
        )
        self.assertEqual(verdict["decision"], "STALE")
        self.assertEqual(
            [m for m in verdict["missing"] if m.endswith("_at_relied_revision")],
            [
                "source_observation_at_relied_revision",
                "inspected_license_observation_at_relied_revision",
                "notice_observation_at_relied_revision",
            ],
        )
        self.assertEqual(verdict["grants"], frozenset())
        self.assertEqual(verdict["gate_mutations"], ())


class InspectorPolicyRoleSeparationTests(unittest.TestCase):
    """F02/R2: upstream inspector and project license-policy owner are distinct roles.

    An authoritative bounded-reuse verdict needs both an independently
    attributable current upstream inspection AND an independent project
    license-policy ruling (owner decision); neither role can be swapped,
    inherited or self-declared by a green boolean.
    """

    def test_f02_owner_decision_alone_cannot_replace_current_inspection(self) -> None:
        verdict = evaluate_reuse(
            h3_case(
                subject="F02 owner-only",
                evidence_sources=["owner_decision"],
            )
        )
        self.assertEqual(verdict["decision"], "BLOCKED")
        self.assertIn("current_upstream_inspection_evidence", verdict["missing"])
        self.assertNotIn("bounded_code_reuse", verdict["grants"])
        self.assertEqual(verdict["gate_mutations"], ())

    def test_f02_inspection_alone_cannot_issue_the_license_policy_ruling(self) -> None:
        # A green `license_policy_authorized` boolean without an independent
        # owner attribution rules nothing — the inspector cannot self-issue
        # the project policy disposition.
        verdict = evaluate_reuse(
            h3_case(
                subject="F02 inspector-only",
                evidence_sources=["inspected_upstream"],
                license_policy_authority=None,
            )
        )
        self.assertEqual(verdict["decision"], "BLOCKED")
        self.assertIn("independent_license_policy_authority", verdict["missing"])
        self.assertNotIn("bounded_code_reuse", verdict["grants"])
        self.assertEqual(verdict["gate_mutations"], ())

    def test_f02_inherited_policy_without_current_inspection_is_denied(self) -> None:
        # A policy ruling recorded at the historic revision, carried forward
        # with no current upstream inspection, is inherited history and denies.
        verdict = evaluate_reuse(
            h3_case(
                subject="F02 inherited policy",
                evidence_sources=["owner_decision"],
                license_policy_revision="a" * 40,
            )
        )
        self.assertEqual(verdict["decision"], "BLOCKED")
        self.assertIn("current_upstream_inspection_evidence", verdict["missing"])
        self.assertIn("license_policy_disposition_at_relied_revision", verdict["missing"])
        self.assertNotIn("bounded_code_reuse", verdict["grants"])
        self.assertEqual(verdict["gate_mutations"], ())

    def test_f02_recorded_disposition_cannot_serve_as_upstream_inspection(self) -> None:
        # Role non-interchangeability on the owner side: a recorded prior
        # disposition is owner evidence, but it is not a current upstream
        # inspection and cannot stand in for one.
        verdict = evaluate_reuse(
            h3_case(
                subject="F02 recorded disposition is not inspection",
                evidence_sources=["recorded_disposition", "owner_decision"],
            )
        )
        self.assertEqual(verdict["decision"], "BLOCKED")
        self.assertIn("current_upstream_inspection_evidence", verdict["missing"])
        self.assertNotIn("bounded_code_reuse", verdict["grants"])
        self.assertEqual(verdict["gate_mutations"], ())

    def test_f02_both_roles_present_with_revision_bound_facts_authorize(self) -> None:
        # Control: the split does not over-block. With both roles present and
        # every observation bound to the relied revision, the bounded grant
        # survives.
        verdict = evaluate_reuse(h3_case(subject="F02 control"))
        self.assertEqual(verdict["decision"], "ALLOWED")
        self.assertEqual(verdict["missing"], [])
        self.assertEqual(verdict["grants"], frozenset({"bounded_code_reuse"}))
        self.assertEqual(verdict["gate_mutations"], ())


class MaterialDriftNonCopyModeTests(unittest.TestCase):
    """F03/R2: material rights-bearing drift fails closed in every non-copying mode.

    The mode keeps its shape and floor (no blanket H3 demotion and no copying
    boolean involved), but an ALLOWED verdict may not rest on a stale
    self-description: refreshed, mode-matched evidence is required, otherwise
    the verdict is STALE with fresh-check plus Validation Impact obligations.
    """

    def test_f03_h1_material_delta_without_refreshed_evidence_is_stale(self) -> None:
        verdict = evaluate_reuse(h1_case(subject="F03 H1 stale self-description", material_upstream_delta=True))
        self.assertEqual(verdict["mode"], "PATTERN_HARVEST")
        self.assertEqual(verdict["decision"], "STALE")
        self.assertTrue(verdict["notes"]["stale_material_self_description"])
        self.assertNotIn("pinned_full_sha", verdict["missing"])  # no blanket H3 floor
        for obligation in ("fresh_equivalence_source_check", "validation_impact"):
            with self.subTest(obligation=obligation):
                self.assertIn(obligation, verdict["obligations"])
        self.assertEqual(verdict["grants"], frozenset())
        self.assertEqual(verdict["gate_mutations"], ())

    def test_f03_h2_material_delta_without_refreshed_evidence_is_stale(self) -> None:
        verdict = evaluate_reuse(h2_case(subject="F03 H2 stale self-description", material_upstream_delta=True))
        self.assertEqual(verdict["mode"], "SPEC_MODULE_RECONSTRUCTION")
        self.assertEqual(verdict["decision"], "STALE")
        self.assertTrue(verdict["notes"]["stale_material_self_description"])
        self.assertNotIn("pinned_full_sha", verdict["missing"])  # no blanket H3 floor
        self.assertIn("validation_impact", verdict["obligations"])
        self.assertEqual(verdict["grants"], frozenset())
        self.assertEqual(verdict["gate_mutations"], ())

    def test_f03_build_new_material_delta_without_refreshed_evidence_is_stale(self) -> None:
        verdict = evaluate_reuse(
            build_new_case(subject="F03 BUILD_NEW stale self-description", material_upstream_delta=True)
        )
        self.assertEqual(verdict["mode"], "BUILD_NEW")
        self.assertEqual(verdict["decision"], "STALE")
        self.assertTrue(verdict["notes"]["stale_material_self_description"])
        self.assertNotIn("pinned_full_sha", verdict["missing"])  # no blanket H3 floor
        self.assertIn("validation_impact", verdict["obligations"])
        self.assertEqual(verdict["grants"], frozenset())
        self.assertEqual(verdict["gate_mutations"], ())

    def test_f03_refreshed_mode_matched_evidence_restores_the_mode_verdict(self) -> None:
        # Positive controls: with refreshed mode-matched evidence the mode's
        # own verdict stands (minus the grant-erasing downgrade); the material
        # delta still keeps the Validation Impact obligation.
        cases = [
            h1_case(subject="F03 H1 refreshed", material_upstream_delta=True, refreshed_mode_matched_evidence=True),
            h2_case(subject="F03 H2 refreshed", material_upstream_delta=True, refreshed_mode_matched_evidence=True),
            build_new_case(subject="F03 BUILD_NEW refreshed", material_upstream_delta=True, refreshed_mode_matched_evidence=True),
        ]
        for case in cases:
            verdict = evaluate_reuse(case)
            with self.subTest(subject=case["subject"]):
                self.assertEqual(verdict["decision"], "ALLOWED")
                self.assertIn("validation_impact", verdict["obligations"])
                self.assertNotIn("stale_material_self_description", verdict["notes"])
                self.assertEqual(verdict["gate_mutations"], ())
        self.assertEqual(
            evaluate_reuse(cases[1])["grants"],
            frozenset({"local_spec_module"}),
        )


class IndependentOracleFalsificationTests(unittest.TestCase):
    """F04/R2: negative fixtures derived independently of the decision model.

    The required facts and the routing are re-derived here from the owner
    clause text (Dependency §9/§13) with predicates over the raw fixture
    dict; they never call or mirror `evaluate_reuse`. A loosening of the
    model or a weakening of the clauses breaks the agreement in either
    direction, so the model and the document falsify together instead of
    self-attesting. All fixtures stay synthetic and offline.
    """

    maxDiff = None

    # (§9 clause phrase that must back the fact, raw-case predicate)
    @classmethod
    def floor_fact_groups(cls) -> list[tuple[str, object]]:
        return [
            (
                "the upstream repository, the full commit SHA relied on",
                cls.has_pinned_identity,
            ),
            (
                "exact provenance facts observed at a named upstream revision",
                cls.has_current_inspection_evidence,
            ),
            (
                "the license file and NOTICE content as observed at that revision",
                cls.has_revision_bound_license_and_notice,
            ),
            (
                "the project license-policy disposition authorizing the specific reuse mode",
                cls.has_independent_policy_ruling,
            ),
        ]

    @staticmethod
    def relied_revision(case: dict) -> str:
        current = case.get("current_reliance_revision")
        if current:
            return current
        sha = case.get("upstream_full_sha") or ""
        return sha if FULL_SHA_RE.match(sha) else ""

    @classmethod
    def has_pinned_identity(cls, case: dict) -> bool:
        return (
            bool(case.get("upstream_repo"))
            and bool(cls.relied_revision(case))
            and bool(case.get("material_paths"))
        )

    @staticmethod
    def has_current_inspection_evidence(case: dict) -> bool:
        return "inspected_upstream" in set(case.get("evidence_sources", []))

    @classmethod
    def has_revision_bound_license_and_notice(cls, case: dict) -> bool:
        relied = cls.relied_revision(case)
        if not relied:
            return False
        return (
            case.get("license_observation") == "inspected_authorized"
            and case.get("license_observation_revision") == relied
            and bool(case.get("license_observation_content"))
            and case.get("notice_observation") == "present"
            and case.get("notice_observation_revision") == relied
            and bool(case.get("notice_observation_content"))
        )

    @classmethod
    def has_independent_policy_ruling(cls, case: dict) -> bool:
        relied = cls.relied_revision(case)
        return (
            case.get("license_policy_authorized") is True
            and case.get("license_policy_authority") == "owner_decision"
            and "owner_decision" in set(case.get("evidence_sources", []))
            and bool(relied)
            and case.get("license_policy_revision") == relied
        )

    @classmethod
    def observation_pinned_elsewhere(cls, case: dict) -> bool:
        relied = cls.relied_revision(case)
        if not relied:
            return False
        pinned = (
            (bool(case.get("source_observation_blob")), case.get("source_observation_revision")),
            (case.get("license_observation") == "inspected_authorized", case.get("license_observation_revision")),
            (case.get("notice_observation") == "present", case.get("notice_observation_revision")),
        )
        return any(claimed and revision and revision != relied for claimed, revision in pinned)

    @classmethod
    def independent_disposition(cls, case: dict) -> str:
        """Route from the §13 clause semantics, not from `evaluate_reuse`."""
        if cls.observation_pinned_elsewhere(case):
            return "STALE"
        dep9 = dependency_provenance_license()
        for phrase, predicate in cls.floor_fact_groups():
            if phrase not in dep9:
                raise AssertionError(f"backing clause disappeared from Dependency §9: {phrase!r}")
            if not predicate(case):
                return "NOT_ALLOWED"
        return "ALLOWED"

    def test_backing_clauses_are_present_in_the_owner_sections(self) -> None:
        dep9 = dependency_provenance_license()
        routing = dependency_failure_handling()
        for phrase, _predicate in self.floor_fact_groups():
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, dep9)
        self.assertIn("These observations are revision-bound.", dep9)
        self.assertIn("the prior permission is stale", routing)
        self.assertIn(
            "keep the reuse disposition non-authoritative (`BLOCKED`/unknown)",
            routing,
        )

    def test_full_floor_fixture_matches_the_independent_derivation(self) -> None:
        case = h3_case(subject="independent full-floor control")
        derived = self.independent_disposition(case)
        verdict = evaluate_reuse(case)
        self.assertEqual(derived, "ALLOWED")
        self.assertEqual(verdict["decision"], "ALLOWED")
        self.assertEqual(verdict["grants"], frozenset({"bounded_code_reuse"}))
        self.assertEqual(verdict["gate_mutations"], ())

    def test_negative_fixtures_match_the_independent_derivation(self) -> None:
        a, b, c = "a" * 40, "b" * 40, "c" * 40
        matrix = [
            h3_case(subject="ind owner-only", evidence_sources=["owner_decision"]),
            h3_case(
                subject="ind inspector-only",
                evidence_sources=["inspected_upstream"],
                license_policy_authority=None,
            ),
            h3_case(subject="ind inherited policy", evidence_sources=["owner_decision"], license_policy_revision=a),
            h3_case(
                subject="ind A observations, B reliance",
                historic_permission_revision=a,
                current_reliance_revision=b,
                source_observation_revision=a,
                source_observation_blob="blob:src@a",
                license_observation_revision=a,
                license_observation_content="license@a",
                notice_observation_revision=a,
                notice_observation_content="notice@a",
            ),
            h3_case(
                subject="ind one misbound observation",
                current_reliance_revision=c,
                upstream_full_sha=c,
                license_observation_revision=a,
                license_observation_content="license@a",
                license_policy_revision=c,
            ),
            h3_case(
                subject="ind license only",
                notice_observation=None,
                notice_observation_revision=None,
                notice_observation_content=None,
            ),
            h3_case(
                subject="ind notice only",
                license_observation=None,
                license_observation_revision=None,
                license_observation_content=None,
            ),
            h3_case(
                subject="ind unbound green booleans",
                source_observation_revision=None,
                source_observation_blob=None,
                license_observation_revision=None,
                license_observation_content=None,
                notice_observation_revision=None,
                notice_observation_content=None,
            ),
            h3_case(subject="ind unknown checker", evidence_sources=["unknown_checker"]),
        ]
        for case in matrix:
            derived = self.independent_disposition(case)
            verdict = evaluate_reuse(case)
            with self.subTest(subject=case["subject"], derived=derived, actual=verdict["decision"]):
                self.assertNotEqual(derived, "ALLOWED")
                if derived == "STALE":
                    self.assertEqual(verdict["decision"], "STALE")
                else:
                    self.assertIn(verdict["decision"], {"BLOCKED", "UNKNOWN"})
                self.assertEqual(verdict["grants"], frozenset())
                self.assertEqual(verdict["gate_mutations"], ())

    def test_independent_floor_stays_scoped_to_right_bearing_material(self) -> None:
        # Scope control on the independent side: pattern harvest without any
        # copying stays outside the §9 identity floor on both sides, and the
        # in-file floor_fact_groups must not silently bind it.
        case = h1_case(subject="independent H1 out of scope")
        verdict = evaluate_reuse(case)
        self.assertEqual(verdict["decision"], "ALLOWED")
        self.assertEqual(verdict["mode"], "PATTERN_HARVEST")
        self.assertNotIn("pinned_full_sha", verdict["missing"])


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
