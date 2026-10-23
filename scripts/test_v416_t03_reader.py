#!/usr/bin/env python3
"""ADS v4.16 T03 source-only mixed GitHub reader conformance (no live API/ACL)."""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from verify_github_structured_interaction import (
    ROOT, ContractError, MARKER, validate_record, record_disposition,
    data_digest, report_identity, compare_v5_correction_source,
    compare_v5_summary_revision, inspect_supplied_issue_pages, verify_markdown,
)
from test_github_structured_interaction import WORK, envelope

FIX = ROOT / "tests/fixtures/v415"
SHA = "d" * 40
CLEAR = {"classification": "PUBLISHABLE", "clearance_ref": "fixture:source-only",
         "projection_digest": "c" * 64}


def v5(name="summary"):
    """Upgrade *test data only*, not a production v4-to-v5 coercion path."""
    r = json.loads((FIX / (name + ".json")).read_text(encoding="utf8"))
    r["schema"] = "ads/github/v5"
    d = r["data"]
    d["publication"] = copy.deepcopy(CLEAR)
    s = d["subject"]
    s.update(ads_profile="ads/github/v5:report",
             publisher_source_sha=d.get("publisher_source_sha", SHA),
             source_status="PINNED", source_currentness="CURRENT",
             source_reason=None, collector_observation_refs=[])
    if name == "summary":
        d["cost"].update(accounting_ref=None, economic_scope_ref=None,
                         billing_window_ref=None, cost_category=None)
        d["verifier"]["status"] = "PASS"
        d["metrics"][0].update(metric_id="token:input",
            observation_id="obs:1", logical_call_ref="logical:1",
            physical_attempt_ref="physical:1", adapter_id="adapter:1",
            provider_run_ref=None, measurement_kind="UNKNOWN",
            window_id="window:1", source_revision=1)
    elif name == "correction":
        d["notice_publisher_source_sha"] = SHA
        d["target"].update(repository=s["repository"], comment_id=123,
            ads_profile="ads/github/v5:report", attempt_ref=s["attempt_ref"],
            target_source_status="PINNED", target_source_sha=s["source_sha"])
    return r


def source_comment(record, number=123, edited=False):
    return {"id": number, "url": record["data"]["subject"]["issue_ref"] + "#issuecomment-" + str(number),
            "edited": edited,
            "body": MARKER + "\n\x60\x60\x60yaml\n" + json.dumps(record, ensure_ascii=False) + "\n\x60\x60\x60\n"}


class T03MixedReader(unittest.TestCase):
    def test_three_v5_shapes_and_old_windows(self):
        for name in ("summary", "feedback", "correction"):
            record = v5(name)
            with self.subTest(kind=name):
                self.assertEqual(validate_record(record), "SHAPE_VALID_ONLY")
                self.assertEqual(record_disposition(record, "v4.16"), "V5_SHAPE_ONLY")
                self.assertEqual(record_disposition(record, "v4.16", writing=True), "V5_SHAPE_ONLY")
                with self.assertRaisesRegex(ContractError, "UNSUPPORTED_SCHEMA"):
                    record_disposition(record, "v4.15")
                with self.assertRaisesRegex(ContractError, "UNSUPPORTED_SCHEMA"):
                    record_disposition(record, "v4.14")
        historical = json.loads((FIX / "summary.json").read_text(encoding="utf8"))
        self.assertEqual(record_disposition(historical, "v4.15"), "CURRENT_OBSERVATION")
        self.assertEqual(record_disposition(historical, "v4.16"), "CURRENT_OBSERVATION")
        self.assertEqual(record_disposition(envelope("work_item", WORK), "v4.16"),
                         "CURRENT_EXECUTABLE_SHAPE_ONLY")

    def test_collector_only_original_source_null_is_observational(self):
        r = v5()
        s = r["data"]["subject"]
        s.update(source_status="UNPINNED", source_sha=None,
                 source_currentness="UNKNOWN", source_reason="original source inaccessible",
                 collector_observation_refs=["collector:observation:1"])
        s["currentness"]["state"] = "UNKNOWN"
        verifier = r["data"]["verifier"]
        verifier.update(status="UNKNOWN", subject_sha=None, checked=[], failed=[],
                        epistemic="UNKNOWN")
        verifier["currentness"]["state"] = "UNKNOWN"
        self.assertEqual(validate_record(r), "SHAPE_VALID_ONLY")
        self.assertEqual(record_disposition(r, "v4.16"), "V5_SHAPE_ONLY")
        r["data"]["cost"].update(basis="BILLED", value=3.0)
        with self.assertRaises(ContractError):
            validate_record(r)

    def test_collector_source_association_is_revision_not_canonical_attempt(self):
        previous = v5()
        ps = previous["data"]["subject"]
        ps.update(source_status="UNPINNED", source_sha=None,
                  source_reason="original material not available", source_currentness="UNKNOWN",
                  collector_observation_refs=["collector:trace:source"])
        ps["currentness"]["state"] = "UNKNOWN"
        pver = previous["data"]["verifier"]
        pver.update(subject_sha=None, status="UNKNOWN", epistemic="UNKNOWN",
                    checked=[], failed=[])
        pver["currentness"]["state"] = "UNKNOWN"
        validate_record(previous)
        successor = copy.deepcopy(previous)
        d = successor["data"]
        d["revision"] = 2
        ref = ps["issue_ref"] + "#issuecomment-123"
        d["supersedes"] = {"revision": 1, "comment_ref": ref,
                           "data_digest": data_digest(previous)}
        d["manifest_ref"] = "object:private/task42/attempt1/r2/manifest.json"
        d["manifest_sha256"] = "f" * 64
        d["subject"].update(source_status="PINNED", source_sha="a" * 40,
                             source_reason=None, source_currentness="UNKNOWN")
        d["source_association"] = {
            "original_material_sha256": "e" * 64,
            "source_sha": "a" * 40,
            "artifact_witness_refs": ["github:original-material-ref"],
            "association_currentness": {"state": "UNKNOWN",
                "source_refs": ["github:source-link-proposal"], "limits": ["Not authenticated"]}}
        self.assertEqual(validate_record(successor), "SHAPE_VALID_ONLY")
        self.assertEqual(compare_v5_summary_revision(previous, successor,
            predecessor_comment_ref=ref, previous_unedited=True), "SOURCE_CHAIN_SHAPE_ONLY")
        successor["data"]["subject"]["attempt_binding"] = "CANONICAL_DISPATCH"
        with self.assertRaises(ContractError):
            validate_record(successor)

    def test_summary_source_and_feedback_publisher_identity_rejected(self):
        r = v5()
        r["data"]["verifier"]["subject_sha"] = "f" * 40
        with self.assertRaises(ContractError):
            validate_record(r)
        r = v5("feedback")
        r["data"]["publisher_source_sha"] = "f" * 40
        with self.assertRaises(ContractError):
            validate_record(r)

    def test_correction_native_original_required_never_auto_applied(self):
        original, correction = v5(), v5("correction")
        target = correction["data"]["target"]
        target["data_digest"] = data_digest(original)
        self.assertEqual(validate_record(correction), "SHAPE_VALID_ONLY")
        self.assertEqual(compare_v5_correction_source(correction), "UNVERIFIED")
        self.assertEqual(compare_v5_correction_source(correction, original), "UNVERIFIED")
        url = target["comment_ref"]
        self.assertEqual(compare_v5_correction_source(correction, original,
            target_comment_ref=url, original_unedited=True,
            complete_collection=True), "SOURCE_MATCH_ONLY")
        bad = copy.deepcopy(correction)
        bad["data"]["target"]["report_id"] = "different-original"
        self.assertEqual(compare_v5_correction_source(bad, original,
            target_comment_ref=url, original_unedited=True, complete_collection=True),
            "DISPUTED")
        bad = copy.deepcopy(correction)
        bad["data"]["target"]["publisher_namespace"] = "intruder:other"
        with self.assertRaises(ContractError):
            validate_record(bad)

    def test_revision_digest_and_missing_native_proof(self):
        original, newer = v5(), v5()
        newer["data"]["revision"] = 2
        newer["data"]["manifest_ref"] = "object:private/task42/attempt1/r2/manifest.json"
        newer["data"]["manifest_sha256"] = "f" * 64
        ref = original["data"]["subject"]["issue_ref"] + "#issuecomment-123"
        newer["data"]["supersedes"] = {"revision": 1, "data_digest": data_digest(original),
                                        "comment_ref": ref}
        self.assertEqual(compare_v5_summary_revision(original, newer), "UNVERIFIED")
        self.assertEqual(compare_v5_summary_revision(original, newer,
            predecessor_comment_ref=ref, previous_unedited=True), "SOURCE_CHAIN_SHAPE_ONLY")
        newer["data"]["supersedes"]["data_digest"] = "0" * 64
        with self.assertRaises(ContractError):
            compare_v5_summary_revision(original, newer,
                predecessor_comment_ref=ref, previous_unedited=True)

    def test_mixed_issue_and_complete_page_requirement(self):
        a, b = v5(), json.loads((FIX / "summary.json").read_text(encoding="utf8"))
        c = envelope("work_item", WORK)
        items = [source_comment(a, 123), source_comment(b, 124),
                 {"id": 125, "body": MARKER + "\n\x60\x60\x60yaml\n" + json.dumps(c) + "\n\x60\x60\x60\n",
                  "edited": False}]
        pages = [{"cursor": None, "status": 200, "comments": items[:1], "next": "page:2"},
                 {"cursor": "page:2", "status": 200, "comments": items[1:], "next": None}]
        observed = inspect_supplied_issue_pages(pages)
        self.assertTrue(observed["complete"])
        self.assertEqual(observed["statuses"], ["OBSERVED_SHAPE_ONLY",
            "OBSERVED_SHAPE_ONLY", "CURRENT_EXECUTABLE_SHAPE_ONLY"])
        self.assertFalse(inspect_supplied_issue_pages(pages[:1])["complete"])
        self.assertFalse(inspect_supplied_issue_pages(pages + [pages[-1]])["complete"])
        edited = source_comment(a, 123, edited=True)
        self.assertEqual(inspect_supplied_issue_pages([{"cursor": None,
            "status": 200, "comments": [edited], "next": None}])["statuses"],
            ["UNVERIFIED_EDIT"])

    def test_duplicate_conflict_all_orders_and_source_digest(self):
        a = v5()
        b = copy.deepcopy(a)
        b["data"]["limits"].append("material difference")
        self.assertNotEqual(data_digest(a), data_digest(b))
        self.assertEqual(report_identity(a), report_identity(b))
        for items in ([source_comment(a), source_comment(b, 124)],
                      [source_comment(b, 124), source_comment(a)]):
            statuses = inspect_supplied_issue_pages([{"cursor": None, "status": 200,
                "comments": items, "next": None}])["statuses"]
            self.assertEqual(statuses, ["CONFLICT", "CONFLICT"])

    def test_wrong_kind_unknown_fields_and_unsafe_markdown(self):
        for kind in ("event", "intent", "work_item"):
            r = v5()
            r["kind"] = kind
            with self.assertRaises(ContractError):
                validate_record(r)
        r = v5()
        r["data"]["unapproved_field"] = 1
        with self.assertRaises(ContractError):
            validate_record(r)
        txt = source_comment(v5())["body"]
        self.assertEqual(verify_markdown(txt, "report", effective_pin="v4.16"),
                         "SHAPE_VALID_ONLY")
        with self.assertRaisesRegex(ContractError, "UNSUPPORTED_SCHEMA"):
            verify_markdown(txt, "report", effective_pin="v4.15")
        with self.assertRaises(ContractError):
            verify_markdown(txt.replace('"schema":', '"schema": "ads/github/v5", "schema":', 1),
                effective_pin="v4.16")


if __name__ == "__main__":
    unittest.main(verbosity=2)
