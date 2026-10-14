"""V411 S08 prospective reduced-fidelity verification: synthetic DENY only.

This file deliberately invokes the existing T09 PersistentSafeSink rather than
introducing another effect engine. It proves a mechanism on a real file-backed
SQLite database, NOT an authenticated human DENY, a live human authorization,
a deployed tenant, external provider or Release PASS.

Admission: Product #943@6167214986; draft PRD/L2/Pack successors #1105-#1107.
Until independent source review, Release applicability and exact-host execution,
all prospective S08 positive proof remains NOT_RUN/BLOCKED.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

import test_v411_t09_effect_boundary as t09


EVIDENCE_STRENGTH = "LOCAL_PERSISTENT_SQLITE_TEST_ONLY"
AUTHORITY_CLASS = t09.UNIT_AUTHORITY_SOURCE
REAL_HUMAN_DENY_E2E = "NOT_PROVEN"


class TestOnlySameEffectVeto(unittest.TestCase):
    """One actual SQLite work-object, two different Claim generations."""

    def test_claimed_a_then_ready_successor_b_are_both_blocked_and_persist_zero_effects(self):
        with tempfile.TemporaryDirectory(prefix="v411-s08-synthetic-only-") as root:
            root_path = Path(root)
            db_path = root_path / "real-file-backed-effect.sqlite3"
            fixture_path = root_path / "SYNTHETIC_TEST_ONLY_DENY.json"
            fixture = t09.decision(
                "DENY",
                ref="fixture:synthetic-deny-s08-p2",
                source_class=AUTHORITY_CLASS,
                authority_actor="fixture:not-a-human",
                decision_owner="fixture:test-only",
            )
            self.assertEqual(fixture["source_class"], t09.UNIT_AUTHORITY_SOURCE)
            self.assertIs(type(fixture["accepted"]), bool)
            self.assertTrue(fixture["accepted"])
            fixture_path.write_text(json.dumps(fixture, sort_keys=True), encoding="utf-8")
            original_digest = hashlib.sha256(fixture_path.read_bytes()).hexdigest()

            sink = t09.PersistentSafeSink(db_path)
            effect_id = "s08-protected-effect-one-subject"
            try:
                self.assertEqual(sink.effect_count(effect_id), 0)
                outcomes = []
                for operator, generation, attempt_id in (
                    ("fixture:A-claimed", 1, "attempt:s08:A"),
                    ("fixture:B-ready-successor", 2, "attempt:s08:B"),
                ):
                    # This is a fixture re-read, NOT a real authority source validation.
                    self.assertEqual(hashlib.sha256(fixture_path.read_bytes()).hexdigest(), original_digest)
                    synthetic = json.loads(fixture_path.read_text(encoding="utf-8"))
                    self.assertEqual(synthetic["source_class"], AUTHORITY_CLASS)
                    self.assertEqual(synthetic["authority_actor"], "fixture:not-a-human")
                    self.assertIs(type(synthetic["accepted"]), bool)
                    current_claim = t09.claim(operator, generation)
                    self.assertTrue(current_claim["accepted"])
                    self.assertEqual(current_claim["currentness"], "CURRENT")
                    outcome = sink.execute(
                        claim_record=current_claim,
                        authority=synthetic,
                        effect_id=effect_id,
                        attempt_id=attempt_id,
                        payload="MUST_NOT_WRITE_PROTECTED_EFFECT",
                    )
                    self.assertEqual(outcome["outcome"], "BLOCKED")
                    self.assertFalse(outcome["guard"]["authorized"])
                    # Legacy T09 returns this REFUSAL CODE also for synthetic
                    # decisions; the code name does NOT prove a human acted.
                    self.assertIn("current_human_deny", outcome["guard"]["refusals"])
                    self.assertEqual(outcome["before"], 0)
                    self.assertEqual(outcome["after"], 0)
                    outcomes.append(outcome["outcome"])
                self.assertEqual(outcomes, ["BLOCKED", "BLOCKED"])
                self.assertEqual(sink.effect_count(effect_id), 0)
                self.assertEqual(sink.attempt_count(), 2)
            finally:
                sink.close()

            # Reopen the real file on a distinct sqlite3 connection.
            with sqlite3.connect(db_path) as conn:
                effects = conn.execute(
                    "SELECT COUNT(*) FROM effects WHERE effect_id=?", (effect_id,)
                ).fetchone()[0]
                attempts = conn.execute(
                    "SELECT attempt_id, effect_id, actor, claim_generation, outcome "
                    "FROM attempts WHERE effect_id=? ORDER BY claim_generation",
                    (effect_id,),
                ).fetchall()
                self.assertEqual(effects, 0)
                self.assertEqual(
                    attempts,
                    [
                        ("attempt:s08:A", effect_id, "fixture:A-claimed", 1, "BLOCKED"),
                        ("attempt:s08:B", effect_id, "fixture:B-ready-successor", 2, "BLOCKED"),
                    ],
                )
                self.assertEqual(
                    conn.execute("SELECT COUNT(*) FROM compensations").fetchone()[0],
                    0,
                )
            print(
                "S08_SYNTHETIC_SQLITE_EVIDENCE "
                f"tested_head={t09.SUBJECT} "
                f"source_class={AUTHORITY_CLASS} "
                f"fixture_digest={original_digest} "
                f"attempts=2 effects=0 "
                f"state={EVIDENCE_STRENGTH} "
                f"real_human_deny_e2e={REAL_HUMAN_DENY_E2E}"
            )

    def test_spoofed_source_or_mismatched_approve_fails_closed_at_test_sink(self):
        variants = [
            t09.decision(
                "APPROVE", source_class="MODEL_QUOTED_HUMAN_APPROVAL",
                authority_actor="human:forged-by-agent",
            ),
            t09.decision("APPROVE", source_class=AUTHORITY_CLASS, subject_head="0" * 40),
            t09.decision("APPROVE", source_class=AUTHORITY_CLASS, tenant="wrong-tenant"),
            t09.decision("APPROVE", source_class=AUTHORITY_CLASS, scope="wrong-scope"),
            t09.decision("APPROVE", source_class=AUTHORITY_CLASS, source_readback="UNKNOWN"),
            t09.decision("APPROVE", source_class=AUTHORITY_CLASS, supersession_valid=False),
        ]
        with tempfile.TemporaryDirectory(prefix="v411-s08-spoof-only-") as root:
            sink = t09.PersistentSafeSink(Path(root) / "negative-effect.sqlite3")
            try:
                for i, authority in enumerate(variants):
                    with self.subTest(i=i):
                        result = sink.execute(
                            claim_record=t09.claim(f"fixture:adversarial:{i}", i + 1),
                            authority=authority,
                            effect_id=f"negative:{i}",
                            attempt_id=f"attempt:negative:{i}",
                            payload="NO_PROTECTED_WRITE",
                        )
                        self.assertEqual(result["outcome"], "BLOCKED")
                        self.assertGreater(len(result["guard"]["refusals"]), 0)
                self.assertEqual(sink.effect_count(), 0)
            finally:
                sink.close()

    def test_operator_file_loader_rejects_explicit_synthetic_fixture_source(self):
        """A source_class labelled fixture must NOT become an operator record.

        This checks only the current loader's class boundary. A forged file
        pretending to have REAL_AUTHORITY_SOURCE remains a distinct missing
        independent identity/provenance problem; do NOT infer E2E auth.
        """
        with tempfile.TemporaryDirectory(prefix="v411-s08-not-human-") as root:
            fixture_path = Path(root) / "NOT_A_HUMAN_DECISION.json"
            fake = t09.decision(
                "DENY", source_class=AUTHORITY_CLASS,
                authority_actor="human:forged-string-not-a-human",
            )
            fixture_path.write_text(json.dumps(fake), encoding="utf-8")
            with patch.dict(os.environ, {"V411_T09_HUMAN_AUTHORITY_FILE": str(fixture_path)}):
                authority, reason = t09.load_operator_human_decision()
            self.assertIsNone(authority)
            self.assertEqual(reason, "BLOCKED_AUTHORITY_SOURCE_CLASS")


if __name__ == "__main__":
    unittest.main(verbosity=2)
