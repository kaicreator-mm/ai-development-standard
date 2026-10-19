#!/usr/bin/env python3
"""Positive and adversarial tests for opt-in GitHub structured interaction v1."""
from __future__ import annotations

import copy
import json
import unittest
from verify_github_structured_interaction import (
    ContractError, parse_yaml, verify_markdown, check_intent, check_work_item, REPORT_KINDS
)
from test_protocol_schemas import load_schema, validate_subset

EXACT_SHA = "a" * 40
BASE = {
    "schema_version": "ads/github-structured-interaction/v1",
    "intent_id": "request:1",
    "operation": "ISSUE_METADATA_CHANGE",
    "target": {"repository": "example-org/example-repo", "issue_ref": "#42"},
    "actor": {"actor_role": "builder", "operator_kind": "codex", "operator_id": "codex:one"},
    "expected_source_ref": "github:example-org/example-repo#42@revision-2",
    "payload": {"field": "state", "before": "state:ready", "after": "state:claimed"},
}
WORK = {"schema_version": "ads/work-item/v1", "work_item_type": "type:task",
        "contract": {"task_id": "T02", "goal": "Test", "integration_target": "version/v0.1",
                     "baseline_sha": EXACT_SHA, "review_policy": "recommended",
                     "required_gates": ["unit"], "acceptance": ["one real test"]}}


def emitter(obj, indent=0):
    """Only the explicitly supported subset; fixtures are not a full YAML generator."""
    lines = []
    for key, value in obj.items():
        pad = " " * indent
        if isinstance(value, dict):
            lines.append(pad + key + ":")
            lines.extend(emitter(value, indent + 2))
        elif isinstance(value, list):
            lines.append(pad + key + ":")
            for item in value:
                lines.append(pad + "  - " + json.dumps(item))
        else:
            lines.append(pad + key + ": " + json.dumps(value))
    return lines


def mk(obj, marker="<!-- ads:github-interaction:v1 -->"):
    return marker + "\n```yaml\n" + "\n".join(emitter(obj)) + "\n```\n\n## Note\nSafe prose.\n"


def fails(data, message=None):
    try:
        verify_markdown(data)
    except ContractError as exc:
        if message and message not in str(exc):
            raise AssertionError(f"wanted {message!r}: got {exc}") from exc
        return
    raise AssertionError("expected invalid structured interaction to fail")


class ContractTests(unittest.TestCase):
    def test_registered_envelopes_machine_schema(self):
        for name, value in (("github-structured-interaction-v1.schema.json", BASE),
                            ("github-work-item-document-v1.schema.json", WORK)):
            self.assertEqual(validate_subset(value, load_schema(name)), [])

    def test_markdown_yaml_work_item_and_intent(self):
        self.assertEqual(verify_markdown(mk(BASE)), "SHAPE_VALID_ONLY")
        self.assertEqual(verify_markdown(mk(WORK, "<!-- ads:work-item:v1 -->")),
                         "SHAPE_VALID_ONLY")
        self.assertEqual(verify_markdown("Just a discussion about a possible change."),
                         "UNSTRUCTURED_DISCUSSION")
        self.assertEqual(verify_markdown(mk(BASE), "intent"), "SHAPE_VALID_ONLY")

    def test_all_normative_operations(self):
        examples = {
            "ISSUE_CREATE": ({"work_item": WORK}, None, None),
            "ISSUE_CONTRACT_UPDATE": ({"work_item": WORK, "previous_contract_ref": "blob:old", "change_reason": "Amend scope"}, "#42", "current:sha"),
            "ISSUE_METADATA_CHANGE": (BASE["payload"], "#42", "current:sha"),
            "ISSUE_DEPENDENCY_CHANGE": ({"dependency_issue_ref": "#43", "change": "ADD"}, "#42", "current:sha"),
            "ISSUE_COMMENT_EVENT": ({"event": {"schema": "ai-dev/event-v2", "event": "ROLE_CLAIMED",
                                             "actor_role": "builder", "operator_kind": "codex",
                                             "operator_id": "codex:one", "task": "#42"}},
                                    "#42", "current:sha"),
            "ISSUE_COMMENT_REPORT": ({"report_kind": "EXECUTION_SUMMARY", "report_id": "task:r1",
                                      "revision": 1, "attempt_ref": "attempt:r1",
                                      "publication_key": "github:example-org/example-repo#42 | task:r1 | 1",
                                      "manifest_ref": "object:private/r1/manifest.json",
                                      "manifest_sha256": "b" * 64}, "#42", "current:sha"),
            "ISSUE_CLOSE": ({"reason": "Result evidence", "evidence_refs": ["pr:#9@sha"]}, "#42", "current:sha"),
            "ISSUE_REOPEN": ({"reason": "Post-close regression", "evidence_refs": ["bug:#19"]}, "#42", "current:sha"),
        }
        for operation, (payload, issue, expected) in examples.items():
            with self.subTest(operation=operation):
                v = copy.deepcopy(BASE)
                v["operation"] = operation
                v["payload"] = payload
                v["target"]["issue_ref"] = issue
                v["expected_source_ref"] = expected
                self.assertEqual(verify_markdown(mk(v)), "SHAPE_VALID_ONLY")

    def test_legacy_event_and_report_read_compatibility(self):
        event = {"schema": "ai-dev/event-v2", "event": "ROLE_CLAIMED",
                 "actor_role": "builder", "operator_kind": "codex",
                 "operator_id": "codex:one", "task": "#42"}
        self.assertEqual(verify_markdown(mk(event, "<!-- ai-dev:event:v2 -->")),
                         "SHAPE_VALID_ONLY")
        text = ("<!-- ads:task-report:v1 -->\nREPORT_KIND=EXECUTION_SUMMARY\n"
                "REPORT_ID=task:r1\nREPORT_REVISION=1\nATTEMPT_REF=attempt:1\n"
                "PUBLICATION_KEY=github:example-org/example-repo#42 | task:r1 | 1\n"
                "MANIFEST_REF=object:private/r1/manifest.json\n"
                "MANIFEST_SHA256=" + "c" * 64 + "\n\nSummary of observed work.")
        self.assertEqual(verify_markdown(text), "SHAPE_VALID_ONLY")
        fails(text.replace("REPORT_KIND=EXECUTION_SUMMARY", "REPORT_KIND=UNKNOWN"))

    def test_unsupported_and_tricky_yaml_fails_closed(self):
        fails("## Explanation\n\n" + mk(BASE), "embedded/quoted")
        fails(mk(BASE).replace("intent_id:", "intent_id: 1\nintent_id:"), "duplicate key")
        fails(mk(BASE).replace("intent_id: ", "intent_id: &alias "), "unsupported")
        fails(mk(BASE).replace("```yaml", "```json"), "fenced")
        fails(mk(BASE) + "\n<!-- ads:github-interaction:v1 -->", "unique marker")
        fails(mk(BASE).replace("operation: ", "operation: Z\noperation: "))
        fails(mk(BASE).replace('"ISSUE_METADATA_CHANGE"', '"UNSUPPORTED"'))
        fails(mk(BASE).replace('"codex:one"', 'null'))
        fails(mk(BASE).replace('"#42"', 'null'), "exact Issue")

    def test_authoritative_fact_invariants_are_not_claimed_by_shape(self):
        mut = copy.deepcopy(BASE)
        mut["payload"]["after"] = "state:validated"
        fails(mk(mut), "vocabulary")
        mut = copy.deepcopy(BASE)
        mut["expected_source_ref"] = None
        fails(mk(mut), "precondition")
        mut = copy.deepcopy(BASE)
        mut["payload"]["field"] = "labels"
        mut["payload"]["before"], mut["payload"]["after"] = "state:ready", "gate:pass"
        fails(mk(mut), "labels must be lists")
        mut = copy.deepcopy(BASE)
        mut["operation"] = "ISSUE_DEPENDENCY_CHANGE"
        mut["payload"] = {"dependency_issue_ref": "#42", "change": "ADD"}
        fails(mk(mut), "dependency")
        mut = copy.deepcopy(BASE)
        mut["operation"] = "ISSUE_CLOSE"
        mut["payload"] = {"reason": "I say PASS", "evidence_refs": []}
        fails(mk(mut), "missing nested YAML value")
        mut = copy.deepcopy(BASE)
        mut["operation"] = "ISSUE_COMMENT_REPORT"
        mut["payload"] = {"report_kind": "EXECUTION_SUMMARY", "report_id": "id", "revision": 1,
                          "attempt_ref": "attempt", "publication_key": "bad",
                          "manifest_ref": "private:key", "manifest_sha256": "f" * 64}
        fails(mk(mut), "publication key mismatch")
        mut["payload"]["publication_key"] = "github:example-org/example-repo#42 | id | 1"
        mut["payload"]["manifest_sha256"] = "not-a-hash"
        fails(mk(mut), "checksum")

    def test_nested_event_actor_and_work_item_must_match_envelope(self):
        mut = copy.deepcopy(BASE)
        mut["operation"] = "ISSUE_COMMENT_EVENT"
        mut["payload"] = {"event": {
            "schema": "ai-dev/event-v2", "event": "ROLE_CLAIMED",
            "actor_role": "reviewer", "operator_kind": "codex",
            "operator_id": "codex:one", "task": "#42"
        }}
        fails(mk(mut), "attribution conflicts")
        mut["payload"]["event"]["actor_role"] = "builder"
        mut["payload"]["event"]["task"] = "#43"
        fails(mk(mut), "target conflicts")

    def test_work_item_profiles_and_shape_failures(self):
        wrong = copy.deepcopy(WORK)
        del wrong["contract"]["baseline_sha"]
        fails(mk(wrong, "<!-- ads:work-item:v1 -->"), "task-contract")
        other = {"schema_version": "ads/work-item/v1", "work_item_type": "type:blocker",
                 "contract": {"blocking_fact": "runner down", "unblock_condition": "host ready"}}
        self.assertEqual(verify_markdown(mk(other, "<!-- ads:work-item:v1 -->")),
                         "SHAPE_VALID_ONLY")
        other["contract"]["unblock_condition"] = None
        fails(mk(other, "<!-- ads:work-item:v1 -->"), "unblock_condition")

    def test_parser_returns_shape_only_not_success_or_admission(self):
        result = verify_markdown(mk(BASE))
        self.assertEqual(result, "SHAPE_VALID_ONLY")
        self.assertNotIn(result, ("PASS", "ADMITTED", "MUTATED"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
