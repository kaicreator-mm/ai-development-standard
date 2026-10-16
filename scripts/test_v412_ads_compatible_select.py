#!/usr/bin/env python3
"""S05 source-pinned new/mature synthetic consumer and fail-closed selector tests."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from v412_ads_compatible_select import REQUIRED_DIMENSIONS, parse_version, select


def git(repo, *args):
    p = subprocess.run(["git", "-C", str(repo), *args], check=True,
                       capture_output=True, text=True)
    return p.stdout.strip()


def put(repo, path, data):
    target = repo / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(data, encoding="utf-8")


class SelectorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "ads"
        self.repo.mkdir()
        git(self.repo, "init", "-q")
        git(self.repo, "config", "user.name", "ADS Test")
        git(self.repo, "config", "user.email", "ads@example.invalid")
        self.manifest = {"schema_version": 1, "sections": {"normative_standards": [
            "standards/PROJECT_ADOPTION.md", "standards/INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md"]}}
        put(self.repo, "standard-manifest.json", json.dumps(self.manifest))
        put(self.repo, "VERSION", "4.11.0\n")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-qm", "predecessor")
        self.current = git(self.repo, "rev-parse", "HEAD")
        put(self.repo, "VERSION", "4.12.0\n")
        put(self.repo, "standards/PROJECT_ADOPTION.md", "source change")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-qm", "candidate")
        self.candidate = git(self.repo, "rev-parse", "HEAD")
        git(self.repo, "tag", "v4.12.0", self.candidate)
        self.issue = 1096
        self.comment = 987654321
        self.run_id = 1234567
        self.project = {"preference": "TRACK_LATEST_COMPATIBLE_STABLE",
                        "current_revision": self.current, "current_version": "4.11.0",
                        "active_task": False, "frozen_candidate": False}
        self.record = {
            "schema_version": 1, "record_id": "fixture-v412-compat",
            "contract": {"kind": "ADS", "identity": "consumer"},
            "baseline": {"version_ref": "4.11.0", "sha_or_digest": self.current},
            "candidate": {"version_ref": "4.12.0", "sha_or_digest": self.candidate},
            "change_operations": ["MODIFIED"],
            "producer_refs": ["ADS-source-check"], "consumer_refs": ["consumer-check"],
            "dimensions": [{"name": d, "outcome": "COMPATIBLE",
                            "evidence_refs": ["test:proof:" + d]} for d in sorted(REQUIRED_DIMENSIONS)]}
        self.candidates = [{"sha": self.candidate, "release_tag": "v4.12.0",
                            "qualification_issue": self.issue, "qualification_comment": self.comment,
                            "compatibility_record": self.record}]
        self.network_calls = []

    def tearDown(self):
        self.tmp.cleanup()

    def fetch(self, url):
        self.network_calls.append(url)
        if "/releases/tags/" in url:
            return {"tag_name": "v4.12.0", "draft": False, "prerelease": False,
                    "html_url": "https://github.com/kaicreator-mm/ai-development-standard/releases/tag/v4.12.0"}
        if url.endswith("/issues/comments/987654321"):
            return {"id": self.comment,
                    "html_url": f"https://github.com/kaicreator-mm/ai-development-standard/issues/{self.issue}#issuecomment-{self.comment}",
                    "body": ("<!-- ai-dev:event:v2 -->\nevent=RELEASE_QUALIFICATION\n"
                             f"candidate_sha={self.candidate}\n"
                             "qualification=RELEASE_QUALIFIED\n"
                             "actor_role=release-controller\n"
                             "operator_kind=chatgpt-web\n"
                             "operator_id=reviewed-release-context-01\n"
                             "session_ref=release-session-01\n"
                             "canonical_admission_ref=#1096@admitted\n"
                             "gate_evidence_refs=actions:1234567")}
        if url.endswith("/actions/runs/1234567"):
            return {"id": 1234567, "head_sha": self.candidate,
                    "status": "completed", "conclusion": "success", "name": "verify-standard"}
        raise RuntimeError("unexpected API URL: " + url)

    def assess(self):
        return select(self.repo, self.project, self.candidates, self.fetch)

    def test_new_consumer_positive_exact_sha_recommendation(self):
        decision = self.assess()
        self.assertEqual(decision["decision"], "READ_ONLY_RECOMMENDATION")
        self.assertEqual(decision["proposed_revision"], self.candidate)
        self.assertFalse(decision["effective_pin_changed"])
        self.assertEqual(len(self.network_calls), 3)

    def test_mature_consumer_positive_with_extra_source(self):
        put(self.repo, "consumer/legacy-surface.json", "{}")
        # Existing material consumer file is not silently modified by this selector.
        self.assertEqual(self.assess()["decision"], "READ_ONLY_RECOMMENDATION")

    def test_no_opt_in_stays_pinned(self):
        self.project["preference"] = "PINNED/MANUAL"
        self.assertEqual(self.assess()["reason"], "PROJECT_NOT_OPTED_IN")
        self.assertFalse(self.network_calls)

    def test_active_task_or_frozen_candidate_cannot_rebind(self):
        for name in ("active_task", "frozen_candidate"):
            with self.subTest(name=name):
                self.project[name] = True
                self.assertEqual(self.assess()["decision"], "NO_SAFE_RECOMMENDATION")
                self.project[name] = False

    def test_missing_release_evidence_ref_never_self_certifies(self):
        del self.candidates[0]["qualification_comment"]
        self.assertEqual(self.assess()["reason"], "MISSING_QUALIFICATION_EVENT_REFERENCE")

    def test_qualified_boolean_is_not_canonical_proof(self):
        self.candidates[0]["qualified"] = True
        original = self.fetch
        self.fetch = lambda url: {**original(url), "body": "qualified=true"} if "/comments/" in url else original(url)
        self.assertEqual(self.assess()["reason"], "UNVERIFIED_CURRENT_RELEASE_QUALIFICATION")

    def test_release_gate_exit_must_be_real_success(self):
        old = self.fetch

        def failed_ci(url):
            value = old(url)
            if "/actions/runs/" in url:
                return {**value, "conclusion": "failure"}
            return value

        self.fetch = failed_ci
        self.assertEqual(self.assess()["reason"], "RELEASE_GATE_EVIDENCE_STALE_OR_NOT_EXECUTED")

    def test_source_stale_ci_head_cannot_prove_release(self):
        old = self.fetch

        def stale_ci(url):
            value = old(url)
            if "/actions/runs/" in url:
                return {**value, "head_sha": self.current}
            return value

        self.fetch = stale_ci
        self.assertEqual(self.assess()["reason"], "RELEASE_GATE_EVIDENCE_STALE_OR_NOT_EXECUTED")

    def test_nonqualified_github_release_refused(self):
        old = self.fetch
        self.fetch = lambda url: {**old(url), "prerelease": True} if "/releases/" in url else old(url)
        self.assertEqual(self.assess()["reason"], "NOT_PUBLISHED_STABLE_RELEASE")

    def test_mutable_branch_and_wrong_git_tag_refused(self):
        self.candidates[0]["release_tag"] = "main"
        self.assertEqual(self.assess()["reason"], "UNPINNED_RELEASE_TAG")

    def test_wrong_candidate_blob_same_semver_is_not_identity(self):
        self.candidates[0]["sha"] = self.current
        self.assertEqual(self.assess()["reason"], "NO_NEW_ELIGIBLE_RELEASE")
        self.candidates[0]["sha"] = self.candidate
        self.record["candidate"]["sha_or_digest"] = self.current
        self.assertEqual(self.assess()["reason"], "INVALID_SOURCE_COMPATIBILITY_RECORD")

    def test_source_schema_compatible_but_behavior_unknown(self):
        for dim in self.record["dimensions"]:
            if dim["name"] == "behavior":
                dim["outcome"] = "UNKNOWN"
        self.assertEqual(self.assess()["reason"], "MATERIAL_COMPATIBILITY_UNKNOWN_OR_UNPROVEN")

    def test_authority_change_without_review_evidence_refused(self):
        for dim in self.record["dimensions"]:
            if dim["name"] == "authority":
                dim["evidence_refs"] = []
        self.assertEqual(self.assess()["reason"], "MATERIAL_COMPATIBILITY_UNKNOWN_OR_UNPROVEN")

    def test_malformed_nested_compat_record_fails_closed(self):
        self.record["baseline"] = None
        result = self.assess()
        self.assertEqual(result["decision"], "NO_SAFE_RECOMMENDATION")
        self.assertEqual(result["reason"], "MISSING_OR_INVALID_SOURCE_EVIDENCE")

    def test_missing_material_claim_review_dim_refused(self):
        self.record["dimensions"] = [d for d in self.record["dimensions"] if d["name"] != "claim"]
        self.assertEqual(self.assess()["reason"], "MATERIAL_COMPATIBILITY_DIMENSIONS_MISSING")

    def test_incomparable_branch_rejected(self):
        git(self.repo, "checkout", "-q", "--detach", self.current)
        put(self.repo, "VERSION", "4.12.1\n")
        git(self.repo, "add", "VERSION")
        git(self.repo, "commit", "-qm", "sibling release line")
        sibling = git(self.repo, "rev-parse", "HEAD")
        git(self.repo, "tag", "v4.12.1", sibling)
        other_record = copy.deepcopy(self.record)
        other_record["candidate"]["sha_or_digest"] = sibling
        self.candidates.append({"sha": sibling, "release_tag": "v4.12.1",
                                "qualification_issue": self.issue, "qualification_comment": self.comment + 1,
                                "compatibility_record": other_record})
        original = self.fetch

        def sibling_proof(url):
            if "/releases/tags/v4.12.1" in url:
                return {"tag_name": "v4.12.1", "draft": False, "prerelease": False,
                        "html_url": "https://github.com/kaicreator-mm/ai-development-standard/releases/tag/v4.12.1"}
            if url.endswith("/issues/comments/987654322"):
                return {"id": 987654322,
                        "html_url": "https://github.com/kaicreator-mm/ai-development-standard/issues/1096#issuecomment-987654322",
                        "body": ("<!-- ai-dev:event:v2 -->\nevent=RELEASE_QUALIFICATION\n"
                                 f"candidate_sha={sibling}\nqualification=RELEASE_QUALIFIED\n"
                                 "actor_role=release-controller\n"
                                 "operator_kind=chatgpt-web\n"
                                 "operator_id=reviewed-release-context-02\n"
                                 "session_ref=release-session-02\n"
                                 "canonical_admission_ref=#1096@admitted\n"
                                 "gate_evidence_refs=actions:1234568")}
            if url.endswith("/actions/runs/1234568"):
                return {"id": 1234568, "head_sha": sibling,
                        "status": "completed", "conclusion": "success", "name": "verify-standard"}
            return original(url)

        self.fetch = sibling_proof
        self.assertEqual(self.assess()["reason"], "MULTIPLE_INCOMPARABLE_LATEST_RELEASES")

    def test_missing_local_sha_object_refused(self):
        self.candidates[0]["sha"] = "f" * 40
        self.assertEqual(self.assess()["reason"], "GIT_SOURCE_UNAVAILABLE")

    def test_sha_and_version_pin_shape(self):
        raw = ("repository=kaicreator-mm/ai-development-standard\n"
               "version=4.11.0\nrevision=" + self.current + "\n")
        self.assertEqual(parse_version(raw)["revision"], self.current)
        self.assertEqual(self.assess()["decision"], "READ_ONLY_RECOMMENDATION")

    def test_actual_git_and_input_objects_untouched(self):
        before = git(self.repo, "status", "--porcelain")
        self.assertEqual(self.assess()["decision"], "READ_ONLY_RECOMMENDATION")
        self.assertEqual(before, git(self.repo, "status", "--porcelain"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
