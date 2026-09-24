from __future__ import annotations

import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"

SUPPORTED_TYPES = {"object", "array", "string", "integer", "boolean", "null"}
SUPPORTED_KEYWORDS = {
    "$schema",
    "$id",
    "title",
    "description",
    "type",
    "required",
    "properties",
    "additionalProperties",
    "enum",
    "const",
    "pattern",
    "minLength",
    "minItems",
    "items",
    "allOf",
    "if",
    "then",
    "else",
}


def load_schema(name: str) -> dict:
    with (SCHEMA_DIR / name).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def assert_supported_schema(schema: dict, path: str = "$") -> None:
    """Fail closed if a machine contract drifts beyond our dependency-free subset."""
    if not isinstance(schema, dict):
        raise ValueError(f"{path}: schema node must be an object")

    unknown = sorted(set(schema) - SUPPORTED_KEYWORDS)
    if unknown:
        raise ValueError(f"{path}: unsupported schema keyword(s): {', '.join(unknown)}")

    schema_type = schema.get("type")
    if schema_type is not None:
        types = schema_type if isinstance(schema_type, list) else [schema_type]
        if not types or not all(isinstance(item, str) and item in SUPPORTED_TYPES for item in types):
            raise ValueError(f"{path}: unsupported schema type declaration: {schema_type!r}")

    if "required" in schema:
        required = schema["required"]
        if not isinstance(required, list) or not all(isinstance(item, str) and item for item in required):
            raise ValueError(f"{path}: required must be a list of non-empty strings")

    if "properties" in schema:
        properties = schema["properties"]
        if not isinstance(properties, dict):
            raise ValueError(f"{path}: properties must be an object")
        for key, child in properties.items():
            if not isinstance(key, str) or not key:
                raise ValueError(f"{path}: property names must be non-empty strings")
            assert_supported_schema(child, f"{path}.properties.{key}")

    if "additionalProperties" in schema and not isinstance(schema["additionalProperties"], bool):
        raise ValueError(f"{path}: only boolean additionalProperties is supported")

    if "items" in schema:
        assert_supported_schema(schema["items"], f"{path}.items")

    if "allOf" in schema:
        all_of = schema["allOf"]
        if not isinstance(all_of, list) or not all_of:
            raise ValueError(f"{path}: allOf must be a non-empty list")
        for index, child in enumerate(all_of):
            assert_supported_schema(child, f"{path}.allOf[{index}]")

    for keyword in ("if", "then", "else"):
        if keyword in schema:
            assert_supported_schema(schema[keyword], f"{path}.{keyword}")


def validate_subset(value, schema: dict, path: str = "$") -> list[str]:
    """Validate exactly the supported JSON-Schema subset used by this repository."""
    errors: list[str] = []
    schema_type = schema.get("type")
    if schema_type is not None:
        allowed = schema_type if isinstance(schema_type, list) else [schema_type]
        matches = False
        type_checks = {
            "object": lambda item: isinstance(item, dict),
            "array": lambda item: isinstance(item, list),
            "string": lambda item: isinstance(item, str),
            "integer": lambda item: isinstance(item, int) and not isinstance(item, bool),
            "boolean": lambda item: isinstance(item, bool),
            "null": lambda item: item is None,
        }
        for expected in allowed:
            check = type_checks.get(expected)
            if check is None:
                return [f"{path}: unsupported schema type {expected!r}"]
            matches = matches or check(value)
        if not matches:
            return [f"{path}: expected type {allowed}, got {type(value).__name__}"]

    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: expected const {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value {value!r} not in enum")

    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append(f"{path}: string shorter than minLength")
        if "pattern" in schema and not re.fullmatch(schema["pattern"], value):
            errors.append(f"{path}: string does not match pattern {schema['pattern']!r}")

    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append(f"{path}: array shorter than minItems")
        if "items" in schema:
            for index, item in enumerate(value):
                errors.extend(validate_subset(item, schema["items"], f"{path}[{index}]"))

    if isinstance(value, dict):
        for required in schema.get("required", []):
            if required not in value:
                errors.append(f"{path}: missing required property {required!r}")
        properties = schema.get("properties", {})
        for key, item in value.items():
            if key in properties:
                errors.extend(validate_subset(item, properties[key], f"{path}.{key}"))
            elif schema.get("additionalProperties") is False:
                errors.append(f"{path}: unexpected property {key!r}")

    for index, child in enumerate(schema.get("allOf", [])):
        errors.extend(validate_subset(value, child, f"{path}.allOf[{index}]"))

    if "if" in schema:
        condition_matches = not validate_subset(value, schema["if"], path)
        if condition_matches and "then" in schema:
            errors.extend(validate_subset(value, schema["then"], path))
        if not condition_matches and "else" in schema:
            errors.extend(validate_subset(value, schema["else"], path))

    return errors


class ProtocolSchemaTests(unittest.TestCase):
    def test_schema_documents_parse_and_use_only_supported_subset(self) -> None:
        for path in sorted(SCHEMA_DIR.glob("*.schema.json")):
            with self.subTest(schema=path.name):
                schema = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(schema.get("$schema"), "https://json-schema.org/draft/2020-12/schema")
                self.assertEqual(schema.get("type"), "object")
                self.assertTrue(schema.get("required"))
                assert_supported_schema(schema)

    def test_schema_subset_fails_closed(self) -> None:
        with self.assertRaises(ValueError):
            assert_supported_schema({"type": "string", "oneOf": []})
        with self.assertRaises(ValueError):
            assert_supported_schema({"type": "strnig"})
        self.assertTrue(validate_subset("x", {"type": "strnig"}))

    def _review_decision(self, **overrides):
        value = {
            "schema": "ai-dev/event-v2",
            "event": "REVIEW_DECISION",
            "actor_role": "merge-controller",
            "operator_kind": "chatgpt-web",
            "operator_id": "chatgpt-web:web-a",
            "session_ref": "merge-control-a",
            "transport_actor": "github:kaicreator-mm",
            "task": "#15",
            "pr": "#19",
            "sha": "f31c9dfb285cb96126ec1babb96d63c5fae6b0d2",
            "review_policy": "recommended",
            "decision": "skipped",
            "status": "NOT_RUN",
            "reason": "optional review explicitly skipped after risk decision",
            "next_state": "merge-ready",
        }
        value.update(overrides)
        return value

    def test_review_decision_contract_valid_combinations(self) -> None:
        schema = load_schema("agent-event-v2.schema.json")
        valid_cases = [
            self._review_decision(review_policy="required", decision="perform", status="NOT_RUN", next_state="review-ready"),
            self._review_decision(review_policy="recommended", decision="perform", status="NOT_RUN", next_state="review-ready"),
            self._review_decision(review_policy="recommended", decision="skipped", status="NOT_RUN", next_state="merge-ready"),
            self._review_decision(review_policy="not-required", decision="not-applicable", status="NOT_APPLICABLE", next_state="merge-ready"),
        ]
        for value in valid_cases:
            with self.subTest(policy=value["review_policy"], decision=value["decision"]):
                self.assertEqual(validate_subset(value, schema), [])

    def test_review_decision_contract_policy_only_forms(self) -> None:
        schema = load_schema("agent-event-v2.schema.json")
        valid_cases = [
            ("required", "NOT_RUN", "ready"),
            ("recommended", "NOT_RUN", "ready"),
            ("not-required", "NOT_APPLICABLE", "merge-ready"),
        ]
        for review_policy, status, next_state in valid_cases:
            value = self._review_decision(
                review_policy=review_policy,
                status=status,
                next_state=next_state,
                reason="record Review Policy without choosing an optional execution decision",
            )
            del value["decision"]
            with self.subTest(policy=review_policy):
                self.assertEqual(validate_subset(value, schema), [])

        required_direct_merge = self._review_decision(
            review_policy="required",
            status="NOT_RUN",
            next_state="merge-ready",
            reason="policy record must not bypass required Independent Review",
        )
        del required_direct_merge["decision"]
        self.assertTrue(validate_subset(required_direct_merge, schema), required_direct_merge)

        recommended_direct_merge = self._review_decision(
            review_policy="recommended",
            status="NOT_RUN",
            next_state="merge-ready",
            reason="recommended review requires explicit skipped decision before merge-ready",
        )
        del recommended_direct_merge["decision"]
        self.assertTrue(validate_subset(recommended_direct_merge, schema), recommended_direct_merge)

    def test_review_decision_contract_rejects_gate_bypass_combinations(self) -> None:
        schema = load_schema("agent-event-v2.schema.json")
        invalid_cases = [
            self._review_decision(review_policy="required", decision="skipped", status="NOT_RUN", next_state="merge-ready"),
            self._review_decision(review_policy="required", decision="perform", status="NOT_RUN", next_state="merge-ready"),
            self._review_decision(review_policy="recommended", decision="not-applicable", status="NOT_APPLICABLE", next_state="merge-ready"),
            self._review_decision(review_policy="recommended", decision="skipped", status="PASS", next_state="merge-ready"),
            self._review_decision(review_policy="not-required", decision="perform", status="NOT_RUN", next_state="review-ready"),
        ]
        for value in invalid_cases:
            with self.subTest(policy=value["review_policy"], decision=value["decision"], state=value["next_state"]):
                self.assertTrue(validate_subset(value, schema), value)

    def test_review_result_contract(self) -> None:
        schema = load_schema("agent-event-v2.schema.json")
        valid = {
            "schema": "ai-dev/event-v2",
            "event": "REVIEW_RESULT",
            "actor_role": "reviewer",
            "operator_kind": "chatgpt-web",
            "operator_id": "chatgpt-web:web-b",
            "session_ref": "review-session-b",
            "transport_actor": "github:kaicreator-mm",
            "task": "#14",
            "pr": "#18",
            "sha": "d7273fc7f1300c1fda5d36e38aed641865b0addc",
            "review_policy": "required",
            "status": "PASS",
            "next_state": "merge-ready",
        }
        self.assertEqual(validate_subset(valid, schema), [])

        missing_sha = dict(valid)
        del missing_sha["sha"]
        self.assertTrue(any("sha" in error for error in validate_subset(missing_sha, schema)))

        missing_policy = dict(valid)
        del missing_policy["review_policy"]
        self.assertTrue(any("review_policy" in error for error in validate_subset(missing_policy, schema)))

        invalid_state = dict(valid, next_state="green-ish")
        self.assertTrue(any("next_state" in error for error in validate_subset(invalid_state, schema)))

    def test_validation_request_contract(self) -> None:
        schema = load_schema("agent-event-v2.schema.json")
        malformed = {
            "schema": "ai-dev/event-v2",
            "event": "VALIDATION_REQUEST",
            "actor_role": "reviewer",
            "operator_kind": "chatgpt-web",
            "operator_id": "chatgpt-web:web-b",
            "sha": "d7273fc7f1300c1fda5d36e38aed641865b0addc",
            "status": "BLOCKED",
            "next_state": "validation-needed",
        }
        errors = validate_subset(malformed, schema)
        for field in ("gate", "environment", "reason"):
            self.assertTrue(any(field in error for error in errors), errors)

    def test_validation_result_contract(self) -> None:
        schema = load_schema("agent-event-v2.schema.json")
        malformed = {
            "schema": "ai-dev/event-v2",
            "event": "VALIDATION_RESULT",
            "actor_role": "validator",
            "operator_kind": "codex",
            "operator_id": "codex:windows-01",
            "sha": "d7273fc7f1300c1fda5d36e38aed641865b0addc",
            "status": "PASS",
            "gate": "platform",
            "environment": "windows",
            "next_state": "review-ready",
        }
        errors = validate_subset(malformed, schema)
        for field in ("command", "exit_code", "evidence"):
            self.assertTrue(any(field in error for error in errors), errors)

    def test_merge_result_contract(self) -> None:
        schema = load_schema("agent-event-v2.schema.json")
        malformed = {
            "schema": "ai-dev/event-v2",
            "event": "MERGE_RESULT",
            "actor_role": "merge-controller",
            "operator_kind": "chatgpt-web",
            "operator_id": "chatgpt-web:web-a",
            "sha": "d7273fc7f1300c1fda5d36e38aed641865b0addc",
            "status": "PASS",
            "next_state": "done",
        }
        errors = validate_subset(malformed, schema)
        self.assertTrue(any("target" in error for error in errors), errors)

    def test_task_contract_examples(self) -> None:
        schema = load_schema("task-contract.schema.json")
        valid = {
            "task_id": "T02",
            "goal": "Machine-verifiable standard contracts",
            "integration_target": "version/v3.2.0",
            "baseline_sha": "db1c960459a1eb896cae6c101c0c57347fee5b96",
            "review_policy": "required",
            "required_gates": ["verify-standard"],
            "acceptance": ["manifest-declared asset deletion fails"],
            "dependencies": [],
        }
        self.assertEqual(validate_subset(valid, schema), [])
        invalid = dict(valid, review_policy="sometimes", required_gates=[])
        errors = validate_subset(invalid, schema)
        self.assertTrue(any("review_policy" in error for error in errors), errors)
        self.assertTrue(any("required_gates" in error for error in errors), errors)

    def test_validation_report_examples(self) -> None:
        schema = load_schema("validation-report.schema.json")
        sha = "d7273fc7f1300c1fda5d36e38aed641865b0addc"
        valid = {
            "repository": "kaicreator-mm/ai-development-standard",
            "tested_sha": sha,
            "requested_sha": sha,
            "actual_checked_out_sha": sha,
            "working_tree_clean": True,
            "source_modifications_after_validation": False,
            "provider_state": "AVAILABLE",
            "execution_host_role": "github-actions",
            "platform": "ubuntu-latest",
            "runtime_toolchain": "Python 3.13",
            "validation_profile": "minimal-ci",
            "command": "python scripts/verify_standard.py",
            "exit_code": 0,
            "state": "PASS",
        }
        self.assertEqual(validate_subset(valid, schema), [])
        invalid = dict(valid, tested_sha="main", state="GREEN")
        errors = validate_subset(invalid, schema)
        self.assertTrue(any("tested_sha" in error for error in errors), errors)
        self.assertTrue(any("state" in error for error in errors), errors)


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(ProtocolSchemaTests)
    )
    raise SystemExit(0 if result.wasSuccessful() else 1)
