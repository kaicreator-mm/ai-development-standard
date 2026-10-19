#!/usr/bin/env python3
"""v4.14 full JSON Schema and Markdown/YAML conformance tests."""
import copy
import unittest
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator
from verify_github_structured_interaction import (
    ContractError, ROOT, SCHEMA_FILE, MARKER, validate_record, verify_markdown
)

SHA="a"*40
WORK={"profile":"type:task","contract":{"task_id":"T01","goal":"Bounded task",
"baseline_sha":SHA,"integration_target":"version/v4.14","review_policy":"recommended",
"required_gates":["unit"],"acceptance":["One exact source-backed test"]}}
INTENT={"id":"intent:one","operation":"ISSUE_METADATA_CHANGE",
"target":{"repository":"example-org/example-repo","issue":"#42"},
"actor":{"role":"builder","operator_kind":"codex","operator_id":"codex:a"},
"expected_ref":"github:current:42",
"change":{"field":"state","before":"state:planned","after":"state:ready"}}
EVENT={"schema":"ai-dev/event-v2","event":"ROLE_CLAIMED",
"actor_role":"builder","operator_kind":"codex","operator_id":"codex:a","task":"#42"}
REPORT={"report_id":"report:42","report_kind":"EXECUTION_SUMMARY","revision":1,
"attempt_ref":"attempt:42","manifest_ref":"object:private/42/r1/manifest.json",
"manifest_sha256":"b"*64,"coverage":"PARTIAL"}

def envelope(kind,data):
    return {"schema":"ads/github/v3","kind":kind,"data":data}

def markdown(kind,data):
    return MARKER+"\n```yaml\n"+yaml.safe_dump(envelope(kind,data),sort_keys=False)+"```\n\n# Context\nActual refs only.\n"

def rejects(kind,data):
    with unittest.TestCase().assertRaises(ContractError):
        validate_record(envelope(kind,data))

class V414(unittest.TestCase):
    def test_four_discriminated_branches(self):
        from json import loads
        schema=loads(SCHEMA_FILE.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
        self.assertEqual(len(schema["oneOf"]),4)
        self.assertIn("oneOf",schema["$defs"]["work_item"])
        self.assertIn("oneOf",schema["$defs"]["intent"])
        for kind,value in (("work_item",WORK),("intent",INTENT),("event",EVENT),("report",REPORT)):
            with self.subTest(kind=kind):
                self.assertEqual(verify_markdown(markdown(kind,value),kind),"SHAPE_VALID_ONLY")
        rejects("work_item",REPORT)
        rejects("event",{"schema":"ai-dev/event-v2","event":"ROLE_CLAIMED"})
        rejects("unknown",WORK)

    def test_all_ten_workitem_profiles(self):
        cases={
        "type:version":{"version":"v4.14","goal":"release","closure_criteria":["CI"]},
        "type:planning":{"goal":"plan","frozen_inputs":"source:abc","acceptance":["evidence"]},
        "type:research":{"question":"Why","scope":"limited","acceptance":["evidence"]},
        "type:research-demo":{"hypothesis":"falsifiable","acceptance":["test"]},
        "type:task":WORK["contract"],
        "type:bug":{"observed_behavior":"bad","expected_behavior":"good","acceptance":["fix"]},
        "type:fix":{"observed_behavior":"bad","expected_behavior":"good","acceptance":["fix"]},
        "type:validation":{"target_sha":SHA,"validation_scope":"concern","expected_checks":["test"]},
        "type:blocker":{"blocking_fact":"down","unblock_condition":"up"},
        "type:release":{"version":"v4.14","release_qualification":"ref"},
        }
        for profile,contract in cases.items():
            with self.subTest(profile=profile):
                self.assertEqual(validate_record(envelope("work_item",{"profile":profile,"contract":contract})),"SHAPE_VALID_ONLY")
        rejects("work_item",{"profile":"type:task","contract":{"goal":"missing"}})
        rejects("work_item",{"profile":"type:research","contract":{"question":"missing"}})
        rejects("work_item",{"profile":"type:invented","contract":{}})
        rejects("work_item",{"profile":"type:bug","contract":{**cases["type:bug"],"hidden":True}})

    def test_six_native_intent_actions(self):
        table={
        "ISSUE_CREATE":(None,None,{"work_item":WORK}),
        "ISSUE_CONTRACT_UPDATE":("#42","current",{"work_item":WORK,"previous_ref":"blob:1","reason":"amend"}),
        "ISSUE_METADATA_CHANGE":("#42","current",INTENT["change"]),
        "ISSUE_DEPENDENCY_CHANGE":("#42","current",{"dependency":"#43","action":"ADD"}),
        "ISSUE_CLOSE":("#42","current",{"reason":"evidence","evidence_refs":["pr:#12@sha"]}),
        "ISSUE_REOPEN":("#42","current",{"reason":"regression","evidence_refs":["issue:#42"]}),
        }
        for operation,(issue,current,change) in table.items():
            obj=copy.deepcopy(INTENT);obj.update(operation=operation,expected_ref=current,change=change)
            obj["target"]["issue"]=issue
            with self.subTest(operation=operation):
                self.assertEqual(validate_record(envelope("intent",obj)),"SHAPE_VALID_ONLY")
                rejects("intent",{**obj,"change":{}})
        rejects("intent",{**INTENT,"operation":"ISSUE_COMMENT_EVENT"})
        rejects("intent",{**INTENT,"expected_ref":None})
        m=copy.deepcopy(INTENT);m["change"]["after"]="state:passed";rejects("intent",m)
        m=copy.deepcopy(INTENT);m["change"]={"field":"labels","before":["state:ready"],"after":["gate:pass"]};rejects("intent",m)

    def test_report_conditional_and_durable_locator(self):
        rejects("report",{**REPORT,"manifest_sha256":"invalid"})
        rejects("report",{**REPORT,"report_kind":"EXECUTION_CORRECTION"})
        self.assertEqual(validate_record(envelope("report",{**REPORT,"report_kind":"EXECUTION_CORRECTION","corrects_ref":"github:comment:100"})),"SHAPE_VALID_ONLY")
        rejects("report",{**REPORT,"corrects_ref":"unexpected"})
        rejects("report",{**REPORT,"manifest_ref":"https://s3/file?X-Amz-Signature=secret"})
        rejects("report",{**REPORT,"publication_key":"redundant"})

    def test_unsafe_yaml_and_latest_only(self):
        source=markdown("intent",INTENT)
        for text in (source.replace("kind: intent","kind: intent\nkind: report"),
                     source.replace("kind: intent","kind: &alias intent"),
                     source.replace("kind: intent","kind: !unsafe intent"),
                     source.replace("kind: intent","kind: *alias"),
                     "## quoted\n"+source,
                     source.replace("ads/github/v3","ads/github/v2"),
                     "<!-- ads:github:v2 -->\n"+source):
            with self.subTest(case=text[:80]),self.assertRaises(ContractError):
                verify_markdown(text)
        self.assertEqual(verify_markdown("free discussion"),"UNSTRUCTURED_DISCUSSION")

    def test_all_current_templates_use_latest_schema(self):
        templates=["task-issue.md","version-issue.md","planning-amendment-issue.md",
        "research-issue.md","research-demo-issue.md","bug-fix-issue.md",
        "validation-request-issue.md","blocker-issue.md"]
        for name in templates:
            with self.subTest(template=name):
                body=(ROOT/"templates"/name).read_text(encoding="utf-8")
                self.assertEqual(verify_markdown(body,"work_item"),"SHAPE_VALID_ONLY")

    def test_shape_is_never_admission(self):
        self.assertEqual(verify_markdown(markdown("intent",INTENT)),"SHAPE_VALID_ONLY")
        self.assertNotEqual(validate_record(envelope("intent",INTENT)),"ADMITTED")

if __name__=="__main__":
    unittest.main(verbosity=2)
