"""v4.7 T10 cross-standard Closure-input integration tests.

T10 composes already-owned T07/T08/T09 repository checks.  This file is not a
Validation, Review, Version Closure, Hidden Validation, or Release authority.
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]

PRD = "docs/implementation/4.7.0/PRD.md"
TASK_PACK = "docs/implementation/4.7.0/task-packs/T10_cross_standard_closure_inputs.md"
T07_REFERENCE = "references/V47_SEMANTIC_CONFORMANCE_MATRIX.md"
T08_RECONSTRUCTION = "docs/implementation/4.7.0/dogfood/reconstruction.json"
T09_MIGRATION = "docs/implementation/4.7.0/MIGRATION_ADOPTION.md"
CLOSURE_INPUTS = "docs/implementation/4.7.0/CLOSURE_INPUTS.md"
REFERENCE = "references/V47_CLOSURE_CONFORMANCE_REFERENCE.md"

EXPECTED_WRITE_SET = {
    CLOSURE_INPUTS,
    REFERENCE,
    "scripts/test_v47_cross_standard_closure.py",
}

OWNER_SUITES = (
    "scripts/test_v47_semantic_conformance.py",
    "scripts/test_v47_fresh_agent_dogfood.py",
    "scripts/test_v47_adoption_wiring.py",
)

COMPATIBILITY_ALIASES = (
    "standards/GITHUB_WORKFLOW.md",
    "standards/VERSION_INTEGRATION_WORKFLOW.md",
)

FROZEN_NEGATIVES = (
    "Task DONE -> Validation PASS",
    "Review PASS -> Validation PASS",
    "Validation PASS -> Release READY",
    "PR merged -> Release READY",
    "Release READY -> Deployment SUCCESS",
    "Deployment SUCCESS -> Runtime Healthy",
    "Dispatch COMPLETED -> product/release PASS",
    "PACK_CURRENT -> implementation correct",
    "old exact-SHA PASS -> successor exact-SHA PASS",
    "provider/tool/credential AVAILABLE -> mutation authority",
    "waiver/exception -> PASS",
    "fresh DB/install PASS -> upgrade PASS",
    "wire/schema compatible -> behavior/source/consumer compatible",
    "mock/sandbox PASS -> higher-fidelity PASS",
    "artifact alias/tag -> immutable artifact identity",
    "incident RECOVERED -> permanent fix/follow-up closed",
    "branch/package exists -> maintenance-supported",
    "Skill installed/capable -> trusted/authorized",
    "Intent/Assumption record -> Frozen Product authority",
    "historical chat/memory -> current durable authority",
    "technical necessity -> Task Pack write authority",
)

FORBIDDEN_T10_VERDICTS = (
    "VERSION_CLOSURE=PASS",
    "RELEASE_QUALIFICATION=PASS",
    "RELEASE_READY=YES",
    "CONVERGENCE_PASS=PASS",
)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def parse_allowed_write_set(text: str) -> set[str]:
    lines = text.splitlines()
    start = next(i for i, line in enumerate(lines) if line.strip() == "allowed_write_set:")
    paths: list[str] = []
    for raw in lines[start + 1 :]:
        if raw.startswith("  - "):
            paths.append(raw[4:].strip())
            continue
        if raw and not raw.startswith((" ", "\t")):
            break
    if not paths or len(paths) != len(set(paths)):
        raise AssertionError("T10 allowed_write_set is empty or duplicated")
    return set(paths)


def exact_subject_matches(
    *,
    requested_head: str,
    observed_head: str,
    expected_base: str,
    observed_base: str,
    required_fidelity: str,
    observed_fidelity: str,
) -> bool:
    return (
        requested_head == observed_head
        and expected_base == observed_base
        and required_fidelity == observed_fidelity
    )


def fail_closed_input_state(state: str) -> str:
    normalized = state.strip().upper()
    if normalized in {"UNAVAILABLE", "WAIVED", "STALE", "MISMATCHED", "UNKNOWN"}:
        return "BLOCKED"
    if normalized in {"NOT_RUN", "BLOCKED", "NOT_APPLICABLE"}:
        return normalized
    return normalized


class CrossStandardClosureInputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.prd = read(PRD)
        cls.task_pack = read(TASK_PACK)
        cls.t07 = read(T07_REFERENCE)
        cls.t08 = json.loads(read(T08_RECONSTRUCTION))
        cls.t09 = read(T09_MIGRATION)
        cls.closure = read(CLOSURE_INPUTS)
        cls.reference = read(REFERENCE)

    def test_t10_write_authority_is_exact(self) -> None:
        self.assertEqual(parse_allowed_write_set(self.task_pack), EXPECTED_WRITE_SET)
        self.assertNotIn("standard-manifest.json", EXPECTED_WRITE_SET)
        self.assertNotIn("checklists/version-closure.md", EXPECTED_WRITE_SET)
        self.assertNotIn("docs/implementation/4.7.0/dogfood/reconstruction.json", EXPECTED_WRITE_SET)

    def test_v41_v47_forbidden_inference_catalog_is_integrated(self) -> None:
        for negative in FROZEN_NEGATIVES:
            self.assertIn(negative, self.prd)
        self.assertIn("U08 | v4.1–v4.6 carry-forward negatives", self.t07)
        self.assertIn("Frozen Product negative catalog remains present", self.t07)
        self.assertIn("v4.1–v4.6 carry-forward forbidden inferences", self.reference)

    def test_owner_suites_execute_instead_of_textual_pass_manufacture(self) -> None:
        for suite in OWNER_SUITES:
            proc = subprocess.run(
                [sys.executable, "-B", suite],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
            )
            self.assertEqual(
                proc.returncode,
                0,
                msg=f"{suite} failed:\n{proc.stdout}",
            )

    def test_historical_alias_payload_and_adoption_compatibility_are_preserved(self) -> None:
        for alias in COMPATIBILITY_ALIASES:
            self.assertTrue((ROOT / alias).is_file(), alias)
            self.assertIn(alias, self.t09)
            self.assertIn(alias, self.closure)
        self.assertIn("historical manifest/payload/adoption evidence remains readable", self.reference)
        self.assertIn("old aliases/payloads/history are not reinterpreted", self.closure)
        self.assertIn("no physical path migration is authorized by T10", self.closure)

    def test_fast_path_and_non_applicability_remain_proportional(self) -> None:
        for text in (self.t09, self.closure, self.reference):
            self.assertIn("Fast Path", text)
            self.assertIn("optional", text.lower())
        self.assertIn("Optional/non-applicable capability stays optional/non-applicable.", self.t09)
        self.assertIn("Fast Path proportionality remains intact", self.t09)

    def test_fresh_agent_evidence_keeps_static_and_real_fidelity_separate(self) -> None:
        self.assertEqual(self.t08["evidence_class"], "STATIC_OR_RECONSTRUCTION")
        self.assertEqual(self.t08["authority_effect"], "NONE")
        self.assertEqual(self.t08["gate_effect"], "NONE")
        self.assertEqual(self.t08["real_fresh_session"]["state"], "NOT_RUN")
        for text in (self.closure, self.reference):
            self.assertIn("static/reconstruction", text.lower())
            self.assertIn("REAL fresh-session", text)

    def test_exact_subject_and_fidelity_do_not_transfer(self) -> None:
        good = dict(
            requested_head="head-a",
            observed_head="head-a",
            expected_base="base-a",
            observed_base="base-a",
            required_fidelity="real-host",
            observed_fidelity="real-host",
        )
        self.assertTrue(exact_subject_matches(**good))
        for key, value in (
            ("observed_head", "head-b"),
            ("observed_base", "base-b"),
            ("observed_fidelity", "sandbox"),
        ):
            mutated = {**good, key: value}
            self.assertFalse(exact_subject_matches(**mutated), key)

    def test_unavailable_waived_stale_or_unknown_never_become_pass(self) -> None:
        for state in ("UNAVAILABLE", "WAIVED", "STALE", "MISMATCHED", "UNKNOWN"):
            self.assertEqual(fail_closed_input_state(state), "BLOCKED")
        for state in ("NOT_RUN", "BLOCKED", "NOT_APPLICABLE"):
            self.assertEqual(fail_closed_input_state(state), state)
        self.assertNotEqual(fail_closed_input_state("WAIVED"), "PASS")

    def test_closure_inputs_are_durable_exact_bound_and_non_verdict(self) -> None:
        required = (
            "T10 DURABLE CLOSURE INPUTS — NON-VERDICT",
            "b2a4cd3f984dd704f864e20b0e8624536ca0c396",
            "8b4072b6afdcbe903888abd9f6e96a4252ddee64",
            "4dea6fb49c6e185aaff15aabae760e183ede2ab2",
            "CLOSURE_EFFECT=NONE",
            "RELEASE_EFFECT=NONE",
            "independent exact-head/current-target",
            "Fresh Independent Review",
            "Hidden Validation",
        )
        for token in required:
            self.assertIn(token, self.closure)
        for token in FORBIDDEN_T10_VERDICTS:
            self.assertEqual(
                self.closure.count(token),
                1,
                msg=f"{token} must appear only in the final explicit prohibition",
            )

    def test_reference_is_owner_map_not_new_authority(self) -> None:
        required = (
            "T10 NON-AUTHORITATIVE EVIDENCE / OWNER MAP — NON-VERDICT",
            "AUTHORITY_EFFECT=NONE",
            "MUTATION_AUTHORITY=NONE",
            "GATE_EFFECT=NONE",
            "CLOSURE_EFFECT=NONE",
            "RELEASE_EFFECT=NONE",
            "T07 `U01`–`U07`",
            "T08 dogfood artifacts + focused suite",
            "T09 wiring + focused suite",
            "different independent actor",
        )
        for token in required:
            self.assertIn(token, self.reference)
        for token in FORBIDDEN_T10_VERDICTS:
            self.assertEqual(
                self.reference.count(token),
                1,
                msg=f"{token} must appear only in the explicit forbidden-claims list",
            )

    def test_open_contradictions_and_downstream_gates_remain_fail_closed(self) -> None:
        required = (
            "Frozen Product/L2 contradiction -> `BLOCKED`",
            "T10 integration Validation | `NOT_RUN`",
            "T10 Fresh Independent Review | `NOT_RUN`",
            "Version Closure | `NOT_RUN`",
            "Hidden Validation / Release Qualification | `NOT_RUN`",
        )
        for token in required:
            self.assertIn(token, self.closure)
        self.assertIn("route to Planning/currentness authority", self.closure)
        self.assertIn("T10 does not repair owner semantics", self.closure)


if __name__ == "__main__":
    unittest.main()
