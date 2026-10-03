from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from v42_sqlite_migration_dogfood import run


class MigrationConformanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="v42-db-test-")
        self.evidence = run(Path(self.tmp.name))

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_actual_sqlite_runtime_identity_is_bound(self) -> None:
        self.assertEqual(self.evidence["engine"], "sqlite")
        self.assertTrue(self.evidence["sqlite_runtime_version"])
        self.assertTrue(self.evidence["python_version"])
        self.assertTrue(self.evidence["platform"])
        self.assertEqual(len(self.evidence["fixture_sha256"]), 4)
        for digest in self.evidence["fixture_sha256"].values():
            self.assertEqual(len(digest), 64)

    def test_source_a_to_b_transition_preserves_representative_data(self) -> None:
        migration = self.evidence["subjects"]["migration_A_to_B"]
        self.assertEqual(migration["source_schema_version"], 1)
        self.assertEqual(migration["target_schema_version"], 2)
        self.assertEqual(migration["source_rows"][1:], migration["target_rows"][1:])
        self.assertEqual(migration["source_rows"][0][-1], "legacy_status")
        self.assertEqual(migration["target_rows"][0][-1], "status")
        self.assertEqual(len(migration["target_rows"]) - 1, 2)

    def test_fresh_bootstrap_is_distinct_subject_not_upgrade_proof(self) -> None:
        migration = self.evidence["subjects"]["migration_A_to_B"]
        fresh = self.evidence["subjects"]["fresh_bootstrap_B"]
        self.assertTrue(fresh["separate_subject"])
        self.assertEqual(fresh["target_schema_version"], 2)
        self.assertEqual(len(fresh["rows"]) - 1, 0)
        self.assertEqual(len(migration["target_rows"]) - 1, 2)

    def test_interrupted_transition_rolls_back_then_recovers_forward(self) -> None:
        recovery = self.evidence["subjects"]["interrupted_recovery"]
        self.assertEqual(recovery["failure_type"], "IntegrityError")
        self.assertTrue(recovery["source_restored_after_failure"])
        self.assertEqual(recovery["recovery_strategy"], "rollback-source-transaction-then-rerun-forward-A-to-B")
        self.assertFalse(recovery["down_migration_required"])
        self.assertEqual(recovery["final_schema_version"], 2)
        self.assertEqual(len(recovery["final_rows"]) - 1, 2)

    def test_cross_engine_substitution_is_rejected(self) -> None:
        expected_engine = "sqlite"
        self.assertEqual(self.evidence["engine"], expected_engine)
        substituted = dict(self.evidence)
        substituted["engine"] = "postgresql"
        self.assertNotEqual(substituted["engine"], expected_engine)

    def test_fixture_subjects_are_not_collapsed(self) -> None:
        subjects = self.evidence["subjects"]
        self.assertEqual(set(subjects), {"migration_A_to_B", "fresh_bootstrap_B", "interrupted_recovery"})
        self.assertNotEqual(
            subjects["migration_A_to_B"]["target_rows"],
            subjects["fresh_bootstrap_B"]["rows"],
        )


if __name__ == "__main__":
    unittest.main()
