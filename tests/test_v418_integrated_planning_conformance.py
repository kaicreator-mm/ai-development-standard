"""ADS v4.18 integrated E1 source-only conformance.

Historic T13/T05A subprocesses retain actual EXIT=1. This oracle rejects any
new failures but does NOT waive the three prior owner-pin failed subtests.
Release-owner applicability remains separately required.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]

def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")

HISTORIC = {
    "scripts/test_v411_t13_role_conduct.py": (
        62, (
            ("test_complete_owner_standards_match_reviewed_qualified_source",
             "owner_path='standards/TASK_DECOMPOSITION_STANDARD.md'"),
            ("test_complete_owner_standards_match_reviewed_qualified_source",
             "owner_path='standards/DEVELOPMENT_WORKFLOW.md'"),
        )
    ),
    "scripts/test_v410_t05a_shared_code_safety.py": (
        39, (("test_owner_blob_identities_are_pinned",
              "owner='TASK_DECOMPOSITION_STANDARD.md'"),)
    ),
}

class IntegratedPlanning(unittest.TestCase):
    def test_tds_bounded_topology_and_no_new_authority(self):
        source = read("standards/TASK_DECOMPOSITION_STANDARD.md")
        section = source.split("## 13. Decomposition decision prompts\n", 1)[1]
        section = section.split("## 14. Failure handling", 1)[0]
        for token in (
            "Planner SHOULD compare", "safe alternative Task DAG topology",
            "serial execution is necessary", "without inventing measured speedups",
            "non-authoritative planning annotations",
            "GitHub native Issue Dependencies", "ready_builder", "JIT",
            "accepted Claim", "write-set/Scaffold Anchor ownership",
            "merge/Release admission",
        ):
            with self.subTest(token=token):
                self.assertIn(token, section)

    def test_template_capability_scaffold_agent_and_native_boundary(self):
        template = read("templates/task-dag.md")
        for token in (
            "maximum safe parallelism", "## Lane Summary",
            "Optional v4.18 Capability-first / Safe Topology Assessment",
            "Product capabilities", "Concerns", "compare one legal alternative",
            "non-authoritative planning explanations",
            "native " + chr(96) + "blocked_by" + chr(96),
            "ready_builder", "JIT admitted Claim",
            "Optional pre-Freeze Scaffold feedback",
            "accepted source-first SF checkpoint", "§10A",
            "SF_PLANNING_FEEDBACK=NOT_APPLICABLE",
            "Candidate Agent, proof and human-assistance fit",
            "WEB / CI / LOCAL",
        ):
            with self.subTest(token=token):
                self.assertIn(token, template)
        self.assertNotIn("Lane = canonical live execution DAG", template)
        self.assertNotIn("Parallel=YES means dependency-free", template)

    def test_golden_registered_owner_and_seven_pairs(self):
        ref = read("references/TASK_DECOMPOSITION_REFERENCE.md")
        coverage = json.loads(read("templates/golden/STANDARD_COVERAGE.json"))
        matches = [item for item in coverage["coverage"]
                   if item["standard"] == "standards/TASK_DECOMPOSITION_STANDARD.md"]
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["golden_ref"],
                         "references/TASK_DECOMPOSITION_REFERENCE.md")
        sections = ref.split("## 10. Optional v4.18 Safe Task DAG Planning Patterns")
        self.assertEqual(len(sections), 2)
        rows = re.findall(r"^\| (G418-\d{2}) \| ([^\n]+)$",
                          sections[1], re.MULTILINE)
        self.assertEqual([case for case, _ in rows],
                         [f"G418-{n:02d}" for n in range(1, 8)])
        corpus = read("templates/golden/STANDARD_CONFORMANCE_EXAMPLES.md")
        for case, content in rows:
            with self.subTest(case=case):
                self.assertEqual(len(content.split(" | ")), 3)
                self.assertNotIn(case, corpus)
        self.assertIn("fictitious E1 planning oracles", ref)

    def test_planning_doc_does_not_supersede_live_issue_dag(self):
        dag = read("docs/implementation/4.18.0/TASK_DAG.md")
        for token in ("NATIVE_DEPENDENCY_EDGES_MISSING", "Issue Dependencies",
                      "#1323", "#1324", "#1325", "#1326", "#1327",
                      "not yet present", "authoritative executable DAG"):
            self.assertIn(token, dag)
        # The planning checkpoint is historical, not live Issue readiness.

    def test_both_full_historic_suites_no_new_failures(self):
        for path, (count, expected) in HISTORIC.items():
            with self.subTest(path=path):
                env = os.environ.copy()
                env["PYTHONDONTWRITEBYTECODE"] = "1"
                # Child unittest emits stable UTF-8 even on Windows code-page hosts.
                env["PYTHONUTF8"] = "1"
                env["PYTHONIOENCODING"] = "utf-8"
                proc = subprocess.run(
                    [sys.executable, path], cwd=ROOT, capture_output=True,
                    text=True, encoding="utf-8", errors="replace",
                    timeout=180, env=env
                )
                log = (proc.stdout or "") + "\n" + (proc.stderr or "")
                headers = re.findall(r"^(?:FAIL|ERROR): [^\n]+", log, re.MULTILINE)
                observed = []
                for header in headers:
                    match = [pair for pair in expected
                             if pair[0] in header and pair[1] in header]
                    observed.append(match[0] if len(match) == 1
                                    else ("UNEXPECTED", header))
                print(f"\nHISTORIC_RAW_SUITE={path} EXIT={proc.returncode} "
                      f"RAN_EXPECTED={count} FAIL_HEADERS={len(headers)}", flush=True)
                for header in headers:
                    print("HISTORIC_RAW_FAILURE_HEADER=" + header, flush=True)
                self.assertEqual(proc.returncode, 1)
                self.assertRegex(log, rf"Ran {count} tests? in ")
                self.assertEqual(sorted(observed), sorted(expected),
                                 f"New/missing historic failure identity:\n{log[-5000:]}")
                self.assertNotRegex(log, r"FAILED \([^)]*(?:errors=[1-9]|skipped=[1-9])")
                self.assertNotIn("OK (skipped=", log)

if __name__ == "__main__":
    unittest.main()
