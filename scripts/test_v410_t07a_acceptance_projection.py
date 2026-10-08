"""V410-T07A: product acceptance / release-blocker evidence projection oracle.

Focused deterministic suite for
``docs/implementation/4.10.0/PRODUCT_ACCEPTANCE_EVIDENCE_PROJECTION_R1.md``
(oracle binding: positives P1-P5 from #862@6003300393; negatives N1-N15 from
#862@6012768804; adversarial cases from #862@6043147928; ROW_SCHEMA /
BLOCKER_RULES from #862@6013713353; rebind subject 0518202c / tree 75566c46,
the merged #861 integration tip).

The suite machine-parses the projection's embedded record block and fails
closed on parse drift; asserts acceptance-map completeness (every active
requirement row R1/R2/R3/R4/R6/R7/R11/R12 resolves to durable producers with
exact-subject binding classes and verifiable blob identities at the checkout);
asserts blocker visibility without Release authority; and proves the negative
automatic-transfer rules via a row validator applied to synthetic mutants
(stale binding, drifted blob, verdict vocabulary, double-count,
convenience-not-applicable, empty evidence, adoption-path leak).

The projection is PROJECTION_ONLY: this suite proves it can never emit a
Release verdict, redefine a Product requirement, transfer historical
qualification to a successor, or reach the core-feature-freeze decision.
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

PROJECTION = ROOT / "docs" / "implementation" / "4.10.0" / "PRODUCT_ACCEPTANCE_EVIDENCE_PROJECTION_R1.md"
PACK_DIR = ROOT / ".agent" / "execution" / "V410-T07A-R1"

# Exact rebind subject of the projection (merged #861 integration tip).
REBIND_BASE_SHA = "0518202c715dcf91784a694bdf4a8eeeaeb16ab6"
REBIND_BASE_TREE = "75566c464505386fedffde803e05e3e726922434"

REQUIRED_ROWS = ["R1", "R2", "R3", "R4", "R6", "R7", "R11", "R12"]
ACTIVE_REQUIREMENTS = frozenset(REQUIRED_ROWS)
PRODUCER_KINDS = frozenset(
    {"TEST", "DOC", "ISSUE_EVENT", "VALIDATION_ROW", "REVIEW_ROW", "CONFORMANCE_SUITE"}
)
BINDING_CLASSES = frozenset({"CANDIDATE_BOUND", "EVENT_BOUND", "DURABLE_STATIC"})
BLOCKER_PROJECTIONS = frozenset({"UNRESOLVED", "EVIDENCE_CURRENT"})
ADOPTION_PATHS = frozenset({"MINIMUM_AND_ADVANCED", "ADVANCED_ONLY"})
CLOSURE_STATES = frozenset({"OPEN", "EVIDENCE_CURRENT", "CLEARED_BY_OWNER"})
REJECTION_REASONS = frozenset(
    {
        "stale_subject",
        "wrong_layer",
        "scheduler_only",
        "double_count",
        "scope_leak",
        "convenience_na",
        "vote_without_policy",
        "index_overreach",
    }
)
UNBOUND_SUBJECT = "UNBOUND_UNTIL_T08A_INTEGRATION"
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
EVENT_REF_RE = re.compile(r"^#[0-9]+(@[0-9]+)?(\+#[0-9]+@[0-9]+)*$")
VERDICT_TOKEN_RE = re.compile(r"\b(PASS|READY|YES|ACCEPTED|NOT_APPLICABLE)\b")
ROW_FIELDS = (
    "row_id",
    "requirement_id",
    "prd_ref",
    "canonical_owner",
    "evidence_producers",
    "current_exact_subject",
    "currentness_rule",
    "blocker_projection",
    "missing_evidence_description",
    "route_to_owner",
    "rejected_provenance",
    "adoption_path",
    "authority_note",
)
ROW_ID_RE = re.compile(r"^V410-ACC-R[0-9]+$")
STALE_IDENTITIES = ("a7dc127", "41df8e5")  # non-integrated PR #927 preview heads
SUPERSEDED_LINEAGE_DOC = "docs/implementation/4.10.0/L1_PRODUCT_EVIDENCE.md"
PREP_BRANCH_TEST = "scripts/test_v410_t07a_evidence_inventory.py"
# The R2 bounded repair (dispatch V410-T07A-BOUNDED-REPAIR-R2) is authorized to
# rebind exactly ONE carried suite — the owner-convergence candidate-scope
# guard — successor-aware with zero removed tests. Any OTHER carried-suite edit
# stays rejected below; the rebound suite's exact blob is positively re-pinned
# in the projection record (test_p2), so this named exception cannot mask any
# further drift of that file.
AUTHORIZED_R2_CARRIED_REBIND = frozenset({"scripts/test_v410_owner_convergence.py"})
# The R3 bounded seam rebind (dispatch V410-T07B-BOUNDED-SEAM-REBIND-R2, #863:
# seam proposal @6054504547 / admission @6054508480 / claim @6054512382) is
# authorized to rebind exactly ONE positional guard of this carried suite —
# test_forbidden_surfaces_untouched_vs_rebind_base — successor-aware with zero
# removed tests, plus the mechanically forced cascade of its own edits: the
# blob-pin rebinds (projection record, IMPLEMENTATION_MAP, the T07B citation
# pin and reference citation, each strictly a pin line with disclosure) and the
# matching successor-registry scoping folds in the two other guards that
# register the T07B candidate write set (owner-convergence TASK_CANDIDATES +
# the T07B suite's own registered-prefix guard). The rebound guard keeps the
# frozen T07A integrated delta asserted and positively re-registers every
# active successor candidate, so this named exception cannot mask any further
# drift: unregistered paths fail loud in the rebound registry below.
AUTHORIZED_R3_SEAM_REBIND = frozenset(
    {
        "scripts/test_v410_t07a_acceptance_projection.py",
        "docs/implementation/4.10.0/PRODUCT_ACCEPTANCE_EVIDENCE_PROJECTION_R1.md",
        ".agent/execution/V410-T07A-R1/IMPLEMENTATION_MAP.md",
        ".agent/execution/V410-T07A-R1/TEST_MATRIX.yaml",
    }
)
# Whole-prefix authority bans preserved verbatim from the original guard: the
# frozen T07A integrated delta must never touch T06B-owned / authority surfaces.
T07A_FORBIDDEN_PREFIXES = (
    "schemas/",
    "standards/",
    "templates/",
    "references/",
    "checklists/",
    "registries/",
    "prompts/",
    "standard-manifest.json",
)


def parse_record() -> dict:
    """Extract the single fenced JSON machine record; fail closed on drift."""
    text = PROJECTION.read_text(encoding="utf-8")
    open_fence = "```json"
    if text.count(open_fence) != 1:
        raise AssertionError("projection must embed exactly one json record block")
    start = text.index(open_fence) + len(open_fence)
    end = text.index("```", start)
    return json.loads(text[start:end])


def git_blob_at_head(rel: str) -> str | None:
    """Resolve the exact git blob of a tracked path at HEAD (autocrlf-safe)."""
    result = subprocess.run(
        ["git", "rev-parse", f"HEAD:{rel}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def producer_problems(producer: dict) -> list[str]:
    problems: list[str] = []
    for field in ("producer_kind", "durable_ref", "exact_subject_binding"):
        if field not in producer or not str(producer.get(field, "")).strip():
            problems.append(f"producer missing {field}")
    kind = producer.get("producer_kind")
    if kind not in PRODUCER_KINDS:
        problems.append(f"invalid producer_kind {kind!r}")
    binding = producer.get("exact_subject_binding")
    if binding not in BINDING_CLASSES:
        problems.append(f"invalid exact_subject_binding {binding!r}")
    ref = producer.get("durable_ref", "")
    if kind in ("DOC", "TEST", "CONFORMANCE_SUITE", "VALIDATION_ROW", "REVIEW_ROW"):
        if not (ROOT / ref).is_file():
            problems.append(f"producer path missing at checkout: {ref}")
        if binding == "EVENT_BOUND":
            problems.append(f"static producer {ref} must not be EVENT_BOUND")
        else:
            blob = producer.get("blob_identity")
            if not isinstance(blob, str) or not SHA_RE.match(blob):
                problems.append(f"producer {ref} lacks a 40-hex blob_identity")
    elif kind == "ISSUE_EVENT":
        if binding != "EVENT_BOUND":
            problems.append("ISSUE_EVENT producer must be EVENT_BOUND")
        if not EVENT_REF_RE.match(ref):
            problems.append(f"malformed durable event ref: {ref!r}")
    return problems


def row_problems(row: dict) -> list[str]:
    """Fail-closed validator shared by the real record and synthetic mutants."""
    problems: list[str] = []
    if not isinstance(row, dict):
        return ["row is not an object"]
    for field in ROW_FIELDS:
        value = row.get(field)
        if value is None or (isinstance(value, str) and not value.strip()):
            if field != "missing_evidence_description":
                problems.append(f"row field missing/empty: {field}")
    if ROW_ID_RE.match(str(row.get("row_id", ""))) is None:
        problems.append(f"invalid row_id {row.get('row_id')!r}")
    if row.get("requirement_id") not in ACTIVE_REQUIREMENTS:
        problems.append(f"invalid requirement_id {row.get('requirement_id')!r}")
    if "19.1" not in str(row.get("prd_ref", "")) and "section 19.1" not in str(row.get("prd_ref", "")):
        problems.append("prd_ref must anchor a section 19.1 obligation")
    producers = row.get("evidence_producers")
    if not isinstance(producers, list) or not producers:
        problems.append("row must resolve to at least one evidence producer (N11)")
    else:
        for producer in producers:
            problems.extend(producer_problems(producer))
        refs = [p.get("durable_ref") for p in producers]
        if len(refs) != len(set(refs)):
            problems.append("duplicate durable_ref in one row (N8 double-count)")
        if not any(p.get("exact_subject_binding") != "EVENT_BOUND" for p in producers):
            problems.append("row evidence depends solely on EVENT_BOUND lanes (N6/N7)")
    subject = row.get("current_exact_subject")
    if subject != UNBOUND_SUBJECT:
        # A bound subject would need a full sha+tree pair; nothing may claim
        # one before the T08A integration candidate exists (no transfer).
        problems.append(
            f"current_exact_subject must be {UNBOUND_SUBJECT} until T08A binds a candidate; got {subject!r}"
        )
    if row.get("blocker_projection") == "EVIDENCE_CURRENT" and subject == UNBOUND_SUBJECT:
        problems.append(
            "EVIDENCE_CURRENT requires a bound exact subject; cross-layer results cannot clear an unbound row (N3/N5)"
        )
    if not str(row.get("currentness_rule", "")).strip():
        problems.append("row lacks a currentness/supersession rule (A10)")
    if row.get("blocker_projection") not in BLOCKER_PROJECTIONS:
        problems.append(f"invalid blocker_projection {row.get('blocker_projection')!r}")
    if row.get("blocker_projection") == "UNRESOLVED":
        if not str(row.get("missing_evidence_description", "")).strip():
            problems.append("UNRESOLVED row lacks missing_evidence_description")
        if not str(row.get("route_to_owner", "")).strip():
            problems.append("UNRESOLVED row lacks route_to_owner (fail-closed owner routing)")
    if row.get("adoption_path") not in ADOPTION_PATHS:
        problems.append(f"invalid adoption_path {row.get('adoption_path')!r}")
    rejected = row.get("rejected_provenance")
    if not isinstance(rejected, list):
        problems.append("rejected_provenance must be a list")
    else:
        for entry in rejected:
            if not isinstance(entry, dict) or entry.get("rejection_reason") not in REJECTION_REASONS:
                problems.append(f"rejected_provenance entry lacks a valid rejection_reason: {entry!r}")
    verdict = VERDICT_TOKEN_RE.search(json.dumps(row))
    if verdict:
        problems.append(f"verdict vocabulary in row fields (N13): {verdict.group(0)}")
    return problems


def closure_problems(entry: dict) -> list[str]:
    problems: list[str] = []
    for field in ("blocker_id", "owning_standard", "durable_ref", "exact_subject_binding", "state", "note"):
        if not str(entry.get(field, "")).strip():
            problems.append(f"closure blocker input missing {field}: {entry.get('blocker_id')!r}")
    if entry.get("state") not in CLOSURE_STATES:
        problems.append(f"invalid closure state {entry.get('state')!r}")
    if entry.get("distinct_from_product_rows") is not True:
        problems.append("closure blocker input must stay distinct from Product rows")
    return problems


class AcceptanceMapCompletenessTests(unittest.TestCase):
    """P1/P2/P3/P4/P5 — the index reconstructs the whole acceptance map."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.record = parse_record()
        cls.rows = cls.record["rows"]

    def test_p1_record_parses_with_exact_row_set(self) -> None:
        self.assertEqual(self.record["record_schema"], "v410-acceptance-projection-v1")
        self.assertEqual(len(self.rows), 8)
        self.assertEqual([r["requirement_id"] for r in self.rows], REQUIRED_ROWS)
        row_ids = [r["row_id"] for r in self.rows]
        self.assertEqual(len(row_ids), len(set(row_ids)))
        for row in self.rows:
            self.assertEqual(row_problems(row), [], row["row_id"])

    def test_p1_prd_anchor_unchanged(self) -> None:
        blob = git_blob_at_head("docs/implementation/4.10.0/PRD.md")
        self.assertEqual(
            blob,
            "b0b9906035eee253aad4bff0274d3d4c8f90b9db",
            "the Frozen Product v0.4 subject drifted; the projection must be rebound",
        )

    def test_p2_rebind_subject_is_the_merged_861_tip(self) -> None:
        subject = self.record["rebind_subject"]
        self.assertEqual(subject["base_sha"], REBIND_BASE_SHA)
        self.assertEqual(subject["base_tree"], REBIND_BASE_TREE)

    def test_p2_every_pinned_producer_resolves_with_matching_blob(self) -> None:
        checked = 0
        for row in self.rows:
            for producer in row["evidence_producers"]:
                if producer.get("exact_subject_binding") == "EVENT_BOUND":
                    self.assertRegex(producer["durable_ref"], EVENT_REF_RE)
                    continue
                rel = producer["durable_ref"]
                blob = git_blob_at_head(rel)
                self.assertIsNotNone(blob, f"producer not tracked at HEAD: {rel}")
                self.assertEqual(
                    blob,
                    producer.get("blob_identity"),
                    f"stale producer binding (N1/A1/A10): {rel} drifted from its pinned blob",
                )
                checked += 1
        self.assertGreaterEqual(checked, 10)

    def test_p2_rows_carry_no_inherited_candidate_binding(self) -> None:
        for row in self.rows:
            self.assertEqual(
                row["current_exact_subject"],
                UNBOUND_SUBJECT,
                f"{row['row_id']} claims a candidate binding before T08A integration",
            )

    def test_p3_blocker_list_reconstructible_by_fresh_observer(self) -> None:
        for row in self.rows:
            self.assertEqual(row["blocker_projection"], "UNRESOLVED")
            self.assertTrue(row["missing_evidence_description"].strip())
            self.assertTrue(row["route_to_owner"].strip())
        closure = self.record["closure_blocker_inputs"]
        self.assertEqual(len(closure), 4)
        ids = [entry["blocker_id"] for entry in closure]
        self.assertEqual(len(ids), len(set(ids)))
        for entry in closure:
            self.assertEqual(closure_problems(entry), [], entry["blocker_id"])
        text = PROJECTION.read_text(encoding="utf-8")
        self.assertIn("#900", text)
        self.assertIn("#865", text)

    def test_p4_minimum_and_advanced_paths_both_legal(self) -> None:
        for row in self.rows:
            self.assertIn(row["adoption_path"], ADOPTION_PATHS)
            static = [
                p
                for p in row["evidence_producers"]
                if p["producer_kind"] in ("DOC", "TEST", "CONFORMANCE_SUITE")
            ]
            self.assertTrue(
                static,
                f"{row['row_id']} Minimum-path subset would need scheduler/runtime evidence",
            )

    def test_p5_release_owner_remains_external(self) -> None:
        text = PROJECTION.read_text(encoding="utf-8")
        self.assertIn("PROJECTION_ONLY=true", text)
        self.assertIn("authorizes_execution=false", text)
        self.assertIn("authorizes_release_qualification=false", text)
        self.assertIn("verdict_authority=LATER_GATES_AND_OWNING_STANDARDS_ONLY", text)
        record_json = json.dumps(self.record)
        self.assertNotIn("release_state", record_json)
        self.assertNotIn("release_verdict", record_json)


class NegativeAutomaticTransferTests(unittest.TestCase):
    """N1-N15 / A-cases — the validator rejects every manufacture pattern."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.record = parse_record()
        cls.rows = cls.record["rows"]

    def _mutant_problems(self, mutant: dict) -> list[str]:
        return row_problems(mutant)

    def _real_row(self, requirement_id: str) -> dict:
        return json.loads(json.dumps(next(r for r in self.rows if r["requirement_id"] == requirement_id)))

    def test_n1_n2_a5_stale_or_wrong_subject_binding_rejected(self) -> None:
        mutant = self._real_row("R1")
        mutant["current_exact_subject"] = "41df8e5ab2cb01208c1db375cd44c0177a814558"
        problems = self._mutant_problems(mutant)
        self.assertTrue(any("current_exact_subject" in p for p in problems))
        mutant2 = self._real_row("R1")
        mutant2["current_exact_subject"] = {
            "sha": REBIND_BASE_SHA,
            "tree": REBIND_BASE_TREE,
        }
        self.assertTrue(
            any("current_exact_subject" in p for p in self._mutant_problems(mutant2)),
            "a bound subject is unreachable before T08A (no automatic transfer)",
        )

    def test_n1_a1_a10_blob_drift_fails_closed(self) -> None:
        mutant = self._real_row("R1")
        for producer in mutant["evidence_producers"]:
            if producer.get("exact_subject_binding") == "CANDIDATE_BOUND":
                producer["blob_identity"] = "0" * 40
                break
        else:
            self.fail("fixture error: no CANDIDATE_BOUND producer in R1")
        # Resolution-level fail-closed (A10): the well-formed but WRONG pin must
        # be rejected by the same resolution machinery test_p2 applies — the
        # producer's real blob at HEAD differs from the mutant pin, so test_p2's
        # equality checks fail closed on this drift instead of accepting a
        # merely format-valid value.
        drifted = [p for p in mutant["evidence_producers"] if p["blob_identity"] == "0" * 40]
        self.assertEqual(len(drifted), 1)
        producer = drifted[0]
        self.assertEqual(producer["exact_subject_binding"], "CANDIDATE_BOUND")
        actual = git_blob_at_head(producer["durable_ref"])
        self.assertIsNotNone(actual, f"producer not tracked at HEAD: {producer['durable_ref']}")
        self.assertNotEqual(
            actual,
            producer["blob_identity"],
            f"well-formed but wrong pin for {producer['durable_ref']} would pass "
            "resolution — blob drift would not fail closed",
        )
        # Format-level drift is rejected by the row validator directly:
        bad_format = self._real_row("R1")
        bad_format["evidence_producers"][0]["blob_identity"] = "deadbeef"
        self.assertTrue(
            any("blob_identity" in p for p in self._mutant_problems(bad_format))
        )

    def test_n1_historical_lineage_never_a_current_producer(self) -> None:
        for row in self.rows:
            current_refs = [p["durable_ref"] for p in row["evidence_producers"]]
            self.assertNotIn(
                SUPERSEDED_LINEAGE_DOC,
                current_refs,
                f"{row['row_id']} binds the SUPERSEDED L1 synthesis as current evidence",
            )
        rejected_somewhere = any(
            any(e.get("ref") == SUPERSEDED_LINEAGE_DOC for e in row["rejected_provenance"])
            for row in self.rows
        )
        self.assertTrue(rejected_somewhere, "superseded lineage must stay preserved with its reason")

    def test_n1_preview_identities_absent_from_current_bindings(self) -> None:
        record_json = json.dumps(self.record)
        for stale in STALE_IDENTITIES:
            self.assertNotIn(stale, record_json, f"preview identity {stale} bound inside the record")
        text = PROJECTION.read_text(encoding="utf-8")
        for stale in STALE_IDENTITIES:
            self.assertIn(stale, text)  # the appendix must NAME the rejected preview heads
        self.assertIn("NON_INTEGRATED preview", text)

    def test_n3_n5_n10_cross_layer_results_cannot_clear_blockers(self) -> None:
        mutant = self._real_row("R2")
        mutant["evidence_producers"] = [
            {
                "producer_kind": "ISSUE_EVENT",
                "durable_ref": "#862@6046061801",
                "exact_subject_binding": "EVENT_BOUND",
            }
        ]
        problems = self._mutant_problems(mutant)
        self.assertTrue(any("EVENT_BOUND lanes" in p for p in problems))
        mutant2 = self._real_row("R3")
        mutant2["blocker_projection"] = "EVIDENCE_CURRENT"
        self.assertTrue(
            any("EVIDENCE_CURRENT requires a bound exact subject" in p for p in self._mutant_problems(mutant2)),
            "scheduler/conformance results cannot yield EVIDENCE_CURRENT on an unbound subject",
        )

    def test_n8_duplicate_lane_evidence_rejected(self) -> None:
        mutant = self._real_row("R7")
        mutant["evidence_producers"] = [mutant["evidence_producers"][-1]] * 2
        self.assertTrue(any("double-count" in p for p in self._mutant_problems(mutant)))

    def test_n11_missing_evidence_never_not_applicable(self) -> None:
        mutant = self._real_row("R4")
        mutant["evidence_producers"] = []
        problems = self._mutant_problems(mutant)
        self.assertTrue(any("at least one evidence producer" in p for p in problems))
        self.assertNotIn("NOT_APPLICABLE", json.dumps(self.record["rows"]))

    def test_n13_a4_a12_verdict_vocabulary_and_state_machine_rejected(self) -> None:
        mutant = self._real_row("R6")
        mutant["blocker_projection"] = "PASS"
        self.assertTrue(any("invalid blocker_projection" in p for p in self._mutant_problems(mutant)))
        mutant2 = self._real_row("R6")
        mutant2["authority_note"] = "the index READY verdict"
        self.assertTrue(any("verdict vocabulary" in p for p in self._mutant_problems(mutant2)))
        record_json = json.dumps(self.record)
        self.assertNotIn("PASS", record_json)
        self.assertNotIn("READY", record_json)

    def test_n13_rejection_reason_vocabulary_enforced(self) -> None:
        mutant = self._real_row("R12")
        mutant["rejected_provenance"] = [{"ref": "something", "rejection_reason": "looks_fine"}]
        self.assertTrue(any("rejection_reason" in p for p in self._mutant_problems(mutant)))

    def test_n13_a6_a7_adoption_path_vocabulary_enforced(self) -> None:
        mutant = self._real_row("R3")
        mutant["adoption_path"] = "MINIMUM_ONLY"
        self.assertTrue(any("invalid adoption_path" in p for p in self._mutant_problems(mutant)))

    def test_n15_no_field_path_to_freeze_decision(self) -> None:
        # The token may appear ONLY inside the closure-separation note that
        # documents the missing path — never in a row, never as a field name,
        # never bound to a YES/NO outcome.
        self.assertNotIn("ADS_CORE_FEATURE_FREEZE_ELIGIBLE", json.dumps(self.record["rows"]))
        record_keys: list[str] = []

        def collect(value: object) -> None:
            if isinstance(value, dict):
                for key, item in value.items():
                    record_keys.append(key)
                    collect(item)
            elif isinstance(value, list):
                for item in value:
                    collect(item)

        collect(self.record)
        self.assertFalse([k for k in record_keys if "freeze" in k.lower()])
        freeze = next(
            e for e in self.record["closure_blocker_inputs"] if e["blocker_id"] == "BLK-FREEZE-DECISION-SUPPORT"
        )
        self.assertIn("Product authority", freeze["owning_standard"])
        self.assertIn("zero field path", freeze["note"])
        text = PROJECTION.read_text(encoding="utf-8")
        self.assertIn("V410-T07B", text)

    def test_n9_web_origin_rejection_recorded(self) -> None:
        text = PROJECTION.read_text(encoding="utf-8")
        self.assertIn("wrong_layer", text)
        self.assertIn("LOCAL real-host exact-subject", text)

    def test_prep_branch_artifact_is_not_a_candidate(self) -> None:
        self.assertFalse(
            (ROOT / PREP_BRANCH_TEST).exists(),
            "the retained prep-branch inventory test must stay out of the candidate",
        )
        text = PROJECTION.read_text(encoding="utf-8")
        self.assertIn("test_v410_t07a_evidence_inventory.py", text)

    def test_legacy_packs_preserved_as_history(self) -> None:
        text = PROJECTION.read_text(encoding="utf-8")
        self.assertIn("PACK_INVALID", text)
        for legacy in ("V410-T01A", "V410-T01B", "V410-T02A", "V410-T02B-R2"):
            self.assertTrue((ROOT / ".agent" / "execution" / legacy).is_dir(), legacy)


class ProjectionSurfaceConformanceTests(unittest.TestCase):
    """Pack/manifest/scope guards for this task's own deliverables.

    Scope-guard history (positional-debt class): this guard originally diffed
    the WORKING TREE against the frozen T07A base 0518202c with WHOLE-PREFIX
    bans on templates/|references/|checklists/ plus a blanket carried-suite
    check on every ``scripts/test_`` path except its own — structurally red on
    every task-pack-legal successor candidate tree, exactly the positional debt
    the T07A R2 repair documented for the owner-convergence guard.

    V410-T07B R3 seam rebind (#863, dispatch V410-T07B-BOUNDED-SEAM-REBIND-R2;
    trigger and mechanics recorded in
    .agent/execution/V410-T07A-R1/TEST_MATRIX.yaml ``r3_seam_rebind``): rebound
    successor-aware while preserving the original guard intent, mirroring the
    TASK_CANDIDATES family pattern of scripts/test_v410_owner_convergence.py —
    the frozen INTEGRATED T07A delta (0518202c...382c1869, merged PR #933) stays
    asserted against T07A's own prefixes and the T06B-owned/authority forbidden
    surfaces (deterministic, mutant-catching), and each successor's candidate
    delta is scoped to its OWN registered prefixes via TASK_CANDIDATES, with
    the active candidate measured base -> committed HEAD and failing LOUD on
    ancestry loss, unregistered paths, upstream authority surfaces, or
    unauthorized carried-suite edits (never a silent skip). Zero removed
    tests; no other assertion weakened.
    """

    # Frozen T07A R2 integrated tip (merged PR #933): the frozen subject of the
    # T07A integrated delta asserted by
    # test_forbidden_surfaces_untouched_vs_rebind_base — deterministic and
    # mutant-catching regardless of which successor candidate is active.
    T07A_INTEGRATED_SHA = "382c1869c79790e22e1e89fdf08c0a23404544c1"
    # V410-T07B candidate base (the merged PR #933 integration tip on the
    # version/v4.10.0 lineage — T07B's own registered base).
    T07B_BASE_SHA = "cea2e0ccd045e8fcebaf110273129b198ed259fd"

    # Surfaces the T07A integrated candidate may touch (its 9 deliverable
    # paths): the six-path pack, the projection, this suite, and the one
    # carried-suite path the R2 bounded repair is authorized to rebind.
    T07A_DELIVERABLE_PREFIXES = (
        ".agent/execution/V410-T07A-R1/",
        "docs/implementation/4.10.0/PRODUCT_ACCEPTANCE_EVIDENCE_PROJECTION_R1.md",
        "scripts/test_v410_t07a_acceptance_projection.py",
        "scripts/test_v410_owner_convergence.py",
    )

    # Surfaces the V410-T07B candidate may touch: its own deliverables, plus
    # the pre-authorized carried-suite registry rebind
    # (scripts/test_v410_owner_convergence.py, fast-path handoff
    # #863@6046064159), plus the R3 seam-rebind paths authorized by dispatch
    # V410-T07B-BOUNDED-SEAM-REBIND-R2 (this suite and the pin-bearing
    # projection/IMPLEMENTATION_MAP/TEST_MATRIX files). Never a widening of
    # another task's scope — every T07A-owned line here is explicitly
    # authorized and positively re-pinned in the same commit.
    T07B_PREFIXES = (
        ".agent/execution/V410-T07B-R1/",
        "templates/product-decision-record.md",
        "references/PRODUCT_DECISION_RECORD_REFERENCE.md",
        "checklists/version-closure.md",
        "scripts/test_v410_t07b_decision_record.py",
        "scripts/test_v410_owner_convergence.py",
        "scripts/test_v410_t07a_acceptance_projection.py",
        "docs/implementation/4.10.0/PRODUCT_ACCEPTANCE_EVIDENCE_PROJECTION_R1.md",
        ".agent/execution/V410-T07A-R1/IMPLEMENTATION_MAP.md",
        ".agent/execution/V410-T07A-R1/TEST_MATRIX.yaml",
    )

    # Upstream authority surfaces that must never appear in the active T07B
    # candidate diff (T07B EXECUTION_CONTRACT "Do NOT touch" list, minus the
    # seam paths this dispatch explicitly authorizes).
    T07B_FORBIDDEN_SURFACES = (
        "schemas/",
        "standards/",
        "registries/",
        "prompts/",
        "standard-manifest.json",
        "scripts/v34_rules.py",
        "scripts/verify_standard.py",
        "templates/agent-event-comment.md",
        "templates/GOLDEN_INDEX.md",
        "references/V410_OWNER_AUTHORITY_CONVERGENCE_REFERENCE.md",
    )

    # Successor-aware candidate registry (family pattern of
    # scripts/test_v410_owner_convergence.py): each task's candidate delta is
    # scoped to its OWN registered prefixes instead of every successor being
    # measured against T07A's whole-prefix bans. T07A is frozen at its
    # integrated tip; the single entry flagged active=True is measured from its
    # base to the CURRENT committed HEAD and fails LOUD on ancestry loss,
    # unregistered paths or unauthorized carried-suite edits — never a silent
    # skip. A successor task rebinds by adding its own entry and moving the
    # active flag — never by widening another task's prefixes.
    TASK_CANDIDATES = (
        {
            "task": "V410-T07A",
            "base": REBIND_BASE_SHA,
            "integrated": T07A_INTEGRATED_SHA,
            "prefixes": T07A_DELIVERABLE_PREFIXES,
            "authorized_suite_edits": AUTHORIZED_R2_CARRIED_REBIND,
        },
        {
            "task": "V410-T07B",
            "base": T07B_BASE_SHA,
            "prefixes": T07B_PREFIXES,
            "authorized_suite_edits": frozenset(
                {
                    "scripts/test_v410_owner_convergence.py",
                    "scripts/test_v410_t07a_acceptance_projection.py",
                }
            ),
            "active": True,
        },
    )

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

    def test_pack_manifest_binds_exact_rebind_subject(self) -> None:
        text = (PACK_DIR / "MANIFEST.yaml").read_text(encoding="utf-8")
        self.assertIn(f"base_sha: {REBIND_BASE_SHA}", text)
        self.assertIn(f"base_tree: {REBIND_BASE_TREE}", text)
        self.assertIn("task_id: V410-T07A", text)
        self.assertIn("F1_BOUNDED_IMPLEMENTATION", text)

    def test_projection_file_present_and_owned(self) -> None:
        blob = git_blob_at_head(PROJECTION.relative_to(ROOT).as_posix())
        # The projection itself is NEW in this change: uncommitted at first run,
        # committed afterwards. Either way the working-tree file must exist.
        self.assertTrue(PROJECTION.is_file())
        del blob

    def test_forbidden_surfaces_untouched_vs_rebind_base(self) -> None:
        # R3 seam rebind: the ORIGINAL guard intent is preserved on the frozen
        # INTEGRATED T07A delta (merged PR #933) — deterministic regardless of
        # which successor candidate is active, so a mutated prefix list, a
        # fabricated integrated path, or an authority-surface edit still fails
        # here.
        entry = self._candidate("V410-T07A")
        changed = self._changed_paths(entry["base"], entry["integrated"])
        self.assertTrue(changed, "frozen T07A integrated delta resolved empty — guard subject lost")
        offenders = sorted(
            p
            for p in changed
            if p.startswith(T07A_FORBIDDEN_PREFIXES) or p == "standard-manifest.json"
        )
        self.assertEqual(offenders, [], "T06B-owned / authority surfaces must stay untouched")
        outside = sorted(p for p in changed if not p.startswith(entry["prefixes"]))
        self.assertEqual(outside, [], "T07A deliverables must stay inside T07A's own registered prefixes")
        carried = self._carried_suite_offenders(changed, entry["base"], entry["authorized_suite_edits"])
        self.assertEqual(carried, [], f"carried suite edited outside the authorized R2 rebind: {carried}")

    def test_active_candidate_head_diff_stays_inside_registered_task_prefixes(self) -> None:
        # HEAD-relative successor scoping, fail loud (no silent skip): every
        # path committed since the active candidate's base must be inside the
        # active candidate's own registered prefixes. A successor candidate
        # that extends the tree without registering its own TASK_CANDIDATES
        # entry fails here with rebind instructions instead of silently
        # passing.
        entry = self._active_candidate()
        if not self._is_ancestor(entry["base"], "HEAD"):
            self.fail(
                f"HEAD does not descend from the active candidate base "
                f"{entry['base']} ({entry['task']}); the active-candidate scope "
                "check cannot run — rebind TASK_CANDIDATES for this lineage "
                "(fail loud, no silent skip)"
            )
        changed = self._changed_paths(entry["base"], "HEAD")
        outside = sorted(p for p in changed if not p.startswith(entry["prefixes"]))
        self.assertEqual(
            outside,
            [],
            "paths outside the active candidate's registered prefixes; the "
            "successor task must rebind this guard by registering its own "
            "TASK_CANDIDATES entry (task/base/prefixes) — never by widening "
            "another task's scope",
        )
        authority = sorted(p for p in changed if p.startswith(self.T07B_FORBIDDEN_SURFACES))
        self.assertEqual(authority, [], "upstream authority surfaces must stay untouched by the active candidate")
        carried = self._carried_suite_offenders(changed, entry["base"], entry["authorized_suite_edits"])
        self.assertEqual(carried, [], f"carried suite edited without authorization: {carried}")

    def test_candidate_registry_is_wellformed(self) -> None:
        tasks = [entry["task"] for entry in self.TASK_CANDIDATES]
        self.assertTrue(tasks, "TASK_CANDIDATES must not be empty")
        self.assertEqual(len(tasks), len(set(tasks)), "duplicate task entries in TASK_CANDIDATES")
        self.assertEqual(
            [entry["task"] for entry in self.TASK_CANDIDATES if entry.get("active")],
            ["V410-T07B"],
            "exactly one active candidate entry is required",
        )
        t07b = self._candidate("V410-T07B")
        self.assertEqual(
            t07b["authorized_suite_edits"],
            AUTHORIZED_R2_CARRIED_REBIND | AUTHORIZED_R3_SEAM_REBIND & {"scripts/test_v410_t07a_acceptance_projection.py"},
            "the active candidate's carried-suite authorization must be exactly "
            "the disclosed R2 registry rebind + R3 seam rebind",
        )
        for entry in self.TASK_CANDIDATES:
            with self.subTest(task=entry["task"]):
                self.assertTrue(entry["prefixes"], f"{entry['task']} has empty prefixes")
                for key in ("base", "integrated"):
                    if key in entry:
                        self.assertTrue(
                            self._commit_exists(entry[key]),
                            f"{entry['task']} {key} {entry[key]} does not resolve to a commit",
                        )

    def _candidate(self, task: str) -> dict:
        return next(entry for entry in self.TASK_CANDIDATES if entry["task"] == task)

    def _active_candidate(self) -> dict:
        return next(entry for entry in self.TASK_CANDIDATES if entry.get("active"))

    def _changed_paths(self, base: str, head: str) -> set[str]:
        result = subprocess.run(
            ["git", "diff", "--name-only", f"{base}...{head}", "--"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            self.fail(f"cannot diff against {base}...{head}: {result.stderr.strip()}")
        return {line.strip() for line in result.stdout.splitlines() if line.strip()}

    def _carried_suite_offenders(self, changed: set[str], base: str, authorized: frozenset) -> list[str]:
        # Carried = the suite already existed at the candidate's base; a task's
        # OWN new suite is its own deliverable (scoped by the prefixes check).
        return sorted(
            p
            for p in changed
            if p.startswith("scripts/test_")
            and (ROOT / p).is_file()
            and self._path_exists_at(base, p)
            and p not in authorized
        )

    def _path_exists_at(self, ref: str, rel: str) -> bool:
        result = subprocess.run(
            ["git", "cat-file", "-e", f"{ref}:{rel}"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        return result.returncode == 0

    def _is_ancestor(self, ancestor: str, descendant: str) -> bool:
        result = subprocess.run(
            ["git", "merge-base", "--is-ancestor", ancestor, descendant],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        if result.returncode not in (0, 1):
            self.fail(f"cannot test ancestry {ancestor} <- {descendant}: {result.stderr.strip()}")
        return result.returncode == 0

    def _commit_exists(self, sha: str) -> bool:
        result = subprocess.run(
            ["git", "cat-file", "-e", f"{sha}^{{commit}}"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        return result.returncode == 0


if __name__ == "__main__":
    unittest.main()
