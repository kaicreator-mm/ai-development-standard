#!/usr/bin/env python3
"""ADS v4.12 S05: executable Git + mocked GitHub provenance boundary tests.

Positive mocks model an actual release, independent review, executed CI jobs
and an empty project task graph. They do NOT qualify a real published release.
"""
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
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          capture_output=True, text=True).stdout.strip()


def put(repo, path, data):
    p = repo / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(data, encoding="utf-8")


def commit(repo, message):
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", message)
    return git(repo, "rev-parse", "HEAD")


class SelectorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "ads"
        self.repo.mkdir()
        git(self.repo, "init", "-q")
        git(self.repo, "config", "user.name", "ADS Synthetic")
        git(self.repo, "config", "user.email", "test@example.invalid")
        put(self.repo, "standard-manifest.json", json.dumps(
            {"schema_version": 1, "sections": {"normative_standards": [
                "standards/PROJECT_ADOPTION.md",
                "standards/INTERFACE_COMPATIBILITY_GOVERNANCE_STANDARD.md"]}}))
        put(self.repo, "VERSION", "4.11.0\n")
        self.current = commit(self.repo, "current")
        put(self.repo, "VERSION", "4.12.0\n")
        put(self.repo, "standards/PROJECT_ADOPTION.md", "new prospective policy")
        self.candidate = commit(self.repo, "candidate")
        git(self.repo, "tag", "v4.12.0", self.candidate)
        self.issue, self.comment, self.review = 1096, 987654321, 987654333
        self.consumer = Path(self.tmp.name) / "consumer"
        self.consumer.mkdir()
        git(self.consumer, "init", "-q")
        git(self.consumer, "config", "user.name", "Synthetic Project")
        git(self.consumer, "config", "user.email", "test@example.invalid")
        git(self.consumer, "branch", "-M", "main")
        git(self.consumer, "remote", "add", "origin", "https://github.com/synthetic/example.git")
        put(self.consumer, "README.md", "synthetic consumer")
        consumer_parent = commit(self.consumer, "before adoption checkpoint")
        self.project = {"preference": "TRACK_LATEST_COMPATIBLE_STABLE",
                        "project_repository": "synthetic/example",
                        "project_root": self.consumer,
                        "consumer_window": "supported-synthetic-A0-A4",
                        "current_revision": self.current,
                        "current_version": "4.11.0"}
        self.status = {"schema_version": 1, "project_repository": "synthetic/example",
                       "checked_parent_sha": consumer_parent,
                       "effective_ads_revision": self.current,
                       "active_claim": "NONE", "frozen_candidate": "NONE"}
        put(self.consumer, ".dev-standard/ADOPTION_STATUS.json", json.dumps(self.status))
        self.consumer_head = commit(self.consumer, "current scoped adoption status")
        self.record = {
            "schema_version": 1, "record_id": "synthetic", "contract": {
                "kind": "ADS", "identity": "source-consumer"},
            "baseline": {"sha_or_digest": self.current},
            "candidate": {"sha_or_digest": self.candidate},
            "change_operations": ["MODIFIED"],
            "producer_refs": ["kaicreator-mm/ai-development-standard"], "consumer_refs": ["synthetic/example"],
            "compatibility_window_ref": self.project["consumer_window"],
            "dimensions": [
                {"name": d, "outcome": "COMPATIBLE",
                 "evidence_refs": [f"actions:1234567:{200001 + i}"]}
                for i, d in enumerate(sorted(REQUIRED_DIMENSIONS))
            ]}
        self.path = "docs/compatibility/consumer.json"
        self.candidates = [{
            "sha": self.candidate, "release_tag": "v4.12.0",
            "qualification_issue": self.issue, "qualification_comment": self.comment,
            "compatibility_record_path": self.path}]
        self.save_proof()
        self.calls = []
        self.live_issues = []
        self.live_pulls = []
        self.release_prerelease = False
        self.release_target_sha = self.candidate
        self.tag_target_sha = self.candidate
        self.ci_conclusion = "success"
        self.ci_subject = self.candidate

    def tearDown(self):
        self.tmp.cleanup()

    def save_proof(self):
        # Explicit source successor avoids self-referential candidate SHA.
        put(self.repo, self.path, json.dumps(self.record))
        self.candidates[0]["compatibility_source_sha"] = commit(self.repo, "evidence")

    def fetch(self, url):
        self.calls.append(url)
        if url.endswith("/git/ref/heads/main"):
            return {"ref": "refs/heads/main", "object": {"type": "commit", "sha": self.consumer_head}}
        if url.endswith("/issues?state=open&per_page=100"):
            return self.live_issues
        if url.endswith("/pulls?state=open&per_page=100"):
            return self.live_pulls
        if "/git/ref/tags/" in url:
            return {"ref": "refs/tags/v4.12.0",
                    "object": {"sha": self.tag_target_sha, "type": "commit"}}
        if "/releases/tags/" in url:
            return {"tag_name": "v4.12.0", "draft": False,
                    "prerelease": self.release_prerelease,
                    "target_commitish": self.release_target_sha,
                    "published_at": "2026-10-16T00:00:00Z",
                    "html_url": "https://github.com/synthetic/release"}
        if url.endswith("/issues/1096"):
            return {"number": 1096, "state": "closed", "title": "ADS v4.12.0"}
        if url.endswith("/issues/comments/987654321"):
            return {"id": self.comment,
                    "html_url": f"https://github.com/kaicreator-mm/ai-development-standard/issues/1096#issuecomment-{self.comment}",
                    "body": ("<!-- ai-dev:event:v2 -->\nevent=RELEASE_QUALIFICATION\n"
                             "qualification=RELEASE_QUALIFIED\n"
                             f"candidate_sha={self.candidate}\n"
                             f"release_integrated_sha={self.candidate}\n"
                             "release_tag=v4.12.0\n"
                             "required_gate_results=PASS\n"
                             "actor_role=release-controller\n"
                             "operator_id=release-agent\noperator_kind=chatgpt-web\n"
                             "session_ref=release-1\ncanonical_admission_ref=#1096@987654344\n"
                             "review_comment_id=987654333\n"
                             "gate_decision_refs=SOURCE_CONSISTENCY:#1096@987654355;SELF_DOGFOOD:#1096@987654356\n"
                             "gate_evidence_refs=actions:1234567")}
        if url.endswith("/issues/comments/987654344"):
            return {"id": 987654344,
                    "html_url": "https://github.com/kaicreator-mm/ai-development-standard/issues/1096#issuecomment-987654344",
                    "body": ("<!-- ai-dev:event:v2 -->\nevent=RELEASE_CANDIDATE_ADMISSION\n"
                             f"candidate_sha={self.candidate}\nadmission=ACCEPTED\n"
                             "required_gate_ids=SOURCE_CONSISTENCY;SELF_DOGFOOD\n")}
        for gid, gate in ((987654355, "SOURCE_CONSISTENCY"),
                          (987654356, "SELF_DOGFOOD")):
            if url.endswith("/issues/comments/" + str(gid)):
                jid = 300001 if gate == "SOURCE_CONSISTENCY" else 300002
                return {"id": gid,
                        "html_url": "https://github.com/kaicreator-mm/ai-development-standard/issues/1096#issuecomment-" + str(gid),
                        "body": ("<!-- ai-dev:event:v2 -->\nevent=RELEASE_GATE_DECISION\n"
                                 f"gate_id={gate}\ncandidate_sha={self.candidate}\n"
                                 "decision=PASS\n" + f"proof_ref=actions:1234567:{jid}\n")}
        if url.endswith("/issues/comments/987654333"):
            return {"id": self.review,
                    "html_url": "https://github.com/kaicreator-mm/ai-development-standard/issues/1096#issuecomment-987654333",
                    "body": ("<!-- ai-dev:event:v2 -->\nevent=INDEPENDENT_RELEASE_REVIEW\n"
                             "review_subject=S06_RELEASE_QUALIFICATION\nactor_role=reviewer\n"
                             "operator_id=independent-reviewer\nsession_ref=review-2\n"
                             "review_verdict=PASS\n"
                             f"reviewed_sha={self.candidate}\n")}
        if url.endswith("/actions/runs/1234567"):
            return {"id": 1234567, "head_sha": self.ci_subject,
                    "status": "completed", "conclusion": self.ci_conclusion}
        if "/actions/jobs/" in url:
            job_id = int(url.rsplit("/", 1)[1])
            if job_id in (300001, 300002):
                gate = "SOURCE_CONSISTENCY" if job_id == 300001 else "SELF_DOGFOOD"
                return {"id": job_id, "run_id": 1234567, "status": "completed",
                        "conclusion": "success", "name": "ads-release:" + gate,
                        "steps": [{"name": "release-proof:" + gate + ":" + self.candidate,
                                   "conclusion": "success"}]}
            i = job_id - 200001
            names = sorted(REQUIRED_DIMENSIONS)
            if i not in range(len(names)):
                raise AssertionError("unknown job")
            dimension = names[i]
            return {"id": job_id, "run_id": 1234567, "status": "completed",
                    "conclusion": "success",
                    "name": f"ads-compat:{self.current[:12]}:synthetic__example:{dimension}",
                    "steps": [{"name": f"probe:{self.current[:12]}:synthetic__example:{dimension}:{self.project['consumer_window']}",
                               "conclusion": "success"}]}
        raise AssertionError("Unexpected mocked endpoint: " + url)

    def assess(self):
        return select(self.repo, self.project, self.candidates, self.fetch)

    def rejected(self, reason):
        result = self.assess()
        self.assertEqual(result["decision"], "NO_SAFE_RECOMMENDATION")
        self.assertEqual(result["reason"], reason)
        self.assertFalse(result["effective_pin_changed"])

    def test_source_verified_new_project_positive(self):
        out = self.assess()
        self.assertEqual(out["decision"], "READ_ONLY_RECOMMENDATION")
        self.assertEqual(out["proposed_revision"], self.candidate)
        self.assertEqual(len(out["compatibility_evidence_refs"]), 10)
        self.assertFalse(out["effective_pin_changed"])

    def test_mature_project_extra_local_files_unchanged(self):
        put(self.repo, "consumer/legacy.txt", "old")
        old = git(self.repo, "status", "--porcelain")
        self.assertEqual(self.assess()["decision"], "READ_ONLY_RECOMMENDATION")
        self.assertEqual(git(self.repo, "status", "--porcelain"), old)

    def test_no_opt_in(self):
        self.project["preference"] = "PINNED/MANUAL"
        self.rejected("PROJECT_NOT_OPTED_IN")
        self.assertFalse(self.calls)

    def test_missing_checkpoint_state_fails_closed(self):
        self.status["active_claim"] = "CLAIM_PENDING"
        self.status["checked_parent_sha"] = self.consumer_head
        put(self.consumer, ".dev-standard/ADOPTION_STATUS.json", json.dumps(self.status))
        self.consumer_head = commit(self.consumer, "new adoption snapshot")
        self.rejected("ACTIVE_FROZEN_OR_UNVERIFIED_CHECKPOINT")

    def test_discovery_false_false_cannot_override_source_frozen(self):
        self.project["active_task"] = False
        self.project["frozen_candidate"] = False
        self.status["frozen_candidate"] = "frozen-candidate-1"
        self.status["checked_parent_sha"] = self.consumer_head
        put(self.consumer, ".dev-standard/ADOPTION_STATUS.json", json.dumps(self.status))
        self.consumer_head = commit(self.consumer, "current known frozen snapshot")
        self.rejected("ACTIVE_FROZEN_OR_UNVERIFIED_CHECKPOINT")

    def test_discovery_false_does_not_override_live_task(self):
        self.live_issues = [{"number": 4, "labels": [{"name": "type:task"}]}]
        self.rejected("ACTIVE_OR_UNCLASSIFIED_WORK_ITEM")

    def test_discovery_false_does_not_override_live_pr(self):
        self.live_pulls = [{"number": 9}]
        self.rejected("ACTIVE_SUBJECT_CANNOT_REBIND")

    def test_unclassified_task_and_pagination_unknown(self):
        self.live_issues = [{"number": 3, "labels": []}]
        self.rejected("ACTIVE_OR_UNCLASSIFIED_WORK_ITEM")
        self.live_issues = [{}] * 100
        self.rejected("UNKNOWN_PROJECT_LIVE_STATE_OR_PAGINATION")

    def test_arbitrary_non_task_label_open_issue_is_not_trusted(self):
        self.live_issues = [{"number": 55, "labels": [{"name": "triage:active"}]}]
        self.rejected("ACTIVE_OR_UNCLASSIFIED_WORK_ITEM")

    def test_stale_local_checkout_rejects_project_inactive_claim(self):
        self.consumer_head = self.current
        self.rejected("PROJECT_REMOTE_CHECKPOINT_STALE")

    def test_dirty_consumer_worktree_unknown(self):
        put(self.consumer, "scratch.txt", "pending")
        self.rejected("PROJECT_WORKTREE_NOT_CLEAN")

    def test_missing_live_project_repo(self):
        self.project["project_repository"] = None
        self.rejected("MISSING_VERIFIABLE_PROJECT_REPOSITORY")

    def test_missing_qualification_ref(self):
        self.candidates[0].pop("qualification_comment")
        self.rejected("MISSING_QUALIFICATION_EVENT_REFERENCE")

    def test_fake_inline_record_not_accepted_as_evidence(self):
        self.candidates[0]["compatibility_record"] = copy.deepcopy(self.record)
        self.candidates[0].pop("compatibility_source_sha")
        self.rejected("INVALID_EXACT_COMMIT")

    def test_wrong_compatibility_record_candidate_identity(self):
        self.record["candidate"]["sha_or_digest"] = self.current
        self.save_proof()
        self.rejected("INVALID_SOURCE_COMPATIBILITY_RECORD")

    def test_consumer_a_proof_does_not_qualify_consumer_b(self):
        # Both projects may declare the same support window.
        self.record["consumer_refs"] = ["synthetic/other-consumer"]
        self.save_proof()
        self.rejected("CONSUMER_IDENTITY_NOT_TESTED")

    def test_producer_must_be_actual_ads_source(self):
        self.record["producer_refs"] = ["some-producer"]
        self.save_proof()
        self.rejected("CONSUMER_IDENTITY_NOT_TESTED")

    def test_unknown_behavior_forces_no_recommendation(self):
        self.record["dimensions"][0]["outcome"] = "UNKNOWN"
        self.save_proof()
        self.rejected("MATERIAL_COMPATIBILITY_UNKNOWN_OR_UNPROVEN")

    def test_pseudo_proof_refs_rejected(self):
        self.record["dimensions"][0]["evidence_refs"] = ["test:fake"]
        self.save_proof()
        self.rejected("INDEPENDENT_COMPATIBILITY_PROOF_MISSING")

    def test_missing_material_claim_dimension(self):
        self.record["dimensions"] = [d for d in self.record["dimensions"] if d["name"] != "claim"]
        self.save_proof()
        self.rejected("MATERIAL_COMPATIBILITY_DIMENSIONS_MISSING")

    def test_unsupported_consumer_window(self):
        self.project["consumer_window"] = "unsupported-new-window"
        self.rejected("UNSUPPORTED_OR_UNVERIFIED_CONSUMER_WINDOW")

    def test_release_prerelease_or_wrong_target_sha(self):
        self.release_prerelease = True
        self.rejected("PUBLISHED_RELEASE_IDENTITY_UNVERIFIED")
        self.release_prerelease = False
        self.release_target_sha = self.current
        self.rejected("PUBLISHED_RELEASE_IDENTITY_UNVERIFIED")

    def test_remote_tag_must_equal_candidate(self):
        self.tag_target_sha = self.current
        self.rejected("REMOTE_RELEASE_TAG_IDENTITY_UNVERIFIED")

    def test_release_canonical_admission_must_be_accepted(self):
        old = self.fetch

        def fake_admission(url):
            result = old(url)
            if url.endswith("/issues/comments/987654344"):
                return {**result, "body": result["body"].replace("admission=ACCEPTED", "admission=PENDING")}
            return result
        self.fetch = fake_admission
        self.rejected("CANONICAL_RELEASE_ADMISSION_NOT_ACCEPTED")

    def test_required_s06_gate_cannot_be_not_run_with_green_ci(self):
        old = self.fetch

        def fake_gate(url):
            result = old(url)
            if url.endswith("/issues/comments/987654356"):
                return {**result, "body": result["body"].replace("decision=PASS", "decision=NOT_RUN")}
            return result

        self.fetch = fake_gate
        self.rejected("REQUIRED_RELEASE_GATE_NOT_PASSED")

    def test_required_s06_gate_job_not_equivalent_to_ordinary_ci(self):
        old = self.fetch

        def ordinary_ci_only(url):
            result = old(url)
            if url.endswith("/actions/jobs/300002"):
                return {**result, "name": "verify-standard"}
            return result

        self.fetch = ordinary_ci_only
        self.rejected("REQUIRED_RELEASE_GATE_PROOF_NOT_EXECUTED")

    def test_review_from_different_issue_not_release_subject(self):
        old = self.fetch

        def unowned_review(url):
            result = old(url)
            if url.endswith("/issues/comments/987654333"):
                return {**result,
                        "html_url": "https://github.com/kaicreator-mm/ai-development-standard/issues/999#issuecomment-987654333"}
            return result

        self.fetch = unowned_review
        self.rejected("MISSING_INDEPENDENT_RELEASE_REVIEW")

    def test_release_ci_real_exit_required(self):
        self.ci_conclusion = "failure"
        self.rejected("EXECUTED_GATE_NOT_PROVEN")

    def test_release_ci_subject_must_equal_exact_candidate(self):
        self.ci_subject = self.current
        self.rejected("EXECUTED_GATE_NOT_PROVEN")

    def test_failed_dimensional_job_proof_refused(self):
        original = self.fetch

        def broken_job(url):
            result = original(url)
            if url.endswith("/actions/jobs/200001"):
                return {**result, "conclusion": "failure"}
            return result
        self.fetch = broken_job
        self.rejected("COMPATIBILITY_TEST_NOT_EXECUTED_ON_EXACT_SUBJECT")

    def test_unqualified_word_not_release_qualification(self):
        old = self.fetch

        def fake_event(url):
            result = old(url)
            if url.endswith("/issues/comments/987654321"):
                return {**result, "body": "<!-- ai-dev:event:v2 -->\nqualified=true"}
            return result
        self.fetch = fake_event
        self.rejected("UNVERIFIED_CURRENT_RELEASE_QUALIFICATION")

    def test_reviewer_must_be_independent_and_exact_source(self):
        old = self.fetch

        def fake_review(url):
            result = old(url)
            if url.endswith("/issues/comments/987654333"):
                return {**result, "body": result["body"].replace("independent-reviewer", "release-agent")}
            return result
        self.fetch = fake_review
        self.rejected("INDEPENDENT_RELEASE_REVIEW_NOT_PROVEN")

    def test_immutable_version_pin_shape(self):
        pin = "repository=kaicreator-mm/ai-development-standard\nversion=4.11.0\nrevision=" + self.current
        self.assertEqual(parse_version(pin)["revision"], self.current)
        self.assertEqual(self.assess()["decision"], "READ_ONLY_RECOMMENDATION")

    def test_no_repo_mutations_after_selection(self):
        old = git(self.repo, "status", "--porcelain")
        self.assertEqual(self.assess()["decision"], "READ_ONLY_RECOMMENDATION")
        self.assertEqual(git(self.repo, "status", "--porcelain"), old)


if __name__ == "__main__":
    unittest.main(verbosity=2)
