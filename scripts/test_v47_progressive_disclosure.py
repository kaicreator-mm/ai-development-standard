"""T05 deterministic fixture conformance; this is not live external validation."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from resolve_standard_read_set import resolve_standard_read_set

ROOT = Path(__file__).resolve().parents[1]
PIN, SUBJECT, BASE = "a" * 40, "b" * 40, "c" * 40
ISSUE = "https://github.com/kaicreator-mm/demo/issues/7"


class ProgressiveDisclosureRoutingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.project = Path(self.tmp.name) / "project"
        self.project.mkdir()
        (self.project / ".dev-standard").mkdir()
        (self.project / "docs/tasks").mkdir(parents=True)
        (self.project / "profiles").mkdir()
        (self.project / "AGENTS.md").write_text("project authority\n", encoding="utf-8")
        (self.project / ".dev-standard/VERSION").write_text(
            f"repository=kaicreator-mm/ai-development-standard\nversion=4.7.0\nrevision={PIN}\n", encoding="utf-8"
        )
        (self.project / "docs/tasks/T05.md").write_text("task T05\n", encoding="utf-8")
        (self.project / "profiles/python.md").write_text("python profile\n", encoding="utf-8")
        self.set_overrides(profile=True)

        self.ads = Path(self.tmp.name) / "ads"
        (self.ads / "schemas").mkdir(parents=True)
        (self.ads / "standards").mkdir()
        (self.ads / "AGENTS.md").write_text("ads authority\n", encoding="utf-8")
        shutil.copyfile(ROOT / "schemas/authority-applicability-entry-v1.schema.json", self.ads / "schemas/authority-applicability-entry-v1.schema.json")
        manifest = json.loads((ROOT / "standard-manifest.json").read_text(encoding="utf-8"))
        (self.ads / "standard-manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        for rel in (manifest["sections"]["normative_standards"] + manifest["sections"]["compatibility_entries"] + manifest["sections"].get("references", [])):
            path = self.ads / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(rel + "\n", encoding="utf-8")
        (self.ads / "profiles").mkdir(exist_ok=True)
        (self.ads / "profiles/python.md").write_text("ads python\n", encoding="utf-8")
        self.request = {
            "task_issue_ref": ISSUE,
            "task_pack_ref": "docs/tasks/T05.md",
            "subject_sha": SUBJECT,
            "base_sha": BASE,
            "requested_concerns": ["github.issue_pr_event_coordination"],
            "requested_capabilities": [],
            "stage": "task",
            "intent": "read",
            "chat_history": "stale owner should win because it is long",
            "provider_available": True,
        }
        self.facts = {
            "task_issue_ref": ISSUE,
            "task_pack_ref": "docs/tasks/T05.md",
            "current_subject_sha": SUBJECT,
            "current_base_sha": BASE,
            "materiality": {
                "github.issue_pr_event_coordination": {"decision": "APPLICABLE", "source_ref": ISSUE}
            },
        }

    def set_overrides(self, *, profile: bool = True, reducer: str = "enabled + durable facts") -> None:
        text = f"""# Project Overrides
- v4.reducer: {reducer}
- v4.controllers: enabled + bounded concerns
- v4.interchange: disabled
- v4.fast_path: canonical
- execution_pack.enabled: false
- validation_queue.enabled: false
"""
        if profile:
            text += "- language_profile_ref: project:profiles/python.md\n"
        (self.project / ".dev-standard/PROJECT_OVERRIDES.md").write_text(text, encoding="utf-8")

    def reader(self, _request):
        return deepcopy(self.facts)

    def resolve(self, request=None, reader=None):
        return resolve_standard_read_set(
            self.project, self.ads, request or self.request,
            authority_reader=reader or self.reader,
            revision_probe=lambda _root: PIN,
            authority_reader_scope="TEST_FIXTURE",
        )

    def test_fresh_pin_owner_overrides_profile_task_order(self) -> None:
        result = self.resolve()
        self.assertEqual(result["status"], "RESOLVED")
        refs = [item["ref"] for item in result["read_set"]]
        self.assertLess(refs.index("project:.dev-standard/VERSION"), refs.index("ads:standard-manifest.json"))
        self.assertLess(refs.index("ads:standards/DEVELOPMENT_WORKFLOW.md"), refs.index("project:.dev-standard/PROJECT_OVERRIDES.md"))
        self.assertLess(refs.index("project:.dev-standard/PROJECT_OVERRIDES.md"), refs.index("project:profiles/python.md"))
        self.assertLess(refs.index("project:profiles/python.md"), refs.index("project:docs/tasks/T05.md"))
        self.assertLess(refs.index("project:docs/tasks/T05.md"), refs.index(ISSUE))
        self.assertEqual(result["authority_reader_scope"], "TEST_FIXTURE")
        self.assertFalse(result["mutation_authorized"])
        self.assertEqual(result["gate_effect"], "NONE")

    def test_optional_context_is_not_forced(self) -> None:
        request = deepcopy(self.request)
        request["requested_concerns"] = []
        self.set_overrides(profile=False)
        result = self.resolve(request)
        refs = [item["ref"] for item in result["read_set"]]
        self.assertEqual(result["status"], "RESOLVED")
        self.assertNotIn("ads:standards/ARCHITECTURE_RESEARCH_DEMO_STANDARD.md", refs)
        self.assertFalse(any(item["kind"] == "selected-profile" for item in result["read_set"]))

    def test_stale_chat_and_larger_context_never_override_owner(self) -> None:
        request = deepcopy(self.request)
        request["chat_history"] = "standards/RELEASE_STANDARD.md " * 1000
        request["context_volume"] = 999999
        result = self.resolve(request)
        owners = [item["ref"] for item in result["read_set"] if item["kind"] == "semantic-owner"]
        self.assertIn("ads:standards/GITHUB_AGENT_INTERACTION_PROTOCOL.md", owners)
        self.assertNotIn("ads:standards/RELEASE_STANDARD.md", owners)
        self.assertIn("context_volume", result["ignored_lower_authority_inputs"])

    def test_registry_conflict_rejects_even_when_reversed(self) -> None:
        manifest_path = self.ads / "standard-manifest.json"
        original = json.loads(manifest_path.read_text(encoding="utf-8"))
        for reverse in (False, True):
            mutant = deepcopy(original)
            contender = deepcopy(mutant["semantic_authorities"]["entries"][0])
            contender["entry_id"] = "competing-owner"
            contender["canonical_owner_ref"] = "standards/RELEASE_STANDARD.md"
            mutant["semantic_authorities"]["entries"].append(contender)
            if reverse:
                mutant["semantic_authorities"]["entries"].reverse()
            manifest_path.write_text(json.dumps(mutant), encoding="utf-8")
            result = self.resolve()
            self.assertEqual(result["status"], "BLOCKED")
            self.assertIn("REGISTRY_UNRESOLVED", {b["code"] for b in result["blockers"]})
        manifest_path.write_text(json.dumps(original), encoding="utf-8")

    def test_materiality_unknown_fails_closed(self) -> None:
        self.facts["materiality"] = {"github.issue_pr_event_coordination": {"decision": "UNKNOWN", "source_ref": ISSUE}}
        result = self.resolve()
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("MATERIALITY_UNKNOWN", {b["code"] for b in result["blockers"]})

    def test_disabled_project_capability_requested_fails_closed(self) -> None:
        request = deepcopy(self.request)
        request["requested_capabilities"] = ["v4.reducer"]
        self.set_overrides(reducer="disabled")
        result = self.resolve(request)
        self.assertIn("CAPABILITY_DISABLED", {b["code"] for b in result["blockers"]})

    def test_conflicting_duplicate_capability_fails_closed_in_both_orders(self) -> None:
        request = deepcopy(self.request)
        request["requested_capabilities"] = ["v4.reducer"]
        path = self.project / ".dev-standard/PROJECT_OVERRIDES.md"
        for first, second in (("disabled", "enabled"), ("enabled", "disabled")):
            with self.subTest(first=first, second=second):
                self.set_overrides(profile=False, reducer=first)
                path.write_text(path.read_text(encoding="utf-8") + f"- v4.reducer: {second}\n", encoding="utf-8")
                result = self.resolve(request)
                self.assertEqual(result["status"], "BLOCKED")
                self.assertFalse(result["complete"])
                self.assertIn("CONFLICTING_PROJECT_OVERRIDE", {b["code"] for b in result["blockers"]})
                self.assertEqual(result["gate_effect"], "NONE")

    def test_duplicate_capability_even_if_identical_is_not_silent(self) -> None:
        path = self.project / ".dev-standard/PROJECT_OVERRIDES.md"
        path.write_text(path.read_text(encoding="utf-8") + "- v4.reducer: enabled + durable facts\n", encoding="utf-8")
        result = self.resolve()
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("DUPLICATE_PROJECT_OVERRIDE", {b["code"] for b in result["blockers"]})

    def test_profile_duplicates_and_conflicts_fail_closed_in_both_orders(self) -> None:
        path = self.project / ".dev-standard/PROJECT_OVERRIDES.md"
        for first, second in (
            ("project:profiles/python.md", "ads:profiles/python.md"),
            ("ads:profiles/python.md", "project:profiles/python.md"),
            ("project:profiles/python.md", "project:profiles/python.md"),
        ):
            with self.subTest(first=first, second=second):
                self.set_overrides(profile=False)
                path.write_text(path.read_text(encoding="utf-8") +
                                f"- language_profile_ref: {first}\n- language_profile_ref: {second}\n", encoding="utf-8")
                result = self.resolve()
                self.assertEqual(result["status"], "BLOCKED")
                expected = "DUPLICATE_PROJECT_OVERRIDE" if first == second else "CONFLICTING_PROJECT_OVERRIDE"
                self.assertIn(expected, {b["code"] for b in result["blockers"]})
                self.assertFalse(any(item["kind"] == "selected-profile" for item in result["read_set"]))

    def test_pin_and_exact_subject_drift_fail_closed(self) -> None:
        result = resolve_standard_read_set(
            self.project, self.ads, self.request,
            authority_reader=self.reader,
            revision_probe=lambda _root: "d" * 40,
            authority_reader_scope="TEST_FIXTURE",
        )
        self.assertIn("ADS_PIN_MISMATCH", {b["code"] for b in result["blockers"]})
        self.facts["current_subject_sha"] = "e" * 40
        result = self.resolve()
        self.assertIn("EXACT_SUBJECT_DRIFT", {b["code"] for b in result["blockers"]})

    def test_provider_availability_without_mutation_authority_rejects(self) -> None:
        request = deepcopy(self.request)
        request["intent"] = "mutation"
        request["provider_available"] = True
        result = self.resolve(request)
        self.assertIn("MUTATION_AUTHORITY_NOT_PROVEN", {b["code"] for b in result["blockers"]})

    def test_invalid_nonempty_stage_and_intent_never_fall_back_to_read(self) -> None:
        for field, invalid, blocker in (
            ("stage", "execution ", "INVALID_ROUTING_STAGE"),
            ("stage", "EXECUTION", "INVALID_ROUTING_STAGE"),
            ("stage", "unrecognized", "INVALID_ROUTING_STAGE"),
            ("stage", 123, "INVALID_ROUTING_STAGE"),
            ("intent", "mutation ", "INVALID_ROUTING_INTENT"),
            ("intent", "MUTATION", "INVALID_ROUTING_INTENT"),
            ("intent", "write", "INVALID_ROUTING_INTENT"),
            ("intent", ["mutation"], "INVALID_ROUTING_INTENT"),
        ):
            with self.subTest(field=field, invalid=invalid):
                request = deepcopy(self.request)
                request[field] = invalid
                result = self.resolve(request)
                self.assertEqual(result["status"], "BLOCKED")
                self.assertFalse(result["complete"])
                self.assertIn(blocker, {b["code"] for b in result["blockers"]})
                self.assertFalse(result["mutation_authorized"])

    def test_omitted_legacy_modes_and_explicit_read_task_modes_resolve(self) -> None:
        for stage, intent in ((None, None), ("", ""), ("read", "read"), ("task", "read")):
            with self.subTest(stage=stage, intent=intent):
                request = deepcopy(self.request)
                if stage is None:
                    request.pop("stage")
                else:
                    request["stage"] = stage
                if intent is None:
                    request.pop("intent")
                else:
                    request["intent"] = intent
                result = self.resolve(request)
                self.assertEqual(result["status"], "RESOLVED")
                self.assertEqual(result["gate_effect"], "NONE")
                self.assertFalse(result["mutation_authorized"])

    def test_valid_mutation_mode_preserves_separate_exact_subject_check(self) -> None:
        request = deepcopy(self.request)
        request["intent"] = "mutation"
        self.facts["mutation_authority_ref"] = "project:.agent/execution/T05/dispatch.json"
        self.facts["mutation_subject_sha"] = "f" * 40
        self.assertIn("MUTATION_AUTHORITY_NOT_PROVEN", {b["code"] for b in self.resolve(request)["blockers"]})
        self.facts["mutation_subject_sha"] = SUBJECT
        result = self.resolve(request)
        self.assertEqual(result["status"], "RESOLVED")
        self.assertFalse(result["mutation_authorized"])
        self.assertEqual(result["authority_effect"], "NONE")

    def test_unknown_owner_never_guesses_from_unmerged_history(self) -> None:
        request = deepcopy(self.request)
        request["requested_concerns"] = ["runtime.future_unmerged_owner"]
        result = self.resolve(request)
        self.assertIn("UNKNOWN_SEMANTIC_OWNER", {b["code"] for b in result["blockers"]})

    def test_execution_requires_existing_exact_subject_authority(self) -> None:
        request = deepcopy(self.request)
        request["stage"] = "execution"
        result = self.resolve(request)
        self.assertIn("EXECUTION_AUTHORITY_MISSING", {b["code"] for b in result["blockers"]})
        self.facts["dispatch_ref"] = "project:.agent/execution/T05/dispatch.json"
        self.facts["execution_pack_ref"] = "project:.agent/execution/T05/MANIFEST.yaml"
        (self.project / ".agent/execution/T05").mkdir(parents=True)
        (self.project / ".agent/execution/T05/dispatch.json").write_text("{}", encoding="utf-8")
        (self.project / ".agent/execution/T05/MANIFEST.yaml").write_text("pack: T05", encoding="utf-8")
        self.facts["execution_pack_subject_sha"] = SUBJECT
        self.facts["dispatch_subject_sha"] = "f" * 40
        result = self.resolve(request)
        self.assertIn("EXECUTION_SUBJECT_DRIFT", {b["code"] for b in result["blockers"]})
        self.facts["dispatch_subject_sha"] = SUBJECT
        result = self.resolve(request)
        self.assertEqual(result["status"], "RESOLVED")
        refs = [item["ref"] for item in result["read_set"]]
        self.assertIn(self.facts["dispatch_ref"], refs)
        self.assertIn(self.facts["execution_pack_ref"], refs)

    def test_raw_asserted_flags_without_authority_reader_are_insufficient(self) -> None:
        request = deepcopy(self.request)
        request["current"] = True
        result = resolve_standard_read_set(
            self.project, self.ads, request,
            authority_reader=None,
            revision_probe=lambda _root: PIN,
            authority_reader_scope="TEST_FIXTURE",
        )
        self.assertIn("CURRENT_AUTHORITY_UNVERIFIED", {b["code"] for b in result["blockers"]})


if __name__ == "__main__":
    unittest.main()