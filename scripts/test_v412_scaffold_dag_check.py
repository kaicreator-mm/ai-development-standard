#!/usr/bin/env python3
"""Focused pure-Git, offline v4.12 source-pair checker regression cases."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from v412_scaffold_dag_check import Reject, evaluate, digest


def git(repo, *argv):
    p = subprocess.run(["git", "-C", str(repo), *argv], check=True, capture_output=True)
    return p.stdout.decode().strip()


def write(repo, path, text):
    path = repo / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf8")


def commit(repo, title):
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", title)
    return git(repo, "rev-parse", "HEAD")


class GitConsumer(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        git(self.repo, "init", "-q")
        git(self.repo, "config", "user.name", "ADS Synthetic Test")
        git(self.repo, "config", "user.email", "synthetic@example.invalid")
        self.l2 = "1" * 40
        self.scope = {
            "schema": "v412-sf-scope-v1", "product_blob": "2" * 40, "l2_blob": self.l2,
            "anchors": [{"anchor_id": "A1", "kind": "module",
                         "location": "app/core.py", "contract_ref": "L2:module:A1"}],
            "exemptions": {
                "docs/df.json": {"role": "DAG_ONLY_INPUT",
                                 "approved_l2_blob": self.l2, "approval_ref": "L2-R3:ADR03"},
                "docs/derived.json": {"role": "DERIVED_NONAUTHORITATIVE_OUTPUT",
                                      "approved_l2_blob": self.l2, "approval_ref": "L2-R3:ADR03"},
                "docs/pair.json": {"role": "FREEZE_RECORD_OUTPUT",
                                   "approved_l2_blob": self.l2, "approval_ref": "L2-R3:ADR03"},
            }
        }
        write(self.repo, "app/core.py", "def compute(): return 1\n")
        write(self.repo, "docs/scope.json", json.dumps(self.scope))
        self.sf = commit(self.repo, "accepted source-first")
        self.binding = {"schema": "v412-df-binding-v1",
                        "writers": [{"anchor_id": "A1", "task_id": "T001", "issue": 123,
                                     "writer_paths": ["app/core.py"], "issue_allowed": ["app/core.py"],
                                     "issue_forbidden": ["secrets.txt"], "claim_ref": "#123@valid-claim"}]}
        self.set_df()

    def tearDown(self):
        self.tmp.cleanup()

    def set_df(self):
        write(self.repo, "docs/df.json", json.dumps(self.binding))
        self.df = commit(self.repo, "Task side binding")

    def check(self, **kwargs):
        return evaluate(self.repo, self.sf, self.df, "docs/scope.json",
                        "docs/df.json", **kwargs)

    def test_new_project_positive_no_external_gate_invention(self):
        result = self.check()
        self.assertEqual(result["source_pair"], "PASS_E1")
        self.assertEqual(result["external_authority"]["github_claim"], "NOT_RUN")
        self.assertEqual(result["maps"]["task_to_anchors"], {"T001": ["A1"]})

    def test_mature_existing_source_reused(self):
        write(self.repo, "README.md", "# Existing mature consumer\n")
        self.sf = commit(self.repo, "pre-existing mature source accepted")
        self.binding["writers"][0]["task_id"] = "T002"
        self.set_df()
        self.assertEqual(self.check()["source_pair"], "PASS_E1")

    def test_binding_change_changes_mi_not_material_source(self):
        first = self.check()
        self.binding["writers"][0]["task_id"] = "T002"
        self.set_df()
        second = self.check()
        self.assertEqual(first["subject"]["sf_mv"], second["subject"]["sf_mv"])
        self.assertNotEqual(first["subject"]["mi_digest"], second["subject"]["mi_digest"])

    def test_changed_module_material(self):
        write(self.repo, "app/core.py", "def compute(): return 2\n")
        self.df = commit(self.repo, "material source changed")
        with self.assertRaisesRegex(Reject, "MATERIAL_SOURCE_DRIFT"):
            self.check()

    def test_added_source_and_unknown_lock_material(self):
        for name in ("other/new.txt", "poetry.lock"):
            with self.subTest(path=name):
                write(self.repo, name, "new")
                self.df = commit(self.repo, "added source")
                with self.assertRaisesRegex(Reject, "MATERIAL_SOURCE_DRIFT"):
                    self.check()

    def test_tab_newline_paths_nul_safe(self):
        # Win32 forbids control characters in filesystem paths. Only an
        # actual POSIX Git object can validate the end-to-end NUL-safe scan.
        if os.name == "nt":
            self.skipTest("Windows cannot create Git-tracked tab/newline paths; run on Linux")
        write(self.repo, "app/weird\tname\nfile.txt", "weird")
        self.sf = commit(self.repo, "special path accepted")
        self.binding["writers"][0]["task_id"] = "T002"
        self.set_df()
        self.assertEqual(self.check()["source_pair"], "PASS_E1")

    def test_renamed_tracked_source_material(self):
        git(self.repo, "mv", "app/core.py", "app/moved.py")
        self.df = commit(self.repo, "renamed module")
        with self.assertRaisesRegex(Reject, "MATERIAL_SOURCE_DRIFT"):
            self.check()

    def test_gitlink_addition_material(self):
        # An index-only Git link has mode 160000: not a regular blob.
        git(self.repo, "update-index", "--add", "--cacheinfo",
            "160000," + ("f" * 40) + ",third-party")
        git(self.repo, "commit", "-qm", "added synthetic gitlink")
        self.df = git(self.repo, "rev-parse", "HEAD")
        with self.assertRaisesRegex(Reject, "MATERIAL_SOURCE_DRIFT"):
            self.check()

    def test_symlink_mode_change_material(self):
        # Set Git index mode 120000 directly; Windows does not require
        # SeCreateSymbolicLinkPrivilege to assert Git-object drift.
        blob = git(self.repo, "hash-object", "-w", "app/core.py")
        git(self.repo, "update-index", "--add", "--cacheinfo",
            "120000," + blob + ",shortcut")
        git(self.repo, "commit", "-qm", "new index-only symlink")
        self.df = git(self.repo, "rev-parse", "HEAD")
        with self.assertRaisesRegex(Reject, "MATERIAL_SOURCE_DRIFT"):
            self.check()

    def test_deleted_file_material(self):
        (self.repo / "app/core.py").unlink()
        self.df = commit(self.repo, "removed module")
        with self.assertRaisesRegex(Reject, "MATERIAL_SOURCE_DRIFT"):
            self.check()

    def test_scope_manifest_self_exception_rejected(self):
        self.scope["exemptions"]["docs/scope.json"] = {
            "role": "DAG_ONLY_INPUT", "approved_l2_blob": self.l2, "approval_ref": "forged"}
        write(self.repo, "docs/scope.json", json.dumps(self.scope))
        self.sf = commit(self.repo, "malicious accepted scope")
        self.binding["writers"][0]["task_id"] = "T002"
        self.set_df()
        with self.assertRaisesRegex(Reject, "SCOPE_MANIFEST_CANNOT_EXEMPT_SELF"):
            self.check()

    def test_writer_exceeds_issue_allowlist(self):
        self.binding["writers"][0]["writer_paths"] = ["app/core.py", "sensitive.py"]
        self.set_df()
        with self.assertRaisesRegex(Reject, "WRITER_SCOPE_OUTSIDE_CANONICAL_ISSUE"):
            self.check()

    def test_writer_hits_issue_forbidden(self):
        self.binding["writers"][0]["issue_forbidden"] = ["app/core.py"]
        self.set_df()
        with self.assertRaisesRegex(Reject, "WRITER_SCOPE_OUTSIDE_CANONICAL_ISSUE"):
            self.check()

    def test_duplicate_active_writer(self):
        self.binding["writers"].append(dict(self.binding["writers"][0]))
        self.set_df()
        with self.assertRaisesRegex(Reject, "DUPLICATE_OR_UNBOUND_WRITER"):
            self.check()

    def test_missing_claim_is_not_evidence(self):
        del self.binding["writers"][0]["claim_ref"]
        self.set_df()
        with self.assertRaisesRegex(Reject, "MISSING_CLAIM_REFERENCE"):
            self.check()

    def test_generated_view_recomputed(self):
        record = self.check()
        write(self.repo, "docs/derived.json", json.dumps(record["maps"]))
        self.df = commit(self.repo, "generated mapping")
        self.assertEqual(self.check(derived_path="docs/derived.json")["source_pair"], "PASS_E1")
        write(self.repo, "docs/derived.json", '{"anchor_to_task": {}, "task_to_anchors": {}}')
        self.df = commit(self.repo, "forged mapping")
        with self.assertRaisesRegex(Reject, "FORGED_OR_STALE_DERIVED_OUTPUT"):
            self.check(derived_path="docs/derived.json")

    def test_pair_record_outside_digest_non_recursive(self):
        source = self.check()
        write(self.repo, "docs/pair.json", json.dumps({"sf_commit": self.sf,
                    "df_blob": source["subject"]["df_blob"],
                    "mi_digest": source["subject"]["mi_digest"]}))
        self.df = commit(self.repo, "out-of-input pair record")
        out = self.check(record_path="docs/pair.json")
        self.assertEqual(out["subject"]["mi_digest"], source["subject"]["mi_digest"])
        write(self.repo, "docs/pair.json", '{"sf_commit":"forged"}')
        self.df = commit(self.repo, "corrupt freeze")
        with self.assertRaisesRegex(Reject, "STALE_OR_SELF_REFERENTIAL_FREEZE"):
            self.check(record_path="docs/pair.json")

    def test_binding_self_digest_rejected(self):
        self.binding["df_blob"] = "self"
        self.set_df()
        with self.assertRaisesRegex(Reject, "SELF_REFERENTIAL_DF_INPUT"):
            self.check()

    def test_exempting_source_code_rejected(self):
        self.scope["exemptions"]["app/core.py"] = {
            "role": "DAG_ONLY_INPUT", "approved_l2_blob": self.l2, "approval_ref": "forged"}
        write(self.repo, "docs/scope.json", json.dumps(self.scope))
        self.sf = commit(self.repo, "malicious scope")
        self.binding["writers"][0]["task_id"] = "T002"
        self.set_df()
        with self.assertRaisesRegex(Reject, "EXEMPTION_MAY_HIDE_MATERIAL_SOURCE"):
            self.check()

    def test_deterministic_repeat_no_repo_writes(self):
        before = git(self.repo, "status", "--porcelain")
        one, two = self.check(), self.check()
        self.assertEqual(digest(one), digest(two))
        self.assertEqual(before, git(self.repo, "status", "--porcelain"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
