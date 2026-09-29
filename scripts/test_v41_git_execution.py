from __future__ import annotations

from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
STANDARD = ROOT / "standards" / "GIT_EXECUTION_STANDARD.md"
REFERENCE = ROOT / "references" / "GIT_EXECUTION_REFERENCE.md"


def writable_workspace_conflict(operators: list[dict[str, str]]) -> bool:
    writers = [op for op in operators if op.get("mode") == "write"]
    seen: set[str] = set()
    for writer in writers:
        workspace = writer["workspace"]
        if workspace in seen:
            return True
        seen.add(workspace)
    return False


def evidence_reusable_after_rewrite(old_sha: str, new_sha: str) -> bool:
    return old_sha == new_sha


def destructive_cleanup_allowed(owner: str | None, classification: str) -> bool:
    return bool(owner) and classification in {"owned", "authorized-disposable"}


class V41GitExecutionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.standard = STANDARD.read_text(encoding="utf-8")
        cls.reference = REFERENCE.read_text(encoding="utf-8")

    def test_local_branch_or_worktree_is_non_authoritative(self) -> None:
        self.assertIn("Local Git facts are non-authoritative", self.standard)
        self.assertIn("Branch existence never means a Task is claimed", self.standard)

    def test_concurrent_writers_require_distinct_workspaces(self) -> None:
        self.assertTrue(
            writable_workspace_conflict(
                [
                    {"operator": "A", "mode": "write", "workspace": "repo-1"},
                    {"operator": "B", "mode": "write", "workspace": "repo-1"},
                ]
            )
        )
        self.assertFalse(
            writable_workspace_conflict(
                [
                    {"operator": "A", "mode": "write", "workspace": "repo-A"},
                    {"operator": "B", "mode": "write", "workspace": "repo-B"},
                ]
            )
        )
        self.assertIn("Two logically independent concurrent writers MUST NOT mutate the same writable workspace", self.standard)

    def test_exact_subject_checkout_is_explicit(self) -> None:
        for phrase in (
            "requested SHA/ref and actual checked-out SHA",
            "current PR HEAD/base identity",
            "working-tree cleanliness",
        ):
            self.assertIn(phrase, self.standard)
        self.assertIn("git checkout --detach", self.reference)

    def test_rewrite_does_not_transfer_old_exact_sha_evidence(self) -> None:
        self.assertTrue(evidence_reusable_after_rewrite("a" * 40, "a" * 40))
        self.assertFalse(evidence_reusable_after_rewrite("a" * 40, "b" * 40))
        self.assertIn("old exact SHA remains historical", self.standard.replace("Evidence attached to an old exact SHA remains historical", "old exact SHA remains historical"))
        self.assertIn("Tree similarity does not rewrite it", self.reference)

    def test_destructive_cleanup_fails_closed_when_ownership_unknown(self) -> None:
        self.assertFalse(destructive_cleanup_allowed(None, "unknown"))
        self.assertFalse(destructive_cleanup_allowed("agent-A", "unknown"))
        self.assertTrue(destructive_cleanup_allowed("agent-A", "owned"))
        self.assertIn("destructive operations MUST fail closed", self.standard)

    def test_cherry_pick_cannot_bypass_task_dag_or_central_wiring(self) -> None:
        self.assertIn("Cherry-pick is a transport mechanism for commits, not Task-DAG authority", self.standard)
        self.assertIn("Central/shared wiring explicitly owned by another Task MUST remain with that owner", self.standard)

    def test_stacked_pr_is_code_topology_not_live_task_dag(self) -> None:
        self.assertIn("Stacked PRs describe real unmerged code-baseline dependency", self.standard)
        self.assertIn("not a substitute for GitHub Issue Dependencies", self.standard)

    def test_recovery_protects_unpublished_work(self) -> None:
        for phrase in ("reflog", "stash", "unpublished commits", "submodule", "LFS", "sparse", "partial-clone"):
            self.assertIn(phrase, self.standard)
        self.assertIn("Before removing a worktree or branch", self.reference)

    def test_worktree_is_reference_not_mandatory_technology(self) -> None:
        self.assertIn("reference mechanism, not mandatory technology", self.standard)
        self.assertIn("independent clone or isolated container checkout", self.reference)


if __name__ == "__main__":
    unittest.main()
