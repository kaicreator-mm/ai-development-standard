"""Focused owner source-consumer negatives: NEVER a real Release/Owner gate."""
from __future__ import annotations

import unittest
import v411_release_owner_readback as r

SHA = "a" * 40
API = f"https://api.github.com/repos/{r.REPOSITORY}/issues/comments/"


def comment(job, number, **changes):
    fields = {
        "schema": "ai-dev/event-v2", "event": r.OWNER_EVENT,
        "actor_role": "validator", "operator_kind": "human",
        "operator_id": "independent-validator", "repository": r.REPOSITORY,
        "sha": SHA, "gate": job, "status": "PASS",
        "owner_authority_ref": "frozen/release-owner-ref",
        "currentness": "CURRENT", "environment": "local",
        "command": "test", "exit_code": "0", "evidence": "ref:validated",
    }
    fields.update(changes)
    body = "<!-- ai-dev:event:v2 -->\n" + chr(96) * 3 + "yaml\n"
    body += "\n".join(f"{k}: {v}" for k, v in fields.items()) + "\n" + chr(96) * 3 + "\n"
    return {
        "id": number, "url": API + str(number),
        "user": {"login": "release-owner"}, "body": body,
    }


def inspect(jobs=None, observed=None, proofs=None, owner="release-owner", reader=None):
    return r.inspect_current_owner_proofs(
        subject=SHA,
        declared_jobs=set(r.JOBS) if jobs is None else jobs,
        observed_jobs=set(r.JOBS) if observed is None else observed,
        proof_urls={j: API + str(100 + i) for i, j in enumerate(r.JOBS)}
        if proofs is None else proofs,
        owner_login=owner,
        owner_authority_ref="frozen/release-owner-ref",
        reader=reader if reader is not None
        else lambda n: comment(r.JOBS[n - 100], n),
    )


class FailClosedReadback(unittest.TestCase):
    def test_source_witness_never_mints_release_pass(self):
        result = inspect()
        self.assertEqual(result.status, "SOURCE_ONLY_OWNER_REVIEW_REQUIRED")
        self.assertEqual(result.release_gate_state, "BLOCKED")
        self.assertEqual(len(result.proof_ids), 4)

    def test_each_missing_job_fails_closed(self):
        for missing in r.JOBS:
            urls = {job: API + str(i + 100) for i, job in enumerate(r.JOBS)
                    if job != missing}
            with self.subTest(job=missing):
                self.assertEqual(inspect(proofs=urls).reason,
                                 f"PROOF_MISSING_OR_BAD_REF_{missing}")

    def test_underdeclared_observed_j12_is_not_waived(self):
        x = inspect(jobs={"J09", "J10", "J11"}, observed=set(r.JOBS))
        self.assertEqual(x.reason, "OBSERVED_JOB_MISSING_FROM_DECLARATION")

    def test_uninspected_materiality_blocks(self):
        x = inspect(observed=None)
        self.assertEqual(x.release_gate_state, "BLOCKED")
        y = r.inspect_current_owner_proofs(
            subject=SHA, declared_jobs=set(r.JOBS), observed_jobs=None,
            proof_urls={}, owner_login="release-owner",
            owner_authority_ref="frozen/release-owner-ref",
        )
        self.assertEqual(y.reason, "OBSERVED_MATERIALITY_UNKNOWN")

    def test_unbound_release_authority_blocks(self):
        self.assertEqual(inspect(owner=None).reason, "OWNER_AUTHORITY_UNVERIFIED")

    def test_stale_or_wrong_subject_verdict(self):
        for change in ({"sha": "b"*40},
                       {"currentness": "STALE"}, {"status": "FAIL"}):
            with self.subTest(change=change):
                def reader(n):
                    return comment(r.JOBS[n-100], n, **change) if n == 100 else comment(r.JOBS[n-100], n)
                self.assertEqual(inspect(reader=reader).status, "BLOCKED")

    def test_wrong_author_or_rebound_source_ref(self):
        for mode in ("user", "id", "url"):
            with self.subTest(mode=mode):
                def reader(n):
                    item = comment(r.JOBS[n-100], n)
                    if n == 100:
                        if mode == "user":
                            item["user"] = {"login": "untrusted-agent"}
                        elif mode == "id":
                            item["id"] = 101
                        else:
                            item["url"] = API + "999"
                    return item
                self.assertEqual(inspect(reader=reader).status, "BLOCKED")

    def test_duplicate_event_fails_closed(self):
        def reader(n):
            item = comment(r.JOBS[n-100], n)
            if n == 100:
                item["body"] += chr(96)*3 + "yaml\nevent: VALIDATION_RESULT\n" + chr(96)*3
            return item
        self.assertEqual(inspect(reader=reader).reason,
                         "PROOF_UNADMITTED_EVENT_J09")

    def test_unavailable_readback_fails_closed(self):
        def reader(_):
            raise OSError("unavailable")
        self.assertEqual(inspect(reader=reader).reason,
                         "PROOF_READBACK_UNAVAILABLE_J09")


if __name__ == "__main__":
    unittest.main()
