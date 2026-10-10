"""V411-T04 focused test: reuse-first modes and source/license currentness.

Encodes the V411-T04 task-pack §3 positive/negative oracles (P01–P05, N01–N07)
as (a) section-scoped textual contract checks binding the decision model to the
owner-local clauses in `standards/DEPENDENCY_TOOLCHAIN_GOVERNANCE_STANDARD.md`
(§6 reuse materiality, §9 exact source/license/NOTICE currentness, §13 failure
routing) and `standards/ARCHITECTURE_DESIGN_STANDARD.md` (§15 reuse-first
adoption and BUILD_NEW), and (b) fixture-driven deterministic decisions over
the J12 H1/H2/H3/BUILD_NEW contract including license drift, revision staleness
and fail-closed routing. Purely textual/offline; no network, no runtime.
"""

from __future__ import annotations

from pathlib import Path
import re
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
    revision/path drift is stale; missing license/NOTICE/rights facts fail
    closed to the project license/security authority. The model never emits
    gate-state mutations or release permission.
    """
    missing: list[str] = []
    obligations: set[str] = set()
    grants: frozenset = frozenset()
    notes: dict = {}
    mode = MODE_ALIASES[case["claimed_mode"]]

    # N06: an actual vendored-source or license delta overrides docs-only/A0/
    # Fast-Path labels; the material mode's full floor still applies.
    if case.get("label_only_claim") and case.get("material_upstream_delta"):
        obligations.add("validation_impact")
        notes["fast_path_refused"] = True
        mode = MODE_ALIASES[case["actual_mode"]]

    # N07: untrusted evidence never substitutes an owner decision or real
    # current validation.
    untrusted = [
        source
        for source in case.get("evidence_sources", [])
        if source in UNTRUSTED_EVIDENCE_SOURCES
    ]
    for source in untrusted:
        missing.append(f"owner_or_inspected_evidence:{source}")

    decision: str
    if mode == "FAST_PATH":
        # P05: proportional Fast Path without mandatory research/catalog.
        decision = "FAST_PATH_ALLOWED"

    elif mode == "PATTERN_HARVEST":
        if case.get("copied_source"):
            # P01: H1 cannot carry copied source; it fails closed at the H3 floor.
            mode = "DIRECT_CODE_REUSE"
        else:
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
            bool(untrusted)
            or not case.get("upstream_repo")
            or not FULL_SHA_RE.match(sha)
            or not case.get("material_paths")
        )
        if not case.get("upstream_repo"):
            missing.append("upstream_repo")
        if not FULL_SHA_RE.match(sha):
            missing.append("pinned_full_sha")
        if not case.get("material_paths"):
            missing.append("material_paths")

        # N01: reliance on a new revision never inherits the historic permission.
        historic = case.get("historic_permission_revision")
        current = case.get("current_reliance_revision")
        if historic and current and historic != current:
            notes["historic_permission_preserved"] = {
                "revision": historic,
                "inheritable": False,
            }
            obligations.update({"license_authority_disposition", "validation_impact"})
            if case.get("upstream_license_changed") or case.get("upstream_notice_changed"):
                missing.append("license_notice_observation_at_current_revision")

        # N02: cited-vs-used revision mismatch or path drift is stale.
        stale = (
            bool(case.get("l2_cited_revision")) and bool(sha) and case["l2_cited_revision"] != sha
        ) or bool(case.get("upstream_path_drift"))
        if stale:
            obligations.add("fresh_equivalence_source_check")

        if case.get("license_observation") != "inspected_authorized":
            missing.append("inspected_license_observation_at_relied_revision")
            if case.get("license_observation") in ("conflicting", "missing"):
                obligations.add("license_authority_disposition")
        if case.get("notice_observation") != "present":
            missing.append("notice_observation_at_relied_revision")
        if not case.get("license_policy_authorized"):
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
    case = {
        "subject": "H3 fixture",
        "claimed_mode": "H3",
        "upstream_repo": "upstream/example-lib",
        "upstream_full_sha": "b" * 40,
        "material_paths": ["src/example.rs"],
        "license_observation": "inspected_authorized",
        "notice_observation": "present",
        "license_policy_authorized": True,
        "attribution": True,
        "local_behavior_tests": True,
        "evidence_sources": ["inspected_upstream", "recorded_disposition"],
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


if __name__ == "__main__":
    import sys

    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
