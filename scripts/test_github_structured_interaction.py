#!/usr/bin/env python3
"""Latest-only GitHub v2 document contract: functional and adversarial tests."""
from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path
from test_protocol_schemas import load_schema, validate_subset
from verify_github_structured_interaction import ContractError, verify_markdown

SHA = "a" * 40
WORK = {"profile": "type:task", "contract": {
    "task_id": "T01", "goal": "Bounded task", "integration_target": "version/v0.1",
    "baseline_sha": SHA, "review_policy": "recommended", "required_gates": ["unit"],
    "acceptance": ["Observed evidence for the intended behavior"]
}}
INTENT = {"id": "operation:123", "operation": "ISSUE_METADATA_CHANGE",
          "target": {"repository": "example-org/example-repo", "issue": "#42"},
          "actor": {"role": "builder", "operator_kind": "codex", "operator_id": "codex:a"},
          "expected_ref": "github:example-org/example-repo#42@revision-2",
          "change": {"field": "state", "before": "state:ready", "after": "state:claimed"}}
EVENT = {"schema": "ai-dev/event-v2", "event": "ROLE_CLAIMED", "actor_role": "builder",
         "operator_kind": "codex", "operator_id": "codex:a", "task": "#42"}
REPORT = {"report_id": "example:report:1", "report_kind": "EXECUTION_SUMMARY",
          "revision": 1, "attempt_ref": "example:attempt:1",
          "manifest_ref": "object:private/example/tasks/42/attempt-1/r1/manifest.json",
          "manifest_sha256": "b" * 64, "coverage": "PARTIAL"}


def yaml_lines(obj, depth=0):
    lines = []
    for key, value in obj.items():
        pad = " " * depth
        if isinstance(value, dict):
            lines.append(pad + key + ":")
            lines.extend(yaml_lines(value, depth + 2))
        elif isinstance(value, list):
            lines.append(pad + key + ":")
            for item in value:
                lines.append(pad + "  - " + json.dumps(item))
        else:
            lines.append(pad + key + ": " + json.dumps(value))
    return lines


def render(kind, data):
    env = {"schema": "ads/github/v2", "kind": kind, "data": data}
    return ("<!-- ads:github:v2 -->\n```yaml\n" + "\n".join(yaml_lines(env))
            + "\n```\n\n## Human notes\nSource-linked context only.\n")


def fail(doc, text=None, **kwargs):
    try:
        verify_markdown(doc, **kwargs)
    except ContractError as exc:
        if text and text not in str(exc):
            raise AssertionError(f"expected {text!r}, got {exc!s}") from exc
        return
    raise AssertionError("invalid record incorrectly accepted")


class LatestOnlyContract(unittest.TestCase):
    def test_all_four_kinds_have_one_format(self):
        for kind, data in (("work_item", WORK), ("intent", INTENT), ("event", EVENT), ("report", REPORT)):
            with self.subTest(kind=kind):
                env = {"schema": "ads/github/v2", "kind": kind, "data": data}
                self.assertEqual(validate_subset(env, load_schema("github-document-v2.schema.json")), [])
                self.assertEqual(verify_markdown(render(kind, data), expected_kind=kind), "SHAPE_VALID_ONLY")

    def test_normative_mutations_six_not_eight(self):
        table = {
            "ISSUE_CREATE": ({"work_item": WORK}, None, None),
            "ISSUE_CONTRACT_UPDATE": ({"work_item": WORK, "previous_ref": "blob:before", "reason": "Revision"}, "#42", "github:actual-before"),
            "ISSUE_METADATA_CHANGE": (INTENT["change"], "#42", "github:actual-before"),
            "ISSUE_DEPENDENCY_CHANGE": ({"dependency": "#43", "action": "ADD"}, "#42", "github:actual-before"),
            "ISSUE_CLOSE": ({"reason": "Merged and checked", "evidence_refs": ["github:pr#8@sha"]}, "#42", "github:actual-before"),
            "ISSUE_REOPEN": ({"reason": "Regression found", "evidence_refs": ["github:bug#11"]}, "#42", "github:actual-before"),
        }
        for op, (change, issue, expected_ref) in table.items():
            with self.subTest(op=op):
                v = copy.deepcopy(INTENT)
                v.update(operation=op, change=change, expected_ref=expected_ref)
                v["target"]["issue"] = issue
                self.assertEqual(verify_markdown(render("intent", v)), "SHAPE_VALID_ONLY")

    def test_latest_only_rejects_old_formats(self):
        for legacy in ("<!-- ai-dev:event:v2 -->", "<!-- ads:task-report:v1 -->",
                       "<!-- ads:work-item:v1 -->", "<!-- ads:github-interaction:v1 -->"):
            fail(legacy + "\n```yaml\nschema: old\n```", "latest-only")
        fail("### Introduction\n" + render("event", EVENT), "latest-only")
        fail(render("event", EVENT) + "\n<!-- ads:github:v2 -->", "exactly one")
        fail(render("event", EVENT).replace("ads/github/v2", "ads/github/v1"))
        fail(render("event", EVENT).replace("event", "unknown", 1))

    def test_safe_yaml_and_unknown_are_fail_closed(self):
        doc = render("intent", INTENT)
        fail(doc.replace("id: ", "id: 1\n    id: ", 1))
        fail(doc.replace('operation: "ISSUE_METADATA_CHANGE"', 'operation: &a "ISSUE_METADATA_CHANGE"'))
        fail(doc.replace("```yaml", "```json"), "fenced yaml")
        fail(doc.replace('"codex:a"', "null"))
        fail(doc.replace('"ISSUE_METADATA_CHANGE"', '"ISSUE_COMMENT_EVENT"'))
        fail(doc.replace('"#42"', "null"), "exact issue")

    def test_no_second_comment_operation_or_redundant_publication_key(self):
        fail(render("intent", {**INTENT, "operation": "ISSUE_COMMENT_EVENT"}))
        fail(render("report", {**REPORT, "publication_key": "caller-forged"}))
        fail(render("report", {**REPORT, "manifest_sha256": "bad"}))
        fail(render("report", {**REPORT, "revision": 0}))
        fail(render("report", {**REPORT, "manifest_ref": "https://s3/x?X-Amz-Signature=secret"}), "signed URL")
        fail(render("report", {**REPORT, "report_kind": "EXECUTION_CORRECTION"}), "correction")
        self.assertEqual(verify_markdown(render("report", {
            **REPORT, "report_kind": "EXECUTION_CORRECTION", "corrects_ref": "github:comment:123"
        })), "SHAPE_VALID_ONLY")

    def test_work_item_shape_and_all_profiles(self):
        fail(render("work_item", {"profile": "type:task", "contract": {}}), "missing nested YAML value")
        fail(render("work_item", {"profile": "type:invented", "contract": WORK["contract"]}))
        for profile, fields in {
            "type:version": {"version": "v1", "goal": "Deliver v1", "closure_criteria": ["CI"]},
            "type:planning": {"goal": "Freeze", "frozen_inputs": "ref", "acceptance": ["Review"]},
            "type:research": {"question": "Why", "scope": "Narrow", "acceptance": ["Result"]},
            "type:research-demo": {"hypothesis": "Falsifiable", "acceptance": ["Observation"]},
            "type:bug": {"observed_behavior": "bad", "expected_behavior": "good", "acceptance": ["Fix"]},
            "type:fix": {"observed_behavior": "bad", "expected_behavior": "good", "acceptance": ["Fix"]},
            "type:validation": {"target_sha": SHA, "validation_scope": "concern", "expected_checks": ["test"]},
            "type:blocker": {"blocking_fact": "Unavailable", "unblock_condition": "Recovered"},
            "type:release": {"version": "v1", "release_qualification": "ref"},
        }.items():
            with self.subTest(profile=profile):
                self.assertEqual(verify_markdown(render("work_item", {"profile": profile, "contract": fields})),
                                 "SHAPE_VALID_ONLY")

    def test_native_authority_not_in_yaml_and_issue_match(self):
        fail(render("intent", {**INTENT, "expected_ref": None}), "currentness")
        v = copy.deepcopy(INTENT)
        v["change"]["after"] = "state:passed"
        fail(render("intent", v), "vocabulary")
        v = copy.deepcopy(INTENT)
        v["change"] = {"field": "labels", "before": ["state:ready"], "after": ["gate:pass"]}
        fail(render("intent", v), "Gate truth")
        v = copy.deepcopy(INTENT)
        v["operation"] = "ISSUE_DEPENDENCY_CHANGE"
        v["change"] = {"dependency": "#42", "action": "ADD"}
        fail(render("intent", v), "self-loop")
        fail(render("event", EVENT), "event target", expected_kind="event", issue="#999")
        self.assertEqual(verify_markdown(render("event", EVENT), expected_kind="event", issue="#42"), "SHAPE_VALID_ONLY")
        self.assertEqual(verify_markdown(render("intent", INTENT)), "SHAPE_VALID_ONLY")

    def test_all_current_issue_templates_use_one_v2_contract(self):
        root = Path(__file__).resolve().parents[1]
        for template in (
            "templates/task-issue.md",
            "templates/version-issue.md",
            "templates/planning-amendment-issue.md",
            "templates/research-issue.md",
            "templates/research-demo-issue.md",
            "templates/bug-fix-issue.md",
            "templates/validation-request-issue.md",
            "templates/blocker-issue.md",
        ):
            with self.subTest(template=template):
                content = (root / template).read_text(encoding="utf-8")
                self.assertEqual(verify_markdown(content, expected_kind="work_item"), "SHAPE_VALID_ONLY")

    def test_unstructured_discussion_is_not_mutation(self):
        self.assertEqual(verify_markdown("Ordinary request, no machine contract."), "UNSTRUCTURED_DISCUSSION")
        fail("Ordinary request, no machine contract.", expected_kind="intent", text="latest-only")
        self.assertNotEqual(verify_markdown(render("intent", INTENT)), "ADMITTED")


if __name__ == "__main__":
    unittest.main(verbosity=2)
