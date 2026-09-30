"""T07 bounded maintenance/hotfix dogfood: a real disposable Git cherry-pick.

This is a fixture-level conformance test, NOT Validation of an actual project's
maintenance-branch result or a Release/Deployment qualification.
Run: python3 -m unittest scripts/test_v45_maintenance_hotfix_conformance.py -v
Requires git >= 2.28 on PATH; modifies only a temporary directory.
"""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "docs" / "implementation" / "4.5.0" / "dogfood" / "maintenance-hotfix"
CASE = json.loads((FIXTURES / "case.json").read_text(encoding="utf-8"))
POLICY = json.loads((FIXTURES / "support-policy.json").read_text(encoding="utf-8"))
SHA1 = re.compile(r"^[0-9a-f]{40}$")


def git(repo: Path, *args: str, date: str | None = None) -> str:
    env = os.environ.copy()
    env.update({
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": str(repo / ".empty-global-gitconfig"),
        "GIT_AUTHOR_NAME": "ADS fixture author",
        "GIT_AUTHOR_EMAIL": "fixture-author@example.invalid",
        "GIT_COMMITTER_NAME": "ADS fixture committer",
        "GIT_COMMITTER_EMAIL": "fixture-committer@example.invalid",
        "GIT_TERMINAL_PROMPT": "0",
        "LC_ALL": "C",
    })
    if date:
        env["GIT_AUTHOR_DATE"] = date
        env["GIT_COMMITTER_DATE"] = date
    # Force SHA-1 to ensure the pinned exact fixture commit identities remain stable.
    proc = subprocess.run(
        ["git", "-c", "core.autocrlf=false", "-c", "commit.gpgsign=false", *args],
        cwd=repo, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=False,
    )
    if proc.returncode:
        raise RuntimeError(f"fixture git {args!r} failed ({proc.returncode}): {proc.stderr.strip()}")
    return proc.stdout.strip()


def provision(repo: Path) -> dict[str, str]:
    """Controlled disposable source/maintenance divergence, then true cherry-pick."""
    git(repo, "init", "-q", "--object-format=sha1", "--initial-branch=main")
    (repo / "service.txt").write_text("line=v2\nsecurity_bug=vulnerable\n", encoding="utf-8")
    git(repo, "add", "service.txt")
    git(repo, "commit", "-qm", "fixture: v2 maintained baseline", date="2001-01-01T00:00:00+0000")
    baseline_sha = git(repo, "rev-parse", "HEAD")

    (repo / "next-release.txt").write_text("new-main-only-context=true\n", encoding="utf-8")
    git(repo, "add", "next-release.txt")
    git(repo, "commit", "-qm", "fixture: main-only context", date="2001-01-02T00:00:00+0000")
    (repo / "service.txt").write_text("line=v2\nsecurity_bug=patched\n", encoding="utf-8")
    git(repo, "add", "service.txt")
    git(repo, "commit", "-qm", "fixture: source security correction", date="2001-01-03T00:00:00+0000")
    source_sha = git(repo, "rev-parse", "HEAD")

    git(repo, "checkout", "-qb", "maintenance/v2", baseline_sha)
    if git(repo, "rev-parse", "HEAD") != baseline_sha:
        raise AssertionError("maintenance baseline drifted before cherry-pick")
    git(repo, "cherry-pick", source_sha, date="2001-01-04T00:00:00+0000")
    result_sha = git(repo, "rev-parse", "HEAD")
    return {
        "source_branch": "main",
        "source_sha": source_sha,
        "target_support_line": "maintenance/v2",
        "target_baseline_sha": baseline_sha,
        "result_sha": result_sha,
    }


def policy_allows(policy: dict, case: dict) -> bool:
    """Only a durable matching owner/policy line authorizes a change class.

    This deliberately does NOT use Git branch/tag/package availability as policy.
    """
    if case.get("policy_id") != policy.get("policy_id") or case.get("product_ref") != policy.get("product_or_component_ref"):
        return False
    matching = [line for line in policy.get("support_lines", []) if line.get("line_id") == case.get("target_support_line")]
    if len(matching) != 1:
        return False
    line = matching[0]
    return bool(
        line.get("baseline_ref") == case.get("target_baseline_sha")
        and line.get("authority_ref") == case.get("owner_ref")
        and line.get("support_state") == "SECURITY_ONLY"
        and case.get("change_class") in line.get("allowed_change_classes", [])
        and SHA1.fullmatch(case.get("source_sha", ""))
        and SHA1.fullmatch(case.get("result_sha", ""))
    )


def evidence_binds_result(evidence: dict | None, result_sha: str) -> bool:
    """Identity check only; does NOT authenticate external evidence or issue PASS."""
    return bool(
        isinstance(evidence, dict)
        and evidence.get("subject_sha") == result_sha
        and SHA1.fullmatch(result_sha)
        and evidence.get("status") == "PASS"
        and evidence.get("evidence_ref")
        and evidence.get("environment_ref")
        and evidence.get("authority_ref")
    )


class MaintenanceHotfixConformance(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temp = tempfile.TemporaryDirectory(prefix="ads-t07-git-fixture-")
        cls.repo = Path(cls.temp.name)
        cls.actual = provision(cls.repo)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temp.cleanup()

    def test_01_exact_identity_pinned_to_repeatable_real_cherry_pick(self) -> None:
        for key, value in self.actual.items():
            self.assertEqual(value, CASE[key], f"pinned fixture identity drift: {key}")
        self.assertNotEqual(self.actual["source_sha"], self.actual["result_sha"])
        self.assertTrue(all(SHA1.fullmatch(self.actual[k]) for k in (
            "source_sha", "target_baseline_sha", "result_sha")))
        self.assertEqual(git(self.repo, "branch", "--show-current"), "maintenance/v2")
        self.assertEqual(git(self.repo, "rev-parse", "HEAD^"), self.actual["target_baseline_sha"])
        self.assertEqual(git(self.repo, "rev-parse", "main"), self.actual["source_sha"])
        self.assertEqual(git(self.repo, "show", f'{self.actual["result_sha"]}:service.txt'),
                         "line=v2\nsecurity_bug=patched")
        self.assertEqual(
            git(self.repo, "diff", f'{self.actual["source_sha"]}^', self.actual["source_sha"], "--", "service.txt"),
            git(self.repo, "diff", self.actual["target_baseline_sha"], self.actual["result_sha"], "--", "service.txt"),
        )
        # Main-only context did not silently migrate into the maintained line.
        self.assertNotIn("next-release.txt", git(self.repo, "ls-tree", "--name-only", self.actual["result_sha"]))

    def test_02_policy_authority_not_git_topology(self) -> None:
        policy = copy.deepcopy(POLICY)
        policy["support_lines"][0]["baseline_ref"] = self.actual["target_baseline_sha"]
        self.assertTrue(policy_allows(policy, CASE))
        for mutation in (
            {"target_support_line": "unlisted/branch"},
            {"target_baseline_sha": self.actual["source_sha"]},
            {"change_class": "new-feature"},
            {"owner_ref": "untrusted-caller"},
            {"policy_id": "fabricated-policy"},
            {"product_ref": "other-project"},
        ):
            with self.subTest(mutation=mutation):
                self.assertFalse(policy_allows(policy, CASE | mutation))
        eol = copy.deepcopy(policy)
        eol["support_lines"][0]["support_state"] = "EOL"
        self.assertFalse(policy_allows(eol, CASE))
        self.assertEqual(git(self.repo, "branch", "--list", "maintenance/v2"), "* maintenance/v2")

    def test_03_policy_baseline_is_pinned_not_placeholder(self) -> None:
        self.assertEqual(POLICY["support_lines"][0]["baseline_ref"], self.actual["target_baseline_sha"])
        self.assertEqual(POLICY["support_lines"][0]["authority_ref"], CASE["owner_ref"])
        self.assertEqual(POLICY["support_lines"][0]["allowed_change_classes"], ["security-fix"])

    def test_04_fresh_result_focused_test_is_not_source_test(self) -> None:
        # Actual Git show reads the RESULT commit, not source HEAD, and checks its behavior.
        self.assertEqual(git(self.repo, "show", f'{CASE["result_sha"]}:service.txt').splitlines()[1],
                         "security_bug=patched")
        self.assertEqual(CASE["fixture_testing"]["subject_sha"], CASE["result_sha"])
        self.assertEqual(CASE["fixture_testing"]["fidelity"], "DISPOSABLE_GIT_FIXTURE_ONLY")
        self.assertNotEqual(CASE["source_evidence_claim"]["subject_sha"], CASE["result_sha"])

    def test_05_source_pass_and_stale_result_claim_never_transfer(self) -> None:
        self.assertFalse(evidence_binds_result(CASE["source_evidence_claim"], CASE["result_sha"]))
        stale = dict(CASE["source_evidence_claim"], status="PASS", evidence_ref="fixture:stale",
                     environment_ref="fixture:source", authority_ref="fixture:source")
        self.assertFalse(evidence_binds_result(stale, CASE["result_sha"]))
        for candidate in (
            {"status": "PASS", "subject_sha": CASE["result_sha"]},
            {"status": "PASS", "subject_sha": CASE["result_sha"], "evidence_ref": "claim"},
            {"status": "PASS", "subject_sha": CASE["result_sha"], "evidence_ref": "claim", "environment_ref": "fixture"},
            {"status": "BLOCKED", "subject_sha": CASE["result_sha"], "evidence_ref": "claim", "environment_ref": "fixture", "authority_ref": "owner"},
        ):
            self.assertFalse(evidence_binds_result(candidate, CASE["result_sha"]))
        # Even a syntactically matched tuple would still need real independent
        # authority/provenance verification; identity matching alone is not PASS.
        synthetic = {"status": "PASS", "subject_sha": CASE["result_sha"],
                     "evidence_ref": "not-a-real-report", "environment_ref": "synthetic",
                     "authority_ref": "synthetic"}
        self.assertTrue(evidence_binds_result(synthetic, CASE["result_sha"]))
        self.assertEqual(CASE["real_project_result_validation"]["status"], "NOT_RUN")
        self.assertEqual(CASE["real_project_result_validation"]["evidence_ref"], None)

    def test_06_hotfix_fast_path_release_deployment_separation(self) -> None:
        self.assertEqual(CASE["fast_path"]["waived_optional_ceremony"], ["batch-scheduling"])
        self.assertEqual(CASE["fast_path"]["required_gates"], [
            "exact-result-testing", "exact-result-validation", "fresh-independent-review",
            "release-qualification", "rollback-when-applicable",
        ])
        self.assertEqual(CASE["real_project_result_validation"]["status"], "NOT_RUN")
        self.assertEqual(CASE["fresh_independent_review"]["status"], "NOT_RUN")
        self.assertEqual(CASE["release_qualification"]["status"], "NOT_RUN")
        self.assertEqual(CASE["deployment_result"]["status"], "NOT_RUN")
        self.assertEqual(CASE["backport_preparation"]["status"], "FIXTURE_ONLY")
        self.assertEqual(CASE["real_backport_completion"]["status"], "NOT_RUN")

    def test_07_no_real_project_pass_in_bounded_fixture(self) -> None:
        self.assertEqual(CASE["fidelity"], "CONTROLLED_DISPOSABLE_GIT_NOT_PROJECT_MAINTENANCE")
        for field in ("real_project_result_validation", "fresh_independent_review",
                      "release_qualification", "deployment_result", "real_backport_completion"):
            self.assertNotEqual(CASE[field]["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
