from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import unittest

from test_protocol_schemas import load_schema, validate_subset
from test_v49_task_learning_v2 import minimal_v2_record


ROOT = Path(__file__).resolve().parents[1]
BASE_SHA = "7844041c1fd9a69d923cb4da67a86745401c3988"

LANDED_OWNERS = {
    "V411-T01", "V411-T02", "V411-T03", "V411-T04", "V411-T05", "V411-T06",
    "V411-T07", "V411-T08", "V411-T09", "V411-T10", "V411-T13", "V411-T14",
}

# T11 disposition is explicit for every landed predecessor. "BLOCKED_NAMED"
# means there was no admissible five-element central proposal and T11 refuses
# to manufacture one. This is a truthful P05 outcome, not a silent promotion.
OWNER_DISPOSITIONS = {
    "V411-T01": ("BLOCKED_NAMED", "no complete central proposal contract landed"),
    "V411-T02": ("BLOCKED_NAMED", "no complete central proposal contract landed"),
    "V411-T03": ("BLOCKED_NAMED", "consumer/currentness dimensions remain proposal-scoped"),
    "V411-T04": ("NO_SHARED_DELTA", "P2 mode-binding hardening did not require a shared contract"),
    "V411-T05": ("BLOCKED_NAMED", "event/shared projection proposal is incomplete"),
    "V411-T06": ("NO_SHARED_DELTA", "owner landed without a shared schema request"),
    "V411-T07": ("WIRED_SHARED_TEST", "LAST_ADMISSION_SWEEP reusable semantics wired centrally"),
    "V411-T08": ("NO_SHARED_DELTA", "owner explicitly creates no shared schema"),
    "V411-T09": ("NO_SHARED_DELTA", "effect facts remain owner-local; shared projection not required"),
    "V411-T10": ("BLOCKED_NAMED", "principal/tenant P2 remains consumer-boundary evidence"),
    "V411-T13": ("BLOCKED_NAMED", "role-conduct projection lacks a complete additive-schema proposal"),
    "V411-T14": ("REUSE_EXISTING_V1_V2", "task-learning v1/v2 family remains authoritative"),
}

T07_SOURCE_BLOB = "f5552653f9fd69697b21d87d9890426943fd7f41"
T07_CURRENT_SUCCESSOR_BLOB = "846158b95e4173182a258f49847e1fde6600baec"
T08_CURRENT_WORKFLOW_BLOB = "28c537e12c03f3f0cef501b8b5505e8ee28ca532"
T09_EXTERNAL_BLOB = "3f7189301f7292200a98ebd027372513a801bc03"
T09_MIGRATION_BLOB = "bf15f3f387cb81a78ecb54169b1cfec00dc8340a"

# Accepted source refs are exact owner-review subjects, not merely any Git blob
# that happens to exist. T07 is the only complete central proposal in this T11
# candidate; every other owner remains NO_SHARED_DELTA/BLOCKED_NAMED/reuse-only.
ACCEPTED_OWNER_SOURCE_REFS = {
    "V411-T07": {
        (
            "standards/EXECUTION_ARCHITECTURE_STANDARD.md",
            "14",
            T07_SOURCE_BLOB,
        ),
    },
}


# Exact-value oracle for the one accepted v4.11 non-schema shared-test handoff.
# The provenance is durable and independently reviewed:
#   owner handoff  #1014@6118552578
#   accepted review #1071@6123914750
# This deliberately does NOT generalize from shape-valid proposal fields. T11
# may consume only these exact accepted semantics; any other owner/delta/
# compatibility/provenance tuple remains blocked instead of being invented.
ACCEPTED_OWNER_PROPOSAL_ORACLES = {
    "V411-T07": {
        "owner_task_id": "V411-T07",
        "frozen_source_ref": {
            "path": "standards/EXECUTION_ARCHITECTURE_STANDARD.md",
            "section": "14",
            "blob": T07_SOURCE_BLOB,
        },
        "additive_schema_delta": {
            "target": "NO_SCHEMA_DELTA_SHARED_TEST_ONLY",
            "posture": "NON_SCHEMA_HANDOFF",
        },
        "compatibility_evidence": {
            "contract": "LAST_ADMISSION_SWEEP",
            "version": "v4.11-t07-owner",
            "baseline_blob": T07_SOURCE_BLOB,
            "candidate_blob": T07_CURRENT_SUCCESSOR_BLOB,
            "producer_classes": ["T07 owner-lane sweep producer"],
            "consumer_classes": ["T11 shared execution-suite consumer"],
            "support_window": "v4.11 central convergence",
            "old_producer_to_new_reader": "NOT_APPLICABLE_SHARED_TEST",
            "new_producer_to_old_reader": "NOT_APPLICABLE_SHARED_TEST",
        },
        "failing_verification_note": {
            "status": "DEFERRED_TO_T11",
            "owner_task_id": "V411-T07",
            "gate": "T07_COMMON_SUITE",
            "evidence_ref": "#1014@6118552578",
            "accepted_review_ref": "#1071@6123914750",
        },
    },
}

ALLOWED_COMPAT_OUTCOMES = {
    "PASS",
    "BLOCKED",
    "NOT_RUN",
    "NOT_APPLICABLE_SHARED_TEST",
}

ALLOWED_T11_PATHS = {
    "checklists/version-closure.md",
    "fixtures/dogfood-audit-contract/owner_surfaces.json",
    "scripts/test_execution_architecture.py",
    "scripts/test_v49_dogfood_audit_contract.py",
    "scripts/test_v49_integrated_dogfood.py",
    "scripts/test_v411_central_wiring.py",
    "scripts/test_verify_standard.py",
    "scripts/verify_standard.py",
    "standard-manifest.json",
}


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
        check=check,
    )


def blob_at(rev: str, path: str) -> str:
    return git("rev-parse", f"{rev}:{path}").stdout.strip()


def proposal_problems(proposal: dict) -> list[str]:
    required = {
        "owner_task_id",
        "frozen_source_ref",
        "additive_schema_delta",
        "compatibility_evidence",
        "failing_verification_note",
    }
    problems: list[str] = []
    missing = sorted(required - set(proposal))
    if missing:
        problems.append("MISSING_PROPOSAL_ELEMENTS:" + ",".join(missing))
        return problems

    owner = proposal["owner_task_id"]
    if owner not in LANDED_OWNERS:
        problems.append("REJECTED_UNFROZEN")

    source = proposal["frozen_source_ref"]
    if not isinstance(source, dict) or not {"path", "section", "blob"}.issubset(source):
        problems.append("SOURCE_REF_INCOMPLETE")
    else:
        blob = source["blob"]
        if not isinstance(blob, str) or len(blob) != 40:
            problems.append("SOURCE_BLOB_INVALID")
        elif git("cat-file", "-e", f"{blob}^{{blob}}", check=False).returncode != 0:
            problems.append("SOURCE_BLOB_UNRESOLVABLE")
        exact_ref = (source.get("path"), str(source.get("section")), blob)
        if exact_ref not in ACCEPTED_OWNER_SOURCE_REFS.get(owner, set()):
            problems.append("SOURCE_REF_MISMATCH")

    delta = proposal["additive_schema_delta"]
    if not isinstance(delta, dict) or not {"target", "posture"}.issubset(delta):
        problems.append("ADDITIVE_SCHEMA_DELTA_INCOMPLETE")
    elif delta["posture"] == "NON_SCHEMA_HANDOFF":
        if delta["target"] != "NO_SCHEMA_DELTA_SHARED_TEST_ONLY":
            problems.append("NON_SCHEMA_HANDOFF_TARGET_INVALID")
    elif delta["posture"] == "ADDITIVE_SCHEMA":
        required_delta = {"target", "posture", "json_schema_draft", "compatibility_mode"}
        if not required_delta.issubset(delta):
            problems.append("ADDITIVE_SCHEMA_DELTA_INCOMPLETE")
        else:
            if not isinstance(delta["target"], str) or not delta["target"].startswith("schemas/"):
                problems.append("SCHEMA_TARGET_INVALID")
            if delta["json_schema_draft"] != "2020-12":
                problems.append("SCHEMA_DRAFT_INVALID")
            if delta["compatibility_mode"] != "NO_IN_PLACE_BREAKING_CHANGE":
                problems.append("SCHEMA_COMPATIBILITY_POSTURE_INVALID")
    else:
        problems.append("ADDITIVE_SCHEMA_POSTURE_UNKNOWN")

    compat = proposal["compatibility_evidence"]
    required_compat = {
        "contract",
        "version",
        "baseline_blob",
        "candidate_blob",
        "producer_classes",
        "consumer_classes",
        "support_window",
        "old_producer_to_new_reader",
        "new_producer_to_old_reader",
    }
    if not isinstance(compat, dict) or not required_compat.issubset(compat):
        problems.append("COMPATIBILITY_EVIDENCE_INCOMPLETE")
    else:
        for field in ("contract", "version", "support_window"):
            if not isinstance(compat[field], str) or not compat[field].strip():
                problems.append(f"COMPATIBILITY_{field.upper()}_INVALID")
        for field in ("producer_classes", "consumer_classes"):
            value = compat[field]
            if not isinstance(value, list) or not value or not all(
                isinstance(item, str) and item.strip() for item in value
            ):
                problems.append(f"COMPATIBILITY_{field.upper()}_INVALID")
        for field in ("baseline_blob", "candidate_blob"):
            blob = compat[field]
            if (
                not isinstance(blob, str)
                or len(blob) != 40
                or git("cat-file", "-e", f"{blob}^{{blob}}", check=False).returncode != 0
            ):
                problems.append(f"COMPATIBILITY_{field.upper()}_INVALID")
        for field in ("old_producer_to_new_reader", "new_producer_to_old_reader"):
            if compat[field] not in ALLOWED_COMPAT_OUTCOMES:
                problems.append(f"COMPATIBILITY_{field.upper()}_INVALID")

    note = proposal["failing_verification_note"]
    required_note = {"status", "owner_task_id", "gate", "evidence_ref", "accepted_review_ref"}
    if not isinstance(note, dict) or not required_note.issubset(note):
        problems.append("FAILING_VERIFICATION_NOTE_INCOMPLETE")
    else:
        if note["status"] != "DEFERRED_TO_T11" or note["owner_task_id"] != owner:
            problems.append("FAILING_VERIFICATION_NOTE_MISMATCH")
        if not isinstance(note["gate"], str) or not note["gate"].strip():
            problems.append("FAILING_VERIFICATION_GATE_INVALID")
        for field in ("evidence_ref", "accepted_review_ref"):
            evidence_ref = note[field]
            if (
                not isinstance(evidence_ref, str)
                or not evidence_ref.startswith("#")
                or "@" not in evidence_ref
                or not all(part.isdigit() for part in evidence_ref[1:].split("@", 1))
            ):
                problems.append(f"FAILING_VERIFICATION_{field.upper()}_INVALID")

    # R2 repair: shape-valid data is never sufficient. Bind every semantic
    # component to the exact accepted handoff oracle. This also makes a fully
    # well-formed but unauthorized ADDITIVE_SCHEMA proposal fail closed.
    expected = ACCEPTED_OWNER_PROPOSAL_ORACLES.get(owner)
    if expected is None:
        problems.append("NO_ACCEPTED_PROPOSAL_ORACLE")
    else:
        for field, code in (
            ("frozen_source_ref", "SOURCE_REF_EXACT_MISMATCH"),
            ("additive_schema_delta", "ADDITIVE_SCHEMA_DELTA_EXACT_MISMATCH"),
            ("compatibility_evidence", "COMPATIBILITY_EVIDENCE_EXACT_MISMATCH"),
            ("failing_verification_note", "FAILING_VERIFICATION_NOTE_EXACT_MISMATCH"),
        ):
            if proposal.get(field) != expected[field]:
                problems.append(code)
    return problems


def proposal_key(proposal: dict) -> tuple[str, str, str, str]:
    source = proposal["frozen_source_ref"]
    delta = proposal["additive_schema_delta"]
    return (
        proposal["owner_task_id"],
        source["path"],
        str(source["section"]),
        delta["target"],
    )


def reconcile_proposals(proposals: list[dict]) -> dict:
    seen: set[tuple[str, str, str, str]] = set()
    deltas: list[tuple[str, str, str, str]] = []
    problems: list[str] = []
    for proposal in proposals:
        current = proposal_problems(proposal)
        if current:
            problems.extend(current)
            continue
        key = proposal_key(proposal)
        if key in seen:
            problems.append("DUPLICATE_PROPOSAL:" + "|".join(key))
            continue
        seen.add(key)
        deltas.append(key)
    return {
        "verdict": "PASS" if not problems else "BLOCKED",
        "problems": problems,
        "deltas": deltas,
    }

def manifest_problems(manifest: dict) -> list[str]:
    problems: list[str] = []
    seen: set[str] = set()
    for section, entries in manifest.get("sections", {}).items():
        if not isinstance(entries, list):
            problems.append(f"SECTION_NOT_LIST:{section}")
            continue
        for rel in entries:
            if rel in seen:
                problems.append(f"DUPLICATE:{rel}")
            seen.add(rel)
            if not (ROOT / rel).is_file():
                problems.append(f"ABSENT:{rel}")
    return problems


def mandatory_fact_gate(record: dict) -> str:
    required = ("owner_task_id", "source_ref", "subject", "currentness")
    if any(record.get(field) in (None, "", "UNKNOWN") for field in required):
        return "BLOCKED"
    if record["owner_task_id"] not in LANDED_OWNERS:
        return "BLOCKED"
    if record["currentness"] != "CURRENT":
        return "BLOCKED"
    return "PASS"


class CentralWiringOwnerLedgerTests(unittest.TestCase):
    def test_p01_all_twelve_landed_owners_have_one_explicit_disposition(self) -> None:
        self.assertEqual(set(OWNER_DISPOSITIONS), LANDED_OWNERS)
        self.assertEqual(len(OWNER_DISPOSITIONS), 12)
        self.assertEqual(
            [task for task, (state, _) in OWNER_DISPOSITIONS.items() if state == "WIRED_SHARED_TEST"],
            ["V411-T07"],
        )

    def test_p05_no_deferred_item_is_silently_promoted(self) -> None:
        allowed = {"BLOCKED_NAMED", "NO_SHARED_DELTA", "WIRED_SHARED_TEST", "REUSE_EXISTING_V1_V2"}
        for task, (state, reason) in OWNER_DISPOSITIONS.items():
            with self.subTest(task=task):
                self.assertIn(state, allowed)
                self.assertTrue(reason.strip())
                self.assertNotEqual(state, "PASS_BY_OMISSION")

    def test_jit_owner_provenance_and_successor_chain_resolve(self) -> None:
        self.assertEqual(
            T07_CURRENT_SUCCESSOR_BLOB,
            blob_at(BASE_SHA, "standards/EXECUTION_ARCHITECTURE_STANDARD.md"),
        )
        self.assertEqual(
            T08_CURRENT_WORKFLOW_BLOB,
            blob_at(BASE_SHA, "standards/DEVELOPMENT_WORKFLOW.md"),
        )
        self.assertEqual(
            T09_EXTERNAL_BLOB,
            blob_at(BASE_SHA, "standards/EXTERNAL_SYSTEM_EXECUTION_STANDARD.md"),
        )
        self.assertEqual(
            T09_MIGRATION_BLOB,
            blob_at(BASE_SHA, "standards/DATA_MIGRATION_GOVERNANCE_STANDARD.md"),
        )
        self.assertEqual(0, git("cat-file", "-e", f"{T07_SOURCE_BLOB}^{{blob}}", check=False).returncode)
        self.assertNotEqual(T07_SOURCE_BLOB, T07_CURRENT_SUCCESSOR_BLOB)

    def test_t11_source_write_set_is_central_only(self) -> None:
        self.assertEqual(0, git("merge-base", "--is-ancestor", BASE_SHA, "HEAD", check=False).returncode)
        changed = set(git("diff", "--name-only", BASE_SHA, "HEAD").stdout.splitlines())
        self.assertTrue(changed)
        self.assertTrue(changed.issubset(ALLOWED_T11_PATHS), sorted(changed - ALLOWED_T11_PATHS))
        self.assertFalse(any(path.startswith("standards/") for path in changed))
        self.assertFalse(any(path.startswith("schemas/") for path in changed))


class ProposalContractTests(unittest.TestCase):
    def valid_shape(self) -> dict:
        return deepcopy(ACCEPTED_OWNER_PROPOSAL_ORACLES["V411-T07"])

    def test_complete_source_bound_proposal_shape_is_resolvable(self) -> None:
        self.assertEqual(proposal_problems(self.valid_shape()), [])

    def test_n01_missing_element_or_unlanded_owner_is_rejected(self) -> None:
        missing = self.valid_shape()
        del missing["compatibility_evidence"]
        self.assertTrue(proposal_problems(missing))
        unfrozen = self.valid_shape()
        unfrozen["owner_task_id"] = "V411-T99"
        self.assertIn("REJECTED_UNFROZEN", proposal_problems(unfrozen))

    def test_n01_existing_but_wrong_source_blob_is_rejected(self) -> None:
        wrong = self.valid_shape()
        wrong["frozen_source_ref"] = dict(wrong["frozen_source_ref"])
        wrong["frozen_source_ref"]["blob"] = T07_CURRENT_SUCCESSOR_BLOB
        self.assertEqual(
            0,
            git("cat-file", "-e", f"{T07_CURRENT_SUCCESSOR_BLOB}^{{blob}}", check=False).returncode,
        )
        self.assertIn("SOURCE_REF_MISMATCH", proposal_problems(wrong))

    def test_n01_wrong_owner_section_is_rejected(self) -> None:
        wrong = self.valid_shape()
        wrong["frozen_source_ref"] = dict(wrong["frozen_source_ref"], section="99")
        self.assertIn("SOURCE_REF_MISMATCH", proposal_problems(wrong))

    def test_proposal_contract_missing_mandatory_subfields_fails_closed(self) -> None:
        cases: list[tuple[str, dict, str]] = []

        bad_delta = self.valid_shape()
        bad_delta["additive_schema_delta"] = {"posture": "NON_SCHEMA_HANDOFF"}
        cases.append(("delta", bad_delta, "ADDITIVE_SCHEMA_DELTA_INCOMPLETE"))

        bad_compat = self.valid_shape()
        bad_compat["compatibility_evidence"] = dict(bad_compat["compatibility_evidence"])
        del bad_compat["compatibility_evidence"]["support_window"]
        cases.append(("compat", bad_compat, "COMPATIBILITY_EVIDENCE_INCOMPLETE"))

        bad_note = self.valid_shape()
        bad_note["failing_verification_note"] = dict(bad_note["failing_verification_note"])
        bad_note["failing_verification_note"]["evidence_ref"] = "chat-only"
        cases.append(("note", bad_note, "FAILING_VERIFICATION_EVIDENCE_REF_INVALID"))

        for label, proposal, expected in cases:
            with self.subTest(label=label):
                self.assertIn(expected, proposal_problems(proposal))


    def test_r2_shape_valid_but_semantically_mismatched_proposals_fail_closed(self) -> None:
        cases: list[tuple[str, dict, str]] = []

        wrong_baseline = self.valid_shape()
        wrong_baseline["compatibility_evidence"]["baseline_blob"] = T07_CURRENT_SUCCESSOR_BLOB
        cases.append(("baseline_blob", wrong_baseline, "COMPATIBILITY_EVIDENCE_EXACT_MISMATCH"))

        wrong_candidate = self.valid_shape()
        wrong_candidate["compatibility_evidence"]["candidate_blob"] = T08_CURRENT_WORKFLOW_BLOB
        cases.append(("candidate_blob", wrong_candidate, "COMPATIBILITY_EVIDENCE_EXACT_MISMATCH"))

        for field, value in (
            ("contract", "LOOKS_VALID_BUT_WRONG"),
            ("version", "v4.11-wrong-owner"),
            ("support_window", "another-current-looking-window"),
            ("producer_classes", ["wrong producer"]),
            ("consumer_classes", ["wrong consumer"]),
        ):
            proposal = self.valid_shape()
            proposal["compatibility_evidence"][field] = value
            cases.append((field, proposal, "COMPATIBILITY_EVIDENCE_EXACT_MISMATCH"))

        fake_provenance = self.valid_shape()
        fake_provenance["failing_verification_note"]["evidence_ref"] = "#1014@9999999999"
        cases.append(("fake_evidence_ref", fake_provenance, "FAILING_VERIFICATION_NOTE_EXACT_MISMATCH"))

        mismatched_review = self.valid_shape()
        mismatched_review["failing_verification_note"]["accepted_review_ref"] = "#1071@9999999999"
        cases.append(("wrong_review_ref", mismatched_review, "FAILING_VERIFICATION_NOTE_EXACT_MISMATCH"))

        wrong_gate = self.valid_shape()
        wrong_gate["failing_verification_note"]["gate"] = "T07_LOOKS_VALID_BUT_WRONG_GATE"
        cases.append(("wrong_gate", wrong_gate, "FAILING_VERIFICATION_NOTE_EXACT_MISMATCH"))

        unauthorized_schema = self.valid_shape()
        unauthorized_schema["additive_schema_delta"] = {
            "target": "schemas/plausible-but-unaccepted-v411.schema.json",
            "posture": "ADDITIVE_SCHEMA",
            "json_schema_draft": "2020-12",
            "compatibility_mode": "NO_IN_PLACE_BREAKING_CHANGE",
        }
        cases.append(("unauthorized_schema", unauthorized_schema, "ADDITIVE_SCHEMA_DELTA_EXACT_MISMATCH"))

        for label, proposal, expected in cases:
            with self.subTest(label=label):
                self.assertIn(expected, proposal_problems(proposal))

    def test_p01_proposal_ledger_is_exactly_once_and_duplicate_fails_closed(self) -> None:
        proposal = self.valid_shape()
        one = reconcile_proposals([proposal])
        self.assertEqual("PASS", one["verdict"])
        self.assertEqual(1, len(one["deltas"]))

        duplicate = reconcile_proposals([proposal, deepcopy(proposal)])
        self.assertEqual("BLOCKED", duplicate["verdict"])
        self.assertEqual(1, len(duplicate["deltas"]))
        self.assertTrue(any(p.startswith("DUPLICATE_PROPOSAL:") for p in duplicate["problems"]))

    def test_n02_conflicting_same_surface_semantics_stay_blocked(self) -> None:
        proposals = [
            ("V411-T05", "agent-event-v2:event", "A"),
            ("V411-T13", "agent-event-v2:event", "B"),
        ]
        by_surface: dict[str, set[str]] = {}
        for _, surface, semantics in proposals:
            by_surface.setdefault(surface, set()).add(semantics)
        self.assertEqual({"agent-event-v2:event"}, {k for k, v in by_surface.items() if len(v) > 1})

class CompatibilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.v1 = load_schema("task-learning-v1.schema.json")
        self.v2 = load_schema("task-learning-v2.schema.json")
        self.event = load_schema("agent-event-v2.schema.json")

    def test_p02_v1_v2_schema_blobs_are_unchanged_from_t11_base(self) -> None:
        for path in ("schemas/task-learning-v1.schema.json", "schemas/task-learning-v2.schema.json"):
            with self.subTest(path=path):
                self.assertEqual(blob_at(BASE_SHA, path), blob_at("HEAD", path))

    def test_n07_same_v2_required_set_increase_rejects_historical_minimal_record(self) -> None:
        historical = minimal_v2_record()
        self.assertEqual(validate_subset(historical, self.v2), [])
        incompatible = deepcopy(self.v2)
        incompatible["required"] = list(incompatible["required"]) + ["new_mandatory_source_ref"]
        errors = validate_subset(historical, incompatible)
        self.assertTrue(any("new_mandatory_source_ref" in error for error in errors), errors)

    def test_n08_closed_old_reader_rejects_new_optional_property(self) -> None:
        historical = minimal_v2_record()
        new_payload = dict(historical, future_optional="new-value")
        self.assertIs(self.v2.get("additionalProperties"), False)
        errors = validate_subset(new_payload, self.v2)
        self.assertTrue(
            any("unexpected property" in error or "additional property" in error for error in errors),
            errors,
        )

    def test_n08_bounded_old_event_enum_rejects_new_member(self) -> None:
        old_event_reader = self.event["properties"]["event"]
        self.assertNotIn("V411_FUTURE_EVENT", old_event_reader["enum"])
        errors = validate_subset("V411_FUTURE_EVENT", old_event_reader)
        self.assertTrue(any("not in enum" in error for error in errors), errors)


class ManifestAndGateTests(unittest.TestCase):
    def test_p03_no_schema_or_template_delta_preserves_manifest_and_golden_index(self) -> None:
        # Pack P03 is conditional: only a NEW schema/template is registered.
        # This T11 candidate intentionally creates neither, so changing the
        # canonical manifest/GOLDEN_INDEX would be an incompatible ceremony-only delta.
        self.assertEqual(
            blob_at(BASE_SHA, "standard-manifest.json"),
            blob_at("HEAD", "standard-manifest.json"),
        )
        self.assertEqual(
            blob_at(BASE_SHA, "templates/GOLDEN_INDEX.md"),
            blob_at("HEAD", "templates/GOLDEN_INDEX.md"),
        )
        manifest = json.loads((ROOT / "standard-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest_problems(manifest), [])

    def test_n04_duplicate_or_absent_manifest_path_fails(self) -> None:
        manifest = json.loads((ROOT / "standard-manifest.json").read_text(encoding="utf-8"))
        dup = deepcopy(manifest)
        dup["sections"]["verification"].append("scripts/test_execution_architecture.py")
        self.assertTrue(any(p.startswith("DUPLICATE:") for p in manifest_problems(dup)))
        absent = deepcopy(manifest)
        absent["sections"]["verification"].append("scripts/does-not-exist-v411.py")
        self.assertTrue(any(p.startswith("ABSENT:") for p in manifest_problems(absent)))

    def test_n05_missing_mandatory_projection_fact_is_blocked(self) -> None:
        good = {
            "owner_task_id": "V411-T07",
            "source_ref": T07_SOURCE_BLOB,
            "subject": "merged-owner",
            "currentness": "CURRENT",
        }
        self.assertEqual(mandatory_fact_gate(good), "PASS")
        for field in tuple(good):
            with self.subTest(field=field):
                bad = dict(good)
                bad[field] = "UNKNOWN" if field == "currentness" else ""
                self.assertEqual(mandatory_fact_gate(bad), "BLOCKED")

    def test_n06_deferred_without_complete_owner_contract_remains_named_blocked(self) -> None:
        for task in ("V411-T01", "V411-T02", "V411-T03", "V411-T05", "V411-T10", "V411-T13"):
            with self.subTest(task=task):
                state, reason = OWNER_DISPOSITIONS[task]
                self.assertEqual(state, "BLOCKED_NAMED")
                self.assertTrue(reason)


class SharedGateExecutionTests(unittest.TestCase):
    def run_script(self, rel: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(ROOT / rel)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
            timeout=180,
        )

    def test_p04_shared_execution_architecture_common_suite_passes(self) -> None:
        source = (ROOT / "scripts/test_execution_architecture.py").read_text(encoding="utf-8")
        self.assertIn("class V411IntegratedLastAdmissionSweepTests", source)
        result = self.run_script("scripts/test_execution_architecture.py")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_dogfood_and_audit_debt_are_executable_not_keyword_only(self) -> None:
        for rel in (
            "scripts/test_v49_dogfood_audit_contract.py",
            "scripts/test_v49_integrated_dogfood.py",
        ):
            with self.subTest(rel=rel):
                result = self.run_script(rel)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
